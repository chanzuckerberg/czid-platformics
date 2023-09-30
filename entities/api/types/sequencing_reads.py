import typing
import uuid
from collections import defaultdict
from typing import Any, Mapping, Optional, Tuple

import database.models as db
import strawberry
from api.types.entities import EntityInterface
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource
from fastapi import Depends
from platformics.api.core.deps import (get_cerbos_client, get_db_session,
                                       require_auth_principal)
from platformics.api.core.gql_to_sql import (EnumComparators, IntComparators,
                                             StrComparators, UUIDComparators,
                                             strawberry_sqlalchemy_mapper)
from platformics.api.core.strawberry_extensions import DependencyExtension
from platformics.database.connect import AsyncDB
from platformics.security.authorization import CerbosAction, get_resource_query
from sqlalchemy import ColumnElement, ColumnExpressionArgument, tuple_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import RelationshipProperty
from strawberry.arguments import StrawberryArgument
from strawberry.dataloader import DataLoader
from typing_extensions import TypedDict
from platformics.api.core.gql_to_sql import (
    convert_where_clauses_to_sql,
)
from api.core.helpers import get_db_rows

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")


@strawberry.input
class SequencingReadWhereClause(TypedDict):
    id: typing.Optional[UUIDComparators]
    name: typing.Optional[StrComparators]
    location: typing.Optional[StrComparators]

@strawberry_sqlalchemy_mapper.type(db.SequencingRead)
class SequencingRead(EntityInterface):
    _where_clause_ = SequencingReadWhereClause


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_sequencing_reads(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: SequencingReadWhereClause = {},
) -> typing.Sequence[SequencingRead]:
    return await get_db_rows(db.SequencingRead, session, cerbos_client, principal, where, [])  # type: ignore
