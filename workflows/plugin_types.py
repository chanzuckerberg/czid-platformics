from abc import ABC, abstractmethod
from typing import Callable, List, NamedTuple, TypedDict, Literal, Optional, Coroutine, Any

from semver import Version

from entity_interface import Entity


class WorkflowStartedMessage(TypedDict):
    runner_id: str
    status: Literal["WORKFLOW_STARTED"]


class WorkflowSucceededMessage(TypedDict):
    runner_id: str
    status: Literal["WORKFLOW_SUCCESS"]


class WorkflowFailedMessage(TypedDict):
    runner_id: str
    status: Literal["WORKFLOW_FAILURE"]


WorkflowStatusMessage = WorkflowStartedMessage | WorkflowSucceededMessage | WorkflowFailedMessage


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
    async def run_workflow(
        self,
        on_complete: Callable[[WorkflowStatusMessage], Coroutine[Any, Any, Any]],
        workflow_run_id: str,
        workflow_path: str,
        inputs: dict,
    ) -> str:
        raise NotImplementedError()


class EventListener:
    @abstractmethod
    async def send(message: WorkflowStatusMessage) -> None:
        pass

    @abstractmethod
    async def poll() -> List[WorkflowStatusMessage]:
        pass


class LoaderInput(NamedTuple):
    output_or_type: Literal["output", "type"]
    name: str
    version: Version


class LoaderInputConstraint(NamedTuple):
    output_or_type: Literal["output", "type"]
    name: str
    min_version: Optional[Version]
    max_version: Optional[Version]


class Loader(ABC):
    @abstractmethod
    def constraints(self) -> List[LoaderInputConstraint]:
        raise NotImplementedError()

    def satisfies(self, inputs: List[LoaderInput]) -> bool:
        if len(inputs) != len(self.constraints()):
            return False

        for input, constraint in zip(inputs, self.constraints()):
            if input.output_or_type != constraint.output_or_type:
                return False
            if input.name != constraint.name:
                return False
            if constraint.min_version is not None and input.version < constraint.min_version:
                return False
            if constraint.max_version is not None and input.version > constraint.max_version:
                return False

        return True

    @abstractmethod
    async def load(self, *args) -> List[List[Entity]]:
        """Processes workflow output specified by the type constraints in worrkflow_output_types and returns a list of lists of entities. The outer list represents the order the entities must be created in, while the inner lists can be created in parallel."""
        raise NotImplementedError()
