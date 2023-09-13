import asyncio
from typing import Dict, List, Literal, Tuple, Type, TypeVar
from importlib.metadata import entry_points

from sqlalchemy import select
from database.models.workflow import Run

from semver import Version
from sqlalchemy.ext.asyncio import AsyncSession
from entity_interface import create_entities

from plugin_types import EventBus, EntityInputLoader, EntityOutputLoader, WorkflowSucceededMessage
from manifest import Manifest, load_manifest

T = TypeVar('T', bound=Type[EntityInputLoader] | Type[EntityOutputLoader])
def load_loader_plugins(input_or_output: Literal["input", "output"], cls: T) -> Dict[str, List[Tuple[Version, T]]]:
    loaders: Dict[str, List[Tuple[Version, T]]] = {}
    for plugin in entry_points(group=f"czid.plugin.entity_{input_or_output}_loader"):
        assert plugin.dist, "Plugin distribution not found"
        name = plugin.name
        vesion =  Version.parse(plugin.dist.version)
        loader = plugin.load()()
        assert isinstance(loader, cls)
        if name not in loaders:
            loaders[name] = []
        loaders[name].append((vesion, loader))
    return loaders

input_loaders = load_loader_plugins("input", EntityInputLoader)
def resolve_entity_input_loaders(workflow_manifest: Manifest) -> List[EntityInputLoader]:
    resolved_loaders = []
    for loader_reference in workflow_manifest.input_loaders:
        name = loader_reference.name
        if name not in input_loaders:
            raise Exception(f"Could not find loader named '{name}'")
        versons = input_loaders[loader_reference.name]
        # TODO: version constrants, for now pick latest version
        _, latest = max(versons, key=lambda x: x[0])
        resolved_loaders.append(latest)
    return resolved_loaders

output_loaders = load_loader_plugins("output", EntityOutputLoader)
# TODO: DRY with above but make the types work poperly
def resolve_entity_output_loaders(workflow_manifest: Manifest) -> List[EntityOutputLoader]:
    resolved_loaders = []
    for loader_reference in workflow_manifest.output_loaders:
        name = loader_reference.name
        if name not in output_loaders:
            raise Exception(f"Could not find loader named '{name}'")
        versons = output_loaders[loader_reference.name]
        # TODO: version constrants, for now pick latest version
        _, latest = max(versons, key=lambda x: x[0])
        resolved_loaders.append(latest)
    return resolved_loaders


class LoaderDriver:
    session: AsyncSession
    bus: EventBus

    def __init__(self, session: AsyncSession, bus: EventBus) -> None:
        self.session = session
        self.bus = bus

    async def process_workflow_completed(self, workflow_manifest: Manifest, outputs: Dict[str, str]):
        loaders = resolve_entity_output_loaders(workflow_manifest)
        loader_futures = []
        for loader_reference, loader in zip(workflow_manifest.output_loaders, loaders):
            outputs = {k: outputs[f'{workflow_manifest.name}.{k}'] for k in loader_reference.workflow_outputs}
            loader_futures.append(loader.load(outputs))
        entities_lists = await asyncio.gather(*loader_futures)
        for entities in entities_lists:
            await create_entities(entities)

    async def main(self):
        while True:
            for event in await self.bus.poll():
                if isinstance(event, WorkflowSucceededMessage):

                    first_sequence = load_manifest(open("first_workflow_manifest.json").read())
                    _event: WorkflowSucceededMessage = event
                    # run = (await self.session.execute(
                    #     select(Run).where(Run.runner_assigned_id == _event.runner_id)
                    # )).scalar_one()
                    await self.process_workflow_completed(first_sequence, _event.outputs)
            await asyncio.sleep(1)
