"""
Helper functions for working with the database.
"""

import typing
from typing import Any, Optional

import database.models as db
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal
from platformics.security.authorization import CerbosAction, get_resource_query
from sqlalchemy import ColumnElement, func
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
    action: CerbosAction,
    query: Select,
    sa_model: Base,
    whereClause: dict[str, Any],
    depth: int,
) -> Select:
    """
    Convert a query with a where clause to a SQLAlchemy query.
    """
    if not whereClause:
        return query
    for k, v in whereClause.items():
        for comparator, value in v.items():
            # TODO it would be nicer if we could have the WhereClause classes inherit from a BaseWhereClause
            # so that these type checks could be smarter, but TypedDict doesn't support type checks like that
            if isinstance(value, dict):
                mapper = inspect(sa_model)
                relationship = mapper.relationships[k]  # type: ignore
                related_cls = relationship.mapper.entity
                subquery = get_db_query(
                    related_cls, action, cerbos_client, principal, v, depth
                ).subquery()  # type: ignore
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
    action: CerbosAction,
    cerbos_client: CerbosClient,
    principal: Principal,
    where: dict[str, Any],
    depth: Optional[int] = None,
) -> Select:
    """
    Given a model class and a where clause, return a SQLAlchemy query that is limited
    based on the where clause, and which entities the user has access to.
    """
    if not depth:
        depth = 0
    depth += 1
    # TODO, this may need to be adjusted, 5 just seemed like a reasonable starting point
    if depth >= 5:
        raise Exception("Max filter depth exceeded")
    query = get_resource_query(principal, cerbos_client, action, model_cls)
    query = convert_where_clauses_to_sql(
        principal, cerbos_client, action, query, model_cls, where, depth  # type: ignore
    )
    return query


async def get_db_rows(
    model_cls: type[E],  # type: ignore
    session: AsyncSession,
    cerbos_client: CerbosClient,
    principal: Principal,
    where: Any,
    order_by: Optional[list[tuple[ColumnElement[Any], ...]]] = [],
    action: CerbosAction = CerbosAction.VIEW,
) -> typing.Sequence[E]:
    """
    Retrieve rows from the database, filtered by the where clause and the user's permissions.
    """
    query = get_db_query(model_cls, action, cerbos_client, principal, where)
    if order_by:
        query = query.order_by(*order_by)  # type: ignore
    result = await session.execute(query)
    return result.scalars().all()

# TODO: how to handle nesting?

def convert_where_and_aggregate_clauses_to_sql(
    principal: Principal,
    cerbos_client: CerbosClient,
    action: CerbosAction,
    query: Select,
    sa_model: Base,
    whereClause: dict[str, Any],
    depth: int,
) -> Select:
    """
    Convert a query with a where clause to a SQLAlchemy query.
    """
    if not whereClause:
        return query
    for k, v in whereClause.items():
        for comparator, value in v.items():
            # TODO it would be nicer if we could have the WhereClause classes inherit from a BaseWhereClause
            # so that these type checks could be smarter, but TypedDict doesn't support type checks like that
            if isinstance(value, dict):
                mapper = inspect(sa_model)
                relationship = mapper.relationships[k]  # type: ignore
                related_cls = relationship.mapper.entity
                subquery = get_db_query(
                    related_cls, action, cerbos_client, principal, v, depth
                ).subquery()  # type: ignore
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

# TODO: move this somewhere else
aggregate_functions = {
    "avg": func.avg,
    "sum": func.sum,
    "min": func.min,
    "max": func.max,
    "stddev": func.stddev,
    "variance": func.variance,
}

def get_aggregate_db_query(
    model_cls: type[E],
    action: CerbosAction,
    cerbos_client: CerbosClient,
    principal: Principal,
    where: dict[str, Any],
    aggregate: Any,
    depth: Optional[int] = None,
) -> Select:
    """
    Given a model class and a where clause, return a SQLAlchemy query that is limited
    based on the where clause, and which entities the user has access to.
    """
    if not depth:
        depth = 0
    depth += 1
    # TODO, this may need to be adjusted, 5 just seemed like a reasonable starting point
    if depth >= 5:
        raise Exception("Max filter depth exceeded")
    query = get_resource_query(principal, cerbos_client, action, model_cls)
    # deconstruct the aggregate dict and build mappings for the query
    aggregate_query_fields = []
    for aggregator_name, value in aggregate.items():
        if value:
            if aggregator_name == "count":
                aggregate_query_fields.append(func.count(model_cls.id).label("count"))
            else:
                agg_fn = aggregate_functions[aggregator_name]
                for col, col_value in value.items():
                    if col_value:
                        aggregate_query_fields.append(agg_fn(getattr(model_cls, col)).label(f"{aggregator_name}_{col}"))
    query = query.with_only_columns(*aggregate_query_fields)
    query = convert_where_and_aggregate_clauses_to_sql(
        principal, cerbos_client, action, query, model_cls, where, depth  # type: ignore
    )
    return query


async def get_aggregate_db_rows(
    model_cls: type[E],  # type: ignore
    session: AsyncSession,
    cerbos_client: CerbosClient,
    principal: Principal,
    where: Any,
    aggregate: Any,
    order_by: Optional[list[tuple[ColumnElement[Any], ...]]] = [],
    action: CerbosAction = CerbosAction.VIEW,
) -> typing.Sequence[E]:
    """
    Retrieve rows from the database, filtered by the where clause and the user's permissions.
    """
    query = get_aggregate_db_query(model_cls, action, cerbos_client, principal, where, aggregate)
    if order_by:
        query = query.order_by(*order_by)  # type: ignore
    print(f"query: {query}")
    result = await session.execute(query)
    result = result.mappings().one()
    return result
