"""
GraphQL type for MetricConsensusGenome

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


import typing
from typing import TYPE_CHECKING, Annotated, Optional, Sequence, List

import database.models as db
import strawberry
from platformics.api.core.helpers import get_db_rows, get_aggregate_db_rows
from api.types.entities import EntityInterface
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource
from fastapi import Depends
from platformics.api.core.errors import PlatformicsException
from platformics.api.core.deps import get_cerbos_client, get_db_session, require_auth_principal
from platformics.api.core.gql_to_sql import (
    aggregator_map,
    orderBy,
    IntComparators,
    FloatComparators,
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
    from api.types.consensus_genome import ConsensusGenomeWhereClause, ConsensusGenome

    pass
else:
    ConsensusGenomeWhereClause = "ConsensusGenomeWhereClause"
    ConsensusGenome = "ConsensusGenome"
    pass


"""
------------------------------------------------------------------------------
Dataloaders
------------------------------------------------------------------------------
These are batching functions for loading related objects to avoid N+1 queries.
"""


@strawberry.field
async def load_consensus_genome_rows(
    root: "MetricConsensusGenome",
    info: Info,
    where: Annotated["ConsensusGenomeWhereClause", strawberry.lazy("api.types.consensus_genome")] | None = None,
) -> Optional[Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.MetricConsensusGenome)
    relationship = mapper.relationships["consensus_genome"]
    return await dataloader.loader_for(relationship, where).load(root.consensus_genome_id)  # type:ignore


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
class MetricConsensusGenomeWhereClauseMutations(TypedDict):
    id: UUIDComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class MetricConsensusGenomeWhereClause(TypedDict):
    id: UUIDComparators | None
    producing_run_id: IntComparators | None
    owner_user_id: IntComparators | None
    collection_id: IntComparators | None
    consensus_genome: Optional[
        Annotated["ConsensusGenomeWhereClause", strawberry.lazy("api.types.consensus_genome")]
    ] | None
    reference_genome_length: Optional[FloatComparators] | None
    percent_genome_called: Optional[FloatComparators] | None
    percent_identity: Optional[FloatComparators] | None
    gc_percent: Optional[FloatComparators] | None
    total_reads: Optional[IntComparators] | None
    mapped_reads: Optional[IntComparators] | None
    ref_snps: Optional[IntComparators] | None
    n_actg: Optional[IntComparators] | None
    n_missing: Optional[IntComparators] | None
    n_ambiguous: Optional[IntComparators] | None
    coverage_depth: Optional[FloatComparators] | None
    coverage_breadth: Optional[FloatComparators] | None
    coverage_bin_size: Optional[FloatComparators] | None
    coverage_total_length: Optional[IntComparators] | None

"""
Supported ORDER BY clause attributes
"""

@strawberry.enum
class MetricConsensusGenomeOrderByColumns(enum.Enum):
    id = "id"
    producing_run_id = "producing_run_id"
    owner_user_id = "owner_user_id"
    collection_id = "collection_id"
    consensus_genome = "consensus_genome"
    coverage_depth = "coverage_depth"
    reference_genome_length = "reference_genome_length"
    percent_genome_called = "percent_genome_called"
    percent_identity = "percent_identity"
    gc_percent = "gc_percent"
    total_reads = "total_reads"
    mapped_reads = "mapped_reads"
    ref_snps = "ref_snps"
    n_actg = "n_actg"
    n_missing = "n_missing"
    n_ambiguous = "n_ambiguous"
    coverage_viz_summary_file = "coverage_viz_summary_file"

# GraphQL doesn't support tuples, so we need to define a custom type for the order_by clause
@strawberry.input
class MetricConsensusGenomeOrderByClause:
    column: MetricConsensusGenomeOrderByColumns
    direction: orderBy


"""
Define MetricConsensusGenome type
"""


@strawberry.type
class MetricConsensusGenome(EntityInterface):
    id: strawberry.ID
    producing_run_id: Optional[int]
    owner_user_id: int
    collection_id: int
    consensus_genome: Optional[
        Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]
    ] = load_consensus_genome_rows  # type:ignore
    reference_genome_length: Optional[float] = None
    percent_genome_called: Optional[float] = None
    percent_identity: Optional[float] = None
    gc_percent: Optional[float] = None
    total_reads: Optional[int] = None
    mapped_reads: Optional[int] = None
    ref_snps: Optional[int] = None
    n_actg: Optional[int] = None
    n_missing: Optional[int] = None
    n_ambiguous: Optional[int] = None
    coverage_depth: Optional[float] = None
    coverage_breadth: Optional[float] = None
    coverage_bin_size: Optional[float] = None
    coverage_total_length: Optional[int] = None
    coverage_viz: Optional[List[List[int]]] = None


"""
We need to add this to each Queryable type so that strawberry will accept either our
Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
"""
MetricConsensusGenome.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.MetricConsensusGenome or type(obj) == MetricConsensusGenome
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
class MetricConsensusGenomeNumericalColumns:
    producing_run_id: Optional[int] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    reference_genome_length: Optional[float] = None
    percent_genome_called: Optional[float] = None
    percent_identity: Optional[float] = None
    gc_percent: Optional[float] = None
    total_reads: Optional[int] = None
    mapped_reads: Optional[int] = None
    ref_snps: Optional[int] = None
    n_actg: Optional[int] = None
    n_missing: Optional[int] = None
    n_ambiguous: Optional[int] = None
    coverage_depth: Optional[float] = None
    coverage_breadth: Optional[float] = None
    coverage_bin_size: Optional[float] = None
    coverage_total_length: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class MetricConsensusGenomeMinMaxColumns:
    producing_run_id: Optional[int] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    reference_genome_length: Optional[float] = None
    percent_genome_called: Optional[float] = None
    percent_identity: Optional[float] = None
    gc_percent: Optional[float] = None
    total_reads: Optional[int] = None
    mapped_reads: Optional[int] = None
    ref_snps: Optional[int] = None
    n_actg: Optional[int] = None
    n_missing: Optional[int] = None
    n_ambiguous: Optional[int] = None
    coverage_depth: Optional[float] = None
    coverage_breadth: Optional[float] = None
    coverage_bin_size: Optional[float] = None
    coverage_total_length: Optional[int] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class MetricConsensusGenomeCountColumns(enum.Enum):
    consensus_genome = "consensus_genome"
    reference_genome_length = "reference_genome_length"
    percent_genome_called = "percent_genome_called"
    percent_identity = "percent_identity"
    gc_percent = "gc_percent"
    total_reads = "total_reads"
    mapped_reads = "mapped_reads"
    ref_snps = "ref_snps"
    n_actg = "n_actg"
    n_missing = "n_missing"
    n_ambiguous = "n_ambiguous"
    coverage_depth = "coverage_depth"
    coverage_breadth = "coverage_breadth"
    coverage_bin_size = "coverage_bin_size"
    coverage_total_length = "coverage_total_length"
    coverage_viz = "coverage_viz"
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
class MetricConsensusGenomeAggregateFunctions:
    # This is a hack to accept "distinct" and "columns" as arguments to "count"
    @strawberry.field
    def count(
        self, distinct: Optional[bool] = False, columns: Optional[MetricConsensusGenomeCountColumns] = None
    ) -> Optional[int]:
        # Count gets set with the proper value in the resolver, so we just return it here
        return self.count  # type: ignore

    sum: Optional[MetricConsensusGenomeNumericalColumns] = None
    avg: Optional[MetricConsensusGenomeNumericalColumns] = None
    min: Optional[MetricConsensusGenomeMinMaxColumns] = None
    max: Optional[MetricConsensusGenomeMinMaxColumns] = None
    stddev: Optional[MetricConsensusGenomeNumericalColumns] = None
    variance: Optional[MetricConsensusGenomeNumericalColumns] = None


"""
Wrapper around MetricConsensusGenomeAggregateFunctions
"""


@strawberry.type
class MetricConsensusGenomeAggregate:
    aggregate: Optional[MetricConsensusGenomeAggregateFunctions] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class MetricConsensusGenomeCreateInput:
    collection_id: int
    consensus_genome_id: strawberry.ID
    reference_genome_length: Optional[float] = None
    percent_genome_called: Optional[float] = None
    percent_identity: Optional[float] = None
    gc_percent: Optional[float] = None
    total_reads: Optional[int] = None
    mapped_reads: Optional[int] = None
    ref_snps: Optional[int] = None
    n_actg: Optional[int] = None
    n_missing: Optional[int] = None
    n_ambiguous: Optional[int] = None
    coverage_depth: Optional[float] = None
    coverage_breadth: Optional[float] = None
    coverage_bin_size: Optional[float] = None
    coverage_total_length: Optional[int] = None
    coverage_viz: Optional[List[List[int]]] = None


@strawberry.input()
class MetricConsensusGenomeUpdateInput:
    collection_id: Optional[int] = None
    consensus_genome_id: Optional[strawberry.ID] = None
    reference_genome_length: Optional[float] = None
    percent_genome_called: Optional[float] = None
    percent_identity: Optional[float] = None
    gc_percent: Optional[float] = None
    total_reads: Optional[int] = None
    mapped_reads: Optional[int] = None
    ref_snps: Optional[int] = None
    n_actg: Optional[int] = None
    n_missing: Optional[int] = None
    n_ambiguous: Optional[int] = None
    coverage_depth: Optional[float] = None
    coverage_breadth: Optional[float] = None
    coverage_bin_size: Optional[float] = None
    coverage_total_length: Optional[int] = None
    coverage_viz: Optional[List[List[int]]] = None


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_metrics_consensus_genomes(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[MetricConsensusGenomeWhereClause] = None,
    order_by: Optional[list[MetricConsensusGenomeOrderByClause]] = [],
) -> typing.Sequence[MetricConsensusGenome]:
    """
    Resolve MetricConsensusGenome objects. Used for queries (see api/queries.py).
    """
    return await get_db_rows(db.MetricConsensusGenome, session, cerbos_client, principal, where, order_by)  # type: ignore


def format_metric_consensus_genome_aggregate_output(
    query_results: RowMapping,
) -> MetricConsensusGenomeAggregateFunctions:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = MetricConsensusGenomeAggregateFunctions()
    for aggregate_name, value in query_results.items():
        if aggregate_name == "count":
            output.count = value
        else:
            aggregator_fn, col_name = aggregate_name.split("_", 1)
            # Filter out the group_by key from the results if one was provided.
            if aggregator_fn in aggregator_map.keys():
                if not getattr(output, aggregator_fn):
                    if aggregate_name in ["min", "max"]:
                        setattr(output, aggregator_fn, MetricConsensusGenomeMinMaxColumns())
                    else:
                        setattr(output, aggregator_fn, MetricConsensusGenomeNumericalColumns())
                setattr(getattr(output, aggregator_fn), col_name, value)
    return output


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_metrics_consensus_genomes_aggregate(
    info: Info,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[MetricConsensusGenomeWhereClause] = None,
) -> MetricConsensusGenomeAggregate:
    """
    Aggregate values for MetricConsensusGenome objects. Used for queries (see api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on
    # TODO: not sure why selected_fields is a list
    # The first list of selections will always be ["aggregate"], so just grab the first item
    selections = info.selected_fields[0].selections[0].selections
    rows = await get_aggregate_db_rows(db.MetricConsensusGenome, session, cerbos_client, principal, where, selections, [])  # type: ignore
    aggregate_output = format_metric_consensus_genome_aggregate_output(rows)
    return MetricConsensusGenomeAggregate(aggregate=aggregate_output)


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_metric_consensus_genome(
    input: MetricConsensusGenomeCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> db.Entity:
    """
    Create a new MetricConsensusGenome object. Used for mutations (see api/mutations.py).
    """
    params = input.__dict__

    # Validate that user can create entity in this collection
    attr = {"collection_id": input.collection_id}
    resource = Resource(id="NEW_ID", kind=db.MetricConsensusGenome.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise PlatformicsException("Unauthorized: Cannot create entity in this collection")

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.MetricConsensusGenome(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_metric_consensus_genome(
    input: MetricConsensusGenomeUpdateInput,
    where: MetricConsensusGenomeWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Update MetricConsensusGenome objects. Used for mutations (see api/mutations.py).
    """
    params = input.__dict__

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise PlatformicsException("No fields to update")

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(
        db.MetricConsensusGenome, session, cerbos_client, principal, where, [], CerbosAction.UPDATE
    )
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot update entities")

    # Validate that the user has access to the new collection ID
    if input.collection_id:
        attr = {"collection_id": input.collection_id}
        resource = Resource(id="SOME_ID", kind=db.MetricConsensusGenome.__tablename__, attr=attr)
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
async def delete_metric_consensus_genome(
    where: MetricConsensusGenomeWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Delete MetricConsensusGenome objects. Used for mutations (see api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(
        db.MetricConsensusGenome, session, cerbos_client, principal, where, [], CerbosAction.DELETE
    )
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
