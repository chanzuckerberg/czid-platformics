"""
GraphQL type for ConsensusGenome

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


import typing
from typing import TYPE_CHECKING, Annotated, Optional, Sequence, Callable

import database.models as db
import strawberry
from platformics.api.core.helpers import get_db_rows, get_aggregate_db_rows
from api.files import File, FileWhereClause
from api.types.entities import EntityInterface
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource
from fastapi import Depends
from platformics.api.core.errors import PlatformicsException
from platformics.api.core.deps import get_cerbos_client, get_db_session, require_auth_principal
from platformics.api.core.gql_to_sql import (
    aggregator_map,
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

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.taxon import TaxonWhereClause, Taxon
    from api.types.sequencing_read import SequencingReadWhereClause, SequencingRead
    from api.types.reference_genome import ReferenceGenomeWhereClause, ReferenceGenome
    from api.types.metric_consensus_genome import MetricConsensusGenomeWhereClause, MetricConsensusGenome

    pass
else:
    TaxonWhereClause = "TaxonWhereClause"
    Taxon = "Taxon"
    SequencingReadWhereClause = "SequencingReadWhereClause"
    SequencingRead = "SequencingRead"
    ReferenceGenomeWhereClause = "ReferenceGenomeWhereClause"
    ReferenceGenome = "ReferenceGenome"
    MetricConsensusGenomeWhereClause = "MetricConsensusGenomeWhereClause"
    MetricConsensusGenome = "MetricConsensusGenome"
    pass


"""
------------------------------------------------------------------------------
Dataloaders
------------------------------------------------------------------------------
These are batching functions for loading related objects to avoid N+1 queries.
"""


@strawberry.field
async def load_taxon_rows(
    root: "ConsensusGenome",
    info: Info,
    where: Annotated["TaxonWhereClause", strawberry.lazy("api.types.taxon")] | None = None,
) -> Optional[Annotated["Taxon", strawberry.lazy("api.types.taxon")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.ConsensusGenome)
    relationship = mapper.relationships["taxon"]
    return await dataloader.loader_for(relationship, where).load(root.taxon_id)  # type:ignore


@strawberry.field
async def load_sequencing_read_rows(
    root: "ConsensusGenome",
    info: Info,
    where: Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")] | None = None,
) -> Optional[Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.ConsensusGenome)
    relationship = mapper.relationships["sequence_read"]
    return await dataloader.loader_for(relationship, where).load(root.sequence_read_id)  # type:ignore


@strawberry.field
async def load_reference_genome_rows(
    root: "ConsensusGenome",
    info: Info,
    where: Annotated["ReferenceGenomeWhereClause", strawberry.lazy("api.types.reference_genome")] | None = None,
) -> Optional[Annotated["ReferenceGenome", strawberry.lazy("api.types.reference_genome")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.ConsensusGenome)
    relationship = mapper.relationships["reference_genome"]
    return await dataloader.loader_for(relationship, where).load(root.reference_genome_id)  # type:ignore


@strawberry.field
async def load_metric_consensus_genome_rows(
    root: "ConsensusGenome",
    info: Info,
    where: Annotated["MetricConsensusGenomeWhereClause", strawberry.lazy("api.types.metric_consensus_genome")]
    | None = None,
) -> Optional[Annotated["MetricConsensusGenome", strawberry.lazy("api.types.metric_consensus_genome")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.ConsensusGenome)
    relationship = mapper.relationships["metrics"]
    return await dataloader.loader_for(relationship, where).load(root.metrics_id)  # type:ignore


"""
------------------------------------------------------------------------------
Dataloader for File object
------------------------------------------------------------------------------
"""


def load_files_from(attr_name: str) -> Callable:
    @strawberry.field
    async def load_files(
        root: "ConsensusGenome",
        info: Info,
        where: Annotated["FileWhereClause", strawberry.lazy("api.files")] | None = None,
    ) -> Optional[Annotated["File", strawberry.lazy("api.files")]]:
        """
        Given a list of ConsensusGenome IDs for a certain file type, return related Files
        """
        dataloader = info.context["sqlalchemy_loader"]
        mapper = inspect(db.ConsensusGenome)
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
class ConsensusGenomeWhereClauseMutations(TypedDict):
    id: UUIDComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class ConsensusGenomeWhereClause(TypedDict):
    id: UUIDComparators | None
    producing_run_id: IntComparators | None
    owner_user_id: IntComparators | None
    collection_id: IntComparators | None
    taxon: Optional[Annotated["TaxonWhereClause", strawberry.lazy("api.types.taxon")]] | None
    sequence_read: Optional[Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")]] | None
    reference_genome: Optional[
        Annotated["ReferenceGenomeWhereClause", strawberry.lazy("api.types.reference_genome")]
    ] | None
    metrics: Optional[
        Annotated["MetricConsensusGenomeWhereClause", strawberry.lazy("api.types.metric_consensus_genome")]
    ] | None


"""
Define ConsensusGenome type
"""


@strawberry.type
class ConsensusGenome(EntityInterface):
    id: strawberry.ID
    producing_run_id: Optional[int]
    owner_user_id: int
    collection_id: int
    taxon: Optional[Annotated["Taxon", strawberry.lazy("api.types.taxon")]] = load_taxon_rows  # type:ignore
    sequence_read: Optional[
        Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]
    ] = load_sequencing_read_rows  # type:ignore
    reference_genome: Optional[
        Annotated["ReferenceGenome", strawberry.lazy("api.types.reference_genome")]
    ] = load_reference_genome_rows  # type:ignore
    sequence_id: Optional[strawberry.ID]
    sequence: Optional[Annotated["File", strawberry.lazy("api.files")]] = load_files_from("sequence")  # type: ignore
    metrics: Optional[
        Annotated["MetricConsensusGenome", strawberry.lazy("api.types.metric_consensus_genome")]
    ] = load_metric_consensus_genome_rows  # type:ignore
    intermediate_outputs_id: Optional[strawberry.ID]
    intermediate_outputs: Optional[Annotated["File", strawberry.lazy("api.files")]] = load_files_from("intermediate_outputs")  # type: ignore


"""
We need to add this to each Queryable type so that strawberry will accept either our
Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
"""
ConsensusGenome.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.ConsensusGenome or type(obj) == ConsensusGenome
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
class ConsensusGenomeNumericalColumns:
    producing_run_id: Optional[int] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class ConsensusGenomeMinMaxColumns:
    producing_run_id: Optional[int] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class ConsensusGenomeCountColumns(enum.Enum):
    taxon = "taxon"
    sequence_read = "sequence_read"
    reference_genome = "reference_genome"
    sequence = "sequence"
    metrics = "metrics"
    intermediate_outputs = "intermediate_outputs"
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
class ConsensusGenomeAggregateFunctions:
    # This is a hack to accept "distinct" and "columns" as arguments to "count"
    @strawberry.field
    def count(
        self, distinct: Optional[bool] = False, columns: Optional[ConsensusGenomeCountColumns] = None
    ) -> Optional[int]:
        # Count gets set with the proper value in the resolver, so we just return it here
        return self.count  # type: ignore

    sum: Optional[ConsensusGenomeNumericalColumns] = None
    avg: Optional[ConsensusGenomeNumericalColumns] = None
    min: Optional[ConsensusGenomeMinMaxColumns] = None
    max: Optional[ConsensusGenomeMinMaxColumns] = None
    stddev: Optional[ConsensusGenomeNumericalColumns] = None
    variance: Optional[ConsensusGenomeNumericalColumns] = None


"""
Wrapper around ConsensusGenomeAggregateFunctions
"""


@strawberry.type
class ConsensusGenomeAggregate:
    aggregate: Optional[ConsensusGenomeAggregateFunctions] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class ConsensusGenomeCreateInput:
    collection_id: int
    taxon_id: strawberry.ID
    sequence_read_id: strawberry.ID
    reference_genome_id: strawberry.ID
    sequence_id: Optional[strawberry.ID] = None
    metrics_id: Optional[strawberry.ID] = None
    intermediate_outputs_id: Optional[strawberry.ID] = None


@strawberry.input()
class ConsensusGenomeUpdateInput:
    collection_id: Optional[int] = None
    taxon_id: Optional[strawberry.ID] = None
    sequence_read_id: Optional[strawberry.ID] = None
    reference_genome_id: Optional[strawberry.ID] = None
    sequence_id: Optional[strawberry.ID] = None
    metrics_id: Optional[strawberry.ID] = None
    intermediate_outputs_id: Optional[strawberry.ID] = None


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_consensus_genomes(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[ConsensusGenomeWhereClause] = None,
) -> typing.Sequence[ConsensusGenome]:
    """
    Resolve ConsensusGenome objects. Used for queries (see api/queries.py).
    """
    return await get_db_rows(db.ConsensusGenome, session, cerbos_client, principal, where, [])  # type: ignore


def format_consensus_genome_aggregate_output(query_results: RowMapping) -> ConsensusGenomeAggregateFunctions:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = ConsensusGenomeAggregateFunctions()
    for aggregate_name, value in query_results.items():
        if aggregate_name == "count":
            output.count = value
        else:
            aggregator_fn, col_name = aggregate_name.split("_", 1)
            # Filter out the group_by key from the results if one was provided.
            if aggregator_fn in aggregator_map.keys():
                if not getattr(output, aggregator_fn):
                    if aggregate_name in ["min", "max"]:
                        setattr(output, aggregator_fn, ConsensusGenomeMinMaxColumns())
                    else:
                        setattr(output, aggregator_fn, ConsensusGenomeNumericalColumns())
                setattr(getattr(output, aggregator_fn), col_name, value)
    return output


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_consensus_genomes_aggregate(
    info: Info,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[ConsensusGenomeWhereClause] = None,
) -> ConsensusGenomeAggregate:
    """
    Aggregate values for ConsensusGenome objects. Used for queries (see api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on
    # TODO: not sure why selected_fields is a list
    # The first list of selections will always be ["aggregate"], so just grab the first item
    selections = info.selected_fields[0].selections[0].selections
    rows = await get_aggregate_db_rows(db.ConsensusGenome, session, cerbos_client, principal, where, selections, [])  # type: ignore
    aggregate_output = format_consensus_genome_aggregate_output(rows)
    return ConsensusGenomeAggregate(aggregate=aggregate_output)


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_consensus_genome(
    input: ConsensusGenomeCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> db.Entity:
    """
    Create a new ConsensusGenome object. Used for mutations (see api/mutations.py).
    """
    params = input.__dict__

    # Validate that user can create entity in this collection
    attr = {"collection_id": input.collection_id}
    resource = Resource(id="NEW_ID", kind=db.ConsensusGenome.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise PlatformicsException("Unauthorized: Cannot create entity in this collection")

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.ConsensusGenome(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_consensus_genome(
    input: ConsensusGenomeUpdateInput,
    where: ConsensusGenomeWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Update ConsensusGenome objects. Used for mutations (see api/mutations.py).
    """
    params = input.__dict__

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise PlatformicsException("No fields to update")

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(db.ConsensusGenome, session, cerbos_client, principal, where, [], CerbosAction.UPDATE)
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot update entities")

    # Validate that the user has access to the new collection ID
    if input.collection_id:
        attr = {"collection_id": input.collection_id}
        resource = Resource(id="SOME_ID", kind=db.ConsensusGenome.__tablename__, attr=attr)
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
async def delete_consensus_genome(
    where: ConsensusGenomeWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Delete ConsensusGenome objects. Used for mutations (see api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(db.ConsensusGenome, session, cerbos_client, principal, where, [], CerbosAction.DELETE)
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
