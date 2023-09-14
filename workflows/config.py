from importlib.metadata import entry_points
from typing import Dict
from plugin_types import EventBus, WorkflowRunner


def load_workflow_runners() -> Dict[str, WorkflowRunner]:
    workflow_runners_by_name: Dict[str, WorkflowRunner] = {}
    for plugin in entry_points(group="czid.plugin.workflow_runner"):
        workflow_runner = plugin.load()()
        assert isinstance(workflow_runner, WorkflowRunner)
        workflow_runners_by_name[plugin.name] = workflow_runner
    return workflow_runners_by_name

def load_event_buses() -> Dict[str, EventBus]:
    event_buses_by_name: Dict[str, EventBus] = {}
    for plugin in entry_points(group="czid.plugin.event_bus"):
        event_bus = plugin.load()()
        assert isinstance(event_bus, EventBus)
        event_buses_by_name[plugin.name] = event_bus
    return event_buses_by_name
