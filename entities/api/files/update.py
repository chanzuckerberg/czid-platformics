import typing
from typing_extensions import TypedDict

import database.models as db
import strawberry
from api.core.deps import get_cerbos_client, get_db_session, require_auth_principal
from api.core.gql_to_sql import strawberry_sqlalchemy_mapper
from api.core.strawberry_extensions import DependencyExtension
from cerbos.sdk.client import CerbosClient
from database.models import FileStatus
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.core.gql_to_sql import (
    UUIDComparators,
    StrComparators,
    IntComparators,
    EnumComparators,
    convert_where_clauses_to_sql,
)
from thirdparty.cerbos_sqlalchemy.query import get_query
from cerbos.sdk.model import Principal, ResourceDesc

CERBOS_ACTION_UPDATE = "update"

FileStatusEnum = strawberry.enum(FileStatus)


@strawberry_sqlalchemy_mapper.type(db.File)
class File:
    pass


@strawberry.input
class FileSetParams(TypedDict):
    status: typing.Optional[FileStatus]
    protocol: typing.Optional[str]
    namespace: typing.Optional[str]
    path: typing.Optional[str]
    compression_type: typing.Optional[str]


@strawberry.input
class FileWhereClause(TypedDict):
    id: typing.Optional[UUIDComparators]
    status: typing.Optional[EnumComparators[FileStatus]]
    protocol: typing.Optional[StrComparators]
    namespace: typing.Optional[StrComparators]
    path: typing.Optional[StrComparators]
    compression_type: typing.Optional[StrComparators]
    size: typing.Optional[IntComparators]


@strawberry.type
class FileUpdated:
    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    returning: list[File]


@strawberry.field(extensions=[DependencyExtension()])
async def update_one_file(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: FileWhereClause = {},
    _set: FileSetParams = {},
) -> FileUpdated:
    model_cls = db.File
    rd = ResourceDesc(model_cls.__tablename__)
    plan = cerbos_client.plan_resources(CERBOS_ACTION_UPDATE, principal, rd)
    query = get_query(
        plan,
        model_cls,  # type: ignore
        {
            "request.resource.attr.owner_user_id": db.Entity.owner_user_id,
            "request.resource.attr.collection_id": db.Entity.collection_id,
        },
        [(db.Entity, model_cls.entity_id == db.Entity.id)],  # type: ignore
    )
    # TODO - we should switch to doing this directly with update/where queries
    # for better perf. For now this is a little easier to debug and we're not
    # expecting huge bulk updates <yet>.
    query = convert_where_clauses_to_sql(query, model_cls, where)
    rows = await session.execute(query)
    res = []
    items = rows.scalars().one()
    for row in items:
        res.append(row)
        for k, v in _set.items():
            setattr(row, k, v)
    await session.commit()
    res = FileUpdated(returning=res)
    return res


@strawberry.field(extensions=[DependencyExtension()])
async def update_many_files(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: FileWhereClause = {},
    _set: FileSetParams = {},
) -> FileUpdated:
    model_cls = db.File
    rd = ResourceDesc(model_cls.__tablename__)
    plan = cerbos_client.plan_resources(CERBOS_ACTION_UPDATE, principal, rd)
    query = get_query(
        plan,
        model_cls,  # type: ignore
        {
            "request.resource.attr.owner_user_id": db.Entity.owner_user_id,
            "request.resource.attr.collection_id": db.Entity.collection_id,
        },
        [(db.Entity, model_cls.entity_id == db.Entity.id)],  # type: ignore
    )
    # TODO - we should switch to doing this directly with update/where queries
    # for better perf. For now this is a little easier to debug and we're not
    # expecting huge bulk updates <yet>.
    query = convert_where_clauses_to_sql(query, model_cls, where)
    rows = await session.execute(query)
    res = []
    items = rows.scalars().all()
    for row in items:
        res.append(row)
        for k, v in _set.items():
            setattr(row, k, v)
    await session.commit()
    res = FileUpdated(returning=res)
    return res
