import typing
import uuid
from collections import defaultdict
from typing import Any, Mapping, Optional, Tuple

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
                                             convert_where_clauses_to_sql,
                                             strawberry_sqlalchemy_mapper)
from platformics.api.core.strawberry_extensions import DependencyExtension
from platformics.database.connect import AsyncDB
from platformics.security.authorization import CerbosAction, get_resource_query
from sqlalchemy import ColumnElement, ColumnExpressionArgument, tuple_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import RelationshipProperty
from strawberry.arguments import StrawberryArgument
from strawberry.dataloader import DataLoader
from typing_extensions import TypedDict

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")


async def get_db_rows(
    model_cls: type[E],
    session: AsyncSession,
    cerbos_client: CerbosClient,
    principal: Principal,
    where: Any,
    order_by: Optional[list[tuple[ColumnElement[Any], ...]]] = [],
) -> typing.Sequence[E]:
    query = get_resource_query(principal, cerbos_client, CerbosAction.VIEW, model_cls)
    query = convert_where_clauses_to_sql(query, model_cls, where)
    if order_by:
        query = query.order_by(*order_by)  # type: ignore
    result = await session.execute(query)
    return result.scalars().all()
