"""
GraphQL type for Taxon

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
from api.validators.taxon import TaxonCreateInputValidator, TaxonUpdateInputValidator
from api.helpers.taxon import TaxonGroupByOptions, build_taxon_groupby_output
from api.types.entities import EntityInterface
from api.types.consensus_genome import ConsensusGenomeAggregate, format_consensus_genome_aggregate_output
from api.types.sequencing_read import SequencingReadAggregate, format_sequencing_read_aggregate_output
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
from support.enums import TaxonLevel

E = typing.TypeVar("E", db.File, db.Entity)
T = typing.TypeVar("T")

if TYPE_CHECKING:
    from api.types.upstream_database import UpstreamDatabaseOrderByClause, UpstreamDatabaseWhereClause, UpstreamDatabase
    from api.types.consensus_genome import ConsensusGenomeOrderByClause, ConsensusGenomeWhereClause, ConsensusGenome
    from api.types.sequencing_read import SequencingReadOrderByClause, SequencingReadWhereClause, SequencingRead

    pass
else:
    UpstreamDatabaseWhereClause = "UpstreamDatabaseWhereClause"
    UpstreamDatabase = "UpstreamDatabase"
    UpstreamDatabaseOrderByClause = "UpstreamDatabaseOrderByClause"
    ConsensusGenomeWhereClause = "ConsensusGenomeWhereClause"
    ConsensusGenome = "ConsensusGenome"
    ConsensusGenomeOrderByClause = "ConsensusGenomeOrderByClause"
    SequencingReadWhereClause = "SequencingReadWhereClause"
    SequencingRead = "SequencingRead"
    SequencingReadOrderByClause = "SequencingReadOrderByClause"
    pass


"""
------------------------------------------------------------------------------
Dataloaders
------------------------------------------------------------------------------
These are batching functions for loading related objects to avoid N+1 queries.
"""


@strawberry.field
async def load_upstream_database_rows(
    root: "Taxon",
    info: Info,
    where: Annotated["UpstreamDatabaseWhereClause", strawberry.lazy("api.types.upstream_database")] | None = None,
    order_by: Optional[
        list[Annotated["UpstreamDatabaseOrderByClause", strawberry.lazy("api.types.upstream_database")]]
    ] = [],
) -> Optional[Annotated["UpstreamDatabase", strawberry.lazy("api.types.upstream_database")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Taxon)
    relationship = mapper.relationships["upstream_database"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.upstream_database_id)  # type:ignore


@relay.connection(
    relay.ListConnection[Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]]  # type:ignore
)
async def load_consensus_genome_rows(
    root: "Taxon",
    info: Info,
    where: Annotated["ConsensusGenomeWhereClause", strawberry.lazy("api.types.consensus_genome")] | None = None,
    order_by: Optional[
        list[Annotated["ConsensusGenomeOrderByClause", strawberry.lazy("api.types.consensus_genome")]]
    ] = [],
) -> Sequence[Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Taxon)
    relationship = mapper.relationships["consensus_genomes"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.id)  # type:ignore


@strawberry.field
async def load_consensus_genome_aggregate_rows(
    root: "Taxon",
    info: Info,
    where: Annotated["ConsensusGenomeWhereClause", strawberry.lazy("api.types.consensus_genome")] | None = None,
) -> Optional[Annotated["ConsensusGenomeAggregate", strawberry.lazy("api.types.consensus_genome")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Taxon)
    relationship = mapper.relationships["consensus_genomes"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    aggregate_output = format_consensus_genome_aggregate_output(rows)
    return aggregate_output


@relay.connection(
    relay.ListConnection[Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]]  # type:ignore
)
async def load_sequencing_read_rows(
    root: "Taxon",
    info: Info,
    where: Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")] | None = None,
    order_by: Optional[
        list[Annotated["SequencingReadOrderByClause", strawberry.lazy("api.types.sequencing_read")]]
    ] = [],
) -> Sequence[Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]]:
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Taxon)
    relationship = mapper.relationships["sequencing_reads"]
    return await dataloader.loader_for(relationship, where, order_by).load(root.id)  # type:ignore


@strawberry.field
async def load_sequencing_read_aggregate_rows(
    root: "Taxon",
    info: Info,
    where: Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")] | None = None,
) -> Optional[Annotated["SequencingReadAggregate", strawberry.lazy("api.types.sequencing_read")]]:
    selections = info.selected_fields[0].selections[0].selections
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.Taxon)
    relationship = mapper.relationships["sequencing_reads"]
    rows = await dataloader.aggregate_loader_for(relationship, where, selections).load(root.id)  # type:ignore
    aggregate_output = format_sequencing_read_aggregate_output(rows)
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
class TaxonWhereClauseMutations(TypedDict):
    id: UUIDComparators | None


"""
Supported WHERE clause attributes
"""


@strawberry.input
class TaxonWhereClause(TypedDict):
    wikipedia_id: Optional[StrComparators] | None
    description: Optional[StrComparators] | None
    common_name: Optional[StrComparators] | None
    name: Optional[StrComparators] | None
    is_phage: Optional[BoolComparators] | None
    upstream_database: Optional[
        Annotated["UpstreamDatabaseWhereClause", strawberry.lazy("api.types.upstream_database")]
    ] | None
    upstream_database_identifier: Optional[StrComparators] | None
    level: Optional[EnumComparators[TaxonLevel]] | None
    consensus_genomes: Optional[
        Annotated["ConsensusGenomeWhereClause", strawberry.lazy("api.types.consensus_genome")]
    ] | None
    sequencing_reads: Optional[
        Annotated["SequencingReadWhereClause", strawberry.lazy("api.types.sequencing_read")]
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
class TaxonOrderByClause(TypedDict):
    wikipedia_id: Optional[orderBy] | None
    description: Optional[orderBy] | None
    common_name: Optional[orderBy] | None
    name: Optional[orderBy] | None
    is_phage: Optional[orderBy] | None
    upstream_database: Optional[
        Annotated["UpstreamDatabaseOrderByClause", strawberry.lazy("api.types.upstream_database")]
    ] | None
    upstream_database_identifier: Optional[orderBy] | None
    level: Optional[orderBy] | None
    tax_parent: Optional[orderBy] | None
    tax_subspecies: Optional[orderBy] | None
    tax_species: Optional[orderBy] | None
    tax_genus: Optional[orderBy] | None
    tax_family: Optional[orderBy] | None
    tax_order: Optional[orderBy] | None
    tax_class: Optional[orderBy] | None
    tax_phylum: Optional[orderBy] | None
    tax_kingdom: Optional[orderBy] | None
    tax_superkingdom: Optional[orderBy] | None
    id: Optional[orderBy] | None
    producing_run_id: Optional[orderBy] | None
    owner_user_id: Optional[orderBy] | None
    collection_id: Optional[orderBy] | None
    created_at: Optional[orderBy] | None
    updated_at: Optional[orderBy] | None


"""
Define Taxon type
"""


@strawberry.type
class Taxon(EntityInterface):
    wikipedia_id: Optional[str] = None
    description: Optional[str] = None
    common_name: Optional[str] = None
    name: str
    is_phage: bool
    upstream_database: Optional[
        Annotated["UpstreamDatabase", strawberry.lazy("api.types.upstream_database")]
    ] = load_upstream_database_rows  # type:ignore
    upstream_database_identifier: str
    level: TaxonLevel
    consensus_genomes: Sequence[
        Annotated["ConsensusGenome", strawberry.lazy("api.types.consensus_genome")]
    ] = load_consensus_genome_rows  # type:ignore
    consensus_genomes_aggregate: Optional[
        Annotated["ConsensusGenomeAggregate", strawberry.lazy("api.types.consensus_genome")]
    ] = load_consensus_genome_aggregate_rows  # type:ignore
    sequencing_reads: Sequence[
        Annotated["SequencingRead", strawberry.lazy("api.types.sequencing_read")]
    ] = load_sequencing_read_rows  # type:ignore
    sequencing_reads_aggregate: Optional[
        Annotated["SequencingReadAggregate", strawberry.lazy("api.types.sequencing_read")]
    ] = load_sequencing_read_aggregate_rows  # type:ignore
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
Taxon.__strawberry_definition__.is_type_of = (  # type: ignore
    lambda obj, info: type(obj) == db.Taxon or type(obj) == Taxon
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
class TaxonNumericalColumns:
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None


"""
Define columns that support min/max aggregations
"""


@strawberry.type
class TaxonMinMaxColumns:
    wikipedia_id: Optional[str] = None
    description: Optional[str] = None
    common_name: Optional[str] = None
    name: Optional[str] = None
    upstream_database_identifier: Optional[str] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


"""
Define enum of all columns to support count and count(distinct) aggregations
"""


@strawberry.enum
class TaxonCountColumns(enum.Enum):
    wikipedia_id = "wikipedia_id"
    description = "description"
    common_name = "common_name"
    name = "name"
    is_phage = "is_phage"
    upstream_database = "upstream_database"
    upstream_database_identifier = "upstream_database_identifier"
    level = "level"
    tax_parent = "tax_parent"
    tax_subspecies = "tax_subspecies"
    tax_species = "tax_species"
    tax_genus = "tax_genus"
    tax_family = "tax_family"
    tax_order = "tax_order"
    tax_class = "tax_class"
    tax_phylum = "tax_phylum"
    tax_kingdom = "tax_kingdom"
    tax_superkingdom = "tax_superkingdom"
    consensus_genomes = "consensus_genomes"
    sequencing_reads = "sequencing_reads"
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
class TaxonAggregateFunctions:
    # This is a hack to accept "distinct" and "columns" as arguments to "count"
    @strawberry.field
    def count(self, distinct: Optional[bool] = False, columns: Optional[TaxonCountColumns] = None) -> Optional[int]:
        # Count gets set with the proper value in the resolver, so we just return it here
        return self.count  # type: ignore

    sum: Optional[TaxonNumericalColumns] = None
    avg: Optional[TaxonNumericalColumns] = None
    stddev: Optional[TaxonNumericalColumns] = None
    variance: Optional[TaxonNumericalColumns] = None
    min: Optional[TaxonMinMaxColumns] = None
    max: Optional[TaxonMinMaxColumns] = None
    groupBy: Optional[TaxonGroupByOptions] = None


"""
Wrapper around TaxonAggregateFunctions
"""


@strawberry.type
class TaxonAggregate:
    aggregate: Optional[list[TaxonAggregateFunctions]] = None


"""
------------------------------------------------------------------------------
Mutation types
------------------------------------------------------------------------------
"""


@strawberry.input()
class TaxonCreateInput:
    wikipedia_id: Optional[str] = None
    description: Optional[str] = None
    common_name: Optional[str] = None
    name: str
    is_phage: bool
    upstream_database_id: strawberry.ID
    upstream_database_identifier: str
    level: TaxonLevel
    tax_parent_id: Optional[strawberry.ID] = None
    tax_subspecies_id: Optional[strawberry.ID] = None
    tax_species_id: Optional[strawberry.ID] = None
    tax_genus_id: Optional[strawberry.ID] = None
    tax_family_id: Optional[strawberry.ID] = None
    tax_order_id: Optional[strawberry.ID] = None
    tax_class_id: Optional[strawberry.ID] = None
    tax_phylum_id: Optional[strawberry.ID] = None
    tax_kingdom_id: Optional[strawberry.ID] = None
    tax_superkingdom_id: Optional[strawberry.ID] = None
    producing_run_id: Optional[strawberry.ID] = None
    collection_id: int


@strawberry.input()
class TaxonUpdateInput:
    wikipedia_id: Optional[str] = None
    description: Optional[str] = None
    common_name: Optional[str] = None
    is_phage: Optional[bool] = None
    level: Optional[TaxonLevel] = None
    tax_parent_id: Optional[strawberry.ID] = None
    tax_subspecies_id: Optional[strawberry.ID] = None
    tax_species_id: Optional[strawberry.ID] = None
    tax_genus_id: Optional[strawberry.ID] = None
    tax_family_id: Optional[strawberry.ID] = None
    tax_order_id: Optional[strawberry.ID] = None
    tax_class_id: Optional[strawberry.ID] = None
    tax_phylum_id: Optional[strawberry.ID] = None
    tax_kingdom_id: Optional[strawberry.ID] = None
    tax_superkingdom_id: Optional[strawberry.ID] = None


"""
------------------------------------------------------------------------------
Utilities
------------------------------------------------------------------------------
"""


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_taxa(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[TaxonWhereClause] = None,
    order_by: Optional[list[TaxonOrderByClause]] = [],
) -> typing.Sequence[Taxon]:
    """
    Resolve Taxon objects. Used for queries (see api/queries.py).
    """
    return await get_db_rows(db.Taxon, session, cerbos_client, principal, where, order_by)  # type: ignore


def format_taxon_aggregate_output(query_results: Sequence[RowMapping] | RowMapping) -> TaxonAggregate:
    """
    Given a row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    aggregate = []
    if type(query_results) is not list:
        query_results = [query_results]  # type: ignore
    for row in query_results:
        aggregate.append(format_taxon_aggregate_row(row))
    return TaxonAggregate(aggregate=aggregate)


