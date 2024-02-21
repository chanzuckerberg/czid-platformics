"""
GraphQL type for IndexFile

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


import typing
from typing import TYPE_CHECKING, Annotated, Optional, Sequence, Callable

import database.models as db
import strawberry
import datetime
from platformics.api.core.helpers import get_db_rows, get_aggregate_db_rows
from api.validators.index_file import IndexFileCreateInputValidator, IndexFileUpdateInputValidator
from api.files import File, FileWhereClause
from api.helpers.index_file import IndexFileGroupByOptions, build_index_file_groupby_output
from api.types.entities import EntityInterface
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource
from fastapi import Depends
from platformics.api.core.errors import PlatformicsException
from platformics.api.core.deps import get_cerbos_client, get_db_session, require_auth_principal, is_system_user
from platformics.api.core.gql_to_sql import (
    aggregator_map,
    orderBy,
    EnumComparators,
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
from strawberry.types import Info
from typing_extensions import TypedDict
import enum
from support.enums import IndexTypes

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.upstream_database import UpstreamDatabaseOrderByClause, UpstreamDatabaseWhereClause, UpstreamDatabase
    from api.types.host_organism import HostOrganismOrderByClause, HostOrganismWhereClause, HostOrganism

    pass
else:
    UpstreamDatabaseWhereClause = "UpstreamDatabaseWhereClause"
    UpstreamDatabase = "UpstreamDatabase"
    UpstreamDatabaseOrderByClause = "UpstreamDatabaseOrderByClause"
    HostOrganismWhereClause = "HostOrganismWhereClause"
    HostOrganism = "HostOrganism"
    HostOrganismOrderByClause = "HostOrganismOrderByClause"
    pass


"""
------------------------------------------------------------------------------
Dataloaders
------------------------------------------------------------------------------
These are batching functions for loading related objects to avoid N+1 queries.
"""


@strawberry.field
async def load_upstream_database_rows(
    root: "IndexFile",
    info: Info,
    where: Annotated["UpstreamDatabaseWhereClause", strawberry.lazy("api.types.upstream_database")] | None = None,
    order_by: Optional[
        list[Annotated["UpstreamDatabaseOrderByClause", strawberry.lazy("api.types.upstream_database")]]
    ] = [],
) -> Optional[Annotated["UpstreamDatabase", strawberry.lazy("api.types.upstream_database")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.IndexFile)
    relationship = mapper.relationships["upstream_database"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.upstream_database_id)  # type:ignore


@strawberry.field
async def load_host_organism_rows(
    root: "IndexFile",
    info: Info,
    where: Annotated["HostOrganismWhereClause", strawberry.lazy("api.types.host_organism")] | None = None,
    order_by: Optional[list[Annotated["HostOrganismOrderByClause", strawberry.lazy("api.types.host_organism")]]] = [],
) -> Optional[Annotated["HostOrganism", strawberry.lazy("api.types.host_organism")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.IndexFile)
    relationship = mapper.relationships["host_organism"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.host_organism_id)  # type:ignore


"""
------------------------------------------------------------------------------
Dataloader for File object
------------------------------------------------------------------------------
"""


def load_files_from(attr_name: str) -> Callable:
    @strawberry.field
    async def load_files(
        root: "IndexFile",
        info: Info,
        where: Annotated["FileWhereClause", strawberry.lazy("api.files")] | None = None,
    ) -> Optional[Annotated["File", strawberry.lazy("api.files")]]:
        """
        Given a list of IndexFile IDs for a certain file type, return related Files
        """
        dataloader = info.context["sqlalchemy_loader"]
        mapper = inspect(db.IndexFile)
        relationship = mapper.relationships[attr_name]
        return await dataloader.loader_for(relationship, where).load(getattr(root, f"{attr_name}_id"))  # type:ignore

    return load_files


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
class IndexFileWhereClauseMutations(TypedDict):
    id: UUIDComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class IndexFileWhereClause(TypedDict):
    name: Optional[EnumComparators[IndexTypes]] | None
    version: Optional[StrComparators] | None
    upstream_database: Optional[
        Annotated["UpstreamDatabaseWhereClause", strawberry.lazy("api.types.upstream_database")]
    ] | None
    host_organism: Optional[Annotated["HostOrganismWhereClause", strawberry.lazy("api.types.host_organism")]] | None
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
class IndexFileOrderByClause(TypedDict):
    name: Optional[orderBy] | None
    version: Optional[orderBy] | None
    upstream_database: Optional[
        Annotated["UpstreamDatabaseOrderByClause", strawberry.lazy("api.types.upstream_database")]
    ] | None
    host_organism: Optional[Annotated["HostOrganismOrderByClause", strawberry.lazy("api.types.host_organism")]] | None
    id: Optional[orderBy] | None
    producing_run_id: Optional[orderBy] | None
    owner_user_id: Optional[orderBy] | None
    collection_id: Optional[orderBy] | None
    created_at: Optional[orderBy] | None
    updated_at: Optional[orderBy] | None


"""
Define IndexFile type
"""


@strawberry.type
class IndexFile(EntityInterface):
    name: IndexTypes
    version: str
    file_id: Optional[strawberry.ID]
    file: Optional[Annotated["File", strawberry.lazy("api.files")]] = load_files_from("file")  # type: ignore
    upstream_database: Optional[
        Annotated["UpstreamDatabase", strawberry.lazy("api.types.upstream_database")]
    ] = load_upstream_database_rows  # type:ignore
    host_organism: Optional[
        Annotated["HostOrganism", strawberry.lazy("api.types.host_organism")]
    ] = load_host_organism_rows  # type:ignore
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
IndexFile.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.IndexFile or type(obj) == IndexFile
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
class IndexFileNumericalColumns:
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class IndexFileMinMaxColumns:
    version: Optional[str] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class IndexFileCountColumns(enum.Enum):
    name = "name"
    version = "version"
    file = "file"
    upstream_database = "upstream_database"
    host_organism = "host_organism"
    id = "id"
    producing_run_id = "producing_run_id"
    owner_user_id = "owner_user_id"
    collection_id = "collection_id"
    created_at = "created_at"
    updated_at = "updated_at"


"""
All supported aggregation functions
"""


@strawberry.type
class IndexFileAggregateFunctions:
    # This is a hack to accept "distinct" and "columns" as arguments to "count"
    @strawberry.field
    def count(self, distinct: Optional[bool] = False, columns: Optional[IndexFileCountColumns] = None) -> Optional[int]:
        # Count gets set with the proper value in the resolver, so we just return it here
        return self.count  # type: ignore

    sum: Optional[IndexFileNumericalColumns] = None
    avg: Optional[IndexFileNumericalColumns] = None
    stddev: Optional[IndexFileNumericalColumns] = None
    variance: Optional[IndexFileNumericalColumns] = None
    min: Optional[IndexFileMinMaxColumns] = None
    max: Optional[IndexFileMinMaxColumns] = None
    groupBy: Optional[IndexFileGroupByOptions] = None


"""
Wrapper around IndexFileAggregateFunctions
"""


@strawberry.type
class IndexFileAggregate:
    aggregate: Optional[list[IndexFileAggregateFunctions]] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class IndexFileCreateInput:
    name: IndexTypes
    version: str
    upstream_database_id: Optional[strawberry.ID] = None
    host_organism_id: Optional[strawberry.ID] = None
    producing_run_id: Optional[strawberry.ID] = None
    collection_id: int


@strawberry.input()
class IndexFileUpdateInput:
    name: Optional[IndexTypes] = None
    version: Optional[str] = None


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_index_files(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[IndexFileWhereClause] = None,
    order_by: Optional[list[IndexFileOrderByClause]] = [],
) -> typing.Sequence[IndexFile]:
    """
    Resolve IndexFile objects. Used for queries (see api/queries.py).
    """
    return await get_db_rows(db.IndexFile, session, cerbos_client, principal, where, order_by)  # type: ignore


def format_index_file_aggregate_output(query_results: list[RowMapping]) -> IndexFileAggregate:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    aggregate = []
    for row in query_results:
        aggregate.append(format_index_file_aggregate_row(row))
    return IndexFileAggregate(aggregate=aggregate)


def format_index_file_aggregate_row(row: RowMapping) -> IndexFileAggregateFunctions:
    """
    Given a single row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = IndexFileAggregateFunctions()
    for key, value in row.items():
        # Key is either an aggregate function or a groupby key
        group_keys = key.split(".")
        aggregate = key.split("_", 1)
        if aggregate[0] not in aggregator_map.keys():
            # Turn list of groupby keys into nested objects
            if not getattr(output, "groupBy"):
                setattr(output, "groupBy", IndexFileGroupByOptions())
            group = build_index_file_groupby_output(getattr(output, "groupBy"), group_keys, value)
            setattr(output, "groupBy", group)
        else:
            aggregate_name = aggregate[0]
            if aggregate_name == "count":
                output.count = value
            else:
                aggregator_fn, col_name = aggregate[0], aggregate[1]
                if not getattr(output, aggregator_fn):
                    if aggregate_name in ["min", "max"]:
                        setattr(output, aggregator_fn, IndexFileMinMaxColumns())
                    else:
                        setattr(output, aggregator_fn, IndexFileNumericalColumns())
                setattr(getattr(output, aggregator_fn), col_name, value)
    return output


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_index_files_aggregate(
    info: Info,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[IndexFileWhereClause] = None,
) -> IndexFileAggregate:
    """
    Aggregate values for IndexFile objects. Used for queries (see api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on, and groupby options if any were provided.
    # TODO: not sure why selected_fields is a list
    selections = info.selected_fields[0].selections[0].selections
    aggregate_selections = [selection for selection in selections if getattr(selection, "name") != "groupBy"]
    groupby_selections = [selection for selection in selections if getattr(selection, "name") == "groupBy"]
    groupby_selections = groupby_selections[0].selections if groupby_selections else []

    if not aggregate_selections:
        raise Exception("No aggregate functions selected")

    rows = await get_aggregate_db_rows(db.IndexFile, session, cerbos_client, principal, where, aggregate_selections, [], groupby_selections)  # type: ignore
    aggregate_output = format_index_file_aggregate_output(rows)
    return aggregate_output


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_index_file(
    input: IndexFileCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> db.Entity:
    """
    Create a new IndexFile object. Used for mutations (see api/mutations.py).
    """
    validated = IndexFileCreateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Validate that the user can read all of the entities they're linking to.
    # If we have any system_writable fields present, make sure that our auth'd user *is* a system user
    if not is_system_user:
        del params["producing_run_id"]
    # Validate that the user can create entities in this collection
    attr = {"collection_id": validated.collection_id}
    resource = Resource(id="NEW_ID", kind=db.IndexFile.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise PlatformicsException("Unauthorized: Cannot create entity in this collection")

    # Validate that the user can read all of the entities they're linking to.
    # Check that upstream_database relationship is accessible.
    if validated.upstream_database_id:
        upstream_database = await get_db_rows(
            db.UpstreamDatabase,
            session,
            cerbos_client,
            principal,
            {"id": {"_eq": validated.upstream_database_id}},
            [],
            CerbosAction.VIEW,
        )
        if not upstream_database:
            raise PlatformicsException("Unauthorized: upstream_database does not exist")
    # Check that host_organism relationship is accessible.
    if validated.host_organism_id:
        host_organism = await get_db_rows(
            db.HostOrganism,
            session,
            cerbos_client,
            principal,
            {"id": {"_eq": validated.host_organism_id}},
            [],
            CerbosAction.VIEW,
        )
        if not host_organism:
            raise PlatformicsException("Unauthorized: host_organism does not exist")

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.IndexFile(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_index_file(
    input: IndexFileUpdateInput,
    where: IndexFileWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> Sequence[db.Entity]:
    """
    Update IndexFile objects. Used for mutations (see api/mutations.py).
    """
    validated = IndexFileUpdateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise PlatformicsException("No fields to update")

    # Validate that the user can read all of the entities they're linking to.

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(db.IndexFile, session, cerbos_client, principal, where, [], CerbosAction.UPDATE)
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
async def delete_index_file(
    where: IndexFileWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Delete IndexFile objects. Used for mutations (see api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(db.IndexFile, session, cerbos_client, principal, where, [], CerbosAction.DELETE)
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
