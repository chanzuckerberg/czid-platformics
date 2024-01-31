"""
Module to define basic plugin types
"""

from abc import ABC, abstractmethod
from gql import Client
from pydantic import BaseModel
from typing import Dict, List, Literal
from entity_interface import Entity

from manifest.manifest import EntityInput, RawInput

from mypy_boto3_s3 import S3Client

WorkflowStatus = Literal["WORKFLOW_STARTED", "WORKFLOW_SUCCESS", "WORKFLOW_FAILURE"]


class WorkflowStatusMessage(BaseModel):
    """Base status message"""

    runner_id: str


class WorkflowStartedMessage(WorkflowStatusMessage):
    status: Literal["WORKFLOW_STARTED"] = "WORKFLOW_STARTED"


class WorkflowSucceededMessage(WorkflowStatusMessage):
    status: Literal["WORKFLOW_SUCCESS"] = "WORKFLOW_SUCCESS"
    outputs: Dict[str, str] = {}


class WorkflowFailedMessage(WorkflowStatusMessage):
    status: Literal["WORKFLOW_FAILURE"] = "WORKFLOW_FAILURE"


def parse_workflow_status_message(obj: dict) -> WorkflowStatusMessage:
    status = obj["status"]
    if status == "WORKFLOW_STARTED":
        return WorkflowStartedMessage(**obj)
    elif status == "WORKFLOW_SUCCESS":
        return WorkflowSucceededMessage(**obj)
    elif status == "WORKFLOW_FAILURE":
        return WorkflowFailedMessage(**obj)
    else:
        raise Exception(f"Unknown workflow status: {status}")


class EventBus(ABC):
    """Abstract class that defines the Event Bus"""

    @abstractmethod
    async def send(self, message: WorkflowStatusMessage) -> None:
        """Send message"""
        pass

    @abstractmethod
    async def poll(self) -> List[WorkflowStatusMessage]:
        """Poll for new messages"""
        pass


class WorkflowRunner(ABC):
    """Abstract class that defines the WorkflowRunner plugins"""

    @abstractmethod
    def supported_workflow_types(self) -> List[str]:
        """Returns the supported workflow types, ie ["WDL"]"""
        raise NotImplementedError()

    @abstractmethod
    def description(self) -> str:
        """Returns a description of the workflow runner"""
        raise NotImplementedError()

    @abstractmethod
    async def run_workflow(self, event_bus: EventBus, workflow_path: str, inputs: dict) -> str:
        """Runs a workflow"""
        raise NotImplementedError()


class InputLoader:
    @abstractmethod
    async def load(self, entity_inputs: dict[str, EntityInput], raw_inputs: dict[str, RawInput]) -> dict[str, str]:
        """Processes workflow output specified by the type constraints in
        worrkflow_output_types and returns a list of lists of entities.
        The outer list represents the order the entities
        must be created in, while the inner lists can be created in parallel.
        """
        raise NotImplementedError()


class OutputLoader:
    entity_client: Client
    s3_client: S3Client

    def __init__(self, entity_client: Client, s3_client: S3Client):
        self.entity_client = entity_client
        self.s3_client = s3_client

    @abstractmethod
    async def load(self, entity_inputs: dict[str, EntityInput], raw_inputs: dict[str, RawInput]) -> List[Entity]:
        """Processes workflow output specified by the type constraints
        in workflow_output_types and returns a list of lists of entities.
        The outer list represents the order the entities must be created
        in, while the inner lists can be created in parallel.
        """
        raise NotImplementedError()
