# Auto-generated by running 'make codegen'. Do not edit.
# Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.

import typing
from typing import TYPE_CHECKING, Annotated, Optional

import database.models as db
import strawberry
from api.core.helpers import get_db_rows
from api.types.entities import EntityInterface
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal
from fastapi import Depends
from platformics.api.core.deps import get_cerbos_client, get_db_session, require_auth_principal
from platformics.api.core.gql_to_sql import (
    EnumComparators,
    IntComparators,
    StrComparators,
    UUIDComparators,
    BoolComparators,
)
from platformics.api.core.strawberry_extensions import DependencyExtension
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.types import Info
from typing_extensions import TypedDict
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


# ------------------------------------------------------------------------------
# Dataloaders
# ------------------------------------------------------------------------------


@strawberry.field(extensions=[DependencyExtension()])
async def load_upstream_database_rows(
    root: "Taxon",
    info: Info,
    where: Annotated["UpstreamDatabaseWhereClause", strawberry.lazy("api.types.upstream_database")] | None = None,
) -> Optional[Annotated["UpstreamDatabase", strawberry.lazy("api.types.upstream_database")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Taxon)
    relationship = mapper.relationships["upstream_database"]
    return await dataloader.loader_for(relationship, where).load(root.upstream_database_id)  # type:ignore


@strawberry.field(extensions=[DependencyExtension()])
async def load_consensus_genome_rows(
    root: "Taxon",
    info: Info,
    where: Annotated["ConsensusGenomeWhereClause", strawberry.lazy("api.types.consensus_genome")] | None = None,
) -> typing.Sequence[Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Taxon)
    relationship = mapper.relationships["consensus_genome"]
    return await dataloader.loader_for(relationship, where).load(root.id)  # type:ignore


@strawberry.field(extensions=[DependencyExtension()])
async def load_reference_genome_rows(
    root: "Taxon",
    info: Info,
    where: Annotated["ReferenceGenomeWhereClause", strawberry.lazy("api.types.reference_genome")] | None = None,
) -> typing.Sequence[Annotated["ReferenceGenome", strawberry.lazy("api.types.reference_genome")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Taxon)
    relationship = mapper.relationships["reference_genome"]
    return await dataloader.loader_for(relationship, where).load(root.id)  # type:ignore


@strawberry.field(extensions=[DependencyExtension()])
async def load_sequencing_read_rows(
    root: "Taxon",
    info: Info,
    where: Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")] | None = None,
) -> typing.Sequence[Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Taxon)
    relationship = mapper.relationships["sequencing_read"]
    return await dataloader.loader_for(relationship, where).load(root.id)  # type:ignore


@strawberry.field(extensions=[DependencyExtension()])
async def load_sample_rows(
    root: "Taxon",
    info: Info,
    where: Annotated["SampleWhereClause", strawberry.lazy("api.types.sample")] | None = None,
) -> typing.Sequence[Annotated["Sample", strawberry.lazy("api.types.sample")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Taxon)
    relationship = mapper.relationships["sample"]
    return await dataloader.loader_for(relationship, where).load(root.id)  # type:ignore


# ------------------------------------------------------------------------------
# Define Strawberry GQL types
# ------------------------------------------------------------------------------


# Supported WHERE clause attributes
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
    tax_id: Optional[IntComparators] | None
    tax_id_parent: Optional[IntComparators] | None
    tax_id_species: Optional[IntComparators] | None
    tax_id_genus: Optional[IntComparators] | None
    tax_id_family: Optional[IntComparators] | None
    tax_id_order: Optional[IntComparators] | None
    tax_id_class: Optional[IntComparators] | None
    tax_id_phylum: Optional[IntComparators] | None
    tax_id_kingdom: Optional[IntComparators] | None
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
    entity_id: Optional[UUIDComparators] | None


# Define Taxon type
@strawberry.type
class Taxon(EntityInterface):
    id: strawberry.ID
    producing_run_id: int
    owner_user_id: int
    collection_id: int
    wikipedia_id: str
    description: str
    common_name: str
    name: str
    is_phage: bool
    upstream_database: Optional[
        Annotated["UpstreamDatabase", strawberry.lazy("api.types.upstream_database")]
    ] = load_upstream_database_rows
    upstream_database_identifier: str
    level: TaxonLevel
    tax_id: int
    tax_id_parent: int
    tax_id_species: int
    tax_id_genus: int
    tax_id_family: int
    tax_id_order: int
    tax_id_class: int
    tax_id_phylum: int
    tax_id_kingdom: int
    consensus_genomes: typing.Sequence[
        Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]
    ] = load_consensus_genome_rows
    reference_genomes: typing.Sequence[
        Annotated["ReferenceGenome", strawberry.lazy("api.types.reference_genome")]
    ] = load_reference_genome_rows
    sequencing_reads: typing.Sequence[
        Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]
    ] = load_sequencing_read_rows
    samples: typing.Sequence[Annotated["Sample", strawberry.lazy("api.types.sample")]] = load_sample_rows
    entity_id: strawberry.ID


# We need to add this to each Queryable type so that strawberry will accept either our
# Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
Taxon.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.Taxon or type(obj) == Taxon
)


# Resolvers used in api/queries
@strawberry.field(extensions=[DependencyExtension()])
async def resolve_taxon(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[TaxonWhereClause] = None,
) -> typing.Sequence[Taxon]:
    return await get_db_rows(db.Taxon, session, cerbos_client, principal, where, [])  # type: ignore
