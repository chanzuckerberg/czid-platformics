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
class AlignmentTool(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("bowtie2", "minimap2", "ncbi")


Boolean = sgqlc.types.Boolean

DateTime = sgqlc.types.datetime.DateTime


class FileStatus(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("FAILED", "PENDING", "SUCCESS")


class GlobalID(sgqlc.types.Scalar):
    __schema__ = gql_schema


ID = sgqlc.types.ID

Int = sgqlc.types.Int


class JSON(sgqlc.types.Scalar):
    __schema__ = gql_schema


class NucleicAcid(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("DNA", "RNA")


class PhylogeneticTreeFormat(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("auspice_v1", "auspice_v2", "newick")


class SequencingProtocol(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("MNGS", "MSSPE", "TARGETED")


class SequencingTechnology(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("Illumina", "Nanopore")


String = sgqlc.types.String


class TaxonLevel(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("family", "genus", "species")


class UUID(sgqlc.types.Scalar):
    __schema__ = gql_schema


########################################################################
# Input Objects
########################################################################
class AlignmentToolEnumComparators(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("_eq", "_neq", "_in", "_nin", "_gt", "_gte", "_lt", "_lte", "_is_null")
    _eq = sgqlc.types.Field(AlignmentTool, graphql_name="_eq")
    _neq = sgqlc.types.Field(AlignmentTool, graphql_name="_neq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(AlignmentTool)), graphql_name="_in")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(AlignmentTool)), graphql_name="_nin")
    _gt = sgqlc.types.Field(AlignmentTool, graphql_name="_gt")
    _gte = sgqlc.types.Field(AlignmentTool, graphql_name="_gte")
    _lt = sgqlc.types.Field(AlignmentTool, graphql_name="_lt")
    _lte = sgqlc.types.Field(AlignmentTool, graphql_name="_lte")
    _is_null = sgqlc.types.Field(AlignmentTool, graphql_name="_is_null")


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
    protocol = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="protocol")
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
    __field_names__ = ("id", "status", "protocol", "namespace", "path", "compression_type", "size")
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    status = sgqlc.types.Field(FileStatusEnumComparators, graphql_name="status")
    protocol = sgqlc.types.Field("StrComparators", graphql_name="protocol")
    namespace = sgqlc.types.Field("StrComparators", graphql_name="namespace")
    path = sgqlc.types.Field("StrComparators", graphql_name="path")
    compression_type = sgqlc.types.Field("StrComparators", graphql_name="compressionType")
    size = sgqlc.types.Field("IntComparators", graphql_name="size")


class GenomicRangeCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "reference_genome_id", "file_id")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    reference_genome_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="referenceGenomeId")
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


class MetadataFieldCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "collection_id",
        "field_name",
        "description",
        "field_type",
        "is_required",
        "options",
        "default_value",
    )
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    field_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="fieldName")
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="description")
    field_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="fieldType")
    is_required = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="isRequired")
    options = sgqlc.types.Field(String, graphql_name="options")
    default_value = sgqlc.types.Field(String, graphql_name="defaultValue")


class MetadataFieldProjectCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "project_id", "metadata_field_id")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    project_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="projectId")
    metadata_field_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="metadataFieldId")


class MetadataFieldProjectUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "project_id", "metadata_field_id")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    project_id = sgqlc.types.Field(Int, graphql_name="projectId")
    metadata_field_id = sgqlc.types.Field(ID, graphql_name="metadataFieldId")


class MetadataFieldProjectWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id", "producing_run_id", "owner_user_id", "collection_id", "project_id", "metadata_field")
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    project_id = sgqlc.types.Field(IntComparators, graphql_name="projectId")
    metadata_field = sgqlc.types.Field("MetadataFieldWhereClause", graphql_name="metadataField")


class MetadataFieldProjectWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")


class MetadataFieldUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "collection_id",
        "field_name",
        "description",
        "field_type",
        "is_required",
        "options",
        "default_value",
    )
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    field_name = sgqlc.types.Field(String, graphql_name="fieldName")
    description = sgqlc.types.Field(String, graphql_name="description")
    field_type = sgqlc.types.Field(String, graphql_name="fieldType")
    is_required = sgqlc.types.Field(Boolean, graphql_name="isRequired")
    options = sgqlc.types.Field(String, graphql_name="options")
    default_value = sgqlc.types.Field(String, graphql_name="defaultValue")


class MetadataFieldWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "field_group",
        "field_name",
        "description",
        "field_type",
        "is_required",
        "options",
        "default_value",
        "metadatas",
    )
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    field_group = sgqlc.types.Field(MetadataFieldProjectWhereClause, graphql_name="fieldGroup")
    field_name = sgqlc.types.Field("StrComparators", graphql_name="fieldName")
    description = sgqlc.types.Field("StrComparators", graphql_name="description")
    field_type = sgqlc.types.Field("StrComparators", graphql_name="fieldType")
    is_required = sgqlc.types.Field(BoolComparators, graphql_name="isRequired")
    options = sgqlc.types.Field("StrComparators", graphql_name="options")
    default_value = sgqlc.types.Field("StrComparators", graphql_name="defaultValue")
    metadatas = sgqlc.types.Field("MetadatumWhereClause", graphql_name="metadatas")


class MetadataFieldWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")


class MetadatumCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "sample_id", "metadata_field_id", "value")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    sample_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="sampleId")
    metadata_field_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="metadataFieldId")
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="value")


class MetadatumUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "sample_id", "metadata_field_id", "value")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    sample_id = sgqlc.types.Field(ID, graphql_name="sampleId")
    metadata_field_id = sgqlc.types.Field(ID, graphql_name="metadataFieldId")
    value = sgqlc.types.Field(String, graphql_name="value")


class MetadatumWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id", "producing_run_id", "owner_user_id", "collection_id", "sample", "metadata_field", "value")
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    sample = sgqlc.types.Field("SampleWhereClause", graphql_name="sample")
    metadata_field = sgqlc.types.Field(MetadataFieldWhereClause, graphql_name="metadataField")
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
        "total_reads",
        "mapped_reads",
        "ref_snps",
        "n_actg",
        "n_missing",
        "n_ambiguous",
        "coverage_viz_summary_file_id",
    )
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    consensus_genome_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="consensusGenomeId")
    total_reads = sgqlc.types.Field(Int, graphql_name="totalReads")
    mapped_reads = sgqlc.types.Field(Int, graphql_name="mappedReads")
    ref_snps = sgqlc.types.Field(Int, graphql_name="refSnps")
    n_actg = sgqlc.types.Field(Int, graphql_name="nActg")
    n_missing = sgqlc.types.Field(Int, graphql_name="nMissing")
    n_ambiguous = sgqlc.types.Field(Int, graphql_name="nAmbiguous")
    coverage_viz_summary_file_id = sgqlc.types.Field(ID, graphql_name="coverageVizSummaryFileId")


class MetricConsensusGenomeUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "collection_id",
        "consensus_genome_id",
        "total_reads",
        "mapped_reads",
        "ref_snps",
        "n_actg",
        "n_missing",
        "n_ambiguous",
        "coverage_viz_summary_file_id",
    )
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    consensus_genome_id = sgqlc.types.Field(ID, graphql_name="consensusGenomeId")
    total_reads = sgqlc.types.Field(Int, graphql_name="totalReads")
    mapped_reads = sgqlc.types.Field(Int, graphql_name="mappedReads")
    ref_snps = sgqlc.types.Field(Int, graphql_name="refSnps")
    n_actg = sgqlc.types.Field(Int, graphql_name="nActg")
    n_missing = sgqlc.types.Field(Int, graphql_name="nMissing")
    n_ambiguous = sgqlc.types.Field(Int, graphql_name="nAmbiguous")
    coverage_viz_summary_file_id = sgqlc.types.Field(ID, graphql_name="coverageVizSummaryFileId")


class MetricConsensusGenomeWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "consensus_genome",
        "total_reads",
        "mapped_reads",
        "ref_snps",
        "n_actg",
        "n_missing",
        "n_ambiguous",
    )
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    consensus_genome = sgqlc.types.Field(ConsensusGenomeWhereClause, graphql_name="consensusGenome")
    total_reads = sgqlc.types.Field(IntComparators, graphql_name="totalReads")
    mapped_reads = sgqlc.types.Field(IntComparators, graphql_name="mappedReads")
    ref_snps = sgqlc.types.Field(IntComparators, graphql_name="refSnps")
    n_actg = sgqlc.types.Field(IntComparators, graphql_name="nActg")
    n_missing = sgqlc.types.Field(IntComparators, graphql_name="nMissing")
    n_ambiguous = sgqlc.types.Field(IntComparators, graphql_name="nAmbiguous")


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
    __field_names__ = ("collection_id", "file_id", "file_index_id", "name", "description", "taxon_id", "accession_id")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    file_id = sgqlc.types.Field(ID, graphql_name="fileId")
    file_index_id = sgqlc.types.Field(ID, graphql_name="fileIndexId")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="description")
    taxon_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="taxonId")
    accession_id = sgqlc.types.Field(String, graphql_name="accessionId")


class ReferenceGenomeUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "file_id", "file_index_id", "name", "description", "taxon_id", "accession_id")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    file_id = sgqlc.types.Field(ID, graphql_name="fileId")
    file_index_id = sgqlc.types.Field(ID, graphql_name="fileIndexId")
    name = sgqlc.types.Field(String, graphql_name="name")
    description = sgqlc.types.Field(String, graphql_name="description")
    taxon_id = sgqlc.types.Field(ID, graphql_name="taxonId")
    accession_id = sgqlc.types.Field(String, graphql_name="accessionId")


class ReferenceGenomeWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "name",
        "description",
        "taxon",
        "accession_id",
        "sequence_alignment_indices",
        "consensus_genomes",
        "genomic_ranges",
    )
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    name = sgqlc.types.Field("StrComparators", graphql_name="name")
    description = sgqlc.types.Field("StrComparators", graphql_name="description")
    taxon = sgqlc.types.Field("TaxonWhereClause", graphql_name="taxon")
    accession_id = sgqlc.types.Field("StrComparators", graphql_name="accessionId")
    sequence_alignment_indices = sgqlc.types.Field(
        "SequenceAlignmentIndexWhereClause", graphql_name="sequenceAlignmentIndices"
    )
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
        "name",
        "sample_type",
        "water_control",
        "collection_date",
        "collection_location",
        "description",
        "host_taxon_id",
    )
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    sample_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="sampleType")
    water_control = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="waterControl")
    collection_date = sgqlc.types.Field(DateTime, graphql_name="collectionDate")
    collection_location = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="collectionLocation")
    description = sgqlc.types.Field(String, graphql_name="description")
    host_taxon_id = sgqlc.types.Field(ID, graphql_name="hostTaxonId")


class SampleUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "collection_id",
        "name",
        "sample_type",
        "water_control",
        "collection_date",
        "collection_location",
        "description",
        "host_taxon_id",
    )
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
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


class SequenceAlignmentIndexCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "index_file_id", "reference_genome_id", "tool")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    index_file_id = sgqlc.types.Field(ID, graphql_name="indexFileId")
    reference_genome_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="referenceGenomeId")
    tool = sgqlc.types.Field(sgqlc.types.non_null(AlignmentTool), graphql_name="tool")


class SequenceAlignmentIndexUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "index_file_id", "reference_genome_id", "tool")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    index_file_id = sgqlc.types.Field(ID, graphql_name="indexFileId")
    reference_genome_id = sgqlc.types.Field(ID, graphql_name="referenceGenomeId")
    tool = sgqlc.types.Field(AlignmentTool, graphql_name="tool")


class SequenceAlignmentIndexWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id", "producing_run_id", "owner_user_id", "collection_id", "reference_genome", "tool")
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    reference_genome = sgqlc.types.Field(ReferenceGenomeWhereClause, graphql_name="referenceGenome")
    tool = sgqlc.types.Field(AlignmentToolEnumComparators, graphql_name="tool")


class SequenceAlignmentIndexWhereClauseMutations(sgqlc.types.Input):
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
        "has_ercc",
        "taxon_id",
        "primer_file_id",
    )
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    sample_id = sgqlc.types.Field(ID, graphql_name="sampleId")
    protocol = sgqlc.types.Field(sgqlc.types.non_null(SequencingProtocol), graphql_name="protocol")
    r1_file_id = sgqlc.types.Field(ID, graphql_name="r1FileId")
    r2_file_id = sgqlc.types.Field(ID, graphql_name="r2FileId")
    technology = sgqlc.types.Field(sgqlc.types.non_null(SequencingTechnology), graphql_name="technology")
    nucleic_acid = sgqlc.types.Field(sgqlc.types.non_null(NucleicAcid), graphql_name="nucleicAcid")
    has_ercc = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="hasErcc")
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
        "has_ercc",
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
    has_ercc = sgqlc.types.Field(Boolean, graphql_name="hasErcc")
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
        "has_ercc",
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
    has_ercc = sgqlc.types.Field(BoolComparators, graphql_name="hasErcc")
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
        "tax_id",
        "tax_id_parent",
        "tax_id_species",
        "tax_id_genus",
        "tax_id_family",
        "tax_id_order",
        "tax_id_class",
        "tax_id_phylum",
        "tax_id_kingdom",
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
    tax_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="taxId")
    tax_id_parent = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="taxIdParent")
    tax_id_species = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="taxIdSpecies")
    tax_id_genus = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="taxIdGenus")
    tax_id_family = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="taxIdFamily")
    tax_id_order = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="taxIdOrder")
    tax_id_class = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="taxIdClass")
    tax_id_phylum = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="taxIdPhylum")
    tax_id_kingdom = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="taxIdKingdom")


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
        "tax_id",
        "tax_id_parent",
        "tax_id_species",
        "tax_id_genus",
        "tax_id_family",
        "tax_id_order",
        "tax_id_class",
        "tax_id_phylum",
        "tax_id_kingdom",
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
    tax_id = sgqlc.types.Field(Int, graphql_name="taxId")
    tax_id_parent = sgqlc.types.Field(Int, graphql_name="taxIdParent")
    tax_id_species = sgqlc.types.Field(Int, graphql_name="taxIdSpecies")
    tax_id_genus = sgqlc.types.Field(Int, graphql_name="taxIdGenus")
    tax_id_family = sgqlc.types.Field(Int, graphql_name="taxIdFamily")
    tax_id_order = sgqlc.types.Field(Int, graphql_name="taxIdOrder")
    tax_id_class = sgqlc.types.Field(Int, graphql_name="taxIdClass")
    tax_id_phylum = sgqlc.types.Field(Int, graphql_name="taxIdPhylum")
    tax_id_kingdom = sgqlc.types.Field(Int, graphql_name="taxIdKingdom")


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
        "tax_id",
        "tax_id_parent",
        "tax_id_species",
        "tax_id_genus",
        "tax_id_family",
        "tax_id_order",
        "tax_id_class",
        "tax_id_phylum",
        "tax_id_kingdom",
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
    tax_id = sgqlc.types.Field(IntComparators, graphql_name="taxId")
    tax_id_parent = sgqlc.types.Field(IntComparators, graphql_name="taxIdParent")
    tax_id_species = sgqlc.types.Field(IntComparators, graphql_name="taxIdSpecies")
    tax_id_genus = sgqlc.types.Field(IntComparators, graphql_name="taxIdGenus")
    tax_id_family = sgqlc.types.Field(IntComparators, graphql_name="taxIdFamily")
    tax_id_order = sgqlc.types.Field(IntComparators, graphql_name="taxIdOrder")
    tax_id_class = sgqlc.types.Field(IntComparators, graphql_name="taxIdClass")
    tax_id_phylum = sgqlc.types.Field(IntComparators, graphql_name="taxIdPhylum")
    tax_id_kingdom = sgqlc.types.Field(IntComparators, graphql_name="taxIdKingdom")
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
    protocol = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="protocol")
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


