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

DateTime = sgqlc.types.datetime.DateTime


class GlobalID(sgqlc.types.Scalar):
    __schema__ = gql_schema


ID = sgqlc.types.ID

Int = sgqlc.types.Int

String = sgqlc.types.String


class UUID(sgqlc.types.Scalar):
    __schema__ = gql_schema


class WorkflowCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "collectionId",
        "createdAt",
        "defaultVersion",
        "id",
        "minimumSupportedVersion",
        "name",
        "ownerUserId",
        "updatedAt",
        "versions",
    )


class WorkflowRunCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "collectionId",
        "createdAt",
        "deprecatedBy",
        "endedAt",
        "entityInputs",
        "executionId",
        "id",
        "outputsJson",
        "ownerUserId",
        "railsWorkflowRunId",
        "rawInputsJson",
        "startedAt",
        "status",
        "steps",
        "updatedAt",
        "workflowRunnerInputsJson",
        "workflowVersion",
    )


class WorkflowRunEntityInputCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "collectionId",
        "createdAt",
        "entityType",
        "fieldName",
        "id",
        "inputEntityId",
        "ownerUserId",
        "updatedAt",
        "workflowRun",
    )


class WorkflowRunStatus(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "ABORTED",
        "CREATED",
        "FAILED",
        "PENDING",
        "RUNNING",
        "STARTED",
        "SUCCEEDED",
        "SUCCEEDED_WITH_ISSUE",
        "TIMED_OUT",
    )


class WorkflowRunStepCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "collectionId",
        "createdAt",
        "endedAt",
        "id",
        "ownerUserId",
        "startedAt",
        "status",
        "updatedAt",
        "workflowRun",
    )


class WorkflowRunStepStatus(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("FAILED", "RUNNING", "SUCCEEDED")


class WorkflowVersionCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "collectionId",
        "createdAt",
        "graphJson",
        "id",
        "manifest",
        "ownerUserId",
        "runs",
        "updatedAt",
        "version",
        "workflow",
        "workflowUri",
    )


class orderBy(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("asc", "asc_nulls_first", "asc_nulls_last", "desc", "desc_nulls_first", "desc_nulls_last")


########################################################################
# Input Objects
########################################################################
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


class EntityInputType(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("name", "entity_id", "entity_type")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    entity_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="entityId")
    entity_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="entityType")


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


class RunWorkflowVersionInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "workflow_version_id", "entity_inputs", "raw_input_json")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    workflow_version_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="workflowVersionId")
    entity_inputs = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(EntityInputType)), graphql_name="entityInputs"
    )
    raw_input_json = sgqlc.types.Field(String, graphql_name="rawInputJson")


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


class WorkflowCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("name", "default_version", "minimum_supported_version", "collection_id")
    name = sgqlc.types.Field(String, graphql_name="name")
    default_version = sgqlc.types.Field(String, graphql_name="defaultVersion")
    minimum_supported_version = sgqlc.types.Field(String, graphql_name="minimumSupportedVersion")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")


class WorkflowOrderByClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "name",
        "default_version",
        "minimum_supported_version",
        "id",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    name = sgqlc.types.Field(orderBy, graphql_name="name")
    default_version = sgqlc.types.Field(orderBy, graphql_name="defaultVersion")
    minimum_supported_version = sgqlc.types.Field(orderBy, graphql_name="minimumSupportedVersion")
    id = sgqlc.types.Field(orderBy, graphql_name="id")
    owner_user_id = sgqlc.types.Field(orderBy, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(orderBy, graphql_name="collectionId")
    created_at = sgqlc.types.Field(orderBy, graphql_name="createdAt")
    updated_at = sgqlc.types.Field(orderBy, graphql_name="updatedAt")


class WorkflowRunEntityInputCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("input_entity_id", "field_name", "entity_type", "workflow_run_id", "collection_id")
    input_entity_id = sgqlc.types.Field(ID, graphql_name="inputEntityId")
    field_name = sgqlc.types.Field(String, graphql_name="fieldName")
    entity_type = sgqlc.types.Field(String, graphql_name="entityType")
    workflow_run_id = sgqlc.types.Field(ID, graphql_name="workflowRunId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")


class WorkflowRunEntityInputOrderByClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "input_entity_id",
        "field_name",
        "entity_type",
        "workflow_run",
        "id",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    input_entity_id = sgqlc.types.Field(orderBy, graphql_name="inputEntityId")
    field_name = sgqlc.types.Field(orderBy, graphql_name="fieldName")
    entity_type = sgqlc.types.Field(orderBy, graphql_name="entityType")
    workflow_run = sgqlc.types.Field("WorkflowRunOrderByClause", graphql_name="workflowRun")
    id = sgqlc.types.Field(orderBy, graphql_name="id")
    owner_user_id = sgqlc.types.Field(orderBy, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(orderBy, graphql_name="collectionId")
    created_at = sgqlc.types.Field(orderBy, graphql_name="createdAt")
    updated_at = sgqlc.types.Field(orderBy, graphql_name="updatedAt")


class WorkflowRunEntityInputWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "input_entity_id",
        "field_name",
        "entity_type",
        "workflow_run",
        "id",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    input_entity_id = sgqlc.types.Field(UUIDComparators, graphql_name="inputEntityId")
    field_name = sgqlc.types.Field(StrComparators, graphql_name="fieldName")
    entity_type = sgqlc.types.Field(StrComparators, graphql_name="entityType")
    workflow_run = sgqlc.types.Field("WorkflowRunWhereClause", graphql_name="workflowRun")
    id = sgqlc.types.Field(UUIDComparators, graphql_name="id")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    created_at = sgqlc.types.Field(DatetimeComparators, graphql_name="createdAt")
    updated_at = sgqlc.types.Field(DatetimeComparators, graphql_name="updatedAt")


class WorkflowRunEntityInputWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(UUIDComparators, graphql_name="id")


class WorkflowRunOrderByClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "rails_workflow_run_id",
        "started_at",
        "ended_at",
        "execution_id",
        "outputs_json",
        "workflow_runner_inputs_json",
        "status",
        "workflow_version",
        "raw_inputs_json",
        "deprecated_by",
        "id",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    rails_workflow_run_id = sgqlc.types.Field(orderBy, graphql_name="railsWorkflowRunId")
    started_at = sgqlc.types.Field(orderBy, graphql_name="startedAt")
    ended_at = sgqlc.types.Field(orderBy, graphql_name="endedAt")
    execution_id = sgqlc.types.Field(orderBy, graphql_name="executionId")
    outputs_json = sgqlc.types.Field(orderBy, graphql_name="outputsJson")
    workflow_runner_inputs_json = sgqlc.types.Field(orderBy, graphql_name="workflowRunnerInputsJson")
    status = sgqlc.types.Field(orderBy, graphql_name="status")
    workflow_version = sgqlc.types.Field("WorkflowVersionOrderByClause", graphql_name="workflowVersion")
    raw_inputs_json = sgqlc.types.Field(orderBy, graphql_name="rawInputsJson")
    deprecated_by = sgqlc.types.Field(orderBy, graphql_name="deprecatedBy")
    id = sgqlc.types.Field(orderBy, graphql_name="id")
    owner_user_id = sgqlc.types.Field(orderBy, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(orderBy, graphql_name="collectionId")
    created_at = sgqlc.types.Field(orderBy, graphql_name="createdAt")
    updated_at = sgqlc.types.Field(orderBy, graphql_name="updatedAt")


class WorkflowRunStatusEnumComparators(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("_eq", "_neq", "_in", "_nin", "_gt", "_gte", "_lt", "_lte", "_is_null")
    _eq = sgqlc.types.Field(WorkflowRunStatus, graphql_name="_eq")
    _neq = sgqlc.types.Field(WorkflowRunStatus, graphql_name="_neq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(WorkflowRunStatus)), graphql_name="_in")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(WorkflowRunStatus)), graphql_name="_nin")
    _gt = sgqlc.types.Field(WorkflowRunStatus, graphql_name="_gt")
    _gte = sgqlc.types.Field(WorkflowRunStatus, graphql_name="_gte")
    _lt = sgqlc.types.Field(WorkflowRunStatus, graphql_name="_lt")
    _lte = sgqlc.types.Field(WorkflowRunStatus, graphql_name="_lte")
    _is_null = sgqlc.types.Field(WorkflowRunStatus, graphql_name="_is_null")


class WorkflowRunStepCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("workflow_run_id", "ended_at", "status", "collection_id")
    workflow_run_id = sgqlc.types.Field(ID, graphql_name="workflowRunId")
    ended_at = sgqlc.types.Field(DateTime, graphql_name="endedAt")
    status = sgqlc.types.Field(WorkflowRunStepStatus, graphql_name="status")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")


class WorkflowRunStepOrderByClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "workflow_run",
        "started_at",
        "ended_at",
        "status",
        "id",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    workflow_run = sgqlc.types.Field(WorkflowRunOrderByClause, graphql_name="workflowRun")
    started_at = sgqlc.types.Field(orderBy, graphql_name="startedAt")
    ended_at = sgqlc.types.Field(orderBy, graphql_name="endedAt")
    status = sgqlc.types.Field(orderBy, graphql_name="status")
    id = sgqlc.types.Field(orderBy, graphql_name="id")
    owner_user_id = sgqlc.types.Field(orderBy, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(orderBy, graphql_name="collectionId")
    created_at = sgqlc.types.Field(orderBy, graphql_name="createdAt")
    updated_at = sgqlc.types.Field(orderBy, graphql_name="updatedAt")


class WorkflowRunStepStatusEnumComparators(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("_eq", "_neq", "_in", "_nin", "_gt", "_gte", "_lt", "_lte", "_is_null")
    _eq = sgqlc.types.Field(WorkflowRunStepStatus, graphql_name="_eq")
    _neq = sgqlc.types.Field(WorkflowRunStepStatus, graphql_name="_neq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(WorkflowRunStepStatus)), graphql_name="_in")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(WorkflowRunStepStatus)), graphql_name="_nin")
    _gt = sgqlc.types.Field(WorkflowRunStepStatus, graphql_name="_gt")
    _gte = sgqlc.types.Field(WorkflowRunStepStatus, graphql_name="_gte")
    _lt = sgqlc.types.Field(WorkflowRunStepStatus, graphql_name="_lt")
    _lte = sgqlc.types.Field(WorkflowRunStepStatus, graphql_name="_lte")
    _is_null = sgqlc.types.Field(WorkflowRunStepStatus, graphql_name="_is_null")


class WorkflowRunStepUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("ended_at", "status")
    ended_at = sgqlc.types.Field(DateTime, graphql_name="endedAt")
    status = sgqlc.types.Field(WorkflowRunStepStatus, graphql_name="status")


class WorkflowRunStepWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "workflow_run",
        "started_at",
        "ended_at",
        "status",
        "id",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    workflow_run = sgqlc.types.Field("WorkflowRunWhereClause", graphql_name="workflowRun")
    started_at = sgqlc.types.Field(DatetimeComparators, graphql_name="startedAt")
    ended_at = sgqlc.types.Field(DatetimeComparators, graphql_name="endedAt")
    status = sgqlc.types.Field(WorkflowRunStepStatusEnumComparators, graphql_name="status")
    id = sgqlc.types.Field(UUIDComparators, graphql_name="id")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    created_at = sgqlc.types.Field(DatetimeComparators, graphql_name="createdAt")
    updated_at = sgqlc.types.Field(DatetimeComparators, graphql_name="updatedAt")


class WorkflowRunStepWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(UUIDComparators, graphql_name="id")


class WorkflowRunUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "ended_at",
        "execution_id",
        "outputs_json",
        "workflow_runner_inputs_json",
        "status",
        "deprecated_by_id",
    )
    ended_at = sgqlc.types.Field(DateTime, graphql_name="endedAt")
    execution_id = sgqlc.types.Field(String, graphql_name="executionId")
    outputs_json = sgqlc.types.Field(String, graphql_name="outputsJson")
    workflow_runner_inputs_json = sgqlc.types.Field(String, graphql_name="workflowRunnerInputsJson")
    status = sgqlc.types.Field(WorkflowRunStatus, graphql_name="status")
    deprecated_by_id = sgqlc.types.Field(ID, graphql_name="deprecatedById")


class WorkflowRunWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "rails_workflow_run_id",
        "started_at",
        "ended_at",
        "execution_id",
        "outputs_json",
        "workflow_runner_inputs_json",
        "status",
        "workflow_version",
        "steps",
        "entity_inputs",
        "raw_inputs_json",
        "id",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    rails_workflow_run_id = sgqlc.types.Field(IntComparators, graphql_name="railsWorkflowRunId")
    started_at = sgqlc.types.Field(DatetimeComparators, graphql_name="startedAt")
    ended_at = sgqlc.types.Field(DatetimeComparators, graphql_name="endedAt")
    execution_id = sgqlc.types.Field(StrComparators, graphql_name="executionId")
    outputs_json = sgqlc.types.Field(StrComparators, graphql_name="outputsJson")
    workflow_runner_inputs_json = sgqlc.types.Field(StrComparators, graphql_name="workflowRunnerInputsJson")
    status = sgqlc.types.Field(WorkflowRunStatusEnumComparators, graphql_name="status")
    workflow_version = sgqlc.types.Field("WorkflowVersionWhereClause", graphql_name="workflowVersion")
    steps = sgqlc.types.Field(WorkflowRunStepWhereClause, graphql_name="steps")
    entity_inputs = sgqlc.types.Field(WorkflowRunEntityInputWhereClause, graphql_name="entityInputs")
    raw_inputs_json = sgqlc.types.Field(StrComparators, graphql_name="rawInputsJson")
    id = sgqlc.types.Field(UUIDComparators, graphql_name="id")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    created_at = sgqlc.types.Field(DatetimeComparators, graphql_name="createdAt")
    updated_at = sgqlc.types.Field(DatetimeComparators, graphql_name="updatedAt")


class WorkflowRunWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(UUIDComparators, graphql_name="id")


class WorkflowUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("name", "default_version", "minimum_supported_version")
    name = sgqlc.types.Field(String, graphql_name="name")
    default_version = sgqlc.types.Field(String, graphql_name="defaultVersion")
    minimum_supported_version = sgqlc.types.Field(String, graphql_name="minimumSupportedVersion")


class WorkflowVersionCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("graph_json", "workflow_uri", "version", "manifest", "workflow_id", "collection_id")
    graph_json = sgqlc.types.Field(String, graphql_name="graphJson")
    workflow_uri = sgqlc.types.Field(String, graphql_name="workflowUri")
    version = sgqlc.types.Field(String, graphql_name="version")
    manifest = sgqlc.types.Field(String, graphql_name="manifest")
    workflow_id = sgqlc.types.Field(ID, graphql_name="workflowId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")


class WorkflowVersionOrderByClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "graph_json",
        "workflow_uri",
        "version",
        "manifest",
        "workflow",
        "id",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    graph_json = sgqlc.types.Field(orderBy, graphql_name="graphJson")
    workflow_uri = sgqlc.types.Field(orderBy, graphql_name="workflowUri")
    version = sgqlc.types.Field(orderBy, graphql_name="version")
    manifest = sgqlc.types.Field(orderBy, graphql_name="manifest")
    workflow = sgqlc.types.Field(WorkflowOrderByClause, graphql_name="workflow")
    id = sgqlc.types.Field(orderBy, graphql_name="id")
    owner_user_id = sgqlc.types.Field(orderBy, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(orderBy, graphql_name="collectionId")
    created_at = sgqlc.types.Field(orderBy, graphql_name="createdAt")
    updated_at = sgqlc.types.Field(orderBy, graphql_name="updatedAt")


class WorkflowVersionWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "graph_json",
        "workflow_uri",
        "version",
        "manifest",
        "workflow",
        "runs",
        "id",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    graph_json = sgqlc.types.Field(StrComparators, graphql_name="graphJson")
    workflow_uri = sgqlc.types.Field(StrComparators, graphql_name="workflowUri")
    version = sgqlc.types.Field(StrComparators, graphql_name="version")
    manifest = sgqlc.types.Field(StrComparators, graphql_name="manifest")
    workflow = sgqlc.types.Field("WorkflowWhereClause", graphql_name="workflow")
    runs = sgqlc.types.Field(WorkflowRunWhereClause, graphql_name="runs")
    id = sgqlc.types.Field(UUIDComparators, graphql_name="id")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    created_at = sgqlc.types.Field(DatetimeComparators, graphql_name="createdAt")
    updated_at = sgqlc.types.Field(DatetimeComparators, graphql_name="updatedAt")


class WorkflowVersionWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(UUIDComparators, graphql_name="id")


class WorkflowWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "name",
        "default_version",
        "minimum_supported_version",
        "versions",
        "id",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    name = sgqlc.types.Field(StrComparators, graphql_name="name")
    default_version = sgqlc.types.Field(StrComparators, graphql_name="defaultVersion")
    minimum_supported_version = sgqlc.types.Field(StrComparators, graphql_name="minimumSupportedVersion")
    versions = sgqlc.types.Field(WorkflowVersionWhereClause, graphql_name="versions")
    id = sgqlc.types.Field(UUIDComparators, graphql_name="id")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    created_at = sgqlc.types.Field(DatetimeComparators, graphql_name="createdAt")
    updated_at = sgqlc.types.Field(DatetimeComparators, graphql_name="updatedAt")


class WorkflowWhereClauseMutations(sgqlc.types.Input):
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


class Mutation(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "create_workflow_run",
        "update_workflow_run",
        "delete_workflow_run",
        "create_workflow",
        "update_workflow",
        "delete_workflow",
        "create_workflow_run_step",
        "update_workflow_run_step",
        "delete_workflow_run_step",
        "create_workflow_run_entity_input",
        "delete_workflow_run_entity_input",
        "create_workflow_version",
        "delete_workflow_version",
        "run_workflow_version",
        "run_workflow_run",
    )
    create_workflow_run = sgqlc.types.Field(
        sgqlc.types.non_null("WorkflowRun"),
        graphql_name="createWorkflowRun",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(sgqlc.types.non_null(RunWorkflowVersionInput), graphql_name="input", default=None),
                ),
            )
        ),
    )
    update_workflow_run = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("WorkflowRun"))),
        graphql_name="updateWorkflowRun",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(sgqlc.types.non_null(WorkflowRunUpdateInput), graphql_name="input", default=None),
                ),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(WorkflowRunWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_workflow_run = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("WorkflowRun"))),
        graphql_name="deleteWorkflowRun",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(WorkflowRunWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    create_workflow = sgqlc.types.Field(
        sgqlc.types.non_null("Workflow"),
        graphql_name="createWorkflow",
        args=sgqlc.types.ArgDict(
            (("input", sgqlc.types.Arg(sgqlc.types.non_null(WorkflowCreateInput), graphql_name="input", default=None)),)
        ),
    )
    update_workflow = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Workflow"))),
        graphql_name="updateWorkflow",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(sgqlc.types.non_null(WorkflowUpdateInput), graphql_name="input", default=None),
                ),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(WorkflowWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_workflow = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Workflow"))),
        graphql_name="deleteWorkflow",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(WorkflowWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    create_workflow_run_step = sgqlc.types.Field(
        sgqlc.types.non_null("WorkflowRunStep"),
        graphql_name="createWorkflowRunStep",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(WorkflowRunStepCreateInput), graphql_name="input", default=None
                    ),
                ),
            )
        ),
    )
    update_workflow_run_step = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("WorkflowRunStep"))),
        graphql_name="updateWorkflowRunStep",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(WorkflowRunStepUpdateInput), graphql_name="input", default=None
                    ),
                ),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(WorkflowRunStepWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_workflow_run_step = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("WorkflowRunStep"))),
        graphql_name="deleteWorkflowRunStep",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(WorkflowRunStepWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    create_workflow_run_entity_input = sgqlc.types.Field(
        sgqlc.types.non_null("WorkflowRunEntityInput"),
        graphql_name="createWorkflowRunEntityInput",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(WorkflowRunEntityInputCreateInput), graphql_name="input", default=None
                    ),
                ),
            )
        ),
    )
    delete_workflow_run_entity_input = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("WorkflowRunEntityInput"))),
        graphql_name="deleteWorkflowRunEntityInput",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(WorkflowRunEntityInputWhereClauseMutations),
                        graphql_name="where",
                        default=None,
                    ),
                ),
            )
        ),
    )
    create_workflow_version = sgqlc.types.Field(
        sgqlc.types.non_null("WorkflowVersion"),
        graphql_name="createWorkflowVersion",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(WorkflowVersionCreateInput), graphql_name="input", default=None
                    ),
                ),
            )
        ),
    )
    delete_workflow_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("WorkflowVersion"))),
        graphql_name="deleteWorkflowVersion",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(WorkflowVersionWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    run_workflow_version = sgqlc.types.Field(
        sgqlc.types.non_null("WorkflowRun"),
        graphql_name="runWorkflowVersion",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(sgqlc.types.non_null(RunWorkflowVersionInput), graphql_name="input", default=None),
                ),
            )
        ),
    )
    run_workflow_run = sgqlc.types.Field(
        sgqlc.types.non_null("WorkflowRun"),
        graphql_name="runWorkflowRun",
        args=sgqlc.types.ArgDict(
            (
                (
                    "workflow_run_id",
                    sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name="workflowRunId", default=None),
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
        "workflow_runs",
        "workflows",
        "workflow_run_steps",
        "workflow_run_entity_inputs",
        "workflow_versions",
        "workflow_runs_aggregate",
        "workflows_aggregate",
        "workflow_run_steps_aggregate",
        "workflow_run_entity_inputs_aggregate",
        "workflow_versions_aggregate",
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
    workflow_runs = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("WorkflowRun"))),
        graphql_name="workflowRuns",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(WorkflowRunWhereClause, graphql_name="where", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(WorkflowRunOrderByClause)),
                        graphql_name="orderBy",
                        default=(),
                    ),
                ),
            )
        ),
    )
    workflows = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Workflow"))),
        graphql_name="workflows",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(WorkflowWhereClause, graphql_name="where", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(WorkflowOrderByClause)),
                        graphql_name="orderBy",
                        default=(),
                    ),
                ),
            )
        ),
    )
    workflow_run_steps = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("WorkflowRunStep"))),
        graphql_name="workflowRunSteps",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(WorkflowRunStepWhereClause, graphql_name="where", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(WorkflowRunStepOrderByClause)),
                        graphql_name="orderBy",
                        default=(),
                    ),
                ),
            )
        ),
    )
    workflow_run_entity_inputs = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("WorkflowRunEntityInput"))),
        graphql_name="workflowRunEntityInputs",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(WorkflowRunEntityInputWhereClause, graphql_name="where", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(WorkflowRunEntityInputOrderByClause)),
                        graphql_name="orderBy",
                        default=(),
                    ),
                ),
            )
        ),
    )
    workflow_versions = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("WorkflowVersion"))),
        graphql_name="workflowVersions",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(WorkflowVersionWhereClause, graphql_name="where", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(WorkflowVersionOrderByClause)),
                        graphql_name="orderBy",
                        default=(),
                    ),
                ),
            )
        ),
    )
    workflow_runs_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("WorkflowRunAggregate"),
        graphql_name="workflowRunsAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(WorkflowRunWhereClause, graphql_name="where", default=None)),)
        ),
    )
    workflows_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("WorkflowAggregate"),
        graphql_name="workflowsAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(WorkflowWhereClause, graphql_name="where", default=None)),)
        ),
    )
    workflow_run_steps_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("WorkflowRunStepAggregate"),
        graphql_name="workflowRunStepsAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(WorkflowRunStepWhereClause, graphql_name="where", default=None)),)
        ),
    )
    workflow_run_entity_inputs_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("WorkflowRunEntityInputAggregate"),
        graphql_name="workflowRunEntityInputsAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(WorkflowRunEntityInputWhereClause, graphql_name="where", default=None)),)
        ),
    )
    workflow_versions_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("WorkflowVersionAggregate"),
        graphql_name="workflowVersionsAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(WorkflowVersionWhereClause, graphql_name="where", default=None)),)
        ),
    )


class WorkflowAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("WorkflowAggregateFunctions")), graphql_name="aggregate"
    )


class WorkflowAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "stddev", "variance", "min", "max", "group_by", "count")
    sum = sgqlc.types.Field("WorkflowNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("WorkflowNumericalColumns", graphql_name="avg")
    stddev = sgqlc.types.Field("WorkflowNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("WorkflowNumericalColumns", graphql_name="variance")
    min = sgqlc.types.Field("WorkflowMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("WorkflowMinMaxColumns", graphql_name="max")
    group_by = sgqlc.types.Field("WorkflowGroupByOptions", graphql_name="groupBy")
    count = sgqlc.types.Field(
        Int,
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=False)),
                ("columns", sgqlc.types.Arg(WorkflowCountColumns, graphql_name="columns", default=None)),
            )
        ),
    )


class WorkflowGroupByOptions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "name",
        "default_version",
        "minimum_supported_version",
        "id",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    name = sgqlc.types.Field(String, graphql_name="name")
    default_version = sgqlc.types.Field(String, graphql_name="defaultVersion")
    minimum_supported_version = sgqlc.types.Field(String, graphql_name="minimumSupportedVersion")
    id = sgqlc.types.Field(UUID, graphql_name="id")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    created_at = sgqlc.types.Field(DateTime, graphql_name="createdAt")
    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")


class WorkflowMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "name",
        "default_version",
        "minimum_supported_version",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    name = sgqlc.types.Field(String, graphql_name="name")
    default_version = sgqlc.types.Field(String, graphql_name="defaultVersion")
    minimum_supported_version = sgqlc.types.Field(String, graphql_name="minimumSupportedVersion")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    created_at = sgqlc.types.Field(DateTime, graphql_name="createdAt")
    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")


class WorkflowNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("owner_user_id", "collection_id")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class WorkflowRunAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("WorkflowRunAggregateFunctions")), graphql_name="aggregate"
    )


class WorkflowRunAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "stddev", "variance", "min", "max", "group_by", "count")
    sum = sgqlc.types.Field("WorkflowRunNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("WorkflowRunNumericalColumns", graphql_name="avg")
    stddev = sgqlc.types.Field("WorkflowRunNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("WorkflowRunNumericalColumns", graphql_name="variance")
    min = sgqlc.types.Field("WorkflowRunMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("WorkflowRunMinMaxColumns", graphql_name="max")
    group_by = sgqlc.types.Field("WorkflowRunGroupByOptions", graphql_name="groupBy")
    count = sgqlc.types.Field(
        Int,
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=False)),
                ("columns", sgqlc.types.Arg(WorkflowRunCountColumns, graphql_name="columns", default=None)),
            )
        ),
    )


