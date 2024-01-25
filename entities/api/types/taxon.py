"""
GraphQL type for Taxon

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
from api.types.consensus_genome import ConsensusGenomeAggregate, format_consensus_genome_aggregate_output
from api.types.reference_genome import ReferenceGenomeAggregate, format_reference_genome_aggregate_output
from api.types.sequencing_read import SequencingReadAggregate, format_sequencing_read_aggregate_output
from api.types.sample import SampleAggregate, format_sample_aggregate_output
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource
from fastapi import Depends
from platformics.api.core.errors import PlatformicsException
from platformics.api.core.deps import get_cerbos_client, get_db_session, require_auth_principal
from platformics.api.core.gql_to_sql import (
    aggregator_map,
    EnumComparators,
    IntComparators,
    StrComparators,
    UUIDComparators,
    BoolComparators,
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
from support.enums import TaxonLevel

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.upstream_database import UpstreamDatabaseWhereClause, UpstreamDatabase
    from api.types.consensus_genome import ConsensusGenomeWhereClause, ConsensusGenome
    from api.types.reference_genome import ReferenceGenomeWhereClause, ReferenceGenome
    from api.types.sequencing_read import SequencingReadWhereClause, SequencingRead
    from api.types.sample import SampleWhereClause, Sample

    pass
else:
    UpstreamDatabaseWhereClause = "UpstreamDatabaseWhereClause"
    UpstreamDatabase = "UpstreamDatabase"
    ConsensusGenomeWhereClause = "ConsensusGenomeWhereClause"
    ConsensusGenome = "ConsensusGenome"
    ReferenceGenomeWhereClause = "ReferenceGenomeWhereClause"
    ReferenceGenome = "ReferenceGenome"
    SequencingReadWhereClause = "SequencingReadWhereClause"
    SequencingRead = "SequencingRead"
    SampleWhereClause = "SampleWhereClause"
    Sample = "Sample"
    pass


"""
------------------------------------------------------------------------------
Dataloaders
------------------------------------------------------------------------------
These are batching functions for loading related objects to avoid N+1 queries.
"""


@strawberry.field
async def load_upstream_database_rows(
    root: "Taxon",
    info: Info,
    where: Annotated["UpstreamDatabaseWhereClause", strawberry.lazy("api.types.upstream_database")] | None = None,
) -> Optional[Annotated["UpstreamDatabase", strawberry.lazy("api.types.upstream_database")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Taxon)
    relationship = mapper.relationships["upstream_database"]
    return await dataloader.loader_for(relationship, where).load(root.upstream_database_id)  # type:ignore


@relay.connection(
    relay.ListConnection[Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]]  # type:ignore
)
async def load_consensus_genome_rows(
    root: "Taxon",
    info: Info,
    where: Annotated["ConsensusGenomeWhereClause", strawberry.lazy("api.types.consensus_genome")] | None = None,
) -> Sequence[Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Taxon)
    relationship = mapper.relationships["consensus_genomes"]
    return await dataloader.loader_for(relationship, where).load(root.id)  # type:ignore


@strawberry.field
async def load_consensus_genome_aggregate_rows(
    root: "Taxon",
    info: Info,
    where: Annotated["ConsensusGenomeWhereClause", strawberry.lazy("api.types.consensus_genome")] | None = None,
) -> Optional[Annotated["ConsensusGenomeAggregate", strawberry.lazy("api.types.consensus_genome")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Taxon)
    relationship = mapper.relationships["consensus_genomes"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    # Aggregate queries always return a single row, so just grab the first one
    result = rows[0] if rows else None
    aggregate_output = format_consensus_genome_aggregate_output(result)
    return ConsensusGenomeAggregate(aggregate=aggregate_output)


@relay.connection(
    relay.ListConnection[Annotated["ReferenceGenome", strawberry.lazy("api.types.reference_genome")]]  # type:ignore
)
async def load_reference_genome_rows(
    root: "Taxon",
    info: Info,
    where: Annotated["ReferenceGenomeWhereClause", strawberry.lazy("api.types.reference_genome")] | None = None,
) -> Sequence[Annotated["ReferenceGenome", strawberry.lazy("api.types.reference_genome")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Taxon)
    relationship = mapper.relationships["reference_genomes"]
    return await dataloader.loader_for(relationship, where).load(root.id)  # type:ignore


@strawberry.field
async def load_reference_genome_aggregate_rows(
    root: "Taxon",
    info: Info,
    where: Annotated["ReferenceGenomeWhereClause", strawberry.lazy("api.types.reference_genome")] | None = None,
) -> Optional[Annotated["ReferenceGenomeAggregate", strawberry.lazy("api.types.reference_genome")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Taxon)
    relationship = mapper.relationships["reference_genomes"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    # Aggregate queries always return a single row, so just grab the first one
    result = rows[0] if rows else None
    aggregate_output = format_reference_genome_aggregate_output(result)
    return ReferenceGenomeAggregate(aggregate=aggregate_output)


@relay.connection(
    relay.ListConnection[Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]]  # type:ignore
)
async def load_sequencing_read_rows(
    root: "Taxon",
    info: Info,
    where: Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")] | None = None,
) -> Sequence[Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Taxon)
    relationship = mapper.relationships["sequencing_reads"]
    return await dataloader.loader_for(relationship, where).load(root.id)  # type:ignore


@strawberry.field
async def load_sequencing_read_aggregate_rows(
    root: "Taxon",
    info: Info,
    where: Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")] | None = None,
) -> Optional[Annotated["SequencingReadAggregate", strawberry.lazy("api.types.sequencing_read")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Taxon)
    relationship = mapper.relationships["sequencing_reads"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    # Aggregate queries always return a single row, so just grab the first one
    result = rows[0] if rows else None
    aggregate_output = format_sequencing_read_aggregate_output(result)
    return SequencingReadAggregate(aggregate=aggregate_output)


@relay.connection(
    relay.ListConnection[Annotated["Sample", strawberry.lazy("api.types.sample")]]  # type:ignore
)
async def load_sample_rows(
    root: "Taxon",
    info: Info,
    where: Annotated["SampleWhereClause", strawberry.lazy("api.types.sample")] | None = None,
) -> Sequence[Annotated["Sample", strawberry.lazy("api.types.sample")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Taxon)
    relationship = mapper.relationships["samples"]
    return await dataloader.loader_for(relationship, where).load(root.id)  # type:ignore


@strawberry.field
async def load_sample_aggregate_rows(
    root: "Taxon",
    info: Info,
    where: Annotated["SampleWhereClause", strawberry.lazy("api.types.sample")] | None = None,
) -> Optional[Annotated["SampleAggregate", strawberry.lazy("api.types.sample")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Taxon)
    relationship = mapper.relationships["samples"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    # Aggregate queries always return a single row, so just grab the first one
    result = rows[0] if rows else None
    aggregate_output = format_sample_aggregate_output(result)
    return SampleAggregate(aggregate=aggregate_output)


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
class TaxonWhereClauseMutations(TypedDict):
    id: UUIDComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class TaxonWhereClause(TypedDict):
    id: UUIDComparators | None
    producing_run_id: IntComparators | None
    owner_user_id: IntComparators | None
    collection_id: IntComparators | None
    wikipedia_id: Optional[StrComparators] | None
    description: Optional[StrComparators] | None
    common_name: Optional[StrComparators] | None
    name: Optional[StrComparators] | None
    is_phage: Optional[BoolComparators] | None
    upstream_database: Optional[
        Annotated["UpstreamDatabaseWhereClause", strawberry.lazy("api.types.upstream_database")]
    ] | None
    upstream_database_identifier: Optional[StrComparators] | None
    level: Optional[EnumComparators[TaxonLevel]] | None
    consensus_genomes: Optional[
        Annotated["ConsensusGenomeWhereClause", strawberry.lazy("api.types.consensus_genome")]
    ] | None
    reference_genomes: Optional[
        Annotated["ReferenceGenomeWhereClause", strawberry.lazy("api.types.reference_genome")]
    ] | None
    sequencing_reads: Optional[
        Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")]
    ] | None
    samples: Optional[Annotated["SampleWhereClause", strawberry.lazy("api.types.sample")]] | None


"""
Define Taxon type
"""


@strawberry.type
class Taxon(EntityInterface):
    id: strawberry.ID
    producing_run_id: Optional[int]
    owner_user_id: int
    collection_id: int
    wikipedia_id: Optional[str] = None
    description: Optional[str] = None
    common_name: Optional[str] = None
    name: str
    is_phage: bool
    upstream_database: Optional[
        Annotated["UpstreamDatabase", strawberry.lazy("api.types.upstream_database")]
    ] = load_upstream_database_rows  # type:ignore
    upstream_database_identifier: str
    level: TaxonLevel
    consensus_genomes: Sequence[
        Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]
    ] = load_consensus_genome_rows  # type:ignore
    consensus_genomes_aggregate: Optional[
        Annotated["ConsensusGenomeAggregate", strawberry.lazy("api.types.consensus_genome")]
    ] = load_consensus_genome_aggregate_rows  # type:ignore
    reference_genomes: Sequence[
        Annotated["ReferenceGenome", strawberry.lazy("api.types.reference_genome")]
    ] = load_reference_genome_rows  # type:ignore
    reference_genomes_aggregate: Optional[
        Annotated["ReferenceGenomeAggregate", strawberry.lazy("api.types.reference_genome")]
    ] = load_reference_genome_aggregate_rows  # type:ignore
    sequencing_reads: Sequence[
        Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]
    ] = load_sequencing_read_rows  # type:ignore
    sequencing_reads_aggregate: Optional[
        Annotated["SequencingReadAggregate", strawberry.lazy("api.types.sequencing_read")]
    ] = load_sequencing_read_aggregate_rows  # type:ignore
    samples: Sequence[Annotated["Sample", strawberry.lazy("api.types.sample")]] = load_sample_rows  # type:ignore
    samples_aggregate: Optional[
        Annotated["SampleAggregate", strawberry.lazy("api.types.sample")]
    ] = load_sample_aggregate_rows  # type:ignore


"""
We need to add this to each Queryable type so that strawberry will accept either our
Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
"""
Taxon.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.Taxon or type(obj) == Taxon
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
class TaxonNumericalColumns:
    producing_run_id: Optional[int] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class TaxonMinMaxColumns:
    producing_run_id: Optional[int] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    wikipedia_id: Optional[str] = None
    description: Optional[str] = None
    common_name: Optional[str] = None
    name: Optional[str] = None
    upstream_database_identifier: Optional[str] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class TaxonCountColumns(enum.Enum):
    wikipedia_id = "wikipedia_id"
    description = "description"
    common_name = "common_name"
    name = "name"
    is_phage = "is_phage"
    upstream_database = "upstream_database"
    upstream_database_identifier = "upstream_database_identifier"
    level = "level"
    tax_parent = "tax_parent"
    tax_subspecies = "tax_subspecies"
    tax_species = "tax_species"
    tax_genus = "tax_genus"
    tax_family = "tax_family"
    tax_order = "tax_order"
    tax_class = "tax_class"
    tax_phylum = "tax_phylum"
    tax_kingdom = "tax_kingdom"
    tax_superkingdom = "tax_superkingdom"
    consensus_genomes = "consensus_genomes"
    reference_genomes = "reference_genomes"
    sequencing_reads = "sequencing_reads"
    samples = "samples"
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
class TaxonAggregateFunctions:
    # This is a hack to accept "distinct" and "columns" as arguments to "count"
    @strawberry.field
    def count(self, distinct: Optional[bool] = False, columns: Optional[TaxonCountColumns] = None) -> Optional[int]:
        # Count gets set with the proper value in the resolver, so we just return it here
        return self.count  # type: ignore

    sum: Optional[TaxonNumericalColumns] = None
    avg: Optional[TaxonNumericalColumns] = None
    min: Optional[TaxonMinMaxColumns] = None
    max: Optional[TaxonMinMaxColumns] = None
    stddev: Optional[TaxonNumericalColumns] = None
    variance: Optional[TaxonNumericalColumns] = None


"""
Wrapper around TaxonAggregateFunctions
"""


@strawberry.type
class TaxonAggregate:
    aggregate: Optional[TaxonAggregateFunctions] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class TaxonCreateInput:
    collection_id: int
    wikipedia_id: Optional[str] = None
    description: Optional[str] = None
    common_name: Optional[str] = None
    name: str
    is_phage: bool
    upstream_database_id: strawberry.ID
    upstream_database_identifier: str
    level: TaxonLevel


@strawberry.input()
class TaxonUpdateInput:
    collection_id: Optional[int] = None
    wikipedia_id: Optional[str] = None
    description: Optional[str] = None
    common_name: Optional[str] = None
    name: Optional[str] = None
    is_phage: Optional[bool] = None
    upstream_database_id: Optional[strawberry.ID] = None
    upstream_database_identifier: Optional[str] = None
    level: Optional[TaxonLevel] = None


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_taxa(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[TaxonWhereClause] = None,
) -> typing.Sequence[Taxon]:
    """
    Resolve Taxon objects. Used for queries (see api/queries.py).
    """
    return await get_db_rows(db.Taxon, session, cerbos_client, principal, where, [])  # type: ignore


def format_taxon_aggregate_output(query_results: RowMapping) -> TaxonAggregateFunctions:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = TaxonAggregateFunctions()
    for aggregate_name, value in query_results.items():
        if aggregate_name == "count":
            output.count = value
        else:
            aggregator_fn, col_name = aggregate_name.split("_", 1)
            # Filter out the group_by key from the results if one was provided.
            if aggregator_fn in aggregator_map.keys():
                if not getattr(output, aggregator_fn):
                    if aggregate_name in ["min", "max"]:
                        setattr(output, aggregator_fn, TaxonMinMaxColumns())
                    else:
                        setattr(output, aggregator_fn, TaxonNumericalColumns())
                setattr(getattr(output, aggregator_fn), col_name, value)
    return output


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_taxa_aggregate(
    info: Info,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[TaxonWhereClause] = None,
) -> TaxonAggregate:
    """
    Aggregate values for Taxon objects. Used for queries (see api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on
    # TODO: not sure why selected_fields is a list
    # The first list of selections will always be ["aggregate"], so just grab the first item
    selections = info.selected_fields[0].selections[0].selections
    rows = await get_aggregate_db_rows(db.Taxon, session, cerbos_client, principal, where, selections, [])  # type: ignore
    aggregate_output = format_taxon_aggregate_output(rows)
    return TaxonAggregate(aggregate=aggregate_output)


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_taxon(
    input: TaxonCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> db.Entity:
    """
    Create a new Taxon object. Used for mutations (see api/mutations.py).
    """
    params = input.__dict__

    # Validate that user can create entity in this collection
    attr = {"collection_id": input.collection_id}
    resource = Resource(id="NEW_ID", kind=db.Taxon.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise PlatformicsException("Unauthorized: Cannot create entity in this collection")

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.Taxon(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_taxon(
    input: TaxonUpdateInput,
    where: TaxonWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Update Taxon objects. Used for mutations (see api/mutations.py).
    """
    params = input.__dict__

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise PlatformicsException("No fields to update")

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(db.Taxon, session, cerbos_client, principal, where, [], CerbosAction.UPDATE)
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot update entities")

    # Validate that the user has access to the new collection ID
    if input.collection_id:
        attr = {"collection_id": input.collection_id}
        resource = Resource(id="SOME_ID", kind=db.Taxon.__tablename__, attr=attr)
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
async def delete_taxon(
    where: TaxonWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Delete Taxon objects. Used for mutations (see api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(db.Taxon, session, cerbos_client, principal, where, [], CerbosAction.DELETE)
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
