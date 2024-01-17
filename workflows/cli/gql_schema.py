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


class RunCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "collection_id",
        "ended_at",
        "entity_id",
        "execution_id",
        "id",
        "inputs_json",
        "outputs_json",
        "owner_user_id",
        "producing_run_id",
        "run_entity_inputs",
        "run_steps",
        "started_at",
        "status",
        "workflow_version",
    )


class RunEntityInputCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "collection_id",
        "entity_id",
        "field_name",
        "id",
        "new_entity_id",
        "owner_user_id",
        "producing_run_id",
        "run",
    )


class RunStatus(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("FAILED", "PENDING", "RUNNING", "STARTED", "SUCCEEDED")


class RunStepCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "collection_id",
        "ended_at",
        "entity_id",
        "id",
        "owner_user_id",
        "producing_run_id",
        "run",
        "started_at",
        "status",
    )


String = sgqlc.types.String


class UUID(sgqlc.types.Scalar):
    __schema__ = gql_schema


class WorkflowCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "collection_id",
        "default_version",
        "entity_id",
        "id",
        "minimum_supported_version",
        "name",
        "owner_user_id",
        "producing_run_id",
        "versions",
    )


class WorkflowVersionCountColumns(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = (
        "collection_id",
        "entity_id",
        "graph_json",
        "id",
        "manifest",
        "owner_user_id",
        "producing_run_id",
        "runs",
        "version",
        "workflow",
        "workflow_uri",
    )


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


class RunCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "collection_id",
        "started_at",
        "ended_at",
        "execution_id",
        "outputs_json",
        "inputs_json",
        "status",
        "workflow_version_id",
    )
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    started_at = sgqlc.types.Field(DateTime, graphql_name="startedAt")
    ended_at = sgqlc.types.Field(DateTime, graphql_name="endedAt")
    execution_id = sgqlc.types.Field(String, graphql_name="executionId")
    outputs_json = sgqlc.types.Field(String, graphql_name="outputsJson")
    inputs_json = sgqlc.types.Field(String, graphql_name="inputsJson")
    status = sgqlc.types.Field(RunStatus, graphql_name="status")
    workflow_version_id = sgqlc.types.Field(ID, graphql_name="workflowVersionId")


class RunEntityInputCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "new_entity_id", "field_name", "run_id")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    new_entity_id = sgqlc.types.Field(Int, graphql_name="newEntityId")
    field_name = sgqlc.types.Field(String, graphql_name="fieldName")
    run_id = sgqlc.types.Field(ID, graphql_name="runId")


class RunEntityInputUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "new_entity_id", "field_name", "run_id")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    new_entity_id = sgqlc.types.Field(Int, graphql_name="newEntityId")
    field_name = sgqlc.types.Field(String, graphql_name="fieldName")
    run_id = sgqlc.types.Field(ID, graphql_name="runId")


class RunEntityInputWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id", "producing_run_id", "owner_user_id", "collection_id", "new_entity_id", "field_name", "run")
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    new_entity_id = sgqlc.types.Field(IntComparators, graphql_name="newEntityId")
    field_name = sgqlc.types.Field("StrComparators", graphql_name="fieldName")
    run = sgqlc.types.Field("RunWhereClause", graphql_name="run")


class RunEntityInputWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")


class RunStatusEnumComparators(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("_eq", "_neq", "_in", "_nin", "_gt", "_gte", "_lt", "_lte", "_is_null")
    _eq = sgqlc.types.Field(RunStatus, graphql_name="_eq")
    _neq = sgqlc.types.Field(RunStatus, graphql_name="_neq")
    _in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(RunStatus)), graphql_name="_in")
    _nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(RunStatus)), graphql_name="_nin")
    _gt = sgqlc.types.Field(RunStatus, graphql_name="_gt")
    _gte = sgqlc.types.Field(RunStatus, graphql_name="_gte")
    _lt = sgqlc.types.Field(RunStatus, graphql_name="_lt")
    _lte = sgqlc.types.Field(RunStatus, graphql_name="_lte")
    _is_null = sgqlc.types.Field(RunStatus, graphql_name="_is_null")


class RunStepCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "run_id", "started_at", "ended_at", "status")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    run_id = sgqlc.types.Field(ID, graphql_name="runId")
    started_at = sgqlc.types.Field(DateTime, graphql_name="startedAt")
    ended_at = sgqlc.types.Field(DateTime, graphql_name="endedAt")
    status = sgqlc.types.Field(RunStatus, graphql_name="status")


class RunStepUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "run_id", "started_at", "ended_at", "status")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    run_id = sgqlc.types.Field(ID, graphql_name="runId")
    started_at = sgqlc.types.Field(DateTime, graphql_name="startedAt")
    ended_at = sgqlc.types.Field(DateTime, graphql_name="endedAt")
    status = sgqlc.types.Field(RunStatus, graphql_name="status")


class RunStepWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "run",
        "started_at",
        "ended_at",
        "status",
    )
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    run = sgqlc.types.Field("RunWhereClause", graphql_name="run")
    started_at = sgqlc.types.Field(DatetimeComparators, graphql_name="startedAt")
    ended_at = sgqlc.types.Field(DatetimeComparators, graphql_name="endedAt")
    status = sgqlc.types.Field(RunStatusEnumComparators, graphql_name="status")


class RunStepWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")


class RunUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "collection_id",
        "started_at",
        "ended_at",
        "execution_id",
        "outputs_json",
        "inputs_json",
        "status",
        "workflow_version_id",
    )
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    started_at = sgqlc.types.Field(DateTime, graphql_name="startedAt")
    ended_at = sgqlc.types.Field(DateTime, graphql_name="endedAt")
    execution_id = sgqlc.types.Field(String, graphql_name="executionId")
    outputs_json = sgqlc.types.Field(String, graphql_name="outputsJson")
    inputs_json = sgqlc.types.Field(String, graphql_name="inputsJson")
    status = sgqlc.types.Field(RunStatus, graphql_name="status")
    workflow_version_id = sgqlc.types.Field(ID, graphql_name="workflowVersionId")


class RunWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "started_at",
        "ended_at",
        "execution_id",
        "outputs_json",
        "inputs_json",
        "status",
        "workflow_version",
        "run_steps",
        "run_entity_inputs",
    )
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    started_at = sgqlc.types.Field(DatetimeComparators, graphql_name="startedAt")
    ended_at = sgqlc.types.Field(DatetimeComparators, graphql_name="endedAt")
    execution_id = sgqlc.types.Field("StrComparators", graphql_name="executionId")
    outputs_json = sgqlc.types.Field("StrComparators", graphql_name="outputsJson")
    inputs_json = sgqlc.types.Field("StrComparators", graphql_name="inputsJson")
    status = sgqlc.types.Field(RunStatusEnumComparators, graphql_name="status")
    workflow_version = sgqlc.types.Field("WorkflowVersionWhereClause", graphql_name="workflowVersion")
    run_steps = sgqlc.types.Field(RunStepWhereClause, graphql_name="runSteps")
    run_entity_inputs = sgqlc.types.Field(RunEntityInputWhereClause, graphql_name="runEntityInputs")


class RunWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field("UUIDComparators", graphql_name="id")


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
    __field_names__ = ("collection_id", "name", "default_version", "minimum_supported_version")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    name = sgqlc.types.Field(String, graphql_name="name")
    default_version = sgqlc.types.Field(String, graphql_name="defaultVersion")
    minimum_supported_version = sgqlc.types.Field(String, graphql_name="minimumSupportedVersion")


class WorkflowUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "name", "default_version", "minimum_supported_version")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    name = sgqlc.types.Field(String, graphql_name="name")
    default_version = sgqlc.types.Field(String, graphql_name="defaultVersion")
    minimum_supported_version = sgqlc.types.Field(String, graphql_name="minimumSupportedVersion")


class WorkflowVersionCreateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "graph_json", "workflow_uri", "version", "manifest", "workflow_id")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    graph_json = sgqlc.types.Field(String, graphql_name="graphJson")
    workflow_uri = sgqlc.types.Field(String, graphql_name="workflowUri")
    version = sgqlc.types.Field(String, graphql_name="version")
    manifest = sgqlc.types.Field(String, graphql_name="manifest")
    workflow_id = sgqlc.types.Field(ID, graphql_name="workflowId")


class WorkflowVersionUpdateInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("collection_id", "graph_json", "workflow_uri", "version", "manifest", "workflow_id")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    graph_json = sgqlc.types.Field(String, graphql_name="graphJson")
    workflow_uri = sgqlc.types.Field(String, graphql_name="workflowUri")
    version = sgqlc.types.Field(String, graphql_name="version")
    manifest = sgqlc.types.Field(String, graphql_name="manifest")
    workflow_id = sgqlc.types.Field(ID, graphql_name="workflowId")


class WorkflowVersionWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "graph_json",
        "workflow_uri",
        "version",
        "manifest",
        "workflow",
        "runs",
    )
    id = sgqlc.types.Field(UUIDComparators, graphql_name="id")
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    graph_json = sgqlc.types.Field(StrComparators, graphql_name="graphJson")
    workflow_uri = sgqlc.types.Field(StrComparators, graphql_name="workflowUri")
    version = sgqlc.types.Field(StrComparators, graphql_name="version")
    manifest = sgqlc.types.Field(StrComparators, graphql_name="manifest")
    workflow = sgqlc.types.Field("WorkflowWhereClause", graphql_name="workflow")
    runs = sgqlc.types.Field(RunWhereClause, graphql_name="runs")


