import sgqlc.types
import sgqlc.types.datetime
import sgqlc.types.relay


entities_schema = sgqlc.types.Schema()


# Unexport Node/PageInfo, let schema re-declare them
entities_schema -= sgqlc.types.relay.Node
entities_schema -= sgqlc.types.relay.PageInfo



########################################################################
# Scalars and Enumerations
########################################################################
class AccessionCountColumns(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('accession_id', 'accession_name', 'collection_id', 'consensus_genomes', 'created_at', 'deleted_at', 'id', 'owner_user_id', 'producing_run_id', 'updated_at', 'upstream_database')


Boolean = sgqlc.types.Boolean

class BulkDownloadCountColumns(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('collection_id', 'created_at', 'deleted_at', 'download_type', 'file', 'id', 'owner_user_id', 'producing_run_id', 'updated_at')


class BulkDownloadType(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('concatenate', 'zip')


class ConsensusGenomeCountColumns(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('accession', 'collection_id', 'created_at', 'deleted_at', 'id', 'intermediate_outputs', 'metrics', 'owner_user_id', 'producing_run_id', 'reference_genome', 'sequence', 'sequence_read', 'taxon', 'updated_at')


DateTime = sgqlc.types.datetime.DateTime

class FileAccessProtocol(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('s3',)


class FileStatus(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('FAILED', 'PENDING', 'SUCCESS')


Float = sgqlc.types.Float

class GenomicRangeCountColumns(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('collection_id', 'created_at', 'deleted_at', 'file', 'id', 'owner_user_id', 'producing_run_id', 'sequencing_reads', 'updated_at')


class GlobalID(sgqlc.types.Scalar):
    __schema__ = entities_schema


class HostOrganismCategory(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('human', 'insect', 'non_human_animal', 'unknown')


class HostOrganismCountColumns(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('category', 'collection_id', 'created_at', 'deleted_at', 'id', 'indexes', 'is_deuterostome', 'name', 'owner_user_id', 'producing_run_id', 'samples', 'sequence', 'updated_at', 'version')


ID = sgqlc.types.ID

class IndexFileCountColumns(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('collection_id', 'created_at', 'deleted_at', 'file', 'host_organism', 'id', 'name', 'owner_user_id', 'producing_run_id', 'updated_at', 'upstream_database', 'version')


class IndexTypes(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('accession2taxid', 'bowtie2', 'bowtie2_v2', 'deuterostome', 'diamond', 'hisat2', 'kallisto', 'lineage', 'minimap2_dna', 'minimap2_long', 'minimap2_rna', 'minimap2_short', 'nr', 'nr_loc', 'nt', 'nt_info', 'nt_loc', 'original_transcripts_gtf', 'star', 'taxon_blacklist')


Int = sgqlc.types.Int

class JSON(sgqlc.types.Scalar):
    __schema__ = entities_schema


class MetadatumCountColumns(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('collection_id', 'created_at', 'deleted_at', 'field_name', 'id', 'owner_user_id', 'producing_run_id', 'sample', 'updated_at', 'value')


class MetricConsensusGenomeCountColumns(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('collection_id', 'consensus_genome', 'coverage_bin_size', 'coverage_breadth', 'coverage_depth', 'coverage_total_length', 'coverage_viz', 'created_at', 'deleted_at', 'gc_percent', 'id', 'mapped_reads', 'n_actg', 'n_ambiguous', 'n_missing', 'owner_user_id', 'percent_genome_called', 'percent_identity', 'producing_run_id', 'ref_snps', 'reference_genome_length', 'total_reads', 'updated_at')


class NucleicAcid(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('DNA', 'RNA')


class PhylogeneticTreeCountColumns(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('collection_id', 'created_at', 'deleted_at', 'format', 'id', 'owner_user_id', 'producing_run_id', 'tree', 'updated_at')


class PhylogeneticTreeFormat(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('auspice_v1', 'auspice_v2', 'newick')


class ReferenceGenomeCountColumns(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('collection_id', 'consensus_genomes', 'created_at', 'deleted_at', 'file', 'id', 'name', 'owner_user_id', 'producing_run_id', 'updated_at')


class SampleCountColumns(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('collection_date', 'collection_id', 'collection_location', 'created_at', 'deleted_at', 'host_organism', 'id', 'metadatas', 'name', 'notes', 'owner_user_id', 'producing_run_id', 'rails_sample_id', 'sample_type', 'sequencing_reads', 'updated_at', 'water_control')


class SequencingProtocol(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('ampliseq', 'artic', 'artic_v3', 'artic_v4', 'artic_v5', 'combined_msspe_artic', 'covidseq', 'easyseq', 'midnight', 'msspe', 'snap', 'varskip')


class SequencingReadCountColumns(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('clearlabs_export', 'collection_id', 'consensus_genomes', 'created_at', 'deleted_at', 'id', 'medaka_model', 'nucleic_acid', 'owner_user_id', 'primer_file', 'producing_run_id', 'protocol', 'r1_file', 'r2_file', 'sample', 'taxon', 'technology', 'updated_at')


class SequencingTechnology(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('Illumina', 'Nanopore')


String = sgqlc.types.String

class TaxonCountColumns(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('collection_id', 'common_name', 'consensus_genomes', 'created_at', 'deleted_at', 'description', 'id', 'is_phage', 'level', 'name', 'owner_user_id', 'producing_run_id', 'sequencing_reads', 'tax_class', 'tax_family', 'tax_genus', 'tax_kingdom', 'tax_order', 'tax_parent', 'tax_phylum', 'tax_species', 'tax_subspecies', 'tax_superkingdom', 'updated_at', 'upstream_database', 'upstream_database_identifier', 'wikipedia_id')


class TaxonLevel(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('level_class', 'level_family', 'level_genus', 'level_kingdom', 'level_order', 'level_phylum', 'level_species', 'level_subspecies', 'level_superkingdom')


class UUID(sgqlc.types.Scalar):
    __schema__ = entities_schema


class UpstreamDatabaseCountColumns(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('accessions', 'collection_id', 'created_at', 'deleted_at', 'id', 'indexes', 'name', 'owner_user_id', 'producing_run_id', 'taxa', 'updated_at')


class orderBy(sgqlc.types.Enum):
    __schema__ = entities_schema
    __choices__ = ('asc', 'asc_nulls_first', 'asc_nulls_last', 'desc', 'desc_nulls_first', 'desc_nulls_last')



########################################################################
# Input Objects
########################################################################
class AccessionCreateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('accession_id', 'accession_name', 'upstream_database_id', 'producing_run_id', 'collection_id')
    accession_id = sgqlc.types.Field(String, graphql_name='accessionId')
    accession_name = sgqlc.types.Field(String, graphql_name='accessionName')
    upstream_database_id = sgqlc.types.Field(ID, graphql_name='upstreamDatabaseId')
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class AccessionOrderByClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('accession_id', 'accession_name', 'upstream_database', 'id', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    accession_id = sgqlc.types.Field(orderBy, graphql_name='accessionId')
    accession_name = sgqlc.types.Field(orderBy, graphql_name='accessionName')
    upstream_database = sgqlc.types.Field('UpstreamDatabaseOrderByClause', graphql_name='upstreamDatabase')
    id = sgqlc.types.Field(orderBy, graphql_name='id')
    producing_run_id = sgqlc.types.Field(orderBy, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(orderBy, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(orderBy, graphql_name='collectionId')
    created_at = sgqlc.types.Field(orderBy, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(orderBy, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(orderBy, graphql_name='deletedAt')


class AccessionUpdateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('accession_name',)
    accession_name = sgqlc.types.Field(String, graphql_name='accessionName')


class AccessionWhereClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id', 'producing_run_id', 'owner_user_id', 'collection_id', 'accession_id', 'accession_name', 'upstream_database', 'consensus_genomes', 'entity_id')
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')
    producing_run_id = sgqlc.types.Field('IntComparators', graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field('IntComparators', graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field('IntComparators', graphql_name='collectionId')
    accession_id = sgqlc.types.Field('StrComparators', graphql_name='accessionId')
    accession_name = sgqlc.types.Field('StrComparators', graphql_name='accessionName')
    upstream_database = sgqlc.types.Field('UpstreamDatabaseWhereClause', graphql_name='upstreamDatabase')
    consensus_genomes = sgqlc.types.Field('ConsensusGenomeWhereClause', graphql_name='consensusGenomes')
    entity_id = sgqlc.types.Field('UUIDComparators', graphql_name='entityId')


class AccessionWhereClauseMutations(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')


class BoolComparators(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('_eq', '_neq', '_in', '_nin', '_gt', '_gte', '_lt', '_lte', '_is_null')
    _eq = sgqlc.types.Field(Int, graphql_name='_eq')
    _neq = sgqlc.types.Field(Int, graphql_name='_neq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Int)), graphql_name='_in')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Int)), graphql_name='_nin')
    _gt = sgqlc.types.Field(Int, graphql_name='_gt')
    _gte = sgqlc.types.Field(Int, graphql_name='_gte')
    _lt = sgqlc.types.Field(Int, graphql_name='_lt')
    _lte = sgqlc.types.Field(Int, graphql_name='_lte')
    _is_null = sgqlc.types.Field(Int, graphql_name='_is_null')


class BulkDownloadCreateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('download_type', 'producing_run_id', 'collection_id')
    download_type = sgqlc.types.Field(BulkDownloadType, graphql_name='downloadType')
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class BulkDownloadOrderByClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('download_type', 'id', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    download_type = sgqlc.types.Field(orderBy, graphql_name='downloadType')
    id = sgqlc.types.Field(orderBy, graphql_name='id')
    producing_run_id = sgqlc.types.Field(orderBy, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(orderBy, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(orderBy, graphql_name='collectionId')
    created_at = sgqlc.types.Field(orderBy, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(orderBy, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(orderBy, graphql_name='deletedAt')


class BulkDownloadTypeEnumComparators(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('_eq', '_neq', '_in', '_nin', '_gt', '_gte', '_lt', '_lte', '_is_null')
    _eq = sgqlc.types.Field(BulkDownloadType, graphql_name='_eq')
    _neq = sgqlc.types.Field(BulkDownloadType, graphql_name='_neq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(BulkDownloadType)), graphql_name='_in')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(BulkDownloadType)), graphql_name='_nin')
    _gt = sgqlc.types.Field(BulkDownloadType, graphql_name='_gt')
    _gte = sgqlc.types.Field(BulkDownloadType, graphql_name='_gte')
    _lt = sgqlc.types.Field(BulkDownloadType, graphql_name='_lt')
    _lte = sgqlc.types.Field(BulkDownloadType, graphql_name='_lte')
    _is_null = sgqlc.types.Field(BulkDownloadType, graphql_name='_is_null')


class BulkDownloadWhereClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id', 'producing_run_id', 'owner_user_id', 'collection_id', 'download_type', 'entity_id')
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')
    producing_run_id = sgqlc.types.Field('IntComparators', graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field('IntComparators', graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field('IntComparators', graphql_name='collectionId')
    download_type = sgqlc.types.Field(BulkDownloadTypeEnumComparators, graphql_name='downloadType')
    entity_id = sgqlc.types.Field('UUIDComparators', graphql_name='entityId')


class BulkDownloadWhereClauseMutations(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')


class ConsensusGenomeCreateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('taxon_id', 'sequence_read_id', 'reference_genome_id', 'accession_id', 'producing_run_id', 'collection_id')
    taxon_id = sgqlc.types.Field(ID, graphql_name='taxonId')
    sequence_read_id = sgqlc.types.Field(ID, graphql_name='sequenceReadId')
    reference_genome_id = sgqlc.types.Field(ID, graphql_name='referenceGenomeId')
    accession_id = sgqlc.types.Field(ID, graphql_name='accessionId')
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class ConsensusGenomeOrderByClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('taxon', 'sequence_read', 'reference_genome', 'accession', 'metrics', 'id', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    taxon = sgqlc.types.Field('TaxonOrderByClause', graphql_name='taxon')
    sequence_read = sgqlc.types.Field('SequencingReadOrderByClause', graphql_name='sequenceRead')
    reference_genome = sgqlc.types.Field('ReferenceGenomeOrderByClause', graphql_name='referenceGenome')
    accession = sgqlc.types.Field(AccessionOrderByClause, graphql_name='accession')
    metrics = sgqlc.types.Field('MetricConsensusGenomeOrderByClause', graphql_name='metrics')
    id = sgqlc.types.Field(orderBy, graphql_name='id')
    producing_run_id = sgqlc.types.Field(orderBy, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(orderBy, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(orderBy, graphql_name='collectionId')
    created_at = sgqlc.types.Field(orderBy, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(orderBy, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(orderBy, graphql_name='deletedAt')


class ConsensusGenomeWhereClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id', 'producing_run_id', 'owner_user_id', 'collection_id', 'taxon', 'sequence_read', 'reference_genome', 'accession', 'metrics', 'entity_id')
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')
    producing_run_id = sgqlc.types.Field('IntComparators', graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field('IntComparators', graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field('IntComparators', graphql_name='collectionId')
    taxon = sgqlc.types.Field('TaxonWhereClause', graphql_name='taxon')
    sequence_read = sgqlc.types.Field('SequencingReadWhereClause', graphql_name='sequenceRead')
    reference_genome = sgqlc.types.Field('ReferenceGenomeWhereClause', graphql_name='referenceGenome')
    accession = sgqlc.types.Field(AccessionWhereClause, graphql_name='accession')
    metrics = sgqlc.types.Field('MetricConsensusGenomeWhereClause', graphql_name='metrics')
    entity_id = sgqlc.types.Field('UUIDComparators', graphql_name='entityId')


class ConsensusGenomeWhereClauseMutations(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')


class DatetimeComparators(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('_eq', '_neq', '_in', '_nin', '_gt', '_gte', '_lt', '_lte', '_is_null')
    _eq = sgqlc.types.Field(DateTime, graphql_name='_eq')
    _neq = sgqlc.types.Field(DateTime, graphql_name='_neq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(DateTime)), graphql_name='_in')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(DateTime)), graphql_name='_nin')
    _gt = sgqlc.types.Field(DateTime, graphql_name='_gt')
    _gte = sgqlc.types.Field(DateTime, graphql_name='_gte')
    _lt = sgqlc.types.Field(DateTime, graphql_name='_lt')
    _lte = sgqlc.types.Field(DateTime, graphql_name='_lte')
    _is_null = sgqlc.types.Field(DateTime, graphql_name='_is_null')


class EntityWhereClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id', 'entity_id', 'producing_run_id', 'owner_user_id', 'collection_id')
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')
    entity_id = sgqlc.types.Field('UUIDComparators', graphql_name='entityId')
    producing_run_id = sgqlc.types.Field('IntComparators', graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field('IntComparators', graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field('IntComparators', graphql_name='collectionId')


class FileCreate(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('name', 'file_format', 'compression_type', 'protocol', 'namespace', 'path')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    file_format = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='fileFormat')
    compression_type = sgqlc.types.Field(String, graphql_name='compressionType')
    protocol = sgqlc.types.Field(sgqlc.types.non_null(FileAccessProtocol), graphql_name='protocol')
    namespace = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='namespace')
    path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='path')


class FileStatusEnumComparators(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('_eq', '_neq', '_in', '_nin', '_gt', '_gte', '_lt', '_lte', '_is_null')
    _eq = sgqlc.types.Field(FileStatus, graphql_name='_eq')
    _neq = sgqlc.types.Field(FileStatus, graphql_name='_neq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(FileStatus)), graphql_name='_in')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(FileStatus)), graphql_name='_nin')
    _gt = sgqlc.types.Field(FileStatus, graphql_name='_gt')
    _gte = sgqlc.types.Field(FileStatus, graphql_name='_gte')
    _lt = sgqlc.types.Field(FileStatus, graphql_name='_lt')
    _lte = sgqlc.types.Field(FileStatus, graphql_name='_lte')
    _is_null = sgqlc.types.Field(FileStatus, graphql_name='_is_null')


class FileUpload(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('name', 'file_format', 'compression_type')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    file_format = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='fileFormat')
    compression_type = sgqlc.types.Field(String, graphql_name='compressionType')


class FileWhereClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id', 'entity_id', 'entity_field_name', 'status', 'protocol', 'namespace', 'path', 'file_format', 'compression_type', 'size')
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')
    entity_id = sgqlc.types.Field('UUIDComparators', graphql_name='entityId')
    entity_field_name = sgqlc.types.Field('StrComparators', graphql_name='entityFieldName')
    status = sgqlc.types.Field(FileStatusEnumComparators, graphql_name='status')
    protocol = sgqlc.types.Field('StrComparators', graphql_name='protocol')
    namespace = sgqlc.types.Field('StrComparators', graphql_name='namespace')
    path = sgqlc.types.Field('StrComparators', graphql_name='path')
    file_format = sgqlc.types.Field('StrComparators', graphql_name='fileFormat')
    compression_type = sgqlc.types.Field('StrComparators', graphql_name='compressionType')
    size = sgqlc.types.Field('IntComparators', graphql_name='size')


class FloatComparators(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('_eq', '_neq', '_in', '_nin', '_gt', '_gte', '_lt', '_lte', '_is_null')
    _eq = sgqlc.types.Field(Float, graphql_name='_eq')
    _neq = sgqlc.types.Field(Float, graphql_name='_neq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Float)), graphql_name='_in')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Float)), graphql_name='_nin')
    _gt = sgqlc.types.Field(Float, graphql_name='_gt')
    _gte = sgqlc.types.Field(Float, graphql_name='_gte')
    _lt = sgqlc.types.Field(Float, graphql_name='_lt')
    _lte = sgqlc.types.Field(Float, graphql_name='_lte')
    _is_null = sgqlc.types.Field(Float, graphql_name='_is_null')


class GenomicRangeCreateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('producing_run_id', 'collection_id')
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class GenomicRangeOrderByClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    id = sgqlc.types.Field(orderBy, graphql_name='id')
    producing_run_id = sgqlc.types.Field(orderBy, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(orderBy, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(orderBy, graphql_name='collectionId')
    created_at = sgqlc.types.Field(orderBy, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(orderBy, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(orderBy, graphql_name='deletedAt')


class GenomicRangeWhereClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id', 'producing_run_id', 'owner_user_id', 'collection_id', 'sequencing_reads', 'entity_id')
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')
    producing_run_id = sgqlc.types.Field('IntComparators', graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field('IntComparators', graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field('IntComparators', graphql_name='collectionId')
    sequencing_reads = sgqlc.types.Field('SequencingReadWhereClause', graphql_name='sequencingReads')
    entity_id = sgqlc.types.Field('UUIDComparators', graphql_name='entityId')


class GenomicRangeWhereClauseMutations(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')


class HostOrganismCategoryEnumComparators(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('_eq', '_neq', '_in', '_nin', '_gt', '_gte', '_lt', '_lte', '_is_null')
    _eq = sgqlc.types.Field(HostOrganismCategory, graphql_name='_eq')
    _neq = sgqlc.types.Field(HostOrganismCategory, graphql_name='_neq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(HostOrganismCategory)), graphql_name='_in')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(HostOrganismCategory)), graphql_name='_nin')
    _gt = sgqlc.types.Field(HostOrganismCategory, graphql_name='_gt')
    _gte = sgqlc.types.Field(HostOrganismCategory, graphql_name='_gte')
    _lt = sgqlc.types.Field(HostOrganismCategory, graphql_name='_lt')
    _lte = sgqlc.types.Field(HostOrganismCategory, graphql_name='_lte')
    _is_null = sgqlc.types.Field(HostOrganismCategory, graphql_name='_is_null')


class HostOrganismCreateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('name', 'version', 'category', 'is_deuterostome', 'producing_run_id', 'collection_id')
    name = sgqlc.types.Field(String, graphql_name='name')
    version = sgqlc.types.Field(String, graphql_name='version')
    category = sgqlc.types.Field(HostOrganismCategory, graphql_name='category')
    is_deuterostome = sgqlc.types.Field(Boolean, graphql_name='isDeuterostome')
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class HostOrganismOrderByClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('name', 'version', 'category', 'is_deuterostome', 'id', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    name = sgqlc.types.Field(orderBy, graphql_name='name')
    version = sgqlc.types.Field(orderBy, graphql_name='version')
    category = sgqlc.types.Field(orderBy, graphql_name='category')
    is_deuterostome = sgqlc.types.Field(orderBy, graphql_name='isDeuterostome')
    id = sgqlc.types.Field(orderBy, graphql_name='id')
    producing_run_id = sgqlc.types.Field(orderBy, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(orderBy, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(orderBy, graphql_name='collectionId')
    created_at = sgqlc.types.Field(orderBy, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(orderBy, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(orderBy, graphql_name='deletedAt')


class HostOrganismUpdateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('name', 'version', 'category', 'is_deuterostome')
    name = sgqlc.types.Field(String, graphql_name='name')
    version = sgqlc.types.Field(String, graphql_name='version')
    category = sgqlc.types.Field(HostOrganismCategory, graphql_name='category')
    is_deuterostome = sgqlc.types.Field(Boolean, graphql_name='isDeuterostome')


class HostOrganismWhereClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id', 'producing_run_id', 'owner_user_id', 'collection_id', 'name', 'version', 'category', 'is_deuterostome', 'indexes', 'samples', 'entity_id')
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')
    producing_run_id = sgqlc.types.Field('IntComparators', graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field('IntComparators', graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field('IntComparators', graphql_name='collectionId')
    name = sgqlc.types.Field('StrComparators', graphql_name='name')
    version = sgqlc.types.Field('StrComparators', graphql_name='version')
    category = sgqlc.types.Field(HostOrganismCategoryEnumComparators, graphql_name='category')
    is_deuterostome = sgqlc.types.Field(BoolComparators, graphql_name='isDeuterostome')
    indexes = sgqlc.types.Field('IndexFileWhereClause', graphql_name='indexes')
    samples = sgqlc.types.Field('SampleWhereClause', graphql_name='samples')
    entity_id = sgqlc.types.Field('UUIDComparators', graphql_name='entityId')


class HostOrganismWhereClauseMutations(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')


class IndexFileCreateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('name', 'version', 'upstream_database_id', 'host_organism_id', 'producing_run_id', 'collection_id')
    name = sgqlc.types.Field(IndexTypes, graphql_name='name')
    version = sgqlc.types.Field(String, graphql_name='version')
    upstream_database_id = sgqlc.types.Field(ID, graphql_name='upstreamDatabaseId')
    host_organism_id = sgqlc.types.Field(ID, graphql_name='hostOrganismId')
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class IndexFileOrderByClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('name', 'version', 'upstream_database', 'host_organism', 'id', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    name = sgqlc.types.Field(orderBy, graphql_name='name')
    version = sgqlc.types.Field(orderBy, graphql_name='version')
    upstream_database = sgqlc.types.Field('UpstreamDatabaseOrderByClause', graphql_name='upstreamDatabase')
    host_organism = sgqlc.types.Field(HostOrganismOrderByClause, graphql_name='hostOrganism')
    id = sgqlc.types.Field(orderBy, graphql_name='id')
    producing_run_id = sgqlc.types.Field(orderBy, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(orderBy, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(orderBy, graphql_name='collectionId')
    created_at = sgqlc.types.Field(orderBy, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(orderBy, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(orderBy, graphql_name='deletedAt')


class IndexFileUpdateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('name', 'version')
    name = sgqlc.types.Field(IndexTypes, graphql_name='name')
    version = sgqlc.types.Field(String, graphql_name='version')


class IndexFileWhereClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id', 'producing_run_id', 'owner_user_id', 'collection_id', 'name', 'version', 'upstream_database', 'host_organism', 'entity_id')
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')
    producing_run_id = sgqlc.types.Field('IntComparators', graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field('IntComparators', graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field('IntComparators', graphql_name='collectionId')
    name = sgqlc.types.Field('IndexTypesEnumComparators', graphql_name='name')
    version = sgqlc.types.Field('StrComparators', graphql_name='version')
    upstream_database = sgqlc.types.Field('UpstreamDatabaseWhereClause', graphql_name='upstreamDatabase')
    host_organism = sgqlc.types.Field(HostOrganismWhereClause, graphql_name='hostOrganism')
    entity_id = sgqlc.types.Field('UUIDComparators', graphql_name='entityId')


class IndexFileWhereClauseMutations(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')


class IndexTypesEnumComparators(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('_eq', '_neq', '_in', '_nin', '_gt', '_gte', '_lt', '_lte', '_is_null')
    _eq = sgqlc.types.Field(IndexTypes, graphql_name='_eq')
    _neq = sgqlc.types.Field(IndexTypes, graphql_name='_neq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(IndexTypes)), graphql_name='_in')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(IndexTypes)), graphql_name='_nin')
    _gt = sgqlc.types.Field(IndexTypes, graphql_name='_gt')
    _gte = sgqlc.types.Field(IndexTypes, graphql_name='_gte')
    _lt = sgqlc.types.Field(IndexTypes, graphql_name='_lt')
    _lte = sgqlc.types.Field(IndexTypes, graphql_name='_lte')
    _is_null = sgqlc.types.Field(IndexTypes, graphql_name='_is_null')


class IntComparators(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('_eq', '_neq', '_in', '_nin', '_gt', '_gte', '_lt', '_lte', '_is_null')
    _eq = sgqlc.types.Field(Int, graphql_name='_eq')
    _neq = sgqlc.types.Field(Int, graphql_name='_neq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Int)), graphql_name='_in')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Int)), graphql_name='_nin')
    _gt = sgqlc.types.Field(Int, graphql_name='_gt')
    _gte = sgqlc.types.Field(Int, graphql_name='_gte')
    _lt = sgqlc.types.Field(Int, graphql_name='_lt')
    _lte = sgqlc.types.Field(Int, graphql_name='_lte')
    _is_null = sgqlc.types.Field(Int, graphql_name='_is_null')


class MetadatumCreateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('sample_id', 'field_name', 'value', 'producing_run_id', 'collection_id')
    sample_id = sgqlc.types.Field(ID, graphql_name='sampleId')
    field_name = sgqlc.types.Field(String, graphql_name='fieldName')
    value = sgqlc.types.Field(String, graphql_name='value')
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class MetadatumOrderByClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('sample', 'field_name', 'value', 'id', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    sample = sgqlc.types.Field('SampleOrderByClause', graphql_name='sample')
    field_name = sgqlc.types.Field(orderBy, graphql_name='fieldName')
    value = sgqlc.types.Field(orderBy, graphql_name='value')
    id = sgqlc.types.Field(orderBy, graphql_name='id')
    producing_run_id = sgqlc.types.Field(orderBy, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(orderBy, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(orderBy, graphql_name='collectionId')
    created_at = sgqlc.types.Field(orderBy, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(orderBy, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(orderBy, graphql_name='deletedAt')


class MetadatumUpdateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('value',)
    value = sgqlc.types.Field(String, graphql_name='value')


class MetadatumWhereClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id', 'producing_run_id', 'owner_user_id', 'collection_id', 'sample', 'field_name', 'value', 'entity_id')
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(IntComparators, graphql_name='collectionId')
    sample = sgqlc.types.Field('SampleWhereClause', graphql_name='sample')
    field_name = sgqlc.types.Field('StrComparators', graphql_name='fieldName')
    value = sgqlc.types.Field('StrComparators', graphql_name='value')
    entity_id = sgqlc.types.Field('UUIDComparators', graphql_name='entityId')


class MetadatumWhereClauseMutations(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')


class MetricConsensusGenomeCreateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('consensus_genome_id', 'reference_genome_length', 'percent_genome_called', 'percent_identity', 'gc_percent', 'total_reads', 'mapped_reads', 'ref_snps', 'n_actg', 'n_missing', 'n_ambiguous', 'coverage_depth', 'coverage_breadth', 'coverage_bin_size', 'coverage_total_length', 'coverage_viz', 'producing_run_id', 'collection_id')
    consensus_genome_id = sgqlc.types.Field(ID, graphql_name='consensusGenomeId')
    reference_genome_length = sgqlc.types.Field(Float, graphql_name='referenceGenomeLength')
    percent_genome_called = sgqlc.types.Field(Float, graphql_name='percentGenomeCalled')
    percent_identity = sgqlc.types.Field(Float, graphql_name='percentIdentity')
    gc_percent = sgqlc.types.Field(Float, graphql_name='gcPercent')
    total_reads = sgqlc.types.Field(Int, graphql_name='totalReads')
    mapped_reads = sgqlc.types.Field(Int, graphql_name='mappedReads')
    ref_snps = sgqlc.types.Field(Int, graphql_name='refSnps')
    n_actg = sgqlc.types.Field(Int, graphql_name='nActg')
    n_missing = sgqlc.types.Field(Int, graphql_name='nMissing')
    n_ambiguous = sgqlc.types.Field(Int, graphql_name='nAmbiguous')
    coverage_depth = sgqlc.types.Field(Float, graphql_name='coverageDepth')
    coverage_breadth = sgqlc.types.Field(Float, graphql_name='coverageBreadth')
    coverage_bin_size = sgqlc.types.Field(Float, graphql_name='coverageBinSize')
    coverage_total_length = sgqlc.types.Field(Int, graphql_name='coverageTotalLength')
    coverage_viz = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Int)))), graphql_name='coverageViz')
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class MetricConsensusGenomeOrderByClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('consensus_genome', 'reference_genome_length', 'percent_genome_called', 'percent_identity', 'gc_percent', 'total_reads', 'mapped_reads', 'ref_snps', 'n_actg', 'n_missing', 'n_ambiguous', 'coverage_depth', 'coverage_breadth', 'coverage_bin_size', 'coverage_total_length', 'coverage_viz', 'id', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    consensus_genome = sgqlc.types.Field(ConsensusGenomeOrderByClause, graphql_name='consensusGenome')
    reference_genome_length = sgqlc.types.Field(orderBy, graphql_name='referenceGenomeLength')
    percent_genome_called = sgqlc.types.Field(orderBy, graphql_name='percentGenomeCalled')
    percent_identity = sgqlc.types.Field(orderBy, graphql_name='percentIdentity')
    gc_percent = sgqlc.types.Field(orderBy, graphql_name='gcPercent')
    total_reads = sgqlc.types.Field(orderBy, graphql_name='totalReads')
    mapped_reads = sgqlc.types.Field(orderBy, graphql_name='mappedReads')
    ref_snps = sgqlc.types.Field(orderBy, graphql_name='refSnps')
    n_actg = sgqlc.types.Field(orderBy, graphql_name='nActg')
    n_missing = sgqlc.types.Field(orderBy, graphql_name='nMissing')
    n_ambiguous = sgqlc.types.Field(orderBy, graphql_name='nAmbiguous')
    coverage_depth = sgqlc.types.Field(orderBy, graphql_name='coverageDepth')
    coverage_breadth = sgqlc.types.Field(orderBy, graphql_name='coverageBreadth')
    coverage_bin_size = sgqlc.types.Field(orderBy, graphql_name='coverageBinSize')
    coverage_total_length = sgqlc.types.Field(orderBy, graphql_name='coverageTotalLength')
    coverage_viz = sgqlc.types.Field(orderBy, graphql_name='coverageViz')
    id = sgqlc.types.Field(orderBy, graphql_name='id')
    producing_run_id = sgqlc.types.Field(orderBy, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(orderBy, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(orderBy, graphql_name='collectionId')
    created_at = sgqlc.types.Field(orderBy, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(orderBy, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(orderBy, graphql_name='deletedAt')


class MetricConsensusGenomeWhereClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id', 'producing_run_id', 'owner_user_id', 'collection_id', 'consensus_genome', 'reference_genome_length', 'percent_genome_called', 'percent_identity', 'gc_percent', 'total_reads', 'mapped_reads', 'ref_snps', 'n_actg', 'n_missing', 'n_ambiguous', 'coverage_depth', 'coverage_breadth', 'coverage_bin_size', 'coverage_total_length', 'entity_id')
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(IntComparators, graphql_name='collectionId')
    consensus_genome = sgqlc.types.Field(ConsensusGenomeWhereClause, graphql_name='consensusGenome')
    reference_genome_length = sgqlc.types.Field(FloatComparators, graphql_name='referenceGenomeLength')
    percent_genome_called = sgqlc.types.Field(FloatComparators, graphql_name='percentGenomeCalled')
    percent_identity = sgqlc.types.Field(FloatComparators, graphql_name='percentIdentity')
    gc_percent = sgqlc.types.Field(FloatComparators, graphql_name='gcPercent')
    total_reads = sgqlc.types.Field(IntComparators, graphql_name='totalReads')
    mapped_reads = sgqlc.types.Field(IntComparators, graphql_name='mappedReads')
    ref_snps = sgqlc.types.Field(IntComparators, graphql_name='refSnps')
    n_actg = sgqlc.types.Field(IntComparators, graphql_name='nActg')
    n_missing = sgqlc.types.Field(IntComparators, graphql_name='nMissing')
    n_ambiguous = sgqlc.types.Field(IntComparators, graphql_name='nAmbiguous')
    coverage_depth = sgqlc.types.Field(FloatComparators, graphql_name='coverageDepth')
    coverage_breadth = sgqlc.types.Field(FloatComparators, graphql_name='coverageBreadth')
    coverage_bin_size = sgqlc.types.Field(FloatComparators, graphql_name='coverageBinSize')
    coverage_total_length = sgqlc.types.Field(IntComparators, graphql_name='coverageTotalLength')
    entity_id = sgqlc.types.Field('UUIDComparators', graphql_name='entityId')


class MetricConsensusGenomeWhereClauseMutations(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')


class NucleicAcidEnumComparators(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('_eq', '_neq', '_in', '_nin', '_gt', '_gte', '_lt', '_lte', '_is_null')
    _eq = sgqlc.types.Field(NucleicAcid, graphql_name='_eq')
    _neq = sgqlc.types.Field(NucleicAcid, graphql_name='_neq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(NucleicAcid)), graphql_name='_in')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(NucleicAcid)), graphql_name='_nin')
    _gt = sgqlc.types.Field(NucleicAcid, graphql_name='_gt')
    _gte = sgqlc.types.Field(NucleicAcid, graphql_name='_gte')
    _lt = sgqlc.types.Field(NucleicAcid, graphql_name='_lt')
    _lte = sgqlc.types.Field(NucleicAcid, graphql_name='_lte')
    _is_null = sgqlc.types.Field(NucleicAcid, graphql_name='_is_null')


class PhylogeneticTreeCreateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('format', 'producing_run_id', 'collection_id')
    format = sgqlc.types.Field(PhylogeneticTreeFormat, graphql_name='format')
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class PhylogeneticTreeFormatEnumComparators(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('_eq', '_neq', '_in', '_nin', '_gt', '_gte', '_lt', '_lte', '_is_null')
    _eq = sgqlc.types.Field(PhylogeneticTreeFormat, graphql_name='_eq')
    _neq = sgqlc.types.Field(PhylogeneticTreeFormat, graphql_name='_neq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(PhylogeneticTreeFormat)), graphql_name='_in')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(PhylogeneticTreeFormat)), graphql_name='_nin')
    _gt = sgqlc.types.Field(PhylogeneticTreeFormat, graphql_name='_gt')
    _gte = sgqlc.types.Field(PhylogeneticTreeFormat, graphql_name='_gte')
    _lt = sgqlc.types.Field(PhylogeneticTreeFormat, graphql_name='_lt')
    _lte = sgqlc.types.Field(PhylogeneticTreeFormat, graphql_name='_lte')
    _is_null = sgqlc.types.Field(PhylogeneticTreeFormat, graphql_name='_is_null')


class PhylogeneticTreeOrderByClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('format', 'id', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    format = sgqlc.types.Field(orderBy, graphql_name='format')
    id = sgqlc.types.Field(orderBy, graphql_name='id')
    producing_run_id = sgqlc.types.Field(orderBy, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(orderBy, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(orderBy, graphql_name='collectionId')
    created_at = sgqlc.types.Field(orderBy, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(orderBy, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(orderBy, graphql_name='deletedAt')


class PhylogeneticTreeUpdateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('format',)
    format = sgqlc.types.Field(PhylogeneticTreeFormat, graphql_name='format')


class PhylogeneticTreeWhereClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id', 'producing_run_id', 'owner_user_id', 'collection_id', 'format', 'entity_id')
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(IntComparators, graphql_name='collectionId')
    format = sgqlc.types.Field(PhylogeneticTreeFormatEnumComparators, graphql_name='format')
    entity_id = sgqlc.types.Field('UUIDComparators', graphql_name='entityId')


class PhylogeneticTreeWhereClauseMutations(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')


class ReferenceGenomeCreateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('name', 'producing_run_id', 'collection_id')
    name = sgqlc.types.Field(String, graphql_name='name')
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class ReferenceGenomeOrderByClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('name', 'id', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    name = sgqlc.types.Field(orderBy, graphql_name='name')
    id = sgqlc.types.Field(orderBy, graphql_name='id')
    producing_run_id = sgqlc.types.Field(orderBy, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(orderBy, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(orderBy, graphql_name='collectionId')
    created_at = sgqlc.types.Field(orderBy, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(orderBy, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(orderBy, graphql_name='deletedAt')


class ReferenceGenomeUpdateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('name',)
    name = sgqlc.types.Field(String, graphql_name='name')


class ReferenceGenomeWhereClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id', 'producing_run_id', 'owner_user_id', 'collection_id', 'name', 'consensus_genomes', 'entity_id')
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(IntComparators, graphql_name='collectionId')
    name = sgqlc.types.Field('StrComparators', graphql_name='name')
    consensus_genomes = sgqlc.types.Field(ConsensusGenomeWhereClause, graphql_name='consensusGenomes')
    entity_id = sgqlc.types.Field('UUIDComparators', graphql_name='entityId')


class ReferenceGenomeWhereClauseMutations(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')


class SampleCreateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('rails_sample_id', 'name', 'sample_type', 'water_control', 'collection_date', 'collection_location', 'notes', 'host_organism_id', 'producing_run_id', 'collection_id')
    rails_sample_id = sgqlc.types.Field(Int, graphql_name='railsSampleId')
    name = sgqlc.types.Field(String, graphql_name='name')
    sample_type = sgqlc.types.Field(String, graphql_name='sampleType')
    water_control = sgqlc.types.Field(Boolean, graphql_name='waterControl')
    collection_date = sgqlc.types.Field(DateTime, graphql_name='collectionDate')
    collection_location = sgqlc.types.Field(String, graphql_name='collectionLocation')
    notes = sgqlc.types.Field(String, graphql_name='notes')
    host_organism_id = sgqlc.types.Field(ID, graphql_name='hostOrganismId')
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class SampleOrderByClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('rails_sample_id', 'name', 'sample_type', 'water_control', 'collection_date', 'collection_location', 'notes', 'host_organism', 'id', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    rails_sample_id = sgqlc.types.Field(orderBy, graphql_name='railsSampleId')
    name = sgqlc.types.Field(orderBy, graphql_name='name')
    sample_type = sgqlc.types.Field(orderBy, graphql_name='sampleType')
    water_control = sgqlc.types.Field(orderBy, graphql_name='waterControl')
    collection_date = sgqlc.types.Field(orderBy, graphql_name='collectionDate')
    collection_location = sgqlc.types.Field(orderBy, graphql_name='collectionLocation')
    notes = sgqlc.types.Field(orderBy, graphql_name='notes')
    host_organism = sgqlc.types.Field(HostOrganismOrderByClause, graphql_name='hostOrganism')
    id = sgqlc.types.Field(orderBy, graphql_name='id')
    producing_run_id = sgqlc.types.Field(orderBy, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(orderBy, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(orderBy, graphql_name='collectionId')
    created_at = sgqlc.types.Field(orderBy, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(orderBy, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(orderBy, graphql_name='deletedAt')


class SampleUpdateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('name', 'sample_type', 'water_control', 'collection_date', 'collection_location', 'notes')
    name = sgqlc.types.Field(String, graphql_name='name')
    sample_type = sgqlc.types.Field(String, graphql_name='sampleType')
    water_control = sgqlc.types.Field(Boolean, graphql_name='waterControl')
    collection_date = sgqlc.types.Field(DateTime, graphql_name='collectionDate')
    collection_location = sgqlc.types.Field(String, graphql_name='collectionLocation')
    notes = sgqlc.types.Field(String, graphql_name='notes')


class SampleWhereClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id', 'producing_run_id', 'owner_user_id', 'collection_id', 'rails_sample_id', 'name', 'sample_type', 'water_control', 'collection_date', 'collection_location', 'notes', 'host_organism', 'sequencing_reads', 'metadatas', 'entity_id')
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(IntComparators, graphql_name='collectionId')
    rails_sample_id = sgqlc.types.Field(IntComparators, graphql_name='railsSampleId')
    name = sgqlc.types.Field('StrComparators', graphql_name='name')
    sample_type = sgqlc.types.Field('StrComparators', graphql_name='sampleType')
    water_control = sgqlc.types.Field(BoolComparators, graphql_name='waterControl')
    collection_date = sgqlc.types.Field(DatetimeComparators, graphql_name='collectionDate')
    collection_location = sgqlc.types.Field('StrComparators', graphql_name='collectionLocation')
    notes = sgqlc.types.Field('StrComparators', graphql_name='notes')
    host_organism = sgqlc.types.Field(HostOrganismWhereClause, graphql_name='hostOrganism')
    sequencing_reads = sgqlc.types.Field('SequencingReadWhereClause', graphql_name='sequencingReads')
    metadatas = sgqlc.types.Field(MetadatumWhereClause, graphql_name='metadatas')
    entity_id = sgqlc.types.Field('UUIDComparators', graphql_name='entityId')


class SampleWhereClauseMutations(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')


class SequencingProtocolEnumComparators(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('_eq', '_neq', '_in', '_nin', '_gt', '_gte', '_lt', '_lte', '_is_null')
    _eq = sgqlc.types.Field(SequencingProtocol, graphql_name='_eq')
    _neq = sgqlc.types.Field(SequencingProtocol, graphql_name='_neq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(SequencingProtocol)), graphql_name='_in')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(SequencingProtocol)), graphql_name='_nin')
    _gt = sgqlc.types.Field(SequencingProtocol, graphql_name='_gt')
    _gte = sgqlc.types.Field(SequencingProtocol, graphql_name='_gte')
    _lt = sgqlc.types.Field(SequencingProtocol, graphql_name='_lt')
    _lte = sgqlc.types.Field(SequencingProtocol, graphql_name='_lte')
    _is_null = sgqlc.types.Field(SequencingProtocol, graphql_name='_is_null')


class SequencingReadCreateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('sample_id', 'protocol', 'technology', 'nucleic_acid', 'clearlabs_export', 'medaka_model', 'taxon_id', 'primer_file_id', 'producing_run_id', 'collection_id')
    sample_id = sgqlc.types.Field(ID, graphql_name='sampleId')
    protocol = sgqlc.types.Field(SequencingProtocol, graphql_name='protocol')
    technology = sgqlc.types.Field(SequencingTechnology, graphql_name='technology')
    nucleic_acid = sgqlc.types.Field(NucleicAcid, graphql_name='nucleicAcid')
    clearlabs_export = sgqlc.types.Field(Boolean, graphql_name='clearlabsExport')
    medaka_model = sgqlc.types.Field(String, graphql_name='medakaModel')
    taxon_id = sgqlc.types.Field(ID, graphql_name='taxonId')
    primer_file_id = sgqlc.types.Field(ID, graphql_name='primerFileId')
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class SequencingReadOrderByClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('sample', 'protocol', 'technology', 'nucleic_acid', 'clearlabs_export', 'medaka_model', 'taxon', 'primer_file', 'id', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    sample = sgqlc.types.Field(SampleOrderByClause, graphql_name='sample')
    protocol = sgqlc.types.Field(orderBy, graphql_name='protocol')
    technology = sgqlc.types.Field(orderBy, graphql_name='technology')
    nucleic_acid = sgqlc.types.Field(orderBy, graphql_name='nucleicAcid')
    clearlabs_export = sgqlc.types.Field(orderBy, graphql_name='clearlabsExport')
    medaka_model = sgqlc.types.Field(orderBy, graphql_name='medakaModel')
    taxon = sgqlc.types.Field('TaxonOrderByClause', graphql_name='taxon')
    primer_file = sgqlc.types.Field(GenomicRangeOrderByClause, graphql_name='primerFile')
    id = sgqlc.types.Field(orderBy, graphql_name='id')
    producing_run_id = sgqlc.types.Field(orderBy, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(orderBy, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(orderBy, graphql_name='collectionId')
    created_at = sgqlc.types.Field(orderBy, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(orderBy, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(orderBy, graphql_name='deletedAt')


class SequencingReadUpdateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('nucleic_acid', 'clearlabs_export', 'medaka_model')
    nucleic_acid = sgqlc.types.Field(NucleicAcid, graphql_name='nucleicAcid')
    clearlabs_export = sgqlc.types.Field(Boolean, graphql_name='clearlabsExport')
    medaka_model = sgqlc.types.Field(String, graphql_name='medakaModel')


class SequencingReadWhereClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id', 'producing_run_id', 'owner_user_id', 'collection_id', 'sample', 'protocol', 'technology', 'nucleic_acid', 'clearlabs_export', 'medaka_model', 'taxon', 'primer_file', 'consensus_genomes', 'entity_id')
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(IntComparators, graphql_name='collectionId')
    sample = sgqlc.types.Field(SampleWhereClause, graphql_name='sample')
    protocol = sgqlc.types.Field(SequencingProtocolEnumComparators, graphql_name='protocol')
    technology = sgqlc.types.Field('SequencingTechnologyEnumComparators', graphql_name='technology')
    nucleic_acid = sgqlc.types.Field(NucleicAcidEnumComparators, graphql_name='nucleicAcid')
    clearlabs_export = sgqlc.types.Field(BoolComparators, graphql_name='clearlabsExport')
    medaka_model = sgqlc.types.Field('StrComparators', graphql_name='medakaModel')
    taxon = sgqlc.types.Field('TaxonWhereClause', graphql_name='taxon')
    primer_file = sgqlc.types.Field(GenomicRangeWhereClause, graphql_name='primerFile')
    consensus_genomes = sgqlc.types.Field(ConsensusGenomeWhereClause, graphql_name='consensusGenomes')
    entity_id = sgqlc.types.Field('UUIDComparators', graphql_name='entityId')


class SequencingReadWhereClauseMutations(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')


class SequencingTechnologyEnumComparators(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('_eq', '_neq', '_in', '_nin', '_gt', '_gte', '_lt', '_lte', '_is_null')
    _eq = sgqlc.types.Field(SequencingTechnology, graphql_name='_eq')
    _neq = sgqlc.types.Field(SequencingTechnology, graphql_name='_neq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(SequencingTechnology)), graphql_name='_in')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(SequencingTechnology)), graphql_name='_nin')
    _gt = sgqlc.types.Field(SequencingTechnology, graphql_name='_gt')
    _gte = sgqlc.types.Field(SequencingTechnology, graphql_name='_gte')
    _lt = sgqlc.types.Field(SequencingTechnology, graphql_name='_lt')
    _lte = sgqlc.types.Field(SequencingTechnology, graphql_name='_lte')
    _is_null = sgqlc.types.Field(SequencingTechnology, graphql_name='_is_null')


class StrComparators(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('_eq', '_neq', '_in', '_nin', '_is_null', '_gt', '_gte', '_lt', '_lte', '_like', '_nlike', '_ilike', '_nilike', '_regex', '_nregex', '_iregex', '_niregex')
    _eq = sgqlc.types.Field(String, graphql_name='_eq')
    _neq = sgqlc.types.Field(String, graphql_name='_neq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='_in')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='_nin')
    _is_null = sgqlc.types.Field(Int, graphql_name='_is_null')
    _gt = sgqlc.types.Field(String, graphql_name='_gt')
    _gte = sgqlc.types.Field(String, graphql_name='_gte')
    _lt = sgqlc.types.Field(String, graphql_name='_lt')
    _lte = sgqlc.types.Field(String, graphql_name='_lte')
    _like = sgqlc.types.Field(String, graphql_name='_like')
    _nlike = sgqlc.types.Field(String, graphql_name='_nlike')
    _ilike = sgqlc.types.Field(String, graphql_name='_ilike')
    _nilike = sgqlc.types.Field(String, graphql_name='_nilike')
    _regex = sgqlc.types.Field(String, graphql_name='_regex')
    _nregex = sgqlc.types.Field(String, graphql_name='_nregex')
    _iregex = sgqlc.types.Field(String, graphql_name='_iregex')
    _niregex = sgqlc.types.Field(String, graphql_name='_niregex')


class TaxonCreateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('wikipedia_id', 'description', 'common_name', 'name', 'is_phage', 'upstream_database_id', 'upstream_database_identifier', 'level', 'producing_run_id', 'collection_id')
    wikipedia_id = sgqlc.types.Field(String, graphql_name='wikipediaId')
    description = sgqlc.types.Field(String, graphql_name='description')
    common_name = sgqlc.types.Field(String, graphql_name='commonName')
    name = sgqlc.types.Field(String, graphql_name='name')
    is_phage = sgqlc.types.Field(Boolean, graphql_name='isPhage')
    upstream_database_id = sgqlc.types.Field(ID, graphql_name='upstreamDatabaseId')
    upstream_database_identifier = sgqlc.types.Field(String, graphql_name='upstreamDatabaseIdentifier')
    level = sgqlc.types.Field(TaxonLevel, graphql_name='level')
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class TaxonLevelEnumComparators(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('_eq', '_neq', '_in', '_nin', '_gt', '_gte', '_lt', '_lte', '_is_null')
    _eq = sgqlc.types.Field(TaxonLevel, graphql_name='_eq')
    _neq = sgqlc.types.Field(TaxonLevel, graphql_name='_neq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(TaxonLevel)), graphql_name='_in')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(TaxonLevel)), graphql_name='_nin')
    _gt = sgqlc.types.Field(TaxonLevel, graphql_name='_gt')
    _gte = sgqlc.types.Field(TaxonLevel, graphql_name='_gte')
    _lt = sgqlc.types.Field(TaxonLevel, graphql_name='_lt')
    _lte = sgqlc.types.Field(TaxonLevel, graphql_name='_lte')
    _is_null = sgqlc.types.Field(TaxonLevel, graphql_name='_is_null')


class TaxonOrderByClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('wikipedia_id', 'description', 'common_name', 'name', 'is_phage', 'upstream_database', 'upstream_database_identifier', 'level', 'tax_parent', 'tax_subspecies', 'tax_species', 'tax_genus', 'tax_family', 'tax_order', 'tax_class', 'tax_phylum', 'tax_kingdom', 'tax_superkingdom', 'id', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    wikipedia_id = sgqlc.types.Field(orderBy, graphql_name='wikipediaId')
    description = sgqlc.types.Field(orderBy, graphql_name='description')
    common_name = sgqlc.types.Field(orderBy, graphql_name='commonName')
    name = sgqlc.types.Field(orderBy, graphql_name='name')
    is_phage = sgqlc.types.Field(orderBy, graphql_name='isPhage')
    upstream_database = sgqlc.types.Field('UpstreamDatabaseOrderByClause', graphql_name='upstreamDatabase')
    upstream_database_identifier = sgqlc.types.Field(orderBy, graphql_name='upstreamDatabaseIdentifier')
    level = sgqlc.types.Field(orderBy, graphql_name='level')
    tax_parent = sgqlc.types.Field(orderBy, graphql_name='taxParent')
    tax_subspecies = sgqlc.types.Field(orderBy, graphql_name='taxSubspecies')
    tax_species = sgqlc.types.Field(orderBy, graphql_name='taxSpecies')
    tax_genus = sgqlc.types.Field(orderBy, graphql_name='taxGenus')
    tax_family = sgqlc.types.Field(orderBy, graphql_name='taxFamily')
    tax_order = sgqlc.types.Field(orderBy, graphql_name='taxOrder')
    tax_class = sgqlc.types.Field(orderBy, graphql_name='taxClass')
    tax_phylum = sgqlc.types.Field(orderBy, graphql_name='taxPhylum')
    tax_kingdom = sgqlc.types.Field(orderBy, graphql_name='taxKingdom')
    tax_superkingdom = sgqlc.types.Field(orderBy, graphql_name='taxSuperkingdom')
    id = sgqlc.types.Field(orderBy, graphql_name='id')
    producing_run_id = sgqlc.types.Field(orderBy, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(orderBy, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(orderBy, graphql_name='collectionId')
    created_at = sgqlc.types.Field(orderBy, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(orderBy, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(orderBy, graphql_name='deletedAt')


class TaxonUpdateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('wikipedia_id', 'description', 'common_name', 'is_phage', 'level')
    wikipedia_id = sgqlc.types.Field(String, graphql_name='wikipediaId')
    description = sgqlc.types.Field(String, graphql_name='description')
    common_name = sgqlc.types.Field(String, graphql_name='commonName')
    is_phage = sgqlc.types.Field(Boolean, graphql_name='isPhage')
    level = sgqlc.types.Field(TaxonLevel, graphql_name='level')


class TaxonWhereClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id', 'producing_run_id', 'owner_user_id', 'collection_id', 'wikipedia_id', 'description', 'common_name', 'name', 'is_phage', 'upstream_database', 'upstream_database_identifier', 'level', 'consensus_genomes', 'sequencing_reads', 'entity_id')
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(IntComparators, graphql_name='collectionId')
    wikipedia_id = sgqlc.types.Field(StrComparators, graphql_name='wikipediaId')
    description = sgqlc.types.Field(StrComparators, graphql_name='description')
    common_name = sgqlc.types.Field(StrComparators, graphql_name='commonName')
    name = sgqlc.types.Field(StrComparators, graphql_name='name')
    is_phage = sgqlc.types.Field(BoolComparators, graphql_name='isPhage')
    upstream_database = sgqlc.types.Field('UpstreamDatabaseWhereClause', graphql_name='upstreamDatabase')
    upstream_database_identifier = sgqlc.types.Field(StrComparators, graphql_name='upstreamDatabaseIdentifier')
    level = sgqlc.types.Field(TaxonLevelEnumComparators, graphql_name='level')
    consensus_genomes = sgqlc.types.Field(ConsensusGenomeWhereClause, graphql_name='consensusGenomes')
    sequencing_reads = sgqlc.types.Field(SequencingReadWhereClause, graphql_name='sequencingReads')
    entity_id = sgqlc.types.Field('UUIDComparators', graphql_name='entityId')


class TaxonWhereClauseMutations(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field('UUIDComparators', graphql_name='id')


class UUIDComparators(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('_eq', '_neq', '_in', '_nin', '_gt', '_gte', '_lt', '_lte')
    _eq = sgqlc.types.Field(UUID, graphql_name='_eq')
    _neq = sgqlc.types.Field(UUID, graphql_name='_neq')
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(UUID)), graphql_name='_in')
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(UUID)), graphql_name='_nin')
    _gt = sgqlc.types.Field(UUID, graphql_name='_gt')
    _gte = sgqlc.types.Field(UUID, graphql_name='_gte')
    _lt = sgqlc.types.Field(UUID, graphql_name='_lt')
    _lte = sgqlc.types.Field(UUID, graphql_name='_lte')


class UpstreamDatabaseCreateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('name', 'producing_run_id', 'collection_id')
    name = sgqlc.types.Field(String, graphql_name='name')
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class UpstreamDatabaseOrderByClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('name', 'id', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    name = sgqlc.types.Field(orderBy, graphql_name='name')
    id = sgqlc.types.Field(orderBy, graphql_name='id')
    producing_run_id = sgqlc.types.Field(orderBy, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(orderBy, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(orderBy, graphql_name='collectionId')
    created_at = sgqlc.types.Field(orderBy, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(orderBy, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(orderBy, graphql_name='deletedAt')


class UpstreamDatabaseUpdateInput(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('name',)
    name = sgqlc.types.Field(String, graphql_name='name')


class UpstreamDatabaseWhereClause(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id', 'producing_run_id', 'owner_user_id', 'collection_id', 'name', 'taxa', 'indexes', 'accessions', 'entity_id')
    id = sgqlc.types.Field(UUIDComparators, graphql_name='id')
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(IntComparators, graphql_name='collectionId')
    name = sgqlc.types.Field(StrComparators, graphql_name='name')
    taxa = sgqlc.types.Field(TaxonWhereClause, graphql_name='taxa')
    indexes = sgqlc.types.Field(IndexFileWhereClause, graphql_name='indexes')
    accessions = sgqlc.types.Field(AccessionWhereClause, graphql_name='accessions')
    entity_id = sgqlc.types.Field(UUIDComparators, graphql_name='entityId')


class UpstreamDatabaseWhereClauseMutations(sgqlc.types.Input):
    __schema__ = entities_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(UUIDComparators, graphql_name='id')



########################################################################
# Output Objects and Interfaces
########################################################################
class Node(sgqlc.types.Interface):
    __schema__ = entities_schema
    __field_names__ = ('_id',)
    _id = sgqlc.types.Field(sgqlc.types.non_null(GlobalID), graphql_name='_id')


class EntityInterface(sgqlc.types.Interface):
    __schema__ = entities_schema
    __field_names__ = ('_id',)
    _id = sgqlc.types.Field(sgqlc.types.non_null(GlobalID), graphql_name='_id')


class AccessionAggregate(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('aggregate',)
    aggregate = sgqlc.types.Field('AccessionAggregateFunctions', graphql_name='aggregate')


class AccessionAggregateFunctions(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('sum', 'avg', 'min', 'max', 'stddev', 'variance', 'count')
    sum = sgqlc.types.Field('AccessionNumericalColumns', graphql_name='sum')
    avg = sgqlc.types.Field('AccessionNumericalColumns', graphql_name='avg')
    min = sgqlc.types.Field('AccessionMinMaxColumns', graphql_name='min')
    max = sgqlc.types.Field('AccessionMinMaxColumns', graphql_name='max')
    stddev = sgqlc.types.Field('AccessionNumericalColumns', graphql_name='stddev')
    variance = sgqlc.types.Field('AccessionNumericalColumns', graphql_name='variance')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=False)),
        ('columns', sgqlc.types.Arg(AccessionCountColumns, graphql_name='columns', default=None)),
))
    )


class AccessionConnection(sgqlc.types.relay.Connection):
    __schema__ = entities_schema
    __field_names__ = ('page_info', 'edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('AccessionEdge'))), graphql_name='edges')


class AccessionEdge(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Accession'), graphql_name='node')


class AccessionMinMaxColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('accession_id', 'accession_name', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    accession_id = sgqlc.types.Field(String, graphql_name='accessionId')
    accession_name = sgqlc.types.Field(String, graphql_name='accessionName')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(DateTime, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class AccessionNumericalColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('owner_user_id', 'collection_id')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class BulkDownloadAggregate(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('aggregate',)
    aggregate = sgqlc.types.Field('BulkDownloadAggregateFunctions', graphql_name='aggregate')


class BulkDownloadAggregateFunctions(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('sum', 'avg', 'min', 'max', 'stddev', 'variance', 'count')
    sum = sgqlc.types.Field('BulkDownloadNumericalColumns', graphql_name='sum')
    avg = sgqlc.types.Field('BulkDownloadNumericalColumns', graphql_name='avg')
    min = sgqlc.types.Field('BulkDownloadMinMaxColumns', graphql_name='min')
    max = sgqlc.types.Field('BulkDownloadMinMaxColumns', graphql_name='max')
    stddev = sgqlc.types.Field('BulkDownloadNumericalColumns', graphql_name='stddev')
    variance = sgqlc.types.Field('BulkDownloadNumericalColumns', graphql_name='variance')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=False)),
        ('columns', sgqlc.types.Arg(BulkDownloadCountColumns, graphql_name='columns', default=None)),
))
    )


class BulkDownloadMinMaxColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(DateTime, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class BulkDownloadNumericalColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('owner_user_id', 'collection_id')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class ConsensusGenomeAggregate(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('aggregate',)
    aggregate = sgqlc.types.Field('ConsensusGenomeAggregateFunctions', graphql_name='aggregate')


class ConsensusGenomeAggregateFunctions(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('sum', 'avg', 'min', 'max', 'stddev', 'variance', 'count')
    sum = sgqlc.types.Field('ConsensusGenomeNumericalColumns', graphql_name='sum')
    avg = sgqlc.types.Field('ConsensusGenomeNumericalColumns', graphql_name='avg')
    min = sgqlc.types.Field('ConsensusGenomeMinMaxColumns', graphql_name='min')
    max = sgqlc.types.Field('ConsensusGenomeMinMaxColumns', graphql_name='max')
    stddev = sgqlc.types.Field('ConsensusGenomeNumericalColumns', graphql_name='stddev')
    variance = sgqlc.types.Field('ConsensusGenomeNumericalColumns', graphql_name='variance')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=False)),
        ('columns', sgqlc.types.Arg(ConsensusGenomeCountColumns, graphql_name='columns', default=None)),
))
    )


class ConsensusGenomeConnection(sgqlc.types.relay.Connection):
    __schema__ = entities_schema
    __field_names__ = ('page_info', 'edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ConsensusGenomeEdge'))), graphql_name='edges')


class ConsensusGenomeEdge(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('ConsensusGenome'), graphql_name='node')


class ConsensusGenomeMinMaxColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(DateTime, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class ConsensusGenomeNumericalColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('owner_user_id', 'collection_id')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class Entity(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('id', 'type', 'producing_run_id', 'owner_user_id', 'collection_id')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')
    producing_run_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='collectionId')


class File(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('id', 'entity_id', 'entity_field_name', 'entity', 'status', 'protocol', 'namespace', 'path', 'file_format', 'compression_type', 'size', 'download_link', 'contents')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    entity_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='entityId')
    entity_field_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='entityFieldName')
    entity = sgqlc.types.Field(Entity, graphql_name='entity', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(EntityWhereClause, graphql_name='where', default=None)),
))
    )
    status = sgqlc.types.Field(sgqlc.types.non_null(FileStatus), graphql_name='status')
    protocol = sgqlc.types.Field(sgqlc.types.non_null(FileAccessProtocol), graphql_name='protocol')
    namespace = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='namespace')
    path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='path')
    file_format = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='fileFormat')
    compression_type = sgqlc.types.Field(Int, graphql_name='compressionType')
    size = sgqlc.types.Field(Int, graphql_name='size')
    download_link = sgqlc.types.Field('SignedURL', graphql_name='downloadLink', args=sgqlc.types.ArgDict((
        ('expiration', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='expiration', default=3600)),
))
    )
    contents = sgqlc.types.Field(String, graphql_name='contents')


class GenomicRangeAggregate(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('aggregate',)
    aggregate = sgqlc.types.Field('GenomicRangeAggregateFunctions', graphql_name='aggregate')


class GenomicRangeAggregateFunctions(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('sum', 'avg', 'min', 'max', 'stddev', 'variance', 'count')
    sum = sgqlc.types.Field('GenomicRangeNumericalColumns', graphql_name='sum')
    avg = sgqlc.types.Field('GenomicRangeNumericalColumns', graphql_name='avg')
    min = sgqlc.types.Field('GenomicRangeMinMaxColumns', graphql_name='min')
    max = sgqlc.types.Field('GenomicRangeMinMaxColumns', graphql_name='max')
    stddev = sgqlc.types.Field('GenomicRangeNumericalColumns', graphql_name='stddev')
    variance = sgqlc.types.Field('GenomicRangeNumericalColumns', graphql_name='variance')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=False)),
        ('columns', sgqlc.types.Arg(GenomicRangeCountColumns, graphql_name='columns', default=None)),
))
    )


class GenomicRangeMinMaxColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(DateTime, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class GenomicRangeNumericalColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('owner_user_id', 'collection_id')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class HostOrganismAggregate(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('aggregate',)
    aggregate = sgqlc.types.Field('HostOrganismAggregateFunctions', graphql_name='aggregate')


class HostOrganismAggregateFunctions(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('sum', 'avg', 'min', 'max', 'stddev', 'variance', 'count')
    sum = sgqlc.types.Field('HostOrganismNumericalColumns', graphql_name='sum')
    avg = sgqlc.types.Field('HostOrganismNumericalColumns', graphql_name='avg')
    min = sgqlc.types.Field('HostOrganismMinMaxColumns', graphql_name='min')
    max = sgqlc.types.Field('HostOrganismMinMaxColumns', graphql_name='max')
    stddev = sgqlc.types.Field('HostOrganismNumericalColumns', graphql_name='stddev')
    variance = sgqlc.types.Field('HostOrganismNumericalColumns', graphql_name='variance')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=False)),
        ('columns', sgqlc.types.Arg(HostOrganismCountColumns, graphql_name='columns', default=None)),
))
    )


class HostOrganismMinMaxColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('name', 'version', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    name = sgqlc.types.Field(String, graphql_name='name')
    version = sgqlc.types.Field(String, graphql_name='version')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(DateTime, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class HostOrganismNumericalColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('owner_user_id', 'collection_id')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class IndexFileAggregate(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('aggregate',)
    aggregate = sgqlc.types.Field('IndexFileAggregateFunctions', graphql_name='aggregate')


class IndexFileAggregateFunctions(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('sum', 'avg', 'min', 'max', 'stddev', 'variance', 'count')
    sum = sgqlc.types.Field('IndexFileNumericalColumns', graphql_name='sum')
    avg = sgqlc.types.Field('IndexFileNumericalColumns', graphql_name='avg')
    min = sgqlc.types.Field('IndexFileMinMaxColumns', graphql_name='min')
    max = sgqlc.types.Field('IndexFileMinMaxColumns', graphql_name='max')
    stddev = sgqlc.types.Field('IndexFileNumericalColumns', graphql_name='stddev')
    variance = sgqlc.types.Field('IndexFileNumericalColumns', graphql_name='variance')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=False)),
        ('columns', sgqlc.types.Arg(IndexFileCountColumns, graphql_name='columns', default=None)),
))
    )


class IndexFileConnection(sgqlc.types.relay.Connection):
    __schema__ = entities_schema
    __field_names__ = ('page_info', 'edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('IndexFileEdge'))), graphql_name='edges')


class IndexFileEdge(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('IndexFile'), graphql_name='node')


class IndexFileMinMaxColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('version', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    version = sgqlc.types.Field(String, graphql_name='version')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(DateTime, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class IndexFileNumericalColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('owner_user_id', 'collection_id')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class MetadatumAggregate(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('aggregate',)
    aggregate = sgqlc.types.Field('MetadatumAggregateFunctions', graphql_name='aggregate')


class MetadatumAggregateFunctions(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('sum', 'avg', 'min', 'max', 'stddev', 'variance', 'count')
    sum = sgqlc.types.Field('MetadatumNumericalColumns', graphql_name='sum')
    avg = sgqlc.types.Field('MetadatumNumericalColumns', graphql_name='avg')
    min = sgqlc.types.Field('MetadatumMinMaxColumns', graphql_name='min')
    max = sgqlc.types.Field('MetadatumMinMaxColumns', graphql_name='max')
    stddev = sgqlc.types.Field('MetadatumNumericalColumns', graphql_name='stddev')
    variance = sgqlc.types.Field('MetadatumNumericalColumns', graphql_name='variance')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=False)),
        ('columns', sgqlc.types.Arg(MetadatumCountColumns, graphql_name='columns', default=None)),
))
    )


class MetadatumConnection(sgqlc.types.relay.Connection):
    __schema__ = entities_schema
    __field_names__ = ('page_info', 'edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null('PageInfo'), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MetadatumEdge'))), graphql_name='edges')


class MetadatumEdge(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Metadatum'), graphql_name='node')


class MetadatumMinMaxColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('field_name', 'value', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    field_name = sgqlc.types.Field(String, graphql_name='fieldName')
    value = sgqlc.types.Field(String, graphql_name='value')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(DateTime, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class MetadatumNumericalColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('owner_user_id', 'collection_id')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class MetricConsensusGenomeAggregate(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('aggregate',)
    aggregate = sgqlc.types.Field('MetricConsensusGenomeAggregateFunctions', graphql_name='aggregate')


class MetricConsensusGenomeAggregateFunctions(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('sum', 'avg', 'min', 'max', 'stddev', 'variance', 'count')
    sum = sgqlc.types.Field('MetricConsensusGenomeNumericalColumns', graphql_name='sum')
    avg = sgqlc.types.Field('MetricConsensusGenomeNumericalColumns', graphql_name='avg')
    min = sgqlc.types.Field('MetricConsensusGenomeMinMaxColumns', graphql_name='min')
    max = sgqlc.types.Field('MetricConsensusGenomeMinMaxColumns', graphql_name='max')
    stddev = sgqlc.types.Field('MetricConsensusGenomeNumericalColumns', graphql_name='stddev')
    variance = sgqlc.types.Field('MetricConsensusGenomeNumericalColumns', graphql_name='variance')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=False)),
        ('columns', sgqlc.types.Arg(MetricConsensusGenomeCountColumns, graphql_name='columns', default=None)),
))
    )


class MetricConsensusGenomeMinMaxColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('reference_genome_length', 'percent_genome_called', 'percent_identity', 'gc_percent', 'total_reads', 'mapped_reads', 'ref_snps', 'n_actg', 'n_missing', 'n_ambiguous', 'coverage_depth', 'coverage_breadth', 'coverage_bin_size', 'coverage_total_length', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    reference_genome_length = sgqlc.types.Field(Float, graphql_name='referenceGenomeLength')
    percent_genome_called = sgqlc.types.Field(Float, graphql_name='percentGenomeCalled')
    percent_identity = sgqlc.types.Field(Float, graphql_name='percentIdentity')
    gc_percent = sgqlc.types.Field(Float, graphql_name='gcPercent')
    total_reads = sgqlc.types.Field(Int, graphql_name='totalReads')
    mapped_reads = sgqlc.types.Field(Int, graphql_name='mappedReads')
    ref_snps = sgqlc.types.Field(Int, graphql_name='refSnps')
    n_actg = sgqlc.types.Field(Int, graphql_name='nActg')
    n_missing = sgqlc.types.Field(Int, graphql_name='nMissing')
    n_ambiguous = sgqlc.types.Field(Int, graphql_name='nAmbiguous')
    coverage_depth = sgqlc.types.Field(Float, graphql_name='coverageDepth')
    coverage_breadth = sgqlc.types.Field(Float, graphql_name='coverageBreadth')
    coverage_bin_size = sgqlc.types.Field(Float, graphql_name='coverageBinSize')
    coverage_total_length = sgqlc.types.Field(Int, graphql_name='coverageTotalLength')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(DateTime, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class MetricConsensusGenomeNumericalColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('reference_genome_length', 'percent_genome_called', 'percent_identity', 'gc_percent', 'total_reads', 'mapped_reads', 'ref_snps', 'n_actg', 'n_missing', 'n_ambiguous', 'coverage_depth', 'coverage_breadth', 'coverage_bin_size', 'coverage_total_length', 'owner_user_id', 'collection_id')
    reference_genome_length = sgqlc.types.Field(Float, graphql_name='referenceGenomeLength')
    percent_genome_called = sgqlc.types.Field(Float, graphql_name='percentGenomeCalled')
    percent_identity = sgqlc.types.Field(Float, graphql_name='percentIdentity')
    gc_percent = sgqlc.types.Field(Float, graphql_name='gcPercent')
    total_reads = sgqlc.types.Field(Int, graphql_name='totalReads')
    mapped_reads = sgqlc.types.Field(Int, graphql_name='mappedReads')
    ref_snps = sgqlc.types.Field(Int, graphql_name='refSnps')
    n_actg = sgqlc.types.Field(Int, graphql_name='nActg')
    n_missing = sgqlc.types.Field(Int, graphql_name='nMissing')
    n_ambiguous = sgqlc.types.Field(Int, graphql_name='nAmbiguous')
    coverage_depth = sgqlc.types.Field(Float, graphql_name='coverageDepth')
    coverage_breadth = sgqlc.types.Field(Float, graphql_name='coverageBreadth')
    coverage_bin_size = sgqlc.types.Field(Float, graphql_name='coverageBinSize')
    coverage_total_length = sgqlc.types.Field(Int, graphql_name='coverageTotalLength')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class MultipartUploadCredentials(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('protocol', 'namespace', 'path', 'access_key_id', 'secret_access_key', 'session_token', 'expiration')
    protocol = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='protocol')
    namespace = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='namespace')
    path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='path')
    access_key_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='accessKeyId')
    secret_access_key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='secretAccessKey')
    session_token = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='sessionToken')
    expiration = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='expiration')


class MultipartUploadResponse(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('credentials', 'file')
    credentials = sgqlc.types.Field(sgqlc.types.non_null(MultipartUploadCredentials), graphql_name='credentials')
    file = sgqlc.types.Field(sgqlc.types.non_null(File), graphql_name='file')


class Mutation(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('create_file', 'upload_file', 'mark_upload_complete', 'concatenate_files', 'create_sample', 'update_sample', 'delete_sample', 'create_sequencing_read', 'update_sequencing_read', 'delete_sequencing_read', 'create_genomic_range', 'delete_genomic_range', 'create_reference_genome', 'update_reference_genome', 'delete_reference_genome', 'create_accession', 'update_accession', 'delete_accession', 'create_host_organism', 'update_host_organism', 'delete_host_organism', 'create_metadatum', 'update_metadatum', 'delete_metadatum', 'create_consensus_genome', 'delete_consensus_genome', 'create_metric_consensus_genome', 'delete_metric_consensus_genome', 'create_taxon', 'update_taxon', 'delete_taxon', 'create_upstream_database', 'update_upstream_database', 'delete_upstream_database', 'create_index_file', 'update_index_file', 'delete_index_file', 'create_phylogenetic_tree', 'update_phylogenetic_tree', 'delete_phylogenetic_tree', 'create_bulk_download', 'delete_bulk_download')
    create_file = sgqlc.types.Field(sgqlc.types.non_null(File), graphql_name='createFile', args=sgqlc.types.ArgDict((
        ('entity_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='entityId', default=None)),
        ('entity_field_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='entityFieldName', default=None)),
        ('file', sgqlc.types.Arg(sgqlc.types.non_null(FileCreate), graphql_name='file', default=None)),
))
    )
    upload_file = sgqlc.types.Field(sgqlc.types.non_null(MultipartUploadResponse), graphql_name='uploadFile', args=sgqlc.types.ArgDict((
        ('entity_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='entityId', default=None)),
        ('entity_field_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='entityFieldName', default=None)),
        ('file', sgqlc.types.Arg(sgqlc.types.non_null(FileUpload), graphql_name='file', default=None)),
        ('expiration', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='expiration', default=3600)),
))
    )
    mark_upload_complete = sgqlc.types.Field(sgqlc.types.non_null(File), graphql_name='markUploadComplete', args=sgqlc.types.ArgDict((
        ('file_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='fileId', default=None)),
))
    )
    concatenate_files = sgqlc.types.Field(sgqlc.types.non_null('SignedURL'), graphql_name='concatenateFiles', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(UUID))), graphql_name='ids', default=None)),
))
    )
    create_sample = sgqlc.types.Field(sgqlc.types.non_null('Sample'), graphql_name='createSample', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(SampleCreateInput), graphql_name='input', default=None)),
))
    )
    update_sample = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Sample'))), graphql_name='updateSample', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(SampleUpdateInput), graphql_name='input', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(SampleWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    delete_sample = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Sample'))), graphql_name='deleteSample', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(SampleWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    create_sequencing_read = sgqlc.types.Field(sgqlc.types.non_null('SequencingRead'), graphql_name='createSequencingRead', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(SequencingReadCreateInput), graphql_name='input', default=None)),
))
    )
    update_sequencing_read = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SequencingRead'))), graphql_name='updateSequencingRead', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(SequencingReadUpdateInput), graphql_name='input', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(SequencingReadWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    delete_sequencing_read = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SequencingRead'))), graphql_name='deleteSequencingRead', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(SequencingReadWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    create_genomic_range = sgqlc.types.Field(sgqlc.types.non_null('GenomicRange'), graphql_name='createGenomicRange', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(GenomicRangeCreateInput), graphql_name='input', default=None)),
))
    )
    delete_genomic_range = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('GenomicRange'))), graphql_name='deleteGenomicRange', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(GenomicRangeWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    create_reference_genome = sgqlc.types.Field(sgqlc.types.non_null('ReferenceGenome'), graphql_name='createReferenceGenome', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(ReferenceGenomeCreateInput), graphql_name='input', default=None)),
))
    )
    update_reference_genome = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ReferenceGenome'))), graphql_name='updateReferenceGenome', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(ReferenceGenomeUpdateInput), graphql_name='input', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(ReferenceGenomeWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    delete_reference_genome = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ReferenceGenome'))), graphql_name='deleteReferenceGenome', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(ReferenceGenomeWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    create_accession = sgqlc.types.Field(sgqlc.types.non_null('Accession'), graphql_name='createAccession', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(AccessionCreateInput), graphql_name='input', default=None)),
))
    )
    update_accession = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Accession'))), graphql_name='updateAccession', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(AccessionUpdateInput), graphql_name='input', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(AccessionWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    delete_accession = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Accession'))), graphql_name='deleteAccession', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(AccessionWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    create_host_organism = sgqlc.types.Field(sgqlc.types.non_null('HostOrganism'), graphql_name='createHostOrganism', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(HostOrganismCreateInput), graphql_name='input', default=None)),
))
    )
    update_host_organism = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('HostOrganism'))), graphql_name='updateHostOrganism', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(HostOrganismUpdateInput), graphql_name='input', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(HostOrganismWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    delete_host_organism = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('HostOrganism'))), graphql_name='deleteHostOrganism', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(HostOrganismWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    create_metadatum = sgqlc.types.Field(sgqlc.types.non_null('Metadatum'), graphql_name='createMetadatum', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(MetadatumCreateInput), graphql_name='input', default=None)),
))
    )
    update_metadatum = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Metadatum'))), graphql_name='updateMetadatum', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(MetadatumUpdateInput), graphql_name='input', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(MetadatumWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    delete_metadatum = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Metadatum'))), graphql_name='deleteMetadatum', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(MetadatumWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    create_consensus_genome = sgqlc.types.Field(sgqlc.types.non_null('ConsensusGenome'), graphql_name='createConsensusGenome', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(ConsensusGenomeCreateInput), graphql_name='input', default=None)),
))
    )
    delete_consensus_genome = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ConsensusGenome'))), graphql_name='deleteConsensusGenome', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(ConsensusGenomeWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    create_metric_consensus_genome = sgqlc.types.Field(sgqlc.types.non_null('MetricConsensusGenome'), graphql_name='createMetricConsensusGenome', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(MetricConsensusGenomeCreateInput), graphql_name='input', default=None)),
))
    )
    delete_metric_consensus_genome = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MetricConsensusGenome'))), graphql_name='deleteMetricConsensusGenome', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(MetricConsensusGenomeWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    create_taxon = sgqlc.types.Field(sgqlc.types.non_null('Taxon'), graphql_name='createTaxon', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(TaxonCreateInput), graphql_name='input', default=None)),
))
    )
    update_taxon = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Taxon'))), graphql_name='updateTaxon', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(TaxonUpdateInput), graphql_name='input', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(TaxonWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    delete_taxon = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Taxon'))), graphql_name='deleteTaxon', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(TaxonWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    create_upstream_database = sgqlc.types.Field(sgqlc.types.non_null('UpstreamDatabase'), graphql_name='createUpstreamDatabase', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpstreamDatabaseCreateInput), graphql_name='input', default=None)),
))
    )
    update_upstream_database = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('UpstreamDatabase'))), graphql_name='updateUpstreamDatabase', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpstreamDatabaseUpdateInput), graphql_name='input', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(UpstreamDatabaseWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    delete_upstream_database = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('UpstreamDatabase'))), graphql_name='deleteUpstreamDatabase', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(UpstreamDatabaseWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    create_index_file = sgqlc.types.Field(sgqlc.types.non_null('IndexFile'), graphql_name='createIndexFile', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(IndexFileCreateInput), graphql_name='input', default=None)),
))
    )
    update_index_file = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('IndexFile'))), graphql_name='updateIndexFile', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(IndexFileUpdateInput), graphql_name='input', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(IndexFileWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    delete_index_file = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('IndexFile'))), graphql_name='deleteIndexFile', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(IndexFileWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    create_phylogenetic_tree = sgqlc.types.Field(sgqlc.types.non_null('PhylogeneticTree'), graphql_name='createPhylogeneticTree', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(PhylogeneticTreeCreateInput), graphql_name='input', default=None)),
))
    )
    update_phylogenetic_tree = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('PhylogeneticTree'))), graphql_name='updatePhylogeneticTree', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(PhylogeneticTreeUpdateInput), graphql_name='input', default=None)),
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(PhylogeneticTreeWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    delete_phylogenetic_tree = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('PhylogeneticTree'))), graphql_name='deletePhylogeneticTree', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(PhylogeneticTreeWhereClauseMutations), graphql_name='where', default=None)),
))
    )
    create_bulk_download = sgqlc.types.Field(sgqlc.types.non_null('BulkDownload'), graphql_name='createBulkDownload', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(BulkDownloadCreateInput), graphql_name='input', default=None)),
))
    )
    delete_bulk_download = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('BulkDownload'))), graphql_name='deleteBulkDownload', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(sgqlc.types.non_null(BulkDownloadWhereClauseMutations), graphql_name='where', default=None)),
))
    )


class PageInfo(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('has_next_page', 'has_previous_page', 'start_cursor', 'end_cursor')
    has_next_page = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hasNextPage')
    has_previous_page = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hasPreviousPage')
    start_cursor = sgqlc.types.Field(String, graphql_name='startCursor')
    end_cursor = sgqlc.types.Field(String, graphql_name='endCursor')


class PhylogeneticTreeAggregate(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('aggregate',)
    aggregate = sgqlc.types.Field('PhylogeneticTreeAggregateFunctions', graphql_name='aggregate')


class PhylogeneticTreeAggregateFunctions(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('sum', 'avg', 'min', 'max', 'stddev', 'variance', 'count')
    sum = sgqlc.types.Field('PhylogeneticTreeNumericalColumns', graphql_name='sum')
    avg = sgqlc.types.Field('PhylogeneticTreeNumericalColumns', graphql_name='avg')
    min = sgqlc.types.Field('PhylogeneticTreeMinMaxColumns', graphql_name='min')
    max = sgqlc.types.Field('PhylogeneticTreeMinMaxColumns', graphql_name='max')
    stddev = sgqlc.types.Field('PhylogeneticTreeNumericalColumns', graphql_name='stddev')
    variance = sgqlc.types.Field('PhylogeneticTreeNumericalColumns', graphql_name='variance')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=False)),
        ('columns', sgqlc.types.Arg(PhylogeneticTreeCountColumns, graphql_name='columns', default=None)),
))
    )


class PhylogeneticTreeMinMaxColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(DateTime, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class PhylogeneticTreeNumericalColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('owner_user_id', 'collection_id')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class Query(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('node', 'nodes', 'files', 'samples', 'sequencing_reads', 'genomic_ranges', 'reference_genomes', 'accessions', 'host_organisms', 'metadatas', 'consensus_genomes', 'metrics_consensus_genomes', 'taxa', 'upstream_databases', 'index_files', 'phylogenetic_trees', 'bulk_downloads', 'samples_aggregate', 'sequencing_reads_aggregate', 'genomic_ranges_aggregate', 'reference_genomes_aggregate', 'accessions_aggregate', 'host_organisms_aggregate', 'metadatas_aggregate', 'consensus_genomes_aggregate', 'metrics_consensus_genomes_aggregate', 'taxa_aggregate', 'upstream_databases_aggregate', 'index_files_aggregate', 'phylogenetic_trees_aggregate', 'bulk_downloads_aggregate')
    node = sgqlc.types.Field(sgqlc.types.non_null(Node), graphql_name='node', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(GlobalID), graphql_name='id', default=None)),
))
    )
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Node))), graphql_name='nodes', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(GlobalID))), graphql_name='ids', default=None)),
))
    )
    files = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(File))), graphql_name='files', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(FileWhereClause, graphql_name='where', default=None)),
))
    )
    samples = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Sample'))), graphql_name='samples', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(SampleWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(SampleOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    sequencing_reads = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SequencingRead'))), graphql_name='sequencingReads', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(SequencingReadWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(SequencingReadOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    genomic_ranges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('GenomicRange'))), graphql_name='genomicRanges', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(GenomicRangeWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(GenomicRangeOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    reference_genomes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ReferenceGenome'))), graphql_name='referenceGenomes', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(ReferenceGenomeWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ReferenceGenomeOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    accessions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Accession'))), graphql_name='accessions', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(AccessionWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(AccessionOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    host_organisms = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('HostOrganism'))), graphql_name='hostOrganisms', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(HostOrganismWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(HostOrganismOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    metadatas = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Metadatum'))), graphql_name='metadatas', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(MetadatumWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(MetadatumOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    consensus_genomes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ConsensusGenome'))), graphql_name='consensusGenomes', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(ConsensusGenomeWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ConsensusGenomeOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    metrics_consensus_genomes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MetricConsensusGenome'))), graphql_name='metricsConsensusGenomes', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(MetricConsensusGenomeWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(MetricConsensusGenomeOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    taxa = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Taxon'))), graphql_name='taxa', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(TaxonWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(TaxonOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    upstream_databases = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('UpstreamDatabase'))), graphql_name='upstreamDatabases', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(UpstreamDatabaseWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(UpstreamDatabaseOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    index_files = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('IndexFile'))), graphql_name='indexFiles', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(IndexFileWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(IndexFileOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    phylogenetic_trees = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('PhylogeneticTree'))), graphql_name='phylogeneticTrees', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(PhylogeneticTreeWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(PhylogeneticTreeOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    bulk_downloads = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('BulkDownload'))), graphql_name='bulkDownloads', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(BulkDownloadWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(BulkDownloadOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    samples_aggregate = sgqlc.types.Field(sgqlc.types.non_null('SampleAggregate'), graphql_name='samplesAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(SampleWhereClause, graphql_name='where', default=None)),
))
    )
    sequencing_reads_aggregate = sgqlc.types.Field(sgqlc.types.non_null('SequencingReadAggregate'), graphql_name='sequencingReadsAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(SequencingReadWhereClause, graphql_name='where', default=None)),
))
    )
    genomic_ranges_aggregate = sgqlc.types.Field(sgqlc.types.non_null(GenomicRangeAggregate), graphql_name='genomicRangesAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(GenomicRangeWhereClause, graphql_name='where', default=None)),
))
    )
    reference_genomes_aggregate = sgqlc.types.Field(sgqlc.types.non_null('ReferenceGenomeAggregate'), graphql_name='referenceGenomesAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(ReferenceGenomeWhereClause, graphql_name='where', default=None)),
))
    )
    accessions_aggregate = sgqlc.types.Field(sgqlc.types.non_null(AccessionAggregate), graphql_name='accessionsAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(AccessionWhereClause, graphql_name='where', default=None)),
))
    )
    host_organisms_aggregate = sgqlc.types.Field(sgqlc.types.non_null(HostOrganismAggregate), graphql_name='hostOrganismsAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(HostOrganismWhereClause, graphql_name='where', default=None)),
))
    )
    metadatas_aggregate = sgqlc.types.Field(sgqlc.types.non_null(MetadatumAggregate), graphql_name='metadatasAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(MetadatumWhereClause, graphql_name='where', default=None)),
))
    )
    consensus_genomes_aggregate = sgqlc.types.Field(sgqlc.types.non_null(ConsensusGenomeAggregate), graphql_name='consensusGenomesAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(ConsensusGenomeWhereClause, graphql_name='where', default=None)),
))
    )
    metrics_consensus_genomes_aggregate = sgqlc.types.Field(sgqlc.types.non_null(MetricConsensusGenomeAggregate), graphql_name='metricsConsensusGenomesAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(MetricConsensusGenomeWhereClause, graphql_name='where', default=None)),
))
    )
    taxa_aggregate = sgqlc.types.Field(sgqlc.types.non_null('TaxonAggregate'), graphql_name='taxaAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(TaxonWhereClause, graphql_name='where', default=None)),
))
    )
    upstream_databases_aggregate = sgqlc.types.Field(sgqlc.types.non_null('UpstreamDatabaseAggregate'), graphql_name='upstreamDatabasesAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(UpstreamDatabaseWhereClause, graphql_name='where', default=None)),
))
    )
    index_files_aggregate = sgqlc.types.Field(sgqlc.types.non_null(IndexFileAggregate), graphql_name='indexFilesAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(IndexFileWhereClause, graphql_name='where', default=None)),
))
    )
    phylogenetic_trees_aggregate = sgqlc.types.Field(sgqlc.types.non_null(PhylogeneticTreeAggregate), graphql_name='phylogeneticTreesAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(PhylogeneticTreeWhereClause, graphql_name='where', default=None)),
))
    )
    bulk_downloads_aggregate = sgqlc.types.Field(sgqlc.types.non_null(BulkDownloadAggregate), graphql_name='bulkDownloadsAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(BulkDownloadWhereClause, graphql_name='where', default=None)),
))
    )


