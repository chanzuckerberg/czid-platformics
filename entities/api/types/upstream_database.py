"""
GraphQL type for UpstreamDatabase

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


import typing
from typing import TYPE_CHECKING, Annotated, Optional, Sequence

import database.models as db
import strawberry
import datetime
from platformics.api.core.helpers import get_db_rows, get_aggregate_db_rows
from api.validators.upstream_database import UpstreamDatabaseCreateInputValidator, UpstreamDatabaseUpdateInputValidator
from api.helpers.upstream_database import UpstreamDatabaseGroupByOptions, build_upstream_database_groupby_output
from api.types.entities import EntityInterface
from api.types.taxon import TaxonAggregate, format_taxon_aggregate_output
from api.types.index_file import IndexFileAggregate, format_index_file_aggregate_output
from api.types.accession import AccessionAggregate, format_accession_aggregate_output
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource
from fastapi import Depends
from platformics.api.core.errors import PlatformicsException
from platformics.api.core.deps import get_cerbos_client, get_db_session, require_auth_principal, is_system_user
from platformics.api.core.gql_to_sql import (
    aggregator_map,
    orderBy,
    DatetimeComparators,
    IntComparators,
    StrComparators,
    UUIDComparators,
)
from platformics.api.core.strawberry_extensions import DependencyExtension
from platformics.security.authorization import CerbosAction
from sqlalchemy import inspect
from sqlalchemy.engine.row import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import relay
from strawberry.types import Info
from support.limit_offset import LimitOffsetClause
from typing_extensions import TypedDict
import enum


E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.taxon import TaxonOrderByClause, TaxonWhereClause, Taxon
    from api.types.index_file import IndexFileOrderByClause, IndexFileWhereClause, IndexFile
    from api.types.accession import AccessionOrderByClause, AccessionWhereClause, Accession

    pass
else:
    TaxonWhereClause = "TaxonWhereClause"
    Taxon = "Taxon"
    TaxonOrderByClause = "TaxonOrderByClause"
    IndexFileWhereClause = "IndexFileWhereClause"
    IndexFile = "IndexFile"
    IndexFileOrderByClause = "IndexFileOrderByClause"
    AccessionWhereClause = "AccessionWhereClause"
    Accession = "Accession"
    AccessionOrderByClause = "AccessionOrderByClause"
    pass


"""
------------------------------------------------------------------------------
Dataloaders
------------------------------------------------------------------------------
These are batching functions for loading related objects to avoid N+1 queries.
"""


@relay.connection(
    relay.ListConnection[Annotated["Taxon", strawberry.lazy("api.types.taxon")]]  # type:ignore
)
async def load_taxon_rows(
    root: "UpstreamDatabase",
    info: Info,
    where: Annotated["TaxonWhereClause", strawberry.lazy("api.types.taxon")] | None = None,
    order_by: Optional[list[Annotated["TaxonOrderByClause", strawberry.lazy("api.types.taxon")]]] = [],
) -> Sequence[Annotated["Taxon", strawberry.lazy("api.types.taxon")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.UpstreamDatabase)
    relationship = mapper.relationships["taxa"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.id)  # type:ignore


@strawberry.field
async def load_taxon_aggregate_rows(
    root: "UpstreamDatabase",
    info: Info,
    where: Annotated["TaxonWhereClause", strawberry.lazy("api.types.taxon")] | None = None,
) -> Optional[Annotated["TaxonAggregate", strawberry.lazy("api.types.taxon")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.UpstreamDatabase)
    relationship = mapper.relationships["taxa"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    aggregate_output = format_taxon_aggregate_output(rows)
    return aggregate_output


@relay.connection(
    relay.ListConnection[Annotated["IndexFile", strawberry.lazy("api.types.index_file")]]  # type:ignore
)
async def load_index_file_rows(
    root: "UpstreamDatabase",
    info: Info,
    where: Annotated["IndexFileWhereClause", strawberry.lazy("api.types.index_file")] | None = None,
    order_by: Optional[list[Annotated["IndexFileOrderByClause", strawberry.lazy("api.types.index_file")]]] = [],
) -> Sequence[Annotated["IndexFile", strawberry.lazy("api.types.index_file")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.UpstreamDatabase)
    relationship = mapper.relationships["indexes"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.id)  # type:ignore


@strawberry.field
async def load_index_file_aggregate_rows(
    root: "UpstreamDatabase",
    info: Info,
    where: Annotated["IndexFileWhereClause", strawberry.lazy("api.types.index_file")] | None = None,
) -> Optional[Annotated["IndexFileAggregate", strawberry.lazy("api.types.index_file")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.UpstreamDatabase)
    relationship = mapper.relationships["indexes"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    aggregate_output = format_index_file_aggregate_output(rows)
    return aggregate_output


@relay.connection(
    relay.ListConnection[Annotated["Accession", strawberry.lazy("api.types.accession")]]  # type:ignore
)
async def load_accession_rows(
    root: "UpstreamDatabase",
    info: Info,
    where: Annotated["AccessionWhereClause", strawberry.lazy("api.types.accession")] | None = None,
    order_by: Optional[list[Annotated["AccessionOrderByClause", strawberry.lazy("api.types.accession")]]] = [],
) -> Sequence[Annotated["Accession", strawberry.lazy("api.types.accession")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.UpstreamDatabase)
    relationship = mapper.relationships["accessions"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.id)  # type:ignore


@strawberry.field
async def load_accession_aggregate_rows(
    root: "UpstreamDatabase",
    info: Info,
    where: Annotated["AccessionWhereClause", strawberry.lazy("api.types.accession")] | None = None,
) -> Optional[Annotated["AccessionAggregate", strawberry.lazy("api.types.accession")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.UpstreamDatabase)
    relationship = mapper.relationships["accessions"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    aggregate_output = format_accession_aggregate_output(rows)
    return aggregate_output


"""
------------------------------------------------------------------------------
Define Strawberry GQL types
------------------------------------------------------------------------------
"""

"""
Only let users specify IDs in WHERE clause when mutating data (for safety).
We can extend that list as we gather more use cases from the FE team.
"""


@strawberry.input
class UpstreamDatabaseWhereClauseMutations(TypedDict):
    id: UUIDComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class UpstreamDatabaseWhereClause(TypedDict):
    name: Optional[StrComparators] | None
    taxa: Optional[Annotated["TaxonWhereClause", strawberry.lazy("api.types.taxon")]] | None
    indexes: Optional[Annotated["IndexFileWhereClause", strawberry.lazy("api.types.index_file")]] | None
    accessions: Optional[Annotated["AccessionWhereClause", strawberry.lazy("api.types.accession")]] | None
    id: Optional[UUIDComparators] | None
    producing_run_id: Optional[UUIDComparators] | None
    owner_user_id: Optional[IntComparators] | None
    collection_id: Optional[IntComparators] | None
    created_at: Optional[DatetimeComparators] | None
    updated_at: Optional[DatetimeComparators] | None


"""
Supported ORDER BY clause attributes
"""


@strawberry.input
class UpstreamDatabaseOrderByClause(TypedDict):
    name: Optional[orderBy] | None
    id: Optional[orderBy] | None
    producing_run_id: Optional[orderBy] | None
    owner_user_id: Optional[orderBy] | None
    collection_id: Optional[orderBy] | None
    created_at: Optional[orderBy] | None
    updated_at: Optional[orderBy] | None


"""
Define UpstreamDatabase type
"""


@strawberry.type
class UpstreamDatabase(EntityInterface):
    name: str
    taxa: Sequence[Annotated["Taxon", strawberry.lazy("api.types.taxon")]] = load_taxon_rows  # type:ignore
    taxa_aggregate: Optional[
        Annotated["TaxonAggregate", strawberry.lazy("api.types.taxon")]
    ] = load_taxon_aggregate_rows  # type:ignore
    indexes: Sequence[
        Annotated["IndexFile", strawberry.lazy("api.types.index_file")]
    ] = load_index_file_rows  # type:ignore
    indexes_aggregate: Optional[
        Annotated["IndexFileAggregate", strawberry.lazy("api.types.index_file")]
    ] = load_index_file_aggregate_rows  # type:ignore
    accessions: Sequence[
        Annotated["Accession", strawberry.lazy("api.types.accession")]
    ] = load_accession_rows  # type:ignore
    accessions_aggregate: Optional[
        Annotated["AccessionAggregate", strawberry.lazy("api.types.accession")]
    ] = load_accession_aggregate_rows  # type:ignore
    id: strawberry.ID
    producing_run_id: Optional[strawberry.ID] = None
    owner_user_id: int
    collection_id: int
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None


"""
We need to add this to each Queryable type so that strawberry will accept either our
Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
"""
UpstreamDatabase.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.UpstreamDatabase or type(obj) == UpstreamDatabase
)

"""
------------------------------------------------------------------------------
Aggregation types
------------------------------------------------------------------------------
"""
"""
Define columns that support numerical aggregations
"""


@strawberry.type
class UpstreamDatabaseNumericalColumns:
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class UpstreamDatabaseMinMaxColumns:
    name: Optional[str] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class UpstreamDatabaseCountColumns(enum.Enum):
    name = "name"
    taxa = "taxa"
    indexes = "indexes"
    accessions = "accessions"
    id = "id"
    producingRunId = "producing_run_id"
    ownerUserId = "owner_user_id"
    collectionId = "collection_id"
    createdAt = "created_at"
    updatedAt = "updated_at"


"""
All supported aggregation functions
"""


@strawberry.type
class UpstreamDatabaseAggregateFunctions:
    # This is a hack to accept "distinct" and "columns" as arguments to "count"
    @strawberry.field
    def count(
        self, distinct: Optional[bool] = False, columns: Optional[UpstreamDatabaseCountColumns] = None
    ) -> Optional[int]:
        # Count gets set with the proper value in the resolver, so we just return it here
        return self.count  # type: ignore

    sum: Optional[UpstreamDatabaseNumericalColumns] = None
    avg: Optional[UpstreamDatabaseNumericalColumns] = None
    stddev: Optional[UpstreamDatabaseNumericalColumns] = None
    variance: Optional[UpstreamDatabaseNumericalColumns] = None
    min: Optional[UpstreamDatabaseMinMaxColumns] = None
    max: Optional[UpstreamDatabaseMinMaxColumns] = None
    groupBy: Optional[UpstreamDatabaseGroupByOptions] = None


"""
Wrapper around UpstreamDatabaseAggregateFunctions
"""


@strawberry.type
class UpstreamDatabaseAggregate:
    aggregate: Optional[list[UpstreamDatabaseAggregateFunctions]] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class UpstreamDatabaseCreateInput:
    name: str
    producing_run_id: Optional[strawberry.ID] = None
    collection_id: int


@strawberry.input()
class UpstreamDatabaseUpdateInput:
    name: Optional[str] = None


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_upstream_databases(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[UpstreamDatabaseWhereClause] = None,
    order_by: Optional[list[UpstreamDatabaseOrderByClause]] = [],
    limit_offset: Optional[LimitOffsetClause] = None,
) -> typing.Sequence[UpstreamDatabase]:
    """
    Resolve UpstreamDatabase objects. Used for queries (see api/queries.py).
    """
    limit = limit_offset["limit"] if limit_offset and "limit" in limit_offset else None
    offset = limit_offset["offset"] if limit_offset and "offset" in limit_offset else None
    if offset and not limit:
        raise PlatformicsException("Cannot use offset without limit")
    return await get_db_rows(db.UpstreamDatabase, session, cerbos_client, principal, where, order_by, CerbosAction.VIEW, limit, offset)  # type: ignore


def format_upstream_database_aggregate_output(
    query_results: Sequence[RowMapping] | RowMapping,
) -> UpstreamDatabaseAggregate:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    aggregate = []
    if type(query_results) is not list:
        query_results = [query_results]  # type: ignore
    for row in query_results:
        aggregate.append(format_upstream_database_aggregate_row(row))
    return UpstreamDatabaseAggregate(aggregate=aggregate)


def format_upstream_database_aggregate_row(row: RowMapping) -> UpstreamDatabaseAggregateFunctions:
    """
    Given a single row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = UpstreamDatabaseAggregateFunctions()
    for key, value in row.items():
        # Key is either an aggregate function or a groupby key
        group_keys = key.split(".")
        aggregate = key.split("_", 1)
        if aggregate[0] not in aggregator_map.keys():
            # Turn list of groupby keys into nested objects
            if not getattr(output, "groupBy"):
                setattr(output, "groupBy", UpstreamDatabaseGroupByOptions())
            group = build_upstream_database_groupby_output(getattr(output, "groupBy"), group_keys, value)
            setattr(output, "groupBy", group)
        else:
            aggregate_name = aggregate[0]
            if aggregate_name == "count":
                output.count = value
            else:
                aggregator_fn, col_name = aggregate[0], aggregate[1]
                if not getattr(output, aggregator_fn):
                    if aggregate_name in ["min", "max"]:
                        setattr(output, aggregator_fn, UpstreamDatabaseMinMaxColumns())
                    else:
                        setattr(output, aggregator_fn, UpstreamDatabaseNumericalColumns())
                setattr(getattr(output, aggregator_fn), col_name, value)
    return output


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_upstream_databases_aggregate(
    info: Info,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[UpstreamDatabaseWhereClause] = None,
    # TODO: add support for groupby, limit/offset
) -> UpstreamDatabaseAggregate:
    """
    Aggregate values for UpstreamDatabase objects. Used for queries (see api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on, and groupby options if any were provided.
    # TODO: not sure why selected_fields is a list
    selections = info.selected_fields[0].selections[0].selections
    aggregate_selections = [selection for selection in selections if getattr(selection, "name") != "groupBy"]
    groupby_selections = [selection for selection in selections if getattr(selection, "name") == "groupBy"]
    groupby_selections = groupby_selections[0].selections if groupby_selections else []

    if not aggregate_selections:
        raise PlatformicsException("No aggregate functions selected")

    rows = await get_aggregate_db_rows(db.UpstreamDatabase, session, cerbos_client, principal, where, aggregate_selections, [], groupby_selections)  # type: ignore
    aggregate_output = format_upstream_database_aggregate_output(rows)
    return aggregate_output


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_upstream_database(
    input: UpstreamDatabaseCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> db.Entity:
    """
    Create a new UpstreamDatabase object. Used for mutations (see api/mutations.py).
    """
    validated = UpstreamDatabaseCreateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Validate that the user can read all of the entities they're linking to.
    # If we have any system_writable fields present, make sure that our auth'd user *is* a system user
    if not is_system_user:
        del params["producing_run_id"]
    # Validate that the user can create entities in this collection
    attr = {"collection_id": validated.collection_id}
    resource = Resource(id="NEW_ID", kind=db.UpstreamDatabase.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise PlatformicsException("Unauthorized: Cannot create entity in this collection")

    # Validate that the user can read all of the entities they're linking to.

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.UpstreamDatabase(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_upstream_database(
    input: UpstreamDatabaseUpdateInput,
    where: UpstreamDatabaseWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> Sequence[db.Entity]:
    """
    Update UpstreamDatabase objects. Used for mutations (see api/mutations.py).
    """
    validated = UpstreamDatabaseUpdateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise PlatformicsException("No fields to update")

    # Validate that the user can read all of the entities they're linking to.

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(db.UpstreamDatabase, session, cerbos_client, principal, where, [], CerbosAction.UPDATE)
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot update entities")

    # Update DB
    updated_at = datetime.datetime.now()
    for entity in entities:
        entity.updated_at = updated_at
        for key in params:
            if params[key] is not None:
                setattr(entity, key, params[key])
    await session.commit()
    return entities


@strawberry.mutation(extensions=[DependencyExtension()])
async def delete_upstream_database(
    where: UpstreamDatabaseWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Delete UpstreamDatabase objects. Used for mutations (see api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(db.UpstreamDatabase, session, cerbos_client, principal, where, [], CerbosAction.DELETE)
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