class WorkflowRunConnection(sgqlc.types.relay.Connection):
    __schema__ = gql_schema
    __field_names__ = ("page_info", "edges")
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name="pageInfo")
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("WorkflowRunEdge"))), graphql_name="edges"
    )


class WorkflowRunEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("cursor", "node")
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="cursor")
    node = sgqlc.types.Field(sgqlc.types.non_null("WorkflowRun"), graphql_name="node")


class WorkflowRunEntityInputAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("WorkflowRunEntityInputAggregateFunctions")), graphql_name="aggregate"
    )


class WorkflowRunEntityInputAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "stddev", "variance", "min", "max", "group_by", "count")
    sum = sgqlc.types.Field("WorkflowRunEntityInputNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("WorkflowRunEntityInputNumericalColumns", graphql_name="avg")
    stddev = sgqlc.types.Field("WorkflowRunEntityInputNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("WorkflowRunEntityInputNumericalColumns", graphql_name="variance")
    min = sgqlc.types.Field("WorkflowRunEntityInputMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("WorkflowRunEntityInputMinMaxColumns", graphql_name="max")
    group_by = sgqlc.types.Field("WorkflowRunEntityInputGroupByOptions", graphql_name="groupBy")
    count = sgqlc.types.Field(
        Int,
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=False)),
                ("columns", sgqlc.types.Arg(WorkflowRunEntityInputCountColumns, graphql_name="columns", default=None)),
            )
        ),
    )


