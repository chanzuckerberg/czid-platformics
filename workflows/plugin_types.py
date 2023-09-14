from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Dict, List, Literal, Coroutine, Any

from entity_interface import Entity
from version import WorkflowInput, WorkflowOutput

@dataclass
class WorkflowStatusMessage:
    runner_id: str
    status: Literal["WORKFLOW_STARTED", "WORKFLOW_SUCCESS", "WORKFLOW_FAILURE"]

@dataclass
class WorkflowStartedMessage(WorkflowStatusMessage):
    status: Literal["WORKFLOW_STARTED"]

class WorkflowStepMessage(WorkflowStatusMessage):
    status: Literal["WORKFLOW_STARTED"] = "WORKFLOW_STARTED"
    task: str
    outputs: Dict[str, str]

    def __init__(self, runner_id: str, task: str, outputs: Dict[str, str]):
        self.runner_id = runner_id
        self.task = task
        self.outputs = outputs

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
    async def poll() -> List[WorkflowStatusMessage]:
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
    async def load(self, **kwargs: Dict[str, Entity]) -> WorkflowInput:
        """Processes workflow output specified by the type constraints in worrkflow_output_types and returns a list of lists of entities. The outer list represents the order the entities must be created in, while the inner lists can be created in parallel."""
        raise NotImplementedError()


class EntityOutputLoader(ABC):
    @abstractmethod
    # TODO: type specificity on workflow_outputs, convert values from str to a representation of workflow outputs
    async def load(self, workflow_outputs: Dict[str, str]) -> List[Entity]:
        """Processes workflow output specified by the type constraints in worrkflow_output_types and returns a list of lists of entities. The outer list represents the order the entities must be created in, while the inner lists can be created in parallel."""
        raise NotImplementedError()
