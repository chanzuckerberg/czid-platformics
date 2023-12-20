"""
GraphQL type for SequenceAlignmentIndex

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long

import typing
from typing import TYPE_CHECKING, Annotated, Optional, Sequence, Callable

import database.models as db
import strawberry
from api.core.helpers import get_db_rows, get_aggregate_db_rows
from api.files import File, FileWhereClause
from api.types.entities import EntityInterface
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource
from fastapi import Depends
from platformics.api.core.deps import get_cerbos_client, get_db_session, require_auth_principal
from platformics.api.core.gql_to_sql import (
    aggregator_map,
    EnumComparators,
    IntComparators,
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
from support.enums import AlignmentTool

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.reference_genome import ReferenceGenomeWhereClause, ReferenceGenome

    pass
else:
    ReferenceGenomeWhereClause = "ReferenceGenomeWhereClause"
    ReferenceGenome = "ReferenceGenome"
    pass


"""
------------------------------------------------------------------------------
Dataloaders
------------------------------------------------------------------------------
These are batching functions for loading related objects to avoid N+1 queries.
"""


@strawberry.field
async def load_reference_genome_rows(
    root: "SequenceAlignmentIndex",
    info: Info,
    where: Annotated["ReferenceGenomeWhereClause", strawberry.lazy("api.types.reference_genome")] | None = None,
) -> Optional[Annotated["ReferenceGenome", strawberry.lazy("api.types.reference_genome")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.SequenceAlignmentIndex)
    relationship = mapper.relationships["reference_genome"]
    return await dataloader.loader_for(relationship, where).load(root.reference_genome_id)  # type:ignore


"""
------------------------------------------------------------------------------
Dataloader for File object
------------------------------------------------------------------------------
"""


def load_files_from(attr_name: str) -> Callable:
    @strawberry.field
    async def load_files(
        root: "SequenceAlignmentIndex",
        info: Info,
        where: Annotated["FileWhereClause", strawberry.lazy("api.files")] | None = None,
    ) -> Optional[Annotated["File", strawberry.lazy("api.files")]]:
        """
        Given a list of SequenceAlignmentIndex IDs for a certain file type, return related Files
        """
        dataloader = info.context["sqlalchemy_loader"]
        mapper = inspect(db.SequenceAlignmentIndex)
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
class SequenceAlignmentIndexWhereClauseMutations(TypedDict):
    id: UUIDComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class SequenceAlignmentIndexWhereClause(TypedDict):
    id: UUIDComparators | None
    producing_run_id: IntComparators | None
    owner_user_id: IntComparators | None
    collection_id: IntComparators | None
    reference_genome: Optional[
        Annotated["ReferenceGenomeWhereClause", strawberry.lazy("api.types.reference_genome")]
    ] | None
    tool: Optional[EnumComparators[AlignmentTool]] | None


"""
Define SequenceAlignmentIndex type
"""


@strawberry.type
class SequenceAlignmentIndex(EntityInterface):
    id: strawberry.ID
    producing_run_id: Optional[int]
    owner_user_id: int
    collection_id: int
    index_file_id: Optional[strawberry.ID]
    index_file: Optional[Annotated["File", strawberry.lazy("api.files")]] = load_files_from("index_file")  # type: ignore
    reference_genome: Optional[
        Annotated["ReferenceGenome", strawberry.lazy("api.types.reference_genome")]
    ] = load_reference_genome_rows  # type:ignore
    tool: AlignmentTool


"""
We need to add this to each Queryable type so that strawberry will accept either our
Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
"""
SequenceAlignmentIndex.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.SequenceAlignmentIndex or type(obj) == SequenceAlignmentIndex
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
class SequenceAlignmentIndexNumericalColumns:
    producing_run_id: Optional[int] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class SequenceAlignmentIndexMinMaxColumns:
    producing_run_id: Optional[int] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class SequenceAlignmentIndexCountColumns(enum.Enum):
    index_file = "index_file"
    reference_genome = "reference_genome"
    tool = "tool"
    entity_id = "entity_id"
    id = "id"
    producing_run_id = "producing_run_id"
    owner_user_id = "owner_user_id"
    collection_id = "collection_id"


"""
All supported aggregation functions
"""


@strawberry.type
class SequenceAlignmentIndexAggregateFunctions:
    # This is a hack to accept "distinct" and "columns" as arguments to "count"
    @strawberry.field
    def count(
        self, distinct: Optional[bool] = False, columns: Optional[SequenceAlignmentIndexCountColumns] = None
    ) -> Optional[int]:
        # Count gets set with the proper value in the resolver, so we just return it here
        return self.count  # type: ignore

    sum: Optional[SequenceAlignmentIndexNumericalColumns] = None
    avg: Optional[SequenceAlignmentIndexNumericalColumns] = None
    min: Optional[SequenceAlignmentIndexMinMaxColumns] = None
    max: Optional[SequenceAlignmentIndexMinMaxColumns] = None
    stddev: Optional[SequenceAlignmentIndexNumericalColumns] = None
    variance: Optional[SequenceAlignmentIndexNumericalColumns] = None


"""
Wrapper around SequenceAlignmentIndexAggregateFunctions
"""


@strawberry.type
class SequenceAlignmentIndexAggregate:
    aggregate: Optional[SequenceAlignmentIndexAggregateFunctions] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class SequenceAlignmentIndexCreateInput:
    collection_id: int
    index_file_id: Optional[strawberry.ID] = None
    reference_genome_id: strawberry.ID
    tool: AlignmentTool


@strawberry.input()
class SequenceAlignmentIndexUpdateInput:
    collection_id: Optional[int] = None
    index_file_id: Optional[strawberry.ID] = None
    reference_genome_id: Optional[strawberry.ID] = None
    tool: Optional[AlignmentTool] = None


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_sequence_alignment_indices(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[SequenceAlignmentIndexWhereClause] = None,
) -> typing.Sequence[SequenceAlignmentIndex]:
    """
    Resolve SequenceAlignmentIndex objects. Used for queries (see api/queries.py).
    """
    return await get_db_rows(db.SequenceAlignmentIndex, session, cerbos_client, principal, where, [])  # type: ignore


def format_sequence_alignment_index_aggregate_output(
    query_results: RowMapping,
) -> SequenceAlignmentIndexAggregateFunctions:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = SequenceAlignmentIndexAggregateFunctions()
    for aggregate_name, value in query_results.items():
        if aggregate_name == "count":
            output.count = value
        else:
            aggregator_fn, col_name = aggregate_name.split("_", 1)
            # Filter out the group_by key from the results if one was provided.
            if aggregator_fn in aggregator_map.keys():
                if not getattr(output, aggregator_fn):
                    if aggregate_name in ["min", "max"]:
                        setattr(output, aggregator_fn, SequenceAlignmentIndexMinMaxColumns())
                    else:
                        setattr(output, aggregator_fn, SequenceAlignmentIndexNumericalColumns())
                setattr(getattr(output, aggregator_fn), col_name, value)
    return output


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_sequence_alignment_indices_aggregate(
    info: Info,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[SequenceAlignmentIndexWhereClause] = None,
) -> SequenceAlignmentIndexAggregate:
    """
    Aggregate values for SequenceAlignmentIndex objects. Used for queries (see api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on
    # TODO: not sure why selected_fields is a list
    # The first list of selections will always be ["aggregate"], so just grab the first item
    selections = info.selected_fields[0].selections[0].selections
    rows = await get_aggregate_db_rows(db.SequenceAlignmentIndex, session, cerbos_client, principal, where, selections, [])  # type: ignore
    aggregate_output = format_sequence_alignment_index_aggregate_output(rows)
    return SequenceAlignmentIndexAggregate(aggregate=aggregate_output)


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_sequence_alignment_index(
    input: SequenceAlignmentIndexCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> db.Entity:
    """
    Create a new SequenceAlignmentIndex object. Used for mutations (see api/mutations.py).
    """
    params = input.__dict__

    # Validate that user can create entity in this collection
    attr = {"collection_id": input.collection_id}
    resource = Resource(id="NEW_ID", kind=db.SequenceAlignmentIndex.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise Exception("Unauthorized: Cannot create entity in this collection")

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.SequenceAlignmentIndex(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_sequence_alignment_index(
    input: SequenceAlignmentIndexUpdateInput,
    where: SequenceAlignmentIndexWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Update SequenceAlignmentIndex objects. Used for mutations (see api/mutations.py).
    """
    params = input.__dict__

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise Exception("No fields to update")

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(
        db.SequenceAlignmentIndex, session, cerbos_client, principal, where, [], CerbosAction.UPDATE
    )
    if len(entities) == 0:
        raise Exception("Unauthorized: Cannot update entities")

    # Validate that the user has access to the new collection ID
    if input.collection_id:
        attr = {"collection_id": input.collection_id}
        resource = Resource(id="SOME_ID", kind=db.SequenceAlignmentIndex.__tablename__, attr=attr)
        if not cerbos_client.is_allowed(CerbosAction.UPDATE, principal, resource):
            raise Exception("Unauthorized: Cannot access new collection")

    # Update DB
    for entity in entities:
        for key in params:
            if params[key]:
                setattr(entity, key, params[key])
    await session.commit()
    return entities


@strawberry.mutation(extensions=[DependencyExtension()])
async def delete_sequence_alignment_index(
    where: SequenceAlignmentIndexWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Delete SequenceAlignmentIndex objects. Used for mutations (see api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(
        db.SequenceAlignmentIndex, session, cerbos_client, principal, where, [], CerbosAction.DELETE
    )
    if len(entities) == 0:
        raise Exception("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