class WorkflowRunEntityInputConnection(sgqlc.types.relay.Connection):
    __schema__ = gql_schema
    __field_names__ = ("page_info", "edges")
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name="pageInfo")
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("WorkflowRunEntityInputEdge"))),
        graphql_name="edges",
    )


class WorkflowRunEntityInputEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("cursor", "node")
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="cursor")
    node = sgqlc.types.Field(sgqlc.types.non_null("WorkflowRunEntityInput"), graphql_name="node")


class WorkflowRunEntityInputGroupByOptions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "input_entity_id",
        "field_name",
        "entity_type",
        "workflow_run",
        "id",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    input_entity_id = sgqlc.types.Field(UUID, graphql_name="inputEntityId")
    field_name = sgqlc.types.Field(String, graphql_name="fieldName")
    entity_type = sgqlc.types.Field(String, graphql_name="entityType")
    workflow_run = sgqlc.types.Field("WorkflowRunGroupByOptions", graphql_name="workflowRun")
    id = sgqlc.types.Field(UUID, graphql_name="id")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    created_at = sgqlc.types.Field(DateTime, graphql_name="createdAt")
    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")


class WorkflowRunEntityInputMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("field_name", "entity_type", "owner_user_id", "collection_id", "created_at", "updated_at")
    field_name = sgqlc.types.Field(String, graphql_name="fieldName")
    entity_type = sgqlc.types.Field(String, graphql_name="entityType")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    created_at = sgqlc.types.Field(DateTime, graphql_name="createdAt")
    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")


class WorkflowRunEntityInputNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("owner_user_id", "collection_id")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class WorkflowRunGroupByOptions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "rails_workflow_run_id",
        "started_at",
        "ended_at",
        "execution_id",
        "outputs_json",
        "workflow_runner_inputs_json",
        "status",
        "workflow_version",
        "raw_inputs_json",
        "deprecated_by",
        "id",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    rails_workflow_run_id = sgqlc.types.Field(Int, graphql_name="railsWorkflowRunId")
    started_at = sgqlc.types.Field(DateTime, graphql_name="startedAt")
    ended_at = sgqlc.types.Field(DateTime, graphql_name="endedAt")
    execution_id = sgqlc.types.Field(String, graphql_name="executionId")
    outputs_json = sgqlc.types.Field(String, graphql_name="outputsJson")
    workflow_runner_inputs_json = sgqlc.types.Field(String, graphql_name="workflowRunnerInputsJson")
    status = sgqlc.types.Field(WorkflowRunStatus, graphql_name="status")
    workflow_version = sgqlc.types.Field("WorkflowVersionGroupByOptions", graphql_name="workflowVersion")
    raw_inputs_json = sgqlc.types.Field(String, graphql_name="rawInputsJson")
    deprecated_by = sgqlc.types.Field("WorkflowRunGroupByOptions", graphql_name="deprecatedBy")
    id = sgqlc.types.Field(UUID, graphql_name="id")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    created_at = sgqlc.types.Field(DateTime, graphql_name="createdAt")
    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")


class WorkflowRunMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "rails_workflow_run_id",
        "started_at",
        "ended_at",
        "execution_id",
        "outputs_json",
        "workflow_runner_inputs_json",
        "raw_inputs_json",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    rails_workflow_run_id = sgqlc.types.Field(Int, graphql_name="railsWorkflowRunId")
    started_at = sgqlc.types.Field(DateTime, graphql_name="startedAt")
    ended_at = sgqlc.types.Field(DateTime, graphql_name="endedAt")
    execution_id = sgqlc.types.Field(String, graphql_name="executionId")
    outputs_json = sgqlc.types.Field(String, graphql_name="outputsJson")
    workflow_runner_inputs_json = sgqlc.types.Field(String, graphql_name="workflowRunnerInputsJson")
    raw_inputs_json = sgqlc.types.Field(String, graphql_name="rawInputsJson")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    created_at = sgqlc.types.Field(DateTime, graphql_name="createdAt")
    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")


class WorkflowRunNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("rails_workflow_run_id", "owner_user_id", "collection_id")
    rails_workflow_run_id = sgqlc.types.Field(Int, graphql_name="railsWorkflowRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class WorkflowRunStepAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("WorkflowRunStepAggregateFunctions")), graphql_name="aggregate"
    )


class WorkflowRunStepAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "stddev", "variance", "min", "max", "group_by", "count")
    sum = sgqlc.types.Field("WorkflowRunStepNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("WorkflowRunStepNumericalColumns", graphql_name="avg")
    stddev = sgqlc.types.Field("WorkflowRunStepNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("WorkflowRunStepNumericalColumns", graphql_name="variance")
    min = sgqlc.types.Field("WorkflowRunStepMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("WorkflowRunStepMinMaxColumns", graphql_name="max")
    group_by = sgqlc.types.Field("WorkflowRunStepGroupByOptions", graphql_name="groupBy")
    count = sgqlc.types.Field(
        Int,
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=False)),
                ("columns", sgqlc.types.Arg(WorkflowRunStepCountColumns, graphql_name="columns", default=None)),
            )
        ),
    )