class MetadataFieldProjectConnection(sgqlc.types.relay.Connection):
    __schema__ = gql_schema
    __field_names__ = ("page_info", "edges")
    page_info = sgqlc.types.Field(sgqlc.types.non_null("PageInfo"), graphql_name="pageInfo")
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("MetadataFieldProjectEdge"))),
        graphql_name="edges",
    )


class MetadataFieldProjectEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("cursor", "node")
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="cursor")
    node = sgqlc.types.Field(sgqlc.types.non_null("MetadataFieldProject"), graphql_name="node")


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
        "create_sequence_alignment_index",
        "update_sequence_alignment_index",
        "delete_sequence_alignment_index",
        "create_metadatum",
        "update_metadatum",
        "delete_metadatum",
        "create_metadata_field",
        "update_metadata_field",
        "delete_metadata_field",
        "create_metadata_field_project",
        "update_metadata_field_project",
        "delete_metadata_field_project",
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
    create_sequence_alignment_index = sgqlc.types.Field(
        sgqlc.types.non_null("SequenceAlignmentIndex"),
        graphql_name="createSequenceAlignmentIndex",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SequenceAlignmentIndexCreateInput), graphql_name="input", default=None
                    ),
                ),
            )
        ),
    )
    update_sequence_alignment_index = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("SequenceAlignmentIndex"))),
        graphql_name="updateSequenceAlignmentIndex",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SequenceAlignmentIndexUpdateInput), graphql_name="input", default=None
                    ),
                ),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SequenceAlignmentIndexWhereClauseMutations),
                        graphql_name="where",
                        default=None,
                    ),
                ),
            )
        ),
    )
    delete_sequence_alignment_index = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("SequenceAlignmentIndex"))),
        graphql_name="deleteSequenceAlignmentIndex",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SequenceAlignmentIndexWhereClauseMutations),
                        graphql_name="where",
                        default=None,
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
    create_metadata_field = sgqlc.types.Field(
        sgqlc.types.non_null("MetadataField"),
        graphql_name="createMetadataField",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(sgqlc.types.non_null(MetadataFieldCreateInput), graphql_name="input", default=None),
                ),
            )
        ),
    )
    update_metadata_field = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("MetadataField"))),
        graphql_name="updateMetadataField",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(sgqlc.types.non_null(MetadataFieldUpdateInput), graphql_name="input", default=None),
                ),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(MetadataFieldWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_metadata_field = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("MetadataField"))),
        graphql_name="deleteMetadataField",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(MetadataFieldWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    create_metadata_field_project = sgqlc.types.Field(
        sgqlc.types.non_null("MetadataFieldProject"),
        graphql_name="createMetadataFieldProject",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(MetadataFieldProjectCreateInput), graphql_name="input", default=None
                    ),
                ),
            )
        ),
    )
    update_metadata_field_project = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("MetadataFieldProject"))),
        graphql_name="updateMetadataFieldProject",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(MetadataFieldProjectUpdateInput), graphql_name="input", default=None
                    ),
                ),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(MetadataFieldProjectWhereClauseMutations),
                        graphql_name="where",
                        default=None,
                    ),
                ),
            )
        ),
    )
    delete_metadata_field_project = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("MetadataFieldProject"))),
        graphql_name="deleteMetadataFieldProject",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(MetadataFieldProjectWhereClauseMutations),
                        graphql_name="where",
                        default=None,
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


