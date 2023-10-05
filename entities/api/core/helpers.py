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
from platformics.api.core.gql_to_sql import operator_map
from sqlalchemy import inspect, and_
from sqlalchemy.orm import aliased

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

def convert_where_clauses_to_sql(principal, cerbos_client, action, query, sa_model, whereClause):
    if not whereClause:
        return query
    for k, v in whereClause.items():
        for comparator, value in v.items():
            if comparator not in operator_map:
                mapper = inspect(sa_model)
                relationship = mapper.relationships[k]
                related_cls = relationship.mapper.entity
                subquery = get_db_query(related_cls, action, cerbos_client, principal, v).subquery()
                query_alias = aliased(related_cls, subquery)
                joincondition_a = [(getattr(sa_model, local.key) == getattr(query_alias, remote.key)) for local, remote in relationship.local_remote_pairs]
                query = query.join(query_alias, and_(*joincondition_a))
                continue
            sa_comparator = operator_map[comparator]
            if sa_comparator == "IS_NULL":
                query = query.filter(getattr(sa_model, k).is_(None))
            else:
                query = query.filter(getattr(getattr(sa_model, k), sa_comparator)(value))
    return query



def get_db_query(
    model_cls: type[E],
    action: str,
    cerbos_client: CerbosClient,
    principal: Principal,
    where: Any,
) -> typing.Sequence[E]:
    action = CerbosAction.VIEW
    query = get_resource_query(principal, cerbos_client, action, model_cls)
    query = convert_where_clauses_to_sql(principal, cerbos_client, action, query, model_cls, where)
    return query

async def get_db_rows(
    model_cls: type[E],
    session: AsyncSession,
    cerbos_client: CerbosClient,
    principal: Principal,
    where: Any,
    order_by: Optional[list[tuple[ColumnElement[Any], ...]]] = [],
) -> typing.Sequence[E]:
    action = CerbosAction.VIEW
    query = get_db_query(model_cls, action, cerbos_client, principal, where)

    result = await session.execute(query)
    return result.scalars().all()
