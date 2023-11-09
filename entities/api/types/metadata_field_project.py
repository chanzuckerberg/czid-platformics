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
    from api.types.metadata_field import MetadataFieldWhereClause, MetadataField

    pass
else:
    MetadataFieldWhereClause = "MetadataFieldWhereClause"
    MetadataField = "MetadataField"
    pass


# ------------------------------------------------------------------------------
# Dataloaders
# ------------------------------------------------------------------------------
@strawberry.field
async def load_metadata_field_rows(
    root: "MetadataFieldProject",
    info: Info,
    where: Annotated["MetadataFieldWhereClause", strawberry.lazy("api.types.metadata_field")] | None = None,
) -> Optional[Annotated["MetadataField", strawberry.lazy("api.types.metadata_field")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.MetadataFieldProject)
    relationship = mapper.relationships["metadata_field"]
    return await dataloader.loader_for(relationship, where).load(root.metadata_field_id)  # type:ignore


# ------------------------------------------------------------------------------
# Define Strawberry GQL types
# ------------------------------------------------------------------------------


# Supported WHERE clause attributes
@strawberry.input
class MetadataFieldProjectWhereClause(TypedDict):
    id: UUIDComparators | None
    producing_run_id: IntComparators | None
    owner_user_id: IntComparators | None
    collection_id: IntComparators | None
    project_id: Optional[IntComparators] | None
    metadata_field: Optional[Annotated["MetadataFieldWhereClause", strawberry.lazy("api.types.metadata_field")]] | None
    entity_id: Optional[UUIDComparators] | None


# Define MetadataFieldProject type
@strawberry.type
class MetadataFieldProject(EntityInterface):
    id: strawberry.ID
    project_id: int
    metadata_field: Optional[
        Annotated["MetadataField", strawberry.lazy("api.types.metadata_field")]
    ] = load_metadata_field_rows  # type:ignore
    entity_id: strawberry.ID


# We need to add this to each Queryable type so that strawberry will accept either our
# Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
MetadataFieldProject.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.MetadataFieldProject or type(obj) == MetadataFieldProject
)


# ------------------------------------------------------------------------------
# Mutation types
# ------------------------------------------------------------------------------


@strawberry.input()
class MetadataFieldProjectCreateInput:
    project_id: int
    metadata_field_id: strawberry.ID


@strawberry.input()
class MetadataFieldProjectUpdateInput:
    project_id: Optional[int]
    metadata_field_id: Optional[strawberry.ID]


# ------------------------------------------------------------------------------
# Utilities
# ------------------------------------------------------------------------------


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_metadata_field_project(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[MetadataFieldProjectWhereClause] = None,
) -> typing.Sequence[MetadataFieldProject]:
    return await get_db_rows(db.MetadataFieldProject, session, cerbos_client, principal, where, [])  # type: ignore