class ReferenceGenomeAggregate(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('aggregate',)
    aggregate = sgqlc.types.Field('ReferenceGenomeAggregateFunctions', graphql_name='aggregate')


class ReferenceGenomeAggregateFunctions(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('sum', 'avg', 'min', 'max', 'stddev', 'variance', 'count')
    sum = sgqlc.types.Field('ReferenceGenomeNumericalColumns', graphql_name='sum')
    avg = sgqlc.types.Field('ReferenceGenomeNumericalColumns', graphql_name='avg')
    min = sgqlc.types.Field('ReferenceGenomeMinMaxColumns', graphql_name='min')
    max = sgqlc.types.Field('ReferenceGenomeMinMaxColumns', graphql_name='max')
    stddev = sgqlc.types.Field('ReferenceGenomeNumericalColumns', graphql_name='stddev')
    variance = sgqlc.types.Field('ReferenceGenomeNumericalColumns', graphql_name='variance')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=False)),
        ('columns', sgqlc.types.Arg(ReferenceGenomeCountColumns, graphql_name='columns', default=None)),
))
    )


class ReferenceGenomeMinMaxColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('name', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    name = sgqlc.types.Field(String, graphql_name='name')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(DateTime, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class ReferenceGenomeNumericalColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('owner_user_id', 'collection_id')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class SampleAggregate(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('aggregate',)
    aggregate = sgqlc.types.Field('SampleAggregateFunctions', graphql_name='aggregate')


class SampleAggregateFunctions(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('sum', 'avg', 'min', 'max', 'stddev', 'variance', 'count')
    sum = sgqlc.types.Field('SampleNumericalColumns', graphql_name='sum')
    avg = sgqlc.types.Field('SampleNumericalColumns', graphql_name='avg')
    min = sgqlc.types.Field('SampleMinMaxColumns', graphql_name='min')
    max = sgqlc.types.Field('SampleMinMaxColumns', graphql_name='max')
    stddev = sgqlc.types.Field('SampleNumericalColumns', graphql_name='stddev')
    variance = sgqlc.types.Field('SampleNumericalColumns', graphql_name='variance')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=False)),
        ('columns', sgqlc.types.Arg(SampleCountColumns, graphql_name='columns', default=None)),
))
    )