class WorkflowVersionWhereClauseMutations(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(UUIDComparators, graphql_name="id")


class WorkflowWhereClause(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "name",
        "default_version",
        "minimum_supported_version",
        "versions",
    )
    id = sgqlc.types.Field(UUIDComparators, graphql_name="id")
    producing_run_id = sgqlc.types.Field(IntComparators, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(IntComparators, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(IntComparators, graphql_name="collectionId")
    name = sgqlc.types.Field(StrComparators, graphql_name="name")
    default_version = sgqlc.types.Field(StrComparators, graphql_name="defaultVersion")
    minimum_supported_version = sgqlc.types.Field(StrComparators, graphql_name="minimumSupportedVersion")
    versions = sgqlc.types.Field(WorkflowVersionWhereClause, graphql_name="versions")


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
        "create_run",
        "update_run",
        "delete_run",
        "create_workflow",
        "update_workflow",
        "delete_workflow",
        "create_run_step",
        "update_run_step",
        "delete_run_step",
        "create_run_entity_input",
        "update_run_entity_input",
        "delete_run_entity_input",
        "create_workflow_version",
        "update_workflow_version",
        "delete_workflow_version",
    )
    create_run = sgqlc.types.Field(
        sgqlc.types.non_null("Run"),
        graphql_name="createRun",
        args=sgqlc.types.ArgDict(
            (("input", sgqlc.types.Arg(sgqlc.types.non_null(RunCreateInput), graphql_name="input", default=None)),)
        ),
    )
    update_run = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Run"))),
        graphql_name="updateRun",
        args=sgqlc.types.ArgDict(
            (
                ("input", sgqlc.types.Arg(sgqlc.types.non_null(RunUpdateInput), graphql_name="input", default=None)),
                (
                    "where",
                    sgqlc.types.Arg(sgqlc.types.non_null(RunWhereClauseMutations), graphql_name="where", default=None),
                ),
            )
        ),
    )
    delete_run = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Run"))),
        graphql_name="deleteRun",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(sgqlc.types.non_null(RunWhereClauseMutations), graphql_name="where", default=None),
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
    create_run_step = sgqlc.types.Field(
        sgqlc.types.non_null("RunStep"),
        graphql_name="createRunStep",
        args=sgqlc.types.ArgDict(
            (("input", sgqlc.types.Arg(sgqlc.types.non_null(RunStepCreateInput), graphql_name="input", default=None)),)
        ),
    )
    update_run_step = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("RunStep"))),
        graphql_name="updateRunStep",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(sgqlc.types.non_null(RunStepUpdateInput), graphql_name="input", default=None),
                ),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(RunStepWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_run_step = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("RunStep"))),
        graphql_name="deleteRunStep",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(RunStepWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    create_run_entity_input = sgqlc.types.Field(
        sgqlc.types.non_null("RunEntityInput"),
        graphql_name="createRunEntityInput",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(RunEntityInputCreateInput), graphql_name="input", default=None
                    ),
                ),
            )
        ),
    )
    update_run_entity_input = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("RunEntityInput"))),
        graphql_name="updateRunEntityInput",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(RunEntityInputUpdateInput), graphql_name="input", default=None
                    ),
                ),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(RunEntityInputWhereClauseMutations), graphql_name="where", default=None
                    ),
                ),
            )
        ),
    )
    delete_run_entity_input = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("RunEntityInput"))),
        graphql_name="deleteRunEntityInput",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(RunEntityInputWhereClauseMutations), graphql_name="where", default=None
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
    update_workflow_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("WorkflowVersion"))),
        graphql_name="updateWorkflowVersion",
        args=sgqlc.types.ArgDict(
            (
                (
                    "input",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(WorkflowVersionUpdateInput), graphql_name="input", default=None
                    ),
                ),
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(WorkflowVersionWhereClauseMutations), graphql_name="where", default=None
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
        "runs",
        "workflows",
        "run_steps",
        "run_entity_inputs",
        "workflow_versions",
        "runs_aggregate",
        "workflows_aggregate",
        "run_steps_aggregate",
        "run_entity_inputs_aggregate",
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
    runs = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Run"))),
        graphql_name="runs",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(RunWhereClause, graphql_name="where", default=None)),)),
    )
    workflows = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Workflow"))),
        graphql_name="workflows",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(WorkflowWhereClause, graphql_name="where", default=None)),)
        ),
    )
    run_steps = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("RunStep"))),
        graphql_name="runSteps",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(RunStepWhereClause, graphql_name="where", default=None)),)),
    )
    run_entity_inputs = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("RunEntityInput"))),
        graphql_name="runEntityInputs",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(RunEntityInputWhereClause, graphql_name="where", default=None)),)
        ),
    )
    workflow_versions = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("WorkflowVersion"))),
        graphql_name="workflowVersions",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(WorkflowVersionWhereClause, graphql_name="where", default=None)),)
        ),
    )
    runs_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("RunAggregate"),
        graphql_name="runsAggregate",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(RunWhereClause, graphql_name="where", default=None)),)),
    )
    workflows_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("WorkflowAggregate"),
        graphql_name="workflowsAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(WorkflowWhereClause, graphql_name="where", default=None)),)
        ),
    )
    run_steps_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("RunStepAggregate"),
        graphql_name="runStepsAggregate",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(RunStepWhereClause, graphql_name="where", default=None)),)),
    )
    run_entity_inputs_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("RunEntityInputAggregate"),
        graphql_name="runEntityInputsAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(RunEntityInputWhereClause, graphql_name="where", default=None)),)
        ),
    )
    workflow_versions_aggregate = sgqlc.types.Field(
        sgqlc.types.non_null("WorkflowVersionAggregate"),
        graphql_name="workflowVersionsAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(WorkflowVersionWhereClause, graphql_name="where", default=None)),)
        ),
    )


class RunAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field("RunAggregateFunctions", graphql_name="aggregate")


class RunAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "min", "max", "stddev", "variance", "count")
    sum = sgqlc.types.Field("RunNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("RunNumericalColumns", graphql_name="avg")
    min = sgqlc.types.Field("RunMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("RunMinMaxColumns", graphql_name="max")
    stddev = sgqlc.types.Field("RunNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("RunNumericalColumns", graphql_name="variance")
    count = sgqlc.types.Field(
        Int,
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=False)),
                ("columns", sgqlc.types.Arg(RunCountColumns, graphql_name="columns", default=None)),
            )
        ),
    )


class RunConnection(sgqlc.types.relay.Connection):
    __schema__ = gql_schema
    __field_names__ = ("page_info", "edges")
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name="pageInfo")
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("RunEdge"))), graphql_name="edges"
    )


class RunEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("cursor", "node")
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="cursor")
    node = sgqlc.types.Field(sgqlc.types.non_null("Run"), graphql_name="node")


class RunEntityInputAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field("RunEntityInputAggregateFunctions", graphql_name="aggregate")


class RunEntityInputAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "min", "max", "stddev", "variance", "count")
    sum = sgqlc.types.Field("RunEntityInputNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("RunEntityInputNumericalColumns", graphql_name="avg")
    min = sgqlc.types.Field("RunEntityInputMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("RunEntityInputMinMaxColumns", graphql_name="max")
    stddev = sgqlc.types.Field("RunEntityInputNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("RunEntityInputNumericalColumns", graphql_name="variance")
    count = sgqlc.types.Field(
        Int,
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=False)),
                ("columns", sgqlc.types.Arg(RunEntityInputCountColumns, graphql_name="columns", default=None)),
            )
        ),
    )


class RunEntityInputConnection(sgqlc.types.relay.Connection):
    __schema__ = gql_schema
    __field_names__ = ("page_info", "edges")
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name="pageInfo")
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("RunEntityInputEdge"))), graphql_name="edges"
    )


class RunEntityInputEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("cursor", "node")
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="cursor")
    node = sgqlc.types.Field(sgqlc.types.non_null("RunEntityInput"), graphql_name="node")


class RunEntityInputMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id", "new_entity_id", "field_name")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    new_entity_id = sgqlc.types.Field(Int, graphql_name="newEntityId")
    field_name = sgqlc.types.Field(String, graphql_name="fieldName")


class RunEntityInputNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id", "new_entity_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    new_entity_id = sgqlc.types.Field(Int, graphql_name="newEntityId")


class RunMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "started_at",
        "ended_at",
        "execution_id",
        "outputs_json",
        "inputs_json",
    )
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    started_at = sgqlc.types.Field(DateTime, graphql_name="startedAt")
    ended_at = sgqlc.types.Field(DateTime, graphql_name="endedAt")
    execution_id = sgqlc.types.Field(String, graphql_name="executionId")
    outputs_json = sgqlc.types.Field(String, graphql_name="outputsJson")
    inputs_json = sgqlc.types.Field(String, graphql_name="inputsJson")


class RunNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class RunStepAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field("RunStepAggregateFunctions", graphql_name="aggregate")


class RunStepAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "min", "max", "stddev", "variance", "count")
    sum = sgqlc.types.Field("RunStepNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("RunStepNumericalColumns", graphql_name="avg")
    min = sgqlc.types.Field("RunStepMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("RunStepMinMaxColumns", graphql_name="max")
    stddev = sgqlc.types.Field("RunStepNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("RunStepNumericalColumns", graphql_name="variance")
    count = sgqlc.types.Field(
        Int,
        graphql_name="count",
        args=sgqlc.types.ArgDict(
            (
                ("distinct", sgqlc.types.Arg(Boolean, graphql_name="distinct", default=False)),
                ("columns", sgqlc.types.Arg(RunStepCountColumns, graphql_name="columns", default=None)),
            )
        ),
    )


class RunStepConnection(sgqlc.types.relay.Connection):
    __schema__ = gql_schema
    __field_names__ = ("page_info", "edges")
    page_info = sgqlc.types.Field(sgqlc.types.non_null(PageInfo), graphql_name="pageInfo")
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("RunStepEdge"))), graphql_name="edges"
    )


class RunStepEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("cursor", "node")
    cursor = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="cursor")
    node = sgqlc.types.Field(sgqlc.types.non_null("RunStep"), graphql_name="node")


class RunStepMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id", "started_at", "ended_at")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    started_at = sgqlc.types.Field(DateTime, graphql_name="startedAt")
    ended_at = sgqlc.types.Field(DateTime, graphql_name="endedAt")


class RunStepNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class WorkflowAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field("WorkflowAggregateFunctions", graphql_name="aggregate")


class WorkflowAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "min", "max", "stddev", "variance", "count")
    sum = sgqlc.types.Field("WorkflowNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("WorkflowNumericalColumns", graphql_name="avg")
    min = sgqlc.types.Field("WorkflowMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("WorkflowMinMaxColumns", graphql_name="max")
    stddev = sgqlc.types.Field("WorkflowNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("WorkflowNumericalColumns", graphql_name="variance")
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


class WorkflowMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "name",
        "default_version",
        "minimum_supported_version",
    )
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    name = sgqlc.types.Field(String, graphql_name="name")
    default_version = sgqlc.types.Field(String, graphql_name="defaultVersion")
    minimum_supported_version = sgqlc.types.Field(String, graphql_name="minimumSupportedVersion")


class WorkflowNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class WorkflowVersionAggregate(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("aggregate",)
    aggregate = sgqlc.types.Field("WorkflowVersionAggregateFunctions", graphql_name="aggregate")


class WorkflowVersionAggregateFunctions(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("sum", "avg", "min", "max", "stddev", "variance", "count")
    sum = sgqlc.types.Field("WorkflowVersionNumericalColumns", graphql_name="sum")
    avg = sgqlc.types.Field("WorkflowVersionNumericalColumns", graphql_name="avg")
    min = sgqlc.types.Field("WorkflowVersionMinMaxColumns", graphql_name="min")
    max = sgqlc.types.Field("WorkflowVersionMinMaxColumns", graphql_name="max")
    stddev = sgqlc.types.Field("WorkflowVersionNumericalColumns", graphql_name="stddev")
    variance = sgqlc.types.Field("WorkflowVersionNumericalColumns", graphql_name="variance")
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


class WorkflowVersionMinMaxColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "graph_json",
        "workflow_uri",
        "version",
        "manifest",
    )
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")
    graph_json = sgqlc.types.Field(String, graphql_name="graphJson")
    workflow_uri = sgqlc.types.Field(String, graphql_name="workflowUri")
    version = sgqlc.types.Field(String, graphql_name="version")
    manifest = sgqlc.types.Field(String, graphql_name="manifest")


class WorkflowVersionNumericalColumns(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("producing_run_id", "owner_user_id", "collection_id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(Int, graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(Int, graphql_name="collectionId")


class Run(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "started_at",
        "ended_at",
        "execution_id",
        "outputs_json",
        "inputs_json",
        "status",
        "workflow_version",
        "run_steps",
        "run_steps_aggregate",
        "run_entity_inputs",
        "run_entity_inputs_aggregate",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    started_at = sgqlc.types.Field(DateTime, graphql_name="startedAt")
    ended_at = sgqlc.types.Field(DateTime, graphql_name="endedAt")
    execution_id = sgqlc.types.Field(String, graphql_name="executionId")
    outputs_json = sgqlc.types.Field(String, graphql_name="outputsJson")
    inputs_json = sgqlc.types.Field(String, graphql_name="inputsJson")
    status = sgqlc.types.Field(RunStatus, graphql_name="status")
    workflow_version = sgqlc.types.Field(
        "WorkflowVersion",
        graphql_name="workflowVersion",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(WorkflowVersionWhereClause, graphql_name="where", default=None)),)
        ),
    )
    run_steps = sgqlc.types.Field(
        sgqlc.types.non_null(RunStepConnection),
        graphql_name="runSteps",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(RunStepWhereClause, graphql_name="where", default=None)),
                ("before", sgqlc.types.Arg(String, graphql_name="before", default=None)),
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
            )
        ),
    )
    run_steps_aggregate = sgqlc.types.Field(
        RunStepAggregate,
        graphql_name="runStepsAggregate",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(RunStepWhereClause, graphql_name="where", default=None)),)),
    )
    run_entity_inputs = sgqlc.types.Field(
        sgqlc.types.non_null(RunEntityInputConnection),
        graphql_name="runEntityInputs",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(RunEntityInputWhereClause, graphql_name="where", default=None)),
                ("before", sgqlc.types.Arg(String, graphql_name="before", default=None)),
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
            )
        ),
    )
    run_entity_inputs_aggregate = sgqlc.types.Field(
        RunEntityInputAggregate,
        graphql_name="runEntityInputsAggregate",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(RunEntityInputWhereClause, graphql_name="where", default=None)),)
        ),
    )


