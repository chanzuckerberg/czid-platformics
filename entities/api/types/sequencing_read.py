"""
GraphQL type for SequencingRead

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
from api.validators.sequencing_read import SequencingReadCreateInputValidator, SequencingReadUpdateInputValidator
from api.files import File, FileWhereClause
from api.helpers.sequencing_read import SequencingReadGroupByOptions, build_sequencing_read_groupby_output
from api.types.entities import EntityInterface
from api.types.consensus_genome import ConsensusGenomeAggregate, format_consensus_genome_aggregate_output
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
from support.enums import SequencingProtocol, SequencingTechnology, NucleicAcid

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.sample import SampleOrderByClause, SampleWhereClause, Sample
    from api.types.taxon import TaxonOrderByClause, TaxonWhereClause, Taxon
    from api.types.genomic_range import GenomicRangeOrderByClause, GenomicRangeWhereClause, GenomicRange
    from api.types.consensus_genome import ConsensusGenomeOrderByClause, ConsensusGenomeWhereClause, ConsensusGenome

    pass
else:
    SampleWhereClause = "SampleWhereClause"
    Sample = "Sample"
    SampleOrderByClause = "SampleOrderByClause"
    TaxonWhereClause = "TaxonWhereClause"
    Taxon = "Taxon"
    TaxonOrderByClause = "TaxonOrderByClause"
    GenomicRangeWhereClause = "GenomicRangeWhereClause"
    GenomicRange = "GenomicRange"
    GenomicRangeOrderByClause = "GenomicRangeOrderByClause"
    ConsensusGenomeWhereClause = "ConsensusGenomeWhereClause"
    ConsensusGenome = "ConsensusGenome"
    ConsensusGenomeOrderByClause = "ConsensusGenomeOrderByClause"
    pass


"""
------------------------------------------------------------------------------
Dataloaders
------------------------------------------------------------------------------
These are batching functions for loading related objects to avoid N+1 queries.
"""


@strawberry.field
async def load_sample_rows(
    root: "SequencingRead",
    info: Info,
    where: Annotated["SampleWhereClause", strawberry.lazy("api.types.sample")] | None = None,
    order_by: Optional[list[Annotated["SampleOrderByClause", strawberry.lazy("api.types.sample")]]] = [],
) -> Optional[Annotated["Sample", strawberry.lazy("api.types.sample")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.SequencingRead)
    relationship = mapper.relationships["sample"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.sample_id)  # type:ignore


@strawberry.field
async def load_taxon_rows(
    root: "SequencingRead",
    info: Info,
    where: Annotated["TaxonWhereClause", strawberry.lazy("api.types.taxon")] | None = None,
    order_by: Optional[list[Annotated["TaxonOrderByClause", strawberry.lazy("api.types.taxon")]]] = [],
) -> Optional[Annotated["Taxon", strawberry.lazy("api.types.taxon")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.SequencingRead)
    relationship = mapper.relationships["taxon"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.taxon_id)  # type:ignore


@strawberry.field
async def load_genomic_range_rows(
    root: "SequencingRead",
    info: Info,
    where: Annotated["GenomicRangeWhereClause", strawberry.lazy("api.types.genomic_range")] | None = None,
    order_by: Optional[list[Annotated["GenomicRangeOrderByClause", strawberry.lazy("api.types.genomic_range")]]] = [],
) -> Optional[Annotated["GenomicRange", strawberry.lazy("api.types.genomic_range")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.SequencingRead)
    relationship = mapper.relationships["primer_file"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.primer_file_id)  # type:ignore


@relay.connection(
    relay.ListConnection[Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]]  # type:ignore
)
async def load_consensus_genome_rows(
    root: "SequencingRead",
    info: Info,
    where: Annotated["ConsensusGenomeWhereClause", strawberry.lazy("api.types.consensus_genome")] | None = None,
    order_by: Optional[
        list[Annotated["ConsensusGenomeOrderByClause", strawberry.lazy("api.types.consensus_genome")]]
    ] = [],
) -> Sequence[Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.SequencingRead)
    relationship = mapper.relationships["consensus_genomes"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.id)  # type:ignore


@strawberry.field
async def load_consensus_genome_aggregate_rows(
    root: "SequencingRead",
    info: Info,
    where: Annotated["ConsensusGenomeWhereClause", strawberry.lazy("api.types.consensus_genome")] | None = None,
) -> Optional[Annotated["ConsensusGenomeAggregate", strawberry.lazy("api.types.consensus_genome")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.SequencingRead)
    relationship = mapper.relationships["consensus_genomes"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    # Aggregate queries always return a single row, so just grab the first one
    result = rows[0] if rows else None
    aggregate_output = format_consensus_genome_aggregate_output(result)
    return aggregate_output


"""
------------------------------------------------------------------------------
Dataloader for File object
------------------------------------------------------------------------------
"""


def load_files_from(attr_name: str) -> Callable:
    @strawberry.field
    async def load_files(
        root: "SequencingRead",
        info: Info,
        where: Annotated["FileWhereClause", strawberry.lazy("api.files")] | None = None,
    ) -> Optional[Annotated["File", strawberry.lazy("api.files")]]:
        """
        Given a list of SequencingRead IDs for a certain file type, return related Files
        """
        dataloader = info.context["sqlalchemy_loader"]
        mapper = inspect(db.SequencingRead)
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
class SequencingReadWhereClauseMutations(TypedDict):
    id: UUIDComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class SequencingReadWhereClause(TypedDict):
    sample: Optional[Annotated["SampleWhereClause", strawberry.lazy("api.types.sample")]] | None
    protocol: Optional[EnumComparators[SequencingProtocol]] | None
    technology: Optional[EnumComparators[SequencingTechnology]] | None
    nucleic_acid: Optional[EnumComparators[NucleicAcid]] | None
    clearlabs_export: Optional[BoolComparators] | None
    medaka_model: Optional[StrComparators] | None
    taxon: Optional[Annotated["TaxonWhereClause", strawberry.lazy("api.types.taxon")]] | None
    primer_file: Optional[Annotated["GenomicRangeWhereClause", strawberry.lazy("api.types.genomic_range")]] | None
    consensus_genomes: Optional[
        Annotated["ConsensusGenomeWhereClause", strawberry.lazy("api.types.consensus_genome")]
    ] | None
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
class SequencingReadOrderByClause(TypedDict):
    sample: Optional[Annotated["SampleOrderByClause", strawberry.lazy("api.types.sample")]] | None
    protocol: Optional[orderBy] | None
    technology: Optional[orderBy] | None
    nucleic_acid: Optional[orderBy] | None
    clearlabs_export: Optional[orderBy] | None
    medaka_model: Optional[orderBy] | None
    taxon: Optional[Annotated["TaxonOrderByClause", strawberry.lazy("api.types.taxon")]] | None
    primer_file: Optional[Annotated["GenomicRangeOrderByClause", strawberry.lazy("api.types.genomic_range")]] | None
    id: Optional[orderBy] | None
    producing_run_id: Optional[orderBy] | None
    owner_user_id: Optional[orderBy] | None
    collection_id: Optional[orderBy] | None
    created_at: Optional[orderBy] | None
    updated_at: Optional[orderBy] | None


"""
Define SequencingRead type
"""


@strawberry.type
class SequencingRead(EntityInterface):
    sample: Optional[Annotated["Sample", strawberry.lazy("api.types.sample")]] = load_sample_rows  # type:ignore
    protocol: Optional[SequencingProtocol] = None
    r1_file_id: Optional[strawberry.ID]
    r1_file: Optional[Annotated["File", strawberry.lazy("api.files")]] = load_files_from("r1_file")  # type: ignore
    r2_file_id: Optional[strawberry.ID]
    r2_file: Optional[Annotated["File", strawberry.lazy("api.files")]] = load_files_from("r2_file")  # type: ignore
    technology: SequencingTechnology
    nucleic_acid: NucleicAcid
    clearlabs_export: bool
    medaka_model: Optional[str] = None
    taxon: Optional[Annotated["Taxon", strawberry.lazy("api.types.taxon")]] = load_taxon_rows  # type:ignore
    primer_file: Optional[
        Annotated["GenomicRange", strawberry.lazy("api.types.genomic_range")]
    ] = load_genomic_range_rows  # type:ignore
    consensus_genomes: Sequence[
        Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]
    ] = load_consensus_genome_rows  # type:ignore
    consensus_genomes_aggregate: Optional[
        Annotated["ConsensusGenomeAggregate", strawberry.lazy("api.types.consensus_genome")]
    ] = load_consensus_genome_aggregate_rows  # type:ignore
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
SequencingRead.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.SequencingRead or type(obj) == SequencingRead
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
class SequencingReadNumericalColumns:
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class SequencingReadMinMaxColumns:
    medaka_model: Optional[str] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class SequencingReadCountColumns(enum.Enum):
    sample = "sample"
    protocol = "protocol"
    r1_file = "r1_file"
    r2_file = "r2_file"
    technology = "technology"
    nucleic_acid = "nucleic_acid"
    clearlabs_export = "clearlabs_export"
    medaka_model = "medaka_model"
    taxon = "taxon"
    primer_file = "primer_file"
    consensus_genomes = "consensus_genomes"
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
class SequencingReadAggregateFunctions:
    # This is a hack to accept "distinct" and "columns" as arguments to "count"
    @strawberry.field
    def count(
        self, distinct: Optional[bool] = False, columns: Optional[SequencingReadCountColumns] = None
    ) -> Optional[int]:
        # Count gets set with the proper value in the resolver, so we just return it here
        return self.count  # type: ignore

    sum: Optional[SequencingReadNumericalColumns] = None
    avg: Optional[SequencingReadNumericalColumns] = None
    stddev: Optional[SequencingReadNumericalColumns] = None
    variance: Optional[SequencingReadNumericalColumns] = None
    min: Optional[SequencingReadMinMaxColumns] = None
    max: Optional[SequencingReadMinMaxColumns] = None
    groupBy: Optional[SequencingReadGroupByOptions] = None


"""
Wrapper around SequencingReadAggregateFunctions
"""


@strawberry.type
class SequencingReadAggregate:
    aggregate: Optional[list[SequencingReadAggregateFunctions]] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class SequencingReadCreateInput:
    sample_id: Optional[strawberry.ID] = None
    protocol: Optional[SequencingProtocol] = None
    technology: SequencingTechnology
    nucleic_acid: NucleicAcid
    clearlabs_export: bool
    medaka_model: Optional[str] = None
    taxon_id: Optional[strawberry.ID] = None
    primer_file_id: Optional[strawberry.ID] = None
    producing_run_id: Optional[strawberry.ID] = None
    collection_id: int


@strawberry.input()
class SequencingReadUpdateInput:
    nucleic_acid: Optional[NucleicAcid] = None
    clearlabs_export: Optional[bool] = None
    medaka_model: Optional[str] = None


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_sequencing_reads(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[SequencingReadWhereClause] = None,
    order_by: Optional[list[SequencingReadOrderByClause]] = [],
) -> typing.Sequence[SequencingRead]:
    """
    Resolve SequencingRead objects. Used for queries (see api/queries.py).
    """
    return await get_db_rows(db.SequencingRead, session, cerbos_client, principal, where, order_by)  # type: ignore


def format_sequencing_read_aggregate_output(
    query_results: Sequence[RowMapping] | RowMapping,
) -> SequencingReadAggregate:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    aggregate = []
    if type(query_results) is not list:
        query_results = [query_results]  # type: ignore
    for row in query_results:
        aggregate.append(format_sequencing_read_aggregate_row(row))
    return SequencingReadAggregate(aggregate=aggregate)


def format_sequencing_read_aggregate_row(row: RowMapping) -> SequencingReadAggregateFunctions:
    """
    Given a single row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = SequencingReadAggregateFunctions()
    for key, value in row.items():
        # Key is either an aggregate function or a groupby key
        group_keys = key.split(".")
        aggregate = key.split("_", 1)
        if aggregate[0] not in aggregator_map.keys():
            # Turn list of groupby keys into nested objects
            if not getattr(output, "groupBy"):
                setattr(output, "groupBy", SequencingReadGroupByOptions())
            group = build_sequencing_read_groupby_output(getattr(output, "groupBy"), group_keys, value)
            setattr(output, "groupBy", group)
        else:
            aggregate_name = aggregate[0]
            if aggregate_name == "count":
                output.count = value
            else:
                aggregator_fn, col_name = aggregate[0], aggregate[1]
                if not getattr(output, aggregator_fn):
                    if aggregate_name in ["min", "max"]:
                        setattr(output, aggregator_fn, SequencingReadMinMaxColumns())
                    else:
                        setattr(output, aggregator_fn, SequencingReadNumericalColumns())
                setattr(getattr(output, aggregator_fn), col_name, value)
    return output


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_sequencing_reads_aggregate(
    info: Info,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[SequencingReadWhereClause] = None,
) -> SequencingReadAggregate:
    """
    Aggregate values for SequencingRead objects. Used for queries (see api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on, and groupby options if any were provided.
    # TODO: not sure why selected_fields is a list
    selections = info.selected_fields[0].selections[0].selections
    aggregate_selections = [selection for selection in selections if getattr(selection, "name") != "groupBy"]
    groupby_selections = [selection for selection in selections if getattr(selection, "name") == "groupBy"]
    groupby_selections = groupby_selections[0].selections if groupby_selections else []

    if not aggregate_selections:
        raise Exception("No aggregate functions selected")

    rows = await get_aggregate_db_rows(db.SequencingRead, session, cerbos_client, principal, where, aggregate_selections, [], groupby_selections)  # type: ignore
    aggregate_output = format_sequencing_read_aggregate_output(rows)
    return aggregate_output


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_sequencing_read(
    input: SequencingReadCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> db.Entity:
    """
    Create a new SequencingRead object. Used for mutations (see api/mutations.py).
    """
    validated = SequencingReadCreateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Validate that the user can read all of the entities they're linking to.
    # If we have any system_writable fields present, make sure that our auth'd user *is* a system user
    if not is_system_user:
        del params["producing_run_id"]
    # Validate that the user can create entities in this collection
    attr = {"collection_id": validated.collection_id}
    resource = Resource(id="NEW_ID", kind=db.SequencingRead.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise PlatformicsException("Unauthorized: Cannot create entity in this collection")

    # Validate that the user can read all of the entities they're linking to.
    # Check that sample relationship is accessible.
    if validated.sample_id:
        sample = await get_db_rows(
            db.Sample, session, cerbos_client, principal, {"id": {"_eq": validated.sample_id}}, [], CerbosAction.VIEW
        )
        if not sample:
            raise PlatformicsException("Unauthorized: sample does not exist")
    # Check that taxon relationship is accessible.
    if validated.taxon_id:
        taxon = await get_db_rows(
            db.Taxon, session, cerbos_client, principal, {"id": {"_eq": validated.taxon_id}}, [], CerbosAction.VIEW
        )
        if not taxon:
            raise PlatformicsException("Unauthorized: taxon does not exist")
    # Check that primer_file relationship is accessible.
    if validated.primer_file_id:
        primer_file = await get_db_rows(
            db.GenomicRange,
            session,
            cerbos_client,
            principal,
            {"id": {"_eq": validated.primer_file_id}},
            [],
            CerbosAction.VIEW,
        )
        if not primer_file:
            raise PlatformicsException("Unauthorized: primer_file does not exist")

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.SequencingRead(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_sequencing_read(
    input: SequencingReadUpdateInput,
    where: SequencingReadWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> Sequence[db.Entity]:
    """
    Update SequencingRead objects. Used for mutations (see api/mutations.py).
    """
    validated = SequencingReadUpdateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise PlatformicsException("No fields to update")

    # Validate that the user can read all of the entities they're linking to.

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(db.SequencingRead, session, cerbos_client, principal, where, [], CerbosAction.UPDATE)
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
async def delete_sequencing_read(
    where: SequencingReadWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Delete SequencingRead objects. Used for mutations (see api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(db.SequencingRead, session, cerbos_client, principal, where, [], CerbosAction.DELETE)
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
