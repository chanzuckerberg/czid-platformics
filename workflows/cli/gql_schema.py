import sgqlc.types
import sgqlc.types.datetime


gql_schema = sgqlc.types.Schema()


########################################################################
# Scalars and Enumerations
########################################################################
Boolean = sgqlc.types.Boolean

DateTime = sgqlc.types.datetime.DateTime

Int = sgqlc.types.Int


class RunStatus(sgqlc.types.Enum):
    __schema__ = gql_schema
    __choices__ = ("FAILED", "PENDING", "RUNNING", "STARTED", "SUCCEEDED")


String = sgqlc.types.String


class UUID(sgqlc.types.Scalar):
    __schema__ = gql_schema


########################################################################
# Input Objects
########################################################################
class WorkflowInput(sgqlc.types.Input):
    __schema__ = gql_schema
    __field_names__ = ("name", "value")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="value")


########################################################################
# Output Objects and Interfaces
########################################################################
class Mutation(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "add_workflow",
        "add_workflow_version",
        "add_run",
        "create_run",
        "add_run_step",
        "add_run_entity_input",
    )
    add_workflow = sgqlc.types.Field(
        sgqlc.types.non_null("Workflow"),
        graphql_name="addWorkflow",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                (
                    "default_version",
                    sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="defaultVersion", default=None),
                ),
                (
                    "minimum_supported_version",
                    sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="minimumSupportedVersion", default=None),
                ),
            )
        ),
    )
    add_workflow_version = sgqlc.types.Field(
        sgqlc.types.non_null("WorkflowVersion"),
        graphql_name="addWorkflowVersion",
        args=sgqlc.types.ArgDict(
            (
                ("workflow_id", sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="workflowId", default=None)),
                ("version", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="version", default=None)),
                ("type", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="type", default=None)),
                ("package_uri", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="packageUri", default=None)),
                ("beta", sgqlc.types.Arg(sgqlc.types.non_null(Boolean), graphql_name="beta", default=None)),
                ("deprecated", sgqlc.types.Arg(sgqlc.types.non_null(Boolean), graphql_name="deprecated", default=None)),
                ("graph_json", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="graphJson", default=None)),
            )
        ),
    )
    add_run = sgqlc.types.Field(
        sgqlc.types.non_null("Run"),
        graphql_name="addRun",
        args=sgqlc.types.ArgDict(
            (
                (
                    "workflow_version_id",
                    sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="workflowVersionId", default=None),
                ),
                (
                    "workflow_inputs",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(WorkflowInput))),
                        graphql_name="workflowInputs",
                        default=None,
                    ),
                ),
                (
                    "workflow_runner",
                    sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="workflowRunner", default=None),
                ),
            )
        ),
    )
    create_run = sgqlc.types.Field(
        sgqlc.types.non_null("Run"),
        graphql_name="createRun",
        args=sgqlc.types.ArgDict(
            (
                ("project_id", sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="projectId", default=None)),
                (
                    "workflow_version_id",
                    sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="workflowVersionId", default=None),
                ),
                (
                    "workflow_inputs",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(WorkflowInput))),
                        graphql_name="workflowInputs",
                        default=None,
                    ),
                ),
                (
                    "workflow_runner",
                    sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="workflowRunner", default=None),
                ),
            )
        ),
    )
    add_run_step = sgqlc.types.Field(
        sgqlc.types.non_null("RunStep"),
        graphql_name="addRunStep",
        args=sgqlc.types.ArgDict(
            (
                ("run_id", sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="runId", default=None)),
                ("step_name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="stepName", default=None)),
                ("status", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="status", default=None)),
                ("start_time", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="startTime", default=None)),
                ("end_time", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="endTime", default=None)),
            )
        ),
    )
    add_run_entity_input = sgqlc.types.Field(
        sgqlc.types.non_null("RunEntityInput"),
        graphql_name="addRunEntityInput",
        args=sgqlc.types.ArgDict(
            (
                ("run_id", sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="runId", default=None)),
                (
                    "workflow_version_input_id",
                    sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="workflowVersionInputId", default=None),
                ),
                ("entity_id", sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="entityId", default=None)),
            )
        ),
    )


class Query(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "workflows",
        "runs",
        "workflow_versions",
        "run_steps",
        "run_entity_inputs",
        "get_workflow_runners",
    )
    workflows = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Workflow"))),
        graphql_name="workflows",
        args=sgqlc.types.ArgDict((("id", sgqlc.types.Arg(UUID, graphql_name="id", default=None)),)),
    )
    runs = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Run"))),
        graphql_name="runs",
        args=sgqlc.types.ArgDict((("id", sgqlc.types.Arg(UUID, graphql_name="id", default=None)),)),
    )
    workflow_versions = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("WorkflowVersion"))),
        graphql_name="workflowVersions",
        args=sgqlc.types.ArgDict((("id", sgqlc.types.Arg(UUID, graphql_name="id", default=None)),)),
    )
    run_steps = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("RunStep"))),
        graphql_name="runSteps",
        args=sgqlc.types.ArgDict((("id", sgqlc.types.Arg(UUID, graphql_name="id", default=None)),)),
    )
    run_entity_inputs = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("RunEntityInput"))),
        graphql_name="runEntityInputs",
        args=sgqlc.types.ArgDict((("id", sgqlc.types.Arg(UUID, graphql_name="id", default=None)),)),
    )
    get_workflow_runners = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("WorkflowRunner"))),
        graphql_name="getWorkflowRunners",
    )


