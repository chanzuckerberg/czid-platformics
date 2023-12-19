"""
GraphQL type for GenomicRange

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
    IntComparators,
    UUIDComparators,
)
from platformics.api.core.strawberry_extensions import DependencyExtension
from platformics.security.authorization import CerbosAction
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import relay
from strawberry.types import Info
from typing_extensions import TypedDict

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.reference_genome import ReferenceGenomeWhereClause, ReferenceGenome
    from api.types.sequencing_read import SequencingReadWhereClause, SequencingRead

    pass
else:
    ReferenceGenomeWhereClause = "ReferenceGenomeWhereClause"
    ReferenceGenome = "ReferenceGenome"
    SequencingReadWhereClause = "SequencingReadWhereClause"
    SequencingRead = "SequencingRead"
    pass


"""
------------------------------------------------------------------------------
Dataloaders
------------------------------------------------------------------------------
These are batching functions for loading related objects to avoid N+1 queries.
"""


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
    relay.ListConnection[Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]]  # type:ignore
)
async def load_sequencing_read_rows(
    root: "GenomicRange",
    info: Info,
    where: Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")] | None = None,
) -> Sequence[Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.GenomicRange)
    relationship = mapper.relationships["sequencing_reads"]
    return await dataloader.loader_for(relationship, where).load(root.id)  # type:ignore


"""
------------------------------------------------------------------------------
Dataloader for File object
------------------------------------------------------------------------------
"""


def load_files_from(attr_name: str) -> Callable:
    @strawberry.field
    async def load_files(
        root: "GenomicRange",
        info: Info,
        where: Annotated["FileWhereClause", strawberry.lazy("api.files")] | None = None,
    ) -> Optional[Annotated["File", strawberry.lazy("api.files")]]:
        """
        Given a list of GenomicRange IDs for a certain file type, return related Files
        """
        dataloader = info.context["sqlalchemy_loader"]
        mapper = inspect(db.GenomicRange)
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
class GenomicRangeWhereClauseMutations(TypedDict):
    id: UUIDComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class GenomicRangeWhereClause(TypedDict):
    id: UUIDComparators | None
    producing_run_id: IntComparators | None
    owner_user_id: IntComparators | None
    collection_id: IntComparators | None
    reference_genome: Optional[
        Annotated["ReferenceGenomeWhereClause", strawberry.lazy("api.types.reference_genome")]
    ] | None
    sequencing_reads: Optional[
        Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")]
    ] | None


"""
Define GenomicRange type
"""


@strawberry.type
class GenomicRange(EntityInterface):
    id: strawberry.ID
    producing_run_id: Optional[int]
    owner_user_id: int
    collection_id: int
    reference_genome: Optional[
        Annotated["ReferenceGenome", strawberry.lazy("api.types.reference_genome")]
    ] = load_reference_genome_rows  # type:ignore
    file_id: Optional[strawberry.ID]
    file: Optional[Annotated["File", strawberry.lazy("api.files")]] = load_files_from("file")  # type: ignore
    sequencing_reads: Sequence[
        Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]
    ] = load_sequencing_read_rows  # type:ignore


"""
We need to add this to each Queryable type so that strawberry will accept either our
Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
"""
GenomicRange.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.GenomicRange or type(obj) == GenomicRange
)

"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class GenomicRangeCreateInput:
    collection_id: int
    reference_genome_id: strawberry.ID
    file_id: Optional[strawberry.ID] = None


@strawberry.input()
class GenomicRangeUpdateInput:
    collection_id: Optional[int] = None
    reference_genome_id: Optional[strawberry.ID] = None
    file_id: Optional[strawberry.ID] = None


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_genomic_ranges(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[GenomicRangeWhereClause] = None,
) -> typing.Sequence[GenomicRange]:
    """
    Resolve GenomicRange objects. Used for queries (see api/queries.py).
    """
    return await get_db_rows(db.GenomicRange, session, cerbos_client, principal, where, [])  # type: ignore


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_genomic_range(
    input: GenomicRangeCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> db.Entity:
    """
    Create a new GenomicRange object. Used for mutations (see api/mutations.py).
    """
    params = input.__dict__

    # Validate that user can create entity in this collection
    attr = {"collection_id": input.collection_id}
    resource = Resource(id="NEW_ID", kind=db.GenomicRange.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise Exception("Unauthorized: Cannot create entity in this collection")

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.GenomicRange(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_genomic_range(
    input: GenomicRangeUpdateInput,
    where: GenomicRangeWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Update GenomicRange objects. Used for mutations (see api/mutations.py).
    """
    params = input.__dict__

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise Exception("No fields to update")

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(db.GenomicRange, session, cerbos_client, principal, where, [], CerbosAction.UPDATE)
    if len(entities) == 0:
        raise Exception("Unauthorized: Cannot update entities")

    # Validate that the user has access to the new collection ID
    if input.collection_id:
        attr = {"collection_id": input.collection_id}
        resource = Resource(id="SOME_ID", kind=db.GenomicRange.__tablename__, attr=attr)
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
async def delete_genomic_range(
    where: GenomicRangeWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Delete GenomicRange objects. Used for mutations (see api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(db.GenomicRange, session, cerbos_client, principal, where, [], CerbosAction.DELETE)
    if len(entities) == 0:
        raise Exception("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
