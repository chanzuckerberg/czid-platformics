# Auto-generated by running 'make codegen'. Do not edit.
# Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.

# ruff: noqa: E501 Line too long

import typing
from typing import TYPE_CHECKING, Annotated, Optional, Sequence, Callable

import database.models as db
import strawberry
from api.core.helpers import get_db_rows
from api.files import File, FileWhereClause
from api.types.entities import EntityInterface
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal
from fastapi import Depends
from platformics.api.core.deps import get_cerbos_client, get_db_session, require_auth_principal
from platformics.api.core.gql_to_sql import (
    EnumComparators,
    IntComparators,
    UUIDComparators,
    BoolComparators,
)
from platformics.api.core.strawberry_extensions import DependencyExtension
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import relay
from strawberry.types import Info
from typing_extensions import TypedDict
from support.enums import SequencingProtocol, SequencingTechnology, NucleicAcid

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.sample import SampleWhereClause, Sample
    from api.types.taxon import TaxonWhereClause, Taxon
    from api.types.consensus_genome import ConsensusGenomeWhereClause, ConsensusGenome
    from api.types.contig import ContigWhereClause, Contig

    pass
else:
    SampleWhereClause = "SampleWhereClause"
    Sample = "Sample"
    TaxonWhereClause = "TaxonWhereClause"
    Taxon = "Taxon"
    ConsensusGenomeWhereClause = "ConsensusGenomeWhereClause"
    ConsensusGenome = "ConsensusGenome"
    ContigWhereClause = "ContigWhereClause"
    Contig = "Contig"
    pass


