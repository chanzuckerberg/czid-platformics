import asyncio
from typing import Dict, List, Literal, Tuple, Type, TypeVar
from importlib.metadata import entry_points

from sqlalchemy import select
from database.models.workflow import Run

from semver import Version
from sqlalchemy.ext.asyncio import AsyncSession
from entity_interface import create_entities

from plugin_types import EventBus, EntityInputLoader, EntityOutputLoader, WorkflowSucceededMessage
from version import WorkflowVersion, static_sample

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
def resolve_entity_input_loaders(workflow_version: WorkflowVersion) -> List[EntityInputLoader]:
    resolved_loaders = []
    for loader_reference in workflow_version.input_loaders:
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
def resolve_entity_output_loaders(workflow_version: WorkflowVersion) -> List[EntityOutputLoader]:
    resolved_loaders = []
    for loader_reference in workflow_version.output_loaders:
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

    async def process_workflow_completed(self, user_id: int, collection_id: int, workflow_version: WorkflowVersion, outputs: Dict[str, str]):
        loaders = resolve_entity_output_loaders(workflow_version)
        loader_futures = []
        for loader_reference, loader in zip(workflow_version.output_loaders, loaders):
            outputs = {k: outputs[f'{workflow_version.name}.{k}'] for k in loader_reference.workflow_outputs}
            loader_futures.append(loader.load(outputs))
        entities_lists = await asyncio.gather(*loader_futures)
        for entities in entities_lists:
            await create_entities(user_id, collection_id, entities)

    async def main(self):
        while True:
            for event in await self.bus.poll():
                if isinstance(event, WorkflowSucceededMessage):
                    _event: WorkflowSucceededMessage = event
                    # run = (await self.session.execute(
                    #     select(Run).where(Run.runner_assigned_id == _event.runner_id)
                    # )).scalar_one()
                    user_id = 111
                    collection_id = 444 # TODO: get from run
                    await self.process_workflow_completed(user_id, collection_id, static_sample, _event.outputs)
            await asyncio.sleep(1)
