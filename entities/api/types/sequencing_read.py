"""
GraphQL type for SequencingRead

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long

import typing
from typing import TYPE_CHECKING, Annotated, Optional, Sequence, Callable

import database.models as db
import strawberry
from platformics.api.core.helpers import get_db_rows
from api.files import File, FileWhereClause
from api.types.entities import EntityInterface
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource
from fastapi import Depends
from platformics.api.core.deps import get_cerbos_client, get_db_session, require_auth_principal
from platformics.api.core.gql_to_sql import (
    EnumComparators,
    IntComparators,
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
from support.enums import SequencingProtocol, SequencingTechnology, NucleicAcid

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.sample import SampleWhereClause, Sample
    from api.types.taxon import TaxonWhereClause, Taxon
    from api.types.genomic_range import GenomicRangeWhereClause, GenomicRange
    from api.types.consensus_genome import ConsensusGenomeWhereClause, ConsensusGenome
    from api.types.contig import ContigWhereClause, Contig

    pass
else:
    SampleWhereClause = "SampleWhereClause"
    Sample = "Sample"
    TaxonWhereClause = "TaxonWhereClause"
    Taxon = "Taxon"
    GenomicRangeWhereClause = "GenomicRangeWhereClause"
    GenomicRange = "GenomicRange"
    ConsensusGenomeWhereClause = "ConsensusGenomeWhereClause"
    ConsensusGenome = "ConsensusGenome"
    ContigWhereClause = "ContigWhereClause"
    Contig = "Contig"
    pass


"""
------------------------------------------------------------------------------
Dataloaders
------------------------------------------------------------------------------
These are batching functions for loading related objects to avoid N+1 queries.
"""


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


@strawberry.field
async def load_genomic_range_rows(
    root: "SequencingRead",
    info: Info,
    where: Annotated["GenomicRangeWhereClause", strawberry.lazy("api.types.genomic_range")] | None = None,
) -> Optional[Annotated["GenomicRange", strawberry.lazy("api.types.genomic_range")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.SequencingRead)
    relationship = mapper.relationships["primer_file"]
    return await dataloader.loader_for(relationship, where).load(root.primer_file_id)  # type:ignore


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
    relationship = mapper.relationships["consensus_genomes"]
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
    relationship = mapper.relationships["contigs"]
    return await dataloader.loader_for(relationship, where).load(root.id)  # type:ignore


"""
------------------------------------------------------------------------------
Dataloader for File object
------------------------------------------------------------------------------
"""


def load_files_from(attr_name: str) -> Callable:
    @strawberry.field
    async def load_files(
        root: "SequencingRead",
        info: Info,
        where: Annotated["FileWhereClause", strawberry.lazy("api.files")] | None = None,
    ) -> Optional[Annotated["File", strawberry.lazy("api.files")]]:
        """
        Given a list of SequencingRead IDs for a certain file type, return related Files
        """
        dataloader = info.context["sqlalchemy_loader"]
        mapper = inspect(db.SequencingRead)
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
class SequencingReadWhereClauseMutations(TypedDict):
    id: UUIDComparators | None


"""
Supported WHERE clause attributes
"""


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
    primer_file: Optional[Annotated["GenomicRangeWhereClause", strawberry.lazy("api.types.genomic_range")]] | None
    consensus_genomes: Optional[
        Annotated["ConsensusGenomeWhereClause", strawberry.lazy("api.types.consensus_genome")]
    ] | None
    contigs: Optional[Annotated["ContigWhereClause", strawberry.lazy("api.types.contig")]] | None


"""
Define SequencingRead type
"""


@strawberry.type
class SequencingRead(EntityInterface):
    id: strawberry.ID
    producing_run_id: Optional[int]
    owner_user_id: int
    collection_id: int
    sample: Optional[Annotated["Sample", strawberry.lazy("api.types.sample")]] = load_sample_rows  # type:ignore
    protocol: SequencingProtocol
    r1_file_id: Optional[strawberry.ID]
    r1_file: Optional[Annotated["File", strawberry.lazy("api.files")]] = load_files_from("r1_file")  # type: ignore
    r2_file_id: Optional[strawberry.ID]
    r2_file: Optional[Annotated["File", strawberry.lazy("api.files")]] = load_files_from("r2_file")  # type: ignore
    technology: SequencingTechnology
    nucleic_acid: NucleicAcid
    has_ercc: bool
    taxon: Optional[Annotated["Taxon", strawberry.lazy("api.types.taxon")]] = load_taxon_rows  # type:ignore
    primer_file: Optional[
        Annotated["GenomicRange", strawberry.lazy("api.types.genomic_range")]
    ] = load_genomic_range_rows  # type:ignore
    consensus_genomes: Sequence[
        Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]
    ] = load_consensus_genome_rows  # type:ignore
    contigs: Sequence[Annotated["Contig", strawberry.lazy("api.types.contig")]] = load_contig_rows  # type:ignore


"""
We need to add this to each Queryable type so that strawberry will accept either our
Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
"""
SequencingRead.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.SequencingRead or type(obj) == SequencingRead
)

"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class SequencingReadCreateInput:
    collection_id: int
    sample_id: Optional[strawberry.ID] = None
    protocol: SequencingProtocol
    r1_file_id: Optional[strawberry.ID] = None
    r2_file_id: Optional[strawberry.ID] = None
    technology: SequencingTechnology
    nucleic_acid: NucleicAcid
    has_ercc: bool
    taxon_id: Optional[strawberry.ID] = None
    primer_file_id: Optional[strawberry.ID] = None


@strawberry.input()
class SequencingReadUpdateInput:
    collection_id: Optional[int] = None
    sample_id: Optional[strawberry.ID] = None
    protocol: Optional[SequencingProtocol] = None
    r1_file_id: Optional[strawberry.ID] = None
    r2_file_id: Optional[strawberry.ID] = None
    technology: Optional[SequencingTechnology] = None
    nucleic_acid: Optional[NucleicAcid] = None
    has_ercc: Optional[bool] = None
    taxon_id: Optional[strawberry.ID] = None
    primer_file_id: Optional[strawberry.ID] = None


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_sequencing_reads(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[SequencingReadWhereClause] = None,
) -> typing.Sequence[SequencingRead]:
    """
    Resolve SequencingRead objects. Used for queries (see api/queries.py).
    """
    return await get_db_rows(db.SequencingRead, session, cerbos_client, principal, where, [])  # type: ignore


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_sequencing_read(
    input: SequencingReadCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> db.Entity:
    """
    Create a new SequencingRead object. Used for mutations (see api/mutations.py).
    """
    params = input.__dict__

    # Validate that user can create entity in this collection
    attr = {"collection_id": input.collection_id}
    resource = Resource(id="NEW_ID", kind=db.SequencingRead.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise Exception("Unauthorized: Cannot create entity in this collection")

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.SequencingRead(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_sequencing_read(
    input: SequencingReadUpdateInput,
    where: SequencingReadWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Update SequencingRead objects. Used for mutations (see api/mutations.py).
    """
    params = input.__dict__

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise Exception("No fields to update")

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(db.SequencingRead, session, cerbos_client, principal, where, [], CerbosAction.UPDATE)
    if len(entities) == 0:
        raise Exception("Unauthorized: Cannot update entities")

    # Validate that the user has access to the new collection ID
    if input.collection_id:
        attr = {"collection_id": input.collection_id}
        resource = Resource(id="SOME_ID", kind=db.SequencingRead.__tablename__, attr=attr)
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
async def delete_sequencing_read(
    where: SequencingReadWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Delete SequencingRead objects. Used for mutations (see api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(db.SequencingRead, session, cerbos_client, principal, where, [], CerbosAction.DELETE)
    if len(entities) == 0:
        raise Exception("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
