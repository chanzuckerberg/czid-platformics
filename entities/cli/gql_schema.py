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


class Mutation(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("create_sample", "create_sequencing_read")
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
                ("sample_id", sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name="sampleId", default=None)),
                (
                    "collection_id",
                    sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="collectionId", default=None),
                ),
            )
        ),
    )


class Query(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("samples", "sequencing_reads")
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


class Sample(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "type",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "entity_id",
        "name",
        "location",
        "sequencing_reads",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="id")
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="type")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    entity_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="entityId")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    location = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="location")
    sequencing_reads = sgqlc.types.Field(
        sgqlc.types.non_null("SequencingReadConnection"), graphql_name="sequencingReads"
    )


class SequencingRead(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "type",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "entity_id",
        "nucleotide",
        "sequence",
        "protocol",
        "sample_id",
        "sample",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="id")
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="type")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    entity_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="entityId")
    nucleotide = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="nucleotide")
    sequence = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="sequence")
    protocol = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="protocol")
    sample_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="sampleId")
    sample = sgqlc.types.Field(sgqlc.types.non_null(Sample), graphql_name="sample")


class SequencingReadConnection(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("edges",)
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("SequencingReadEdge"))), graphql_name="edges"
    )


class SequencingReadEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("node",)
    node = sgqlc.types.Field(sgqlc.types.non_null(SequencingRead), graphql_name="node")


########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
gql_schema.query_type = Query
gql_schema.mutation_type = Mutation
gql_schema.subscription_type = None
