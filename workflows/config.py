from importlib.metadata import entry_points
from typing import Dict
from platformics.api.core.settings import APISettings
from plugin_types import EventBus, WorkflowRunner


def load_workflow_runners() -> Dict[str, WorkflowRunner]:
    workflow_runners_by_name: Dict[str, WorkflowRunner] = {}
    for plugin in entry_points(group="czid.plugin.workflow_runner"):
        workflow_runner = plugin.load()()
        assert isinstance(workflow_runner, WorkflowRunner)
        workflow_runners_by_name[plugin.name] = workflow_runner
    return workflow_runners_by_name


def load_event_bus(settings: APISettings) -> EventBus:
    for plugin in entry_points(group="czid.plugin.event_bus"):
        if plugin.name != settings.PLATFORMICS_EVENT_BUS_PLUGIN:
            continue
        event_bus = plugin.load()(
            getattr(settings.PLATFORMICS_EVENT_BUS, settings.PLATFORMICS_EVENT_BUS_PLUGIN.upper())
        )
        assert isinstance(event_bus, EventBus)
        return event_bus
    raise Exception(f"Event bus plugin {settings.PLATFORMICS_EVENT_BUS_PLUGIN} not found")
