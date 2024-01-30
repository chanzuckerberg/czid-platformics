"""
Helper functions for working with the database.
"""

import typing
from collections import defaultdict
from typing import Any, Optional, Tuple

import database.models as db
import strcase
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal
from platformics.api.core.gql_to_sql import aggregator_map, operator_map
from platformics.database.models.base import Base
from platformics.security.authorization import CerbosAction, get_resource_query
from sqlalchemy import ColumnElement, and_, distinct, inspect
from sqlalchemy.engine.row import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy.sql import Select

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

def apply_order_by(field, direction, query: Select):
    print(f"applying order by on {field} {direction}")
    match direction.value:
        case "asc":
            query = query.order_by(getattr(query.selected_columns, field).asc())
        case "asc_nulls_first":
            query = query.order_by(getattr(query.selected_columns, field).asc().nullsfirst())
        case "asc_nulls_last":
            query = query.order_by(getattr(query.selected_columns, field).asc().nullslast())
        case "desc":
            query = query.order_by(getattr(query.selected_columns, field).desc())
        case "desc_nulls_first":
            query = query.order_by(getattr(query.selected_columns, field).desc().nullsfirst())
        case "desc_nulls_last":
            query = query.order_by(getattr(query.selected_columns, field).desc().nullslast())
    return query


def convert_where_clauses_to_sql(
    principal: Principal,
    cerbos_client: CerbosClient,
    action: CerbosAction,
    query: Select,
    sa_model: Base,
    whereClause: dict[str, Any],
    order_by: Optional[list[dict[str, Any]]], # FIXME: update this type
    depth: int,
) -> Tuple[Select, list[Any]]:
    """
    Convert a query with a where clause clause to a SQLAlchemy query.
    If order_by is provided, also return a list of order_by fields that need to be applied.
    """
    print(f"=== generate query for {sa_model}")
    if not whereClause and not order_by:
        return query, []
    if not order_by:
        order_by = []
    if not whereClause:
        whereClause = {}

    local_order_by = []  # Fields that we can sort by on the *current* class without having to deal with recursion
    local_where_clauses = {}  # Fields that we can filter on the *current* class without having to deal with recursion
    print(order_by)
    print(whereClause)

    mapper = inspect(sa_model)

    # create a dictionary with the keys as the related field/field names, the values are dict of {order_by: {...}, where: {...}}
    all_joins = defaultdict(dict)
    # {'field': {'mapped_reads': <orderBy.asc: 'asc'>}, 'index': 1}
    # {'field': {'consensus_genome': {'mapped_reads': <orderBy.asc: 'asc'>}}, 'index': 0}
    for item in order_by:
        for col, v in item["field"].items():
            if col in mapper.relationships:
                if not all_joins[col].get("order_by"):
                    all_joins[col]["order_by"] = []
                print(f"order join field {col}")
                all_joins[col]["order_by"].append({"field": v, "index": item["index"]})
            else:
                print(f"order local field {col}")
                local_order_by.append({"field": col, "sort": v, "index": item["index"]})
        # TODO we're not preserving the order of the order_by fields properly, we need
        # to stash that information somewhere so we can re-sort these fields after we're
        # done recursing.
    for col, v in whereClause.items():
        if col in mapper.relationships:
            all_joins[col]["where"] = v
        else:
            local_where_clauses[col] = v
    print("===all_joins===")
    print(all_joins)
    print("===local_order_by===")
    print(local_order_by)

    # handle related fields
    for join_field, join_info in all_joins.items():
        relationship = mapper.relationships[join_field]  # type: ignore
        related_cls = relationship.mapper.entity
        cerbos_query = get_resource_query(principal, cerbos_client, action, related_cls)
        # get the subquery and nested order_by fields that need to be applied to the current query
        subquery, subquery_order_by = convert_where_clauses_to_sql(
            principal, cerbos_client, action, cerbos_query, related_cls, join_info.get("where"), join_info.get("order_by"), depth  # type: ignore
        )
        # if subquery_order_by:
        #     print(f"Got related order by for {related_cls}")
        #     print(subquery_order_by)
        subquery = subquery.subquery()
        query_alias = aliased(related_cls, subquery)
        joincondition_a = [
            (getattr(sa_model, local.key) == getattr(query_alias, remote.key))
            for local, remote in relationship.local_remote_pairs
        ]
        query = query.join(query_alias, and_(*joincondition_a))
        aliased_field_num = 0
        print("===subquery order by====")
        print(subquery_order_by)
        for item in subquery_order_by:
            print(f"item {item}")
            print(order_by)
            aliased_field_name = f"order_field_{aliased_field_num}"
            field_to_match = getattr(subquery.c, item["field"])
            aliased_field_num += 1
            print(f"adding alias {aliased_field_name} to query for {item}")
            print(field_to_match)

            query = query.add_columns(field_to_match.label(aliased_field_name))

            local_order_by.append({"field": aliased_field_name, "sort": item["sort"], "index": item["index"]})
            # local_order_by.append({"field": aliased_field_name, "sort": item["sort"]})

    # handle not-related fields
    print(local_where_clauses)
    for col, v in local_where_clauses.items():
        for comparator, value in v.items():
            sa_comparator = operator_map[comparator]
            if sa_comparator == "IS_NULL":
                query = query.filter(getattr(sa_model, col).is_(None))
            else:
                query = query.filter(getattr(getattr(sa_model, col), sa_comparator)(value))

    # print(f"*** {sa_model} query ***")
    # print(f"{query}")
    return query, local_order_by