class WorkflowRunStepConnection(sgqlc.types.relay.Connection):
    __schema__ = gql_schema
    __field_names__ = ("page_info", "edges")
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name="pageInfo")
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("WorkflowRunStepEdge"))), graphql_name="edges"
    )


class WorkflowRunStepEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("cursor", "node")
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="cursor")
    node = sgqlc.types.Field(sgqlc.types.non_null("WorkflowRunStep"), graphql_name="node")


class WorkflowRunStepGroupByOptions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "workflow_run",
        "started_at",
        "ended_at",
        "status",
        "id",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    workflow_run = sgqlc.types.Field(WorkflowRunGroupByOptions, graphql_name="workflowRun")
    started_at = sgqlc.types.Field(DateTime, graphql_name="startedAt")
    ended_at = sgqlc.types.Field(DateTime, graphql_name="endedAt")
    status = sgqlc.types.Field(WorkflowRunStepStatus, graphql_name="status")
    id = sgqlc.types.Field(UUID, graphql_name="id")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    created_at = sgqlc.types.Field(DateTime, graphql_name="createdAt")
    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")


class WorkflowRunStepMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("started_at", "ended_at", "owner_user_id", "collection_id", "created_at", "updated_at")
    started_at = sgqlc.types.Field(DateTime, graphql_name="startedAt")
    ended_at = sgqlc.types.Field(DateTime, graphql_name="endedAt")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    created_at = sgqlc.types.Field(DateTime, graphql_name="createdAt")
    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")


class WorkflowRunStepNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("owner_user_id", "collection_id")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class WorkflowVersionAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("WorkflowVersionAggregateFunctions")), graphql_name="aggregate"
    )


class WorkflowVersionAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "stddev", "variance", "min", "max", "group_by", "count")
    sum = sgqlc.types.Field("WorkflowVersionNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("WorkflowVersionNumericalColumns", graphql_name="avg")
    stddev = sgqlc.types.Field("WorkflowVersionNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("WorkflowVersionNumericalColumns", graphql_name="variance")
    min = sgqlc.types.Field("WorkflowVersionMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("WorkflowVersionMinMaxColumns", graphql_name="max")
    group_by = sgqlc.types.Field("WorkflowVersionGroupByOptions", graphql_name="groupBy")
    count = sgqlc.types.Field(
        Int,
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=False)),
                ("columns", sgqlc.types.Arg(WorkflowVersionCountColumns, graphql_name="columns", default=None)),
            )
        ),
    )


class WorkflowVersionConnection(sgqlc.types.relay.Connection):
    __schema__ = gql_schema
    __field_names__ = ("page_info", "edges")
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name="pageInfo")
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("WorkflowVersionEdge"))), graphql_name="edges"
    )


class WorkflowVersionEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("cursor", "node")
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="cursor")
    node = sgqlc.types.Field(sgqlc.types.non_null("WorkflowVersion"), graphql_name="node")


class WorkflowVersionGroupByOptions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "graph_json",
        "workflow_uri",
        "version",
        "manifest",
        "workflow",
        "id",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    graph_json = sgqlc.types.Field(String, graphql_name="graphJson")
    workflow_uri = sgqlc.types.Field(String, graphql_name="workflowUri")
    version = sgqlc.types.Field(String, graphql_name="version")
    manifest = sgqlc.types.Field(String, graphql_name="manifest")
    workflow = sgqlc.types.Field(WorkflowGroupByOptions, graphql_name="workflow")
    id = sgqlc.types.Field(UUID, graphql_name="id")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    created_at = sgqlc.types.Field(DateTime, graphql_name="createdAt")
    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")


class WorkflowVersionMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "graph_json",
        "workflow_uri",
        "version",
        "manifest",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    graph_json = sgqlc.types.Field(String, graphql_name="graphJson")
    workflow_uri = sgqlc.types.Field(String, graphql_name="workflowUri")
    version = sgqlc.types.Field(String, graphql_name="version")
    manifest = sgqlc.types.Field(String, graphql_name="manifest")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    created_at = sgqlc.types.Field(DateTime, graphql_name="createdAt")
    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")


class WorkflowVersionNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("owner_user_id", "collection_id")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class Workflow(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "name",
        "default_version",
        "minimum_supported_version",
        "versions",
        "versions_aggregate",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    name = sgqlc.types.Field(String, graphql_name="name")
    default_version = sgqlc.types.Field(String, graphql_name="defaultVersion")
    minimum_supported_version = sgqlc.types.Field(String, graphql_name="minimumSupportedVersion")
    versions = sgqlc.types.Field(
        sgqlc.types.non_null(WorkflowVersionConnection),
        graphql_name="versions",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(WorkflowVersionWhereClause, graphql_name="where", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(WorkflowVersionOrderByClause)),
                        graphql_name="orderBy",
                        default=(),
                    ),
                ),
                ("before", sgqlc.types.Arg(String, graphql_name="before", default=None)),
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
            )
        ),
    )
    versions_aggregate = sgqlc.types.Field(
        WorkflowVersionAggregate,
        graphql_name="versionsAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(WorkflowVersionWhereClause, graphql_name="where", default=None)),)
        ),
    )
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    created_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name="createdAt")
    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")


