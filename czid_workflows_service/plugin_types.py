from abc import ABC, abstractmethod
from typing import Callable, List, TypedDict, Literal, Optional, Coroutine, Any


class WorkflowStatusMessage(TypedDict):
    runner_id: str
    status: Literal["STARTED", "SUCCESS", "FAILURE"]
    outputs: Optional[dict]
    error: Optional[str]


class StatusQueue(ABC):
    @abstractmethod
    async def send_message(self, message: WorkflowStatusMessage):
        raise NotImplementedError()

    @abstractmethod
    async def poll(self) -> List[WorkflowStatusMessage]:
        raise NotImplementedError()


class WorkflowRunner(ABC):
    @abstractmethod
    async def run_workflow(self, on_complete: Callable[[WorkflowStatusMessage], Coroutine[Any, Any, Any]], workflow_run_id: str, workflow_path: str, inputs: dict) -> str:
        raise NotImplementedError()

