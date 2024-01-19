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
from platformics.api.core.input_validation import validate_input
from api.validators.workflow_run_entity_input import (
    WorkflowRunEntityInputCreateInputValidator,
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
    deleted_at: Optional[DatetimeComparators] | None


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
    deleted_at: Optional[orderBy] | None


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
    deleted_at: Optional[datetime.datetime] = None


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
    deleted_at: Optional[datetime.datetime] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class WorkflowRunEntityInputCountColumns(enum.Enum):
    input_entity_id = "input_entity_id"
    field_name = "field_name"
    entity_type = "entity_type"
    workflow_run = "workflow_run"
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
    min: Optional[WorkflowRunEntityInputMinMaxColumns] = None
    max: Optional[WorkflowRunEntityInputMinMaxColumns] = None
    stddev: Optional[WorkflowRunEntityInputNumericalColumns] = None
    variance: Optional[WorkflowRunEntityInputNumericalColumns] = None


"""
Wrapper around WorkflowRunEntityInputAggregateFunctions
"""


@strawberry.type
class WorkflowRunEntityInputAggregate:
    aggregate: Optional[WorkflowRunEntityInputAggregateFunctions] = None


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
    collection_id: Optional[int] = None


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
) -> typing.Sequence[WorkflowRunEntityInput]:
    """
    Resolve WorkflowRunEntityInput objects. Used for queries (see api/queries.py).
    """
    return await get_db_rows(db.WorkflowRunEntityInput, session, cerbos_client, principal, where, order_by)  # type: ignore


def format_workflow_run_entity_input_aggregate_output(
    query_results: RowMapping,
) -> WorkflowRunEntityInputAggregateFunctions:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = WorkflowRunEntityInputAggregateFunctions()
    for aggregate_name, value in query_results.items():
        if aggregate_name == "count":
            output.count = value
        else:
            aggregator_fn, col_name = aggregate_name.split("_", 1)
            # Filter out the group_by key from the results if one was provided.
            if aggregator_fn in aggregator_map.keys():
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
) -> WorkflowRunEntityInputAggregate:
    """
    Aggregate values for WorkflowRunEntityInput objects. Used for queries (see api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on
    # TODO: not sure why selected_fields is a list
    # The first list of selections will always be ["aggregate"], so just grab the first item
    selections = info.selected_fields[0].selections[0].selections
    rows = await get_aggregate_db_rows(db.WorkflowRunEntityInput, session, cerbos_client, principal, where, selections, [])  # type: ignore
    aggregate_output = format_workflow_run_entity_input_aggregate_output(rows)
    return WorkflowRunEntityInputAggregate(aggregate=aggregate_output)


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
    params = input.__dict__
    validate_input(input, WorkflowRunEntityInputCreateInputValidator)

    # Validate that the user can read all of the entities they're linking to.
    # Validate that the user can create entities in this collection
    attr = {"collection_id": input.collection_id}
    resource = Resource(id="NEW_ID", kind=db.WorkflowRunEntityInput.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise PlatformicsException("Unauthorized: Cannot create entity in this collection")

    # Validate that the user can read all of the entities they're linking to.
    # Check that workflow_run relationship is accessible.
    if input.workflow_run_id:
        workflow_run = await get_db_rows(
            db.WorkflowRun,
            session,
            cerbos_client,
            principal,
            {"id": {"_eq": input.workflow_run_id}},
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
