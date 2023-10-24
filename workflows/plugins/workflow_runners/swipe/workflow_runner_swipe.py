import json
from typing import Callable, Coroutine, Any, List, Optional
from uuid import uuid4
import boto3
import os
from datetime import datetime

from plugin_types import WorkflowRunner, WorkflowStatusMessage

# TODO: maybe split out these decisions into another module, or a YAML file??
if os.environ.get("ENVIRONMENT", None) == "test":
    sfn = boto3.client("stepfunctions", endpoint_url="http://sfn.czidnet:8083")
    sts = boto3.client("sts", endpoint_url="http://motoserver.czidnet:4000")
    REGION = "us-east-1"
    SFN_NAME = "swipe-test-default-wdl"
else:
    sfn = boto3.client("stepfunctions")
    sts = boto3.client("sts")
    REGION = "us-west-2"
    SFN_NAME = "idseq-swipe-dev-default-wdl"


class SwipeWorkflowRunner(WorkflowRunner):
    """Runs the submitted inputs on the infrastucture
    generated by SWIPE
    """

    def __init__(self, output_path: Optional[str] = None):
        # TODO: remove this
        self.output_path = output_path or "s3://idseq-samples-development/rlim-test/test-nxtg/"

    def supported_workflow_types(self) -> List[str]:
        """Returns the supported workflow types"""
        return ["WDL"]

    def description(self) -> str:
        """Returns a description of the workflow runner"""
        return "Runs WDL workflows on SWIPE infrastructure, using AWS Step Functions and Batch"

    def get_account_id(self) -> str:
        """Returns the account id"""
        return sts.get_caller_identity()["Account"]

    def workflow_name(self) -> str:
        """Creates the workflow name"""
        return f"workflows-test-execution-rlim-{datetime.now().strftime('%d-%m-%Y-%H%M%S')}"

    def execution_id(self) -> str:
        """Returns the state machine name to run. Modify SFN_NAME to change"""
        return f"arn:aws:states:{REGION}:{self.get_account_id()}:stateMachine:{SFN_NAME}"

    def start_execution(self, inputs_json: dict) -> dict:
        """Kicks off Step Function"""
        return sfn.start_execution(
            stateMachineArn=self.execution_id(),
            name=self.workflow_name(),
            input=json.dumps(inputs_json),
        )

    def format_inputs_json(self, workflow_path: str, inputs: dict) -> dict:
        """Create the inputs dict in the structure that SWIPE expects"""
        return {
            "RUN_WDL_URI": workflow_path,
            "Input": {"Run": inputs},
            "OutputPrefix": self.output_path,
        }

    # FIXME: error: Return type "str" of "run_workflow" incompatible with return type "Coroutine[Any, Any, str]" in
    # supertype "WorkflowRunner"
    # FIXME: error: Argument 1 of "run_workflow" is incompatible with supertype "WorkflowRunner"; supertype defines
    # the argument type as "EventBus"
    def run_workflow(  # type: ignore
        self,
        on_complete: Callable[[WorkflowStatusMessage], Coroutine[Any, Any, Any]],  # type: ignore
        workflow_run_id: str,
        workflow_path: str,
        inputs: dict,
    ) -> str:
        """Formats the inputs into SWIPE format and kicks off the SFN execution

        :param on_complete: Fill in
        :param workflow_run_id: Fill in
        :param workflow_path: Fill in
        :param inputs: Fill in

        """
        runner_id = str(uuid4())
        inputs_json = self.format_inputs_json(workflow_path=workflow_path, inputs=inputs)
        exc_response = self.start_execution(inputs_json=inputs_json)
        return json.dumps(
            {
                "runner_id": runner_id,
                "response": exc_response,
            },
            sort_keys=True,
            default=str,
        )
