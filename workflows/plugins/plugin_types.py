"""
Module to define basic plugin types
"""

from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Dict, List, Literal, Any

WorkflowStatus = Literal["WORKFLOW_STARTED", "WORKFLOW_SUCCESS", "WORKFLOW_FAILURE"]


class WorkflowStatusMessage(BaseModel):
    """Base status message"""
    runner_id: str
    status: WorkflowStatus


class WorkflowStartedMessage(WorkflowStatusMessage):
    status: Literal["WORKFLOW_STARTED"] = "WORKFLOW_STARTED"


class WorkflowSucceededMessage(WorkflowStatusMessage):
    status: Literal["WORKFLOW_SUCCESS"] = "WORKFLOW_SUCCESS"
    outputs: Dict[str, str] = {}


class WorkflowFailedMessage(WorkflowStatusMessage):
    status: Literal["WORKFLOW_FAILURE"] = "WORKFLOW_FAILURE"


def parse_workflow_status_message(obj: dict[str, str]) -> WorkflowStatusMessage:
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
    """Abstract class that defines the Event Bus""""
    @abstractmethod
    async def send(self, message: WorkflowStatusMessage) -> None:
        """ Send message """
        pass

    @abstractmethod
    async def poll(self) -> List[WorkflowStatusMessage]:
        """ Poll for new messages """
        pass


class WorkflowRunner(ABC):
    """ Abstract class that defines the WorkflowRunner plugins """
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


class EntityInputLoader(ABC):
    @abstractmethod
    async def load(self, args: Any) -> List[List[Any]]:
        """Processes workflow output specified by the type constraints in
        worrkflow_output_types and returns a list of lists of entities.
        The outer list represents the order the entities
        must be created in, while the inner lists can be created in parallel.
        """
        raise NotImplementedError()


class EntityOutputLoader(ABC):
    @abstractmethod
    # TODO: type specificity on workflow_outputs, convert values from str to a representation of workflow outputs
    async def load(self, args: Any) -> List[Any]:
        """Processes workflow output specified by the type constraints
        in workflow_output_types and returns a list of lists of entities.
        The outer list represents the order the entities must be created
        in, while the inner lists can be created in parallel.
        """
        raise NotImplementedError()