class SampleConnection(sgqlc.types.relay.Connection):
    __schema__ = entities_schema
    __field_names__ = ('page_info', 'edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SampleEdge'))), graphql_name='edges')


class SampleEdge(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Sample'), graphql_name='node')


class SampleMinMaxColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('rails_sample_id', 'name', 'sample_type', 'collection_date', 'collection_location', 'notes', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    rails_sample_id = sgqlc.types.Field(Int, graphql_name='railsSampleId')
    name = sgqlc.types.Field(String, graphql_name='name')
    sample_type = sgqlc.types.Field(String, graphql_name='sampleType')
    collection_date = sgqlc.types.Field(DateTime, graphql_name='collectionDate')
    collection_location = sgqlc.types.Field(String, graphql_name='collectionLocation')
    notes = sgqlc.types.Field(String, graphql_name='notes')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(DateTime, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class SampleNumericalColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('rails_sample_id', 'owner_user_id', 'collection_id')
    rails_sample_id = sgqlc.types.Field(Int, graphql_name='railsSampleId')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class SequencingReadAggregate(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('aggregate',)
    aggregate = sgqlc.types.Field('SequencingReadAggregateFunctions', graphql_name='aggregate')


class SequencingReadAggregateFunctions(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('sum', 'avg', 'min', 'max', 'stddev', 'variance', 'count')
    sum = sgqlc.types.Field('SequencingReadNumericalColumns', graphql_name='sum')
    avg = sgqlc.types.Field('SequencingReadNumericalColumns', graphql_name='avg')
    min = sgqlc.types.Field('SequencingReadMinMaxColumns', graphql_name='min')
    max = sgqlc.types.Field('SequencingReadMinMaxColumns', graphql_name='max')
    stddev = sgqlc.types.Field('SequencingReadNumericalColumns', graphql_name='stddev')
    variance = sgqlc.types.Field('SequencingReadNumericalColumns', graphql_name='variance')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=False)),
        ('columns', sgqlc.types.Arg(SequencingReadCountColumns, graphql_name='columns', default=None)),
))
    )


