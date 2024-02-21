from cli.gql_schema import Mutation, RunWorkflowVersionInput

from sgqlc.operation import Operation

op = Operation(Mutation)
op.run_workflow(
    input=RunWorkflowVersionInput(
        workflow_version_id="workflow-version-id",
    )
)
