import typing
import uuid
from collections import defaultdict
from typing import Any, Mapping, Optional, Tuple, TypedDict

import database.models as db
import strawberry
from api.types.entities import EntityInterface
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource
from fastapi import Depends
from platformics.api.core.deps import (get_cerbos_client, get_db_session,
                                       require_auth_principal)
from platformics.api.core.gql_to_sql import (EnumComparators, IntComparators,
                                             StrComparators, UUIDComparators,
                                             strawberry_sqlalchemy_mapper)
from platformics.api.core.strawberry_extensions import DependencyExtension
from platformics.database.connect import AsyncDB
from platformics.security.authorization import CerbosAction, get_resource_query
from sqlalchemy import ColumnElement, ColumnExpressionArgument, tuple_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import RelationshipProperty
from strawberry.arguments import StrawberryArgument
from strawberry.dataloader import DataLoader

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")


@strawberry_sqlalchemy_mapper.type(db.Sample)
class Sample(EntityInterface):
    pass


@strawberry.input
class SampleWhereClause(TypedDict):
    id: typing.Optional[UUIDComparators]
    status: typing.Optional[EnumComparators[FileStatus]]
    protocol: typing.Optional[StrComparators]
    namespace: typing.Optional[StrComparators]
    path: typing.Optional[StrComparators]
    compression_type: typing.Optional[StrComparators]
    size: typing.Optional[IntComparators]


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


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_entity(
    id: typing.Optional[uuid.UUID] = None,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: SampleWhereClause = {},
) -> typing.Sequence[Sample]:
    filters = []
    return await get_db_rows(sql_model, session, cerbos_client, principal, filters, [])  # type: ignore
