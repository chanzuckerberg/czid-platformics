from collections import defaultdict
from typing import Any, Dict, List, Mapping, Tuple, Optional

from sqlalchemy import tuple_
from sqlalchemy.orm import RelationshipProperty
from strawberry.dataloader import DataLoader
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, ResourceDesc
from thirdparty.cerbos_sqlalchemy.query import get_query

from fastapi import Depends

import typing

import database.models as db
import strawberry
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, ResourceDesc
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from thirdparty.cerbos_sqlalchemy.query import get_query
import uuid

from api.core.deps import (
    require_auth_principal,
    get_cerbos_client,
    get_db_session,
)
from api.core.strawberry_extensions import DependencyExtension
from sqlalchemy import ColumnExpressionArgument, ColumnElement


async def get_entities(
    model: db.Entity,
    session: AsyncSession,
    cerbos_client: CerbosClient,
    principal: Principal,
    filters: Optional[typing.List[ColumnExpressionArgument]],
    order_by: Optional[typing.List[ColumnElement]],
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

    _loaders: Dict[RelationshipProperty, DataLoader]

    def __init__(
        self, engine, cerbos_client: CerbosClient, principal: Principal
    ) -> None:
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

            async def load_fn(keys: List[Tuple]) -> List[Any]:
                filters = [
                    tuple_(
                        *[remote for _, remote in relationship.local_remote_pairs]
                    ).in_(keys)
                ]
                order_by = []
                if relationship.order_by:
                    order_by = relationship.order_by
                rows = await get_entities(
                    related_model,
                    self.engine.session(),
                    self.cerbos_client,
                    self.principal,
                    filters,
                    order_by,
                )

                def group_by_remote_key(row: Any) -> Tuple:
                    return tuple(
                        [
                            getattr(row, remote.key)
                            for _, remote in relationship.local_remote_pairs
                        ]
                    )

                grouped_keys: Mapping[Tuple, List[Any]] = defaultdict(list)
                for row in rows:
                    grouped_keys[group_by_remote_key(row)].append(row)
                if relationship.uselist:
                    return [grouped_keys[key] for key in keys]
                else:
                    return [
                        grouped_keys[key][0] if grouped_keys[key] else None
                        for key in keys
                    ]

            self._loaders[relationship] = DataLoader(load_fn=load_fn)
            return self._loaders[relationship]


def get_base_loader(entity_model, gql_type):
    @strawberry.field(extensions=[DependencyExtension()])
    async def resolve_entity(
        id: typing.Optional[uuid.UUID] = None,
        session: AsyncSession = Depends(get_db_session, use_cache=False),
        cerbos_client: CerbosClient = Depends(get_cerbos_client),
        principal: Principal = Depends(require_auth_principal),
    ) -> typing.List[gql_type]:
        filters = []
        if id:
            filters.append(entity_model.entity_id == id)
        return await get_entities(
            entity_model, session, cerbos_client, principal, filters, []
        )

    return resolve_entity
