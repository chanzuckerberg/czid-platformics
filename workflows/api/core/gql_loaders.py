"""
Helper functions to map data from the database to strawberry
"""

import typing
import uuid
from collections import defaultdict
from typing import Any, Mapping, Optional, Tuple

import database.models as db
import strawberry
from platformics.api.core.deps import get_cerbos_client, get_db_session, require_auth_principal
from platformics.api.core.strawberry_extensions import DependencyExtension
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource, ResourceDesc
from platformics.database.connect import AsyncDB
from fastapi import Depends
from sqlalchemy import ColumnElement, ColumnExpressionArgument, tuple_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import RelationshipProperty
from strawberry.arguments import StrawberryArgument
from strawberry.dataloader import DataLoader
from platformics.thirdparty.cerbos_sqlalchemy.query import get_query

CERBOS_ACTION_VIEW = "view"
CERBOS_ACTION_CREATE = "create"
CERBOS_ACTION_UPDATE = "update"

E = typing.TypeVar("E", bound=db.Base)
T = typing.TypeVar("T")


def get_authz_map(
    model_cls: type[db.Base],
) -> tuple[dict, list]:
    authz_map = {
        "request.resource.attr.owner_user_id": db.WorkflowRun.owner_user_id,
        "request.resource.attr.collection_id": db.WorkflowRun.collection_id,
    }

    if model_cls == db.WorkflowRun:
        return authz_map, []
    if model_cls in [db.WorkflowRunStep, db.WorkflowRunEntityInput]:
        return authz_map, [(db.Run, model_cls.run_id == db.Run.id)]  # type: ignore
    # The rest don't apply authorization rules, they just require authentication.
    return {}, []


async def db_rows(
    model_cls: type[db.Base],
    session: AsyncSession,
    cerbos_client: CerbosClient,
    principal: Principal,
    filters: Optional[list[ColumnExpressionArgument]] = [],
    order_by: Optional[list[tuple[ColumnElement[Any], ...]]] = [],
) -> typing.Sequence[db.Base]:
    rd = ResourceDesc(model_cls.__tablename__)
    plan = cerbos_client.plan_resources(CERBOS_ACTION_VIEW, principal, rd)
    authz_map, extra_models = get_authz_map(model_cls)
    query = get_query(
        plan,
        model_cls,  # type: ignore
        authz_map,  # type: ignore
        extra_models,  # type: ignore
    )
    if filters:
        query = query.filter(*filters)  # type: ignore
    if order_by:
        query = query.order_by(*order_by)  # type: ignore
    result = await session.execute(query)
    return result.scalars().all()


class WorkflowLoader:
    """
    Creates DataLoader instances on-the-fly for SQLAlchemy relationships
    """

    _loaders: dict[RelationshipProperty, DataLoader]

    def __init__(self, engine: AsyncDB, cerbos_client: CerbosClient, principal: Principal) -> None:
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

            load_method = db_rows  # type: ignore

            async def load_fn(keys: list[Tuple]) -> typing.Sequence[Any]:
                if not relationship.local_remote_pairs:
                    raise Exception("invalid relationship")
                filters = [tuple_(*[remote for _, remote in relationship.local_remote_pairs]).in_(keys)]
                order_by: list[tuple[ColumnElement[Any], ...]] = []
                if relationship.order_by:
                    order_by = [relationship.order_by]
                db_session = self.engine.session()
                rows = await load_method(
                    related_model,  # type: ignore
                    db_session,
                    self.cerbos_client,
                    self.principal,
                    filters,  # type: ignore
                    order_by,
                )
                await db_session.close()

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


def get_base_loader(sql_model: type[E], gql_type: type[T]) -> typing.Sequence[T]:
    @strawberry.field(extensions=[DependencyExtension()])
    async def resolve_entity(
        id: typing.Optional[uuid.UUID] = None,
        session: AsyncSession = Depends(get_db_session, use_cache=False),
        cerbos_client: CerbosClient = Depends(get_cerbos_client),
        principal: Principal = Depends(require_auth_principal),
    ) -> typing.Sequence[E]:
        filters = []
        if id:
            # FIXME: error: "type[E]" has no attribute "id"
            filters.append(sql_model.id == id)  # type: ignore
        return await db_rows(sql_model, session, cerbos_client, principal, filters, [])  # type: ignore

    return typing.cast(typing.Sequence[T], resolve_entity)