class WorkflowRun(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "rails_workflow_run_id",
        "started_at",
        "ended_at",
        "execution_id",
        "outputs_json",
        "workflow_runner_inputs_json",
        "status",
        "workflow_version",
        "steps",
        "steps_aggregate",
        "entity_inputs",
        "entity_inputs_aggregate",
        "raw_inputs_json",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    rails_workflow_run_id = sgqlc.types.Field(Int, graphql_name="railsWorkflowRunId")
    started_at = sgqlc.types.Field(DateTime, graphql_name="startedAt")
    ended_at = sgqlc.types.Field(DateTime, graphql_name="endedAt")
    execution_id = sgqlc.types.Field(String, graphql_name="executionId")
    outputs_json = sgqlc.types.Field(String, graphql_name="outputsJson")
    workflow_runner_inputs_json = sgqlc.types.Field(String, graphql_name="workflowRunnerInputsJson")
    status = sgqlc.types.Field(WorkflowRunStatus, graphql_name="status")
    workflow_version = sgqlc.types.Field(
        "WorkflowVersion",
        graphql_name="workflowVersion",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(WorkflowVersionWhereClause, graphql_name="where", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(WorkflowVersionOrderByClause)),
                        graphql_name="orderBy",
                        default=(),
                    ),
                ),
            )
        ),
    )
    steps = sgqlc.types.Field(
        sgqlc.types.non_null(WorkflowRunStepConnection),
        graphql_name="steps",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(WorkflowRunStepWhereClause, graphql_name="where", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(WorkflowRunStepOrderByClause)),
                        graphql_name="orderBy",
                        default=(),
                    ),
                ),
                ("before", sgqlc.types.Arg(String, graphql_name="before", default=None)),
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
            )
        ),
    )
    steps_aggregate = sgqlc.types.Field(
        WorkflowRunStepAggregate,
        graphql_name="stepsAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(WorkflowRunStepWhereClause, graphql_name="where", default=None)),)
        ),
    )
    entity_inputs = sgqlc.types.Field(
        sgqlc.types.non_null(WorkflowRunEntityInputConnection),
        graphql_name="entityInputs",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(WorkflowRunEntityInputWhereClause, graphql_name="where", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(WorkflowRunEntityInputOrderByClause)),
                        graphql_name="orderBy",
                        default=(),
                    ),
                ),
                ("before", sgqlc.types.Arg(String, graphql_name="before", default=None)),
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
            )
        ),
    )
    entity_inputs_aggregate = sgqlc.types.Field(
        WorkflowRunEntityInputAggregate,
        graphql_name="entityInputsAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(WorkflowRunEntityInputWhereClause, graphql_name="where", default=None)),)
        ),
    )
    raw_inputs_json = sgqlc.types.Field(String, graphql_name="rawInputsJson")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    created_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name="createdAt")
    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")


class WorkflowRunEntityInput(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "input_entity_id",
        "field_name",
        "entity_type",
        "workflow_run",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    input_entity_id = sgqlc.types.Field(ID, graphql_name="inputEntityId")
    field_name = sgqlc.types.Field(String, graphql_name="fieldName")
    entity_type = sgqlc.types.Field(String, graphql_name="entityType")
    workflow_run = sgqlc.types.Field(
        WorkflowRun,
        graphql_name="workflowRun",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(WorkflowRunWhereClause, graphql_name="where", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(WorkflowRunOrderByClause)),
                        graphql_name="orderBy",
                        default=(),
                    ),
                ),
            )
        ),
    )
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    created_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name="createdAt")
    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")


class WorkflowRunStep(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "workflow_run",
        "started_at",
        "ended_at",
        "status",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    workflow_run = sgqlc.types.Field(
        WorkflowRun,
        graphql_name="workflowRun",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(WorkflowRunWhereClause, graphql_name="where", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(WorkflowRunOrderByClause)),
                        graphql_name="orderBy",
                        default=(),
                    ),
                ),
            )
        ),
    )
    started_at = sgqlc.types.Field(DateTime, graphql_name="startedAt")
    ended_at = sgqlc.types.Field(DateTime, graphql_name="endedAt")
    status = sgqlc.types.Field(WorkflowRunStepStatus, graphql_name="status")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    created_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name="createdAt")
    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")


class WorkflowVersion(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "graph_json",
        "workflow_uri",
        "version",
        "manifest",
        "workflow",
        "runs",
        "runs_aggregate",
        "owner_user_id",
        "collection_id",
        "created_at",
        "updated_at",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    graph_json = sgqlc.types.Field(String, graphql_name="graphJson")
    workflow_uri = sgqlc.types.Field(String, graphql_name="workflowUri")
    version = sgqlc.types.Field(String, graphql_name="version")
    manifest = sgqlc.types.Field(String, graphql_name="manifest")
    workflow = sgqlc.types.Field(
        Workflow,
        graphql_name="workflow",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(WorkflowWhereClause, graphql_name="where", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(WorkflowOrderByClause)),
                        graphql_name="orderBy",
                        default=(),
                    ),
                ),
            )
        ),
    )
    runs = sgqlc.types.Field(
        sgqlc.types.non_null(WorkflowRunConnection),
        graphql_name="runs",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(WorkflowRunWhereClause, graphql_name="where", default=None)),
                (
                    "order_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(WorkflowRunOrderByClause)),
                        graphql_name="orderBy",
                        default=(),
                    ),
                ),
                ("before", sgqlc.types.Arg(String, graphql_name="before", default=None)),
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
            )
        ),
    )
    runs_aggregate = sgqlc.types.Field(
        WorkflowRunAggregate,
        graphql_name="runsAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(WorkflowRunWhereClause, graphql_name="where", default=None)),)
        ),
    )
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    created_at = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name="createdAt")
    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")


########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
gql_schema.query_type = Query
gql_schema.mutation_type = Mutation
gql_schema.subscription_type = None