class SequencingReadConnection(sgqlc.types.relay.Connection):
    __schema__ = entities_schema
    __field_names__ = ('page_info', 'edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SequencingReadEdge'))), graphql_name='edges')


class SequencingReadEdge(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('SequencingRead'), graphql_name='node')


class SequencingReadMinMaxColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('medaka_model', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    medaka_model = sgqlc.types.Field(String, graphql_name='medakaModel')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(DateTime, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class SequencingReadNumericalColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('owner_user_id', 'collection_id')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class SignedURL(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('url', 'protocol', 'method', 'expiration', 'fields')
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='url')
    protocol = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='protocol')
    method = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='method')
    expiration = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='expiration')
    fields = sgqlc.types.Field(JSON, graphql_name='fields')


class TaxonAggregate(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('aggregate',)
    aggregate = sgqlc.types.Field('TaxonAggregateFunctions', graphql_name='aggregate')


class TaxonAggregateFunctions(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('sum', 'avg', 'min', 'max', 'stddev', 'variance', 'count')
    sum = sgqlc.types.Field('TaxonNumericalColumns', graphql_name='sum')
    avg = sgqlc.types.Field('TaxonNumericalColumns', graphql_name='avg')
    min = sgqlc.types.Field('TaxonMinMaxColumns', graphql_name='min')
    max = sgqlc.types.Field('TaxonMinMaxColumns', graphql_name='max')
    stddev = sgqlc.types.Field('TaxonNumericalColumns', graphql_name='stddev')
    variance = sgqlc.types.Field('TaxonNumericalColumns', graphql_name='variance')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=False)),
        ('columns', sgqlc.types.Arg(TaxonCountColumns, graphql_name='columns', default=None)),
))
    )


