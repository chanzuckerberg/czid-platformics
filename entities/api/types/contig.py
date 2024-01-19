"""
GraphQL type for Contig

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


import typing
from typing import TYPE_CHECKING, Annotated, Optional, Sequence

import database.models as db
import strawberry
from platformics.api.core.helpers import get_db_rows, get_aggregate_db_rows
from platformics.api.core.input_validation import validate_input
from api.validators.contig import ContigCreateInputValidator, ContigUpdateInputValidator
from api.types.entities import EntityInterface
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
from strawberry.types import Info
from typing_extensions import TypedDict
import enum

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.sequencing_read import SequencingReadWhereClause, SequencingRead

    pass
else:
    SequencingReadWhereClause = "SequencingReadWhereClause"
    SequencingRead = "SequencingRead"
    pass


"""
------------------------------------------------------------------------------
Dataloaders
------------------------------------------------------------------------------
These are batching functions for loading related objects to avoid N+1 queries.
"""


@strawberry.field
async def load_sequencing_read_rows(
    root: "Contig",
    info: Info,
    where: Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")] | None = None,
) -> Optional[Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Contig)
    relationship = mapper.relationships["sequencing_read"]
    return await dataloader.loader_for(relationship, where).load(root.sequencing_read_id)  # type:ignore


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
class ContigWhereClauseMutations(TypedDict):
    id: UUIDComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class ContigWhereClause(TypedDict):
    id: UUIDComparators | None
    producing_run_id: IntComparators | None
    owner_user_id: IntComparators | None
    collection_id: IntComparators | None
    sequencing_read: Optional[
        Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")]
    ] | None
    sequence: Optional[StrComparators] | None


"""
Define Contig type
"""


@strawberry.type
class Contig(EntityInterface):
    id: strawberry.ID
    producing_run_id: Optional[int]
    owner_user_id: int
    collection_id: int
    sequencing_read: Optional[
        Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]
    ] = load_sequencing_read_rows  # type:ignore
    sequence: str


"""
We need to add this to each Queryable type so that strawberry will accept either our
Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
"""
Contig.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.Contig or type(obj) == Contig
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
class ContigNumericalColumns:
    producing_run_id: Optional[int] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class ContigMinMaxColumns:
    producing_run_id: Optional[int] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    sequence: Optional[str] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class ContigCountColumns(enum.Enum):
    sequencing_read = "sequencing_read"
    sequence = "sequence"
    entity_id = "entity_id"
    id = "id"
    producing_run_id = "producing_run_id"
    owner_user_id = "owner_user_id"
    collection_id = "collection_id"


"""
All supported aggregation functions
"""


@strawberry.type
class ContigAggregateFunctions:
    # This is a hack to accept "distinct" and "columns" as arguments to "count"
    @strawberry.field
    def count(self, distinct: Optional[bool] = False, columns: Optional[ContigCountColumns] = None) -> Optional[int]:
        # Count gets set with the proper value in the resolver, so we just return it here
        return self.count  # type: ignore

    sum: Optional[ContigNumericalColumns] = None
    avg: Optional[ContigNumericalColumns] = None
    min: Optional[ContigMinMaxColumns] = None
    max: Optional[ContigMinMaxColumns] = None
    stddev: Optional[ContigNumericalColumns] = None
    variance: Optional[ContigNumericalColumns] = None


"""
Wrapper around ContigAggregateFunctions
"""


@strawberry.type
class ContigAggregate:
    aggregate: Optional[ContigAggregateFunctions] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class ContigCreateInput:
    collection_id: int
    sequencing_read_id: Optional[strawberry.ID] = None
    sequence: str


@strawberry.input()
class ContigUpdateInput:
    collection_id: Optional[int] = None
    sequencing_read_id: Optional[strawberry.ID] = None
    sequence: Optional[str] = None


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_contigs(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[ContigWhereClause] = None,
) -> typing.Sequence[Contig]:
    """
    Resolve Contig objects. Used for queries (see api/queries.py).
    """
    return await get_db_rows(db.Contig, session, cerbos_client, principal, where, [])  # type: ignore


def format_contig_aggregate_output(query_results: RowMapping) -> ContigAggregateFunctions:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = ContigAggregateFunctions()
    for aggregate_name, value in query_results.items():
        if aggregate_name == "count":
            output.count = value
        else:
            aggregator_fn, col_name = aggregate_name.split("_", 1)
            # Filter out the group_by key from the results if one was provided.
            if aggregator_fn in aggregator_map.keys():
                if not getattr(output, aggregator_fn):
                    if aggregate_name in ["min", "max"]:
                        setattr(output, aggregator_fn, ContigMinMaxColumns())
                    else:
                        setattr(output, aggregator_fn, ContigNumericalColumns())
                setattr(getattr(output, aggregator_fn), col_name, value)
    return output


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_contigs_aggregate(
    info: Info,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[ContigWhereClause] = None,
) -> ContigAggregate:
    """
    Aggregate values for Contig objects. Used for queries (see api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on
    # TODO: not sure why selected_fields is a list
    # The first list of selections will always be ["aggregate"], so just grab the first item
    selections = info.selected_fields[0].selections[0].selections
    rows = await get_aggregate_db_rows(db.Contig, session, cerbos_client, principal, where, selections, [])  # type: ignore
    aggregate_output = format_contig_aggregate_output(rows)
    return ContigAggregate(aggregate=aggregate_output)


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_contig(
    input: ContigCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> db.Entity:
    """
    Create a new Contig object. Used for mutations (see api/mutations.py).
    """
    params = input.__dict__
    validate_input(input, ContigCreateInputValidator)

    # Validate that user can create entity in this collection
    attr = {"collection_id": input.collection_id}
    resource = Resource(id="NEW_ID", kind=db.Contig.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise PlatformicsException("Unauthorized: Cannot create entity in this collection")

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.Contig(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_contig(
    input: ContigUpdateInput,
    where: ContigWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Update Contig objects. Used for mutations (see api/mutations.py).
    """
    params = input.__dict__
    validate_input(input, ContigUpdateInputValidator)

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise PlatformicsException("No fields to update")

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(db.Contig, session, cerbos_client, principal, where, [], CerbosAction.UPDATE)
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot update entities")

    # Validate that the user has access to the new collection ID
    if input.collection_id:
        attr = {"collection_id": input.collection_id}
        resource = Resource(id="SOME_ID", kind=db.Contig.__tablename__, attr=attr)
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
async def delete_contig(
    where: ContigWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Delete Contig objects. Used for mutations (see api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(db.Contig, session, cerbos_client, principal, where, [], CerbosAction.DELETE)
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
