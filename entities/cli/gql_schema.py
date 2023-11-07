import sgqlc.types
import sgqlc.types.relay


gql_schema = sgqlc.types.Schema()


# Unexport Node/PageInfo, let schema re-declare them
gql_schema -= sgqlc.types.relay.Node
gql_schema -= sgqlc.types.relay.PageInfo


########################################################################
# Scalars and Enumerations
########################################################################
Boolean = sgqlc.types.Boolean


class FileStatus(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("FAILED", "PENDING", "SUCCESS")


class GlobalID(sgqlc.types.Scalar):
    __schema__ = gql_schema


ID = sgqlc.types.ID

Int = sgqlc.types.Int


class JSON(sgqlc.types.Scalar):
    __schema__ = gql_schema


class Nucleotide(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("DNA", "RNA")


class SequencingProtocol(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("MNGS", "MSSPE", "TARGETED")


String = sgqlc.types.String


class UUID(sgqlc.types.Scalar):
    __schema__ = gql_schema


########################################################################
# Input Objects
########################################################################
class ContigWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "sequencing_read",
        "sequence",
        "entity_id",
    )
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field("IntComparators", graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field("IntComparators", graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field("IntComparators", graphql_name="collectionId")
    sequencing_read = sgqlc.types.Field("SequencingReadWhereClause", graphql_name="sequencingRead")
    sequence = sgqlc.types.Field("StrComparators", graphql_name="sequence")
    entity_id = sgqlc.types.Field("UUIDComparators", graphql_name="entityId")


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


class NucleotideEnumComparators(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("_eq", "_neq", "_in", "_nin", "_gt", "_gte", "_lt", "_lte", "_is_null")
    _eq = sgqlc.types.Field(Nucleotide, graphql_name="_eq")
    _neq = sgqlc.types.Field(Nucleotide, graphql_name="_neq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Nucleotide)), graphql_name="_in")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Nucleotide)), graphql_name="_nin")
    _gt = sgqlc.types.Field(Nucleotide, graphql_name="_gt")
    _gte = sgqlc.types.Field(Nucleotide, graphql_name="_gte")
    _lt = sgqlc.types.Field(Nucleotide, graphql_name="_lt")
    _lte = sgqlc.types.Field(Nucleotide, graphql_name="_lte")
    _is_null = sgqlc.types.Field(Nucleotide, graphql_name="_is_null")


class SampleWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "name",
        "location",
        "sequencing_reads",
        "entity_id",
    )
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    name = sgqlc.types.Field("StrComparators", graphql_name="name")
    location = sgqlc.types.Field("StrComparators", graphql_name="location")
    sequencing_reads = sgqlc.types.Field("SequencingReadWhereClause", graphql_name="sequencingReads")
    entity_id = sgqlc.types.Field("UUIDComparators", graphql_name="entityId")


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


class SequencingReadWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "nucleotide",
        "sequence",
        "protocol",
        "sample",
        "contigs",
        "entity_id",
    )
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    nucleotide = sgqlc.types.Field(NucleotideEnumComparators, graphql_name="nucleotide")
    sequence = sgqlc.types.Field("StrComparators", graphql_name="sequence")
    protocol = sgqlc.types.Field(SequencingProtocolEnumComparators, graphql_name="protocol")
    sample = sgqlc.types.Field(SampleWhereClause, graphql_name="sample")
    contigs = sgqlc.types.Field(ContigWhereClause, graphql_name="contigs")
    entity_id = sgqlc.types.Field("UUIDComparators", graphql_name="entityId")


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
class Node(sgqlc.types.Interface):
    __schema__ = gql_schema
    __field_names__ = ("_id",)
    _id = sgqlc.types.Field(sgqlc.types.non_null(GlobalID), graphql_name="_id")


class EntityInterface(sgqlc.types.Interface):
    __schema__ = gql_schema
    __field_names__ = ("_id",)
    _id = sgqlc.types.Field(sgqlc.types.non_null(GlobalID), graphql_name="_id")


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
        "create_sample",
        "create_sequencing_read",
        "update_sample",
        "create_file",
        "upload_file",
        "mark_upload_complete",
    )
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
                (
                    "nucleotide",
                    sgqlc.types.Arg(sgqlc.types.non_null(Nucleotide), graphql_name="nucleotide", default=None),
                ),
                ("sequence", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="sequence", default=None)),
                (
                    "protocol",
                    sgqlc.types.Arg(sgqlc.types.non_null(SequencingProtocol), graphql_name="protocol", default=None),
                ),
                (
                    "sequence_file_id",
                    sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name="sequenceFileId", default=None),
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
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("location", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="location", default=None)),
                ("entity_id", sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name="entityId", default=None)),
            )
        ),
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


class PageInfo(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("has_next_page", "has_previous_page", "start_cursor", "end_cursor")
    has_next_page = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="hasNextPage")
    has_previous_page = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="hasPreviousPage")
    start_cursor = sgqlc.types.Field(String, graphql_name="startCursor")
    end_cursor = sgqlc.types.Field(String, graphql_name="endCursor")


class Query(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("node", "samples", "sequencing_reads", "contigs", "files")
    node = sgqlc.types.Field(
        sgqlc.types.non_null(Node),
        graphql_name="node",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(sgqlc.types.non_null(GlobalID), graphql_name="id", default=None)),)
        ),
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
    contigs = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Contig"))),
        graphql_name="contigs",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(ContigWhereClause, graphql_name="where", default=None)),)),
    )
    files = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(File))),
        graphql_name="files",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(FileWhereClause, graphql_name="where", default=None)),)),
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


class SignedURL(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("url", "protocol", "method", "expiration", "fields")
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="url")
    protocol = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="protocol")
    method = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="method")
    expiration = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="expiration")
    fields = sgqlc.types.Field(JSON, graphql_name="fields")


class Contig(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "sequencing_read",
        "sequence",
        "entity_id",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="producingRunId")
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
    entity_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="entityId")


class Sample(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "name",
        "location",
        "sequencing_reads",
        "entity_id",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    location = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="location")
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
    entity_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="entityId")


class SequencingRead(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "nucleotide",
        "sequence",
        "protocol",
        "sequence_file_id",
        "sequence_file",
        "sample",
        "contigs",
        "entity_id",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    nucleotide = sgqlc.types.Field(sgqlc.types.non_null(Nucleotide), graphql_name="nucleotide")
    sequence = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="sequence")
    protocol = sgqlc.types.Field(sgqlc.types.non_null(SequencingProtocol), graphql_name="protocol")
    sequence_file_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="sequenceFileId")
    sequence_file = sgqlc.types.Field(
        sgqlc.types.non_null(File),
        graphql_name="sequenceFile",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(FileWhereClause, graphql_name="where", default=None)),)),
    )
    sample = sgqlc.types.Field(
        Sample,
        graphql_name="sample",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(SampleWhereClause, graphql_name="where", default=None)),)),
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
    entity_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="entityId")


########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
gql_schema.query_type = Query
gql_schema.mutation_type = Mutation
gql_schema.subscription_type = None
