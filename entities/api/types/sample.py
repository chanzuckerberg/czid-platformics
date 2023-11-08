# Auto-generated by running 'make codegen'. Do not edit.
# Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.

import typing
from typing import TYPE_CHECKING, Annotated, Optional

import database.models as db
import strawberry
import datetime
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
    BoolComparators,
)
from platformics.api.core.strawberry_extensions import DependencyExtension
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.types import Info
from typing_extensions import TypedDict

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.taxon import TaxonWhereClause, Taxon
    from api.types.sequencing_read import SequencingReadWhereClause, SequencingRead
    from api.types.metadatum import MetadatumWhereClause, Metadatum

    pass
else:
    TaxonWhereClause = "TaxonWhereClause"
    Taxon = "Taxon"
    SequencingReadWhereClause = "SequencingReadWhereClause"
    SequencingRead = "SequencingRead"
    MetadatumWhereClause = "MetadatumWhereClause"
    Metadatum = "Metadatum"
    pass


# ------------------------------------------------------------------------------
# Dataloaders
# ------------------------------------------------------------------------------


@strawberry.field(extensions=[DependencyExtension()])
async def load_taxon_rows(
    root: "Sample",
    info: Info,
    where: Annotated["TaxonWhereClause", strawberry.lazy("api.types.taxon")] | None = None,
) -> Optional[Annotated["Taxon", strawberry.lazy("api.types.taxon")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Sample)
    relationship = mapper.relationships["taxon"]
    return await dataloader.loader_for(relationship, where).load(root.taxon_id)  # type:ignore


@strawberry.field(extensions=[DependencyExtension()])
async def load_sequencing_read_rows(
    root: "Sample",
    info: Info,
    where: Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")] | None = None,
) -> typing.Sequence[Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Sample)
    relationship = mapper.relationships["sequencing_read"]
    return await dataloader.loader_for(relationship, where).load(root.id)  # type:ignore


@strawberry.field(extensions=[DependencyExtension()])
async def load_metadatum_rows(
    root: "Sample",
    info: Info,
    where: Annotated["MetadatumWhereClause", strawberry.lazy("api.types.metadatum")] | None = None,
) -> typing.Sequence[Annotated["Metadatum", strawberry.lazy("api.types.metadatum")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Sample)
    relationship = mapper.relationships["metadatum"]
    return await dataloader.loader_for(relationship, where).load(root.id)  # type:ignore


# ------------------------------------------------------------------------------
# Define Strawberry GQL types
# ------------------------------------------------------------------------------


# Supported WHERE clause attributes
@strawberry.input
class SampleWhereClause(TypedDict):
    id: UUIDComparators | None
    producing_run_id: IntComparators | None
    owner_user_id: IntComparators | None
    collection_id: IntComparators | None
    name: Optional[StrComparators] | None
    sample_type: Optional[StrComparators] | None
    water_control: Optional[BoolComparators] | None
    # TODO: Add proper datetime comparator
    collection_date: Optional[StrComparators] | None
    collection_location: Optional[StrComparators] | None
    description: Optional[StrComparators] | None
    host_taxon: Optional[Annotated["TaxonWhereClause", strawberry.lazy("api.types.taxon")]] | None
    sequencing_reads: Optional[
        Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")]
    ] | None
    metadatas: Optional[Annotated["MetadatumWhereClause", strawberry.lazy("api.types.metadatum")]] | None
    entity_id: Optional[UUIDComparators] | None


# Define Sample type
@strawberry.type
class Sample(EntityInterface):
    id: strawberry.ID
    producing_run_id: int
    owner_user_id: int
    collection_id: int
    name: str
    sample_type: str
    water_control: bool
    collection_date: datetime.datetime
    collection_location: str
    description: str
    host_taxon: Optional[Annotated["Taxon", strawberry.lazy("api.types.taxon")]] = load_taxon_rows
    sequencing_reads: typing.Sequence[
        Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]
    ] = load_sequencing_read_rows
    metadatas: typing.Sequence[Annotated["Metadatum", strawberry.lazy("api.types.metadatum")]] = load_metadatum_rows
    entity_id: strawberry.ID


# We need to add this to each Queryable type so that strawberry will accept either our
# Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
Sample.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.Sample or type(obj) == Sample
)


# Resolvers used in api/queries
@strawberry.field(extensions=[DependencyExtension()])
async def resolve_sample(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[SampleWhereClause] = None,
) -> typing.Sequence[Sample]:
    return await get_db_rows(db.Sample, session, cerbos_client, principal, where, [])  # type: ignore
