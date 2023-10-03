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

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.sequencing_reads import SequencingReadWhereClause, SequencingRead
    from api.types.samples import Sample, SampleWhereClause



@strawberry.field(extensions=[DependencyExtension()])
def load_sequencing_reads(where: Optional[Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_reads")]]) -> Optional[Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_reads")]]:
    return None

@strawberry.field(extensions=[DependencyExtension()])
def load_samples(where: Optional[Annotated["SampleWhereClause", strawberry.lazy("api.types.samples")]]) -> Optional[Annotated["Sample", strawberry.lazy("api.types.samples")]]:
    return None