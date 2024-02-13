"""
GraphQL type for WorkflowRun

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
from api.types.entities import EntityInterface
from api.types.workflow_run_step import WorkflowRunStepAggregate, format_workflow_run_step_aggregate_output
from api.types.workflow_run_entity_input import (
    WorkflowRunEntityInputAggregate,
    format_workflow_run_entity_input_aggregate_output,
)
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
from strawberry import relay
from strawberry.types import Info
from typing_extensions import TypedDict
import enum
from support.enums import WorkflowRunStatus

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.workflow_version import WorkflowVersionOrderByClause, WorkflowVersionWhereClause, WorkflowVersion
    from api.types.workflow_run_step import WorkflowRunStepOrderByClause, WorkflowRunStepWhereClause, WorkflowRunStep
    from api.types.workflow_run_entity_input import (
        WorkflowRunEntityInputOrderByClause,
        WorkflowRunEntityInputWhereClause,
        WorkflowRunEntityInput,
    )

    pass
else:
    WorkflowVersionWhereClause = "WorkflowVersionWhereClause"
    WorkflowVersion = "WorkflowVersion"
    WorkflowVersionOrderByClause = "WorkflowVersionOrderByClause"
    WorkflowRunStepWhereClause = "WorkflowRunStepWhereClause"
    WorkflowRunStep = "WorkflowRunStep"
    WorkflowRunStepOrderByClause = "WorkflowRunStepOrderByClause"
    WorkflowRunEntityInputWhereClause = "WorkflowRunEntityInputWhereClause"
    WorkflowRunEntityInput = "WorkflowRunEntityInput"
    WorkflowRunEntityInputOrderByClause = "WorkflowRunEntityInputOrderByClause"
    pass


"""
------------------------------------------------------------------------------
Dataloaders
------------------------------------------------------------------------------
These are batching functions for loading related objects to avoid N+1 queries.
"""


@strawberry.field
async def load_workflow_version_rows(
    root: "WorkflowRun",
    info: Info,
    where: Annotated["WorkflowVersionWhereClause", strawberry.lazy("api.types.workflow_version")] | None = None,
    order_by: Optional[
        list[Annotated["WorkflowVersionOrderByClause", strawberry.lazy("api.types.workflow_version")]]
    ] = [],
) -> Optional[Annotated["WorkflowVersion", strawberry.lazy("api.types.workflow_version")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.WorkflowRun)
    relationship = mapper.relationships["workflow_version"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.workflow_version_id)  # type:ignore


@relay.connection(
    relay.ListConnection[Annotated["WorkflowRunStep", strawberry.lazy("api.types.workflow_run_step")]]  # type:ignore
)
async def load_workflow_run_step_rows(
    root: "WorkflowRun",
    info: Info,
    where: Annotated["WorkflowRunStepWhereClause", strawberry.lazy("api.types.workflow_run_step")] | None = None,
    order_by: Optional[
        list[Annotated["WorkflowRunStepOrderByClause", strawberry.lazy("api.types.workflow_run_step")]]
    ] = [],
) -> Sequence[Annotated["WorkflowRunStep", strawberry.lazy("api.types.workflow_run_step")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.WorkflowRun)
    relationship = mapper.relationships["steps"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.id)  # type:ignore


@strawberry.field
async def load_workflow_run_step_aggregate_rows(
    root: "WorkflowRun",
    info: Info,
    where: Annotated["WorkflowRunStepWhereClause", strawberry.lazy("api.types.workflow_run_step")] | None = None,
) -> Optional[Annotated["WorkflowRunStepAggregate", strawberry.lazy("api.types.workflow_run_step")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.WorkflowRun)
    relationship = mapper.relationships["steps"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    # Aggregate queries always return a single row, so just grab the first one
    result = rows[0] if rows else None
    aggregate_output = format_workflow_run_step_aggregate_output(result)
    return WorkflowRunStepAggregate(aggregate=aggregate_output)


@relay.connection(
    relay.ListConnection[
        Annotated["WorkflowRunEntityInput", strawberry.lazy("api.types.workflow_run_entity_input")]
    ]  # type:ignore
)
async def load_workflow_run_entity_input_rows(
    root: "WorkflowRun",
    info: Info,
    where: Annotated["WorkflowRunEntityInputWhereClause", strawberry.lazy("api.types.workflow_run_entity_input")]
    | None = None,
    order_by: Optional[
        list[Annotated["WorkflowRunEntityInputOrderByClause", strawberry.lazy("api.types.workflow_run_entity_input")]]
    ] = [],
) -> Sequence[Annotated["WorkflowRunEntityInput", strawberry.lazy("api.types.workflow_run_entity_input")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.WorkflowRun)
    relationship = mapper.relationships["entity_inputs"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.id)  # type:ignore


@strawberry.field
async def load_workflow_run_entity_input_aggregate_rows(
    root: "WorkflowRun",
    info: Info,
    where: Annotated["WorkflowRunEntityInputWhereClause", strawberry.lazy("api.types.workflow_run_entity_input")]
    | None = None,
) -> Optional[Annotated["WorkflowRunEntityInputAggregate", strawberry.lazy("api.types.workflow_run_entity_input")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.WorkflowRun)
    relationship = mapper.relationships["entity_inputs"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    # Aggregate queries always return a single row, so just grab the first one
    result = rows[0] if rows else None
    aggregate_output = format_workflow_run_entity_input_aggregate_output(result)
    return WorkflowRunEntityInputAggregate(aggregate=aggregate_output)


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
class WorkflowRunWhereClauseMutations(TypedDict):
    id: UUIDComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class WorkflowRunWhereClause(TypedDict):
    started_at: Optional[DatetimeComparators] | None
    ended_at: Optional[DatetimeComparators] | None
    execution_id: Optional[StrComparators] | None
    outputs_json: Optional[StrComparators] | None
    workflow_runner_inputs_json: Optional[StrComparators] | None
    status: Optional[EnumComparators[WorkflowRunStatus]] | None
    workflow_version: Optional[
        Annotated["WorkflowVersionWhereClause", strawberry.lazy("api.types.workflow_version")]
    ] | None
    steps: Optional[Annotated["WorkflowRunStepWhereClause", strawberry.lazy("api.types.workflow_run_step")]] | None
    entity_inputs: Optional[
        Annotated["WorkflowRunEntityInputWhereClause", strawberry.lazy("api.types.workflow_run_entity_input")]
    ] | None
    raw_inputs_json: Optional[StrComparators] | None
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
class WorkflowRunOrderByClause(TypedDict):
    started_at: Optional[orderBy] | None
    ended_at: Optional[orderBy] | None
    execution_id: Optional[orderBy] | None
    outputs_json: Optional[orderBy] | None
    workflow_runner_inputs_json: Optional[orderBy] | None
    status: Optional[orderBy] | None
    workflow_version: Optional[
        Annotated["WorkflowVersionOrderByClause", strawberry.lazy("api.types.workflow_version")]
    ] | None
    raw_inputs_json: Optional[orderBy] | None
    deprecated_by: Optional[orderBy] | None
    id: Optional[orderBy] | None
    owner_user_id: Optional[orderBy] | None
    collection_id: Optional[orderBy] | None
    created_at: Optional[orderBy] | None
    updated_at: Optional[orderBy] | None
    deleted_at: Optional[orderBy] | None


"""
Define WorkflowRun type
"""


@strawberry.type
class WorkflowRun(EntityInterface):
    started_at: Optional[datetime.datetime] = None
    ended_at: Optional[datetime.datetime] = None
    execution_id: Optional[str] = None
    outputs_json: Optional[str] = None
    workflow_runner_inputs_json: Optional[str] = None
    status: Optional[WorkflowRunStatus] = None
    workflow_version: Optional[
        Annotated["WorkflowVersion", strawberry.lazy("api.types.workflow_version")]
    ] = load_workflow_version_rows  # type:ignore
    steps: Sequence[
        Annotated["WorkflowRunStep", strawberry.lazy("api.types.workflow_run_step")]
    ] = load_workflow_run_step_rows  # type:ignore
    steps_aggregate: Optional[
        Annotated["WorkflowRunStepAggregate", strawberry.lazy("api.types.workflow_run_step")]
    ] = load_workflow_run_step_aggregate_rows  # type:ignore
    entity_inputs: Sequence[
        Annotated["WorkflowRunEntityInput", strawberry.lazy("api.types.workflow_run_entity_input")]
    ] = load_workflow_run_entity_input_rows  # type:ignore
    entity_inputs_aggregate: Optional[
        Annotated["WorkflowRunEntityInputAggregate", strawberry.lazy("api.types.workflow_run_entity_input")]
    ] = load_workflow_run_entity_input_aggregate_rows  # type:ignore
    raw_inputs_json: Optional[str] = None
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
WorkflowRun.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.WorkflowRun or type(obj) == WorkflowRun
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
class WorkflowRunNumericalColumns:
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class WorkflowRunMinMaxColumns:
    started_at: Optional[datetime.datetime] = None
    ended_at: Optional[datetime.datetime] = None
    execution_id: Optional[str] = None
    outputs_json: Optional[str] = None
    workflow_runner_inputs_json: Optional[str] = None
    raw_inputs_json: Optional[str] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class WorkflowRunCountColumns(enum.Enum):
    started_at = "started_at"
    ended_at = "ended_at"
    execution_id = "execution_id"
    outputs_json = "outputs_json"
    workflow_runner_inputs_json = "workflow_runner_inputs_json"
    status = "status"
    workflow_version = "workflow_version"
    steps = "steps"
    entity_inputs = "entity_inputs"
    raw_inputs_json = "raw_inputs_json"
    deprecated_by = "deprecated_by"
    id = "id"
    owner_user_id = "owner_user_id"
    collection_id = "collection_id"
    created_at = "created_at"
    updated_at = "updated_at"
    deleted_at = "deleted_at"


"""
All supported aggregation functions
"""


@strawberry.type
class WorkflowRunAggregateFunctions:
    # This is a hack to accept "distinct" and "columns" as arguments to "count"
    @strawberry.field
    def count(
        self, distinct: Optional[bool] = False, columns: Optional[WorkflowRunCountColumns] = None
    ) -> Optional[int]:
        # Count gets set with the proper value in the resolver, so we just return it here
        return self.count  # type: ignore

    sum: Optional[WorkflowRunNumericalColumns] = None
    avg: Optional[WorkflowRunNumericalColumns] = None
    min: Optional[WorkflowRunMinMaxColumns] = None
    max: Optional[WorkflowRunMinMaxColumns] = None
    stddev: Optional[WorkflowRunNumericalColumns] = None
    variance: Optional[WorkflowRunNumericalColumns] = None


"""
Wrapper around WorkflowRunAggregateFunctions
"""


@strawberry.type
class WorkflowRunAggregate:
    aggregate: Optional[WorkflowRunAggregateFunctions] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class WorkflowRunCreateInput:
    ended_at: Optional[datetime.datetime] = None
    execution_id: Optional[str] = None
    outputs_json: Optional[str] = None
    workflow_runner_inputs_json: Optional[str] = None
    status: Optional[WorkflowRunStatus] = None
    workflow_version_id: Optional[strawberry.ID] = None
    raw_inputs_json: Optional[str] = None
    deprecated_by_id: Optional[strawberry.ID] = None
    collection_id: Optional[int] = None


@strawberry.input()
class WorkflowRunUpdateInput:
    ended_at: Optional[datetime.datetime] = None
    execution_id: Optional[str] = None
    outputs_json: Optional[str] = None
    workflow_runner_inputs_json: Optional[str] = None
    status: Optional[WorkflowRunStatus] = None
    deprecated_by_id: Optional[strawberry.ID] = None


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_workflow_runs(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[WorkflowRunWhereClause] = None,
    order_by: Optional[list[WorkflowRunOrderByClause]] = [],
) -> typing.Sequence[WorkflowRun]:
    """
    Resolve WorkflowRun objects. Used for queries (see api/queries.py).
    """
    return await get_db_rows(db.WorkflowRun, session, cerbos_client, principal, where, order_by)  # type: ignore


def format_workflow_run_aggregate_output(query_results: RowMapping) -> WorkflowRunAggregateFunctions:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = WorkflowRunAggregateFunctions()
    for aggregate_name, value in query_results.items():
        if aggregate_name == "count":
            output.count = value
        else:
            aggregator_fn, col_name = aggregate_name.split("_", 1)
            # Filter out the group_by key from the results if one was provided.
            if aggregator_fn in aggregator_map.keys():
                if not getattr(output, aggregator_fn):
                    if aggregate_name in ["min", "max"]:
                        setattr(output, aggregator_fn, WorkflowRunMinMaxColumns())
                    else:
                        setattr(output, aggregator_fn, WorkflowRunNumericalColumns())
                setattr(getattr(output, aggregator_fn), col_name, value)
    return output


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_workflow_runs_aggregate(
    info: Info,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[WorkflowRunWhereClause] = None,
) -> WorkflowRunAggregate:
    """
    Aggregate values for WorkflowRun objects. Used for queries (see api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on
    # TODO: not sure why selected_fields is a list
    # The first list of selections will always be ["aggregate"], so just grab the first item
    selections = info.selected_fields[0].selections[0].selections
    rows = await get_aggregate_db_rows(db.WorkflowRun, session, cerbos_client, principal, where, selections, [])  # type: ignore
    aggregate_output = format_workflow_run_aggregate_output(rows)
    return WorkflowRunAggregate(aggregate=aggregate_output)


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_workflow_run(
    input: WorkflowRunCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> db.Entity:
    """
    Create a new WorkflowRun object. Used for mutations (see api/mutations.py).
    """
    params = input.__dict__

    # Validate that the user can read all of the entities they're linking to.
    # If we have any system_writable fields present, make sure that our auth'd user *is* a system user
    if not is_system_user:
        input.ended_at = None
        input.execution_id = None
        input.outputs_json = None
        input.workflow_runner_inputs_json = None
        input.status = None
    # Validate that the user can create entities in this collection
    attr = {"collection_id": input.collection_id}
    resource = Resource(id="NEW_ID", kind=db.WorkflowRun.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise PlatformicsException("Unauthorized: Cannot create entity in this collection")

    # Validate that the user can read all of the entities they're linking to.
    # Check that workflow_version relationship is accessible.
    if input.workflow_version_id:
        workflow_version = await get_db_rows(
            db.WorkflowVersion,
            session,
            cerbos_client,
            principal,
            {"id": {"_eq": input.workflow_version_id}},
            [],
            CerbosAction.VIEW,
        )
        if not workflow_version:
            raise PlatformicsException("Unauthorized: workflow_version does not exist")
    # Check that deprecated_by relationship is accessible.
    if input.deprecated_by_id:
        deprecated_by = await get_db_rows(
            db.WorkflowRun,
            session,
            cerbos_client,
            principal,
            {"id": {"_eq": input.deprecated_by_id}},
            [],
            CerbosAction.VIEW,
        )
        if not deprecated_by:
            raise PlatformicsException("Unauthorized: deprecated_by does not exist")

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.WorkflowRun(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_workflow_run(
    input: WorkflowRunUpdateInput,
    where: WorkflowRunWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> Sequence[db.Entity]:
    """
    Update WorkflowRun objects. Used for mutations (see api/mutations.py).
    """
    params = input.__dict__

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise PlatformicsException("No fields to update")

    # Validate that the user can read all of the entities they're linking to.
    # Check that deprecated_by relationship is accessible.
    if input.deprecated_by_id:
        deprecated_by = await get_db_rows(
            db.WorkflowRun,
            session,
            cerbos_client,
            principal,
            {"id": {"_eq": input.deprecated_by_id}},
            [],
            CerbosAction.VIEW,
        )
        if not deprecated_by:
            raise PlatformicsException("Unauthorized: deprecated_by does not exist")
        params["deprecated_by"] = deprecated_by[0]
        del params["deprecated_by_id"]
    # If we have any system_writable fields present, make sure that our auth'd user *is* a system user
    if not is_system_user:
        del params["ended_at"]
        del params["execution_id"]
        del params["outputs_json"]
        del params["workflow_runner_inputs_json"]
        del params["status"]

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(db.WorkflowRun, session, cerbos_client, principal, where, [], CerbosAction.UPDATE)
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot update entities")

    # Update DB
    for entity in entities:
        for key in params:
            if params[key]:
                setattr(entity, key, params[key])
    await session.commit()
    return entities


@strawberry.mutation(extensions=[DependencyExtension()])
async def delete_workflow_run(
    where: WorkflowRunWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Delete WorkflowRun objects. Used for mutations (see api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(db.WorkflowRun, session, cerbos_client, principal, where, [], CerbosAction.DELETE)
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
