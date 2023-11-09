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
from cerbos.sdk.model import Principal, Resource
from fastapi import Depends
from platformics.api.core.deps import get_cerbos_client, get_db_session, require_auth_principal
from platformics.api.core.gql_to_sql import (
    IntComparators,
    StrComparators,
    UUIDComparators,
)
from platformics.api.core.strawberry_extensions import DependencyExtension
from platformics.security.authorization import CerbosAction
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.types import Info
from typing_extensions import TypedDict

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.sample import SampleWhereClause, Sample
    from api.types.metadata_field import MetadataFieldWhereClause, MetadataField

    pass
else:
    SampleWhereClause = "SampleWhereClause"
    Sample = "Sample"
    MetadataFieldWhereClause = "MetadataFieldWhereClause"
    MetadataField = "MetadataField"
    pass


# ------------------------------------------------------------------------------
# Dataloaders
# ------------------------------------------------------------------------------
@strawberry.field
async def load_sample_rows(
    root: "Metadatum",
    info: Info,
    where: Annotated["SampleWhereClause", strawberry.lazy("api.types.sample")] | None = None,
) -> Optional[Annotated["Sample", strawberry.lazy("api.types.sample")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Metadatum)
    relationship = mapper.relationships["sample"]
    return await dataloader.loader_for(relationship, where).load(root.sample_id)  # type:ignore


@strawberry.field
async def load_metadata_field_rows(
    root: "Metadatum",
    info: Info,
    where: Annotated["MetadataFieldWhereClause", strawberry.lazy("api.types.metadata_field")] | None = None,
) -> Optional[Annotated["MetadataField", strawberry.lazy("api.types.metadata_field")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Metadatum)
    relationship = mapper.relationships["metadata_field"]
    return await dataloader.loader_for(relationship, where).load(root.metadata_field_id)  # type:ignore


# ------------------------------------------------------------------------------
# Define Strawberry GQL types
# ------------------------------------------------------------------------------


# Supported WHERE clause attributes
@strawberry.input
class MetadatumWhereClause(TypedDict):
    id: UUIDComparators | None
    producing_run_id: IntComparators | None
    owner_user_id: IntComparators | None
    collection_id: IntComparators | None
    sample: Optional[Annotated["SampleWhereClause", strawberry.lazy("api.types.sample")]] | None
    metadata_field: Optional[Annotated["MetadataFieldWhereClause", strawberry.lazy("api.types.metadata_field")]] | None
    value: Optional[StrComparators] | None
    entity_id: Optional[UUIDComparators] | None


# Define Metadatum type
@strawberry.type
class Metadatum(EntityInterface):
    id: strawberry.ID
    producing_run_id: Optional[int]
    owner_user_id: int
    collection_id: int
    sample: Optional[Annotated["Sample", strawberry.lazy("api.types.sample")]] = load_sample_rows  # type:ignore
    metadata_field: Optional[
        Annotated["MetadataField", strawberry.lazy("api.types.metadata_field")]
    ] = load_metadata_field_rows  # type:ignore
    value: str
    entity_id: strawberry.ID


# We need to add this to each Queryable type so that strawberry will accept either our
# Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
Metadatum.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.Metadatum or type(obj) == Metadatum
)


# ------------------------------------------------------------------------------
# Mutation types
# ------------------------------------------------------------------------------


@strawberry.input()
class MetadatumCreateInput:
    collection_id: int
    sample_id: strawberry.ID
    metadata_field_id: strawberry.ID
    value: str


@strawberry.input()
class MetadatumUpdateInput:
    collection_id: Optional[int] = None
    sample_id: Optional[strawberry.ID] = None
    metadata_field_id: Optional[strawberry.ID] = None
    value: Optional[str] = None


# ------------------------------------------------------------------------------
# Utilities
# ------------------------------------------------------------------------------


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_metadatum(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[MetadatumWhereClause] = None,
) -> typing.Sequence[Metadatum]:
    return await get_db_rows(db.Metadatum, session, cerbos_client, principal, where, [])  # type: ignore


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_metadatum(
    input: MetadatumCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Metadatum:
    params = input.__dict__

    # Validate that user can create entity in this collection
    attr = {"collection_id": input.collection_id}
    resource = Resource(id="NEW_ID", kind=db.Metadatum.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise Exception("Unauthorized: Cannot create entity in this collection")

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.Metadatum(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_metadatum(
    input: MetadatumUpdateInput,
    where: MetadatumWhereClause,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Metadatum:
    params = input.__dict__

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise Exception("No fields to update")

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(db.Metadatum, session, cerbos_client, principal, where, [], CerbosAction.UPDATE)
    if len(entities) == 0:
        raise Exception("Unauthorized: Cannot update entities")

    # Validate that the user has access to the new collection ID
    if input.collection_id:
        attr = {"collection_id": input.collection_id}
        resource = Resource(id="SOME_ID", kind=db.Metadatum.__tablename__, attr=attr)
        if not cerbos_client.is_allowed(CerbosAction.UPDATE, principal, resource):
            raise Exception("Unauthorized: Cannot access new collection")

    # Update DB
    for entity in entities:
        for key in params:
            if params[key]:
                setattr(entity, key, params[key])
    await session.commit()
    return entities
