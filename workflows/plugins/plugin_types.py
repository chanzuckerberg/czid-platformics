"""
Module to define basic plugin types
"""

import os
from abc import ABC, abstractmethod
import typing
from pydantic import BaseModel
from typing import Dict, List, Literal

from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation

from database.models import WorkflowVersion, WorkflowRun
from manifest.manifest import EntityInput

from mypy_boto3_s3 import S3Client

ENTITY_SERVICE_URL = os.environ["ENTITY_SERVICE_URL"]
ENTITY_SERVICE_AUTH_TOKEN = os.environ["ENTITY_SERVICE_AUTH_TOKEN"]

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


class IOLoader:
    _entitties_endpoint: HTTPEndpoint
    _s3_client: S3Client

    def __init__(self) -> None:
        self.entities_endpoint = HTTPEndpoint(ENTITY_SERVICE_URL + "/graphql")

    def _entities_gql(self, op: Operation) -> dict:
        # TODO: dynamically fetch token
        headers = {"Authorization": f"Bearer {ENTITY_SERVICE_AUTH_TOKEN}"}
        return self.entities_endpoint(op, extra_headers=headers)


class InputLoader(IOLoader):
    entities_endpoint: HTTPEndpoint

    @abstractmethod
    async def load(
        self,
        workflow_version: WorkflowVersion,
        entity_inputs: dict[str, EntityInput],
        raw_inputs: dict[str, typing.Any],
        requested_outputs: list[str] = [],
    ) -> dict[str, str]:
        """Processes workflow output specified by the type constraints in
        worrkflow_output_types and returns a list of lists of entities.
        The outer list represents the order the entities
        must be created in, while the inner lists can be created in parallel.
        """
        raise NotImplementedError()


class OutputLoader(IOLoader):
    @abstractmethod
    async def load(
        self,
        workflow_run: WorkflowRun,
        entity_inputs: dict[str, EntityInput],
        raw_inputs: dict[str, typing.Any],
        workflow_outputs: dict[str, str],
    ) -> None:
        """Processes workflow output specified by the type constraints
        in workflow_output_types and returns a list of lists of entities.
        The outer list represents the order the entities must be created
        in, while the inner lists can be created in parallel.
        """
        raise NotImplementedError()
