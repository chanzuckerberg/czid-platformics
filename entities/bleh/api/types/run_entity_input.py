# Auto-generated by running 'make codegen'. Do not edit.
# Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.

# ruff: noqa: E501 Line too long

import typing
from typing import TYPE_CHECKING, Annotated, Optional, Sequence, Callable

import database.models as db
import strawberry
import datetime
from api.core.helpers import get_db_rows
from api.files import File, FileWhereClause
from api.types.entities import EntityInterface
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource
from fastapi import Depends
from platformics.api.core.deps import get_cerbos_client, get_db_session, require_auth_principal
from platformics.api.core.gql_to_sql import EnumComparators, IntComparators, StrComparators, UUIDComparators, BoolComparators
from platformics.api.core.strawberry_extensions import DependencyExtension
from platformics.security.authorization import CerbosAction, get_resource_query
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import relay
from strawberry.types import Info
from typing_extensions import TypedDict

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.run import (RunWhereClause, Run)
    pass
else:
    RunWhereClause = "RunWhereClause"
    Run = "Run"
    pass


# ------------------------------------------------------------------------------
# Dataloaders
# ------------------------------------------------------------------------------
@strawberry.field
async def load_run_rows(
    root: "RunEntityInput",
    info: Info,
    where: Annotated["RunWhereClause", strawberry.lazy("api.types.run")] | None = None,
) -> Optional[Annotated["Run", strawberry.lazy("api.types.run")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.RunEntityInput)
    relationship = mapper.relationships["run"]
    return await dataloader.loader_for(relationship, where).load(root.run_id) # type:ignore


# ------------------------------------------------------------------------------
# Define Strawberry GQL types
# ------------------------------------------------------------------------------


# Only let users specify IDs in WHERE clause when mutating data (for safety).
# We can extend that list as we gather more use cases from the FE team.
@strawberry.input
class RunEntityInputWhereClauseMutations(TypedDict):
    id: UUIDComparators | None


# Supported WHERE clause attributes
@strawberry.input
class RunEntityInputWhereClause(TypedDict):
    id: UUIDComparators | None
    producing_run_id: IntComparators | None
    owner_user_id: IntComparators | None
    collection_id: IntComparators | None
    new_entity_id: Optional[IntComparators] | None
    field_name: Optional[StrComparators] | None
    run: Optional[Annotated["RunWhereClause", strawberry.lazy("api.types.run")]] | None




# Define RunEntityInput type
@strawberry.type
class RunEntityInput(EntityInterface):
    id: strawberry.ID
    producing_run_id: Optional[int]
    owner_user_id: int
    collection_id: int
    new_entity_id:  Optional[int] = None
    field_name:  Optional[str] = None
    run: Optional[Annotated["Run", strawberry.lazy("api.types.run")]] = load_run_rows  # type:ignore


# We need to add this to each Queryable type so that strawberry will accept either our
# Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
RunEntityInput.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.RunEntityInput or type(obj) == RunEntityInput
)


# ------------------------------------------------------------------------------
# Mutation types
# ------------------------------------------------------------------------------




@strawberry.input()
class RunEntityInputCreateInput:
    collection_id:  int
    new_entity_id:  Optional[int] = None
    field_name:  Optional[str] = None 
    run_id:  Optional[strawberry.ID] = None 
@strawberry.input()
class RunEntityInputUpdateInput:
    collection_id:  Optional[int] = None
    new_entity_id:  Optional[int] = None
    field_name:  Optional[str] = None 
    run_id:  Optional[strawberry.ID] = None 


# ------------------------------------------------------------------------------
# Utilities
# ------------------------------------------------------------------------------

@strawberry.field(extensions=[DependencyExtension()])
async def resolve_run_entity_inputs(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[RunEntityInputWhereClause] = None,
) -> typing.Sequence[RunEntityInput]:
    return await get_db_rows(db.RunEntityInput, session, cerbos_client, principal, where, [])  # type: ignore

@strawberry.mutation(extensions=[DependencyExtension()])
async def create_run_entity_input(
    input: RunEntityInputCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> db.Entity:
    params = input.__dict__

    # Validate that user can create entity in this collection
    attr = {"collection_id": input.collection_id}
    resource = Resource(id="NEW_ID", kind=db.RunEntityInput.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise Exception("Unauthorized: Cannot create entity in this collection")

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.RunEntityInput(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_run_entity_input(
    input: RunEntityInputUpdateInput,
    where: RunEntityInputWhereClauseMutations,
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
    entities = await get_db_rows(db.RunEntityInput, session, cerbos_client, principal, where, [], CerbosAction.UPDATE)
    if len(entities) == 0:
        raise Exception("Unauthorized: Cannot update entities")

    # Validate that the user has access to the new collection ID
    if input.collection_id:
        attr = {"collection_id": input.collection_id}
        resource = Resource(id="SOME_ID", kind=db.RunEntityInput.__tablename__, attr=attr)
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
async def delete_run_entity_input(
    where: RunEntityInputWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(db.RunEntityInput, session, cerbos_client, principal, where, [], CerbosAction.DELETE)
    if len(entities) == 0:
        raise Exception("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities