"""
Module to define basic plugin types
"""

import boto3
import logging
import os
from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Any, Literal, TypedDict
from urllib.parse import urlparse

from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation

from database.models import WorkflowVersion, WorkflowRun
from manifest.manifest import EntityInput
from platformics.api.core.errors import PlatformicsException
from platformics.client.entities_schema import FileAccessProtocol
from platformics.util.types_utils import JSONValue

from mypy_boto3_s3 import S3Client

ENTITY_SERVICE_URL = os.environ["ENTITY_SERVICE_URL"]

WorkflowStatus = Literal["WORKFLOW_STARTED", "WORKFLOW_SUCCESS", "WORKFLOW_FAILURE"]


class WorkflowStatusMessage(BaseModel):
    """Base status message"""

    runner_id: str


class WorkflowStartedMessage(WorkflowStatusMessage):
    status: Literal["WORKFLOW_STARTED"] = "WORKFLOW_STARTED"


class WorkflowSucceededMessage(WorkflowStatusMessage):
    status: Literal["WORKFLOW_SUCCESS"] = "WORKFLOW_SUCCESS"
    outputs: dict[str, JSONValue] = {}


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
    async def poll(self) -> list[WorkflowStatusMessage]:
        """Poll for new messages"""
        pass


class WorkflowRunner(ABC):
    """Abstract class that defines the WorkflowRunner plugins"""

    @abstractmethod
    def supported_workflow_types(self) -> list[str]:
        """Returns the supported workflow types, ie ["WDL"]"""
        raise NotImplementedError()

    @abstractmethod
    def description(self) -> str:
        """Returns a description of the workflow runner"""
        raise NotImplementedError()

    @abstractmethod
    async def run_workflow(self, event_bus: EventBus, workflow_path: str, inputs: dict[str, JSONValue]) -> str:
        """Runs a workflow"""
        raise NotImplementedError()


class IOLoader:
    _entitties_endpoint: HTTPEndpoint
    _s3_client: S3Client
    _user_token: str

    def _fetch_file(self, gql_file: Any) -> None:
        gql_file.protocol()
        gql_file.namespace()
        gql_file.path()

    def _uri_file(self, file_result: Any) -> str | None:
        if not file_result:
            return None
        return f"{file_result['protocol']}://{file_result['namespace']}/{file_result['path']}"

    def __init__(self, user_token: str) -> None:
        self.entities_endpoint = HTTPEndpoint(ENTITY_SERVICE_URL + "/graphql")
        self._s3_client = boto3.client("s3", endpoint_url=os.getenv("BOTO3_ENDPOINT_URL"))
        self._user_token = user_token
        self.logger = logging.getLogger("IOLoader")

    def _entities_gql(self, op: Operation) -> dict:
        headers = {"Authorization": f"Bearer {self._user_token}"}
        resp = self.entities_endpoint(op, extra_headers=headers)
        if resp.get("errors"):
            self.logger.error(f"Error fetching entities: {resp['errors']}")
            raise PlatformicsException("Internal error")
        return resp["data"]


class InputLoader(IOLoader):
    entities_endpoint: HTTPEndpoint

    @abstractmethod
    async def load(
        self,
        workflow_version: WorkflowVersion,
        entity_inputs: dict[str, EntityInput],
        raw_inputs: dict[str, JSONValue],
        requested_outputs: list[str] = [],
    ) -> dict[str, JSONValue]:
        """Processes workflow output specified by the type constraints in
        worrkflow_output_types and returns a list of lists of entities.
        The outer list represents the order the entities
        must be created in, while the inner lists can be created in parallel.
        """
        raise NotImplementedError()


class ParsedURI(TypedDict):
    protocol: FileAccessProtocol
    namespace: str
    path: str


class OutputLoader(IOLoader):
    def _parse_uri(self, uri: str) -> ParsedURI:
        parsed = urlparse(uri)
        return {
            "protocol": getattr(FileAccessProtocol, parsed.scheme),
            "namespace": parsed.netloc,
            "path": parsed.path.lstrip("/"),
        }

    def _s3_object_data(self, path: str):
        parsed = self._parse_uri(path)
        return self._s3_client.get_object(Bucket=parsed["namespace"], Key=parsed["path"]).read()

    @abstractmethod
    async def load(
        self,
        workflow_run: WorkflowRun,
        entity_inputs: dict[str, EntityInput],
        raw_inputs: dict[str, JSONValue],
        workflow_outputs: dict[str, JSONValue],
    ) -> None:
        """Processes workflow output specified by the type constraints
        in workflow_output_types and returns a list of lists of entities.
        The outer list represents the order the entities must be created
        in, while the inner lists can be created in parallel.
        """
        raise NotImplementedError()
