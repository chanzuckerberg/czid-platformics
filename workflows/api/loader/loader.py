"""
Loader functions
"""

import asyncio
import sys
from typing import Dict, List, Literal, Tuple, Type, TypeVar
from importlib.metadata import entry_points


from semver import Version
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from entity_interface import create_entities

from plugins.plugin_types import EventBus, EntityInputLoader, EntityOutputLoader, WorkflowSucceededMessage
from database.models import Run
from manifest.manifest import Manifest

T = TypeVar("T", bound=Type[EntityInputLoader] | Type[EntityOutputLoader])


def load_loader_plugins(input_or_output: Literal["input", "output"], cls: T) -> Dict[str, List[Tuple[Version, T]]]:
    """Loads in loader plugins"""
    loaders: Dict[str, List[Tuple[Version, T]]] = {}
    for plugin in entry_points(group=f"czid.plugin.entity_{input_or_output}_loader"):
        assert plugin.dist, "Plugin distribution not found"
        name = plugin.name
        vesion = Version.parse(plugin.dist.version)
        loader = plugin.load()()
        assert isinstance(loader, cls)
        if name not in loaders:
            loaders[name] = []
        loaders[name].append((vesion, loader))
    return loaders


input_loaders = load_loader_plugins("input", EntityInputLoader)


def resolve_entity_input_loaders(workflow_manifest: Manifest) -> List[type[EntityInputLoader]]:
    """
    Given a manifest, resolve input loaders
    """
    resolved_loaders = []
    for loader_config in workflow_manifest.input_loaders:
        name = loader_config.name
        try:
            versions = input_loaders[loader_config.name]
        except KeyError:
            raise Exception(f"Could not find loader named '{name}'")
        # TODO: version constrants, for now pick latest version
        _, latest = max(versions, key=lambda x: x[0])
        resolved_loaders.append(latest)
    return resolved_loaders


output_loaders = load_loader_plugins("output", EntityOutputLoader)


# TODO: DRY with above but make the types work poperly
def resolve_entity_output_loaders(workflow_manifest: Manifest) -> List[type[EntityOutputLoader]]:
    """
    Given a manifest, resolve output loaders
    """
    resolved_loaders = []
    for loader_config in workflow_manifest.output_loaders:
        name = loader_config.name
        try:
            versions = output_loaders[name]
        except KeyError:
            raise Exception(f"Could not find loader named '{name}'")
        # TODO: version constrants, for now pick latest version
        _, latest = max(versions, key=lambda x: x[0])
        resolved_loaders.append(latest)
    return resolved_loaders


class LoaderDriver:
    """
    Class to watch for events and run loaders
    """

    session: AsyncSession
    bus: EventBus

    def __init__(self, session: AsyncSession, bus: EventBus) -> None:
        self.session = session
        self.bus = bus

    async def process_workflow_completed(
        self, user_id: int, collection_id: int, workflow_manifest: Manifest, outputs: Dict[str, str]
    ) -> None:
        """
        After workflow completes run output loaders
        """
        loaders = resolve_entity_output_loaders(workflow_manifest)
        loader_futures = []
        for loader_config, loader in zip(workflow_manifest.output_loaders, loaders):
            args = {}
            for loader_input_name, workflow_input_name in loader_config.inputs.items():
                if workflow_input_name in workflow_manifest.raw_inputs:
                    args[loader_input_name] = workflow_manifest.raw_inputs[workflow_input_name]
                elif workflow_input_name in workflow_manifest.entity_inputs:
                    args[loader_input_name] = workflow_manifest.entity_inputs[workflow_input_name]
                else:
                    raise Exception(f"Could not find input '{workflow_input_name}'")
            for loader_input_name, workflow_output_name in loader_config.workflow_outputs:
                args[loader_input_name] = outputs[workflow_output_name]

            loader_futures.append(loader.load(args=args))  # type: ignore
        entities_lists = await asyncio.gather(*loader_futures)
        for entities in entities_lists:
            await create_entities(user_id, collection_id, entities)

    async def main(self) -> None:
        """Waits for events and if a workflow completes, runs the loaders"""
        while True:
            for event in await self.bus.poll():
                print("event", event, file=sys.stderr)
                if isinstance(event, WorkflowSucceededMessage):
                    _event: WorkflowSucceededMessage = event
                    run = (
                        await self.session.execute(select(Run).where(Run.execution_id == _event.runner_id))
                    ).scalar_one()
                    manifest = Manifest.model_validate(run.workflow_version.manifest)
                    user_id = 111
                    collection_id = 444
                    await self.process_workflow_completed(user_id, collection_id, manifest, _event.outputs)
            await asyncio.sleep(1)