class Run(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "type",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "user_id",
        "project_id",
        "started_at",
        "ended_at",
        "execution_id",
        "outputs_json",
        "inputs_json",
        "status",
        "workflow_version_id",
        "entity_id",
        "workflow_version",
        "run_steps",
        "run_entity_inputs",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="id")
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="type")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    user_id = sgqlc.types.Field(Int, graphql_name="userId")
    project_id = sgqlc.types.Field(Int, graphql_name="projectId")
    started_at = sgqlc.types.Field(DateTime, graphql_name="startedAt")
    ended_at = sgqlc.types.Field(DateTime, graphql_name="endedAt")
    execution_id = sgqlc.types.Field(String, graphql_name="executionId")
    outputs_json = sgqlc.types.Field(String, graphql_name="outputsJson")
    inputs_json = sgqlc.types.Field(String, graphql_name="inputsJson")
    status = sgqlc.types.Field(RunStatus, graphql_name="status")
    workflow_version_id = sgqlc.types.Field(UUID, graphql_name="workflowVersionId")
    entity_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="entityId")
    workflow_version = sgqlc.types.Field("WorkflowVersion", graphql_name="workflowVersion")
    run_steps = sgqlc.types.Field(sgqlc.types.non_null("RunStepConnection"), graphql_name="runSteps")
    run_entity_inputs = sgqlc.types.Field(
        sgqlc.types.non_null("RunEntityInputConnection"), graphql_name="runEntityInputs"
    )


class RunConnection(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("edges",)
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("RunEdge"))), graphql_name="edges"
    )


class RunEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("node",)
    node = sgqlc.types.Field(sgqlc.types.non_null(Run), graphql_name="node")


class RunEntityInput(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "type",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "new_entity_id",
        "field_name",
        "run_id",
        "entity_id",
        "run",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="id")
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="type")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    new_entity_id = sgqlc.types.Field(Int, graphql_name="newEntityId")
    field_name = sgqlc.types.Field(String, graphql_name="fieldName")
    run_id = sgqlc.types.Field(UUID, graphql_name="runId")
    entity_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="entityId")
    run = sgqlc.types.Field(Run, graphql_name="run")


class RunEntityInputConnection(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("edges",)
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("RunEntityInputEdge"))), graphql_name="edges"
    )


class RunEntityInputEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("node",)
    node = sgqlc.types.Field(sgqlc.types.non_null(RunEntityInput), graphql_name="node")


class RunStep(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "type",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "run_id",
        "started_at",
        "ended_at",
        "status",
        "entity_id",
        "run",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="id")
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="type")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    run_id = sgqlc.types.Field(UUID, graphql_name="runId")
    started_at = sgqlc.types.Field(DateTime, graphql_name="startedAt")
    ended_at = sgqlc.types.Field(DateTime, graphql_name="endedAt")
    status = sgqlc.types.Field(RunStatus, graphql_name="status")
    entity_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="entityId")
    run = sgqlc.types.Field(Run, graphql_name="run")


class RunStepConnection(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("edges",)
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("RunStepEdge"))), graphql_name="edges"
    )


class RunStepEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("node",)
    node = sgqlc.types.Field(sgqlc.types.non_null(RunStep), graphql_name="node")


class Workflow(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "type",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "name",
        "default_version",
        "minimum_supported_version",
        "entity_id",
        "versions",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="id")
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="type")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    name = sgqlc.types.Field(String, graphql_name="name")
    default_version = sgqlc.types.Field(String, graphql_name="defaultVersion")
    minimum_supported_version = sgqlc.types.Field(String, graphql_name="minimumSupportedVersion")
    entity_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="entityId")
    versions = sgqlc.types.Field(sgqlc.types.non_null("WorkflowVersionConnection"), graphql_name="versions")


class WorkflowRunner(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("name", "supported_workflow_types", "description")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")
    supported_workflow_types = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name="supportedWorkflowTypes"
    )
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="description")


class WorkflowVersion(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = (
        "id",
        "type",
        "producing_run_id",
        "owner_user_id",
        "collection_id",
        "graph_json",
        "workflow_id",
        "manifest",
        "entity_id",
        "workflow",
        "runs",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="id")
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="type")
    producing_run_id = sgqlc.types.Field(Int, graphql_name="producingRunId")
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ownerUserId")
    collection_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="collectionId")
    graph_json = sgqlc.types.Field(String, graphql_name="graphJson")
    workflow_id = sgqlc.types.Field(UUID, graphql_name="workflowId")
    manifest = sgqlc.types.Field(String, graphql_name="manifest")
    entity_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name="entityId")
    workflow = sgqlc.types.Field(Workflow, graphql_name="workflow")
    runs = sgqlc.types.Field(sgqlc.types.non_null(RunConnection), graphql_name="runs")


class WorkflowVersionConnection(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("edges",)
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("WorkflowVersionEdge"))), graphql_name="edges"
    )


class WorkflowVersionEdge(sgqlc.types.Type):
    __schema__ = gql_schema
    __field_names__ = ("node",)
    node = sgqlc.types.Field(sgqlc.types.non_null(WorkflowVersion), graphql_name="node")


########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
gql_schema.query_type = Query
gql_schema.mutation_type = Mutation
gql_schema.subscription_type = None
