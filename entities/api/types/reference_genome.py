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
    IntComparators,
    StrComparators,
    UUIDComparators,
)
from platformics.api.core.strawberry_extensions import DependencyExtension
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import relay
from strawberry.types import Info
from typing_extensions import TypedDict

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.taxon import TaxonWhereClause, Taxon
    from api.types.sequence_alignment_index import SequenceAlignmentIndexWhereClause, SequenceAlignmentIndex
    from api.types.consensus_genome import ConsensusGenomeWhereClause, ConsensusGenome
    from api.types.genomic_range import GenomicRangeWhereClause, GenomicRange

    pass
else:
    TaxonWhereClause = "TaxonWhereClause"
    Taxon = "Taxon"
    SequenceAlignmentIndexWhereClause = "SequenceAlignmentIndexWhereClause"
    SequenceAlignmentIndex = "SequenceAlignmentIndex"
    ConsensusGenomeWhereClause = "ConsensusGenomeWhereClause"
    ConsensusGenome = "ConsensusGenome"
    GenomicRangeWhereClause = "GenomicRangeWhereClause"
    GenomicRange = "GenomicRange"
    pass


# ------------------------------------------------------------------------------
# Dataloaders
# ------------------------------------------------------------------------------
@strawberry.field
async def load_taxon_rows(
    root: "ReferenceGenome",
    info: Info,
    where: Annotated["TaxonWhereClause", strawberry.lazy("api.types.taxon")] | None = None,
) -> Optional[Annotated["Taxon", strawberry.lazy("api.types.taxon")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.ReferenceGenome)
    relationship = mapper.relationships["taxon"]
    return await dataloader.loader_for(relationship, where).load(root.taxon_id)  # type:ignore


@relay.connection(
    relay.ListConnection[
        Annotated["SequenceAlignmentIndex", strawberry.lazy("api.types.sequence_alignment_index")]
    ]  # type:ignore
)
async def load_sequence_alignment_index_rows(
    root: "ReferenceGenome",
    info: Info,
    where: Annotated["SequenceAlignmentIndexWhereClause", strawberry.lazy("api.types.sequence_alignment_index")]
    | None = None,
) -> Sequence[Annotated["SequenceAlignmentIndex", strawberry.lazy("api.types.sequence_alignment_index")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.ReferenceGenome)
    relationship = mapper.relationships["sequence_alignment_index"]
    return await dataloader.loader_for(relationship, where).load(root.id)  # type:ignore


@relay.connection(
    relay.ListConnection[Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]]  # type:ignore
)
async def load_consensus_genome_rows(
    root: "ReferenceGenome",
    info: Info,
    where: Annotated["ConsensusGenomeWhereClause", strawberry.lazy("api.types.consensus_genome")] | None = None,
) -> Sequence[Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.ReferenceGenome)
    relationship = mapper.relationships["consensus_genome"]
    return await dataloader.loader_for(relationship, where).load(root.id)  # type:ignore


@relay.connection(
    relay.ListConnection[Annotated["GenomicRange", strawberry.lazy("api.types.genomic_range")]]  # type:ignore
)
async def load_genomic_range_rows(
    root: "ReferenceGenome",
    info: Info,
    where: Annotated["GenomicRangeWhereClause", strawberry.lazy("api.types.genomic_range")] | None = None,
) -> Sequence[Annotated["GenomicRange", strawberry.lazy("api.types.genomic_range")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.ReferenceGenome)
    relationship = mapper.relationships["genomic_range"]
    return await dataloader.loader_for(relationship, where).load(root.id)  # type:ignore


# ------------------------------------------------------------------------------
# Dataloader for File object
# ------------------------------------------------------------------------------


# Given a list of ReferenceGenome IDs for a certain file type, return related Files
def load_files_from(attr_name: str) -> Callable:
    @strawberry.field
    async def load_files(
        root: "ReferenceGenome",
        info: Info,
        where: Annotated["FileWhereClause", strawberry.lazy("api.files")] | None = None,
    ) -> Optional[Annotated["File", strawberry.lazy("api.files")]]:
        dataloader = info.context["sqlalchemy_loader"]
        mapper = inspect(db.ReferenceGenome)
        relationship = mapper.relationships[attr_name]
        return await dataloader.loader_for(relationship, where).load(getattr(root, f"{attr_name}_id"))  # type:ignore

    return load_files


# ------------------------------------------------------------------------------
# Define Strawberry GQL types
# ------------------------------------------------------------------------------


# Supported WHERE clause attributes
@strawberry.input
class ReferenceGenomeWhereClause(TypedDict):
    id: UUIDComparators | None
    producing_run_id: IntComparators | None
    owner_user_id: IntComparators | None
    collection_id: IntComparators | None
    name: Optional[StrComparators] | None
    description: Optional[StrComparators] | None
    taxon: Optional[Annotated["TaxonWhereClause", strawberry.lazy("api.types.taxon")]] | None
    accession_id: Optional[StrComparators] | None
    sequence_alignment_indices: Optional[
        Annotated["SequenceAlignmentIndexWhereClause", strawberry.lazy("api.types.sequence_alignment_index")]
    ] | None
    consensus_genomes: Optional[
        Annotated["ConsensusGenomeWhereClause", strawberry.lazy("api.types.consensus_genome")]
    ] | None
    genomic_ranges: Optional[Annotated["GenomicRangeWhereClause", strawberry.lazy("api.types.genomic_range")]] | None
    entity_id: Optional[UUIDComparators] | None


# Define ReferenceGenome type
@strawberry.type
class ReferenceGenome(EntityInterface):
    id: strawberry.ID
    file_id: strawberry.ID
    file: Annotated["File", strawberry.lazy("api.files")] = load_files_from("file")  # type: ignore
    file_index_id: strawberry.ID
    file_index: Annotated["File", strawberry.lazy("api.files")] = load_files_from("file_index")  # type: ignore
    name: str
    description: str
    taxon: Optional[Annotated["Taxon", strawberry.lazy("api.types.taxon")]] = load_taxon_rows  # type:ignore
    accession_id: str
    sequence_alignment_indices: Sequence[
        Annotated["SequenceAlignmentIndex", strawberry.lazy("api.types.sequence_alignment_index")]
    ] = load_sequence_alignment_index_rows  # type:ignore
    consensus_genomes: Sequence[
        Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]
    ] = load_consensus_genome_rows  # type:ignore
    genomic_ranges: Sequence[
        Annotated["GenomicRange", strawberry.lazy("api.types.genomic_range")]
    ] = load_genomic_range_rows  # type:ignore
    entity_id: strawberry.ID


# ------------------------------------------------------------------------------
# Mutation types
# ------------------------------------------------------------------------------


@strawberry.input()
class ReferenceGenomeCreateInput:
    file_id: strawberry.ID
    file_index_id: strawberry.ID
    name: str
    description: str
    taxon_id: strawberry.ID
    accession_id: str


@strawberry.input()
class ReferenceGenomeUpdateInput:
    file_id: Optional[strawberry.ID]
    file_index_id: Optional[strawberry.ID]
    name: Optional[str]
    description: Optional[str]
    taxon_id: Optional[strawberry.ID]
    accession_id: Optional[str]


# ------------------------------------------------------------------------------
# Setup and utilities
# ------------------------------------------------------------------------------

# We need to add this to each Queryable type so that strawberry will accept either our
# Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
ReferenceGenome.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.ReferenceGenome or type(obj) == ReferenceGenome
)


# Resolvers used in api/queries
@strawberry.field(extensions=[DependencyExtension()])
async def resolve_reference_genome(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[ReferenceGenomeWhereClause] = None,
) -> typing.Sequence[ReferenceGenome]:
    return await get_db_rows(db.ReferenceGenome, session, cerbos_client, principal, where, [])  # type: ignore
