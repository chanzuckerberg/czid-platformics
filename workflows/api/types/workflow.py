"""
GraphQL type for Workflow

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
from api.validators.workflow import WorkflowCreateInputValidator, WorkflowUpdateInputValidator
from api.helpers.workflow import WorkflowGroupByOptions, build_workflow_groupby_output
from api.types.entities import EntityInterface
from api.types.workflow_version import WorkflowVersionAggregate, format_workflow_version_aggregate_output
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
    from api.types.workflow_version import WorkflowVersionOrderByClause, WorkflowVersionWhereClause, WorkflowVersion

    pass
else:
    WorkflowVersionWhereClause = "WorkflowVersionWhereClause"
    WorkflowVersion = "WorkflowVersion"
    WorkflowVersionOrderByClause = "WorkflowVersionOrderByClause"
    pass


"""
------------------------------------------------------------------------------
Dataloaders
------------------------------------------------------------------------------
These are batching functions for loading related objects to avoid N+1 queries.
"""


@relay.connection(
    relay.ListConnection[Annotated["WorkflowVersion", strawberry.lazy("api.types.workflow_version")]]  # type:ignore
)
async def load_workflow_version_rows(
    root: "Workflow",
    info: Info,
    where: Annotated["WorkflowVersionWhereClause", strawberry.lazy("api.types.workflow_version")] | None = None,
    order_by: Optional[
        list[Annotated["WorkflowVersionOrderByClause", strawberry.lazy("api.types.workflow_version")]]
    ] = [],
) -> Sequence[Annotated["WorkflowVersion", strawberry.lazy("api.types.workflow_version")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Workflow)
    relationship = mapper.relationships["versions"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.id)  # type:ignore


@strawberry.field
async def load_workflow_version_aggregate_rows(
    root: "Workflow",
    info: Info,
    where: Annotated["WorkflowVersionWhereClause", strawberry.lazy("api.types.workflow_version")] | None = None,
) -> Optional[Annotated["WorkflowVersionAggregate", strawberry.lazy("api.types.workflow_version")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Workflow)
    relationship = mapper.relationships["versions"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    aggregate_output = format_workflow_version_aggregate_output(rows)
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
class WorkflowWhereClauseMutations(TypedDict):
    id: UUIDComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class WorkflowWhereClause(TypedDict):
    name: Optional[StrComparators] | None
    default_version: Optional[StrComparators] | None
    minimum_supported_version: Optional[StrComparators] | None
    versions: Optional[Annotated["WorkflowVersionWhereClause", strawberry.lazy("api.types.workflow_version")]] | None
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
class WorkflowOrderByClause(TypedDict):
    name: Optional[orderBy] | None
    default_version: Optional[orderBy] | None
    minimum_supported_version: Optional[orderBy] | None
    id: Optional[orderBy] | None
    owner_user_id: Optional[orderBy] | None
    collection_id: Optional[orderBy] | None
    created_at: Optional[orderBy] | None
    updated_at: Optional[orderBy] | None
    deleted_at: Optional[orderBy] | None


"""
Define Workflow type
"""


@strawberry.type
class Workflow(EntityInterface):
    name: Optional[str] = None
    default_version: Optional[str] = None
    minimum_supported_version: Optional[str] = None
    versions: Sequence[
        Annotated["WorkflowVersion", strawberry.lazy("api.types.workflow_version")]
    ] = load_workflow_version_rows  # type:ignore
    versions_aggregate: Optional[
        Annotated["WorkflowVersionAggregate", strawberry.lazy("api.types.workflow_version")]
    ] = load_workflow_version_aggregate_rows  # type:ignore
    id: strawberry.ID
    owner_user_id: int
    collection_id: Optional[int] = None
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None


"""
We need to add this to each Queryable type so that strawberry will accept either our
Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
"""
Workflow.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.Workflow or type(obj) == Workflow
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
class WorkflowNumericalColumns:
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class WorkflowMinMaxColumns:
    name: Optional[str] = None
    default_version: Optional[str] = None
    minimum_supported_version: Optional[str] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class WorkflowCountColumns(enum.Enum):
    name = "name"
    defaultVersion = "default_version"
    minimumSupportedVersion = "minimum_supported_version"
    versions = "versions"
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
class WorkflowAggregateFunctions:
    # This is a hack to accept "distinct" and "columns" as arguments to "count"
    @strawberry.field
    def count(self, distinct: Optional[bool] = False, columns: Optional[WorkflowCountColumns] = None) -> Optional[int]:
        # Count gets set with the proper value in the resolver, so we just return it here
        return self.count  # type: ignore

    sum: Optional[WorkflowNumericalColumns] = None
    avg: Optional[WorkflowNumericalColumns] = None
    stddev: Optional[WorkflowNumericalColumns] = None
    variance: Optional[WorkflowNumericalColumns] = None
    min: Optional[WorkflowMinMaxColumns] = None
    max: Optional[WorkflowMinMaxColumns] = None
    groupBy: Optional[WorkflowGroupByOptions] = None


"""
Wrapper around WorkflowAggregateFunctions
"""


@strawberry.type
class WorkflowAggregate:
    aggregate: Optional[list[WorkflowAggregateFunctions]] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class WorkflowCreateInput:
    name: Optional[str] = None
    default_version: Optional[str] = None
    minimum_supported_version: Optional[str] = None
    collection_id: Optional[int] = None
    deleted_at: Optional[datetime.datetime] = None


@strawberry.input()
class WorkflowUpdateInput:
    name: Optional[str] = None
    default_version: Optional[str] = None
    minimum_supported_version: Optional[str] = None
    deleted_at: Optional[datetime.datetime] = None


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_workflows(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[WorkflowWhereClause] = None,
    order_by: Optional[list[WorkflowOrderByClause]] = [],
    limit_offset: Optional[LimitOffsetClause] = None,
) -> typing.Sequence[Workflow]:
    """
    Resolve Workflow objects. Used for queries (see api/queries.py).
    """
    limit = limit_offset["limit"] if limit_offset and "limit" in limit_offset else None
    offset = limit_offset["offset"] if limit_offset and "offset" in limit_offset else None
    if offset and not limit:
        raise PlatformicsException("Cannot use offset without limit")
    return await get_db_rows(db.Workflow, session, cerbos_client, principal, where, order_by, CerbosAction.VIEW, limit, offset)  # type: ignore


def format_workflow_aggregate_output(query_results: Sequence[RowMapping] | RowMapping) -> WorkflowAggregate:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    aggregate = []
    if type(query_results) is not list:
        query_results = [query_results]  # type: ignore
    for row in query_results:
        aggregate.append(format_workflow_aggregate_row(row))
    return WorkflowAggregate(aggregate=aggregate)


def format_workflow_aggregate_row(row: RowMapping) -> WorkflowAggregateFunctions:
    """
    Given a single row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = WorkflowAggregateFunctions()
    for key, value in row.items():
        # Key is either an aggregate function or a groupby key
        group_keys = key.split(".")
        aggregate = key.split("_", 1)
        if aggregate[0] not in aggregator_map.keys():
            # Turn list of groupby keys into nested objects
            if not getattr(output, "groupBy"):
                setattr(output, "groupBy", WorkflowGroupByOptions())
            group = build_workflow_groupby_output(getattr(output, "groupBy"), group_keys, value)
            setattr(output, "groupBy", group)
        else:
            aggregate_name = aggregate[0]
            if aggregate_name == "count":
                output.count = value
            else:
                aggregator_fn, col_name = aggregate[0], aggregate[1]
                if not getattr(output, aggregator_fn):
                    if aggregate_name in ["min", "max"]:
                        setattr(output, aggregator_fn, WorkflowMinMaxColumns())
                    else:
                        setattr(output, aggregator_fn, WorkflowNumericalColumns())
                setattr(getattr(output, aggregator_fn), col_name, value)
    return output


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_workflows_aggregate(
    info: Info,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[WorkflowWhereClause] = None,
    # TODO: add support for groupby, limit/offset
) -> WorkflowAggregate:
    """
    Aggregate values for Workflow objects. Used for queries (see api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on, and groupby options if any were provided.
    # TODO: not sure why selected_fields is a list
    selections = info.selected_fields[0].selections[0].selections
    aggregate_selections = [selection for selection in selections if getattr(selection, "name") != "groupBy"]
    groupby_selections = [selection for selection in selections if getattr(selection, "name") == "groupBy"]
    groupby_selections = groupby_selections[0].selections if groupby_selections else []

    if not aggregate_selections:
        raise PlatformicsException("No aggregate functions selected")

    rows = await get_aggregate_db_rows(db.Workflow, session, cerbos_client, principal, where, aggregate_selections, [], groupby_selections)  # type: ignore
    aggregate_output = format_workflow_aggregate_output(rows)
    return aggregate_output


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_workflow(
    input: WorkflowCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> db.Entity:
    """
    Create a new Workflow object. Used for mutations (see api/mutations.py).
    """
    validated = WorkflowCreateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Validate that the user can read all of the entities they're linking to.
    # If we have any system_writable fields present, make sure that our auth'd user *is* a system user
    if not is_system_user:
        raise PlatformicsException("Unauthorized: Workflow is not creatable")
    # Validate that the user can create entities in this collection
    attr = {"collection_id": validated.collection_id, "owner_user_id": int(principal.id)}
    resource = Resource(id="NEW_ID", kind=db.Workflow.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise PlatformicsException("Unauthorized: Cannot create entity in this collection")

    # Validate that the user can read all of the entities they're linking to.

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.Workflow(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_workflow(
    input: WorkflowUpdateInput,
    where: WorkflowWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> Sequence[db.Entity]:
    """
    Update Workflow objects. Used for mutations (see api/mutations.py).
    """
    validated = WorkflowUpdateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise PlatformicsException("No fields to update")

    # Validate that the user can read all of the entities they're linking to.
    # If we have any system_writable fields present, make sure that our auth'd user *is* a system user
    if not is_system_user:
        raise PlatformicsException("Unauthorized: Workflow is not mutable")

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(db.Workflow, session, cerbos_client, principal, where, [], CerbosAction.UPDATE)
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
async def delete_workflow(
    where: WorkflowWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Delete Workflow objects. Used for mutations (see api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(db.Workflow, session, cerbos_client, principal, where, [], CerbosAction.DELETE)
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