class PageInfo(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("has_next_page", "has_previous_page", "start_cursor", "end_cursor")
    has_next_page = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="hasNextPage")
    has_previous_page = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="hasPreviousPage")
    start_cursor = sgqlc.types.Field(String, graphql_name="startCursor")
    end_cursor = sgqlc.types.Field(String, graphql_name="endCursor")


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
        "sequence_alignment_indices",
        "metadatas",
        "metadata_fields",
        "metadata_field_projects",
        "consensus_genomes",
        "metrics_consensus_genomes",
        "taxa",
        "upstream_databases",
        "contigs",
        "phylogenetic_trees",
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
    sequence_alignment_indices = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("SequenceAlignmentIndex"))),
        graphql_name="sequenceAlignmentIndices",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(SequenceAlignmentIndexWhereClause, graphql_name="where", default=None)),)
        ),
    )
    metadatas = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Metadatum"))),
        graphql_name="metadatas",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(MetadatumWhereClause, graphql_name="where", default=None)),)
        ),
    )
    metadata_fields = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("MetadataField"))),
        graphql_name="metadataFields",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(MetadataFieldWhereClause, graphql_name="where", default=None)),)
        ),
    )
    metadata_field_projects = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("MetadataFieldProject"))),
        graphql_name="metadataFieldProjects",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(MetadataFieldProjectWhereClause, graphql_name="where", default=None)),)
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


class SequenceAlignmentIndexConnection(sgqlc.types.relay.Connection):
    __schema__ = gql_schema
    __field_names__ = ("page_info", "edges")
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name="pageInfo")
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("SequenceAlignmentIndexEdge"))),
        graphql_name="edges",
    )


class SequenceAlignmentIndexEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("cursor", "node")
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="cursor")
    node = sgqlc.types.Field(sgqlc.types.non_null("SequenceAlignmentIndex"), graphql_name="node")


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


class SignedURL(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("url", "protocol", "method", "expiration", "fields")
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="url")
    protocol = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="protocol")
    method = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="method")
    expiration = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="expiration")
    fields = sgqlc.types.Field(JSON, graphql_name="fields")


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
        "intermediate_outputs_id",
        "intermediate_outputs",
        "metrics",
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
    intermediate_outputs_id = sgqlc.types.Field(ID, graphql_name="intermediateOutputsId")
    intermediate_outputs = sgqlc.types.Field(
        File,
        graphql_name="intermediateOutputs",
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


class MetadataField(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "field_group",
        "field_name",
        "description",
        "field_type",
        "is_required",
        "options",
        "default_value",
        "metadatas",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    field_group = sgqlc.types.Field(
        sgqlc.types.non_null(MetadataFieldProjectConnection),
        graphql_name="fieldGroup",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(MetadataFieldProjectWhereClause, graphql_name="where", default=None)),
                ("before", sgqlc.types.Arg(String, graphql_name="before", default=None)),
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
            )
        ),
    )
    field_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="fieldName")
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="description")
    field_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="fieldType")
    is_required = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="isRequired")
    options = sgqlc.types.Field(String, graphql_name="options")
    default_value = sgqlc.types.Field(String, graphql_name="defaultValue")
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


class MetadataFieldProject(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = ("id", "producing_run_id", "owner_user_id", "collection_id", "project_id", "metadata_field")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    project_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="projectId")
    metadata_field = sgqlc.types.Field(
        MetadataField,
        graphql_name="metadataField",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(MetadataFieldWhereClause, graphql_name="where", default=None)),)
        ),
    )


class Metadatum(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = ("id", "producing_run_id", "owner_user_id", "collection_id", "sample", "metadata_field", "value")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    sample = sgqlc.types.Field(
        "Sample",
        graphql_name="sample",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(SampleWhereClause, graphql_name="where", default=None)),)),
    )
    metadata_field = sgqlc.types.Field(
        MetadataField,
        graphql_name="metadataField",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(MetadataFieldWhereClause, graphql_name="where", default=None)),)
        ),
    )
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="value")


