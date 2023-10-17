from abc import ABC, abstractmethod
from typing import Dict, List, Literal, Any

WorkflowStatus = Literal["WORKFLOW_STARTED", "WORKFLOW_SUCCESS", "WORKFLOW_FAILURE"]

class WorkflowStatusMessage(ABC):
    runner_id: str
    status: WorkflowStatus

    def __init__(self, runner_id: str, status: WorkflowStatus):
        self.runner_id = runner_id
        self.status = status

    @abstractmethod
    def asdict(self) -> dict:
        return {
            "runner_id": self.runner_id,
            "status": self.status
        }


class WorkflowStartedMessage(WorkflowStatusMessage):
    status: Literal["WORKFLOW_STARTED"]

    def __init__(self, runner_id: str):
        super().__init__(runner_id, "WORKFLOW_STARTED")

    def asdict(self) -> dict:
        return super().asdict()


class WorkflowSucceededMessage(WorkflowStatusMessage):
    status: Literal["WORKFLOW_SUCCESS"]
    outputs: Dict[str, str]

    def __init__(self, runner_id: str, outputs: Dict[str, str]):
        super().__init__(runner_id, "WORKFLOW_SUCCESS")
        self.outputs = outputs

    def asdict(self) -> dict:
        d = super().asdict()
        d["outputs"] = self.outputs
        return d


class WorkflowFailedMessage(WorkflowStatusMessage):
    status: Literal["WORKFLOW_FAILURE"]

    def __init__(self, runner_id: str):
        super().__init__(runner_id, "WORKFLOW_FAILURE")

    def asdict(self) -> dict:
        return super().asdict()


def parse_workflow_status_message(obj: dict) -> WorkflowStatusMessage:
    status = obj["status"]
    del obj["status"]
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

