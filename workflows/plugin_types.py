from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Literal, Any


@dataclass
class WorkflowStatusMessage:
    runner_id: str
    status: Literal["WORKFLOW_STARTED", "WORKFLOW_SUCCESS", "WORKFLOW_FAILURE"]


@dataclass
class WorkflowStartedMessage(WorkflowStatusMessage):
    status: Literal["WORKFLOW_STARTED"]


class WorkflowSucceededMessage(WorkflowStatusMessage):
    status: Literal["WORKFLOW_SUCCESS"] = "WORKFLOW_SUCCESS"
    outputs: Dict[str, str]

    def __init__(self, runner_id: str, outputs: Dict[str, str]):
        self.runner_id = runner_id
        self.outputs = outputs


@dataclass
class WorkflowFailedMessage(WorkflowStatusMessage):
    status: Literal["WORKFLOW_FAILURE"]


class EventBus(ABC):
    @abstractmethod
    async def send(self, message: WorkflowStatusMessage) -> None:
        pass

    @abstractmethod
    async def poll(self) -> List[WorkflowStatusMessage]:
        pass


class WorkflowRunner(ABC):
    @abstractmethod
    def supported_workflow_types(self) -> List[str]:
        """Returns the supported workflow types, ie ["WDL"]"""
        raise NotImplementedError()

    @abstractmethod
    def description(self) -> str:
        """Returns a description of the workflow runner"""
        raise NotImplementedError()

    @abstractmethod
    async def run_workflow(self, event_bus: EventBus, workflow_run_id: str, workflow_path: str, inputs: dict) -> str:
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
        in worrkflow_output_types and returns a list of lists of entities.
        The outer list represents the order the entities must be created
        in, while the inner lists can be created in parallel.
        """
        raise NotImplementedError()
