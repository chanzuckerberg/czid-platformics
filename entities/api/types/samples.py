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
    from api.types.sequencing_reads import SequencingReadWhereClause, SequencingRead
else:
    SequencingReadWhereClause = "SequencingReadWhereClause"
    SequencingRead = "SequencingRead"

def cache_key(key: dict) -> str:
    return key["id"]

# Define dataloaders for nested where clauses
async def batch_sequencing_reads(
    keys: list[dict],
) -> Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_reads")]:
    session = keys[0]["session"]
    cerbos_client = keys[0]["cerbos_client"]
    principal = keys[0]["principal"]
    ids = [key["id"] for key in keys]

    query = get_resource_query(principal, cerbos_client, CerbosAction.VIEW, db.SequencingRead)
    query = query.filter(db.SequencingRead.sample_id.in_(ids))
    result = await session.execute(query)
    return result.scalars().all()


sequencing_reads_loader = DataLoader(load_fn=batch_sequencing_reads, cache_key_fn=cache_key)


@strawberry.field(extensions=[DependencyExtension()])
async def load_sequencing_reads(
    root: "Sample",
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_reads")]:
    return await sequencing_reads_loader.load(
        {"session": session, "cerbos_client": cerbos_client, "principal": principal, "id": root.id}
    )

@strawberry.input
class SampleWhereClause(TypedDict):
    id: UUIDComparators | None
    producing_run_id: IntComparators | None
    owner_user_id: IntComparators | None
    collection_id: IntComparators | None
    name: Optional[StrComparators] | None
    location: Optional[StrComparators] | None
    sequencing_reads: Optional[Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_reads")]]
    # entity_id: Optional[UUIDComparators] | None

@strawberry.type
class Sample(EntityInterface):
    id: uuid.UUID
    producing_run_id: int
    owner_user_id: int
    collection_id: int
    name: str
    location: str
    sequencing_reads: Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_reads")] = load_sequencing_reads
    # entity_id: uuid.UUID

# We need to add this to each Queryable type so that strawberry will accept either our
# Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
Sample.__strawberry_definition__.is_type_of = (
    lambda obj, info: type(obj) == db.Sample or type(obj) == Sample
)

@strawberry.field(extensions=[DependencyExtension()])
async def resolve_samples(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[SampleWhereClause] = None,
) -> typing.Sequence[Sample]:
    return await get_db_rows(db.Sample, session, cerbos_client, principal, where, [])  # type: ignore