class RunEntityInput(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = ("id", "producing_run_id", "owner_user_id", "collection_id", "new_entity_id", "field_name", "run")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    new_entity_id = sgqlc.types.Field(Int, graphql_name="newEntityId")
    field_name = sgqlc.types.Field(String, graphql_name="fieldName")
    run = sgqlc.types.Field(
        Run,
        graphql_name="run",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(RunWhereClause, graphql_name="where", default=None)),)),
    )


class RunStep(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "run",
        "started_at",
        "ended_at",
        "status",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    run = sgqlc.types.Field(
        Run,
        graphql_name="run",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(RunWhereClause, graphql_name="where", default=None)),)),
    )
    started_at = sgqlc.types.Field(DateTime, graphql_name="startedAt")
    ended_at = sgqlc.types.Field(DateTime, graphql_name="endedAt")
    status = sgqlc.types.Field(RunStatus, graphql_name="status")


class Workflow(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "name",
        "default_version",
        "minimum_supported_version",
        "versions",
        "versions_aggregate",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    name = sgqlc.types.Field(String, graphql_name="name")
    default_version = sgqlc.types.Field(String, graphql_name="defaultVersion")
    minimum_supported_version = sgqlc.types.Field(String, graphql_name="minimumSupportedVersion")
    versions = sgqlc.types.Field(
        sgqlc.types.non_null(WorkflowVersionConnection),
        graphql_name="versions",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(WorkflowVersionWhereClause, graphql_name="where", default=None)),
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


class WorkflowVersion(sgqlc.types.Type, EntityInterface, Node):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "graph_json",
        "workflow_uri",
        "version",
        "manifest",
        "workflow",
        "runs",
        "runs_aggregate",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    graph_json = sgqlc.types.Field(String, graphql_name="graphJson")
    workflow_uri = sgqlc.types.Field(String, graphql_name="workflowUri")
    version = sgqlc.types.Field(String, graphql_name="version")
    manifest = sgqlc.types.Field(String, graphql_name="manifest")
    workflow = sgqlc.types.Field(
        Workflow,
        graphql_name="workflow",
        args=sgqlc.types.ArgDict(
            (("where", sgqlc.types.Arg(WorkflowWhereClause, graphql_name="where", default=None)),)
        ),
    )
    runs = sgqlc.types.Field(
        sgqlc.types.non_null(RunConnection),
        graphql_name="runs",
        args=sgqlc.types.ArgDict(
            (
                ("where", sgqlc.types.Arg(RunWhereClause, graphql_name="where", default=None)),
                ("before", sgqlc.types.Arg(String, graphql_name="before", default=None)),
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
            )
        ),
    )
    runs_aggregate = sgqlc.types.Field(
        RunAggregate,
        graphql_name="runsAggregate",
        args=sgqlc.types.ArgDict((("where", sgqlc.types.Arg(RunWhereClause, graphql_name="where", default=None)),)),
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
