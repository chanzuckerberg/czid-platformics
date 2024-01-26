import sgqlc.types
import sgqlc.types.datetime
import sgqlc.types.relay


gql_schema = sgqlc.types.Schema()


# Unexport Node/PageInfo, let schema re-declare them
gql_schema -= sgqlc.types.relay.Node
gql_schema -= sgqlc.types.relay.PageInfo


########################################################################
# Scalars and Enumerations
########################################################################
Boolean = sgqlc.types.Boolean


class BulkDownloadCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "collection_id",
        "created_at",
        "deleted_at",
        "download_type",
        "entity_id",
        "file",
        "id",
        "owner_user_id",
        "producing_run_id",
        "updated_at",
    )


class BulkDownloadType(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("concatenate", "zip")


class ConsensusGenomeCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "collection_id",
        "created_at",
        "deleted_at",
        "entity_id",
        "id",
        "intermediate_outputs",
        "metrics",
        "owner_user_id",
        "producing_run_id",
        "reference_genome",
        "sequence",
        "sequence_read",
        "taxon",
        "updated_at",
    )


class ContigCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "collection_id",
        "created_at",
        "deleted_at",
        "entity_id",
        "id",
        "owner_user_id",
        "producing_run_id",
        "sequence",
        "sequencing_read",
        "updated_at",
    )


DateTime = sgqlc.types.datetime.DateTime


class FileAccessProtocol(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("s3",)


class FileStatus(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("FAILED", "PENDING", "SUCCESS")


Float = sgqlc.types.Float


class GenomicRangeCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "collection_id",
        "created_at",
        "deleted_at",
        "entity_id",
        "file",
        "id",
        "owner_user_id",
        "producing_run_id",
        "reference_genome",
        "sequencing_reads",
        "updated_at",
    )


class GlobalID(sgqlc.types.Scalar):
    __schema__ = gql_schema


class HostOrganismCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "collection_id",
        "created_at",
        "deleted_at",
        "entity_id",
        "host_filtering",
        "id",
        "name",
        "owner_user_id",
        "producing_run_id",
        "sequence",
        "updated_at",
        "version",
    )


ID = sgqlc.types.ID

Int = sgqlc.types.Int


class JSON(sgqlc.types.Scalar):
    __schema__ = gql_schema


class MetadatumCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "collection_id",
        "created_at",
        "deleted_at",
        "entity_id",
        "field_name",
        "id",
        "owner_user_id",
        "producing_run_id",
        "sample",
        "updated_at",
        "value",
    )


class MetricConsensusGenomeCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "collection_id",
        "consensus_genome",
        "coverage_bin_size",
        "coverage_breadth",
        "coverage_depth",
        "coverage_total_length",
        "coverage_viz",
        "created_at",
        "deleted_at",
        "entity_id",
        "gc_percent",
        "id",
        "mapped_reads",
        "n_actg",
        "n_ambiguous",
        "n_missing",
        "owner_user_id",
        "percent_genome_called",
        "percent_identity",
        "producing_run_id",
        "ref_snps",
        "reference_genome_length",
        "total_reads",
        "updated_at",
    )


class NucleicAcid(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("DNA", "RNA")


class PhylogeneticTreeCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "collection_id",
        "created_at",
        "deleted_at",
        "entity_id",
        "format",
        "id",
        "owner_user_id",
        "producing_run_id",
        "tree",
        "updated_at",
    )


class PhylogeneticTreeFormat(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("auspice_v1", "auspice_v2", "newick")


class ReferenceGenomeCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "accession_id",
        "collection_id",
        "consensus_genomes",
        "created_at",
        "deleted_at",
        "entity_id",
        "file",
        "genomic_ranges",
        "id",
        "owner_user_id",
        "producing_run_id",
        "taxon",
        "updated_at",
    )


class SampleCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "collection_date",
        "collection_id",
        "collection_location",
        "created_at",
        "deleted_at",
        "description",
        "entity_id",
        "host_taxon",
        "id",
        "metadatas",
        "name",
        "owner_user_id",
        "producing_run_id",
        "rails_sample_id",
        "sample_type",
        "sequencing_reads",
        "updated_at",
        "water_control",
    )


class SequencingProtocol(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "ampliseq",
        "artic",
        "artic_v3",
        "artic_v4",
        "artic_v5",
        "combined_msspe_artic",
        "covidseq",
        "easyseq",
        "midnight",
        "msspe",
        "snap",
        "varskip",
    )


class SequencingReadCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "collection_id",
        "consensus_genomes",
        "contigs",
        "created_at",
        "deleted_at",
        "entity_id",
        "id",
        "nucleic_acid",
        "owner_user_id",
        "primer_file",
        "producing_run_id",
        "protocol",
        "r1_file",
        "r2_file",
        "sample",
        "taxon",
        "technology",
        "updated_at",
    )


class SequencingTechnology(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("Illumina", "Nanopore")


String = sgqlc.types.String


class TaxonCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "collection_id",
        "common_name",
        "consensus_genomes",
        "created_at",
        "deleted_at",
        "description",
        "entity_id",
        "id",
        "is_phage",
        "level",
        "name",
        "owner_user_id",
        "producing_run_id",
        "reference_genomes",
        "samples",
        "sequencing_reads",
        "tax_class",
        "tax_family",
        "tax_genus",
        "tax_kingdom",
        "tax_order",
        "tax_parent",
        "tax_phylum",
        "tax_species",
        "tax_subspecies",
        "tax_superkingdom",
        "updated_at",
        "upstream_database",
        "upstream_database_identifier",
        "wikipedia_id",
    )


class TaxonLevel(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "level_class",
        "level_family",
        "level_genus",
        "level_kingdom",
        "level_order",
        "level_phylum",
        "level_species",
        "level_subspecies",
        "level_superkingdom",
    )


class UUID(sgqlc.types.Scalar):
    __schema__ = gql_schema


class UpstreamDatabaseCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "collection_id",
        "created_at",
        "deleted_at",
        "entity_id",
        "id",
        "name",
        "owner_user_id",
        "producing_run_id",
        "taxa",
        "updated_at",
    )


########################################################################
# Input Objects
########################################################################
class BoolComparators(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("_eq", "_neq", "_in", "_nin", "_gt", "_gte", "_lt", "_lte", "_is_null")
    _eq = sgqlc.types.Field(Int, graphql_name="_eq")
    _neq = sgqlc.types.Field(Int, graphql_name="_neq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Int)), graphql_name="_in")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Int)), graphql_name="_nin")
    _gt = sgqlc.types.Field(Int, graphql_name="_gt")
    _gte = sgqlc.types.Field(Int, graphql_name="_gte")
    _lt = sgqlc.types.Field(Int, graphql_name="_lt")
    _lte = sgqlc.types.Field(Int, graphql_name="_lte")
    _is_null = sgqlc.types.Field(Int, graphql_name="_is_null")


class BulkDownloadCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "download_type", "file_id")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    download_type = sgqlc.types.Field(sgqlc.types.non_null(BulkDownloadType), graphql_name="downloadType")
    file_id = sgqlc.types.Field(ID, graphql_name="fileId")


class BulkDownloadTypeEnumComparators(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("_eq", "_neq", "_in", "_nin", "_gt", "_gte", "_lt", "_lte", "_is_null")
    _eq = sgqlc.types.Field(BulkDownloadType, graphql_name="_eq")
    _neq = sgqlc.types.Field(BulkDownloadType, graphql_name="_neq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(BulkDownloadType)), graphql_name="_in")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(BulkDownloadType)), graphql_name="_nin")
    _gt = sgqlc.types.Field(BulkDownloadType, graphql_name="_gt")
    _gte = sgqlc.types.Field(BulkDownloadType, graphql_name="_gte")
    _lt = sgqlc.types.Field(BulkDownloadType, graphql_name="_lt")
    _lte = sgqlc.types.Field(BulkDownloadType, graphql_name="_lte")
    _is_null = sgqlc.types.Field(BulkDownloadType, graphql_name="_is_null")


class BulkDownloadUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "download_type", "file_id")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    download_type = sgqlc.types.Field(BulkDownloadType, graphql_name="downloadType")
    file_id = sgqlc.types.Field(ID, graphql_name="fileId")


class BulkDownloadWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id", "producing_run_id", "owner_user_id", "collection_id", "download_type")
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field("IntComparators", graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field("IntComparators", graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field("IntComparators", graphql_name="collectionId")
    download_type = sgqlc.types.Field(BulkDownloadTypeEnumComparators, graphql_name="downloadType")


class BulkDownloadWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")


class ConsensusGenomeCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "collection_id",
        "taxon_id",
        "sequence_read_id",
        "reference_genome_id",
        "sequence_id",
        "intermediate_outputs_id",
    )
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    taxon_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="taxonId")
    sequence_read_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="sequenceReadId")
    reference_genome_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="referenceGenomeId")
    sequence_id = sgqlc.types.Field(ID, graphql_name="sequenceId")
    intermediate_outputs_id = sgqlc.types.Field(ID, graphql_name="intermediateOutputsId")


class ConsensusGenomeUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "collection_id",
        "taxon_id",
        "sequence_read_id",
        "reference_genome_id",
        "sequence_id",
        "intermediate_outputs_id",
    )
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    taxon_id = sgqlc.types.Field(ID, graphql_name="taxonId")
    sequence_read_id = sgqlc.types.Field(ID, graphql_name="sequenceReadId")
    reference_genome_id = sgqlc.types.Field(ID, graphql_name="referenceGenomeId")
    sequence_id = sgqlc.types.Field(ID, graphql_name="sequenceId")
    intermediate_outputs_id = sgqlc.types.Field(ID, graphql_name="intermediateOutputsId")


class ConsensusGenomeWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "taxon",
        "sequence_read",
        "reference_genome",
        "metrics",
    )
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field("IntComparators", graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field("IntComparators", graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field("IntComparators", graphql_name="collectionId")
    taxon = sgqlc.types.Field("TaxonWhereClause", graphql_name="taxon")
    sequence_read = sgqlc.types.Field("SequencingReadWhereClause", graphql_name="sequenceRead")
    reference_genome = sgqlc.types.Field("ReferenceGenomeWhereClause", graphql_name="referenceGenome")
    metrics = sgqlc.types.Field("MetricConsensusGenomeWhereClause", graphql_name="metrics")


class ConsensusGenomeWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")


class ContigCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "sequencing_read_id", "sequence")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    sequencing_read_id = sgqlc.types.Field(ID, graphql_name="sequencingReadId")
    sequence = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="sequence")


class ContigUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "sequencing_read_id", "sequence")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    sequencing_read_id = sgqlc.types.Field(ID, graphql_name="sequencingReadId")
    sequence = sgqlc.types.Field(String, graphql_name="sequence")


class ContigWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id", "producing_run_id", "owner_user_id", "collection_id", "sequencing_read", "sequence")
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field("IntComparators", graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field("IntComparators", graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field("IntComparators", graphql_name="collectionId")
    sequencing_read = sgqlc.types.Field("SequencingReadWhereClause", graphql_name="sequencingRead")
    sequence = sgqlc.types.Field("StrComparators", graphql_name="sequence")


class ContigWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")


class DatetimeComparators(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("_eq", "_neq", "_in", "_nin", "_gt", "_gte", "_lt", "_lte", "_is_null")
    _eq = sgqlc.types.Field(DateTime, graphql_name="_eq")
    _neq = sgqlc.types.Field(DateTime, graphql_name="_neq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(DateTime)), graphql_name="_in")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(DateTime)), graphql_name="_nin")
    _gt = sgqlc.types.Field(DateTime, graphql_name="_gt")
    _gte = sgqlc.types.Field(DateTime, graphql_name="_gte")
    _lt = sgqlc.types.Field(DateTime, graphql_name="_lt")
    _lte = sgqlc.types.Field(DateTime, graphql_name="_lte")
    _is_null = sgqlc.types.Field(DateTime, graphql_name="_is_null")


class EntityWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id", "entity_id", "producing_run_id", "owner_user_id", "collection_id")
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    entity_id = sgqlc.types.Field("UUIDComparators", graphql_name="entityId")
    producing_run_id = sgqlc.types.Field("IntComparators", graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field("IntComparators", graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field("IntComparators", graphql_name="collectionId")


class FileCreate(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("name", "file_format", "compression_type", "protocol", "namespace", "path")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    file_format = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="fileFormat")
    compression_type = sgqlc.types.Field(String, graphql_name="compressionType")
    protocol = sgqlc.types.Field(sgqlc.types.non_null(FileAccessProtocol), graphql_name="protocol")
    namespace = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="namespace")
    path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="path")


class FileStatusEnumComparators(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("_eq", "_neq", "_in", "_nin", "_gt", "_gte", "_lt", "_lte", "_is_null")
    _eq = sgqlc.types.Field(FileStatus, graphql_name="_eq")
    _neq = sgqlc.types.Field(FileStatus, graphql_name="_neq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(FileStatus)), graphql_name="_in")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(FileStatus)), graphql_name="_nin")
    _gt = sgqlc.types.Field(FileStatus, graphql_name="_gt")
    _gte = sgqlc.types.Field(FileStatus, graphql_name="_gte")
    _lt = sgqlc.types.Field(FileStatus, graphql_name="_lt")
    _lte = sgqlc.types.Field(FileStatus, graphql_name="_lte")
    _is_null = sgqlc.types.Field(FileStatus, graphql_name="_is_null")


class FileUpload(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("name", "file_format", "compression_type")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    file_format = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="fileFormat")
    compression_type = sgqlc.types.Field(String, graphql_name="compressionType")


class FileWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "entity_id",
        "entity_field_name",
        "status",
        "protocol",
        "namespace",
        "path",
        "file_format",
        "compression_type",
        "size",
    )
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    entity_id = sgqlc.types.Field("UUIDComparators", graphql_name="entityId")
    entity_field_name = sgqlc.types.Field("StrComparators", graphql_name="entityFieldName")
    status = sgqlc.types.Field(FileStatusEnumComparators, graphql_name="status")
    protocol = sgqlc.types.Field("StrComparators", graphql_name="protocol")
    namespace = sgqlc.types.Field("StrComparators", graphql_name="namespace")
    path = sgqlc.types.Field("StrComparators", graphql_name="path")
    file_format = sgqlc.types.Field("StrComparators", graphql_name="fileFormat")
    compression_type = sgqlc.types.Field("StrComparators", graphql_name="compressionType")
    size = sgqlc.types.Field("IntComparators", graphql_name="size")


class FloatComparators(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("_eq", "_neq", "_in", "_nin", "_gt", "_gte", "_lt", "_lte", "_is_null")
    _eq = sgqlc.types.Field(Float, graphql_name="_eq")
    _neq = sgqlc.types.Field(Float, graphql_name="_neq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Float)), graphql_name="_in")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Float)), graphql_name="_nin")
    _gt = sgqlc.types.Field(Float, graphql_name="_gt")
    _gte = sgqlc.types.Field(Float, graphql_name="_gte")
    _lt = sgqlc.types.Field(Float, graphql_name="_lt")
    _lte = sgqlc.types.Field(Float, graphql_name="_lte")
    _is_null = sgqlc.types.Field(Float, graphql_name="_is_null")


class GenomicRangeCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "reference_genome_id", "file_id")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    reference_genome_id = sgqlc.types.Field(ID, graphql_name="referenceGenomeId")
    file_id = sgqlc.types.Field(ID, graphql_name="fileId")


class GenomicRangeUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "reference_genome_id", "file_id")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    reference_genome_id = sgqlc.types.Field(ID, graphql_name="referenceGenomeId")
    file_id = sgqlc.types.Field(ID, graphql_name="fileId")


class GenomicRangeWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "reference_genome",
        "sequencing_reads",
    )
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field("IntComparators", graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field("IntComparators", graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field("IntComparators", graphql_name="collectionId")
    reference_genome = sgqlc.types.Field("ReferenceGenomeWhereClause", graphql_name="referenceGenome")
    sequencing_reads = sgqlc.types.Field("SequencingReadWhereClause", graphql_name="sequencingReads")


class GenomicRangeWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")


class HostOrganismCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "name", "version", "host_filtering_id", "sequence_id")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    version = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="version")
    host_filtering_id = sgqlc.types.Field(ID, graphql_name="hostFilteringId")
    sequence_id = sgqlc.types.Field(ID, graphql_name="sequenceId")


class HostOrganismUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "name", "version", "host_filtering_id", "sequence_id")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    name = sgqlc.types.Field(String, graphql_name="name")
    version = sgqlc.types.Field(String, graphql_name="version")
    host_filtering_id = sgqlc.types.Field(ID, graphql_name="hostFilteringId")
    sequence_id = sgqlc.types.Field(ID, graphql_name="sequenceId")


class HostOrganismWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id", "producing_run_id", "owner_user_id", "collection_id", "name", "version")
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field("IntComparators", graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field("IntComparators", graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field("IntComparators", graphql_name="collectionId")
    name = sgqlc.types.Field("StrComparators", graphql_name="name")
    version = sgqlc.types.Field("StrComparators", graphql_name="version")


class HostOrganismWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")


class IntComparators(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("_eq", "_neq", "_in", "_nin", "_gt", "_gte", "_lt", "_lte", "_is_null")
    _eq = sgqlc.types.Field(Int, graphql_name="_eq")
    _neq = sgqlc.types.Field(Int, graphql_name="_neq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Int)), graphql_name="_in")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Int)), graphql_name="_nin")
    _gt = sgqlc.types.Field(Int, graphql_name="_gt")
    _gte = sgqlc.types.Field(Int, graphql_name="_gte")
    _lt = sgqlc.types.Field(Int, graphql_name="_lt")
    _lte = sgqlc.types.Field(Int, graphql_name="_lte")
    _is_null = sgqlc.types.Field(Int, graphql_name="_is_null")


class MetadatumCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "sample_id", "field_name", "value")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    sample_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="sampleId")
    field_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="fieldName")
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="value")


class MetadatumUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "sample_id", "field_name", "value")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    sample_id = sgqlc.types.Field(ID, graphql_name="sampleId")
    field_name = sgqlc.types.Field(String, graphql_name="fieldName")
    value = sgqlc.types.Field(String, graphql_name="value")


class MetadatumWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id", "producing_run_id", "owner_user_id", "collection_id", "sample", "field_name", "value")
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    sample = sgqlc.types.Field("SampleWhereClause", graphql_name="sample")
    field_name = sgqlc.types.Field("StrComparators", graphql_name="fieldName")
    value = sgqlc.types.Field("StrComparators", graphql_name="value")


class MetadatumWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")


class MetricConsensusGenomeCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "collection_id",
        "consensus_genome_id",
        "reference_genome_length",
        "percent_genome_called",
        "percent_identity",
        "gc_percent",
        "total_reads",
        "mapped_reads",
        "ref_snps",
        "n_actg",
        "n_missing",
        "n_ambiguous",
        "coverage_depth",
        "coverage_breadth",
        "coverage_bin_size",
        "coverage_total_length",
        "coverage_viz",
    )
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    consensus_genome_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="consensusGenomeId")
    reference_genome_length = sgqlc.types.Field(Float, graphql_name="referenceGenomeLength")
    percent_genome_called = sgqlc.types.Field(Float, graphql_name="percentGenomeCalled")
    percent_identity = sgqlc.types.Field(Float, graphql_name="percentIdentity")
    gc_percent = sgqlc.types.Field(Float, graphql_name="gcPercent")
    total_reads = sgqlc.types.Field(Int, graphql_name="totalReads")
    mapped_reads = sgqlc.types.Field(Int, graphql_name="mappedReads")
    ref_snps = sgqlc.types.Field(Int, graphql_name="refSnps")
    n_actg = sgqlc.types.Field(Int, graphql_name="nActg")
    n_missing = sgqlc.types.Field(Int, graphql_name="nMissing")
    n_ambiguous = sgqlc.types.Field(Int, graphql_name="nAmbiguous")
    coverage_depth = sgqlc.types.Field(Float, graphql_name="coverageDepth")
    coverage_breadth = sgqlc.types.Field(Float, graphql_name="coverageBreadth")
    coverage_bin_size = sgqlc.types.Field(Float, graphql_name="coverageBinSize")
    coverage_total_length = sgqlc.types.Field(Int, graphql_name="coverageTotalLength")
    coverage_viz = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Int)))),
        graphql_name="coverageViz",
    )


class MetricConsensusGenomeUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "collection_id",
        "consensus_genome_id",
        "reference_genome_length",
        "percent_genome_called",
        "percent_identity",
        "gc_percent",
        "total_reads",
        "mapped_reads",
        "ref_snps",
        "n_actg",
        "n_missing",
        "n_ambiguous",
        "coverage_depth",
        "coverage_breadth",
        "coverage_bin_size",
        "coverage_total_length",
        "coverage_viz",
    )
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    consensus_genome_id = sgqlc.types.Field(ID, graphql_name="consensusGenomeId")
    reference_genome_length = sgqlc.types.Field(Float, graphql_name="referenceGenomeLength")
    percent_genome_called = sgqlc.types.Field(Float, graphql_name="percentGenomeCalled")
    percent_identity = sgqlc.types.Field(Float, graphql_name="percentIdentity")
    gc_percent = sgqlc.types.Field(Float, graphql_name="gcPercent")
    total_reads = sgqlc.types.Field(Int, graphql_name="totalReads")
    mapped_reads = sgqlc.types.Field(Int, graphql_name="mappedReads")
    ref_snps = sgqlc.types.Field(Int, graphql_name="refSnps")
    n_actg = sgqlc.types.Field(Int, graphql_name="nActg")
    n_missing = sgqlc.types.Field(Int, graphql_name="nMissing")
    n_ambiguous = sgqlc.types.Field(Int, graphql_name="nAmbiguous")
    coverage_depth = sgqlc.types.Field(Float, graphql_name="coverageDepth")
    coverage_breadth = sgqlc.types.Field(Float, graphql_name="coverageBreadth")
    coverage_bin_size = sgqlc.types.Field(Float, graphql_name="coverageBinSize")
    coverage_total_length = sgqlc.types.Field(Int, graphql_name="coverageTotalLength")
    coverage_viz = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Int)))),
        graphql_name="coverageViz",
    )


class MetricConsensusGenomeWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "consensus_genome",
        "reference_genome_length",
        "percent_genome_called",
        "percent_identity",
        "gc_percent",
        "total_reads",
        "mapped_reads",
        "ref_snps",
        "n_actg",
        "n_missing",
        "n_ambiguous",
        "coverage_depth",
        "coverage_breadth",
        "coverage_bin_size",
        "coverage_total_length",
    )
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    consensus_genome = sgqlc.types.Field(ConsensusGenomeWhereClause, graphql_name="consensusGenome")
    reference_genome_length = sgqlc.types.Field(FloatComparators, graphql_name="referenceGenomeLength")
    percent_genome_called = sgqlc.types.Field(FloatComparators, graphql_name="percentGenomeCalled")
    percent_identity = sgqlc.types.Field(FloatComparators, graphql_name="percentIdentity")
    gc_percent = sgqlc.types.Field(FloatComparators, graphql_name="gcPercent")
    total_reads = sgqlc.types.Field(IntComparators, graphql_name="totalReads")
    mapped_reads = sgqlc.types.Field(IntComparators, graphql_name="mappedReads")
    ref_snps = sgqlc.types.Field(IntComparators, graphql_name="refSnps")
    n_actg = sgqlc.types.Field(IntComparators, graphql_name="nActg")
    n_missing = sgqlc.types.Field(IntComparators, graphql_name="nMissing")
    n_ambiguous = sgqlc.types.Field(IntComparators, graphql_name="nAmbiguous")
    coverage_depth = sgqlc.types.Field(FloatComparators, graphql_name="coverageDepth")
    coverage_breadth = sgqlc.types.Field(FloatComparators, graphql_name="coverageBreadth")
    coverage_bin_size = sgqlc.types.Field(FloatComparators, graphql_name="coverageBinSize")
    coverage_total_length = sgqlc.types.Field(IntComparators, graphql_name="coverageTotalLength")


class MetricConsensusGenomeWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")


