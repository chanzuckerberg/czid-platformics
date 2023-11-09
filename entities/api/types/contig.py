# Auto-generated by running 'make codegen'. Do not edit.
# Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.

# ruff: noqa: E501 Line too long

import typing
from typing import TYPE_CHECKING, Annotated, Optional

import database.models as db
import strawberry
from api.core.helpers import get_db_rows
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
from strawberry.types import Info
from typing_extensions import TypedDict

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.sequencing_read import SequencingReadWhereClause, SequencingRead

    pass
else:
    SequencingReadWhereClause = "SequencingReadWhereClause"
    SequencingRead = "SequencingRead"
    pass


# ------------------------------------------------------------------------------
# Dataloaders
# ------------------------------------------------------------------------------
@strawberry.field
async def load_sequencing_read_rows(
    root: "Contig",
    info: Info,
    where: Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")] | None = None,
) -> Optional[Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Contig)
    relationship = mapper.relationships["sequencing_read"]
    return await dataloader.loader_for(relationship, where).load(root.sequencing_read_id)  # type:ignore


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
    sequencing_read: Optional[
        Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")]
    ] | None
    sequence: Optional[StrComparators] | None
    entity_id: Optional[UUIDComparators] | None


# Define Contig type
@strawberry.type
class Contig(EntityInterface):
    id: strawberry.ID
    sequencing_read: Optional[
        Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]
    ] = load_sequencing_read_rows  # type:ignore
    sequence: str
    entity_id: strawberry.ID


# We need to add this to each Queryable type so that strawberry will accept either our
# Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
Contig.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.Contig or type(obj) == Contig
)


# ------------------------------------------------------------------------------
# Mutation types
# ------------------------------------------------------------------------------


@strawberry.input()
class ContigCreateInput:
    sequencing_read_id: strawberry.ID
    sequence: str


@strawberry.input()
class ContigUpdateInput:
    sequencing_read_id: Optional[strawberry.ID]
    sequence: Optional[str]


# ------------------------------------------------------------------------------
# Utilities
# ------------------------------------------------------------------------------


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_contig(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[ContigWhereClause] = None,
) -> typing.Sequence[Contig]:
    return await get_db_rows(db.Contig, session, cerbos_client, principal, where, [])  # type: ignore
