from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Dict, Generic, List, Literal, Any, TypeVar
from database.models.workflow import Run
from entity_interface import Entity

WorkflowStatus = Literal["WORKFLOW_STARTED", "WORKFLOW_SUCCESS", "WORKFLOW_FAILURE"]


class WorkflowStatusMessage(BaseModel):
    runner_id: str
    status: WorkflowStatus


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
    async def run_workflow(self, event_bus: EventBus, workflow_path: str, inputs: dict) -> str:
        raise NotImplementedError()


Primitive = str | int | float | bool | None

class EntityInputLoader(ABC):
    @abstractmethod
    async def load(self, workflow_run: Run, entity_inputs: dict[str, Entity], raw_inputs: dict[str, Primitive]) -> dict[str, Primitive]:
        """Processes workflow output specified by the type constraints in
        worrkflow_output_types and returns a list of lists of entities.
        The outer list represents the order the entities
        must be created in, while the inner lists can be created in parallel.
        """
        raise NotImplementedError()


class EntityOutputLoader(ABC):
    @abstractmethod
    async def load(self, workflow_run: Run, entity_inputs: dict[str, Entity], raw_inputs: dict[str, Primitive], workflow_outputs: dict[str, Primitive]) -> list[Entity]:
        """Processes workflow output specified by the type constraints
        in worrkflow_output_types and returns a list of lists of entities.
        The outer list represents the order the entities must be created
        in, while the inner lists can be created in parallel.
        """
        raise NotImplementedError()
