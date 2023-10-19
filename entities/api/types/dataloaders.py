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
from sqlalchemy import ColumnElement, ColumnExpressionArgument, tuple_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import RelationshipProperty
from strawberry.arguments import StrawberryArgument
from strawberry.dataloader import DataLoader
from typing_extensions import TypedDict
from api.core.helpers import get_db_rows
from typing import TYPE_CHECKING, Annotated
from pydantic import BaseModel
import database.models as db

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.sequencing_reads import SequencingReadWhereClause, SequencingRead
    from api.types.samples import Sample, SampleWhereClause

def cache_key(key: dict) -> str:
    return key["id"]

async def batch_sequencing_reads(keys: list[dict]) -> Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_reads")]:
    session = keys[0]["session"]
    cerbos_client = keys[0]["cerbos_client"]
    principal = keys[0]["principal"]
    ids = [key["id"] for key in keys]

    query = get_resource_query(principal, cerbos_client, CerbosAction.VIEW, db.SequencingRead)
    query = query.filter(db.SequencingRead.sample_id.in_(ids))
    result = await session.execute(query)
    return result.scalars().all()

sequencing_read_loader = DataLoader(load_fn=batch_sequencing_reads, cache_key_fn=cache_key)

@strawberry.field(extensions=[DependencyExtension()])
async def load_sequencing_reads(
    root: "Sample",
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    ) -> Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_reads")]:
    return await sequencing_read_loader.load({"session": session, "cerbos_client": cerbos_client, "principal": principal, "id":root.id})


async def batch_samples(keys: list[dict]) -> Annotated["Sample", strawberry.lazy("api.types.samples")]:
    session = keys[0]["session"]
    cerbos_client = keys[0]["cerbos_client"]
    principal = keys[0]["principal"]
    ids = [key["id"] for key in keys]

    query = get_resource_query(principal, cerbos_client, CerbosAction.VIEW, db.SequencingRead)
    # filter samples based on their sequencing reads' ids
    # TODO: this query isn't working; fix "Received wrong number of results in dataloader, expected: 2, received: 5"
    # number of results returned needs to equal the number of ids that were passed in
    query = query.filter(db.Sample.sequencing_reads.any(db.SequencingRead.id.in_(ids)))
    # query = query.filter(db.Sample.id.in_(select(db.SequencingRead.sample_id).where(db.SequencingRead.id.in_(ids))))
    result = await session.execute(query)
    return result.scalars().all()

sample_loader = DataLoader(load_fn=batch_samples, cache_key_fn=cache_key)

@strawberry.field(extensions=[DependencyExtension()])
async def load_samples(
    root: "SequencingRead",
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    ) -> Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_reads")]:
    return await sample_loader.load({"session": session, "cerbos_client": cerbos_client, "principal": principal, "id":root.id})
