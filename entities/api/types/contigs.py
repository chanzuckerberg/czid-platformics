# Auto-generated by running 'make codegen'. Do not edit.
# Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.

import uuid
import typing
from typing import Optional

import database.models as db
import strawberry
from api.types.entities import EntityInterface
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal
from fastapi import Depends
from platformics.api.core.deps import get_cerbos_client, get_db_session, require_auth_principal
from platformics.api.core.gql_to_sql import IntComparators, StrComparators, UUIDComparators
from platformics.security.authorization import CerbosAction, get_resource_query
from platformics.api.core.strawberry_extensions import DependencyExtension
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.dataloader import DataLoader
from typing_extensions import TypedDict
from api.core.helpers import get_db_rows
from typing import TYPE_CHECKING, Annotated
from api.files import File

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.sequencing_reads import SequencingReadWhereClause, SequencingRead
else:
    SequencingReadWhereClause = "SequencingReadWhereClause"
    SequencingRead = "SequencingRead"

# ------------------------------------------------------------------------------
# Dataloaders
# ------------------------------------------------------------------------------


def cache_key(key: dict) -> str:
    return key["id"]


# Given a list of Contig ids, return a list of lists, where the inner lists correspond to the
# sequencing_read associated with each Contig id.
async def batch_sequencing_read(
    keys: list[dict],
) -> Optional[Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]]:
    session = keys[0]["session"]
    cerbos_client = keys[0]["cerbos_client"]
    principal = keys[0]["principal"]
    ids = [key["id"] for key in keys]

    query = get_resource_query(principal, cerbos_client, CerbosAction.VIEW, db.SequencingRead)
    # The relationship is many-to-one
    # Get all sequencing_reads that are associated with at least one of the Contig ids
    query = query.filter(db.SequencingRead.contigs.any(db.Contig.id.in_(ids)))

    all_sequencing_reads = await session.execute(query)
    all_sequencing_reads = all_sequencing_reads.scalars().all()

    # Order the results by Contig ids
    result = []
    for id in ids:
        for sequencing_read in all_sequencing_reads:
            if id in [contig.id for contig in await sequencing_read.awaitable_attrs.contigs]:
                result.append(sequencing_read)
    return result


sequencing_read_loader = DataLoader(load_fn=batch_sequencing_read, cache_key_fn=cache_key)


@strawberry.field(extensions=[DependencyExtension()])
async def load_sequencing_reads(
    root: "Contig",
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> typing.Sequence[Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]]:
    return await sequencing_read_loader.load(
        {"session": session, "cerbos_client": cerbos_client, "principal": principal, "id": root.id}
    )


# ------------------------------------------------------------------------------
# Dataloader for File object
# ------------------------------------------------------------------------------


# Given a list of Contig IDs for a certain file type, return related Files
def load_files_from(attr_name):
    async def batch_files(keys: list[dict]) -> Annotated["File", strawberry.lazy("api.files")]:
        session = keys[0]["session"]
        cerbos_client = keys[0]["cerbos_client"]
        principal = keys[0]["principal"]
        entity_ids = [key["id"] for key in keys]

        # Retrieve files
        query = get_resource_query(principal, cerbos_client, CerbosAction.VIEW, db.File)
        query = query.filter(db.File.entity_id.in_(entity_ids), db.File.entity_field_name == attr_name)
        all_files = (await session.execute(query)).scalars().all()

        # Order files so they are in the same order as `entity_ids`
        result = []
        for entity_id in entity_ids:
            matching = [f for f in all_files if f.entity_id == entity_id]
            assert len(matching) == 1
            result.append(matching[0])
        return result

    file_loader = DataLoader(load_fn=batch_files, cache_key_fn=cache_key)

    @strawberry.field(extensions=[DependencyExtension()])
    async def load_files(
        root: "Contig",
        session: AsyncSession = Depends(get_db_session, use_cache=False),
        cerbos_client: CerbosClient = Depends(get_cerbos_client),
        principal: Principal = Depends(require_auth_principal),
    ) -> Annotated["Contig", strawberry.lazy("api.files")]:
        return await file_loader.load(
            {"session": session, "cerbos_client": cerbos_client, "principal": principal, "id": root.id}
        )

    return load_files


# ------------------------------------------------------------------------------
# Define Strawberry GQL types
# ------------------------------------------------------------------------------


# Supported WHERE clause attributes
@strawberry.input
class ContigWhereClause(TypedDict):
    id: UUIDComparators | None
    producing_run_id: IntComparators | None
    owner_user_id: IntComparators | None
    collection_id: IntComparators | None
    sequencing_read: Optional[Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_reads")]]
    sequence: Optional[StrComparators] | None
    entity_id: Optional[UUIDComparators] | None


# Define Contig type
@strawberry.type
class Contig(EntityInterface):
    id: uuid.UUID
    producing_run_id: int
    owner_user_id: int
    collection_id: int
    sequencing_read: Optional[
        Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_reads")]
    ] = load_sequencing_reads
    sequence: str
    entity_id: uuid.UUID


# We need to add this to each Queryable type so that strawberry will accept either our
# Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
Contig.__strawberry_definition__.is_type_of = lambda obj, info: type(obj) == db.Contig or type(obj) == Contig


# Resolvers used in api/queries
@strawberry.field(extensions=[DependencyExtension()])
async def resolve_contigs(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[ContigWhereClause] = None,
) -> typing.Sequence[Contig]:
    return await get_db_rows(db.Contig, session, cerbos_client, principal, where, [])  # type: ignore
