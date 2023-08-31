from importlib.metadata import entry_points
from typing import Dict
from plugin_types import WorkflowRunner


def load_workflow_runners() -> Dict[str, WorkflowRunner]:
    workflow_runners_by_name: Dict[str, WorkflowRunner] = {}
    for plugin in entry_points(group="czid.plugin.workflow_runner"):
        workflow_runner = plugin.load()()
        assert isinstance(workflow_runner, WorkflowRunner)
        workflow_runners_by_name[plugin.name] = workflow_runner
    return workflow_runners_by_name

def load_plugin(group: str, name: str):
    for plugin in entry_points(group=f"czid.plugin.{group}"):
        if plugin.name == name:
            return plugin.load()
    raise ValueError(f"Plugin {name} not found in group {group}")
