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
from typing import TYPE_CHECKING, Annotated
from pydantic import BaseModel
from api.types.dataloaders import load_sequencing_reads

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.sequencing_reads import SequencingReadWhereClause, SequencingRead
else:
    SequencingReadWhereClause = "SequencingReadWhereClause"
    SequencingRead = "SequencingRead"


@strawberry.input
class SampleWhereClause(TypedDict):
    id: Optional[UUIDComparators]
    name: Optional[StrComparators]
    location: Optional[StrComparators]
    sequencing_reads: Optional[Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_reads")]]

def get_sequencing_reads(where: "SequencingReadWhereClause", ids: list[int])->typing.Sequence[SequencingRead]:
    return []

@strawberry.field(extensions=[DependencyExtension()])
def do_stuff(where: Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_reads")] | None ) -> Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_reads")] | None:
    return None

@strawberry.type
class Sample(EntityInterface):
    id: uuid.UUID
    name: str
    location: str
    sequencing_reads: Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_reads")] = load_sequencing_reads

Sample.__strawberry_definition__.is_type_of = (
    lambda obj, info: type(obj) == db.Sample or type(obj) == Sample
)

@strawberry.field(extensions=[DependencyExtension()])
async def resolve_samples(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[SampleWhereClause] = None,
) -> typing.Sequence[Sample]:
    return await get_db_rows(db.Sample, session, cerbos_client, principal, where, [])  # type: ignore
