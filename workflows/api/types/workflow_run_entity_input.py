"""
GraphQL type for WorkflowRunEntityInput

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
from api.validators.workflow_run_entity_input import (
    WorkflowRunEntityInputCreateInputValidator,
)
from api.helpers.workflow_run_entity_input import (
    WorkflowRunEntityInputGroupByOptions,
    build_workflow_run_entity_input_groupby_output,
)
from api.types.entities import EntityInterface
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
from strawberry.types import Info
from support.limit_offset import LimitOffsetClause
from typing_extensions import TypedDict
import enum


E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.workflow_run import WorkflowRunOrderByClause, WorkflowRunWhereClause, WorkflowRun

    pass
else:
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
async def load_workflow_run_rows(
    root: "WorkflowRunEntityInput",
    info: Info,
    where: Annotated["WorkflowRunWhereClause", strawberry.lazy("api.types.workflow_run")] | None = None,
    order_by: Optional[list[Annotated["WorkflowRunOrderByClause", strawberry.lazy("api.types.workflow_run")]]] = [],
) -> Optional[Annotated["WorkflowRun", strawberry.lazy("api.types.workflow_run")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.WorkflowRunEntityInput)
    relationship = mapper.relationships["workflow_run"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.workflow_run_id)  # type:ignore


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
class WorkflowRunEntityInputWhereClauseMutations(TypedDict):
    id: UUIDComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class WorkflowRunEntityInputWhereClause(TypedDict):
    input_entity_id: Optional[UUIDComparators] | None
    field_name: Optional[StrComparators] | None
    entity_type: Optional[StrComparators] | None
    workflow_run: Optional[Annotated["WorkflowRunWhereClause", strawberry.lazy("api.types.workflow_run")]] | None
    id: Optional[UUIDComparators] | None
    owner_user_id: Optional[IntComparators] | None
    collection_id: Optional[IntComparators] | None
    created_at: Optional[DatetimeComparators] | None
    updated_at: Optional[DatetimeComparators] | None


"""
Supported ORDER BY clause attributes
"""


@strawberry.input
class WorkflowRunEntityInputOrderByClause(TypedDict):
    input_entity_id: Optional[orderBy] | None
    field_name: Optional[orderBy] | None
    entity_type: Optional[orderBy] | None
    workflow_run: Optional[Annotated["WorkflowRunOrderByClause", strawberry.lazy("api.types.workflow_run")]] | None
    id: Optional[orderBy] | None
    owner_user_id: Optional[orderBy] | None
    collection_id: Optional[orderBy] | None
    created_at: Optional[orderBy] | None
    updated_at: Optional[orderBy] | None


"""
Define WorkflowRunEntityInput type
"""


@strawberry.type
class WorkflowRunEntityInput(EntityInterface):
    input_entity_id: Optional[strawberry.ID] = None
    field_name: Optional[str] = None
    entity_type: Optional[str] = None
    workflow_run: Optional[
        Annotated["WorkflowRun", strawberry.lazy("api.types.workflow_run")]
    ] = load_workflow_run_rows  # type:ignore
    id: strawberry.ID
    owner_user_id: int
    collection_id: int
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None


"""
We need to add this to each Queryable type so that strawberry will accept either our
Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
"""
WorkflowRunEntityInput.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.WorkflowRunEntityInput or type(obj) == WorkflowRunEntityInput
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
class WorkflowRunEntityInputNumericalColumns:
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class WorkflowRunEntityInputMinMaxColumns:
    field_name: Optional[str] = None
    entity_type: Optional[str] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class WorkflowRunEntityInputCountColumns(enum.Enum):
    inputEntityId = "input_entity_id"
    fieldName = "field_name"
    entityType = "entity_type"
    workflowRun = "workflow_run"
    id = "id"
    ownerUserId = "owner_user_id"
    collectionId = "collection_id"
    createdAt = "created_at"
    updatedAt = "updated_at"


"""
All supported aggregation functions
"""


@strawberry.type
class WorkflowRunEntityInputAggregateFunctions:
    # This is a hack to accept "distinct" and "columns" as arguments to "count"
    @strawberry.field
    def count(
        self, distinct: Optional[bool] = False, columns: Optional[WorkflowRunEntityInputCountColumns] = None
    ) -> Optional[int]:
        # Count gets set with the proper value in the resolver, so we just return it here
        return self.count  # type: ignore

    sum: Optional[WorkflowRunEntityInputNumericalColumns] = None
    avg: Optional[WorkflowRunEntityInputNumericalColumns] = None
    stddev: Optional[WorkflowRunEntityInputNumericalColumns] = None
    variance: Optional[WorkflowRunEntityInputNumericalColumns] = None
    min: Optional[WorkflowRunEntityInputMinMaxColumns] = None
    max: Optional[WorkflowRunEntityInputMinMaxColumns] = None
    groupBy: Optional[WorkflowRunEntityInputGroupByOptions] = None


"""
Wrapper around WorkflowRunEntityInputAggregateFunctions
"""


@strawberry.type
class WorkflowRunEntityInputAggregate:
    aggregate: Optional[list[WorkflowRunEntityInputAggregateFunctions]] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class WorkflowRunEntityInputCreateInput:
    input_entity_id: Optional[strawberry.ID] = None
    field_name: Optional[str] = None
    entity_type: Optional[str] = None
    workflow_run_id: Optional[strawberry.ID] = None
    collection_id: int


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_workflow_run_entity_inputs(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[WorkflowRunEntityInputWhereClause] = None,
    order_by: Optional[list[WorkflowRunEntityInputOrderByClause]] = [],
    limit_offset: Optional[LimitOffsetClause] = None,
) -> typing.Sequence[WorkflowRunEntityInput]:
    """
    Resolve WorkflowRunEntityInput objects. Used for queries (see api/queries.py).
    """
    limit = limit_offset["limit"] if limit_offset and "limit" in limit_offset else None
    offset = limit_offset["offset"] if limit_offset and "offset" in limit_offset else None
    if offset and not limit:
        raise PlatformicsException("Cannot use offset without limit")
    return await get_db_rows(db.WorkflowRunEntityInput, session, cerbos_client, principal, where, order_by, CerbosAction.VIEW, limit, offset)  # type: ignore


def format_workflow_run_entity_input_aggregate_output(
    query_results: Sequence[RowMapping] | RowMapping,
) -> WorkflowRunEntityInputAggregate:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    aggregate = []
    if type(query_results) is not list:
        query_results = [query_results]  # type: ignore
    for row in query_results:
        aggregate.append(format_workflow_run_entity_input_aggregate_row(row))
    return WorkflowRunEntityInputAggregate(aggregate=aggregate)


def format_workflow_run_entity_input_aggregate_row(row: RowMapping) -> WorkflowRunEntityInputAggregateFunctions:
    """
    Given a single row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = WorkflowRunEntityInputAggregateFunctions()
    for key, value in row.items():
        # Key is either an aggregate function or a groupby key
        group_keys = key.split(".")
        aggregate = key.split("_", 1)
        if aggregate[0] not in aggregator_map.keys():
            # Turn list of groupby keys into nested objects
            if not getattr(output, "groupBy"):
                setattr(output, "groupBy", WorkflowRunEntityInputGroupByOptions())
            group = build_workflow_run_entity_input_groupby_output(getattr(output, "groupBy"), group_keys, value)
            setattr(output, "groupBy", group)
        else:
            aggregate_name = aggregate[0]
            if aggregate_name == "count":
                output.count = value
            else:
                aggregator_fn, col_name = aggregate[0], aggregate[1]
                if not getattr(output, aggregator_fn):
                    if aggregate_name in ["min", "max"]:
                        setattr(output, aggregator_fn, WorkflowRunEntityInputMinMaxColumns())
                    else:
                        setattr(output, aggregator_fn, WorkflowRunEntityInputNumericalColumns())
                setattr(getattr(output, aggregator_fn), col_name, value)
    return output


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_workflow_run_entity_inputs_aggregate(
    info: Info,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[WorkflowRunEntityInputWhereClause] = None,
    # TODO: add support for groupby, limit/offset
) -> WorkflowRunEntityInputAggregate:
    """
    Aggregate values for WorkflowRunEntityInput objects. Used for queries (see api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on, and groupby options if any were provided.
    # TODO: not sure why selected_fields is a list
    selections = info.selected_fields[0].selections[0].selections
    aggregate_selections = [selection for selection in selections if getattr(selection, "name") != "groupBy"]
    groupby_selections = [selection for selection in selections if getattr(selection, "name") == "groupBy"]
    groupby_selections = groupby_selections[0].selections if groupby_selections else []

    if not aggregate_selections:
        raise PlatformicsException("No aggregate functions selected")

    rows = await get_aggregate_db_rows(db.WorkflowRunEntityInput, session, cerbos_client, principal, where, aggregate_selections, [], groupby_selections)  # type: ignore
    aggregate_output = format_workflow_run_entity_input_aggregate_output(rows)
    return aggregate_output


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_workflow_run_entity_input(
    input: WorkflowRunEntityInputCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> db.Entity:
    """
    Create a new WorkflowRunEntityInput object. Used for mutations (see api/mutations.py).
    """
    validated = WorkflowRunEntityInputCreateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Validate that the user can read all of the entities they're linking to.
    # Validate that the user can create entities in this collection
    attr = {"collection_id": validated.collection_id}
    resource = Resource(id="NEW_ID", kind=db.WorkflowRunEntityInput.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise PlatformicsException("Unauthorized: Cannot create entity in this collection")

    # Validate that the user can read all of the entities they're linking to.
    # Check that workflow_run relationship is accessible.
    if validated.workflow_run_id:
        workflow_run = await get_db_rows(
            db.WorkflowRun,
            session,
            cerbos_client,
            principal,
            {"id": {"_eq": validated.workflow_run_id}},
            [],
            CerbosAction.VIEW,
        )
        if not workflow_run:
            raise PlatformicsException("Unauthorized: workflow_run does not exist")

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.WorkflowRunEntityInput(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def delete_workflow_run_entity_input(
    where: WorkflowRunEntityInputWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Delete WorkflowRunEntityInput objects. Used for mutations (see api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(
        db.WorkflowRunEntityInput, session, cerbos_client, principal, where, [], CerbosAction.DELETE
    )
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