class NucleicAcidEnumComparators(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("_eq", "_neq", "_in", "_nin", "_gt", "_gte", "_lt", "_lte", "_is_null")
    _eq = sgqlc.types.Field(NucleicAcid, graphql_name="_eq")
    _neq = sgqlc.types.Field(NucleicAcid, graphql_name="_neq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(NucleicAcid)), graphql_name="_in")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(NucleicAcid)), graphql_name="_nin")
    _gt = sgqlc.types.Field(NucleicAcid, graphql_name="_gt")
    _gte = sgqlc.types.Field(NucleicAcid, graphql_name="_gte")
    _lt = sgqlc.types.Field(NucleicAcid, graphql_name="_lt")
    _lte = sgqlc.types.Field(NucleicAcid, graphql_name="_lte")
    _is_null = sgqlc.types.Field(NucleicAcid, graphql_name="_is_null")


class PhylogeneticTreeCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "tree_id", "format")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    tree_id = sgqlc.types.Field(ID, graphql_name="treeId")
    format = sgqlc.types.Field(sgqlc.types.non_null(PhylogeneticTreeFormat), graphql_name="format")


class PhylogeneticTreeFormatEnumComparators(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("_eq", "_neq", "_in", "_nin", "_gt", "_gte", "_lt", "_lte", "_is_null")
    _eq = sgqlc.types.Field(PhylogeneticTreeFormat, graphql_name="_eq")
    _neq = sgqlc.types.Field(PhylogeneticTreeFormat, graphql_name="_neq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(PhylogeneticTreeFormat)), graphql_name="_in")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(PhylogeneticTreeFormat)), graphql_name="_nin")
    _gt = sgqlc.types.Field(PhylogeneticTreeFormat, graphql_name="_gt")
    _gte = sgqlc.types.Field(PhylogeneticTreeFormat, graphql_name="_gte")
    _lt = sgqlc.types.Field(PhylogeneticTreeFormat, graphql_name="_lt")
    _lte = sgqlc.types.Field(PhylogeneticTreeFormat, graphql_name="_lte")
    _is_null = sgqlc.types.Field(PhylogeneticTreeFormat, graphql_name="_is_null")


class PhylogeneticTreeUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "tree_id", "format")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    tree_id = sgqlc.types.Field(ID, graphql_name="treeId")
    format = sgqlc.types.Field(PhylogeneticTreeFormat, graphql_name="format")


class PhylogeneticTreeWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id", "producing_run_id", "owner_user_id", "collection_id", "format")
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    format = sgqlc.types.Field(PhylogeneticTreeFormatEnumComparators, graphql_name="format")


class PhylogeneticTreeWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")


class ReferenceGenomeCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "file_id", "taxon_id", "accession_id")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    file_id = sgqlc.types.Field(ID, graphql_name="fileId")
    taxon_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="taxonId")
    accession_id = sgqlc.types.Field(String, graphql_name="accessionId")


class ReferenceGenomeUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "file_id", "taxon_id", "accession_id")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    file_id = sgqlc.types.Field(ID, graphql_name="fileId")
    taxon_id = sgqlc.types.Field(ID, graphql_name="taxonId")
    accession_id = sgqlc.types.Field(String, graphql_name="accessionId")


class ReferenceGenomeWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "taxon",
        "accession_id",
        "consensus_genomes",
        "genomic_ranges",
    )
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    taxon = sgqlc.types.Field("TaxonWhereClause", graphql_name="taxon")
    accession_id = sgqlc.types.Field("StrComparators", graphql_name="accessionId")
    consensus_genomes = sgqlc.types.Field(ConsensusGenomeWhereClause, graphql_name="consensusGenomes")
    genomic_ranges = sgqlc.types.Field(GenomicRangeWhereClause, graphql_name="genomicRanges")


class ReferenceGenomeWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")


class SampleCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "collection_id",
        "rails_sample_id",
        "name",
        "sample_type",
        "water_control",
        "collection_date",
        "collection_location",
        "description",
        "host_taxon_id",
    )
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    rails_sample_id = sgqlc.types.Field(Int, graphql_name="railsSampleId")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    sample_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="sampleType")
    water_control = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="waterControl")
    collection_date = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name="collectionDate")
    collection_location = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="collectionLocation")
    description = sgqlc.types.Field(String, graphql_name="description")
    host_taxon_id = sgqlc.types.Field(ID, graphql_name="hostTaxonId")


class SampleUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "collection_id",
        "rails_sample_id",
        "name",
        "sample_type",
        "water_control",
        "collection_date",
        "collection_location",
        "description",
        "host_taxon_id",
    )
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    rails_sample_id = sgqlc.types.Field(Int, graphql_name="railsSampleId")
    name = sgqlc.types.Field(String, graphql_name="name")
    sample_type = sgqlc.types.Field(String, graphql_name="sampleType")
    water_control = sgqlc.types.Field(Boolean, graphql_name="waterControl")
    collection_date = sgqlc.types.Field(DateTime, graphql_name="collectionDate")
    collection_location = sgqlc.types.Field(String, graphql_name="collectionLocation")
    description = sgqlc.types.Field(String, graphql_name="description")
    host_taxon_id = sgqlc.types.Field(ID, graphql_name="hostTaxonId")


class SampleWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "rails_sample_id",
        "name",
        "sample_type",
        "water_control",
        "collection_date",
        "collection_location",
        "description",
        "host_taxon",
        "sequencing_reads",
        "metadatas",
    )
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    rails_sample_id = sgqlc.types.Field(IntComparators, graphql_name="railsSampleId")
    name = sgqlc.types.Field("StrComparators", graphql_name="name")
    sample_type = sgqlc.types.Field("StrComparators", graphql_name="sampleType")
    water_control = sgqlc.types.Field(BoolComparators, graphql_name="waterControl")
    collection_date = sgqlc.types.Field(DatetimeComparators, graphql_name="collectionDate")
    collection_location = sgqlc.types.Field("StrComparators", graphql_name="collectionLocation")
    description = sgqlc.types.Field("StrComparators", graphql_name="description")
    host_taxon = sgqlc.types.Field("TaxonWhereClause", graphql_name="hostTaxon")
    sequencing_reads = sgqlc.types.Field("SequencingReadWhereClause", graphql_name="sequencingReads")
    metadatas = sgqlc.types.Field(MetadatumWhereClause, graphql_name="metadatas")


class SampleWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")


class SequencingProtocolEnumComparators(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("_eq", "_neq", "_in", "_nin", "_gt", "_gte", "_lt", "_lte", "_is_null")
    _eq = sgqlc.types.Field(SequencingProtocol, graphql_name="_eq")
    _neq = sgqlc.types.Field(SequencingProtocol, graphql_name="_neq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(SequencingProtocol)), graphql_name="_in")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(SequencingProtocol)), graphql_name="_nin")
    _gt = sgqlc.types.Field(SequencingProtocol, graphql_name="_gt")
    _gte = sgqlc.types.Field(SequencingProtocol, graphql_name="_gte")
    _lt = sgqlc.types.Field(SequencingProtocol, graphql_name="_lt")
    _lte = sgqlc.types.Field(SequencingProtocol, graphql_name="_lte")
    _is_null = sgqlc.types.Field(SequencingProtocol, graphql_name="_is_null")


class SequencingReadCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "collection_id",
        "sample_id",
        "protocol",
        "r1_file_id",
        "r2_file_id",
        "technology",
        "nucleic_acid",
        "taxon_id",
        "primer_file_id",
    )
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    sample_id = sgqlc.types.Field(ID, graphql_name="sampleId")
    protocol = sgqlc.types.Field(SequencingProtocol, graphql_name="protocol")
    r1_file_id = sgqlc.types.Field(ID, graphql_name="r1FileId")
    r2_file_id = sgqlc.types.Field(ID, graphql_name="r2FileId")
    technology = sgqlc.types.Field(sgqlc.types.non_null(SequencingTechnology), graphql_name="technology")
    nucleic_acid = sgqlc.types.Field(sgqlc.types.non_null(NucleicAcid), graphql_name="nucleicAcid")
    taxon_id = sgqlc.types.Field(ID, graphql_name="taxonId")
    primer_file_id = sgqlc.types.Field(ID, graphql_name="primerFileId")


class SequencingReadUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "collection_id",
        "sample_id",
        "protocol",
        "r1_file_id",
        "r2_file_id",
        "technology",
        "nucleic_acid",
        "taxon_id",
        "primer_file_id",
    )
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    sample_id = sgqlc.types.Field(ID, graphql_name="sampleId")
    protocol = sgqlc.types.Field(SequencingProtocol, graphql_name="protocol")
    r1_file_id = sgqlc.types.Field(ID, graphql_name="r1FileId")
    r2_file_id = sgqlc.types.Field(ID, graphql_name="r2FileId")
    technology = sgqlc.types.Field(SequencingTechnology, graphql_name="technology")
    nucleic_acid = sgqlc.types.Field(NucleicAcid, graphql_name="nucleicAcid")
    taxon_id = sgqlc.types.Field(ID, graphql_name="taxonId")
    primer_file_id = sgqlc.types.Field(ID, graphql_name="primerFileId")


class SequencingReadWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "sample",
        "protocol",
        "technology",
        "nucleic_acid",
        "taxon",
        "primer_file",
        "consensus_genomes",
        "contigs",
    )
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    sample = sgqlc.types.Field(SampleWhereClause, graphql_name="sample")
    protocol = sgqlc.types.Field(SequencingProtocolEnumComparators, graphql_name="protocol")
    technology = sgqlc.types.Field("SequencingTechnologyEnumComparators", graphql_name="technology")
    nucleic_acid = sgqlc.types.Field(NucleicAcidEnumComparators, graphql_name="nucleicAcid")
    taxon = sgqlc.types.Field("TaxonWhereClause", graphql_name="taxon")
    primer_file = sgqlc.types.Field(GenomicRangeWhereClause, graphql_name="primerFile")
    consensus_genomes = sgqlc.types.Field(ConsensusGenomeWhereClause, graphql_name="consensusGenomes")
    contigs = sgqlc.types.Field(ContigWhereClause, graphql_name="contigs")


class SequencingReadWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")


class SequencingTechnologyEnumComparators(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("_eq", "_neq", "_in", "_nin", "_gt", "_gte", "_lt", "_lte", "_is_null")
    _eq = sgqlc.types.Field(SequencingTechnology, graphql_name="_eq")
    _neq = sgqlc.types.Field(SequencingTechnology, graphql_name="_neq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(SequencingTechnology)), graphql_name="_in")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(SequencingTechnology)), graphql_name="_nin")
    _gt = sgqlc.types.Field(SequencingTechnology, graphql_name="_gt")
    _gte = sgqlc.types.Field(SequencingTechnology, graphql_name="_gte")
    _lt = sgqlc.types.Field(SequencingTechnology, graphql_name="_lt")
    _lte = sgqlc.types.Field(SequencingTechnology, graphql_name="_lte")
    _is_null = sgqlc.types.Field(SequencingTechnology, graphql_name="_is_null")


class StrComparators(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "_eq",
        "_neq",
        "_in",
        "_nin",
        "_is_null",
        "_gt",
        "_gte",
        "_lt",
        "_lte",
        "_like",
        "_nlike",
        "_ilike",
        "_nilike",
        "_regex",
        "_nregex",
        "_iregex",
        "_niregex",
    )
    _eq = sgqlc.types.Field(String, graphql_name="_eq")
    _neq = sgqlc.types.Field(String, graphql_name="_neq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="_in")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="_nin")
    _is_null = sgqlc.types.Field(Int, graphql_name="_is_null")
    _gt = sgqlc.types.Field(String, graphql_name="_gt")
    _gte = sgqlc.types.Field(String, graphql_name="_gte")
    _lt = sgqlc.types.Field(String, graphql_name="_lt")
    _lte = sgqlc.types.Field(String, graphql_name="_lte")
    _like = sgqlc.types.Field(String, graphql_name="_like")
    _nlike = sgqlc.types.Field(String, graphql_name="_nlike")
    _ilike = sgqlc.types.Field(String, graphql_name="_ilike")
    _nilike = sgqlc.types.Field(String, graphql_name="_nilike")
    _regex = sgqlc.types.Field(String, graphql_name="_regex")
    _nregex = sgqlc.types.Field(String, graphql_name="_nregex")
    _iregex = sgqlc.types.Field(String, graphql_name="_iregex")
    _niregex = sgqlc.types.Field(String, graphql_name="_niregex")


class TaxonCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "collection_id",
        "wikipedia_id",
        "description",
        "common_name",
        "name",
        "is_phage",
        "upstream_database_id",
        "upstream_database_identifier",
        "level",
    )
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    wikipedia_id = sgqlc.types.Field(String, graphql_name="wikipediaId")
    description = sgqlc.types.Field(String, graphql_name="description")
    common_name = sgqlc.types.Field(String, graphql_name="commonName")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    is_phage = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="isPhage")
    upstream_database_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="upstreamDatabaseId")
    upstream_database_identifier = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="upstreamDatabaseIdentifier"
    )
    level = sgqlc.types.Field(sgqlc.types.non_null(TaxonLevel), graphql_name="level")


