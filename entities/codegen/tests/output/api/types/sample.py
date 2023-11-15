# Auto-generated by running 'make codegen'. Do not edit.
# Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.

# ruff: noqa: E501 Line too long

import typing
from typing import TYPE_CHECKING, Annotated, Optional, Sequence

import database.models as db
import strawberry
import datetime
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
    BoolComparators,
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
    from api.types.sequencing_read import SequencingReadWhereClause, SequencingRead

    pass
else:
    SequencingReadWhereClause = "SequencingReadWhereClause"
    SequencingRead = "SequencingRead"
    pass


# ------------------------------------------------------------------------------
# Dataloaders
# ------------------------------------------------------------------------------
@relay.connection(
    relay.ListConnection[Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]]  # type:ignore
)
async def load_sequencing_read_rows(
    root: "Sample",
    info: Info,
    where: Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")] | None = None,
) -> Sequence[Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Sample)
    relationship = mapper.relationships["sequencing_reads"]
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
    sequencing_reads: Optional[
        Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")]
    ] | None
    entity_id: Optional[UUIDComparators] | None


# Define Sample type
@strawberry.type
class Sample(EntityInterface):
    id: strawberry.ID
    producing_run_id: Optional[int]
    owner_user_id: int
    collection_id: int
    name: str
    sample_type: str
    water_control: bool
    collection_date: Optional[datetime.datetime] = None
    collection_location: str
    description: Optional[str] = None
    sequencing_reads: Sequence[
        Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]
    ] = load_sequencing_read_rows  # type:ignore
    entity_id: strawberry.ID


# We need to add this to each Queryable type so that strawberry will accept either our
# Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
Sample.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.Sample or type(obj) == Sample
)


# ------------------------------------------------------------------------------
# Mutation types
# ------------------------------------------------------------------------------


@strawberry.input()
class SampleCreateInput:
    collection_id: int
    name: str
    sample_type: str
    water_control: bool
    collection_date: Optional[datetime.datetime] = None
    collection_location: str
    description: Optional[str] = None


@strawberry.input()
class SampleUpdateInput:
    collection_id: Optional[int] = None
    name: Optional[str] = None
    sample_type: Optional[str] = None
    water_control: Optional[bool] = None
    collection_date: Optional[datetime.datetime] = None
    collection_location: Optional[str] = None
    description: Optional[str] = None


# ------------------------------------------------------------------------------
# Utilities
# ------------------------------------------------------------------------------


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_samples(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[SampleWhereClause] = None,
) -> typing.Sequence[Sample]:
    return await get_db_rows(db.Sample, session, cerbos_client, principal, where, [])  # type: ignore


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_sample(
    input: SampleCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> db.Entity:
    params = input.__dict__

    # Validate that user can create entity in this collection
    attr = {"collection_id": input.collection_id}
    resource = Resource(id="NEW_ID", kind=db.Sample.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise Exception("Unauthorized: Cannot create entity in this collection")

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.Sample(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_sample(
    input: SampleUpdateInput,
    where: SampleWhereClause,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    params = input.__dict__

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise Exception("No fields to update")

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(db.Sample, session, cerbos_client, principal, where, [], CerbosAction.UPDATE)
    if len(entities) == 0:
        raise Exception("Unauthorized: Cannot update entities")

    # Validate that the user has access to the new collection ID
    if input.collection_id:
        attr = {"collection_id": input.collection_id}
        resource = Resource(id="SOME_ID", kind=db.Sample.__tablename__, attr=attr)
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
async def delete_sample(
    where: SampleWhereClause,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(db.Sample, session, cerbos_client, principal, where, [], CerbosAction.DELETE)
    if len(entities) == 0:
        raise Exception("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
