from importlib.metadata import entry_points
from plugin_types import WorkflowRunner


def load_workflow_runner(name: str) -> WorkflowRunner:
    workflow_runner_cls = load_plugin("workflow_runner", name)
    workflow_runner = workflow_runner_cls()
    assert isinstance(workflow_runner, WorkflowRunner)
    return workflow_runner

def load_plugin(group: str, name: str):
    for plugin in entry_points(group=f"czid.plugin.{group}"):
        if plugin.name == name:
            return plugin.load()
    raise ValueError(f"Plugin {name} not found in group {group}")

def load_plugin_apps():
    return { plugin.name: plugin.load() for plugin in entry_points(group="czid.plugin.app") }