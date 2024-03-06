"""
GraphQL type for Sample

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
from api.validators.sample import SampleCreateInputValidator, SampleUpdateInputValidator
from api.helpers.sample import SampleGroupByOptions, build_sample_groupby_output
from api.types.entities import EntityInterface
from api.types.sequencing_read import SequencingReadAggregate, format_sequencing_read_aggregate_output
from api.types.metadatum import MetadatumAggregate, format_metadatum_aggregate_output
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource
from fastapi import Depends
from platformics.api.core.errors import PlatformicsException
from platformics.api.core.deps import get_cerbos_client, get_db_session, require_auth_principal, is_system_user
from platformics.api.core.gql_to_sql import (
    aggregator_map,
    orderBy,
    DatetimeComparators,
    IntComparators,
    StrComparators,
    UUIDComparators,
)
from platformics.api.core.strawberry_extensions import DependencyExtension
from platformics.security.authorization import CerbosAction
from sqlalchemy import inspect
from sqlalchemy.engine.row import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import relay
from strawberry.types import Info
from support.limit_offset import LimitOffsetClause
from typing_extensions import TypedDict
import enum


E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.host_organism import HostOrganismOrderByClause, HostOrganismWhereClause, HostOrganism
    from api.types.sequencing_read import SequencingReadOrderByClause, SequencingReadWhereClause, SequencingRead
    from api.types.metadatum import MetadatumOrderByClause, MetadatumWhereClause, Metadatum

    pass
else:
    HostOrganismWhereClause = "HostOrganismWhereClause"
    HostOrganism = "HostOrganism"
    HostOrganismOrderByClause = "HostOrganismOrderByClause"
    SequencingReadWhereClause = "SequencingReadWhereClause"
    SequencingRead = "SequencingRead"
    SequencingReadOrderByClause = "SequencingReadOrderByClause"
    MetadatumWhereClause = "MetadatumWhereClause"
    Metadatum = "Metadatum"
    MetadatumOrderByClause = "MetadatumOrderByClause"
    pass


"""
------------------------------------------------------------------------------
Dataloaders
------------------------------------------------------------------------------
These are batching functions for loading related objects to avoid N+1 queries.
"""


@strawberry.field
async def load_host_organism_rows(
    root: "Sample",
    info: Info,
    where: Annotated["HostOrganismWhereClause", strawberry.lazy("api.types.host_organism")] | None = None,
    order_by: Optional[list[Annotated["HostOrganismOrderByClause", strawberry.lazy("api.types.host_organism")]]] = [],
) -> Optional[Annotated["HostOrganism", strawberry.lazy("api.types.host_organism")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Sample)
    relationship = mapper.relationships["host_organism"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.host_organism_id)  # type:ignore


@relay.connection(
    relay.ListConnection[Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]]  # type:ignore
)
async def load_sequencing_read_rows(
    root: "Sample",
    info: Info,
    where: Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")] | None = None,
    order_by: Optional[
        list[Annotated["SequencingReadOrderByClause", strawberry.lazy("api.types.sequencing_read")]]
    ] = [],
) -> Sequence[Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Sample)
    relationship = mapper.relationships["sequencing_reads"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.id)  # type:ignore


@strawberry.field
async def load_sequencing_read_aggregate_rows(
    root: "Sample",
    info: Info,
    where: Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")] | None = None,
) -> Optional[Annotated["SequencingReadAggregate", strawberry.lazy("api.types.sequencing_read")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Sample)
    relationship = mapper.relationships["sequencing_reads"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    aggregate_output = format_sequencing_read_aggregate_output(rows)
    return aggregate_output


@relay.connection(
    relay.ListConnection[Annotated["Metadatum", strawberry.lazy("api.types.metadatum")]]  # type:ignore
)
async def load_metadatum_rows(
    root: "Sample",
    info: Info,
    where: Annotated["MetadatumWhereClause", strawberry.lazy("api.types.metadatum")] | None = None,
    order_by: Optional[list[Annotated["MetadatumOrderByClause", strawberry.lazy("api.types.metadatum")]]] = [],
) -> Sequence[Annotated["Metadatum", strawberry.lazy("api.types.metadatum")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Sample)
    relationship = mapper.relationships["metadatas"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.id)  # type:ignore


@strawberry.field
async def load_metadatum_aggregate_rows(
    root: "Sample",
    info: Info,
    where: Annotated["MetadatumWhereClause", strawberry.lazy("api.types.metadatum")] | None = None,
) -> Optional[Annotated["MetadatumAggregate", strawberry.lazy("api.types.metadatum")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Sample)
    relationship = mapper.relationships["metadatas"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    aggregate_output = format_metadatum_aggregate_output(rows)
    return aggregate_output


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
class SampleWhereClauseMutations(TypedDict):
    id: UUIDComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class SampleWhereClause(TypedDict):
    rails_sample_id: Optional[IntComparators] | None
    name: Optional[StrComparators] | None
    host_organism: Optional[Annotated["HostOrganismWhereClause", strawberry.lazy("api.types.host_organism")]] | None
    sequencing_reads: Optional[
        Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")]
    ] | None
    metadatas: Optional[Annotated["MetadatumWhereClause", strawberry.lazy("api.types.metadatum")]] | None
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
class SampleOrderByClause(TypedDict):
    rails_sample_id: Optional[orderBy] | None
    name: Optional[orderBy] | None
    host_organism: Optional[Annotated["HostOrganismOrderByClause", strawberry.lazy("api.types.host_organism")]] | None
    id: Optional[orderBy] | None
    producing_run_id: Optional[orderBy] | None
    owner_user_id: Optional[orderBy] | None
    collection_id: Optional[orderBy] | None
    created_at: Optional[orderBy] | None
    updated_at: Optional[orderBy] | None


"""
Define Sample type
"""


@strawberry.type
class Sample(EntityInterface):
    rails_sample_id: Optional[int] = None
    name: str
    host_organism: Optional[
        Annotated["HostOrganism", strawberry.lazy("api.types.host_organism")]
    ] = load_host_organism_rows  # type:ignore
    sequencing_reads: Sequence[
        Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]
    ] = load_sequencing_read_rows  # type:ignore
    sequencing_reads_aggregate: Optional[
        Annotated["SequencingReadAggregate", strawberry.lazy("api.types.sequencing_read")]
    ] = load_sequencing_read_aggregate_rows  # type:ignore
    metadatas: Sequence[
        Annotated["Metadatum", strawberry.lazy("api.types.metadatum")]
    ] = load_metadatum_rows  # type:ignore
    metadatas_aggregate: Optional[
        Annotated["MetadatumAggregate", strawberry.lazy("api.types.metadatum")]
    ] = load_metadatum_aggregate_rows  # type:ignore
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
Sample.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.Sample or type(obj) == Sample
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
class SampleNumericalColumns:
    rails_sample_id: Optional[int] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class SampleMinMaxColumns:
    rails_sample_id: Optional[int] = None
    name: Optional[str] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class SampleCountColumns(enum.Enum):
    railsSampleId = "rails_sample_id"
    name = "name"
    hostOrganism = "host_organism"
    sequencingReads = "sequencing_reads"
    metadatas = "metadatas"
    id = "id"
    producingRunId = "producing_run_id"
    ownerUserId = "owner_user_id"
    collectionId = "collection_id"
    createdAt = "created_at"
    updatedAt = "updated_at"


"""
All supported aggregation functions
"""


@strawberry.type
class SampleAggregateFunctions:
    # This is a hack to accept "distinct" and "columns" as arguments to "count"
    @strawberry.field
    def count(self, distinct: Optional[bool] = False, columns: Optional[SampleCountColumns] = None) -> Optional[int]:
        # Count gets set with the proper value in the resolver, so we just return it here
        return self.count  # type: ignore

    sum: Optional[SampleNumericalColumns] = None
    avg: Optional[SampleNumericalColumns] = None
    stddev: Optional[SampleNumericalColumns] = None
    variance: Optional[SampleNumericalColumns] = None
    min: Optional[SampleMinMaxColumns] = None
    max: Optional[SampleMinMaxColumns] = None
    groupBy: Optional[SampleGroupByOptions] = None


"""
Wrapper around SampleAggregateFunctions
"""


@strawberry.type
class SampleAggregate:
    aggregate: Optional[list[SampleAggregateFunctions]] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class SampleCreateInput:
    rails_sample_id: Optional[int] = None
    name: str
    host_organism_id: Optional[strawberry.ID] = None
    producing_run_id: Optional[strawberry.ID] = None
    collection_id: int


@strawberry.input()
class SampleUpdateInput:
    name: Optional[str] = None


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_samples(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[SampleWhereClause] = None,
    order_by: Optional[list[SampleOrderByClause]] = [],
    limit_offset: Optional[LimitOffsetClause] = None,
) -> typing.Sequence[Sample]:
    """
    Resolve Sample objects. Used for queries (see api/queries.py).
    """
    limit = limit_offset["limit"] if limit_offset and "limit" in limit_offset else None
    offset = limit_offset["offset"] if limit_offset and "offset" in limit_offset else None
    if offset and not limit:
        raise PlatformicsException("Cannot use offset without limit")
    return await get_db_rows(db.Sample, session, cerbos_client, principal, where, order_by, CerbosAction.VIEW, limit, offset)  # type: ignore


def format_sample_aggregate_output(query_results: Sequence[RowMapping] | RowMapping) -> SampleAggregate:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    aggregate = []
    if type(query_results) is not list:
        query_results = [query_results]  # type: ignore
    for row in query_results:
        aggregate.append(format_sample_aggregate_row(row))
    return SampleAggregate(aggregate=aggregate)


def format_sample_aggregate_row(row: RowMapping) -> SampleAggregateFunctions:
    """
    Given a single row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = SampleAggregateFunctions()
    for key, value in row.items():
        # Key is either an aggregate function or a groupby key
        group_keys = key.split(".")
        aggregate = key.split("_", 1)
        if aggregate[0] not in aggregator_map.keys():
            # Turn list of groupby keys into nested objects
            if not getattr(output, "groupBy"):
                setattr(output, "groupBy", SampleGroupByOptions())
            group = build_sample_groupby_output(getattr(output, "groupBy"), group_keys, value)
            setattr(output, "groupBy", group)
        else:
            aggregate_name = aggregate[0]
            if aggregate_name == "count":
                output.count = value
            else:
                aggregator_fn, col_name = aggregate[0], aggregate[1]
                if not getattr(output, aggregator_fn):
                    if aggregate_name in ["min", "max"]:
                        setattr(output, aggregator_fn, SampleMinMaxColumns())
                    else:
                        setattr(output, aggregator_fn, SampleNumericalColumns())
                setattr(getattr(output, aggregator_fn), col_name, value)
    return output


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_samples_aggregate(
    info: Info,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[SampleWhereClause] = None,
    # TODO: add support for groupby, limit/offset
) -> SampleAggregate:
    """
    Aggregate values for Sample objects. Used for queries (see api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on, and groupby options if any were provided.
    # TODO: not sure why selected_fields is a list
    selections = info.selected_fields[0].selections[0].selections
    aggregate_selections = [selection for selection in selections if getattr(selection, "name") != "groupBy"]
    groupby_selections = [selection for selection in selections if getattr(selection, "name") == "groupBy"]
    groupby_selections = groupby_selections[0].selections if groupby_selections else []

    if not aggregate_selections:
        raise PlatformicsException("No aggregate functions selected")

    rows = await get_aggregate_db_rows(db.Sample, session, cerbos_client, principal, where, aggregate_selections, [], groupby_selections)  # type: ignore
    aggregate_output = format_sample_aggregate_output(rows)
    return aggregate_output


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_sample(
    input: SampleCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> db.Entity:
    """
    Create a new Sample object. Used for mutations (see api/mutations.py).
    """
    validated = SampleCreateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Validate that the user can read all of the entities they're linking to.
    # If we have any system_writable fields present, make sure that our auth'd user *is* a system user
    if not is_system_user:
        del params["rails_sample_id"]
        del params["producing_run_id"]
    # Validate that the user can create entities in this collection
    attr = {"collection_id": validated.collection_id}
    resource = Resource(id="NEW_ID", kind=db.Sample.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise PlatformicsException("Unauthorized: Cannot create entity in this collection")

    # Validate that the user can read all of the entities they're linking to.
    # Check that host_organism relationship is accessible.
    if validated.host_organism_id:
        host_organism = await get_db_rows(
            db.HostOrganism,
            session,
            cerbos_client,
            principal,
            {"id": {"_eq": validated.host_organism_id}},
            [],
            CerbosAction.VIEW,
        )
        if not host_organism:
            raise PlatformicsException("Unauthorized: host_organism does not exist")

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.Sample(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_sample(
    input: SampleUpdateInput,
    where: SampleWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> Sequence[db.Entity]:
    """
    Update Sample objects. Used for mutations (see api/mutations.py).
    """
    validated = SampleUpdateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise PlatformicsException("No fields to update")

    # Validate that the user can read all of the entities they're linking to.

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(db.Sample, session, cerbos_client, principal, where, [], CerbosAction.UPDATE)
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
async def delete_sample(
    where: SampleWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Delete Sample objects. Used for mutations (see api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(db.Sample, session, cerbos_client, principal, where, [], CerbosAction.DELETE)
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
