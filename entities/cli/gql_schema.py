import sgqlc.types


gql_schema = sgqlc.types.Schema()


########################################################################
# Scalars and Enumerations
########################################################################
Boolean = sgqlc.types.Boolean

Int = sgqlc.types.Int

String = sgqlc.types.String


class UUID(sgqlc.types.Scalar):
    __schema__ = gql_schema


########################################################################
# Input Objects
########################################################################


########################################################################
# Output Objects and Interfaces
########################################################################
class EntityInterface(sgqlc.types.Interface):
    __schema__ = gql_schema
    __field_names__ = ("id", "type", "producing_run_id", "owner_user_id", "collection_id")
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="id")
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="type")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")


class ContigConnection(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("edges",)
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ContigEdge"))), graphql_name="edges"
    )


class ContigEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("node",)
    node = sgqlc.types.Field(sgqlc.types.non_null("Contig"), graphql_name="node")


class File(sgqlc.types.Type):
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
        "entity",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="id")
    entity_id = sgqlc.types.Field(UUID, graphql_name="entityId")
    entity_field_name = sgqlc.types.Field(String, graphql_name="entityFieldName")
    status = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="status")
    protocol = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="protocol")
    namespace = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="namespace")
    path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="path")
    file_format = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="fileFormat")
    compression_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="compressionType")
    size = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="size")
    entity = sgqlc.types.Field(EntityInterface, graphql_name="entity")


class Mutation(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("create_sample", "create_sequencing_read", "create_contig", "update_sample")
    create_sample = sgqlc.types.Field(
        sgqlc.types.non_null("Sample"),
        graphql_name="createSample",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("location", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="location", default=None)),
                (
                    "collection_id",
                    sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="collectionId", default=None),
                ),
            )
        ),
    )
    create_sequencing_read = sgqlc.types.Field(
        sgqlc.types.non_null("SequencingRead"),
        graphql_name="createSequencingRead",
        args=sgqlc.types.ArgDict(
            (
                ("nucleotide", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="nucleotide", default=None)),
                ("sequence", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="sequence", default=None)),
                ("protocol", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="protocol", default=None)),
                ("sequence_file_id", sgqlc.types.Arg(UUID, graphql_name="sequenceFileId", default=None)),
                ("sample_id", sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name="sampleId", default=None)),
                (
                    "collection_id",
                    sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="collectionId", default=None),
                ),
            )
        ),
    )
    create_contig = sgqlc.types.Field(
        sgqlc.types.non_null("Contig"),
        graphql_name="createContig",
        args=sgqlc.types.ArgDict(
            (
                ("sequence", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="sequence", default=None)),
                (
                    "sequencing_read_id",
                    sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name="sequencingReadId", default=None),
                ),
                (
                    "collection_id",
                    sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="collectionId", default=None),
                ),
            )
        ),
    )
    update_sample = sgqlc.types.Field(
        sgqlc.types.non_null("Sample"),
        graphql_name="updateSample",
        args=sgqlc.types.ArgDict(
            (
                ("entity_id", sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name="entityId", default=None)),
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("location", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="location", default=None)),
            )
        ),
    )


class Query(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("samples", "sequencing_reads", "contigs", "files")
    samples = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Sample"))),
        graphql_name="samples",
        args=sgqlc.types.ArgDict((("id", sgqlc.types.Arg(UUID, graphql_name="id", default=None)),)),
    )
    sequencing_reads = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("SequencingRead"))),
        graphql_name="sequencingReads",
        args=sgqlc.types.ArgDict((("id", sgqlc.types.Arg(UUID, graphql_name="id", default=None)),)),
    )
    contigs = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Contig"))),
        graphql_name="contigs",
        args=sgqlc.types.ArgDict((("id", sgqlc.types.Arg(UUID, graphql_name="id", default=None)),)),
    )
    files = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(File))),
        graphql_name="files",
        args=sgqlc.types.ArgDict((("id", sgqlc.types.Arg(UUID, graphql_name="id", default=None)),)),
    )


class SequencingReadConnection(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("edges",)
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("SequencingReadEdge"))), graphql_name="edges"
    )


class SequencingReadEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("node",)
    node = sgqlc.types.Field(sgqlc.types.non_null("SequencingRead"), graphql_name="node")


class Contig(sgqlc.types.Type, EntityInterface):
    __schema__ = gql_schema
    __field_names__ = ("entity_id", "sequence", "sequencing_read_id", "sequencing_read")
    entity_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="entityId")
    sequence = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="sequence")
    sequencing_read_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="sequencingReadId")
    sequencing_read = sgqlc.types.Field(sgqlc.types.non_null("SequencingRead"), graphql_name="sequencingRead")


class Sample(sgqlc.types.Type, EntityInterface):
    __schema__ = gql_schema
    __field_names__ = ("entity_id", "name", "location", "sequencing_reads")
    entity_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="entityId")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    location = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="location")
    sequencing_reads = sgqlc.types.Field(sgqlc.types.non_null(SequencingReadConnection), graphql_name="sequencingReads")


class SequencingRead(sgqlc.types.Type, EntityInterface):
    __schema__ = gql_schema
    __field_names__ = (
        "entity_id",
        "nucleotide",
        "sequence",
        "protocol",
        "sequence_file_id",
        "sample_id",
        "sequence_file",
        "sample",
        "contigs",
    )
    entity_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="entityId")
    nucleotide = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="nucleotide")
    sequence = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="sequence")
    protocol = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="protocol")
    sequence_file_id = sgqlc.types.Field(UUID, graphql_name="sequenceFileId")
    sample_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="sampleId")
    sequence_file = sgqlc.types.Field(File, graphql_name="sequenceFile")
    sample = sgqlc.types.Field(sgqlc.types.non_null(Sample), graphql_name="sample")
    contigs = sgqlc.types.Field(sgqlc.types.non_null(ContigConnection), graphql_name="contigs")


########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
gql_schema.query_type = Query
gql_schema.mutation_type = Mutation
gql_schema.subscription_type = None