class TaxonLevelEnumComparators(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("_eq", "_neq", "_in", "_nin", "_gt", "_gte", "_lt", "_lte", "_is_null")
    _eq = sgqlc.types.Field(TaxonLevel, graphql_name="_eq")
    _neq = sgqlc.types.Field(TaxonLevel, graphql_name="_neq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(TaxonLevel)), graphql_name="_in")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(TaxonLevel)), graphql_name="_nin")
    _gt = sgqlc.types.Field(TaxonLevel, graphql_name="_gt")
    _gte = sgqlc.types.Field(TaxonLevel, graphql_name="_gte")
    _lt = sgqlc.types.Field(TaxonLevel, graphql_name="_lt")
    _lte = sgqlc.types.Field(TaxonLevel, graphql_name="_lte")
    _is_null = sgqlc.types.Field(TaxonLevel, graphql_name="_is_null")


class TaxonUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "collection_id",
        "wikipedia_id",
        "description",
        "common_name",
        "name",
        "is_phage",
        "upstream_database_id",
        "upstream_database_identifier",
        "level",
    )
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    wikipedia_id = sgqlc.types.Field(String, graphql_name="wikipediaId")
    description = sgqlc.types.Field(String, graphql_name="description")
    common_name = sgqlc.types.Field(String, graphql_name="commonName")
    name = sgqlc.types.Field(String, graphql_name="name")
    is_phage = sgqlc.types.Field(Boolean, graphql_name="isPhage")
    upstream_database_id = sgqlc.types.Field(ID, graphql_name="upstreamDatabaseId")
    upstream_database_identifier = sgqlc.types.Field(String, graphql_name="upstreamDatabaseIdentifier")
    level = sgqlc.types.Field(TaxonLevel, graphql_name="level")


class TaxonWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "wikipedia_id",
        "description",
        "common_name",
        "name",
        "is_phage",
        "upstream_database",
        "upstream_database_identifier",
        "level",
        "consensus_genomes",
        "reference_genomes",
        "sequencing_reads",
        "samples",
    )
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    wikipedia_id = sgqlc.types.Field(StrComparators, graphql_name="wikipediaId")
    description = sgqlc.types.Field(StrComparators, graphql_name="description")
    common_name = sgqlc.types.Field(StrComparators, graphql_name="commonName")
    name = sgqlc.types.Field(StrComparators, graphql_name="name")
    is_phage = sgqlc.types.Field(BoolComparators, graphql_name="isPhage")
    upstream_database = sgqlc.types.Field("UpstreamDatabaseWhereClause", graphql_name="upstreamDatabase")
    upstream_database_identifier = sgqlc.types.Field(StrComparators, graphql_name="upstreamDatabaseIdentifier")
    level = sgqlc.types.Field(TaxonLevelEnumComparators, graphql_name="level")
    consensus_genomes = sgqlc.types.Field(ConsensusGenomeWhereClause, graphql_name="consensusGenomes")
    reference_genomes = sgqlc.types.Field(ReferenceGenomeWhereClause, graphql_name="referenceGenomes")
    sequencing_reads = sgqlc.types.Field(SequencingReadWhereClause, graphql_name="sequencingReads")
    samples = sgqlc.types.Field(SampleWhereClause, graphql_name="samples")


class TaxonWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")


class UUIDComparators(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("_eq", "_neq", "_in", "_nin", "_gt", "_gte", "_lt", "_lte")
    _eq = sgqlc.types.Field(UUID, graphql_name="_eq")
    _neq = sgqlc.types.Field(UUID, graphql_name="_neq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(UUID)), graphql_name="_in")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(UUID)), graphql_name="_nin")
    _gt = sgqlc.types.Field(UUID, graphql_name="_gt")
    _gte = sgqlc.types.Field(UUID, graphql_name="_gte")
    _lt = sgqlc.types.Field(UUID, graphql_name="_lt")
    _lte = sgqlc.types.Field(UUID, graphql_name="_lte")


class UpstreamDatabaseCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "name")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")


class UpstreamDatabaseUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "name")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    name = sgqlc.types.Field(String, graphql_name="name")


class UpstreamDatabaseWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id", "producing_run_id", "owner_user_id", "collection_id", "name", "taxa")
    id = sgqlc.types.Field(UUIDComparators, graphql_name="id")
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    name = sgqlc.types.Field(StrComparators, graphql_name="name")
    taxa = sgqlc.types.Field(TaxonWhereClause, graphql_name="taxa")


class UpstreamDatabaseWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(UUIDComparators, graphql_name="id")


########################################################################
# Output Objects and Interfaces
########################################################################
class Node(sgqlc.types.Interface):
    __schema__ = gql_schema
    __field_names__ = ("_id",)
    _id = sgqlc.types.Field(sgqlc.types.non_null(GlobalID), graphql_name="_id")


class EntityInterface(sgqlc.types.Interface):
    __schema__ = gql_schema
    __field_names__ = ("_id",)
    _id = sgqlc.types.Field(sgqlc.types.non_null(GlobalID), graphql_name="_id")


class BulkDownloadAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field("BulkDownloadAggregateFunctions", graphql_name="aggregate")


class BulkDownloadAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "min", "max", "stddev", "variance", "count")
    sum = sgqlc.types.Field("BulkDownloadNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("BulkDownloadNumericalColumns", graphql_name="avg")
    min = sgqlc.types.Field("BulkDownloadMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("BulkDownloadMinMaxColumns", graphql_name="max")
    stddev = sgqlc.types.Field("BulkDownloadNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("BulkDownloadNumericalColumns", graphql_name="variance")
    count = sgqlc.types.Field(
        Int,
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=False)),
                ("columns", sgqlc.types.Arg(BulkDownloadCountColumns, graphql_name="columns", default=None)),
            )
        ),
    )


class BulkDownloadMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class BulkDownloadNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class ConsensusGenomeAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field("ConsensusGenomeAggregateFunctions", graphql_name="aggregate")


class ConsensusGenomeAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "min", "max", "stddev", "variance", "count")
    sum = sgqlc.types.Field("ConsensusGenomeNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("ConsensusGenomeNumericalColumns", graphql_name="avg")
    min = sgqlc.types.Field("ConsensusGenomeMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("ConsensusGenomeMinMaxColumns", graphql_name="max")
    stddev = sgqlc.types.Field("ConsensusGenomeNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("ConsensusGenomeNumericalColumns", graphql_name="variance")
    count = sgqlc.types.Field(
        Int,
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=False)),
                ("columns", sgqlc.types.Arg(ConsensusGenomeCountColumns, graphql_name="columns", default=None)),
            )
        ),
    )


class ConsensusGenomeConnection(sgqlc.types.relay.Connection):
    __schema__ = gql_schema
    __field_names__ = ("page_info", "edges")
    page_info = sgqlc.types.Field(sgqlc.types.non_null("PageInfo"), graphql_name="pageInfo")
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ConsensusGenomeEdge"))), graphql_name="edges"
    )


class ConsensusGenomeEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("cursor", "node")
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="cursor")
    node = sgqlc.types.Field(sgqlc.types.non_null("ConsensusGenome"), graphql_name="node")


class ConsensusGenomeMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class ConsensusGenomeNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class ContigAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field("ContigAggregateFunctions", graphql_name="aggregate")


class ContigAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "min", "max", "stddev", "variance", "count")
    sum = sgqlc.types.Field("ContigNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("ContigNumericalColumns", graphql_name="avg")
    min = sgqlc.types.Field("ContigMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("ContigMinMaxColumns", graphql_name="max")
    stddev = sgqlc.types.Field("ContigNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("ContigNumericalColumns", graphql_name="variance")
    count = sgqlc.types.Field(
        Int,
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=False)),
                ("columns", sgqlc.types.Arg(ContigCountColumns, graphql_name="columns", default=None)),
            )
        ),
    )


class ContigConnection(sgqlc.types.relay.Connection):
    __schema__ = gql_schema
    __field_names__ = ("page_info", "edges")
    page_info = sgqlc.types.Field(sgqlc.types.non_null("PageInfo"), graphql_name="pageInfo")
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ContigEdge"))), graphql_name="edges"
    )


class ContigEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("cursor", "node")
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="cursor")
    node = sgqlc.types.Field(sgqlc.types.non_null("Contig"), graphql_name="node")


class ContigMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id", "sequence")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    sequence = sgqlc.types.Field(String, graphql_name="sequence")


class ContigNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class Entity(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("id", "type", "producing_run_id", "owner_user_id", "collection_id")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="type")
    producing_run_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")


class File(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "entity_id",
        "entity_field_name",
        "entity",
        "status",
        "protocol",
        "namespace",
        "path",
        "file_format",
        "compression_type",
        "size",
        "download_link",
        "contents",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    entity_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="entityId")
    entity_field_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="entityFieldName")
    entity = sgqlc.types.Field(
        Entity,
        graphql_name="entity",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(EntityWhereClause, graphql_name="where", default=None)),)),
    )
    status = sgqlc.types.Field(sgqlc.types.non_null(FileStatus), graphql_name="status")
    protocol = sgqlc.types.Field(sgqlc.types.non_null(FileAccessProtocol), graphql_name="protocol")
    namespace = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="namespace")
    path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="path")
    file_format = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="fileFormat")
    compression_type = sgqlc.types.Field(Int, graphql_name="compressionType")
    size = sgqlc.types.Field(Int, graphql_name="size")
    download_link = sgqlc.types.Field(
        "SignedURL",
        graphql_name="downloadLink",
        args=sgqlc.types.ArgDict(
            (("expiration", sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="expiration", default=3600)),)
        ),
    )
    contents = sgqlc.types.Field(String, graphql_name="contents")


class GenomicRangeAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field("GenomicRangeAggregateFunctions", graphql_name="aggregate")


class GenomicRangeAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "min", "max", "stddev", "variance", "count")
    sum = sgqlc.types.Field("GenomicRangeNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("GenomicRangeNumericalColumns", graphql_name="avg")
    min = sgqlc.types.Field("GenomicRangeMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("GenomicRangeMinMaxColumns", graphql_name="max")
    stddev = sgqlc.types.Field("GenomicRangeNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("GenomicRangeNumericalColumns", graphql_name="variance")
    count = sgqlc.types.Field(
        Int,
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=False)),
                ("columns", sgqlc.types.Arg(GenomicRangeCountColumns, graphql_name="columns", default=None)),
            )
        ),
    )


class GenomicRangeConnection(sgqlc.types.relay.Connection):
    __schema__ = gql_schema
    __field_names__ = ("page_info", "edges")
    page_info = sgqlc.types.Field(sgqlc.types.non_null("PageInfo"), graphql_name="pageInfo")
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("GenomicRangeEdge"))), graphql_name="edges"
    )


class GenomicRangeEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("cursor", "node")
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="cursor")
    node = sgqlc.types.Field(sgqlc.types.non_null("GenomicRange"), graphql_name="node")


class GenomicRangeMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class GenomicRangeNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class HostOrganismAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field("HostOrganismAggregateFunctions", graphql_name="aggregate")


class HostOrganismAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "min", "max", "stddev", "variance", "count")
    sum = sgqlc.types.Field("HostOrganismNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("HostOrganismNumericalColumns", graphql_name="avg")
    min = sgqlc.types.Field("HostOrganismMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("HostOrganismMinMaxColumns", graphql_name="max")
    stddev = sgqlc.types.Field("HostOrganismNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("HostOrganismNumericalColumns", graphql_name="variance")
    count = sgqlc.types.Field(
        Int,
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=False)),
                ("columns", sgqlc.types.Arg(HostOrganismCountColumns, graphql_name="columns", default=None)),
            )
        ),
    )


class HostOrganismMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id", "name", "version")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    name = sgqlc.types.Field(String, graphql_name="name")
    version = sgqlc.types.Field(String, graphql_name="version")


class HostOrganismNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class MetadatumAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field("MetadatumAggregateFunctions", graphql_name="aggregate")


class MetadatumAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "min", "max", "stddev", "variance", "count")
    sum = sgqlc.types.Field("MetadatumNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("MetadatumNumericalColumns", graphql_name="avg")
    min = sgqlc.types.Field("MetadatumMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("MetadatumMinMaxColumns", graphql_name="max")
    stddev = sgqlc.types.Field("MetadatumNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("MetadatumNumericalColumns", graphql_name="variance")
    count = sgqlc.types.Field(
        Int,
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=False)),
                ("columns", sgqlc.types.Arg(MetadatumCountColumns, graphql_name="columns", default=None)),
            )
        ),
    )


class MetadatumConnection(sgqlc.types.relay.Connection):
    __schema__ = gql_schema
    __field_names__ = ("page_info", "edges")
    page_info = sgqlc.types.Field(sgqlc.types.non_null("PageInfo"), graphql_name="pageInfo")
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("MetadatumEdge"))), graphql_name="edges"
    )


class MetadatumEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("cursor", "node")
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="cursor")
    node = sgqlc.types.Field(sgqlc.types.non_null("Metadatum"), graphql_name="node")


class MetadatumMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id", "field_name", "value")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    field_name = sgqlc.types.Field(String, graphql_name="fieldName")
    value = sgqlc.types.Field(String, graphql_name="value")


class MetadatumNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class MetricConsensusGenomeAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field("MetricConsensusGenomeAggregateFunctions", graphql_name="aggregate")


class MetricConsensusGenomeAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "min", "max", "stddev", "variance", "count")
    sum = sgqlc.types.Field("MetricConsensusGenomeNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("MetricConsensusGenomeNumericalColumns", graphql_name="avg")
    min = sgqlc.types.Field("MetricConsensusGenomeMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("MetricConsensusGenomeMinMaxColumns", graphql_name="max")
    stddev = sgqlc.types.Field("MetricConsensusGenomeNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("MetricConsensusGenomeNumericalColumns", graphql_name="variance")
    count = sgqlc.types.Field(
        Int,
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=False)),
                ("columns", sgqlc.types.Arg(MetricConsensusGenomeCountColumns, graphql_name="columns", default=None)),
            )
        ),
    )


class MetricConsensusGenomeConnection(sgqlc.types.relay.Connection):
    __schema__ = gql_schema
    __field_names__ = ("page_info", "edges")
    page_info = sgqlc.types.Field(sgqlc.types.non_null("PageInfo"), graphql_name="pageInfo")
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("MetricConsensusGenomeEdge"))),
        graphql_name="edges",
    )


class MetricConsensusGenomeEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("cursor", "node")
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="cursor")
    node = sgqlc.types.Field(sgqlc.types.non_null("MetricConsensusGenome"), graphql_name="node")


class MetricConsensusGenomeMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "reference_genome_length",
        "percent_genome_called",
        "percent_identity",
        "gc_percent",
        "total_reads",
        "mapped_reads",
        "ref_snps",
        "n_actg",
        "n_missing",
        "n_ambiguous",
        "coverage_depth",
        "coverage_breadth",
        "coverage_bin_size",
        "coverage_total_length",
    )
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    reference_genome_length = sgqlc.types.Field(Float, graphql_name="referenceGenomeLength")
    percent_genome_called = sgqlc.types.Field(Float, graphql_name="percentGenomeCalled")
    percent_identity = sgqlc.types.Field(Float, graphql_name="percentIdentity")
    gc_percent = sgqlc.types.Field(Float, graphql_name="gcPercent")
    total_reads = sgqlc.types.Field(Int, graphql_name="totalReads")
    mapped_reads = sgqlc.types.Field(Int, graphql_name="mappedReads")
    ref_snps = sgqlc.types.Field(Int, graphql_name="refSnps")
    n_actg = sgqlc.types.Field(Int, graphql_name="nActg")
    n_missing = sgqlc.types.Field(Int, graphql_name="nMissing")
    n_ambiguous = sgqlc.types.Field(Int, graphql_name="nAmbiguous")
    coverage_depth = sgqlc.types.Field(Float, graphql_name="coverageDepth")
    coverage_breadth = sgqlc.types.Field(Float, graphql_name="coverageBreadth")
    coverage_bin_size = sgqlc.types.Field(Float, graphql_name="coverageBinSize")
    coverage_total_length = sgqlc.types.Field(Int, graphql_name="coverageTotalLength")


class MetricConsensusGenomeNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "reference_genome_length",
        "percent_genome_called",
        "percent_identity",
        "gc_percent",
        "total_reads",
        "mapped_reads",
        "ref_snps",
        "n_actg",
        "n_missing",
        "n_ambiguous",
        "coverage_depth",
        "coverage_breadth",
        "coverage_bin_size",
        "coverage_total_length",
    )
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    reference_genome_length = sgqlc.types.Field(Float, graphql_name="referenceGenomeLength")
    percent_genome_called = sgqlc.types.Field(Float, graphql_name="percentGenomeCalled")
    percent_identity = sgqlc.types.Field(Float, graphql_name="percentIdentity")
    gc_percent = sgqlc.types.Field(Float, graphql_name="gcPercent")
    total_reads = sgqlc.types.Field(Int, graphql_name="totalReads")
    mapped_reads = sgqlc.types.Field(Int, graphql_name="mappedReads")
    ref_snps = sgqlc.types.Field(Int, graphql_name="refSnps")
    n_actg = sgqlc.types.Field(Int, graphql_name="nActg")
    n_missing = sgqlc.types.Field(Int, graphql_name="nMissing")
    n_ambiguous = sgqlc.types.Field(Int, graphql_name="nAmbiguous")
    coverage_depth = sgqlc.types.Field(Float, graphql_name="coverageDepth")
    coverage_breadth = sgqlc.types.Field(Float, graphql_name="coverageBreadth")
    coverage_bin_size = sgqlc.types.Field(Float, graphql_name="coverageBinSize")
    coverage_total_length = sgqlc.types.Field(Int, graphql_name="coverageTotalLength")


class MultipartUploadCredentials(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "protocol",
        "namespace",
        "path",
        "access_key_id",
        "secret_access_key",
        "session_token",
        "expiration",
    )
    protocol = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="protocol")
    namespace = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="namespace")
    path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="path")
    access_key_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="accessKeyId")
    secret_access_key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="secretAccessKey")
    session_token = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="sessionToken")
    expiration = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="expiration")


class MultipartUploadResponse(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("credentials", "file")
    credentials = sgqlc.types.Field(sgqlc.types.non_null(MultipartUploadCredentials), graphql_name="credentials")
    file = sgqlc.types.Field(sgqlc.types.non_null(File), graphql_name="file")


class Mutation(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "create_file",
        "upload_file",
        "mark_upload_complete",
        "concatenate_files",
        "create_sample",
        "update_sample",
        "delete_sample",
        "create_sequencing_read",
        "update_sequencing_read",
        "delete_sequencing_read",
        "create_genomic_range",
        "update_genomic_range",
        "delete_genomic_range",
        "create_reference_genome",
        "update_reference_genome",
        "delete_reference_genome",
        "create_host_organism",
        "update_host_organism",
        "delete_host_organism",
        "create_metadatum",
        "update_metadatum",
        "delete_metadatum",
        "create_consensus_genome",
        "update_consensus_genome",
        "delete_consensus_genome",
        "create_metric_consensus_genome",
        "update_metric_consensus_genome",
        "delete_metric_consensus_genome",
        "create_taxon",
        "update_taxon",
        "delete_taxon",
        "create_upstream_database",
        "update_upstream_database",
        "delete_upstream_database",
        "create_contig",
        "update_contig",
        "delete_contig",
        "create_phylogenetic_tree",
        "update_phylogenetic_tree",
        "delete_phylogenetic_tree",
        "create_bulk_download",
        "update_bulk_download",
        "delete_bulk_download",
    )
    create_file = sgqlc.types.Field(
        sgqlc.types.non_null(File),
        graphql_name="createFile",
        args=sgqlc.types.ArgDict(
            (
                ("entity_id", sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name="entityId", default=None)),
                (
                    "entity_field_name",
                    sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="entityFieldName", default=None),
                ),
                ("file", sgqlc.types.Arg(sgqlc.types.non_null(FileCreate), graphql_name="file", default=None)),
            )
        ),
    )
    upload_file = sgqlc.types.Field(
        sgqlc.types.non_null(MultipartUploadResponse),
        graphql_name="uploadFile",
        args=sgqlc.types.ArgDict(
            (
                ("entity_id", sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name="entityId", default=None)),
                (
                    "entity_field_name",
                    sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="entityFieldName", default=None),
                ),
                ("file", sgqlc.types.Arg(sgqlc.types.non_null(FileUpload), graphql_name="file", default=None)),
                ("expiration", sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="expiration", default=3600)),
            )
        ),
    )
    mark_upload_complete = sgqlc.types.Field(
        sgqlc.types.non_null(File),
        graphql_name="markUploadComplete",
        args=sgqlc.types.ArgDict(
            (("file_id", sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name="fileId", default=None)),)
        ),
    )
    concatenate_files = sgqlc.types.Field(
        sgqlc.types.non_null("SignedURL"),
        graphql_name="concatenateFiles",
        args=sgqlc.types.ArgDict(
            (
                (
                    "ids",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(UUID))),
                        graphql_name="ids",
                        default=None,
                    ),
                ),
            )
        ),
    )
    create_sample = sgqlc.types.Field(
        sgqlc.types.non_null("Sample"),
        graphql_name="createSample",
        args=sgqlc.types.ArgDict(
            (("input", sgqlc.types.Arg(sgqlc.types.non_null(SampleCreateInput), graphql_name="input", default=None)),)
        ),
    )
    update_sample = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Sample"))),
        graphql_name="updateSample",
        args=sgqlc.types.ArgDict(
            (
                ("input", sgqlc.types.Arg(sgqlc.types.non_null(SampleUpdateInput), graphql_name="input", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SampleWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_sample = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Sample"))),
        graphql_name="deleteSample",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SampleWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    create_sequencing_read = sgqlc.types.Field(
        sgqlc.types.non_null("SequencingRead"),
        graphql_name="createSequencingRead",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SequencingReadCreateInput), graphql_name="input", default=None
                    ),
                ),
            )
        ),
    )
    update_sequencing_read = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("SequencingRead"))),
        graphql_name="updateSequencingRead",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SequencingReadUpdateInput), graphql_name="input", default=None
                    ),
                ),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SequencingReadWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_sequencing_read = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("SequencingRead"))),
        graphql_name="deleteSequencingRead",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SequencingReadWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    create_genomic_range = sgqlc.types.Field(
        sgqlc.types.non_null("GenomicRange"),
        graphql_name="createGenomicRange",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(sgqlc.types.non_null(GenomicRangeCreateInput), graphql_name="input", default=None),
                ),
            )
        ),
    )
    update_genomic_range = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("GenomicRange"))),
        graphql_name="updateGenomicRange",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(sgqlc.types.non_null(GenomicRangeUpdateInput), graphql_name="input", default=None),
                ),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(GenomicRangeWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_genomic_range = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("GenomicRange"))),
        graphql_name="deleteGenomicRange",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(GenomicRangeWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    create_reference_genome = sgqlc.types.Field(
        sgqlc.types.non_null("ReferenceGenome"),
        graphql_name="createReferenceGenome",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ReferenceGenomeCreateInput), graphql_name="input", default=None
                    ),
                ),
            )
        ),
    )
    update_reference_genome = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ReferenceGenome"))),
        graphql_name="updateReferenceGenome",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ReferenceGenomeUpdateInput), graphql_name="input", default=None
                    ),
                ),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ReferenceGenomeWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_reference_genome = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ReferenceGenome"))),
        graphql_name="deleteReferenceGenome",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ReferenceGenomeWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    create_host_organism = sgqlc.types.Field(
        sgqlc.types.non_null("HostOrganism"),
        graphql_name="createHostOrganism",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(sgqlc.types.non_null(HostOrganismCreateInput), graphql_name="input", default=None),
                ),
            )
        ),
    )
    update_host_organism = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("HostOrganism"))),
        graphql_name="updateHostOrganism",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(sgqlc.types.non_null(HostOrganismUpdateInput), graphql_name="input", default=None),
                ),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(HostOrganismWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_host_organism = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("HostOrganism"))),
        graphql_name="deleteHostOrganism",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(HostOrganismWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    create_metadatum = sgqlc.types.Field(
        sgqlc.types.non_null("Metadatum"),
        graphql_name="createMetadatum",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(sgqlc.types.non_null(MetadatumCreateInput), graphql_name="input", default=None),
                ),
            )
        ),
    )
    update_metadatum = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Metadatum"))),
        graphql_name="updateMetadatum",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(sgqlc.types.non_null(MetadatumUpdateInput), graphql_name="input", default=None),
                ),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(MetadatumWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_metadatum = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Metadatum"))),
        graphql_name="deleteMetadatum",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(MetadatumWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    create_consensus_genome = sgqlc.types.Field(
        sgqlc.types.non_null("ConsensusGenome"),
        graphql_name="createConsensusGenome",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ConsensusGenomeCreateInput), graphql_name="input", default=None
                    ),
                ),
            )
        ),
    )
    update_consensus_genome = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ConsensusGenome"))),
        graphql_name="updateConsensusGenome",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ConsensusGenomeUpdateInput), graphql_name="input", default=None
                    ),
                ),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ConsensusGenomeWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_consensus_genome = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ConsensusGenome"))),
        graphql_name="deleteConsensusGenome",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ConsensusGenomeWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    create_metric_consensus_genome = sgqlc.types.Field(
        sgqlc.types.non_null("MetricConsensusGenome"),
        graphql_name="createMetricConsensusGenome",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(MetricConsensusGenomeCreateInput), graphql_name="input", default=None
                    ),
                ),
            )
        ),
    )
    update_metric_consensus_genome = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("MetricConsensusGenome"))),
        graphql_name="updateMetricConsensusGenome",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(MetricConsensusGenomeUpdateInput), graphql_name="input", default=None
                    ),
                ),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(MetricConsensusGenomeWhereClauseMutations),
                        graphql_name="where",
                        default=None,
                    ),
                ),
            )
        ),
    )
    delete_metric_consensus_genome = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("MetricConsensusGenome"))),
        graphql_name="deleteMetricConsensusGenome",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(MetricConsensusGenomeWhereClauseMutations),
                        graphql_name="where",
                        default=None,
                    ),
                ),
            )
        ),
    )
    create_taxon = sgqlc.types.Field(
        sgqlc.types.non_null("Taxon"),
        graphql_name="createTaxon",
        args=sgqlc.types.ArgDict(
            (("input", sgqlc.types.Arg(sgqlc.types.non_null(TaxonCreateInput), graphql_name="input", default=None)),)
        ),
    )
    update_taxon = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Taxon"))),
        graphql_name="updateTaxon",
        args=sgqlc.types.ArgDict(
            (
                ("input", sgqlc.types.Arg(sgqlc.types.non_null(TaxonUpdateInput), graphql_name="input", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(TaxonWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_taxon = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Taxon"))),
        graphql_name="deleteTaxon",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(TaxonWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    create_upstream_database = sgqlc.types.Field(
        sgqlc.types.non_null("UpstreamDatabase"),
        graphql_name="createUpstreamDatabase",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(UpstreamDatabaseCreateInput), graphql_name="input", default=None
                    ),
                ),
            )
        ),
    )
    update_upstream_database = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("UpstreamDatabase"))),
        graphql_name="updateUpstreamDatabase",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(UpstreamDatabaseUpdateInput), graphql_name="input", default=None
                    ),
                ),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(UpstreamDatabaseWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_upstream_database = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("UpstreamDatabase"))),
        graphql_name="deleteUpstreamDatabase",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(UpstreamDatabaseWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    create_contig = sgqlc.types.Field(
        sgqlc.types.non_null("Contig"),
        graphql_name="createContig",
        args=sgqlc.types.ArgDict(
            (("input", sgqlc.types.Arg(sgqlc.types.non_null(ContigCreateInput), graphql_name="input", default=None)),)
        ),
    )
    update_contig = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Contig"))),
        graphql_name="updateContig",
        args=sgqlc.types.ArgDict(
            (
                ("input", sgqlc.types.Arg(sgqlc.types.non_null(ContigUpdateInput), graphql_name="input", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ContigWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_contig = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Contig"))),
        graphql_name="deleteContig",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ContigWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    create_phylogenetic_tree = sgqlc.types.Field(
        sgqlc.types.non_null("PhylogeneticTree"),
        graphql_name="createPhylogeneticTree",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(PhylogeneticTreeCreateInput), graphql_name="input", default=None
                    ),
                ),
            )
        ),
    )
    update_phylogenetic_tree = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("PhylogeneticTree"))),
        graphql_name="updatePhylogeneticTree",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(PhylogeneticTreeUpdateInput), graphql_name="input", default=None
                    ),
                ),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(PhylogeneticTreeWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_phylogenetic_tree = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("PhylogeneticTree"))),
        graphql_name="deletePhylogeneticTree",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(PhylogeneticTreeWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    create_bulk_download = sgqlc.types.Field(
        sgqlc.types.non_null("BulkDownload"),
        graphql_name="createBulkDownload",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(sgqlc.types.non_null(BulkDownloadCreateInput), graphql_name="input", default=None),
                ),
            )
        ),
    )
    update_bulk_download = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("BulkDownload"))),
        graphql_name="updateBulkDownload",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(sgqlc.types.non_null(BulkDownloadUpdateInput), graphql_name="input", default=None),
                ),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(BulkDownloadWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_bulk_download = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("BulkDownload"))),
        graphql_name="deleteBulkDownload",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(BulkDownloadWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )


