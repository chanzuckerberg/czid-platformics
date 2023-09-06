import typing
import uuid
from typing_extensions import TypedDict

import database.models as db
import strawberry
from api.core.deps import get_cerbos_client, get_db_session, require_auth_principal
from api.core.strawberry_extensions import DependencyExtension
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource
from database.models import FileStatus
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.core.gql_types import UUIDComparators, StrComparators, IntComparators, EnumComparators

CERBOS_ACTION_UPDATE = "update"

FileStatusEnum = strawberry.enum(FileStatus)

@strawberry.input
class FileSetParams(TypedDict):
    status: FileStatus
    protocol: str
    namespace: str
    path: str
    compression_type: str

@strawberry.input
class FileWhereClause(TypedDict):
    id: UUIDComparators
    status: EnumComparators[FileStatus]
    protocol: StrComparators
    namespace: StrComparators
    path: StrComparators
    compression_type: StrComparators


@strawberry.field(extensions=[DependencyExtension()])
async def file_update(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: FileWhereClause = {},
    _set: FileSetParams = {},
) -> db.File:
    return {}
    params = {key: kwargs[key] for key in kwargs if key != "kwargs"}

    # Fetch entity for update, if we have access to it
    filters = [sql_model.id == entity_id]
    entities = await get_entities(sql_model, session, cerbos_client, principal, filters, [])  # type: ignore
    if len(entities) != 1:
        raise Exception("Unauthorized: Cannot retrieve entity")
    entity = entities[0]

    # Validate that user can update this entity. For now, this is redundant with get_entities() above,
    # but it's possible we'll want "update" actions to require additional permissions in the future.
    attr = {"collection_id": entity.collection_id}
    resource = Resource(id=str(entity.id), kind=sql_model.__tablename__, attr=attr)
    if not cerbos_client.is_allowed(CERBOS_ACTION_UPDATE, principal, resource):
        raise Exception("Unauthorized: Cannot update entity")

    # Update DB
    for key in params:
        if params[key]:
            setattr(entity, key, params[key])
    await session.commit()

    return entity

    update.arguments = generate_strawberry_arguments(CERBOS_ACTION_UPDATE, sql_model, gql_type)

    return typing.cast(T, update)
