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
from platformics.api.core.helpers import get_db_rows
from api.types.entities import EntityInterface
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource
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
from platformics.security.authorization import CerbosAction
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import relay
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
    tax_id: int
    tax_id_parent: int
    tax_id_species: int
    tax_id_genus: int
    tax_id_family: int
    tax_id_order: int
    tax_id_class: int
    tax_id_phylum: int
    tax_id_kingdom: int
    consensus_genomes: Sequence[
        Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]
    ] = load_consensus_genome_rows  # type:ignore
    reference_genomes: Sequence[
        Annotated["ReferenceGenome", strawberry.lazy("api.types.reference_genome")]
    ] = load_reference_genome_rows  # type:ignore
    sequencing_reads: Sequence[
        Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]
    ] = load_sequencing_read_rows  # type:ignore
    samples: Sequence[Annotated["Sample", strawberry.lazy("api.types.sample")]] = load_sample_rows  # type:ignore


"""
We need to add this to each Queryable type so that strawberry will accept either our
Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
"""
Taxon.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.Taxon or type(obj) == Taxon
)

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
    tax_id: int
    tax_id_parent: int
    tax_id_species: int
    tax_id_genus: int
    tax_id_family: int
    tax_id_order: int
    tax_id_class: int
    tax_id_phylum: int
    tax_id_kingdom: int


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
    tax_id: Optional[int] = None
    tax_id_parent: Optional[int] = None
    tax_id_species: Optional[int] = None
    tax_id_genus: Optional[int] = None
    tax_id_family: Optional[int] = None
    tax_id_order: Optional[int] = None
    tax_id_class: Optional[int] = None
    tax_id_phylum: Optional[int] = None
    tax_id_kingdom: Optional[int] = None


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
        raise Exception("Unauthorized: Cannot create entity in this collection")

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
        raise Exception("No fields to update")

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(db.Taxon, session, cerbos_client, principal, where, [], CerbosAction.UPDATE)
    if len(entities) == 0:
        raise Exception("Unauthorized: Cannot update entities")

    # Validate that the user has access to the new collection ID
    if input.collection_id:
        attr = {"collection_id": input.collection_id}
        resource = Resource(id="SOME_ID", kind=db.Taxon.__tablename__, attr=attr)
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
        raise Exception("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