class MetricConsensusGenome(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "consensus_genome",
        "total_reads",
        "mapped_reads",
        "ref_snps",
        "n_actg",
        "n_missing",
        "n_ambiguous",
        "coverage_viz_summary_file_id",
        "coverage_viz_summary_file",
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
    total_reads = sgqlc.types.Field(Int, graphql_name="totalReads")
    mapped_reads = sgqlc.types.Field(Int, graphql_name="mappedReads")
    ref_snps = sgqlc.types.Field(Int, graphql_name="refSnps")
    n_actg = sgqlc.types.Field(Int, graphql_name="nActg")
    n_missing = sgqlc.types.Field(Int, graphql_name="nMissing")
    n_ambiguous = sgqlc.types.Field(Int, graphql_name="nAmbiguous")
    coverage_viz_summary_file_id = sgqlc.types.Field(ID, graphql_name="coverageVizSummaryFileId")
    coverage_viz_summary_file = sgqlc.types.Field(
        File,
        graphql_name="coverageVizSummaryFile",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(FileWhereClause, graphql_name="where", default=None)),)),
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
        "file_index_id",
        "file_index",
        "name",
        "description",
        "taxon",
        "accession_id",
        "sequence_alignment_indices",
        "consensus_genomes",
        "genomic_ranges",
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
    file_index_id = sgqlc.types.Field(ID, graphql_name="fileIndexId")
    file_index = sgqlc.types.Field(
        File,
        graphql_name="fileIndex",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(FileWhereClause, graphql_name="where", default=None)),)),
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="description")
    taxon = sgqlc.types.Field(
        "Taxon",
        graphql_name="taxon",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(TaxonWhereClause, graphql_name="where", default=None)),)),
    )
    accession_id = sgqlc.types.Field(String, graphql_name="accessionId")
    sequence_alignment_indices = sgqlc.types.Field(
        sgqlc.types.non_null(SequenceAlignmentIndexConnection),
        graphql_name="sequenceAlignmentIndices",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(SequenceAlignmentIndexWhereClause, graphql_name="where", default=None)),
                ("before", sgqlc.types.Arg(String, graphql_name="before", default=None)),
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
            )
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


class Sample(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
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
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    sample_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="sampleType")
    water_control = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="waterControl")
    collection_date = sgqlc.types.Field(DateTime, graphql_name="collectionDate")
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


class SequenceAlignmentIndex(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "index_file_id",
        "index_file",
        "reference_genome",
        "tool",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    index_file_id = sgqlc.types.Field(ID, graphql_name="indexFileId")
    index_file = sgqlc.types.Field(
        File,
        graphql_name="indexFile",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(FileWhereClause, graphql_name="where", default=None)),)),
    )
    reference_genome = sgqlc.types.Field(
        ReferenceGenome,
        graphql_name="referenceGenome",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(ReferenceGenomeWhereClause, graphql_name="where", default=None)),)
        ),
    )
    tool = sgqlc.types.Field(sgqlc.types.non_null(AlignmentTool), graphql_name="tool")


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
        "has_ercc",
        "taxon",
        "primer_file",
        "consensus_genomes",
        "contigs",
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
    protocol = sgqlc.types.Field(sgqlc.types.non_null(SequencingProtocol), graphql_name="protocol")
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
    has_ercc = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="hasErcc")
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
        "tax_id",
        "tax_id_parent",
        "tax_id_species",
        "tax_id_genus",
        "tax_id_family",
        "tax_id_order",
        "tax_id_class",
        "tax_id_phylum",
        "tax_id_kingdom",
        "consensus_genomes",
        "reference_genomes",
        "sequencing_reads",
        "samples",
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
    tax_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="taxId")
    tax_id_parent = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="taxIdParent")
    tax_id_species = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="taxIdSpecies")
    tax_id_genus = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="taxIdGenus")
    tax_id_family = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="taxIdFamily")
    tax_id_order = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="taxIdOrder")
    tax_id_class = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="taxIdClass")
    tax_id_phylum = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="taxIdPhylum")
    tax_id_kingdom = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="taxIdKingdom")
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


class UpstreamDatabase(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = ("id", "producing_run_id", "owner_user_id", "collection_id", "name", "taxa")
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


########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
gql_schema.query_type = Query
gql_schema.mutation_type = Mutation
gql_schema.subscription_type = None
