"""
GraphQL type for HostOrganism

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


import typing
from typing import TYPE_CHECKING, Annotated, Optional, Sequence

import database.models as db
import strawberry
import datetime
from platformics.api.core.helpers import get_db_rows, get_aggregate_db_rows
from api.validators.host_organism import HostOrganismCreateInputValidator, HostOrganismUpdateInputValidator
from api.types.entities import EntityInterface
from api.types.index_file import IndexFileAggregate, format_index_file_aggregate_output
from api.types.sample import SampleAggregate, format_sample_aggregate_output
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource
from fastapi import Depends
from platformics.api.core.errors import PlatformicsException
from platformics.api.core.deps import get_cerbos_client, get_db_session, require_auth_principal, is_system_user
from platformics.api.core.gql_to_sql import (
    aggregator_map,
    orderBy,
    EnumComparators,
    DatetimeComparators,
    IntComparators,
    StrComparators,
    UUIDComparators,
    BoolComparators,
)
from platformics.api.core.strawberry_extensions import DependencyExtension
from platformics.security.authorization import CerbosAction
from sqlalchemy import inspect
from sqlalchemy.engine.row import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import relay
from strawberry.types import Info
from typing_extensions import TypedDict
import enum
from support.enums import HostOrganismCategory

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.index_file import IndexFileOrderByClause, IndexFileWhereClause, IndexFile
    from api.types.sample import SampleOrderByClause, SampleWhereClause, Sample

    pass
else:
    IndexFileWhereClause = "IndexFileWhereClause"
    IndexFile = "IndexFile"
    IndexFileOrderByClause = "IndexFileOrderByClause"
    SampleWhereClause = "SampleWhereClause"
    Sample = "Sample"
    SampleOrderByClause = "SampleOrderByClause"
    pass


"""
------------------------------------------------------------------------------
Dataloaders
------------------------------------------------------------------------------
These are batching functions for loading related objects to avoid N+1 queries.
"""


@relay.connection(
    relay.ListConnection[Annotated["IndexFile", strawberry.lazy("api.types.index_file")]]  # type:ignore
)
async def load_index_file_rows(
    root: "HostOrganism",
    info: Info,
    where: Annotated["IndexFileWhereClause", strawberry.lazy("api.types.index_file")] | None = None,
    order_by: Optional[list[Annotated["IndexFileOrderByClause", strawberry.lazy("api.types.index_file")]]] = [],
) -> Sequence[Annotated["IndexFile", strawberry.lazy("api.types.index_file")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.HostOrganism)
    relationship = mapper.relationships["indexes"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.id)  # type:ignore


@strawberry.field
async def load_index_file_aggregate_rows(
    root: "HostOrganism",
    info: Info,
    where: Annotated["IndexFileWhereClause", strawberry.lazy("api.types.index_file")] | None = None,
) -> Optional[Annotated["IndexFileAggregate", strawberry.lazy("api.types.index_file")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.HostOrganism)
    relationship = mapper.relationships["indexes"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    # Aggregate queries always return a single row, so just grab the first one
    result = rows[0] if rows else None
    aggregate_output = format_index_file_aggregate_output(result)
    return IndexFileAggregate(aggregate=aggregate_output)


@relay.connection(
    relay.ListConnection[Annotated["Sample", strawberry.lazy("api.types.sample")]]  # type:ignore
)
async def load_sample_rows(
    root: "HostOrganism",
    info: Info,
    where: Annotated["SampleWhereClause", strawberry.lazy("api.types.sample")] | None = None,
    order_by: Optional[list[Annotated["SampleOrderByClause", strawberry.lazy("api.types.sample")]]] = [],
) -> Sequence[Annotated["Sample", strawberry.lazy("api.types.sample")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.HostOrganism)
    relationship = mapper.relationships["samples"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.id)  # type:ignore


@strawberry.field
async def load_sample_aggregate_rows(
    root: "HostOrganism",
    info: Info,
    where: Annotated["SampleWhereClause", strawberry.lazy("api.types.sample")] | None = None,
) -> Optional[Annotated["SampleAggregate", strawberry.lazy("api.types.sample")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.HostOrganism)
    relationship = mapper.relationships["samples"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    # Aggregate queries always return a single row, so just grab the first one
    result = rows[0] if rows else None
    aggregate_output = format_sample_aggregate_output(result)
    return SampleAggregate(aggregate=aggregate_output)


"""
------------------------------------------------------------------------------
Define Strawberry GQL types
------------------------------------------------------------------------------
"""

"""
Only let users specify IDs in WHERE clause when mutating data (for safety).
We can extend that list as we gather more use cases from the FE team.
"""


@strawberry.input
class HostOrganismWhereClauseMutations(TypedDict):
    id: UUIDComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class HostOrganismWhereClause(TypedDict):
    name: Optional[StrComparators] | None
    version: Optional[StrComparators] | None
    category: Optional[EnumComparators[HostOrganismCategory]] | None
    is_deuterostome: Optional[BoolComparators] | None
    indexes: Optional[Annotated["IndexFileWhereClause", strawberry.lazy("api.types.index_file")]] | None
    samples: Optional[Annotated["SampleWhereClause", strawberry.lazy("api.types.sample")]] | None
    id: Optional[UUIDComparators] | None
    producing_run_id: Optional[UUIDComparators] | None
    owner_user_id: Optional[IntComparators] | None
    collection_id: Optional[IntComparators] | None
    created_at: Optional[DatetimeComparators] | None
    updated_at: Optional[DatetimeComparators] | None


"""
Supported ORDER BY clause attributes
"""


@strawberry.input
class HostOrganismOrderByClause(TypedDict):
    name: Optional[orderBy] | None
    version: Optional[orderBy] | None
    category: Optional[orderBy] | None
    is_deuterostome: Optional[orderBy] | None
    id: Optional[orderBy] | None
    producing_run_id: Optional[orderBy] | None
    owner_user_id: Optional[orderBy] | None
    collection_id: Optional[orderBy] | None
    created_at: Optional[orderBy] | None
    updated_at: Optional[orderBy] | None


"""
Define HostOrganism type
"""


@strawberry.type
class HostOrganism(EntityInterface):
    name: str
    version: str
    category: HostOrganismCategory
    is_deuterostome: bool
    indexes: Sequence[
        Annotated["IndexFile", strawberry.lazy("api.types.index_file")]
    ] = load_index_file_rows  # type:ignore
    indexes_aggregate: Optional[
        Annotated["IndexFileAggregate", strawberry.lazy("api.types.index_file")]
    ] = load_index_file_aggregate_rows  # type:ignore
    samples: Sequence[Annotated["Sample", strawberry.lazy("api.types.sample")]] = load_sample_rows  # type:ignore
    samples_aggregate: Optional[
        Annotated["SampleAggregate", strawberry.lazy("api.types.sample")]
    ] = load_sample_aggregate_rows  # type:ignore
    id: strawberry.ID
    producing_run_id: Optional[strawberry.ID] = None
    owner_user_id: int
    collection_id: int
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None


"""
We need to add this to each Queryable type so that strawberry will accept either our
Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
"""
HostOrganism.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.HostOrganism or type(obj) == HostOrganism
)

"""
------------------------------------------------------------------------------
Aggregation types
------------------------------------------------------------------------------
"""
"""
Define columns that support numerical aggregations
"""


@strawberry.type
class HostOrganismNumericalColumns:
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class HostOrganismMinMaxColumns:
    name: Optional[str] = None
    version: Optional[str] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class HostOrganismCountColumns(enum.Enum):
    name = "name"
    version = "version"
    category = "category"
    is_deuterostome = "is_deuterostome"
    indexes = "indexes"
    samples = "samples"
    id = "id"
    producing_run_id = "producing_run_id"
    owner_user_id = "owner_user_id"
    collection_id = "collection_id"
    created_at = "created_at"
    updated_at = "updated_at"


"""
All supported aggregation functions
"""


@strawberry.type
class HostOrganismAggregateFunctions:
    # This is a hack to accept "distinct" and "columns" as arguments to "count"
    @strawberry.field
    def count(
        self, distinct: Optional[bool] = False, columns: Optional[HostOrganismCountColumns] = None
    ) -> Optional[int]:
        # Count gets set with the proper value in the resolver, so we just return it here
        return self.count  # type: ignore

    sum: Optional[HostOrganismNumericalColumns] = None
    avg: Optional[HostOrganismNumericalColumns] = None
    stddev: Optional[HostOrganismNumericalColumns] = None
    variance: Optional[HostOrganismNumericalColumns] = None
    min: Optional[HostOrganismMinMaxColumns] = None
    max: Optional[HostOrganismMinMaxColumns] = None


"""
Wrapper around HostOrganismAggregateFunctions
"""

@strawberry.type
class HostOrganismGroupByOptions:
    name: Optional[str] = None
    version: Optional[str] = None


@strawberry.type
class HostOrganismAggregate:
    aggregate: Optional[HostOrganismAggregateFunctions] = None
    group_by: Optional[HostOrganismGroupByOptions] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class HostOrganismCreateInput:
    name: str
    version: str
    category: HostOrganismCategory
    is_deuterostome: bool
    producing_run_id: Optional[strawberry.ID] = None
    collection_id: int


@strawberry.input()
class HostOrganismUpdateInput:
    name: Optional[str] = None
    version: Optional[str] = None
    category: Optional[HostOrganismCategory] = None
    is_deuterostome: Optional[bool] = None


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_host_organisms(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[HostOrganismWhereClause] = None,
    order_by: Optional[list[HostOrganismOrderByClause]] = [],
) -> typing.Sequence[HostOrganism]:
    """
    Resolve HostOrganism objects. Used for queries (see api/queries.py).
    """
    return await get_db_rows(db.HostOrganism, session, cerbos_client, principal, where, order_by)  # type: ignore


def format_host_organism_aggregate_output(query_results: RowMapping) -> HostOrganismAggregateFunctions:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = HostOrganismAggregateFunctions()
    for aggregate_name, value in query_results.items():
        if aggregate_name == "count":
            output.count = value
        else:
            aggregator_fn, col_name = aggregate_name.split("_", 1)
            # Filter out the group_by key from the results if one was provided.
            if aggregator_fn in aggregator_map.keys():
                if not getattr(output, aggregator_fn):
                    if aggregate_name in ["min", "max"]:
                        setattr(output, aggregator_fn, HostOrganismMinMaxColumns())
                    else:
                        setattr(output, aggregator_fn, HostOrganismNumericalColumns())
                setattr(getattr(output, aggregator_fn), col_name, value)
    return output


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_host_organisms_aggregate(
    info: Info,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[HostOrganismWhereClause] = None,
) -> HostOrganismAggregate:
    """
    Aggregate values for HostOrganism objects. Used for queries (see api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on
    # TODO: not sure why selected_fields is a list
    # The first list of selections will always be ["aggregate"], so just grab the first item
    selections = info.selected_fields[0].selections[0].selections
    rows = await get_aggregate_db_rows(db.HostOrganism, session, cerbos_client, principal, where, selections, [])  # type: ignore
    aggregate_output = format_host_organism_aggregate_output(rows)
    return HostOrganismAggregate(aggregate=aggregate_output)


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_host_organism(
    input: HostOrganismCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> db.Entity:
    """
    Create a new HostOrganism object. Used for mutations (see api/mutations.py).
    """
    validated = HostOrganismCreateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Validate that the user can read all of the entities they're linking to.
    # If we have any system_writable fields present, make sure that our auth'd user *is* a system user
    if not is_system_user:
        del params["producing_run_id"]
    # Validate that the user can create entities in this collection
    attr = {"collection_id": validated.collection_id}
    resource = Resource(id="NEW_ID", kind=db.HostOrganism.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise PlatformicsException("Unauthorized: Cannot create entity in this collection")

    # Validate that the user can read all of the entities they're linking to.

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.HostOrganism(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_host_organism(
    input: HostOrganismUpdateInput,
    where: HostOrganismWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> Sequence[db.Entity]:
    """
    Update HostOrganism objects. Used for mutations (see api/mutations.py).
    """
    validated = HostOrganismUpdateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise PlatformicsException("No fields to update")

    # Validate that the user can read all of the entities they're linking to.

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(db.HostOrganism, session, cerbos_client, principal, where, [], CerbosAction.UPDATE)
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot update entities")

    # Update DB
    updated_at = datetime.datetime.now()
    for entity in entities:
        entity.updated_at = updated_at
        for key in params:
            if params[key] is not None:
                setattr(entity, key, params[key])
    await session.commit()
    return entities


@strawberry.mutation(extensions=[DependencyExtension()])
async def delete_host_organism(
    where: HostOrganismWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Delete HostOrganism objects. Used for mutations (see api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(db.HostOrganism, session, cerbos_client, principal, where, [], CerbosAction.DELETE)
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
