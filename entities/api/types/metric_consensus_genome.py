# Auto-generated by running 'make codegen'. Do not edit.
# Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.

# ruff: noqa: E501 Line too long

import typing
from typing import TYPE_CHECKING, Annotated, Optional, Callable

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
from strawberry.types import Info
from typing_extensions import TypedDict

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.consensus_genome import ConsensusGenomeWhereClause, ConsensusGenome

    pass
else:
    ConsensusGenomeWhereClause = "ConsensusGenomeWhereClause"
    ConsensusGenome = "ConsensusGenome"
    pass


# ------------------------------------------------------------------------------
# Dataloaders
# ------------------------------------------------------------------------------
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


# ------------------------------------------------------------------------------
# Dataloader for File object
# ------------------------------------------------------------------------------


# Given a list of MetricConsensusGenome IDs for a certain file type, return related Files
def load_files_from(attr_name: str) -> Callable:
    @strawberry.field
    async def load_files(
        root: "MetricConsensusGenome",
        info: Info,
        where: Annotated["FileWhereClause", strawberry.lazy("api.files")] | None = None,
    ) -> Optional[Annotated["File", strawberry.lazy("api.files")]]:
        dataloader = info.context["sqlalchemy_loader"]
        mapper = inspect(db.MetricConsensusGenome)
        relationship = mapper.relationships[attr_name]
        return await dataloader.loader_for(relationship, where).load(getattr(root, f"{attr_name}_id"))  # type:ignore

    return load_files


# ------------------------------------------------------------------------------
# Define Strawberry GQL types
# ------------------------------------------------------------------------------


# Supported WHERE clause attributes
@strawberry.input
class MetricConsensusGenomeWhereClause(TypedDict):
    id: UUIDComparators | None
    producing_run_id: IntComparators | None
    owner_user_id: IntComparators | None
    collection_id: IntComparators | None
    consensus_genome: Optional[
        Annotated["ConsensusGenomeWhereClause", strawberry.lazy("api.types.consensus_genome")]
    ] | None
    total_reads: Optional[IntComparators] | None
    mapped_reads: Optional[IntComparators] | None
    ref_snps: Optional[IntComparators] | None
    n_actg: Optional[IntComparators] | None
    n_missing: Optional[IntComparators] | None
    n_ambiguous: Optional[IntComparators] | None
    entity_id: Optional[UUIDComparators] | None


# Define MetricConsensusGenome type
@strawberry.type
class MetricConsensusGenome(EntityInterface):
    id: strawberry.ID
    consensus_genome: Optional[
        Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]
    ] = load_consensus_genome_rows  # type:ignore
    total_reads: int
    mapped_reads: int
    ref_snps: int
    n_actg: int
    n_missing: int
    n_ambiguous: int
    coverage_viz_summary_file_id: strawberry.ID
    coverage_viz_summary_file: Annotated["File", strawberry.lazy("api.files")] = load_files_from("coverage_viz_summary_file")  # type: ignore
    entity_id: strawberry.ID


# ------------------------------------------------------------------------------
# Mutation types
# ------------------------------------------------------------------------------


@strawberry.input()
class MetricConsensusGenomeCreateInput:
    consensus_genome_id: strawberry.ID
    total_reads: int
    mapped_reads: int
    ref_snps: int
    n_actg: int
    n_missing: int
    n_ambiguous: int
    coverage_viz_summary_file_id: strawberry.ID


@strawberry.input()
class MetricConsensusGenomeUpdateInput:
    consensus_genome_id: Optional[strawberry.ID]
    total_reads: Optional[int]
    mapped_reads: Optional[int]
    ref_snps: Optional[int]
    n_actg: Optional[int]
    n_missing: Optional[int]
    n_ambiguous: Optional[int]
    coverage_viz_summary_file_id: Optional[strawberry.ID]


# ------------------------------------------------------------------------------
# Setup and utilities
# ------------------------------------------------------------------------------

# We need to add this to each Queryable type so that strawberry will accept either our
# Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
MetricConsensusGenome.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.MetricConsensusGenome or type(obj) == MetricConsensusGenome
)


# Resolvers used in api/queries
@strawberry.field(extensions=[DependencyExtension()])
async def resolve_metric_consensus_genome(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[MetricConsensusGenomeWhereClause] = None,
) -> typing.Sequence[MetricConsensusGenome]:
    return await get_db_rows(db.MetricConsensusGenome, session, cerbos_client, principal, where, [])  # type: ignore
