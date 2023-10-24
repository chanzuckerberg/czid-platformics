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


class SampleWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_runid",
        "owner_user_id",
        "collection_id",
        "name",
        "location",
        "sequencing_reads",
    )
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_runid = sgqlc.types.Field(IntComparators, graphql_name="producingRunid")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    name = sgqlc.types.Field("StrComparators", graphql_name="name")
    location = sgqlc.types.Field("StrComparators", graphql_name="location")
    sequencing_reads = sgqlc.types.Field("SequencingReadWhereClause", graphql_name="sequencingReads")


class SequencingReadWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id", "producing_runid", "owner_user_id", "collection_id", "sequence", "sample")
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_runid = sgqlc.types.Field(IntComparators, graphql_name="producingRunid")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    sequence = sgqlc.types.Field("StrComparators", graphql_name="sequence")
    sample = sgqlc.types.Field(SampleWhereClause, graphql_name="sample")


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


########################################################################
# Output Objects and Interfaces
########################################################################
class EntityInterface(sgqlc.types.Interface):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="id")


class Query(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("samples", "sequencing_reads")
    samples = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Sample"))),
        graphql_name="samples",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(SampleWhereClause, graphql_name="where", default=None)),)),
    )
    sequencing_reads = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("SequencingRead"))),
        graphql_name="sequencingReads",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(sgqlc.types.non_null(SequencingReadWhereClause), graphql_name="where", default={}),
                ),
            )
        ),
    )


class Sample(sgqlc.types.Type, EntityInterface):
    __schema__ = gql_schema
    __field_names__ = ("producing_runid", "owner_user_id", "collection_id", "name", "location", "sequencing_reads")
    producing_runid = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="producingRunid")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    location = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="location")
    sequencing_reads = sgqlc.types.Field(sgqlc.types.non_null("SequencingRead"), graphql_name="sequencingReads")


class SequencingRead(sgqlc.types.Type, EntityInterface):
    __schema__ = gql_schema
    __field_names__ = ("producing_runid", "owner_user_id", "collection_id", "sequence", "sample")
    producing_runid = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="producingRunid")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    sequence = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="sequence")
    sample = sgqlc.types.Field(sgqlc.types.non_null(Sample), graphql_name="sample")


########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
gql_schema.query_type = Query
gql_schema.mutation_type = None
gql_schema.subscription_type = None
