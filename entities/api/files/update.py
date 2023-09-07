import typing
from typing_extensions import TypedDict

import database.models as db
import strawberry
from api.core.deps import strawberry_sqlalchemy_mapper, get_cerbos_client, get_db_session, require_auth_principal
from api.core.strawberry_extensions import DependencyExtension
from cerbos.sdk.client import CerbosClient
from database.models import FileStatus
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.core.gql_types import UUIDComparators, StrComparators, IntComparators, EnumComparators
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


operator_map = {
    "_eq": "__eq__",
    "_neq": "__ne__",
    "_in_": "in_",
    "_nin": "not_in",
    "_is_null": "SPECIAL",
    "_gt": "__gt__",
    "_gte": "__ge__",
    "_lt": "__lt__",
    "_lte": "__le__",
    "_like": "like",
    "_nlike": "notlike",
    "_ilike": "ilike",
    "_nilike": "notilike",
    "_regex": "regexp_match",
    # "_nregex": Optional[str] # TODO
    # "_iregex": Optional[str]# TODO
    # "_niregex": Optional[str]# TODO
}


def convert_where_clauses_to_sql(query, sa_model, whereClause):
    for k, v in whereClause.items():
        for comparator, value in v.items():
            sa_comparator = operator_map[comparator]
            if sa_comparator == "SPECIAL":
                query = query.filter(getattr(sa_model, k).is_(None))
            else:
                query = query.filter(getattr(getattr(sa_model, k), sa_comparator)(value))
    return query


@strawberry.field(extensions=[DependencyExtension()])
async def file_update(
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
    query = convert_where_clauses_to_sql(query, model_cls, where)
    rows = await session.execute(query)
    print(query)
    res = FileUpdated(returning=rows.scalars().all())
    return res
