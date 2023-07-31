import sgqlc.types


gql_schema = sgqlc.types.Schema()



########################################################################
# Scalars and Enumerations
########################################################################
Boolean = sgqlc.types.Boolean

ID = sgqlc.types.ID

Int = sgqlc.types.Int

String = sgqlc.types.String


########################################################################
# Input Objects
########################################################################

########################################################################
# Output Objects and Interfaces
########################################################################
class Query(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ('get_sample', 'get_all_samples', 'get_sequencing_read', 'get_all_sequencing_reads')
    get_sample = sgqlc.types.Field(sgqlc.types.non_null('Sample'), graphql_name='getSample', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    get_all_samples = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Sample'))), graphql_name='getAllSamples')
    get_sequencing_read = sgqlc.types.Field(sgqlc.types.non_null('SequencingRead'), graphql_name='getSequencingRead', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    get_all_sequencing_reads = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SequencingRead'))), graphql_name='getAllSequencingReads')


class Sample(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ('id', 'type', 'producing_run_id', 'owner_user_id', 'name', 'location', 'sequencing_reads')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')
    producing_run_id = sgqlc.types.Field(Int, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    location = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='location')
    sequencing_reads = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SequencingRead'))), graphql_name='sequencingReads')


class SequencingRead(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ('id', 'type', 'producing_run_id', 'owner_user_id', 'nucleotide', 'sequence', 'protocol', 'sample_id', 'sample')
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='id')
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')
    producing_run_id = sgqlc.types.Field(Int, graphql_name='producingRunId')
    owner_user_id = sgqlc.types.Field(Int, graphql_name='ownerUserId')
    nucleotide = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='nucleotide')
    sequence = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='sequence')
    protocol = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='protocol')
    sample_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='sampleId')
    sample = sgqlc.types.Field(sgqlc.types.non_null(Sample), graphql_name='sample')



########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
gql_schema.query_type = Query
gql_schema.mutation_type = None
gql_schema.subscription_type = None

