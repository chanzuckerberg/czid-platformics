from abc import ABC
import asyncio
from datetime import datetime
from dataclasses import dataclass, field, fields
import enum
import os
import sys
from typing import Generic, Optional
import typing
from uuid import UUID

from semver import Version
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


ENTITY_SERVICE_URL = os.environ["ENTITY_SERVICE_URL"]
ENTITY_SERVICE_AUTH_TOKEN = os.environ["ENTITY_SERVICE_AUTH_TOKEN"]


def _snake_to_camel(s: str) -> str:
    title = "".join(word.title() for word in s.split("_"))
    return title[0].lower() + title[1:]


_type_name_to_graphql_type = {
    "str": "String",
    "int": "Int",
    "float": "Float",
    "bool": "Boolean",
    "Optional": "Optional",
}


@dataclass
class Entity(ABC):
    entity_id: Optional[UUID] = field(default_factory=lambda: None, init=False)
    version: Optional[Version] = field(default_factory=lambda: Version(0), init=False)

    def _mutation_name(self) -> str:
        return f"create{self.__class__.__name__}"

    def _fields(self) -> typing.Iterator:
        for entity_field in fields(self):
            if entity_field.name in ["entity_id", "version"]:
                continue
            yield entity_field

    def gql_create_mutation(self) -> str:
        field_name_types = []
        for entity_field in self._fields():
            if entity_field.type.__name__ == "EntityReference":
                field_name_types.append((entity_field.metadata["id_name"], "UUID"))
                continue
            field_name_types.append(
                (_snake_to_camel(entity_field.name), _type_name_to_graphql_type[entity_field.type.__name__])
            )

        field_name_types.append(("producingRunId", "Int"))
        field_name_types.append(("ownerUserId", "Int"))
        field_name_types.append(("collectionId", "Int"))

        type_signature = ", ".join([f"${field_name}: {field_type}!" for field_name, field_type in field_name_types])
        variable_signature = ", ".join([f"{field_name}: ${field_name}" for field_name, _ in field_name_types])
        return f"""
            mutation Create{self.__class__.__name__}({type_signature}) {'{'}
                {self._mutation_name()}({variable_signature}) {'{'}
                    id
                {'}'}
            {'}'}
        """

    def gql_variables(self) -> dict:
        variables = {}
        for entity_field in self._fields():
            if entity_field.type.__name__ == "EntityReference":
                variables[entity_field.metadata["id_name"]] = getattr(self, entity_field.name).entity_id
                continue
            variables[_snake_to_camel(entity_field.name)] = getattr(self, entity_field.name)

        return variables

    def get_dependent_entities(self) -> typing.Iterator:
        for entity_field in fields(self):
            if entity_field.type.__name__ == "EntityReference":
                entity_ref: EntityReference = getattr(self, entity_field.name)
                yield entity_ref

    async def create_if_not_exists(self, user_id: int, collection_id: int, client: Client) -> None:
        if self.entity_id:
            return

        dependent_entity_futures = []
        for entity_ref in self.get_dependent_entities():
            dependent_entity_futures.append(entity_ref.create_if_not_exists(user_id, collection_id, client))
        await asyncio.gather(*dependent_entity_futures)

        print(self.gql_create_mutation(), file=sys.stderr)
        variables = self.gql_variables()
        variables["userId"] = user_id
        variables["collectionId"] = collection_id
        response = await client.execute_async(gql(self.gql_create_mutation()), variable_values=variables)
        entity_id = response.get(self._mutation_name(), {}).get("id")
        self.entity_id = entity_id


T = typing.TypeVar("T", bound=Entity)


