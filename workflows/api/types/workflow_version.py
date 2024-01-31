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
from platformics.api.core.helpers import get_db_rows, get_aggregate_db_rows
from api.types.entities import EntityInterface
from api.types.workflow_run import WorkflowRunAggregate, format_workflow_run_aggregate_output
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource
from fastapi import Depends
from platformics.api.core.errors import PlatformicsException
from platformics.api.core.deps import get_cerbos_client, get_db_session, require_auth_principal
from platformics.api.core.gql_to_sql import (
    aggregator_map,
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
from typing_extensions import TypedDict
import enum

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.workflow import WorkflowWhereClause, Workflow
    from api.types.workflow_run import WorkflowRunWhereClause, WorkflowRun

    pass
else:
    WorkflowWhereClause = "WorkflowWhereClause"
    Workflow = "Workflow"
    WorkflowRunWhereClause = "WorkflowRunWhereClause"
    WorkflowRun = "WorkflowRun"
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
) -> Optional[Annotated["Workflow", strawberry.lazy("api.types.workflow")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.WorkflowVersion)
    relationship = mapper.relationships["workflow"]
    return await dataloader.loader_for(relationship, where).load(root.workflow_id)  # type:ignore


@relay.connection(
    relay.ListConnection[Annotated["WorkflowRun", strawberry.lazy("api.types.workflow_run")]]  # type:ignore
)
async def load_workflow_run_rows(
    root: "WorkflowVersion",
    info: Info,
    where: Annotated["WorkflowRunWhereClause", strawberry.lazy("api.types.workflow_run")] | None = None,
) -> Sequence[Annotated["WorkflowRun", strawberry.lazy("api.types.workflow_run")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.WorkflowVersion)
    relationship = mapper.relationships["runs"]
    return await dataloader.loader_for(relationship, where).load(root.id)  # type:ignore


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
    # Aggregate queries always return a single row, so just grab the first one
    result = rows[0] if rows else None
    aggregate_output = format_workflow_run_aggregate_output(result)
    return WorkflowRunAggregate(aggregate=aggregate_output)


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
    id: UUIDComparators | None
    producing_run_id: IntComparators | None
    owner_user_id: IntComparators | None
    collection_id: IntComparators | None
    graph_json: Optional[StrComparators] | None
    workflow_uri: Optional[StrComparators] | None
    version: Optional[StrComparators] | None
    manifest: Optional[StrComparators] | None
    workflow: Optional[Annotated["WorkflowWhereClause", strawberry.lazy("api.types.workflow")]] | None
    runs: Optional[Annotated["WorkflowRunWhereClause", strawberry.lazy("api.types.workflow_run")]] | None


"""
Define WorkflowVersion type
"""


@strawberry.type
class WorkflowVersion(EntityInterface):
    id: strawberry.ID
    producing_run_id: Optional[int]
    owner_user_id: int
    collection_id: int
    graph_json: Optional[str] = None
    workflow_uri: Optional[str] = None
    version: Optional[str] = None
    manifest: Optional[str] = None
    workflow: Optional[Annotated["Workflow", strawberry.lazy("api.types.workflow")]] = load_workflow_rows  # type:ignore
    runs: Sequence[
        Annotated["WorkflowRun", strawberry.lazy("api.types.workflow_run")]
    ] = load_workflow_run_rows  # type:ignore
    runs_aggregate: Optional[
        Annotated["WorkflowRunAggregate", strawberry.lazy("api.types.workflow_run")]
    ] = load_workflow_run_aggregate_rows  # type:ignore


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
    producing_run_id: Optional[int] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class WorkflowVersionMinMaxColumns:
    producing_run_id: Optional[int] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    graph_json: Optional[str] = None
    workflow_uri: Optional[str] = None
    version: Optional[str] = None
    manifest: Optional[str] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class WorkflowVersionCountColumns(enum.Enum):
    graph_json = "graph_json"
    workflow_uri = "workflow_uri"
    version = "version"
    manifest = "manifest"
    workflow = "workflow"
    runs = "runs"
    entity_id = "entity_id"
    id = "id"
    producing_run_id = "producing_run_id"
    owner_user_id = "owner_user_id"
    collection_id = "collection_id"
    created_at = "created_at"
    updated_at = "updated_at"
    deleted_at = "deleted_at"


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
    min: Optional[WorkflowVersionMinMaxColumns] = None
    max: Optional[WorkflowVersionMinMaxColumns] = None
    stddev: Optional[WorkflowVersionNumericalColumns] = None
    variance: Optional[WorkflowVersionNumericalColumns] = None


"""
Wrapper around WorkflowVersionAggregateFunctions
"""


@strawberry.type
class WorkflowVersionAggregate:
    aggregate: Optional[WorkflowVersionAggregateFunctions] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class WorkflowVersionCreateInput:
    collection_id: int
    graph_json: Optional[str] = None
    workflow_uri: Optional[str] = None
    version: Optional[str] = None
    manifest: Optional[str] = None
    workflow_id: Optional[strawberry.ID] = None


@strawberry.input()
class WorkflowVersionUpdateInput:
    collection_id: Optional[int] = None
    graph_json: Optional[str] = None
    workflow_uri: Optional[str] = None
    version: Optional[str] = None
    manifest: Optional[str] = None
    workflow_id: Optional[strawberry.ID] = None


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
) -> typing.Sequence[WorkflowVersion]:
    """
    Resolve WorkflowVersion objects. Used for queries (see api/queries.py).
    """
    return await get_db_rows(db.WorkflowVersion, session, cerbos_client, principal, where, [])  # type: ignore


def format_workflow_version_aggregate_output(query_results: RowMapping) -> WorkflowVersionAggregateFunctions:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = WorkflowVersionAggregateFunctions()
    for aggregate_name, value in query_results.items():
        if aggregate_name == "count":
            output.count = value
        else:
            aggregator_fn, col_name = aggregate_name.split("_", 1)
            # Filter out the group_by key from the results if one was provided.
            if aggregator_fn in aggregator_map.keys():
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
) -> WorkflowVersionAggregate:
    """
    Aggregate values for WorkflowVersion objects. Used for queries (see api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on
    # TODO: not sure why selected_fields is a list
    # The first list of selections will always be ["aggregate"], so just grab the first item
    selections = info.selected_fields[0].selections[0].selections
    rows = await get_aggregate_db_rows(db.WorkflowVersion, session, cerbos_client, principal, where, selections, [])  # type: ignore
    aggregate_output = format_workflow_version_aggregate_output(rows)
    return WorkflowVersionAggregate(aggregate=aggregate_output)


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_workflow_version(
    input: WorkflowVersionCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> db.Entity:
    """
    Create a new WorkflowVersion object. Used for mutations (see api/mutations.py).
    """
    params = input.__dict__

    # Validate that user can create entity in this collection
    attr = {"collection_id": input.collection_id}
    resource = Resource(id="NEW_ID", kind=db.WorkflowVersion.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise PlatformicsException("Unauthorized: Cannot create entity in this collection")

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.WorkflowVersion(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_workflow_version(
    input: WorkflowVersionUpdateInput,
    where: WorkflowVersionWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Update WorkflowVersion objects. Used for mutations (see api/mutations.py).
    """
    params = input.__dict__

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise PlatformicsException("No fields to update")

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(db.WorkflowVersion, session, cerbos_client, principal, where, [], CerbosAction.UPDATE)
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot update entities")

    # Validate that the user has access to the new collection ID
    if input.collection_id:
        attr = {"collection_id": input.collection_id}
        resource = Resource(id="SOME_ID", kind=db.WorkflowVersion.__tablename__, attr=attr)
        if not cerbos_client.is_allowed(CerbosAction.UPDATE, principal, resource):
            raise PlatformicsException("Unauthorized: Cannot access new collection")

    # Update DB
    for entity in entities:
        for key in params:
            if params[key]:
                setattr(entity, key, params[key])
    await session.commit()
    return entities


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
