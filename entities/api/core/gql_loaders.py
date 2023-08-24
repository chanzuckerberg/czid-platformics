import uuid
import typing
import strawberry
import database.models as db
from collections import defaultdict
from typing import Any, Mapping, Tuple, Optional
from sqlalchemy import ColumnElement, ColumnExpressionArgument, tuple_
from sqlalchemy.orm import RelationshipProperty
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.type import StrawberryType
from strawberry.dataloader import DataLoader
from strawberry.arguments import StrawberryArgument
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource, ResourceDesc
from fastapi import Depends
from database.models import Base
from thirdparty.cerbos_sqlalchemy.query import get_query
from api.core.deps import require_auth_principal, get_cerbos_client, get_db_session
from api.core.strawberry_extensions import DependencyExtension


async def get_entities(
    model: db.Entity,
    session: AsyncSession,
    cerbos_client: CerbosClient,
    principal: Principal,
    filters: Optional[list[ColumnExpressionArgument]] = [],
    order_by: Optional[list[tuple[ColumnElement[Any], ...]]] = [],
):
    rd = ResourceDesc(model.__tablename__)
    plan = cerbos_client.plan_resources("view", principal, rd)
    query = get_query(
        plan,
        model,
        {
            "request.resource.attr.owner_user_id": model.owner_user_id,
            "request.resource.attr.collection_id": model.collection_id,
        },
        [],
    )
    if filters:
        query = query.filter(*filters)
    if order_by:
        query = query.order_by(*order_by)
    result = await session.execute(query)
    return result.scalars().all()


class EntityLoader:
    """
    Creates DataLoader instances on-the-fly for SQLAlchemy relationships
    """

    _loaders: dict[RelationshipProperty, DataLoader]

    def __init__(self, engine, cerbos_client: CerbosClient, principal: Principal) -> None:
        self._loaders = {}
        self.engine = engine
        self.cerbos_client = cerbos_client
        self.principal = principal

    def loader_for(self, relationship: RelationshipProperty) -> DataLoader:
        """
        Retrieve or create a DataLoader for the given relationship
        """
        try:
            return self._loaders[relationship]
        except KeyError:
            related_model = relationship.entity.entity

            async def load_fn(keys: list[Tuple]) -> list[Any]:
                if not relationship.local_remote_pairs:
                    raise Exception("invalid relationship")
                filters = [tuple_(*[remote for _, remote in relationship.local_remote_pairs]).in_(keys)]
                order_by: list[tuple[ColumnElement[Any], ...]] = []
                if relationship.order_by:
                    order_by = [relationship.order_by]
                rows = await get_entities(
                    related_model,
                    self.engine.session(),
                    self.cerbos_client,
                    self.principal,
                    filters,  # type: ignore
                    order_by,
                )

                def group_by_remote_key(row: Any) -> Tuple:
                    if not relationship.local_remote_pairs:
                        raise Exception("invalid relationship")
                    return tuple(
                        [getattr(row, remote.key) for _, remote in relationship.local_remote_pairs if remote.key]
                    )

                grouped_keys: Mapping[Tuple, list[Any]] = defaultdict(list)
                for row in rows:
                    grouped_keys[group_by_remote_key(row)].append(row)
                if relationship.uselist:
                    return [grouped_keys[key] for key in keys]
                else:
                    return [grouped_keys[key][0] if grouped_keys[key] else None for key in keys]

            self._loaders[relationship] = DataLoader(load_fn=load_fn)
            return self._loaders[relationship]


def get_base_loader(entity_model, gql_type):
    @strawberry.field(extensions=[DependencyExtension()])
    async def resolve_entity(
        id: typing.Optional[uuid.UUID] = None,
        session: AsyncSession = Depends(get_db_session, use_cache=False),
        cerbos_client: CerbosClient = Depends(get_cerbos_client),
        principal: Principal = Depends(require_auth_principal),
    ) -> list[Base]:
        filters = []
        if id:
            filters.append(entity_model.entity_id == id)
        return await get_entities(entity_model, session, cerbos_client, principal, filters, [])

    return resolve_entity


def get_base_creator(entity_model, gql_type):
    @strawberry.mutation(extensions=[DependencyExtension()])
    async def create(
        principal: Principal = Depends(require_auth_principal),
        cerbos_client: CerbosClient = Depends(get_cerbos_client),
        session: AsyncSession = Depends(get_db_session, use_cache=False),
        **kwargs: typing.Any,
    ) -> StrawberryType:
        params = {key: kwargs[key] for key in kwargs if key != "kwargs"}

        # Validate that user can create entity in this collection
        attr = {"collection_id": params.get("collection_id")}
        resource = Resource(id="NEW_ID", kind=entity_model.__tablename__, attr=attr)
        if not cerbos_client.is_allowed("create", principal, resource):
            raise Exception("Unauthorized")

        # TODO: User must have permissions to the sample

        # Save to DB
        params["owner_user_id"] = int(principal.id)
        new_entity = entity_model(**params)
        session.add(new_entity)
        await session.commit()

        # Return GQL object to client (FIXME: is there a better way to convert `new_entity` to `gql_type`?)
        params = {
            **params,
            "id": new_entity.entity_id,
            "type": new_entity.type,
            "producing_run_id": new_entity.producing_run_id,
            "entity_id": new_entity.entity_id,
        }
        return gql_type(**params)

    # Which fields we want to expose to the GQL endpoint
    fields = ["collection_id"]
    for column in entity_model.__table__.columns:
        if not column.primary_key:  # entity_id is autogenerated
            fields.append(column.name)

    # Infer Strawberry arguments from SQLAlchemy columns
    arguments = []
    for f in fields:
        field = gql_type._type_definition.get_field(f)
        if field:
            argument = StrawberryArgument(field.name, field.graphql_name, field.type_annotation)
            arguments.append(argument)

    create.arguments = arguments
    return create

def get_base_updater(sql_model, gql_type):
    @strawberry.field(extensions=[DependencyExtension()])
    async def update(
        entity_id: uuid.UUID,
        session: AsyncSession = Depends(get_db_session, use_cache=False),
        cerbos_client: CerbosClient = Depends(get_cerbos_client),
        principal: Principal = Depends(require_auth_principal),
        **kwargs: typing.Any
    ) -> list[Base]:
        params = {key: kwargs[key] for key in kwargs if key != "kwargs"}

        # Fetch entity for update, if we have access to it
        filters = [sql_model.entity_id == entity_id]
        entities = await get_entities(sql_model, session, cerbos_client, principal, filters, [])
        if len(entities) != 1:
            raise Exception("Unauthorized: Cannot retrieve entity")
        entity = entities[0]

        # Validate that user can update this entity. For now, this is redundant with get_entities() above,
        # but it's possible we'll want "update" actions to require additional permissions in the future.
        resource = Resource(id=entity.id, kind=sql_model.__tablename__, attr={"collection_id": entity.collection_id})
        if not cerbos_client.is_allowed("update", principal, resource):
            raise Exception("Unauthorized: Cannot update entity")

        # Update DB
        for key in params:
            if params[key]:
                setattr(entity, key, params[key])
        await session.commit()

        return entity

    # Infer Strawberry arguments from SQLAlchemy columns
    sql_columns = [column.name for column in sql_model.__table__.columns]
    gql_arguments = []
    for sql_column in sql_columns:
        field = gql_type._type_definition.get_field(sql_column)
        if field:
            argument = StrawberryArgument(field.name, field.graphql_name, field.type_annotation, default=None)
            gql_arguments.append(argument)

    update.arguments = gql_arguments

    return update
