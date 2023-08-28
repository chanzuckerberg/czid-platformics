from abc import ABC, abstractmethod
from typing import Callable, List, TypedDict, Literal, Optional, Coroutine, Any

class WorkflowStatusMessage(TypedDict):
    runner_id: str
    status: Literal["STARTED", "SUCCESS", "FAILURE"]
    outputs: Optional[dict]
    error: Optional[str]

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
    async def run_workflow(self, on_complete: Callable[[WorkflowStatusMessage], Coroutine[Any, Any, Any]], workflow_run_id: str, workflow_path: str, inputs: dict) -> str:
        raise NotImplementedError()