class TaxonConnection(sgqlc.types.relay.Connection):
    __schema__ = entities_schema
    __field_names__ = ('page_info', 'edges')
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name='pageInfo')
    edges = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('TaxonEdge'))), graphql_name='edges')


class TaxonEdge(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('cursor', 'node')
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cursor')
    node = sgqlc.types.Field(sgqlc.types.non_null('Taxon'), graphql_name='node')


class TaxonMinMaxColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('wikipedia_id', 'description', 'common_name', 'name', 'upstream_database_identifier', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    wikipedia_id = sgqlc.types.Field(String, graphql_name='wikipediaId')
    description = sgqlc.types.Field(String, graphql_name='description')
    common_name = sgqlc.types.Field(String, graphql_name='commonName')
    name = sgqlc.types.Field(String, graphql_name='name')
    upstream_database_identifier = sgqlc.types.Field(String, graphql_name='upstreamDatabaseIdentifier')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(DateTime, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class TaxonNumericalColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('owner_user_id', 'collection_id')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class UpstreamDatabaseAggregate(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('aggregate',)
    aggregate = sgqlc.types.Field('UpstreamDatabaseAggregateFunctions', graphql_name='aggregate')


class UpstreamDatabaseAggregateFunctions(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('sum', 'avg', 'min', 'max', 'stddev', 'variance', 'count')
    sum = sgqlc.types.Field('UpstreamDatabaseNumericalColumns', graphql_name='sum')
    avg = sgqlc.types.Field('UpstreamDatabaseNumericalColumns', graphql_name='avg')
    min = sgqlc.types.Field('UpstreamDatabaseMinMaxColumns', graphql_name='min')
    max = sgqlc.types.Field('UpstreamDatabaseMinMaxColumns', graphql_name='max')
    stddev = sgqlc.types.Field('UpstreamDatabaseNumericalColumns', graphql_name='stddev')
    variance = sgqlc.types.Field('UpstreamDatabaseNumericalColumns', graphql_name='variance')
    count = sgqlc.types.Field(Int, graphql_name='count', args=sgqlc.types.ArgDict((
        ('distinct', sgqlc.types.Arg(Boolean, graphql_name='distinct', default=False)),
        ('columns', sgqlc.types.Arg(UpstreamDatabaseCountColumns, graphql_name='columns', default=None)),
))
    )


class UpstreamDatabaseMinMaxColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('name', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    name = sgqlc.types.Field(String, graphql_name='name')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(DateTime, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class UpstreamDatabaseNumericalColumns(sgqlc.types.Type):
    __schema__ = entities_schema
    __field_names__ = ('owner_user_id', 'collection_id')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')


class Accession(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = entities_schema
    __field_names__ = ('id', 'accession_id', 'accession_name', 'upstream_database', 'consensus_genomes', 'consensus_genomes_aggregate', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    accession_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='accessionId')
    accession_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='accessionName')
    upstream_database = sgqlc.types.Field('UpstreamDatabase', graphql_name='upstreamDatabase', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(UpstreamDatabaseWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(UpstreamDatabaseOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    consensus_genomes = sgqlc.types.Field(sgqlc.types.non_null(ConsensusGenomeConnection), graphql_name='consensusGenomes', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(ConsensusGenomeWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ConsensusGenomeOrderByClause)), graphql_name='orderBy', default=())),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    consensus_genomes_aggregate = sgqlc.types.Field(ConsensusGenomeAggregate, graphql_name='consensusGenomesAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(ConsensusGenomeWhereClause, graphql_name='where', default=None)),
))
    )
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class BulkDownload(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = entities_schema
    __field_names__ = ('id', 'download_type', 'file_id', 'file', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    download_type = sgqlc.types.Field(sgqlc.types.non_null(BulkDownloadType), graphql_name='downloadType')
    file_id = sgqlc.types.Field(ID, graphql_name='fileId')
    file = sgqlc.types.Field(File, graphql_name='file', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(FileWhereClause, graphql_name='where', default=None)),
))
    )
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class ConsensusGenome(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = entities_schema
    __field_names__ = ('id', 'taxon', 'sequence_read', 'reference_genome', 'accession', 'sequence_id', 'sequence', 'metrics', 'intermediate_outputs_id', 'intermediate_outputs', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    taxon = sgqlc.types.Field('Taxon', graphql_name='taxon', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(TaxonWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(TaxonOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    sequence_read = sgqlc.types.Field('SequencingRead', graphql_name='sequenceRead', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(SequencingReadWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(SequencingReadOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    reference_genome = sgqlc.types.Field('ReferenceGenome', graphql_name='referenceGenome', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(ReferenceGenomeWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ReferenceGenomeOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    accession = sgqlc.types.Field(Accession, graphql_name='accession', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(AccessionWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(AccessionOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    sequence_id = sgqlc.types.Field(ID, graphql_name='sequenceId')
    sequence = sgqlc.types.Field(File, graphql_name='sequence', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(FileWhereClause, graphql_name='where', default=None)),
))
    )
    metrics = sgqlc.types.Field('MetricConsensusGenome', graphql_name='metrics', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(MetricConsensusGenomeWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(MetricConsensusGenomeOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    intermediate_outputs_id = sgqlc.types.Field(ID, graphql_name='intermediateOutputsId')
    intermediate_outputs = sgqlc.types.Field(File, graphql_name='intermediateOutputs', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(FileWhereClause, graphql_name='where', default=None)),
))
    )
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class GenomicRange(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = entities_schema
    __field_names__ = ('id', 'file_id', 'file', 'sequencing_reads', 'sequencing_reads_aggregate', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    file_id = sgqlc.types.Field(ID, graphql_name='fileId')
    file = sgqlc.types.Field(File, graphql_name='file', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(FileWhereClause, graphql_name='where', default=None)),
))
    )
    sequencing_reads = sgqlc.types.Field(sgqlc.types.non_null(SequencingReadConnection), graphql_name='sequencingReads', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(SequencingReadWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(SequencingReadOrderByClause)), graphql_name='orderBy', default=())),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    sequencing_reads_aggregate = sgqlc.types.Field(SequencingReadAggregate, graphql_name='sequencingReadsAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(SequencingReadWhereClause, graphql_name='where', default=None)),
))
    )
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class HostOrganism(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = entities_schema
    __field_names__ = ('id', 'name', 'version', 'category', 'is_deuterostome', 'indexes', 'indexes_aggregate', 'sequence_id', 'sequence', 'samples', 'samples_aggregate', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    version = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='version')
    category = sgqlc.types.Field(sgqlc.types.non_null(HostOrganismCategory), graphql_name='category')
    is_deuterostome = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isDeuterostome')
    indexes = sgqlc.types.Field(sgqlc.types.non_null(IndexFileConnection), graphql_name='indexes', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(IndexFileWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(IndexFileOrderByClause)), graphql_name='orderBy', default=())),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    indexes_aggregate = sgqlc.types.Field(IndexFileAggregate, graphql_name='indexesAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(IndexFileWhereClause, graphql_name='where', default=None)),
))
    )
    sequence_id = sgqlc.types.Field(ID, graphql_name='sequenceId')
    sequence = sgqlc.types.Field(File, graphql_name='sequence', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(FileWhereClause, graphql_name='where', default=None)),
))
    )
    samples = sgqlc.types.Field(sgqlc.types.non_null(SampleConnection), graphql_name='samples', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(SampleWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(SampleOrderByClause)), graphql_name='orderBy', default=())),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    samples_aggregate = sgqlc.types.Field(SampleAggregate, graphql_name='samplesAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(SampleWhereClause, graphql_name='where', default=None)),
))
    )
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class IndexFile(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = entities_schema
    __field_names__ = ('id', 'name', 'version', 'file_id', 'file', 'upstream_database', 'host_organism', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(IndexTypes), graphql_name='name')
    version = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='version')
    file_id = sgqlc.types.Field(ID, graphql_name='fileId')
    file = sgqlc.types.Field(File, graphql_name='file', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(FileWhereClause, graphql_name='where', default=None)),
))
    )
    upstream_database = sgqlc.types.Field('UpstreamDatabase', graphql_name='upstreamDatabase', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(UpstreamDatabaseWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(UpstreamDatabaseOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    host_organism = sgqlc.types.Field(HostOrganism, graphql_name='hostOrganism', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(HostOrganismWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(HostOrganismOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class Metadatum(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = entities_schema
    __field_names__ = ('id', 'sample', 'field_name', 'value', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    sample = sgqlc.types.Field('Sample', graphql_name='sample', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(SampleWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(SampleOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    field_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='fieldName')
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='value')
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class MetricConsensusGenome(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = entities_schema
    __field_names__ = ('id', 'consensus_genome', 'reference_genome_length', 'percent_genome_called', 'percent_identity', 'gc_percent', 'total_reads', 'mapped_reads', 'ref_snps', 'n_actg', 'n_missing', 'n_ambiguous', 'coverage_depth', 'coverage_breadth', 'coverage_bin_size', 'coverage_total_length', 'coverage_viz', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    consensus_genome = sgqlc.types.Field(ConsensusGenome, graphql_name='consensusGenome', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(ConsensusGenomeWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ConsensusGenomeOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    reference_genome_length = sgqlc.types.Field(Float, graphql_name='referenceGenomeLength')
    percent_genome_called = sgqlc.types.Field(Float, graphql_name='percentGenomeCalled')
    percent_identity = sgqlc.types.Field(Float, graphql_name='percentIdentity')
    gc_percent = sgqlc.types.Field(Float, graphql_name='gcPercent')
    total_reads = sgqlc.types.Field(Int, graphql_name='totalReads')
    mapped_reads = sgqlc.types.Field(Int, graphql_name='mappedReads')
    ref_snps = sgqlc.types.Field(Int, graphql_name='refSnps')
    n_actg = sgqlc.types.Field(Int, graphql_name='nActg')
    n_missing = sgqlc.types.Field(Int, graphql_name='nMissing')
    n_ambiguous = sgqlc.types.Field(Int, graphql_name='nAmbiguous')
    coverage_depth = sgqlc.types.Field(Float, graphql_name='coverageDepth')
    coverage_breadth = sgqlc.types.Field(Float, graphql_name='coverageBreadth')
    coverage_bin_size = sgqlc.types.Field(Float, graphql_name='coverageBinSize')
    coverage_total_length = sgqlc.types.Field(Int, graphql_name='coverageTotalLength')
    coverage_viz = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Int)))), graphql_name='coverageViz')
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class PhylogeneticTree(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = entities_schema
    __field_names__ = ('id', 'tree_id', 'tree', 'format', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    tree_id = sgqlc.types.Field(ID, graphql_name='treeId')
    tree = sgqlc.types.Field(File, graphql_name='tree', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(FileWhereClause, graphql_name='where', default=None)),
))
    )
    format = sgqlc.types.Field(sgqlc.types.non_null(PhylogeneticTreeFormat), graphql_name='format')
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class ReferenceGenome(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = entities_schema
    __field_names__ = ('id', 'file_id', 'file', 'name', 'consensus_genomes', 'consensus_genomes_aggregate', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    file_id = sgqlc.types.Field(ID, graphql_name='fileId')
    file = sgqlc.types.Field(File, graphql_name='file', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(FileWhereClause, graphql_name='where', default=None)),
))
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    consensus_genomes = sgqlc.types.Field(sgqlc.types.non_null(ConsensusGenomeConnection), graphql_name='consensusGenomes', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(ConsensusGenomeWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ConsensusGenomeOrderByClause)), graphql_name='orderBy', default=())),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    consensus_genomes_aggregate = sgqlc.types.Field(ConsensusGenomeAggregate, graphql_name='consensusGenomesAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(ConsensusGenomeWhereClause, graphql_name='where', default=None)),
))
    )
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class Sample(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = entities_schema
    __field_names__ = ('id', 'rails_sample_id', 'name', 'sample_type', 'water_control', 'collection_date', 'collection_location', 'notes', 'host_organism', 'sequencing_reads', 'sequencing_reads_aggregate', 'metadatas', 'metadatas_aggregate', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    id = sgqlc.types.Field(ID, graphql_name='id')
    rails_sample_id = sgqlc.types.Field(Int, graphql_name='railsSampleId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    sample_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='sampleType')
    water_control = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='waterControl')
    collection_date = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='collectionDate')
    collection_location = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='collectionLocation')
    notes = sgqlc.types.Field(String, graphql_name='notes')
    host_organism = sgqlc.types.Field(HostOrganism, graphql_name='hostOrganism', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(HostOrganismWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(HostOrganismOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    sequencing_reads = sgqlc.types.Field(sgqlc.types.non_null(SequencingReadConnection), graphql_name='sequencingReads', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(SequencingReadWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(SequencingReadOrderByClause)), graphql_name='orderBy', default=())),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    sequencing_reads_aggregate = sgqlc.types.Field(SequencingReadAggregate, graphql_name='sequencingReadsAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(SequencingReadWhereClause, graphql_name='where', default=None)),
))
    )
    metadatas = sgqlc.types.Field(sgqlc.types.non_null(MetadatumConnection), graphql_name='metadatas', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(MetadatumWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(MetadatumOrderByClause)), graphql_name='orderBy', default=())),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    metadatas_aggregate = sgqlc.types.Field(MetadatumAggregate, graphql_name='metadatasAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(MetadatumWhereClause, graphql_name='where', default=None)),
))
    )
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class SequencingRead(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = entities_schema
    __field_names__ = ('id', 'sample', 'protocol', 'r1_file_id', 'r1_file', 'r2_file_id', 'r2_file', 'technology', 'nucleic_acid', 'clearlabs_export', 'medaka_model', 'taxon', 'primer_file', 'consensus_genomes', 'consensus_genomes_aggregate', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    sample = sgqlc.types.Field(Sample, graphql_name='sample', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(SampleWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(SampleOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    protocol = sgqlc.types.Field(SequencingProtocol, graphql_name='protocol')
    r1_file_id = sgqlc.types.Field(ID, graphql_name='r1FileId')
    r1_file = sgqlc.types.Field(File, graphql_name='r1File', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(FileWhereClause, graphql_name='where', default=None)),
))
    )
    r2_file_id = sgqlc.types.Field(ID, graphql_name='r2FileId')
    r2_file = sgqlc.types.Field(File, graphql_name='r2File', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(FileWhereClause, graphql_name='where', default=None)),
))
    )
    technology = sgqlc.types.Field(sgqlc.types.non_null(SequencingTechnology), graphql_name='technology')
    nucleic_acid = sgqlc.types.Field(sgqlc.types.non_null(NucleicAcid), graphql_name='nucleicAcid')
    clearlabs_export = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='clearlabsExport')
    medaka_model = sgqlc.types.Field(String, graphql_name='medakaModel')
    taxon = sgqlc.types.Field('Taxon', graphql_name='taxon', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(TaxonWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(TaxonOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    primer_file = sgqlc.types.Field(GenomicRange, graphql_name='primerFile', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(GenomicRangeWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(GenomicRangeOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    consensus_genomes = sgqlc.types.Field(sgqlc.types.non_null(ConsensusGenomeConnection), graphql_name='consensusGenomes', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(ConsensusGenomeWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ConsensusGenomeOrderByClause)), graphql_name='orderBy', default=())),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    consensus_genomes_aggregate = sgqlc.types.Field(ConsensusGenomeAggregate, graphql_name='consensusGenomesAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(ConsensusGenomeWhereClause, graphql_name='where', default=None)),
))
    )
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class Taxon(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = entities_schema
    __field_names__ = ('id', 'wikipedia_id', 'description', 'common_name', 'name', 'is_phage', 'upstream_database', 'upstream_database_identifier', 'level', 'consensus_genomes', 'consensus_genomes_aggregate', 'sequencing_reads', 'sequencing_reads_aggregate', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    wikipedia_id = sgqlc.types.Field(String, graphql_name='wikipediaId')
    description = sgqlc.types.Field(String, graphql_name='description')
    common_name = sgqlc.types.Field(String, graphql_name='commonName')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    is_phage = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isPhage')
    upstream_database = sgqlc.types.Field('UpstreamDatabase', graphql_name='upstreamDatabase', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(UpstreamDatabaseWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(UpstreamDatabaseOrderByClause)), graphql_name='orderBy', default=())),
))
    )
    upstream_database_identifier = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='upstreamDatabaseIdentifier')
    level = sgqlc.types.Field(sgqlc.types.non_null(TaxonLevel), graphql_name='level')
    consensus_genomes = sgqlc.types.Field(sgqlc.types.non_null(ConsensusGenomeConnection), graphql_name='consensusGenomes', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(ConsensusGenomeWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(ConsensusGenomeOrderByClause)), graphql_name='orderBy', default=())),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    consensus_genomes_aggregate = sgqlc.types.Field(ConsensusGenomeAggregate, graphql_name='consensusGenomesAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(ConsensusGenomeWhereClause, graphql_name='where', default=None)),
))
    )
    sequencing_reads = sgqlc.types.Field(sgqlc.types.non_null(SequencingReadConnection), graphql_name='sequencingReads', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(SequencingReadWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(SequencingReadOrderByClause)), graphql_name='orderBy', default=())),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    sequencing_reads_aggregate = sgqlc.types.Field(SequencingReadAggregate, graphql_name='sequencingReadsAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(SequencingReadWhereClause, graphql_name='where', default=None)),
))
    )
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')