def get_base_creator(sql_model: type[db.Base], gql_type: type[T]) -> T:
    @strawberry.mutation(extensions=[DependencyExtension()])
    async def create(
        principal: Principal = Depends(require_auth_principal),
        cerbos_client: CerbosClient = Depends(get_cerbos_client),
        session: AsyncSession = Depends(get_db_session, use_cache=False),
        **kwargs: typing.Any,
    ) -> db.Base:
        params = {key: kwargs[key] for key in kwargs if key != "kwargs"}

        # Validate that user can create entity in this collection
        attr = {"collection_id": params.get("collection_id")}
        resource = Resource(id="NEW_ID", kind=sql_model.__tablename__, attr=attr)
        if not cerbos_client.is_allowed("create", principal, resource):
            raise Exception("Unauthorized: Cannot create entity in this collection")

        # TODO: User must have permissions to the sample

        # Save to DB
        params["owner_user_id"] = int(principal.id)
        new_entity = sql_model(**params)
        session.add(new_entity)
        await session.commit()

        return new_entity

    create.arguments = generate_strawberry_arguments(CERBOS_ACTION_CREATE, sql_model, gql_type)
    return typing.cast(T, create)


def get_base_updater(sql_model: type[db.Base], gql_type: type[T]) -> T:
    @strawberry.field(extensions=[DependencyExtension()])
    async def update(
        entity_id: uuid.UUID,
        session: AsyncSession = Depends(get_db_session, use_cache=False),
        cerbos_client: CerbosClient = Depends(get_cerbos_client),
        principal: Principal = Depends(require_auth_principal),
        **kwargs: typing.Any,
    ) -> db.Base:
        params = {key: kwargs[key] for key in kwargs if key != "kwargs"}

        # Fetch entity for update, if we have access to it
        # FIXME: error: "type[Base]" has no attribute "id"
        filters = [sql_model.id == entity_id]  # type: ignore
        entities = await db_rows(sql_model, session, cerbos_client, principal, filters, [])  # type: ignore
        if len(entities) != 1:
            raise Exception("Unauthorized: Cannot retrieve entity")
        entity = entities[0]

        # Validate that user can update this entity. For now, this is redundant with db_rows() above,
        # but it's possible we'll want "update" actions to require additional permissions in the future.
        # FIXME: error: "Base" has no attribute "collection_id"
        attr = {"collection_id": entity.collection_id}  # type: ignore
        # FIXME: error: "Base" has no attribute "id"
        resource = Resource(id=str(entity.id), kind=sql_model.__tablename__, attr=attr)  # type: ignore
        if not cerbos_client.is_allowed(CERBOS_ACTION_UPDATE, principal, resource):
            raise Exception("Unauthorized: Cannot update entity")

        # Update DB
        for key in params:
            if params[key]:
                setattr(entity, key, params[key])
        await session.commit()

        return entity

    update.arguments = generate_strawberry_arguments(CERBOS_ACTION_UPDATE, sql_model, gql_type)

    return typing.cast(T, update)


# Infer Strawberry arguments from SQLAlchemy columns
def generate_strawberry_arguments(
    action: str, sql_model: type[db.Base | db.Base], gql_type: type[T]
) -> list[StrawberryArgument]:
    sql_columns = [column.name for column in sql_model.__table__.columns]

    # Always create an entity within a collection ID so need to specify it
    if action == CERBOS_ACTION_CREATE:
        sql_columns.append("collection_id")

    gql_arguments = []
    for sql_column in sql_columns:
        # Row ID is autogenerated, so don't let user specify it unless updating a field
        if action != CERBOS_ACTION_UPDATE and sql_column == "id":
            continue

        # Get GQL field
        field = gql_type.__strawberry_definition__.get_field(sql_column)  # type: ignore
        if field:
            # When updating an entity, only entity ID is required
            is_optional_field = action == CERBOS_ACTION_UPDATE and field.name != "entity_id"
            default = None if is_optional_field else strawberry.UNSET
            argument = StrawberryArgument(field.name, field.graphql_name, field.type_annotation, default=default)
            gql_arguments.append(argument)

    return gql_arguments
