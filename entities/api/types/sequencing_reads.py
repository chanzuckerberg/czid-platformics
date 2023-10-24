import typing
import uuid
from typing import TYPE_CHECKING, Annotated

import database.models as db
import strawberry
from api.core.helpers import get_db_rows
from api.types.dataloaders import load_samples
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
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import TypedDict

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.samples import Sample, SampleWhereClause
else:
    SampleWhereClause = "SampleWhereClause"
    Sample = "Sample"


@strawberry.input
class SequencingReadWhereClause(TypedDict):
    id: UUIDComparators | None
    producing_runid: IntComparators | None
    owner_user_id: IntComparators | None
    collection_id: IntComparators | None
    sequence: typing.Optional[StrComparators]
    sample: typing.Optional[Annotated["SampleWhereClause", strawberry.lazy("api.types.samples")]]


@strawberry.type
class SequencingRead(EntityInterface):
    id: uuid.UUID
    producing_runid: int
    owner_user_id: int
    collection_id: int
    sequence: str
    sample: Annotated["Sample", strawberry.lazy("api.types.samples")] = load_samples


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
    where: SequencingReadWhereClause = {},
) -> typing.Sequence[SequencingRead]:
    return await get_db_rows(db.SequencingRead, session, cerbos_client, principal, where, [])  # type: ignore
