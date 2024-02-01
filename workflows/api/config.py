"""
Functions that load installed plugins
"""

from importlib.metadata import entry_points

from packaging.specifiers import SpecifierSet
from settings import APISettings
from plugins.plugin_types import EventBus, InputLoader, OutputLoader, WorkflowRunner


def load_workflow_runner(settings: APISettings) -> WorkflowRunner:
    """Load workflow runners installed at czid.plugin.workflow_runner"""
    for plugin in entry_points(group="czid.plugin.workflow_runner"):
        if plugin.name != settings.PLATFORMICS_WORKFLOW_RUNNER_PLUGIN:
            continue
        workflow_runner = plugin.load()(getattr(settings.PLATFORMICS_WORKFLOW_RUNNER, plugin.name.upper()))
        assert isinstance(workflow_runner, WorkflowRunner)
        return workflow_runner
    raise Exception("Workflow runner plugin not found")


def load_event_bus(settings: APISettings) -> EventBus:
    """Load event bus plugins installed at czid.plugin.event_bus and set by PLATFORMICS_EVENT_BUS_PLUGIN"""
    for plugin in entry_points(group="czid.plugin.event_bus"):
        if plugin.name != settings.PLATFORMICS_EVENT_BUS_PLUGIN:
            continue
        event_bus = plugin.load()(getattr(settings.PLATFORMICS_EVENT_BUS, plugin.name.upper()))
        assert isinstance(event_bus, EventBus)
        return event_bus
    raise Exception(f"Event bus plugin {settings.PLATFORMICS_EVENT_BUS_PLUGIN} not found")


_input_loader_cache = {}


def resolve_input_loader(name: str, specifier: SpecifierSet) -> InputLoader | None:
    """Load input loaders by name"""
    if (name, specifier) in _input_loader_cache:
        return _input_loader_cache[(name, specifier)]
    max_version = None
    latest_plugin = None
    for plugin in entry_points(group="czid.plugin.input_loader"):
        if plugin.name != name or not plugin.dist:
            continue
        if specifier.contains(plugin.dist.version):
            if not max_version or plugin.dist.version > max_version:
                max_version = plugin.dist.version
                latest_plugin = plugin
    if latest_plugin:
        _input_loader_cache[(name, specifier)] = latest_plugin.load()()
    else:
        _input_loader_cache[(name, specifier)] = None
    return _input_loader_cache[(name, specifier)]


_output_loader_cache = {}


def resolve_output_loader(name: str, specifier: SpecifierSet) -> OutputLoader | None:
    """Load output loaders by name"""
    if (name, specifier) in _output_loader_cache:
        return _output_loader_cache[(name, specifier)]
    max_version = None
    latest_plugin = None
    for plugin in entry_points(group="czid.plugin.output_loader"):
        if plugin.name != name or not plugin.dist:
            continue
        if specifier.contains(plugin.dist.version):
            if not max_version or plugin.dist.version > max_version:
                max_version = plugin.dist.version
                latest_plugin = plugin
    if latest_plugin:
        _output_loader_cache[(name, specifier)] = latest_plugin.load()()
    else:
        _output_loader_cache[(name, specifier)] = None
    return _output_loader_cache[(name, specifier)]