# ------------------------------------------------------------------------------
# Dataloaders
# ------------------------------------------------------------------------------
@strawberry.field
async def load_sample_rows(
    root: "SequencingRead",
    info: Info,
    where: Annotated["SampleWhereClause", strawberry.lazy("api.types.sample")] | None = None,
) -> Optional[Annotated["Sample", strawberry.lazy("api.types.sample")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.SequencingRead)
    relationship = mapper.relationships["sample"]
    return await dataloader.loader_for(relationship, where).load(root.sample_id)  # type:ignore


@strawberry.field
async def load_taxon_rows(
    root: "SequencingRead",
    info: Info,
    where: Annotated["TaxonWhereClause", strawberry.lazy("api.types.taxon")] | None = None,
) -> Optional[Annotated["Taxon", strawberry.lazy("api.types.taxon")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.SequencingRead)
    relationship = mapper.relationships["taxon"]
    return await dataloader.loader_for(relationship, where).load(root.taxon_id)  # type:ignore


@relay.connection(
    relay.ListConnection[Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]]  # type:ignore
)
async def load_consensus_genome_rows(
    root: "SequencingRead",
    info: Info,
    where: Annotated["ConsensusGenomeWhereClause", strawberry.lazy("api.types.consensus_genome")] | None = None,
) -> Sequence[Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.SequencingRead)
    relationship = mapper.relationships["consensus_genome"]
    return await dataloader.loader_for(relationship, where).load(root.id)  # type:ignore


@relay.connection(
    relay.ListConnection[Annotated["Contig", strawberry.lazy("api.types.contig")]]  # type:ignore
)
async def load_contig_rows(
    root: "SequencingRead",
    info: Info,
    where: Annotated["ContigWhereClause", strawberry.lazy("api.types.contig")] | None = None,
) -> Sequence[Annotated["Contig", strawberry.lazy("api.types.contig")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.SequencingRead)
    relationship = mapper.relationships["contig"]
    return await dataloader.loader_for(relationship, where).load(root.id)  # type:ignore


# ------------------------------------------------------------------------------
# Dataloader for File object
# ------------------------------------------------------------------------------


# Given a list of SequencingRead IDs for a certain file type, return related Files
def load_files_from(attr_name: str) -> Callable:
    @strawberry.field
    async def load_files(
        root: "SequencingRead",
        info: Info,
        where: Annotated["FileWhereClause", strawberry.lazy("api.files")] | None = None,
    ) -> Optional[Annotated["File", strawberry.lazy("api.files")]]:
        dataloader = info.context["sqlalchemy_loader"]
        mapper = inspect(db.SequencingRead)
        relationship = mapper.relationships[attr_name]
        return await dataloader.loader_for(relationship, where).load(getattr(root, f"{attr_name}_id"))  # type:ignore

    return load_files


# ------------------------------------------------------------------------------
# Define Strawberry GQL types
# ------------------------------------------------------------------------------


# Supported WHERE clause attributes
@strawberry.input
class SequencingReadWhereClause(TypedDict):
    id: UUIDComparators | None
    producing_run_id: IntComparators | None
    owner_user_id: IntComparators | None
    collection_id: IntComparators | None
    sample: Optional[Annotated["SampleWhereClause", strawberry.lazy("api.types.sample")]] | None
    protocol: Optional[EnumComparators[SequencingProtocol]] | None
    technology: Optional[EnumComparators[SequencingTechnology]] | None
    nucleic_acid: Optional[EnumComparators[NucleicAcid]] | None
    has_ercc: Optional[BoolComparators] | None
    taxon: Optional[Annotated["TaxonWhereClause", strawberry.lazy("api.types.taxon")]] | None
    consensus_genomes: Optional[
        Annotated["ConsensusGenomeWhereClause", strawberry.lazy("api.types.consensus_genome")]
    ] | None
    contigs: Optional[Annotated["ContigWhereClause", strawberry.lazy("api.types.contig")]] | None
    entity_id: Optional[UUIDComparators] | None


# Define SequencingRead type
@strawberry.type
class SequencingRead(EntityInterface):
    id: strawberry.ID
    sample: Optional[Annotated["Sample", strawberry.lazy("api.types.sample")]] = load_sample_rows  # type:ignore
    protocol: SequencingProtocol
    r1_file_id: strawberry.ID
    r1_file: Annotated["File", strawberry.lazy("api.files")] = load_files_from("r1_file")  # type: ignore
    r2_file_id: strawberry.ID
    r2_file: Annotated["File", strawberry.lazy("api.files")] = load_files_from("r2_file")  # type: ignore
    technology: SequencingTechnology
    nucleic_acid: NucleicAcid
    has_ercc: bool
    taxon: Optional[Annotated["Taxon", strawberry.lazy("api.types.taxon")]] = load_taxon_rows  # type:ignore
    primer_file_id: strawberry.ID
    primer_file: Annotated["File", strawberry.lazy("api.files")] = load_files_from("primer_file")  # type: ignore
    consensus_genomes: Sequence[
        Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]
    ] = load_consensus_genome_rows  # type:ignore
    contigs: Sequence[Annotated["Contig", strawberry.lazy("api.types.contig")]] = load_contig_rows  # type:ignore
    entity_id: strawberry.ID


# ------------------------------------------------------------------------------
# Mutation types
# ------------------------------------------------------------------------------


@strawberry.input()
class SequencingReadCreateInput:
    sample_id: strawberry.ID
    protocol: SequencingProtocol
    r1_file_id: strawberry.ID
    r2_file_id: strawberry.ID
    technology: SequencingTechnology
    nucleic_acid: NucleicAcid
    has_ercc: bool
    taxon_id: strawberry.ID
    primer_file_id: strawberry.ID


@strawberry.input()
class SequencingReadUpdateInput:
    sample_id: Optional[strawberry.ID]
    protocol: Optional[SequencingProtocol]
    r1_file_id: Optional[strawberry.ID]
    r2_file_id: Optional[strawberry.ID]
    technology: Optional[SequencingTechnology]
    nucleic_acid: Optional[NucleicAcid]
    has_ercc: Optional[bool]
    taxon_id: Optional[strawberry.ID]
    primer_file_id: Optional[strawberry.ID]


# ------------------------------------------------------------------------------
# Setup and utilities
# ------------------------------------------------------------------------------

# We need to add this to each Queryable type so that strawberry will accept either our
# Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
SequencingRead.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.SequencingRead or type(obj) == SequencingRead
)


# Resolvers used in api/queries
@strawberry.field(extensions=[DependencyExtension()])
async def resolve_sequencing_read(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[SequencingReadWhereClause] = None,
) -> typing.Sequence[SequencingRead]:
    return await get_db_rows(db.SequencingRead, session, cerbos_client, principal, where, [])  # type: ignore