class UpstreamDatabase(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = entities_schema
    __field_names__ = ('id', 'name', 'taxa', 'taxa_aggregate', 'indexes', 'indexes_aggregate', 'accessions', 'accessions_aggregate', 'producing_run_id', 'owner_user_id', 'collection_id', 'created_at', 'updated_at', 'deleted_at')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    taxa = sgqlc.types.Field(sgqlc.types.non_null(TaxonConnection), graphql_name='taxa', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(TaxonWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(TaxonOrderByClause)), graphql_name='orderBy', default=())),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    taxa_aggregate = sgqlc.types.Field(TaxonAggregate, graphql_name='taxaAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(TaxonWhereClause, graphql_name='where', default=None)),
))
    )
    indexes = sgqlc.types.Field(sgqlc.types.non_null(IndexFileConnection), graphql_name='indexes', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(IndexFileWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(IndexFileOrderByClause)), graphql_name='orderBy', default=())),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    indexes_aggregate = sgqlc.types.Field(IndexFileAggregate, graphql_name='indexesAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(IndexFileWhereClause, graphql_name='where', default=None)),
))
    )
    accessions = sgqlc.types.Field(sgqlc.types.non_null(AccessionConnection), graphql_name='accessions', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(AccessionWhereClause, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(AccessionOrderByClause)), graphql_name='orderBy', default=())),
        ('before', sgqlc.types.Arg(String, graphql_name='before', default=None)),
        ('after', sgqlc.types.Arg(String, graphql_name='after', default=None)),
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('last', sgqlc.types.Arg(Int, graphql_name='last', default=None)),
))
    )
    accessions_aggregate = sgqlc.types.Field(AccessionAggregate, graphql_name='accessionsAggregate', args=sgqlc.types.ArgDict((
        ('where', sgqlc.types.Arg(AccessionWhereClause, graphql_name='where', default=None)),
))
    )
    producing_run_id = sgqlc.types.Field(ID, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    collection_id = sgqlc.types.Field(Int, graphql_name='collectionId')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(DateTime, graphql_name='updatedAt')
    deleted_at = sgqlc.types.Field(DateTime, graphql_name='deletedAt')



########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
entities_schema.query_type = Query
entities_schema.mutation_type = Mutation
entities_schema.subscription_type = None

