"""
GraphQL type for ConsensusGenome

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/types/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long


import typing
from typing import TYPE_CHECKING, Annotated, Optional, Sequence, Callable

import database.models as db
import strawberry
import datetime
from platformics.api.core.helpers import get_db_rows, get_aggregate_db_rows
from api.validators.consensus_genome import ConsensusGenomeCreateInputValidator, ConsensusGenomeUpdateInputValidator
from api.files import File, FileWhereClause
from api.helpers.consensus_genome import ConsensusGenomeGroupByOptions, build_consensus_genome_groupby_output
from api.types.entities import EntityInterface
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
    UUIDComparators,
)
from platformics.api.core.strawberry_extensions import DependencyExtension
from platformics.security.authorization import CerbosAction
from sqlalchemy import inspect
from sqlalchemy.engine.row import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.types import Info
from support.limit_offset import LimitOffsetClause
from typing_extensions import TypedDict
import enum


E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.taxon import TaxonOrderByClause, TaxonWhereClause, Taxon
    from api.types.sequencing_read import SequencingReadOrderByClause, SequencingReadWhereClause, SequencingRead
    from api.types.reference_genome import ReferenceGenomeOrderByClause, ReferenceGenomeWhereClause, ReferenceGenome
    from api.types.accession import AccessionOrderByClause, AccessionWhereClause, Accession
    from api.types.metric_consensus_genome import (
        MetricConsensusGenomeOrderByClause,
        MetricConsensusGenomeWhereClause,
        MetricConsensusGenome,
    )

    pass
else:
    TaxonWhereClause = "TaxonWhereClause"
    Taxon = "Taxon"
    TaxonOrderByClause = "TaxonOrderByClause"
    SequencingReadWhereClause = "SequencingReadWhereClause"
    SequencingRead = "SequencingRead"
    SequencingReadOrderByClause = "SequencingReadOrderByClause"
    ReferenceGenomeWhereClause = "ReferenceGenomeWhereClause"
    ReferenceGenome = "ReferenceGenome"
    ReferenceGenomeOrderByClause = "ReferenceGenomeOrderByClause"
    AccessionWhereClause = "AccessionWhereClause"
    Accession = "Accession"
    AccessionOrderByClause = "AccessionOrderByClause"
    MetricConsensusGenomeWhereClause = "MetricConsensusGenomeWhereClause"
    MetricConsensusGenome = "MetricConsensusGenome"
    MetricConsensusGenomeOrderByClause = "MetricConsensusGenomeOrderByClause"
    pass


"""
------------------------------------------------------------------------------
Dataloaders
------------------------------------------------------------------------------
These are batching functions for loading related objects to avoid N+1 queries.
"""


@strawberry.field
async def load_taxon_rows(
    root: "ConsensusGenome",
    info: Info,
    where: Annotated["TaxonWhereClause", strawberry.lazy("api.types.taxon")] | None = None,
    order_by: Optional[list[Annotated["TaxonOrderByClause", strawberry.lazy("api.types.taxon")]]] = [],
) -> Optional[Annotated["Taxon", strawberry.lazy("api.types.taxon")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.ConsensusGenome)
    relationship = mapper.relationships["taxon"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.taxon_id)  # type:ignore


@strawberry.field
async def load_sequencing_read_rows(
    root: "ConsensusGenome",
    info: Info,
    where: Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")] | None = None,
    order_by: Optional[
        list[Annotated["SequencingReadOrderByClause", strawberry.lazy("api.types.sequencing_read")]]
    ] = [],
) -> Optional[Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.ConsensusGenome)
    relationship = mapper.relationships["sequencing_read"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.sequencing_read_id)  # type:ignore


@strawberry.field
async def load_reference_genome_rows(
    root: "ConsensusGenome",
    info: Info,
    where: Annotated["ReferenceGenomeWhereClause", strawberry.lazy("api.types.reference_genome")] | None = None,
    order_by: Optional[
        list[Annotated["ReferenceGenomeOrderByClause", strawberry.lazy("api.types.reference_genome")]]
    ] = [],
) -> Optional[Annotated["ReferenceGenome", strawberry.lazy("api.types.reference_genome")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.ConsensusGenome)
    relationship = mapper.relationships["reference_genome"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.reference_genome_id)  # type:ignore


@strawberry.field
async def load_accession_rows(
    root: "ConsensusGenome",
    info: Info,
    where: Annotated["AccessionWhereClause", strawberry.lazy("api.types.accession")] | None = None,
    order_by: Optional[list[Annotated["AccessionOrderByClause", strawberry.lazy("api.types.accession")]]] = [],
) -> Optional[Annotated["Accession", strawberry.lazy("api.types.accession")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.ConsensusGenome)
    relationship = mapper.relationships["accession"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.accession_id)  # type:ignore


@strawberry.field
async def load_metric_consensus_genome_rows(
    root: "ConsensusGenome",
    info: Info,
    where: Annotated["MetricConsensusGenomeWhereClause", strawberry.lazy("api.types.metric_consensus_genome")]
    | None = None,
    order_by: Optional[
        list[Annotated["MetricConsensusGenomeOrderByClause", strawberry.lazy("api.types.metric_consensus_genome")]]
    ] = [],
) -> Optional[Annotated["MetricConsensusGenome", strawberry.lazy("api.types.metric_consensus_genome")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.ConsensusGenome)
    relationship = mapper.relationships["metrics"]
    return await dataloader.loader_for(relationship, where).load(root.id)  # type:ignore


"""
------------------------------------------------------------------------------
Dataloader for File object
------------------------------------------------------------------------------
"""


def load_files_from(attr_name: str) -> Callable:
    @strawberry.field
    async def load_files(
        root: "ConsensusGenome",
        info: Info,
        where: Annotated["FileWhereClause", strawberry.lazy("api.files")] | None = None,
    ) -> Optional[Annotated["File", strawberry.lazy("api.files")]]:
        """
        Given a list of ConsensusGenome IDs for a certain file type, return related Files
        """
        dataloader = info.context["sqlalchemy_loader"]
        mapper = inspect(db.ConsensusGenome)
        relationship = mapper.relationships[attr_name]
        return await dataloader.loader_for(relationship, where).load(getattr(root, f"{attr_name}_id"))  # type:ignore

    return load_files


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
class ConsensusGenomeWhereClauseMutations(TypedDict):
    id: UUIDComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class ConsensusGenomeWhereClause(TypedDict):
    taxon: Optional[Annotated["TaxonWhereClause", strawberry.lazy("api.types.taxon")]] | None
    sequencing_read: Optional[
        Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")]
    ] | None
    reference_genome: Optional[
        Annotated["ReferenceGenomeWhereClause", strawberry.lazy("api.types.reference_genome")]
    ] | None
    accession: Optional[Annotated["AccessionWhereClause", strawberry.lazy("api.types.accession")]] | None
    metrics: Optional[
        Annotated["MetricConsensusGenomeWhereClause", strawberry.lazy("api.types.metric_consensus_genome")]
    ] | None
    id: Optional[UUIDComparators] | None
    producing_run_id: Optional[UUIDComparators] | None
    owner_user_id: Optional[IntComparators] | None
    collection_id: Optional[IntComparators] | None
    created_at: Optional[DatetimeComparators] | None
    updated_at: Optional[DatetimeComparators] | None
    deleted_at: Optional[DatetimeComparators] | None


"""
Supported ORDER BY clause attributes
"""


@strawberry.input
class ConsensusGenomeOrderByClause(TypedDict):
    taxon: Optional[Annotated["TaxonOrderByClause", strawberry.lazy("api.types.taxon")]] | None
    sequencing_read: Optional[
        Annotated["SequencingReadOrderByClause", strawberry.lazy("api.types.sequencing_read")]
    ] | None
    reference_genome: Optional[
        Annotated["ReferenceGenomeOrderByClause", strawberry.lazy("api.types.reference_genome")]
    ] | None
    accession: Optional[Annotated["AccessionOrderByClause", strawberry.lazy("api.types.accession")]] | None
    metrics: Optional[
        Annotated["MetricConsensusGenomeOrderByClause", strawberry.lazy("api.types.metric_consensus_genome")]
    ] | None
    id: Optional[orderBy] | None
    producing_run_id: Optional[orderBy] | None
    owner_user_id: Optional[orderBy] | None
    collection_id: Optional[orderBy] | None
    created_at: Optional[orderBy] | None
    updated_at: Optional[orderBy] | None
    deleted_at: Optional[orderBy] | None


"""
Define ConsensusGenome type
"""


@strawberry.type
class ConsensusGenome(EntityInterface):
    taxon: Optional[Annotated["Taxon", strawberry.lazy("api.types.taxon")]] = load_taxon_rows  # type:ignore
    sequencing_read: Optional[
        Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]
    ] = load_sequencing_read_rows  # type:ignore
    reference_genome: Optional[
        Annotated["ReferenceGenome", strawberry.lazy("api.types.reference_genome")]
    ] = load_reference_genome_rows  # type:ignore
    accession: Optional[
        Annotated["Accession", strawberry.lazy("api.types.accession")]
    ] = load_accession_rows  # type:ignore
    sequence_id: Optional[strawberry.ID]
    sequence: Optional[Annotated["File", strawberry.lazy("api.files")]] = load_files_from("sequence")  # type: ignore
    metrics: Optional[
        Annotated["MetricConsensusGenome", strawberry.lazy("api.types.metric_consensus_genome")]
    ] = load_metric_consensus_genome_rows  # type:ignore
    intermediate_outputs_id: Optional[strawberry.ID]
    intermediate_outputs: Optional[Annotated["File", strawberry.lazy("api.files")]] = load_files_from("intermediate_outputs")  # type: ignore
    id: strawberry.ID
    producing_run_id: Optional[strawberry.ID] = None
    owner_user_id: int
    collection_id: Optional[int] = None
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None


"""
We need to add this to each Queryable type so that strawberry will accept either our
Strawberry type *or* a SQLAlchemy model instance as a valid response class from a resolver
"""
ConsensusGenome.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.ConsensusGenome or type(obj) == ConsensusGenome
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
class ConsensusGenomeNumericalColumns:
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class ConsensusGenomeMinMaxColumns:
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class ConsensusGenomeCountColumns(enum.Enum):
    taxon = "taxon"
    sequencingRead = "sequencing_read"
    referenceGenome = "reference_genome"
    accession = "accession"
    sequence = "sequence"
    metrics = "metrics"
    intermediateOutputs = "intermediate_outputs"
    id = "id"
    producingRunId = "producing_run_id"
    ownerUserId = "owner_user_id"
    collectionId = "collection_id"
    createdAt = "created_at"
    updatedAt = "updated_at"
    deletedAt = "deleted_at"


"""
All supported aggregation functions
"""


@strawberry.type
class ConsensusGenomeAggregateFunctions:
    # This is a hack to accept "distinct" and "columns" as arguments to "count"
    @strawberry.field
    def count(
        self, distinct: Optional[bool] = False, columns: Optional[ConsensusGenomeCountColumns] = None
    ) -> Optional[int]:
        # Count gets set with the proper value in the resolver, so we just return it here
        return self.count  # type: ignore

    sum: Optional[ConsensusGenomeNumericalColumns] = None
    avg: Optional[ConsensusGenomeNumericalColumns] = None
    stddev: Optional[ConsensusGenomeNumericalColumns] = None
    variance: Optional[ConsensusGenomeNumericalColumns] = None
    min: Optional[ConsensusGenomeMinMaxColumns] = None
    max: Optional[ConsensusGenomeMinMaxColumns] = None
    groupBy: Optional[ConsensusGenomeGroupByOptions] = None


"""
Wrapper around ConsensusGenomeAggregateFunctions
"""


@strawberry.type
class ConsensusGenomeAggregate:
    aggregate: Optional[list[ConsensusGenomeAggregateFunctions]] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class ConsensusGenomeCreateInput:
    taxon_id: Optional[strawberry.ID] = None
    sequencing_read_id: strawberry.ID
    reference_genome_id: Optional[strawberry.ID] = None
    accession_id: Optional[strawberry.ID] = None
    producing_run_id: Optional[strawberry.ID] = None
    collection_id: Optional[int] = None
    deleted_at: Optional[datetime.datetime] = None


@strawberry.input()
class ConsensusGenomeUpdateInput:
    deleted_at: Optional[datetime.datetime] = None


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_consensus_genomes(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[ConsensusGenomeWhereClause] = None,
    order_by: Optional[list[ConsensusGenomeOrderByClause]] = [],
    limit_offset: Optional[LimitOffsetClause] = None,
) -> typing.Sequence[ConsensusGenome]:
    """
    Resolve ConsensusGenome objects. Used for queries (see api/queries.py).
    """
    limit = limit_offset["limit"] if limit_offset and "limit" in limit_offset else None
    offset = limit_offset["offset"] if limit_offset and "offset" in limit_offset else None
    if offset and not limit:
        raise PlatformicsException("Cannot use offset without limit")
    return await get_db_rows(db.ConsensusGenome, session, cerbos_client, principal, where, order_by, CerbosAction.VIEW, limit, offset)  # type: ignore


def format_consensus_genome_aggregate_output(
    query_results: Sequence[RowMapping] | RowMapping,
) -> ConsensusGenomeAggregate:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    aggregate = []
    if type(query_results) is not list:
        query_results = [query_results]  # type: ignore
    for row in query_results:
        aggregate.append(format_consensus_genome_aggregate_row(row))
    return ConsensusGenomeAggregate(aggregate=aggregate)


def format_consensus_genome_aggregate_row(row: RowMapping) -> ConsensusGenomeAggregateFunctions:
    """
    Given a single row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = ConsensusGenomeAggregateFunctions()
    for key, value in row.items():
        # Key is either an aggregate function or a groupby key
        group_keys = key.split(".")
        aggregate = key.split("_", 1)
        if aggregate[0] not in aggregator_map.keys():
            # Turn list of groupby keys into nested objects
            if not getattr(output, "groupBy"):
                setattr(output, "groupBy", ConsensusGenomeGroupByOptions())
            group = build_consensus_genome_groupby_output(getattr(output, "groupBy"), group_keys, value)
            setattr(output, "groupBy", group)
        else:
            aggregate_name = aggregate[0]
            if aggregate_name == "count":
                output.count = value
            else:
                aggregator_fn, col_name = aggregate[0], aggregate[1]
                if not getattr(output, aggregator_fn):
                    if aggregate_name in ["min", "max"]:
                        setattr(output, aggregator_fn, ConsensusGenomeMinMaxColumns())
                    else:
                        setattr(output, aggregator_fn, ConsensusGenomeNumericalColumns())
                setattr(getattr(output, aggregator_fn), col_name, value)
    return output


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_consensus_genomes_aggregate(
    info: Info,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[ConsensusGenomeWhereClause] = None,
    # TODO: add support for groupby, limit/offset
) -> ConsensusGenomeAggregate:
    """
    Aggregate values for ConsensusGenome objects. Used for queries (see api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on, and groupby options if any were provided.
    # TODO: not sure why selected_fields is a list
    selections = info.selected_fields[0].selections[0].selections
    aggregate_selections = [selection for selection in selections if getattr(selection, "name") != "groupBy"]
    groupby_selections = [selection for selection in selections if getattr(selection, "name") == "groupBy"]
    groupby_selections = groupby_selections[0].selections if groupby_selections else []

    if not aggregate_selections:
        raise PlatformicsException("No aggregate functions selected")

    rows = await get_aggregate_db_rows(db.ConsensusGenome, session, cerbos_client, principal, where, aggregate_selections, [], groupby_selections)  # type: ignore
    aggregate_output = format_consensus_genome_aggregate_output(rows)
    return aggregate_output


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_consensus_genome(
    input: ConsensusGenomeCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> db.Entity:
    """
    Create a new ConsensusGenome object. Used for mutations (see api/mutations.py).
    """
    validated = ConsensusGenomeCreateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Validate that the user can read all of the entities they're linking to.
    # If we have any system_writable fields present, make sure that our auth'd user *is* a system user
    if not is_system_user:
        del params["producing_run_id"]
        del params["deleted_at"]
    # Validate that the user can create entities in this collection
    attr = {"collection_id": validated.collection_id, "owner_user_id": int(principal.id)}
    resource = Resource(id="NEW_ID", kind=db.ConsensusGenome.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise PlatformicsException("Unauthorized: Cannot create entity in this collection")

    # Validate that the user can read all of the entities they're linking to.
    # Check that taxon relationship is accessible.
    if validated.taxon_id:
        taxon = await get_db_rows(
            db.Taxon, session, cerbos_client, principal, {"id": {"_eq": validated.taxon_id}}, [], CerbosAction.VIEW
        )
        if not taxon:
            raise PlatformicsException("Unauthorized: taxon does not exist")
    # Check that sequencing_read relationship is accessible.
    if validated.sequencing_read_id:
        sequencing_read = await get_db_rows(
            db.SequencingRead,
            session,
            cerbos_client,
            principal,
            {"id": {"_eq": validated.sequencing_read_id}},
            [],
            CerbosAction.VIEW,
        )
        if not sequencing_read:
            raise PlatformicsException("Unauthorized: sequencing_read does not exist")
    # Check that reference_genome relationship is accessible.
    if validated.reference_genome_id:
        reference_genome = await get_db_rows(
            db.ReferenceGenome,
            session,
            cerbos_client,
            principal,
            {"id": {"_eq": validated.reference_genome_id}},
            [],
            CerbosAction.VIEW,
        )
        if not reference_genome:
            raise PlatformicsException("Unauthorized: reference_genome does not exist")
    # Check that accession relationship is accessible.
    if validated.accession_id:
        accession = await get_db_rows(
            db.Accession,
            session,
            cerbos_client,
            principal,
            {"id": {"_eq": validated.accession_id}},
            [],
            CerbosAction.VIEW,
        )
        if not accession:
            raise PlatformicsException("Unauthorized: accession does not exist")

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.ConsensusGenome(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_consensus_genome(
    input: ConsensusGenomeUpdateInput,
    where: ConsensusGenomeWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> Sequence[db.Entity]:
    """
    Update ConsensusGenome objects. Used for mutations (see api/mutations.py).
    """
    validated = ConsensusGenomeUpdateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise PlatformicsException("No fields to update")

    # Validate that the user can read all of the entities they're linking to.
    # If we have any system_writable fields present, make sure that our auth'd user *is* a system user
    if not is_system_user:
        raise PlatformicsException("Unauthorized: ConsensusGenome is not mutable")

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(db.ConsensusGenome, session, cerbos_client, principal, where, [], CerbosAction.UPDATE)
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
async def delete_consensus_genome(
    where: ConsensusGenomeWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Delete ConsensusGenome objects. Used for mutations (see api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(db.ConsensusGenome, session, cerbos_client, principal, where, [], CerbosAction.DELETE)
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
