# Auto-generated by running 'make codegen'. Do not edit.
# Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.

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
    from api.types.reference_genome import ReferenceGenomeWhereClause, ReferenceGenome
    from api.types.consensus_genome import ConsensusGenomeWhereClause, ConsensusGenome

    pass
else:
    ReferenceGenomeWhereClause = "ReferenceGenomeWhereClause"
    ReferenceGenome = "ReferenceGenome"
    ConsensusGenomeWhereClause = "ConsensusGenomeWhereClause"
    ConsensusGenome = "ConsensusGenome"
    pass


# ------------------------------------------------------------------------------
# Dataloaders
# ------------------------------------------------------------------------------
@strawberry.field
async def load_reference_genome_rows(
    root: "GenomicRange",
    info: Info,
    where: Annotated["ReferenceGenomeWhereClause", strawberry.lazy("api.types.reference_genome")] | None = None,
) -> Optional[Annotated["ReferenceGenome", strawberry.lazy("api.types.reference_genome")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.GenomicRange)
    relationship = mapper.relationships["reference_genome"]
    return await dataloader.loader_for(relationship, where).load(root.reference_genome_id)  # type:ignore


@relay.connection(
    relay.ListConnection[Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]]  # type:ignore
)
async def load_consensus_genome_rows(
    root: "GenomicRange",
    info: Info,
    where: Annotated["ConsensusGenomeWhereClause", strawberry.lazy("api.types.consensus_genome")] | None = None,
) -> Sequence[Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.GenomicRange)
    relationship = mapper.relationships["consensus_genome"]
    return await dataloader.loader_for(relationship, where).load(root.id)  # type:ignore


# ------------------------------------------------------------------------------
# Dataloader for File object
# ------------------------------------------------------------------------------


# Given a list of GenomicRange IDs for a certain file type, return related Files
def load_files_from(attr_name: str) -> Callable:
    @strawberry.field
    async def load_files(
        root: "GenomicRange",
        info: Info,
        where: Annotated["FileWhereClause", strawberry.lazy("api.files")] | None = None,
    ) -> Optional[Annotated["File", strawberry.lazy("api.files")]]:
        dataloader = info.context["sqlalchemy_loader"]
        mapper = inspect(db.GenomicRange)
        relationship = mapper.relationships[attr_name]
        return await dataloader.loader_for(relationship, where).load(getattr(root, f"{attr_name}_id"))  # type:ignore

    return load_files


# ------------------------------------------------------------------------------
# Define Strawberry GQL types
# ------------------------------------------------------------------------------


# Supported WHERE clause attributes
@strawberry.input
class GenomicRangeWhereClause(TypedDict):
    id: UUIDComparators | None
    producing_run_id: IntComparators | None
    owner_user_id: IntComparators | None
    collection_id: IntComparators | None
    reference_genome: Optional[
        Annotated["ReferenceGenomeWhereClause", strawberry.lazy("api.types.reference_genome")]
    ] | None
    consensus_genomes: Optional[
        Annotated["ConsensusGenomeWhereClause", strawberry.lazy("api.types.consensus_genome")]
    ] | None
    entity_id: Optional[UUIDComparators] | None


# Define GenomicRange type
@strawberry.type
class GenomicRange(EntityInterface):
    id: strawberry.ID
    producing_run_id: int
    owner_user_id: int
    collection_id: int
    reference_genome: Optional[
        Annotated["ReferenceGenome", strawberry.lazy("api.types.reference_genome")]
    ] = load_reference_genome_rows  # type:ignore
    file_id: strawberry.ID
    file: Annotated["File", strawberry.lazy("api.files")] = load_files_from("file")  # type: ignore
    consensus_genomes: typing.Sequence[
        Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]
    ] = load_consensus_genome_rows
    entity_id: strawberry.ID


# We need to add this to each Queryable type so that strawberry will accept either our
# Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
GenomicRange.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.GenomicRange or type(obj) == GenomicRange
)


# Resolvers used in api/queries
@strawberry.field(extensions=[DependencyExtension()])
async def resolve_genomic_range(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[GenomicRangeWhereClause] = None,
) -> typing.Sequence[GenomicRange]:
    return await get_db_rows(db.GenomicRange, session, cerbos_client, principal, where, [])  # type: ignore