class PageInfo(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("has_next_page", "has_previous_page", "start_cursor", "end_cursor")
    has_next_page = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="hasNextPage")
    has_previous_page = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="hasPreviousPage")
    start_cursor = sgqlc.types.Field(String, graphql_name="startCursor")
    end_cursor = sgqlc.types.Field(String, graphql_name="endCursor")


class PhylogeneticTreeAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field("PhylogeneticTreeAggregateFunctions", graphql_name="aggregate")


class PhylogeneticTreeAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "min", "max", "stddev", "variance", "count")
    sum = sgqlc.types.Field("PhylogeneticTreeNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("PhylogeneticTreeNumericalColumns", graphql_name="avg")
    min = sgqlc.types.Field("PhylogeneticTreeMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("PhylogeneticTreeMinMaxColumns", graphql_name="max")
    stddev = sgqlc.types.Field("PhylogeneticTreeNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("PhylogeneticTreeNumericalColumns", graphql_name="variance")
    count = sgqlc.types.Field(
        Int,
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=False)),
                ("columns", sgqlc.types.Arg(PhylogeneticTreeCountColumns, graphql_name="columns", default=None)),
            )
        ),
    )


class PhylogeneticTreeMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class PhylogeneticTreeNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class Query(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "node",
        "nodes",
        "files",
        "samples",
        "sequencing_reads",
        "genomic_ranges",
        "reference_genomes",
        "host_organisms",
        "metadatas",
        "consensus_genomes",
        "metrics_consensus_genomes",
        "taxa",
        "upstream_databases",
        "contigs",
        "phylogenetic_trees",
        "bulk_downloads",
        "samples_aggregate",
        "sequencing_reads_aggregate",
        "genomic_ranges_aggregate",
        "reference_genomes_aggregate",
        "host_organisms_aggregate",
        "metadatas_aggregate",
        "consensus_genomes_aggregate",
        "metrics_consensus_genomes_aggregate",
        "taxa_aggregate",
        "upstream_databases_aggregate",
        "contigs_aggregate",
        "phylogenetic_trees_aggregate",
        "bulk_downloads_aggregate",
    )
    node = sgqlc.types.Field(
        sgqlc.types.non_null(Node),
        graphql_name="node",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(GlobalID), graphql_name="id", default=None)),)
        ),
    )
    nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Node))),
        graphql_name="nodes",
        args=sgqlc.types.ArgDict(
            (
                (
                    "ids",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(GlobalID))),
                        graphql_name="ids",
                        default=None,
                    ),
                ),
            )
        ),
    )
    files = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(File))),
        graphql_name="files",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(FileWhereClause, graphql_name="where", default=None)),)),
    )
    samples = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Sample"))),
        graphql_name="samples",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(SampleWhereClause, graphql_name="where", default=None)),)),
    )
    sequencing_reads = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("SequencingRead"))),
        graphql_name="sequencingReads",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(SequencingReadWhereClause, graphql_name="where", default=None)),)
        ),
    )
    genomic_ranges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("GenomicRange"))),
        graphql_name="genomicRanges",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(GenomicRangeWhereClause, graphql_name="where", default=None)),)
        ),
    )
    reference_genomes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ReferenceGenome"))),
        graphql_name="referenceGenomes",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(ReferenceGenomeWhereClause, graphql_name="where", default=None)),)
        ),
    )
    host_organisms = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("HostOrganism"))),
        graphql_name="hostOrganisms",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(HostOrganismWhereClause, graphql_name="where", default=None)),)
        ),
    )
    metadatas = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Metadatum"))),
        graphql_name="metadatas",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(MetadatumWhereClause, graphql_name="where", default=None)),)
        ),
    )
    consensus_genomes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ConsensusGenome"))),
        graphql_name="consensusGenomes",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(ConsensusGenomeWhereClause, graphql_name="where", default=None)),)
        ),
    )
    metrics_consensus_genomes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("MetricConsensusGenome"))),
        graphql_name="metricsConsensusGenomes",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(MetricConsensusGenomeWhereClause, graphql_name="where", default=None)),)
        ),
    )
    taxa = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Taxon"))),
        graphql_name="taxa",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(TaxonWhereClause, graphql_name="where", default=None)),)),
    )
    upstream_databases = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("UpstreamDatabase"))),
        graphql_name="upstreamDatabases",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(UpstreamDatabaseWhereClause, graphql_name="where", default=None)),)
        ),
    )
    contigs = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Contig"))),
        graphql_name="contigs",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(ContigWhereClause, graphql_name="where", default=None)),)),
    )
    phylogenetic_trees = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("PhylogeneticTree"))),
        graphql_name="phylogeneticTrees",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(PhylogeneticTreeWhereClause, graphql_name="where", default=None)),)
        ),
    )
    bulk_downloads = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("BulkDownload"))),
        graphql_name="bulkDownloads",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(BulkDownloadWhereClause, graphql_name="where", default=None)),)
        ),
    )
    samples_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("SampleAggregate"),
        graphql_name="samplesAggregate",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(SampleWhereClause, graphql_name="where", default=None)),)),
    )
    sequencing_reads_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("SequencingReadAggregate"),
        graphql_name="sequencingReadsAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(SequencingReadWhereClause, graphql_name="where", default=None)),)
        ),
    )
    genomic_ranges_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null(GenomicRangeAggregate),
        graphql_name="genomicRangesAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(GenomicRangeWhereClause, graphql_name="where", default=None)),)
        ),
    )
    reference_genomes_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("ReferenceGenomeAggregate"),
        graphql_name="referenceGenomesAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(ReferenceGenomeWhereClause, graphql_name="where", default=None)),)
        ),
    )
    host_organisms_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null(HostOrganismAggregate),
        graphql_name="hostOrganismsAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(HostOrganismWhereClause, graphql_name="where", default=None)),)
        ),
    )
    metadatas_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null(MetadatumAggregate),
        graphql_name="metadatasAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(MetadatumWhereClause, graphql_name="where", default=None)),)
        ),
    )
    consensus_genomes_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null(ConsensusGenomeAggregate),
        graphql_name="consensusGenomesAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(ConsensusGenomeWhereClause, graphql_name="where", default=None)),)
        ),
    )
    metrics_consensus_genomes_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null(MetricConsensusGenomeAggregate),
        graphql_name="metricsConsensusGenomesAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(MetricConsensusGenomeWhereClause, graphql_name="where", default=None)),)
        ),
    )
    taxa_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("TaxonAggregate"),
        graphql_name="taxaAggregate",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(TaxonWhereClause, graphql_name="where", default=None)),)),
    )
    upstream_databases_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("UpstreamDatabaseAggregate"),
        graphql_name="upstreamDatabasesAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(UpstreamDatabaseWhereClause, graphql_name="where", default=None)),)
        ),
    )
    contigs_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null(ContigAggregate),
        graphql_name="contigsAggregate",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(ContigWhereClause, graphql_name="where", default=None)),)),
    )
    phylogenetic_trees_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null(PhylogeneticTreeAggregate),
        graphql_name="phylogeneticTreesAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(PhylogeneticTreeWhereClause, graphql_name="where", default=None)),)
        ),
    )
    bulk_downloads_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null(BulkDownloadAggregate),
        graphql_name="bulkDownloadsAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(BulkDownloadWhereClause, graphql_name="where", default=None)),)
        ),
    )


class ReferenceGenomeAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field("ReferenceGenomeAggregateFunctions", graphql_name="aggregate")


class ReferenceGenomeAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "min", "max", "stddev", "variance", "count")
    sum = sgqlc.types.Field("ReferenceGenomeNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("ReferenceGenomeNumericalColumns", graphql_name="avg")
    min = sgqlc.types.Field("ReferenceGenomeMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("ReferenceGenomeMinMaxColumns", graphql_name="max")
    stddev = sgqlc.types.Field("ReferenceGenomeNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("ReferenceGenomeNumericalColumns", graphql_name="variance")
    count = sgqlc.types.Field(
        Int,
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=False)),
                ("columns", sgqlc.types.Arg(ReferenceGenomeCountColumns, graphql_name="columns", default=None)),
            )
        ),
    )


class ReferenceGenomeConnection(sgqlc.types.relay.Connection):
    __schema__ = gql_schema
    __field_names__ = ("page_info", "edges")
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name="pageInfo")
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ReferenceGenomeEdge"))), graphql_name="edges"
    )


class ReferenceGenomeEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("cursor", "node")
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="cursor")
    node = sgqlc.types.Field(sgqlc.types.non_null("ReferenceGenome"), graphql_name="node")


class ReferenceGenomeMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id", "accession_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    accession_id = sgqlc.types.Field(String, graphql_name="accessionId")


class ReferenceGenomeNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class SampleAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field("SampleAggregateFunctions", graphql_name="aggregate")


class SampleAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "min", "max", "stddev", "variance", "count")
    sum = sgqlc.types.Field("SampleNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("SampleNumericalColumns", graphql_name="avg")
    min = sgqlc.types.Field("SampleMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("SampleMinMaxColumns", graphql_name="max")
    stddev = sgqlc.types.Field("SampleNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("SampleNumericalColumns", graphql_name="variance")
    count = sgqlc.types.Field(
        Int,
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=False)),
                ("columns", sgqlc.types.Arg(SampleCountColumns, graphql_name="columns", default=None)),
            )
        ),
    )


class SampleConnection(sgqlc.types.relay.Connection):
    __schema__ = gql_schema
    __field_names__ = ("page_info", "edges")
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name="pageInfo")
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("SampleEdge"))), graphql_name="edges"
    )


class SampleEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("cursor", "node")
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="cursor")
    node = sgqlc.types.Field(sgqlc.types.non_null("Sample"), graphql_name="node")


class SampleMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "rails_sample_id",
        "name",
        "sample_type",
        "collection_date",
        "collection_location",
        "description",
    )
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    rails_sample_id = sgqlc.types.Field(Int, graphql_name="railsSampleId")
    name = sgqlc.types.Field(String, graphql_name="name")
    sample_type = sgqlc.types.Field(String, graphql_name="sampleType")
    collection_date = sgqlc.types.Field(DateTime, graphql_name="collectionDate")
    collection_location = sgqlc.types.Field(String, graphql_name="collectionLocation")
    description = sgqlc.types.Field(String, graphql_name="description")


class SampleNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id", "rails_sample_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    rails_sample_id = sgqlc.types.Field(Int, graphql_name="railsSampleId")


class SequencingReadAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field("SequencingReadAggregateFunctions", graphql_name="aggregate")


class SequencingReadAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "min", "max", "stddev", "variance", "count")
    sum = sgqlc.types.Field("SequencingReadNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("SequencingReadNumericalColumns", graphql_name="avg")
    min = sgqlc.types.Field("SequencingReadMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("SequencingReadMinMaxColumns", graphql_name="max")
    stddev = sgqlc.types.Field("SequencingReadNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("SequencingReadNumericalColumns", graphql_name="variance")
    count = sgqlc.types.Field(
        Int,
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=False)),
                ("columns", sgqlc.types.Arg(SequencingReadCountColumns, graphql_name="columns", default=None)),
            )
        ),
    )


class SequencingReadConnection(sgqlc.types.relay.Connection):
    __schema__ = gql_schema
    __field_names__ = ("page_info", "edges")
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name="pageInfo")
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("SequencingReadEdge"))), graphql_name="edges"
    )


class SequencingReadEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("cursor", "node")
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="cursor")
    node = sgqlc.types.Field(sgqlc.types.non_null("SequencingRead"), graphql_name="node")


class SequencingReadMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class SequencingReadNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class SignedURL(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("url", "protocol", "method", "expiration", "fields")
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="url")
    protocol = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="protocol")
    method = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="method")
    expiration = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="expiration")
    fields = sgqlc.types.Field(JSON, graphql_name="fields")


class TaxonAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field("TaxonAggregateFunctions", graphql_name="aggregate")


class TaxonAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "min", "max", "stddev", "variance", "count")
    sum = sgqlc.types.Field("TaxonNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("TaxonNumericalColumns", graphql_name="avg")
    min = sgqlc.types.Field("TaxonMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("TaxonMinMaxColumns", graphql_name="max")
    stddev = sgqlc.types.Field("TaxonNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("TaxonNumericalColumns", graphql_name="variance")
    count = sgqlc.types.Field(
        Int,
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=False)),
                ("columns", sgqlc.types.Arg(TaxonCountColumns, graphql_name="columns", default=None)),
            )
        ),
    )


class TaxonConnection(sgqlc.types.relay.Connection):
    __schema__ = gql_schema
    __field_names__ = ("page_info", "edges")
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name="pageInfo")
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("TaxonEdge"))), graphql_name="edges"
    )


class TaxonEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("cursor", "node")
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="cursor")
    node = sgqlc.types.Field(sgqlc.types.non_null("Taxon"), graphql_name="node")


class TaxonMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "wikipedia_id",
        "description",
        "common_name",
        "name",
        "upstream_database_identifier",
    )
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    wikipedia_id = sgqlc.types.Field(String, graphql_name="wikipediaId")
    description = sgqlc.types.Field(String, graphql_name="description")
    common_name = sgqlc.types.Field(String, graphql_name="commonName")
    name = sgqlc.types.Field(String, graphql_name="name")
    upstream_database_identifier = sgqlc.types.Field(String, graphql_name="upstreamDatabaseIdentifier")


class TaxonNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class UpstreamDatabaseAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field("UpstreamDatabaseAggregateFunctions", graphql_name="aggregate")


class UpstreamDatabaseAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "min", "max", "stddev", "variance", "count")
    sum = sgqlc.types.Field("UpstreamDatabaseNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("UpstreamDatabaseNumericalColumns", graphql_name="avg")
    min = sgqlc.types.Field("UpstreamDatabaseMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("UpstreamDatabaseMinMaxColumns", graphql_name="max")
    stddev = sgqlc.types.Field("UpstreamDatabaseNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("UpstreamDatabaseNumericalColumns", graphql_name="variance")
    count = sgqlc.types.Field(
        Int,
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=False)),
                ("columns", sgqlc.types.Arg(UpstreamDatabaseCountColumns, graphql_name="columns", default=None)),
            )
        ),
    )


class UpstreamDatabaseMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id", "name")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    name = sgqlc.types.Field(String, graphql_name="name")


class UpstreamDatabaseNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class BulkDownload(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = ("id", "producing_run_id", "owner_user_id", "collection_id", "download_type", "file_id", "file")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    download_type = sgqlc.types.Field(sgqlc.types.non_null(BulkDownloadType), graphql_name="downloadType")
    file_id = sgqlc.types.Field(ID, graphql_name="fileId")
    file = sgqlc.types.Field(
        File,
        graphql_name="file",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(FileWhereClause, graphql_name="where", default=None)),)),
    )


class ConsensusGenome(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "taxon",
        "sequence_read",
        "reference_genome",
        "sequence_id",
        "sequence",
        "metrics",
        "metrics_aggregate",
        "intermediate_outputs_id",
        "intermediate_outputs",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    taxon = sgqlc.types.Field(
        "Taxon",
        graphql_name="taxon",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(TaxonWhereClause, graphql_name="where", default=None)),)),
    )
    sequence_read = sgqlc.types.Field(
        "SequencingRead",
        graphql_name="sequenceRead",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(SequencingReadWhereClause, graphql_name="where", default=None)),)
        ),
    )
    reference_genome = sgqlc.types.Field(
        "ReferenceGenome",
        graphql_name="referenceGenome",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(ReferenceGenomeWhereClause, graphql_name="where", default=None)),)
        ),
    )
    sequence_id = sgqlc.types.Field(ID, graphql_name="sequenceId")
    sequence = sgqlc.types.Field(
        File,
        graphql_name="sequence",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(FileWhereClause, graphql_name="where", default=None)),)),
    )
    metrics = sgqlc.types.Field(
        sgqlc.types.non_null(MetricConsensusGenomeConnection),
        graphql_name="metrics",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(MetricConsensusGenomeWhereClause, graphql_name="where", default=None)),
                ("before", sgqlc.types.Arg(String, graphql_name="before", default=None)),
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
            )
        ),
    )
    metrics_aggregate = sgqlc.types.Field(
        MetricConsensusGenomeAggregate,
        graphql_name="metricsAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(MetricConsensusGenomeWhereClause, graphql_name="where", default=None)),)
        ),
    )
    intermediate_outputs_id = sgqlc.types.Field(ID, graphql_name="intermediateOutputsId")
    intermediate_outputs = sgqlc.types.Field(
        File,
        graphql_name="intermediateOutputs",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(FileWhereClause, graphql_name="where", default=None)),)),
    )


class Contig(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = ("id", "producing_run_id", "owner_user_id", "collection_id", "sequencing_read", "sequence")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    sequencing_read = sgqlc.types.Field(
        "SequencingRead",
        graphql_name="sequencingRead",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(SequencingReadWhereClause, graphql_name="where", default=None)),)
        ),
    )
    sequence = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="sequence")


class GenomicRange(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "reference_genome",
        "file_id",
        "file",
        "sequencing_reads",
        "sequencing_reads_aggregate",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    reference_genome = sgqlc.types.Field(
        "ReferenceGenome",
        graphql_name="referenceGenome",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(ReferenceGenomeWhereClause, graphql_name="where", default=None)),)
        ),
    )
    file_id = sgqlc.types.Field(ID, graphql_name="fileId")
    file = sgqlc.types.Field(
        File,
        graphql_name="file",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(FileWhereClause, graphql_name="where", default=None)),)),
    )
    sequencing_reads = sgqlc.types.Field(
        sgqlc.types.non_null(SequencingReadConnection),
        graphql_name="sequencingReads",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(SequencingReadWhereClause, graphql_name="where", default=None)),
                ("before", sgqlc.types.Arg(String, graphql_name="before", default=None)),
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
            )
        ),
    )
    sequencing_reads_aggregate = sgqlc.types.Field(
        SequencingReadAggregate,
        graphql_name="sequencingReadsAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(SequencingReadWhereClause, graphql_name="where", default=None)),)
        ),
    )


class HostOrganism(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "name",
        "version",
        "host_filtering_id",
        "host_filtering",
        "sequence_id",
        "sequence",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    version = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="version")
    host_filtering_id = sgqlc.types.Field(ID, graphql_name="hostFilteringId")
    host_filtering = sgqlc.types.Field(
        File,
        graphql_name="hostFiltering",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(FileWhereClause, graphql_name="where", default=None)),)),
    )
    sequence_id = sgqlc.types.Field(ID, graphql_name="sequenceId")
    sequence = sgqlc.types.Field(
        File,
        graphql_name="sequence",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(FileWhereClause, graphql_name="where", default=None)),)),
    )


class Metadatum(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = ("id", "producing_run_id", "owner_user_id", "collection_id", "sample", "field_name", "value")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    sample = sgqlc.types.Field(
        "Sample",
        graphql_name="sample",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(SampleWhereClause, graphql_name="where", default=None)),)),
    )
    field_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="fieldName")
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="value")


