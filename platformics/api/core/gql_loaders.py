import typing
import json
import uuid
from collections import defaultdict
from typing import Any, Mapping, Optional, Tuple

import database.models as db
import strawberry
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource
from fastapi import Depends
from platformics.api.core.deps import get_cerbos_client, get_db_session, require_auth_principal
from platformics.api.core.strawberry_extensions import DependencyExtension
from platformics.database.connect import AsyncDB
from sqlalchemy import ColumnElement, ColumnExpressionArgument, tuple_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import RelationshipProperty
from strawberry.arguments import StrawberryArgument
from strawberry.dataloader import DataLoader
from platformics.security.authorization import get_resource_query, CerbosAction
from api.core.helpers import get_db_query

E = typing.TypeVar("E", db.File, db.Entity)  # type: ignore
T = typing.TypeVar("T")

class Hashabledict(dict):
    def __hash__(self):
        return hash(frozenset(self))

def make_hashable(whereclause: dict) -> Hashabledict:
    res = {}
    for k, v in whereclause.items():
        if type(v) == dict:
            v = make_hashable(v)
        res[k] = v
    return Hashabledict(res)

async def get_db_rows(
    model_cls: type[E],
    session: AsyncSession,
    cerbos_client: CerbosClient,
    principal: Principal,
    filters: Optional[list[ColumnExpressionArgument]] = [],
    order_by: Optional[list[tuple[ColumnElement[Any], ...]]] = [],
) -> typing.Sequence[E]:
    query = get_resource_query(principal, cerbos_client, CerbosAction.VIEW, model_cls)
    if filters:
        query = query.filter(*filters)  # type: ignore
    if order_by:
        query = query.order_by(*order_by)  # type: ignore
    result = await session.execute(query)
    return result.scalars().all()


class EntityLoader:
    """
    Creates DataLoader instances on-the-fly for SQLAlchemy relationships
    """

    _loaders: dict[RelationshipProperty, DataLoader]

    def __init__(self, engine: AsyncDB, cerbos_client: CerbosClient, principal: Principal) -> None:
        self._loaders = {}
        self.engine = engine
        self.cerbos_client = cerbos_client
        self.principal = principal

    def loader_for(self, relationship: RelationshipProperty, where: Optional[Any] = None) -> DataLoader:
        """
        Retrieve or create a DataLoader for the given relationship
        """
        if not where:
            where = {}
        where_str = make_hashable(where)
        try:
            return self._loaders[(relationship, where_str)]
        except KeyError:
            related_model = relationship.entity.entity

            async def load_fn(keys: list[Any]) -> typing.Sequence[Any]:
                if not relationship.local_remote_pairs:
                    raise Exception("invalid relationship")
                print(f"WHERE IS {where}")
                filters = []
                for _, remote in relationship.local_remote_pairs:
                    filters.append(remote.in_(keys))
                order_by: list[tuple[ColumnElement[Any], ...]] = []
                if relationship.order_by:
                    order_by = [relationship.order_by]
                query = get_db_query(
                    related_model,  # type: ignore
                    CerbosAction.VIEW,
                    self.cerbos_client,
                    self.principal,
                    where
                )
                for item in filters:
                    query = query.where(item)
                db_session = self.engine.session()
                rows = (await db_session.execute(query)).scalars().all()
                await db_session.close()

                def group_by_remote_key(row: Any) -> Tuple:
                    if not relationship.local_remote_pairs:
                        raise Exception("invalid relationship")
                    # TODO -- Technically, SA supports multiple field filters in a relationship! We'll need to handle this case
                    return [getattr(row, remote.key) for _, remote in relationship.local_remote_pairs if remote.key][0]

                grouped_keys: Mapping[Tuple, list[Any]] = defaultdict(list)
                for row in rows:
                    grouped_keys[group_by_remote_key(row)].append(row)
                if relationship.uselist:
                    return [grouped_keys[key] for key in keys]
                else:
                    return [grouped_keys[key][0] if grouped_keys[key] else None for key in keys]

            self._loaders[(relationship, where_str)] = DataLoader(load_fn=load_fn)
            return self._loaders[(relationship, where_str)]


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

        # Save to DB
        params["owner_user_id"] = int(principal.id)
        new_entity = sql_model(**params)
        session.add(new_entity)
        await session.commit()

        return new_entity

    create.arguments = generate_strawberry_arguments(CerbosAction.CREATE, sql_model, gql_type)
    return typing.cast(T, create)


def get_base_updater(sql_model: type[db.Entity], gql_type: type[T]) -> T:  # type: ignore
    @strawberry.field(extensions=[DependencyExtension()])
    async def update(
        entity_id: uuid.UUID,
        session: AsyncSession = Depends(get_db_session, use_cache=False),
        cerbos_client: CerbosClient = Depends(get_cerbos_client),
        principal: Principal = Depends(require_auth_principal),
        **kwargs: typing.Any,
    ) -> db.Entity:  # type: ignore
        params = {key: kwargs[key] for key in kwargs if key != "kwargs"}

        # Fetch entity for update, if we have access to it
        filters = [sql_model.id == entity_id]
        entities = await get_db_rows(sql_model, session, cerbos_client, principal, filters, [])  # type: ignore
        if len(entities) != 1:
            raise Exception("Unauthorized: Cannot retrieve entity")
        entity = entities[0]

        # Validate that user can update this entity. For now, this is redundant with get_db_rows() above,
        # but it's possible we'll want "update" actions to require additional permissions in the future.
        attr = {"collection_id": entity.collection_id}
        resource = Resource(id=str(entity.id), kind=sql_model.__tablename__, attr=attr)
        if not cerbos_client.is_allowed(CerbosAction.UPDATE, principal, resource):
            raise Exception("Unauthorized: Cannot update entity")

        # Update DB
        for key in params:
            if params[key]:
                setattr(entity, key, params[key])
        await session.commit()

        return entity

    update.arguments = generate_strawberry_arguments(CerbosAction.UPDATE, sql_model, gql_type)

    return typing.cast(T, update)


# Infer Strawberry arguments from SQLAlchemy columns
def generate_strawberry_arguments(
    action: str, sql_model: type[db.Entity | db.Base], gql_type: type[T]  # type: ignore
) -> list[StrawberryArgument]:
    sql_columns = [column.name for column in sql_model.__table__.columns]

    # Always create an entity within a collection ID so need to specify it
    if action == CerbosAction.CREATE:
        sql_columns.append("collection_id")

    gql_arguments = []
    for sql_column in sql_columns:
        # Entity ID is autogenerated, so don't let user specify it unless updating a field
        if action != CerbosAction.UPDATE and sql_column == "entity_id":
            continue

        # Get GQL field
        field = gql_type.__strawberry_definition__.get_field(sql_column)  # type: ignore
        if field:
            # When updating an entity, only entity ID is required
            is_optional_field = action == CerbosAction.UPDATE and field.name != "entity_id"
            default = None if is_optional_field else strawberry.UNSET
            argument = StrawberryArgument(field.name, field.graphql_name, field.type_annotation, default=default)
            gql_arguments.append(argument)

    return gql_arguments
