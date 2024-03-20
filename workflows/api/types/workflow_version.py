"""
GraphQL type for WorkflowVersion

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
from api.validators.workflow_version import WorkflowVersionCreateInputValidator
from api.helpers.workflow_version import WorkflowVersionGroupByOptions, build_workflow_version_groupby_output
from api.types.entities import EntityInterface
from api.types.workflow_run import WorkflowRunAggregate, format_workflow_run_aggregate_output
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
    BoolComparators,
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
    from api.types.workflow import WorkflowOrderByClause, WorkflowWhereClause, Workflow
    from api.types.workflow_run import WorkflowRunOrderByClause, WorkflowRunWhereClause, WorkflowRun

    pass
else:
    WorkflowWhereClause = "WorkflowWhereClause"
    Workflow = "Workflow"
    WorkflowOrderByClause = "WorkflowOrderByClause"
    WorkflowRunWhereClause = "WorkflowRunWhereClause"
    WorkflowRun = "WorkflowRun"
    WorkflowRunOrderByClause = "WorkflowRunOrderByClause"
    pass


"""
------------------------------------------------------------------------------
Dataloaders
------------------------------------------------------------------------------
These are batching functions for loading related objects to avoid N+1 queries.
"""


@strawberry.field
async def load_workflow_rows(
    root: "WorkflowVersion",
    info: Info,
    where: Annotated["WorkflowWhereClause", strawberry.lazy("api.types.workflow")] | None = None,
    order_by: Optional[list[Annotated["WorkflowOrderByClause", strawberry.lazy("api.types.workflow")]]] = [],
) -> Optional[Annotated["Workflow", strawberry.lazy("api.types.workflow")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.WorkflowVersion)
    relationship = mapper.relationships["workflow"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.workflow_id)  # type:ignore


@relay.connection(
    relay.ListConnection[Annotated["WorkflowRun", strawberry.lazy("api.types.workflow_run")]]  # type:ignore
)
async def load_workflow_run_rows(
    root: "WorkflowVersion",
    info: Info,
    where: Annotated["WorkflowRunWhereClause", strawberry.lazy("api.types.workflow_run")] | None = None,
    order_by: Optional[list[Annotated["WorkflowRunOrderByClause", strawberry.lazy("api.types.workflow_run")]]] = [],
) -> Sequence[Annotated["WorkflowRun", strawberry.lazy("api.types.workflow_run")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.WorkflowVersion)
    relationship = mapper.relationships["runs"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.id)  # type:ignore


@strawberry.field
async def load_workflow_run_aggregate_rows(
    root: "WorkflowVersion",
    info: Info,
    where: Annotated["WorkflowRunWhereClause", strawberry.lazy("api.types.workflow_run")] | None = None,
) -> Optional[Annotated["WorkflowRunAggregate", strawberry.lazy("api.types.workflow_run")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.WorkflowVersion)
    relationship = mapper.relationships["runs"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    aggregate_output = format_workflow_run_aggregate_output(rows)
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
class WorkflowVersionWhereClauseMutations(TypedDict):
    id: UUIDComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class WorkflowVersionWhereClause(TypedDict):
    graph_json: Optional[StrComparators] | None
    workflow_uri: Optional[StrComparators] | None
    version: Optional[StrComparators] | None
    manifest: Optional[StrComparators] | None
    workflow: Optional[Annotated["WorkflowWhereClause", strawberry.lazy("api.types.workflow")]] | None
    deprecated: Optional[BoolComparators] | None
    runs: Optional[Annotated["WorkflowRunWhereClause", strawberry.lazy("api.types.workflow_run")]] | None
    id: Optional[UUIDComparators] | None
    owner_user_id: Optional[IntComparators] | None
    collection_id: Optional[IntComparators] | None
    created_at: Optional[DatetimeComparators] | None
    updated_at: Optional[DatetimeComparators] | None
    deleted_at: Optional[DatetimeComparators] | None


"""
Supported ORDER BY clause attributes
"""


@strawberry.input
class WorkflowVersionOrderByClause(TypedDict):
    graph_json: Optional[orderBy] | None
    workflow_uri: Optional[orderBy] | None
    version: Optional[orderBy] | None
    manifest: Optional[orderBy] | None
    workflow: Optional[Annotated["WorkflowOrderByClause", strawberry.lazy("api.types.workflow")]] | None
    deprecated: Optional[orderBy] | None
    id: Optional[orderBy] | None
    owner_user_id: Optional[orderBy] | None
    collection_id: Optional[orderBy] | None
    created_at: Optional[orderBy] | None
    updated_at: Optional[orderBy] | None
    deleted_at: Optional[orderBy] | None


"""
Define WorkflowVersion type
"""


@strawberry.type
class WorkflowVersion(EntityInterface):
    graph_json: Optional[str] = None
    workflow_uri: Optional[str] = None
    version: Optional[str] = None
    manifest: Optional[str] = None
    workflow: Optional[Annotated["Workflow", strawberry.lazy("api.types.workflow")]] = load_workflow_rows  # type:ignore
    deprecated: Optional[bool] = None
    runs: Sequence[
        Annotated["WorkflowRun", strawberry.lazy("api.types.workflow_run")]
    ] = load_workflow_run_rows  # type:ignore
    runs_aggregate: Optional[
        Annotated["WorkflowRunAggregate", strawberry.lazy("api.types.workflow_run")]
    ] = load_workflow_run_aggregate_rows  # type:ignore
    id: strawberry.ID
    owner_user_id: int
    collection_id: int
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None


"""
We need to add this to each Queryable type so that strawberry will accept either our
Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
"""
WorkflowVersion.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.WorkflowVersion or type(obj) == WorkflowVersion
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
class WorkflowVersionNumericalColumns:
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class WorkflowVersionMinMaxColumns:
    graph_json: Optional[str] = None
    workflow_uri: Optional[str] = None
    version: Optional[str] = None
    manifest: Optional[str] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class WorkflowVersionCountColumns(enum.Enum):
    graphJson = "graph_json"
    workflowUri = "workflow_uri"
    version = "version"
    manifest = "manifest"
    workflow = "workflow"
    deprecated = "deprecated"
    runs = "runs"
    id = "id"
    ownerUserId = "owner_user_id"
    collectionId = "collection_id"
    createdAt = "created_at"
    updatedAt = "updated_at"
    deletedAt = "deleted_at"


"""
All supported aggregation functions
"""


@strawberry.type
class WorkflowVersionAggregateFunctions:
    # This is a hack to accept "distinct" and "columns" as arguments to "count"
    @strawberry.field
    def count(
        self, distinct: Optional[bool] = False, columns: Optional[WorkflowVersionCountColumns] = None
    ) -> Optional[int]:
        # Count gets set with the proper value in the resolver, so we just return it here
        return self.count  # type: ignore

    sum: Optional[WorkflowVersionNumericalColumns] = None
    avg: Optional[WorkflowVersionNumericalColumns] = None
    stddev: Optional[WorkflowVersionNumericalColumns] = None
    variance: Optional[WorkflowVersionNumericalColumns] = None
    min: Optional[WorkflowVersionMinMaxColumns] = None
    max: Optional[WorkflowVersionMinMaxColumns] = None
    groupBy: Optional[WorkflowVersionGroupByOptions] = None


"""
Wrapper around WorkflowVersionAggregateFunctions
"""


@strawberry.type
class WorkflowVersionAggregate:
    aggregate: Optional[list[WorkflowVersionAggregateFunctions]] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class WorkflowVersionCreateInput:
    graph_json: Optional[str] = None
    workflow_uri: Optional[str] = None
    version: Optional[str] = None
    manifest: Optional[str] = None
    workflow_id: Optional[strawberry.ID] = None
    deprecated: Optional[bool] = None
    collection_id: int
    deleted_at: Optional[datetime.datetime] = None


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_workflow_versions(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[WorkflowVersionWhereClause] = None,
    order_by: Optional[list[WorkflowVersionOrderByClause]] = [],
    limit_offset: Optional[LimitOffsetClause] = None,
) -> typing.Sequence[WorkflowVersion]:
    """
    Resolve WorkflowVersion objects. Used for queries (see api/queries.py).
    """
    limit = limit_offset["limit"] if limit_offset and "limit" in limit_offset else None
    offset = limit_offset["offset"] if limit_offset and "offset" in limit_offset else None
    if offset and not limit:
        raise PlatformicsException("Cannot use offset without limit")
    return await get_db_rows(db.WorkflowVersion, session, cerbos_client, principal, where, order_by, CerbosAction.VIEW, limit, offset)  # type: ignore


def format_workflow_version_aggregate_output(
    query_results: Sequence[RowMapping] | RowMapping,
) -> WorkflowVersionAggregate:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    aggregate = []
    if type(query_results) is not list:
        query_results = [query_results]  # type: ignore
    for row in query_results:
        aggregate.append(format_workflow_version_aggregate_row(row))
    return WorkflowVersionAggregate(aggregate=aggregate)


def format_workflow_version_aggregate_row(row: RowMapping) -> WorkflowVersionAggregateFunctions:
    """
    Given a single row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = WorkflowVersionAggregateFunctions()
    for key, value in row.items():
        # Key is either an aggregate function or a groupby key
        group_keys = key.split(".")
        aggregate = key.split("_", 1)
        if aggregate[0] not in aggregator_map.keys():
            # Turn list of groupby keys into nested objects
            if not getattr(output, "groupBy"):
                setattr(output, "groupBy", WorkflowVersionGroupByOptions())
            group = build_workflow_version_groupby_output(getattr(output, "groupBy"), group_keys, value)
            setattr(output, "groupBy", group)
        else:
            aggregate_name = aggregate[0]
            if aggregate_name == "count":
                output.count = value
            else:
                aggregator_fn, col_name = aggregate[0], aggregate[1]
                if not getattr(output, aggregator_fn):
                    if aggregate_name in ["min", "max"]:
                        setattr(output, aggregator_fn, WorkflowVersionMinMaxColumns())
                    else:
                        setattr(output, aggregator_fn, WorkflowVersionNumericalColumns())
                setattr(getattr(output, aggregator_fn), col_name, value)
    return output


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_workflow_versions_aggregate(
    info: Info,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[WorkflowVersionWhereClause] = None,
    # TODO: add support for groupby, limit/offset
) -> WorkflowVersionAggregate:
    """
    Aggregate values for WorkflowVersion objects. Used for queries (see api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on, and groupby options if any were provided.
    # TODO: not sure why selected_fields is a list
    selections = info.selected_fields[0].selections[0].selections
    aggregate_selections = [selection for selection in selections if getattr(selection, "name") != "groupBy"]
    groupby_selections = [selection for selection in selections if getattr(selection, "name") == "groupBy"]
    groupby_selections = groupby_selections[0].selections if groupby_selections else []

    if not aggregate_selections:
        raise PlatformicsException("No aggregate functions selected")

    rows = await get_aggregate_db_rows(db.WorkflowVersion, session, cerbos_client, principal, where, aggregate_selections, [], groupby_selections)  # type: ignore
    aggregate_output = format_workflow_version_aggregate_output(rows)
    return aggregate_output


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_workflow_version(
    input: WorkflowVersionCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> db.Entity:
    """
    Create a new WorkflowVersion object. Used for mutations (see api/mutations.py).
    """
    validated = WorkflowVersionCreateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Validate that the user can read all of the entities they're linking to.
    # If we have any system_writable fields present, make sure that our auth'd user *is* a system user
    if not is_system_user:
        raise PlatformicsException("Unauthorized: WorkflowVersion is not creatable")
    # Validate that the user can create entities in this collection
    attr = {"collection_id": validated.collection_id}
    resource = Resource(id="NEW_ID", kind=db.WorkflowVersion.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise PlatformicsException("Unauthorized: Cannot create entity in this collection")

    # Validate that the user can read all of the entities they're linking to.
    # Check that workflow relationship is accessible.
    if validated.workflow_id:
        workflow = await get_db_rows(
            db.Workflow,
            session,
            cerbos_client,
            principal,
            {"id": {"_eq": validated.workflow_id}},
            [],
            CerbosAction.VIEW,
        )
        if not workflow:
            raise PlatformicsException("Unauthorized: workflow does not exist")

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.WorkflowVersion(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def delete_workflow_version(
    where: WorkflowVersionWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Delete WorkflowVersion objects. Used for mutations (see api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(db.WorkflowVersion, session, cerbos_client, principal, where, [], CerbosAction.DELETE)
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