class MetricConsensusGenome(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "consensus_genome",
        "reference_genome_length",
        "percent_genome_called",
        "percent_identity",
        "gc_percent",
        "total_reads",
        "mapped_reads",
        "ref_snps",
        "n_actg",
        "n_missing",
        "n_ambiguous",
        "coverage_depth",
        "coverage_breadth",
        "coverage_bin_size",
        "coverage_total_length",
        "coverage_viz",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    consensus_genome = sgqlc.types.Field(
        ConsensusGenome,
        graphql_name="consensusGenome",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(ConsensusGenomeWhereClause, graphql_name="where", default=None)),)
        ),
    )
    reference_genome_length = sgqlc.types.Field(Float, graphql_name="referenceGenomeLength")
    percent_genome_called = sgqlc.types.Field(Float, graphql_name="percentGenomeCalled")
    percent_identity = sgqlc.types.Field(Float, graphql_name="percentIdentity")
    gc_percent = sgqlc.types.Field(Float, graphql_name="gcPercent")
    total_reads = sgqlc.types.Field(Int, graphql_name="totalReads")
    mapped_reads = sgqlc.types.Field(Int, graphql_name="mappedReads")
    ref_snps = sgqlc.types.Field(Int, graphql_name="refSnps")
    n_actg = sgqlc.types.Field(Int, graphql_name="nActg")
    n_missing = sgqlc.types.Field(Int, graphql_name="nMissing")
    n_ambiguous = sgqlc.types.Field(Int, graphql_name="nAmbiguous")
    coverage_depth = sgqlc.types.Field(Float, graphql_name="coverageDepth")
    coverage_breadth = sgqlc.types.Field(Float, graphql_name="coverageBreadth")
    coverage_bin_size = sgqlc.types.Field(Float, graphql_name="coverageBinSize")
    coverage_total_length = sgqlc.types.Field(Int, graphql_name="coverageTotalLength")
    coverage_viz = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Int)))),
        graphql_name="coverageViz",
    )


class PhylogeneticTree(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = ("id", "producing_run_id", "owner_user_id", "collection_id", "tree_id", "tree", "format")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    tree_id = sgqlc.types.Field(ID, graphql_name="treeId")
    tree = sgqlc.types.Field(
        File,
        graphql_name="tree",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(FileWhereClause, graphql_name="where", default=None)),)),
    )
    format = sgqlc.types.Field(sgqlc.types.non_null(PhylogeneticTreeFormat), graphql_name="format")


class ReferenceGenome(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "file_id",
        "file",
        "taxon",
        "accession_id",
        "consensus_genomes",
        "consensus_genomes_aggregate",
        "genomic_ranges",
        "genomic_ranges_aggregate",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    file_id = sgqlc.types.Field(ID, graphql_name="fileId")
    file = sgqlc.types.Field(
        File,
        graphql_name="file",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(FileWhereClause, graphql_name="where", default=None)),)),
    )
    taxon = sgqlc.types.Field(
        "Taxon",
        graphql_name="taxon",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(TaxonWhereClause, graphql_name="where", default=None)),)),
    )
    accession_id = sgqlc.types.Field(String, graphql_name="accessionId")
    consensus_genomes = sgqlc.types.Field(
        sgqlc.types.non_null(ConsensusGenomeConnection),
        graphql_name="consensusGenomes",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(ConsensusGenomeWhereClause, graphql_name="where", default=None)),
                ("before", sgqlc.types.Arg(String, graphql_name="before", default=None)),
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
            )
        ),
    )
    consensus_genomes_aggregate = sgqlc.types.Field(
        ConsensusGenomeAggregate,
        graphql_name="consensusGenomesAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(ConsensusGenomeWhereClause, graphql_name="where", default=None)),)
        ),
    )
    genomic_ranges = sgqlc.types.Field(
        sgqlc.types.non_null(GenomicRangeConnection),
        graphql_name="genomicRanges",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(GenomicRangeWhereClause, graphql_name="where", default=None)),
                ("before", sgqlc.types.Arg(String, graphql_name="before", default=None)),
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
            )
        ),
    )
    genomic_ranges_aggregate = sgqlc.types.Field(
        GenomicRangeAggregate,
        graphql_name="genomicRangesAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(GenomicRangeWhereClause, graphql_name="where", default=None)),)
        ),
    )


class Sample(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "rails_sample_id",
        "name",
        "sample_type",
        "water_control",
        "collection_date",
        "collection_location",
        "description",
        "host_taxon",
        "sequencing_reads",
        "sequencing_reads_aggregate",
        "metadatas",
        "metadatas_aggregate",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    rails_sample_id = sgqlc.types.Field(Int, graphql_name="railsSampleId")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    sample_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="sampleType")
    water_control = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="waterControl")
    collection_date = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name="collectionDate")
    collection_location = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="collectionLocation")
    description = sgqlc.types.Field(String, graphql_name="description")
    host_taxon = sgqlc.types.Field(
        "Taxon",
        graphql_name="hostTaxon",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(TaxonWhereClause, graphql_name="where", default=None)),)),
    )
    sequencing_reads = sgqlc.types.Field(
        sgqlc.types.non_null(SequencingReadConnection),
        graphql_name="sequencingReads",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(SequencingReadWhereClause, graphql_name="where", default=None)),
                ("before", sgqlc.types.Arg(String, graphql_name="before", default=None)),
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
            )
        ),
    )
    sequencing_reads_aggregate = sgqlc.types.Field(
        SequencingReadAggregate,
        graphql_name="sequencingReadsAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(SequencingReadWhereClause, graphql_name="where", default=None)),)
        ),
    )
    metadatas = sgqlc.types.Field(
        sgqlc.types.non_null(MetadatumConnection),
        graphql_name="metadatas",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(MetadatumWhereClause, graphql_name="where", default=None)),
                ("before", sgqlc.types.Arg(String, graphql_name="before", default=None)),
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
            )
        ),
    )
    metadatas_aggregate = sgqlc.types.Field(
        MetadatumAggregate,
        graphql_name="metadatasAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(MetadatumWhereClause, graphql_name="where", default=None)),)
        ),
    )


class SequencingRead(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "sample",
        "protocol",
        "r1_file_id",
        "r1_file",
        "r2_file_id",
        "r2_file",
        "technology",
        "nucleic_acid",
        "taxon",
        "primer_file",
        "consensus_genomes",
        "consensus_genomes_aggregate",
        "contigs",
        "contigs_aggregate",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    sample = sgqlc.types.Field(
        Sample,
        graphql_name="sample",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(SampleWhereClause, graphql_name="where", default=None)),)),
    )
    protocol = sgqlc.types.Field(SequencingProtocol, graphql_name="protocol")
    r1_file_id = sgqlc.types.Field(ID, graphql_name="r1FileId")
    r1_file = sgqlc.types.Field(
        File,
        graphql_name="r1File",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(FileWhereClause, graphql_name="where", default=None)),)),
    )
    r2_file_id = sgqlc.types.Field(ID, graphql_name="r2FileId")
    r2_file = sgqlc.types.Field(
        File,
        graphql_name="r2File",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(FileWhereClause, graphql_name="where", default=None)),)),
    )
    technology = sgqlc.types.Field(sgqlc.types.non_null(SequencingTechnology), graphql_name="technology")
    nucleic_acid = sgqlc.types.Field(sgqlc.types.non_null(NucleicAcid), graphql_name="nucleicAcid")
    taxon = sgqlc.types.Field(
        "Taxon",
        graphql_name="taxon",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(TaxonWhereClause, graphql_name="where", default=None)),)),
    )
    primer_file = sgqlc.types.Field(
        GenomicRange,
        graphql_name="primerFile",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(GenomicRangeWhereClause, graphql_name="where", default=None)),)
        ),
    )
    consensus_genomes = sgqlc.types.Field(
        sgqlc.types.non_null(ConsensusGenomeConnection),
        graphql_name="consensusGenomes",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(ConsensusGenomeWhereClause, graphql_name="where", default=None)),
                ("before", sgqlc.types.Arg(String, graphql_name="before", default=None)),
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
            )
        ),
    )
    consensus_genomes_aggregate = sgqlc.types.Field(
        ConsensusGenomeAggregate,
        graphql_name="consensusGenomesAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(ConsensusGenomeWhereClause, graphql_name="where", default=None)),)
        ),
    )
    contigs = sgqlc.types.Field(
        sgqlc.types.non_null(ContigConnection),
        graphql_name="contigs",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(ContigWhereClause, graphql_name="where", default=None)),
                ("before", sgqlc.types.Arg(String, graphql_name="before", default=None)),
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
            )
        ),
    )
    contigs_aggregate = sgqlc.types.Field(
        ContigAggregate,
        graphql_name="contigsAggregate",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(ContigWhereClause, graphql_name="where", default=None)),)),
    )


class Taxon(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "wikipedia_id",
        "description",
        "common_name",
        "name",
        "is_phage",
        "upstream_database",
        "upstream_database_identifier",
        "level",
        "consensus_genomes",
        "consensus_genomes_aggregate",
        "reference_genomes",
        "reference_genomes_aggregate",
        "sequencing_reads",
        "sequencing_reads_aggregate",
        "samples",
        "samples_aggregate",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    wikipedia_id = sgqlc.types.Field(String, graphql_name="wikipediaId")
    description = sgqlc.types.Field(String, graphql_name="description")
    common_name = sgqlc.types.Field(String, graphql_name="commonName")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    is_phage = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="isPhage")
    upstream_database = sgqlc.types.Field(
        "UpstreamDatabase",
        graphql_name="upstreamDatabase",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(UpstreamDatabaseWhereClause, graphql_name="where", default=None)),)
        ),
    )
    upstream_database_identifier = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="upstreamDatabaseIdentifier"
    )
    level = sgqlc.types.Field(sgqlc.types.non_null(TaxonLevel), graphql_name="level")
    consensus_genomes = sgqlc.types.Field(
        sgqlc.types.non_null(ConsensusGenomeConnection),
        graphql_name="consensusGenomes",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(ConsensusGenomeWhereClause, graphql_name="where", default=None)),
                ("before", sgqlc.types.Arg(String, graphql_name="before", default=None)),
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
            )
        ),
    )
    consensus_genomes_aggregate = sgqlc.types.Field(
        ConsensusGenomeAggregate,
        graphql_name="consensusGenomesAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(ConsensusGenomeWhereClause, graphql_name="where", default=None)),)
        ),
    )
    reference_genomes = sgqlc.types.Field(
        sgqlc.types.non_null(ReferenceGenomeConnection),
        graphql_name="referenceGenomes",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(ReferenceGenomeWhereClause, graphql_name="where", default=None)),
                ("before", sgqlc.types.Arg(String, graphql_name="before", default=None)),
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
            )
        ),
    )
    reference_genomes_aggregate = sgqlc.types.Field(
        ReferenceGenomeAggregate,
        graphql_name="referenceGenomesAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(ReferenceGenomeWhereClause, graphql_name="where", default=None)),)
        ),
    )
    sequencing_reads = sgqlc.types.Field(
        sgqlc.types.non_null(SequencingReadConnection),
        graphql_name="sequencingReads",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(SequencingReadWhereClause, graphql_name="where", default=None)),
                ("before", sgqlc.types.Arg(String, graphql_name="before", default=None)),
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
            )
        ),
    )
    sequencing_reads_aggregate = sgqlc.types.Field(
        SequencingReadAggregate,
        graphql_name="sequencingReadsAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(SequencingReadWhereClause, graphql_name="where", default=None)),)
        ),
    )
    samples = sgqlc.types.Field(
        sgqlc.types.non_null(SampleConnection),
        graphql_name="samples",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(SampleWhereClause, graphql_name="where", default=None)),
                ("before", sgqlc.types.Arg(String, graphql_name="before", default=None)),
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
            )
        ),
    )
    samples_aggregate = sgqlc.types.Field(
        SampleAggregate,
        graphql_name="samplesAggregate",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(SampleWhereClause, graphql_name="where", default=None)),)),
    )


class UpstreamDatabase(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = ("id", "producing_run_id", "owner_user_id", "collection_id", "name", "taxa", "taxa_aggregate")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    taxa = sgqlc.types.Field(
        sgqlc.types.non_null(TaxonConnection),
        graphql_name="taxa",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(TaxonWhereClause, graphql_name="where", default=None)),
                ("before", sgqlc.types.Arg(String, graphql_name="before", default=None)),
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
            )
        ),
    )
    taxa_aggregate = sgqlc.types.Field(
        TaxonAggregate,
        graphql_name="taxaAggregate",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(TaxonWhereClause, graphql_name="where", default=None)),)),
    )


########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
gql_schema.query_type = Query
gql_schema.mutation_type = Mutation
gql_schema.subscription_type = None