@dataclass
class EntityReference(Generic[T]):
    entity_id: Optional[UUID] = field(default_factory=lambda: None)
    entity: Optional[T] = field(default_factory=lambda: None)

    async def create_if_not_exists(self, user_id: int, collection_id: int, client: Client) -> None:
        if self.entity_id:
            return
        if self.entity is None:
            raise ValueError("EntityReference has no entity")
        await self.entity.create_if_not_exists(user_id, collection_id, client)
        self.entity_id = self.entity.entity_id

    def exists(self) -> bool:
        return self.entity_id is not None

    async def load(self) -> T:
        raise Exception("Not implemented")


class FileStatus(enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PENDING = "PENDING"


@dataclass
class File:
    entity_field_name: str
    entity: EntityReference[Entity] = field(metadata={"id_name": "entityId"})
    status: FileStatus
    protocol: str
    namespace: str
    path: str
    file_format: str
    compression_type: Optional[str]
    size: Optional[int]


class FileReference:
    file_id: Optional[UUID]
    file: Optional[File]

    async def load(self) -> File:
        raise Exception("Not implemented")


@dataclass
class GenomicRange(Entity):
    reference_genome: EntityReference["ReferenceGenome"]
    file: FileReference
    consensus_genomes: list[EntityReference["ConsensusGenome"]]


@dataclass
class MetricConsensusGenome(Entity):
    coverage_depth: Optional[int]
    reference_genome_length: Optional[int]
    percent_genome_called: Optional[int]
    percent_identity: Optional[int]
    gc_percent: Optional[int]
    total_reads: Optional[int]
    mapped_reads: Optional[int]
    ref_snps: Optional[int]
    n_actg: Optional[int]
    n_missing: Optional[int]
    n_ambiguous: Optional[int]
    consensus_genome: EntityReference["ConsensusGenome"] = field(metadata={"id_name": "consensusGenomeId"})
    coverage_viz_summary_file: FileReference = field(metadata={"id_name": "coverageVizSummaryFileId"})


@dataclass
class ConsensusGenome(Entity):
    is_reverse_complement: bool
    taxon: EntityReference["Taxon"] = field(metadata={"id_name": "taxonId"})
    sequence_read: EntityReference["SequencingRead"] = field(metadata={"id_name": "sequenceReadId"})
    genomic_range: EntityReference[GenomicRange] = field(metadata={"id_name": "genomicRangeId"})
    reference_genome: EntityReference["ReferenceGenome"] = field(metadata={"id_name": "referenceGenomeId"})
    sequence: FileReference = field(metadata={"id_name": "sequenceId"})
    intermediate_outputs: FileReference = field(metadata={"id_name": "intermediateOutputsId"})
    metrics: list[EntityReference[MetricConsensusGenome]] 


@dataclass
class Contig(Entity):
    sequence: str
    sequencing_read: Optional[EntityReference["SequencingRead"]] = field(metadata={"id_name": "sequencingReadId"})


@dataclass
class CoverageViz(Entity):
    accession_id: str
    coverage_viz_file: FileReference = field(metadata={"id_name": "coverageVizId"})


@dataclass
class MetadataField(Entity):
    field_group: list[EntityReference["MetadataFieldProject"]] = field(metadata={"id_name": "metadataFieldId"})
    field_name: str
    description: str
    field_type: str
    is_required: bool
    options: Optional[str]
    default_value: Optional[str]
    metadatas: list[EntityReference["Metadatum"]]


@dataclass
class MetadataFieldProject(Entity):
    project_id: int
    metadata_field: EntityReference[MetadataField] = field(metadata={"id_name": "metadataFieldId"})


@dataclass
class Metadatum(Entity):
    sample: EntityReference["Sample"] = field(metadata={"id_name": "sampleId"})
    metadata_field: EntityReference[MetadataField] = field(metadata={"id_name": "metadataFieldId"})
    value: str


@dataclass
class ReferenceGenome(Entity):
    file: FileReference = field(metadata={"id_name": "fileId"})
    file_index: Optional[FileReference] = field(metadata={"id_name": "fileIndexId"})
    name: str
    description: str
    taxon: EntityReference["Taxon"] = field(metadata={"id_name": "taxonId"})
    accession_id: Optional[str]
    sequence_alignment_indices: list[EntityReference["SequenceAlignmentIndex"]]
    consensus_genomes: list[EntityReference[ConsensusGenome]]
    genomic_ranges: list[EntityReference[GenomicRange]]


@dataclass
class Sample(Entity):
    name: str
    sample_type: str
    water_control: bool
    collection_date: Optional[datetime]
    collection_location: str
    description: Optional[str]
    host_taxon: EntityReference["Taxon"] = field(metadata={"id_name": "hostTaxonId"})
    sequencing_reads: list[EntityReference["SequencingRead"]] = field(metadata={"id_name": "sampleId"})
    metadatas: list[EntityReference[Metadatum]]


class AlignmentTool(enum.Enum):
    bowtie2 = "bowtie2"
    minimap2 = "minimap2"
    ncbi = "ncbi"


@dataclass
class SequenceAlignmentIndex(Entity):
    index_file: FileReference = field(metadata={"id_name": "indexFileId"})
    reference_genome: EntityReference[ReferenceGenome] = field(metadata={"id_name": "referenceGenomeId"})
    tool: AlignmentTool


class NucleicAcid(enum.Enum):
    RNA = "RNA"
    DNA = "DNA"


class SequencingTechnology(enum.Enum):
    Illumina = "Illumina"
    Nanopore = "Nanopore"


class SequencingProtocol(enum.Enum):
    MNGS = "MNGS"
    TARGETED = "TARGETED"
    MSSPE = "MSSPE"


@dataclass
class SequencingRead(Entity):
    sample: Optional[EntityReference[Sample]] = field(metadata={"id_name": "sampleId"})
    protocol: SequencingProtocol
    r1_file: FileReference = field(metadata={"id_name": "r1FileId"})
    r2_file: Optional[FileReference] = field(metadata={"id_name": "r2FileId"})
    techonology: SequencingTechnology
    nucleic_acid: NucleicAcid
    has_ercc: bool
    taxon: Optional[EntityReference["Taxon"]] = field(metadata={"id_name": "taxonId"})
    primer_file: Optional[FileReference] = field(metadata={"id_name": "primerFileId"})
    consensus_genomes: list[EntityReference[ConsensusGenome]]
    contigs: list[EntityReference[Contig]]


class TaxonLevel(enum.Enum):
    species = "species"
    genus = "genus"
    family = "family"


@dataclass
class Taxon(Entity):
    wikipedia_id: Optional[str]
    description: Optional[str]
    common_name: Optional[str]
    name: str
    is_phage: bool
    upstream_database: EntityReference["UpstreamDatabase"] = field(metadata={"id_name": "upstreamDatabaseId"})
    upstream_database_identifier: str
    level: TaxonLevel
    tax_id: int
    tax_id_parent: int
    tax_id_species: int
    tax_id_genus: int
    tax_id_family: int
    tax_id_order: int
    tax_id_class: int
    tax_id_phylum: int
    tax_id_kingdom: int
    consensus_genomes: list[EntityReference[ConsensusGenome]]
    reference_genomes: list[EntityReference[ReferenceGenome]]
    sequencing_reads: list[EntityReference[SequencingRead]]
    samples: list[EntityReference[Sample]]


@dataclass
class UpstreamDatabase(Entity):
    name: str
    taxa: list[EntityReference[Taxon]]


async def create_entities(user_id: int, collection_id: int, entities: list[Entity]) -> None:
    headers = {"Authorization": f"Bearer {ENTITY_SERVICE_AUTH_TOKEN}"}
    transport = AIOHTTPTransport(url=ENTITY_SERVICE_URL, headers=headers)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    futures = []
    for entity in entities:
        futures.append(entity.create_if_not_exists(user_id, collection_id, client))
    await asyncio.gather(*futures)
