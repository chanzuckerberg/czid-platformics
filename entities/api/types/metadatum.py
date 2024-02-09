"""
GraphQL type for Metadatum

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
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal
from fastapi import Depends
from platformics.api.core.errors import PlatformicsException
from platformics.api.core.deps import get_cerbos_client, get_db_session, require_auth_principal, is_system_user
from platformics.api.core.gql_to_sql import (
    aggregator_map,
    orderBy,
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
    from api.types.sample import SampleOrderByClause, SampleWhereClause, Sample

    pass
else:
    SampleWhereClause = "SampleWhereClause"
    Sample = "Sample"
    SampleOrderByClause = "SampleOrderByClause"
    pass


"""
------------------------------------------------------------------------------
Dataloaders
------------------------------------------------------------------------------
These are batching functions for loading related objects to avoid N+1 queries.
"""


@strawberry.field
async def load_sample_rows(
    root: "Metadatum",
    info: Info,
    where: Annotated["SampleWhereClause", strawberry.lazy("api.types.sample")] | None = None,
    order_by: Optional[list[Annotated["SampleOrderByClause", strawberry.lazy("api.types.sample")]]] = [],
) -> Optional[Annotated["Sample", strawberry.lazy("api.types.sample")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Metadatum)
    relationship = mapper.relationships["sample"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.sample_id)  # type:ignore


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
class MetadatumWhereClauseMutations(TypedDict):
    id: UUIDComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class MetadatumWhereClause(TypedDict):
    id: UUIDComparators | None
    producing_run_id: IntComparators | None
    owner_user_id: IntComparators | None
    collection_id: IntComparators | None
    sample: Optional[Annotated["SampleWhereClause", strawberry.lazy("api.types.sample")]] | None
    field_name: Optional[StrComparators] | None
    value: Optional[StrComparators] | None
    entity_id: Optional[UUIDComparators] | None


"""
Supported ORDER BY clause attributes
"""


@strawberry.input
class MetadatumOrderByClause(TypedDict):
    sample: Optional[Annotated["SampleOrderByClause", strawberry.lazy("api.types.sample")]] | None
    field_name: Optional[orderBy] | None
    value: Optional[orderBy] | None
    id: Optional[orderBy] | None
    producing_run_id: Optional[orderBy] | None
    owner_user_id: Optional[orderBy] | None
    collection_id: Optional[orderBy] | None
    created_at: Optional[orderBy] | None
    updated_at: Optional[orderBy] | None
    deleted_at: Optional[orderBy] | None


"""
Define Metadatum type
"""


@strawberry.type
class Metadatum(EntityInterface):
    sample: Optional[Annotated["Sample", strawberry.lazy("api.types.sample")]] = load_sample_rows  # type:ignore
    field_name: str
    value: str
    id: strawberry.ID
    producing_run_id: Optional[strawberry.ID] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None


"""
We need to add this to each Queryable type so that strawberry will accept either our
Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
"""
Metadatum.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.Metadatum or type(obj) == Metadatum
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
class MetadatumNumericalColumns:
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class MetadatumMinMaxColumns:
    field_name: Optional[str] = None
    value: Optional[str] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class MetadatumCountColumns(enum.Enum):
    sample = "sample"
    field_name = "field_name"
    value = "value"
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
class MetadatumAggregateFunctions:
    # This is a hack to accept "distinct" and "columns" as arguments to "count"
    @strawberry.field
    def count(self, distinct: Optional[bool] = False, columns: Optional[MetadatumCountColumns] = None) -> Optional[int]:
        # Count gets set with the proper value in the resolver, so we just return it here
        return self.count  # type: ignore

    sum: Optional[MetadatumNumericalColumns] = None
    avg: Optional[MetadatumNumericalColumns] = None
    min: Optional[MetadatumMinMaxColumns] = None
    max: Optional[MetadatumMinMaxColumns] = None
    stddev: Optional[MetadatumNumericalColumns] = None
    variance: Optional[MetadatumNumericalColumns] = None


"""
Wrapper around MetadatumAggregateFunctions
"""


@strawberry.type
class MetadatumAggregate:
    aggregate: Optional[MetadatumAggregateFunctions] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class MetadatumCreateInput:
    sample_id: Optional[strawberry.ID] = None
    field_name: Optional[str] = None
    value: Optional[str] = None
    producing_run_id: Optional[strawberry.ID] = None
    collection_id: Optional[int] = None


@strawberry.input()
class MetadatumUpdateInput:
    value: Optional[str] = None


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_metadatas(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[MetadatumWhereClause] = None,
    order_by: Optional[list[MetadatumOrderByClause]] = [],
) -> typing.Sequence[Metadatum]:
    """
    Resolve Metadatum objects. Used for queries (see api/queries.py).
    """
    return await get_db_rows(db.Metadatum, session, cerbos_client, principal, where, order_by)  # type: ignore


def format_metadatum_aggregate_output(query_results: RowMapping) -> MetadatumAggregateFunctions:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = MetadatumAggregateFunctions()
    for aggregate_name, value in query_results.items():
        if aggregate_name == "count":
            output.count = value
        else:
            aggregator_fn, col_name = aggregate_name.split("_", 1)
            # Filter out the group_by key from the results if one was provided.
            if aggregator_fn in aggregator_map.keys():
                if not getattr(output, aggregator_fn):
                    if aggregate_name in ["min", "max"]:
                        setattr(output, aggregator_fn, MetadatumMinMaxColumns())
                    else:
                        setattr(output, aggregator_fn, MetadatumNumericalColumns())
                setattr(getattr(output, aggregator_fn), col_name, value)
    return output


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_metadatas_aggregate(
    info: Info,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[MetadatumWhereClause] = None,
) -> MetadatumAggregate:
    """
    Aggregate values for Metadatum objects. Used for queries (see api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on
    # TODO: not sure why selected_fields is a list
    # The first list of selections will always be ["aggregate"], so just grab the first item
    selections = info.selected_fields[0].selections[0].selections
    rows = await get_aggregate_db_rows(db.Metadatum, session, cerbos_client, principal, where, selections, [])  # type: ignore
    aggregate_output = format_metadatum_aggregate_output(rows)
    return MetadatumAggregate(aggregate=aggregate_output)


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_metadatum(
    input: MetadatumCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> db.Entity:
    """
    Create a new Metadatum object. Used for mutations (see api/mutations.py).
    """
    params = input.__dict__

    # Validate that the user can read all of the entities they're linking to.
    # Check that sample relationship is accessible.
    if input.sample_id:
        sample = await get_db_rows(
            db.Sample, session, cerbos_client, principal, {"id": {"_eq": input.sample_id}}, [], CerbosAction.VIEW
        )
        if not sample:
            raise PlatformicsException("Unauthorized: sample does not exist")

    # Validate that the user can read all of the entities they're linking to.
    # If we have any system_writable fields present, make sure that our auth'd user *is* a system user
    if not is_system_user:
        input.producing_run_id = None

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.Metadatum(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_metadatum(
    input: MetadatumUpdateInput,
    where: MetadatumWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> Sequence[db.Entity]:
    """
    Update Metadatum objects. Used for mutations (see api/mutations.py).
    """
    params = input.__dict__

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise PlatformicsException("No fields to update")

    # Validate that the user can read all of the entities they're linking to.

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(db.Metadatum, session, cerbos_client, principal, where, [], CerbosAction.UPDATE)
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
async def delete_metadatum(
    where: MetadatumWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Delete Metadatum objects. Used for mutations (see api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(db.Metadatum, session, cerbos_client, principal, where, [], CerbosAction.DELETE)
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