def get_db_query(
    model_cls: type[E],
    action: CerbosAction,
    cerbos_client: CerbosClient,
    principal: Principal,
    where: dict[str, Any],
    order_by: Optional[list[dict[str, Any]]] = [],
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
    # create a new order_by type that includes the index of the order_by field
    # this is needed to preserve the order of the order_by fields
    order_by = [{"field": x, "index": i} for i, x in enumerate(order_by)]
    query, order_by = convert_where_clauses_to_sql(
        principal, cerbos_client, action, query, model_cls, where, order_by, depth  # type: ignore
    )
    order_by.sort(key=lambda x: x["index"])
    print(f"final order_by: {order_by}")
    for item in order_by:
        query = apply_order_by(item["field"], item["sort"], query)

    print(query)
    return query


async def get_db_rows(
    model_cls: type[E],  # type: ignore
    session: AsyncSession,
    cerbos_client: CerbosClient,
    principal: Principal,
    where: Any,
    order_by: Optional[list[dict[str, Any]]] = [],
    action: CerbosAction = CerbosAction.VIEW,
) -> typing.Sequence[E]:
    """
    Retrieve rows from the database, filtered by the where clause and the user's permissions.
    """
    query = get_db_query(model_cls, action, cerbos_client, principal, where, order_by)
    result = await session.execute(query)
    return result.scalars().all()


def get_aggregate_db_query(
    model_cls: type[E],
    action: CerbosAction,
    cerbos_client: CerbosClient,
    principal: Principal,
    where: dict[str, Any],
    aggregate: Any,
    group_by: Optional[ColumnElement[Any]] = None,
    depth: Optional[int] = None,
) -> Select:
    """
    Given a model class, a where clause, and an aggregate clause,
    return a SQLAlchemy query that performs the aggregations, with results
    limited based on the where clause, and which entities the user has access to.
    """
    if not depth:
        depth = 0
    depth += 1
    # TODO, this may need to be adjusted, 5 just seemed like a reasonable starting point
    if depth >= 5:
        raise Exception("Max filter depth exceeded")
    query = get_resource_query(principal, cerbos_client, action, model_cls)
    # Deconstruct the aggregate dict and build mappings for the query
    aggregate_query_fields = []
    if group_by is not None:
        aggregate_query_fields.append(group_by)
    for aggregator in aggregate:
        agg_fn = aggregator_map[aggregator.name]
        if aggregator.name == "count":
            # If provided "distinct" or "columns" arguments, use them to construct the count query
            # Otherwise, default to counting the primary key
            col = model_cls.id
            count_fn = agg_fn(model_cls.id)  # type: ignore
            if aggregator.arguments:
                if colname := aggregator.arguments.get("columns"):
                    col = getattr(model_cls, colname)
                if aggregator.arguments.get("distinct"):
                    count_fn = agg_fn(distinct(col))  # type: ignore
            aggregate_query_fields.append(count_fn.label("count"))
        else:
            for col in aggregator.selections:
                col_name = strcase.to_snake(col.name)
                aggregate_query_fields.append(
                    agg_fn(getattr(model_cls, col_name)).label(f"{aggregator.name}_{col_name}")  # type: ignore
                )
    query = query.with_only_columns(*aggregate_query_fields)
    query, _order_by = convert_where_clauses_to_sql(
        principal, cerbos_client, action, query, model_cls, where, [], depth  # type: ignore
    )
    query = query.group_by(group_by)
    return query


async def get_aggregate_db_rows(
    model_cls: type[E],  # type: ignore
    session: AsyncSession,
    cerbos_client: CerbosClient,
    principal: Principal,
    where: Any,
    aggregate: Any,
    order_by: Optional[list[tuple[ColumnElement[Any], ...]]] = [],
    group_by: Optional[ColumnElement[Any]] = None,
    action: CerbosAction = CerbosAction.VIEW,
) -> RowMapping:
    """
    Retrieve aggregate rows from the database, filtered by the where clause and the user's permissions.
    """
    query = get_aggregate_db_query(model_cls, action, cerbos_client, principal, where, aggregate, group_by)
    if order_by:
        query = query.order_by(*order_by)  # type: ignore
    result = await session.execute(query)
    return result.mappings().one()
