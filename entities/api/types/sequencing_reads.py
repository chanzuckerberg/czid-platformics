# Auto-generated by running 'make codegen'. Do not edit.
# Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.

import uuid
import typing
from typing import Any, Mapping, Optional, Tuple

import database.models as db
import strawberry
from api.types.entities import EntityInterface
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal
from fastapi import Depends
from platformics.api.core.deps import get_cerbos_client, get_db_session, require_auth_principal
from platformics.api.core.gql_to_sql import EnumComparators, IntComparators, StrComparators, UUIDComparators
from platformics.security.authorization import CerbosAction, get_resource_query
from platformics.api.core.strawberry_extensions import DependencyExtension
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from strawberry.dataloader import DataLoader
from typing_extensions import TypedDict
from api.core.helpers import get_db_rows
from typing import TYPE_CHECKING, Annotated

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.samples import SampleWhereClause, Sample
    from api.types.contigs import ContigWhereClause, Contig
else:
    SampleWhereClause = "SampleWhereClause"
    Sample = "Sample"
    ContigWhereClause = "ContigWhereClause"
    Contig = "Contig"

def cache_key(key: dict) -> str:
    return key["id"]

# Define dataloaders for nested where clauses
async def batch_sample(
    keys: list[dict],
) -> Annotated["Sample", strawberry.lazy("api.types.sample")]:
    session = keys[0]["session"]
    cerbos_client = keys[0]["cerbos_client"]
    principal = keys[0]["principal"]
    ids = [key["id"] for key in keys]

    query = get_resource_query(principal, cerbos_client, CerbosAction.VIEW, db.Sample)
    query = query.filter(db.Sample.sequencing_reads.any(db.SequencingRead.id.in_(ids)))
    result = await session.execute(query)
    return result.scalars().all()


sample_loader = DataLoader(load_fn=batch_sample, cache_key_fn=cache_key)


@strawberry.field(extensions=[DependencyExtension()])
async def load_samples(
    root: "SequencingRead",
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Annotated["SequencingRead", strawberry.lazy("api.types.sample")]:
    return await sample_loader.load(
        {"session": session, "cerbos_client": cerbos_client, "principal": principal, "id": root.id}
    )
async def batch_contigs(
    keys: list[dict],
) -> Annotated["Contig", strawberry.lazy("api.types.contigs")]:
    session = keys[0]["session"]
    cerbos_client = keys[0]["cerbos_client"]
    principal = keys[0]["principal"]
    ids = [key["id"] for key in keys]

    query = get_resource_query(principal, cerbos_client, CerbosAction.VIEW, db.Contig)
    query = query.filter(db.Contig.sequencing_read_id.in_(ids))
    result = await session.execute(query)
    return result.scalars().all()


contigs_loader = DataLoader(load_fn=batch_contigs, cache_key_fn=cache_key)


@strawberry.field(extensions=[DependencyExtension()])
async def load_contigs(
    root: "SequencingRead",
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Annotated["SequencingRead", strawberry.lazy("api.types.contigs")]:
    return await contigs_loader.load(
        {"session": session, "cerbos_client": cerbos_client, "principal": principal, "id": root.id}
    )

@strawberry.input
class SequencingReadWhereClause(TypedDict):
    id: UUIDComparators | None
    producing_run_id: IntComparators | None
    owner_user_id: IntComparators | None
    collection_id: IntComparators | None
        # TODO: need to fix enums, pass in the type of the enum
    # nucleotide: Optional[EnumComparators] | None
    sequence: Optional[StrComparators] | None
        # TODO: need to fix enums, pass in the type of the enum
    # protocol: Optional[EnumComparators] | None
    sample: Optional[Annotated["SampleWhereClause", strawberry.lazy("api.types.samples")]]
    contigs: Optional[Annotated["ContigWhereClause", strawberry.lazy("api.types.contigs")]]
    # entity_id: Optional[UUIDComparators] | None

@strawberry.type
class SequencingRead(EntityInterface):
    id: uuid.UUID
    producing_run_id: int
    owner_user_id: int
    collection_id: int
    nucleotide: str
    sequence: str
    protocol: str
    # TODO:
    # sequence_file_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("file.id"), nullable=True)
    # sequence_file: Annotated["File", strawberry.lazy("api.types.sequence_files")] = load_files
    sample: Annotated["Sample", strawberry.lazy("api.types.samples")] = load_samples
    contigs: Annotated["Contig", strawberry.lazy("api.types.contigs")] = load_contigs
    # entity_id: uuid.UUID

# We need to add this to each Queryable type so that strawberry will accept either our
# Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
SequencingRead.__strawberry_definition__.is_type_of = (
    lambda obj, info: type(obj) == db.SequencingRead or type(obj) == SequencingRead
)

@strawberry.field(extensions=[DependencyExtension()])
async def resolve_sequencing_reads(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[SequencingReadWhereClause] = None,
) -> typing.Sequence[SequencingRead]:
    return await get_db_rows(db.SequencingRead, session, cerbos_client, principal, where, [])  # type: ignore