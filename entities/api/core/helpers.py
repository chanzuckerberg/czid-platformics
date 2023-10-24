import typing
from typing import Any, Optional

import database.models as db
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal
from platformics.security.authorization import CerbosAction, get_resource_query
from sqlalchemy import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from platformics.api.core.gql_to_sql import operator_map
from sqlalchemy import inspect, and_
from sqlalchemy.orm import aliased
from platformics.database.models.base import Base
from sqlalchemy.sql import Select

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")


def convert_where_clauses_to_sql(
    principal: Principal,
    cerbos_client: CerbosClient,
    action: str,
    query,
    sa_model: Base,
    whereClause: dict[str, Any],
    depth: int,
) -> Select:
    if not whereClause:
        return query
    for k, v in whereClause.items():
        for comparator, value in v.items():
            # TODO it would be nicer if we could have the WhereClause classes inherit from a BaseWhereClause
            # so that these type checks could be smarter, but TypedDict doesn't support type checks like that
            if isinstance(value, dict):
                mapper = inspect(sa_model)
                relationship = mapper.relationships[k]
                related_cls = relationship.mapper.entity
                subquery = get_db_query(related_cls, action, cerbos_client, principal, v, depth).subquery()
                query_alias = aliased(related_cls, subquery)
                joincondition_a = [
                    (getattr(sa_model, local.key) == getattr(query_alias, remote.key))
                    for local, remote in relationship.local_remote_pairs
                ]
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
    where: dict[str, Any],
    depth: Optional[int] = None,
) -> typing.Sequence[E]:
    if not depth:
        depth = 0
    depth += 1
    # TODO, this may need to be adjusted, 5 just seemed like a reasonable starting point
    if depth >= 5:
        raise Exception("Max filter depth exceeded")
    action = CerbosAction.VIEW
    query = get_resource_query(principal, cerbos_client, action, model_cls)
    query = convert_where_clauses_to_sql(principal, cerbos_client, action, query, model_cls, where, depth)
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
