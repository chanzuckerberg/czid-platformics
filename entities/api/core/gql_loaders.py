import uuid
import typing
import strawberry
import database.models as db
from collections import defaultdict
from typing import Any, Mapping, Tuple, Optional
from sqlalchemy import ColumnElement, ColumnExpressionArgument, tuple_
from sqlalchemy.orm import RelationshipProperty
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.dataloader import DataLoader
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


# Returns function that helps create entities
async def create_entity(
    principal: Principal = Depends(require_auth_principal),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    session: AsyncSession = Depends(get_db_session, use_cache=False),
):
    async def create(entity_model, gql_type, params):
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

    return create


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