def format_taxon_aggregate_row(row: RowMapping) -> TaxonAggregateFunctions:
    """
    Given a single row from the DB containing the results of an aggregate query,
    format the results using the proper GraphQL types.
    """
    output = TaxonAggregateFunctions()
    for key, value in row.items():
        # Key is either an aggregate function or a groupby key
        group_keys = key.split(".")
        aggregate = key.split("_", 1)
        if aggregate[0] not in aggregator_map.keys():
            # Turn list of groupby keys into nested objects
            if not getattr(output, "groupBy"):
                setattr(output, "groupBy", TaxonGroupByOptions())
            group = build_taxon_groupby_output(getattr(output, "groupBy"), group_keys, value)
            setattr(output, "groupBy", group)
        else:
            aggregate_name = aggregate[0]
            if aggregate_name == "count":
                output.count = value
            else:
                aggregator_fn, col_name = aggregate[0], aggregate[1]
                if not getattr(output, aggregator_fn):
                    if aggregate_name in ["min", "max"]:
                        setattr(output, aggregator_fn, TaxonMinMaxColumns())
                    else:
                        setattr(output, aggregator_fn, TaxonNumericalColumns())
                setattr(getattr(output, aggregator_fn), col_name, value)
    return output


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_taxa_aggregate(
    info: Info,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: Optional[TaxonWhereClause] = None,
) -> TaxonAggregate:
    """
    Aggregate values for Taxon objects. Used for queries (see api/queries.py).
    """
    # Get the selected aggregate functions and columns to operate on, and groupby options if any were provided.
    # TODO: not sure why selected_fields is a list
    selections = info.selected_fields[0].selections[0].selections
    aggregate_selections = [selection for selection in selections if getattr(selection, "name") != "groupBy"]
    groupby_selections = [selection for selection in selections if getattr(selection, "name") == "groupBy"]
    groupby_selections = groupby_selections[0].selections if groupby_selections else []

    if not aggregate_selections:
        raise PlatformicsException("No aggregate functions selected")

    rows = await get_aggregate_db_rows(db.Taxon, session, cerbos_client, principal, where, aggregate_selections, [], groupby_selections)  # type: ignore
    aggregate_output = format_taxon_aggregate_output(rows)
    return aggregate_output


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_taxon(
    input: TaxonCreateInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> db.Entity:
    """
    Create a new Taxon object. Used for mutations (see api/mutations.py).
    """
    validated = TaxonCreateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Validate that the user can read all of the entities they're linking to.
    # If we have any system_writable fields present, make sure that our auth'd user *is* a system user
    if not is_system_user:
        del params["producing_run_id"]
    # Validate that the user can create entities in this collection
    attr = {"collection_id": validated.collection_id}
    resource = Resource(id="NEW_ID", kind=db.Taxon.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise PlatformicsException("Unauthorized: Cannot create entity in this collection")

    # Validate that the user can read all of the entities they're linking to.
    # Check that upstream_database relationship is accessible.
    if validated.upstream_database_id:
        upstream_database = await get_db_rows(
            db.UpstreamDatabase,
            session,
            cerbos_client,
            principal,
            {"id": {"_eq": validated.upstream_database_id}},
            [],
            CerbosAction.VIEW,
        )
        if not upstream_database:
            raise PlatformicsException("Unauthorized: upstream_database does not exist")
    # Check that tax_parent relationship is accessible.
    if validated.tax_parent_id:
        tax_parent = await get_db_rows(
            db.Taxon, session, cerbos_client, principal, {"id": {"_eq": validated.tax_parent_id}}, [], CerbosAction.VIEW
        )
        if not tax_parent:
            raise PlatformicsException("Unauthorized: tax_parent does not exist")
    # Check that tax_subspecies relationship is accessible.
    if validated.tax_subspecies_id:
        tax_subspecies = await get_db_rows(
            db.Taxon,
            session,
            cerbos_client,
            principal,
            {"id": {"_eq": validated.tax_subspecies_id}},
            [],
            CerbosAction.VIEW,
        )
        if not tax_subspecies:
            raise PlatformicsException("Unauthorized: tax_subspecies does not exist")
    # Check that tax_species relationship is accessible.
    if validated.tax_species_id:
        tax_species = await get_db_rows(
            db.Taxon,
            session,
            cerbos_client,
            principal,
            {"id": {"_eq": validated.tax_species_id}},
            [],
            CerbosAction.VIEW,
        )
        if not tax_species:
            raise PlatformicsException("Unauthorized: tax_species does not exist")
    # Check that tax_genus relationship is accessible.
    if validated.tax_genus_id:
        tax_genus = await get_db_rows(
            db.Taxon, session, cerbos_client, principal, {"id": {"_eq": validated.tax_genus_id}}, [], CerbosAction.VIEW
        )
        if not tax_genus:
            raise PlatformicsException("Unauthorized: tax_genus does not exist")
    # Check that tax_family relationship is accessible.
    if validated.tax_family_id:
        tax_family = await get_db_rows(
            db.Taxon, session, cerbos_client, principal, {"id": {"_eq": validated.tax_family_id}}, [], CerbosAction.VIEW
        )
        if not tax_family:
            raise PlatformicsException("Unauthorized: tax_family does not exist")
    # Check that tax_order relationship is accessible.
    if validated.tax_order_id:
        tax_order = await get_db_rows(
            db.Taxon, session, cerbos_client, principal, {"id": {"_eq": validated.tax_order_id}}, [], CerbosAction.VIEW
        )
        if not tax_order:
            raise PlatformicsException("Unauthorized: tax_order does not exist")
    # Check that tax_class relationship is accessible.
    if validated.tax_class_id:
        tax_class = await get_db_rows(
            db.Taxon, session, cerbos_client, principal, {"id": {"_eq": validated.tax_class_id}}, [], CerbosAction.VIEW
        )
        if not tax_class:
            raise PlatformicsException("Unauthorized: tax_class does not exist")
    # Check that tax_phylum relationship is accessible.
    if validated.tax_phylum_id:
        tax_phylum = await get_db_rows(
            db.Taxon, session, cerbos_client, principal, {"id": {"_eq": validated.tax_phylum_id}}, [], CerbosAction.VIEW
        )
        if not tax_phylum:
            raise PlatformicsException("Unauthorized: tax_phylum does not exist")
    # Check that tax_kingdom relationship is accessible.
    if validated.tax_kingdom_id:
        tax_kingdom = await get_db_rows(
            db.Taxon,
            session,
            cerbos_client,
            principal,
            {"id": {"_eq": validated.tax_kingdom_id}},
            [],
            CerbosAction.VIEW,
        )
        if not tax_kingdom:
            raise PlatformicsException("Unauthorized: tax_kingdom does not exist")
    # Check that tax_superkingdom relationship is accessible.
    if validated.tax_superkingdom_id:
        tax_superkingdom = await get_db_rows(
            db.Taxon,
            session,
            cerbos_client,
            principal,
            {"id": {"_eq": validated.tax_superkingdom_id}},
            [],
            CerbosAction.VIEW,
        )
        if not tax_superkingdom:
            raise PlatformicsException("Unauthorized: tax_superkingdom does not exist")

    # Save to DB
    params["owner_user_id"] = int(principal.id)
    new_entity = db.Taxon(**params)
    session.add(new_entity)
    await session.commit()
    return new_entity


@strawberry.mutation(extensions=[DependencyExtension()])
async def update_taxon(
    input: TaxonUpdateInput,
    where: TaxonWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    is_system_user: bool = Depends(is_system_user),
) -> Sequence[db.Entity]:
    """
    Update Taxon objects. Used for mutations (see api/mutations.py).
    """
    validated = TaxonUpdateInputValidator(**input.__dict__)
    params = validated.model_dump()

    # Need at least one thing to update
    num_params = len([x for x in params if params[x] is not None])
    if num_params == 0:
        raise PlatformicsException("No fields to update")

    # Validate that the user can read all of the entities they're linking to.
    # Check that tax_parent relationship is accessible.
    if validated.tax_parent_id:
        tax_parent = await get_db_rows(
            db.Taxon, session, cerbos_client, principal, {"id": {"_eq": validated.tax_parent_id}}, [], CerbosAction.VIEW
        )
        if not tax_parent:
            raise PlatformicsException("Unauthorized: tax_parent does not exist")
        params["tax_parent"] = tax_parent[0]
        del params["tax_parent_id"]
    # Check that tax_subspecies relationship is accessible.
    if validated.tax_subspecies_id:
        tax_subspecies = await get_db_rows(
            db.Taxon,
            session,
            cerbos_client,
            principal,
            {"id": {"_eq": validated.tax_subspecies_id}},
            [],
            CerbosAction.VIEW,
        )
        if not tax_subspecies:
            raise PlatformicsException("Unauthorized: tax_subspecies does not exist")
        params["tax_subspecies"] = tax_subspecies[0]
        del params["tax_subspecies_id"]
    # Check that tax_species relationship is accessible.
    if validated.tax_species_id:
        tax_species = await get_db_rows(
            db.Taxon,
            session,
            cerbos_client,
            principal,
            {"id": {"_eq": validated.tax_species_id}},
            [],
            CerbosAction.VIEW,
        )
        if not tax_species:
            raise PlatformicsException("Unauthorized: tax_species does not exist")
        params["tax_species"] = tax_species[0]
        del params["tax_species_id"]
    # Check that tax_genus relationship is accessible.
    if validated.tax_genus_id:
        tax_genus = await get_db_rows(
            db.Taxon, session, cerbos_client, principal, {"id": {"_eq": validated.tax_genus_id}}, [], CerbosAction.VIEW
        )
        if not tax_genus:
            raise PlatformicsException("Unauthorized: tax_genus does not exist")
        params["tax_genus"] = tax_genus[0]
        del params["tax_genus_id"]
    # Check that tax_family relationship is accessible.
    if validated.tax_family_id:
        tax_family = await get_db_rows(
            db.Taxon, session, cerbos_client, principal, {"id": {"_eq": validated.tax_family_id}}, [], CerbosAction.VIEW
        )
        if not tax_family:
            raise PlatformicsException("Unauthorized: tax_family does not exist")
        params["tax_family"] = tax_family[0]
        del params["tax_family_id"]
    # Check that tax_order relationship is accessible.
    if validated.tax_order_id:
        tax_order = await get_db_rows(
            db.Taxon, session, cerbos_client, principal, {"id": {"_eq": validated.tax_order_id}}, [], CerbosAction.VIEW
        )
        if not tax_order:
            raise PlatformicsException("Unauthorized: tax_order does not exist")
        params["tax_order"] = tax_order[0]
        del params["tax_order_id"]
    # Check that tax_class relationship is accessible.
    if validated.tax_class_id:
        tax_class = await get_db_rows(
            db.Taxon, session, cerbos_client, principal, {"id": {"_eq": validated.tax_class_id}}, [], CerbosAction.VIEW
        )
        if not tax_class:
            raise PlatformicsException("Unauthorized: tax_class does not exist")
        params["tax_class"] = tax_class[0]
        del params["tax_class_id"]
    # Check that tax_phylum relationship is accessible.
    if validated.tax_phylum_id:
        tax_phylum = await get_db_rows(
            db.Taxon, session, cerbos_client, principal, {"id": {"_eq": validated.tax_phylum_id}}, [], CerbosAction.VIEW
        )
        if not tax_phylum:
            raise PlatformicsException("Unauthorized: tax_phylum does not exist")
        params["tax_phylum"] = tax_phylum[0]
        del params["tax_phylum_id"]
    # Check that tax_kingdom relationship is accessible.
    if validated.tax_kingdom_id:
        tax_kingdom = await get_db_rows(
            db.Taxon,
            session,
            cerbos_client,
            principal,
            {"id": {"_eq": validated.tax_kingdom_id}},
            [],
            CerbosAction.VIEW,
        )
        if not tax_kingdom:
            raise PlatformicsException("Unauthorized: tax_kingdom does not exist")
        params["tax_kingdom"] = tax_kingdom[0]
        del params["tax_kingdom_id"]
    # Check that tax_superkingdom relationship is accessible.
    if validated.tax_superkingdom_id:
        tax_superkingdom = await get_db_rows(
            db.Taxon,
            session,
            cerbos_client,
            principal,
            {"id": {"_eq": validated.tax_superkingdom_id}},
            [],
            CerbosAction.VIEW,
        )
        if not tax_superkingdom:
            raise PlatformicsException("Unauthorized: tax_superkingdom does not exist")
        params["tax_superkingdom"] = tax_superkingdom[0]
        del params["tax_superkingdom_id"]

    # Fetch entities for update, if we have access to them
    entities = await get_db_rows(db.Taxon, session, cerbos_client, principal, where, [], CerbosAction.UPDATE)
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
async def delete_taxon(
    where: TaxonWhereClauseMutations,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> Sequence[db.Entity]:
    """
    Delete Taxon objects. Used for mutations (see api/mutations.py).
    """
    # Fetch entities for deletion, if we have access to them
    entities = await get_db_rows(db.Taxon, session, cerbos_client, principal, where, [], CerbosAction.DELETE)
    if len(entities) == 0:
        raise PlatformicsException("Unauthorized: Cannot delete entities")

    # Update DB
    for entity in entities:
        await session.delete(entity)
    await session.commit()
    return entities
