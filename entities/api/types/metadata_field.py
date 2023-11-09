# Auto-generated by running 'make codegen'. Do not edit.
# Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.

# ruff: noqa: E501 Line too long

import typing
from typing import TYPE_CHECKING, Annotated, Optional, Sequence

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
    BoolComparators,
)
from platformics.api.core.strawberry_extensions import DependencyExtension
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import relay
from strawberry.types import Info
from typing_extensions import TypedDict

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.metadata_field_project import MetadataFieldProjectWhereClause, MetadataFieldProject
    from api.types.metadatum import MetadatumWhereClause, Metadatum

    pass
else:
    MetadataFieldProjectWhereClause = "MetadataFieldProjectWhereClause"
    MetadataFieldProject = "MetadataFieldProject"
    MetadatumWhereClause = "MetadatumWhereClause"
    Metadatum = "Metadatum"
    pass


# ------------------------------------------------------------------------------
# Dataloaders
# ------------------------------------------------------------------------------
@relay.connection(
    relay.ListConnection[
        Annotated["MetadataFieldProject", strawberry.lazy("api.types.metadata_field_project")]
    ]  # type:ignore
)
async def load_metadata_field_project_rows(
    root: "MetadataField",
    info: Info,
    where: Annotated["MetadataFieldProjectWhereClause", strawberry.lazy("api.types.metadata_field_project")]
    | None = None,
) -> Sequence[Annotated["MetadataFieldProject", strawberry.lazy("api.types.metadata_field_project")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.MetadataField)
    relationship = mapper.relationships["metadata_field_project"]
    return await dataloader.loader_for(relationship, where).load(root.id)  # type:ignore


@relay.connection(
    relay.ListConnection[Annotated["Metadatum", strawberry.lazy("api.types.metadatum")]]  # type:ignore
)
async def load_metadatum_rows(
    root: "MetadataField",
    info: Info,
    where: Annotated["MetadatumWhereClause", strawberry.lazy("api.types.metadatum")] | None = None,
) -> Sequence[Annotated["Metadatum", strawberry.lazy("api.types.metadatum")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.MetadataField)
    relationship = mapper.relationships["metadatum"]
    return await dataloader.loader_for(relationship, where).load(root.id)  # type:ignore


# ------------------------------------------------------------------------------
# Define Strawberry GQL types
# ------------------------------------------------------------------------------


# Supported WHERE clause attributes
@strawberry.input
class MetadataFieldWhereClause(TypedDict):
    id: UUIDComparators | None
    producing_run_id: IntComparators | None
    owner_user_id: IntComparators | None
    collection_id: IntComparators | None
    field_group: Optional[
        Annotated["MetadataFieldProjectWhereClause", strawberry.lazy("api.types.metadata_field_project")]
    ] | None
    field_name: Optional[StrComparators] | None
    description: Optional[StrComparators] | None
    field_type: Optional[StrComparators] | None
    is_required: Optional[BoolComparators] | None
    options: Optional[StrComparators] | None
    default_value: Optional[StrComparators] | None
    metadatas: Optional[Annotated["MetadatumWhereClause", strawberry.lazy("api.types.metadatum")]] | None
    entity_id: Optional[UUIDComparators] | None


# Define MetadataField type
@strawberry.type
class MetadataField(EntityInterface):
    id: strawberry.ID
    producing_run_id: int
    owner_user_id: int
    collection_id: int
    field_group: typing.Sequence[
        Annotated["MetadataFieldProject", strawberry.lazy("api.types.metadata_field_project")]
    ] = load_metadata_field_project_rows
    field_name: str
    description: str
    field_type: str
    is_required: bool
    options: str
    default_value: str
    metadatas: typing.Sequence[Annotated["Metadatum", strawberry.lazy("api.types.metadatum")]] = load_metadatum_rows
    entity_id: strawberry.ID


# We need to add this to each Queryable type so that strawberry will accept either our
# Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
MetadataField.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.MetadataField or type(obj) == MetadataField
)


# Resolvers used in api/queries
@strawberry.field(extensions=[DependencyExtension()])
async def resolve_metadata_field(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[MetadataFieldWhereClause] = None,
) -> typing.Sequence[MetadataField]:
    return await get_db_rows(db.MetadataField, session, cerbos_client, principal, where, [])  # type: ignore
