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
def resolve_entity_output_loaders(workflow_manifest: Manifest) -> List[EntityOutputLoader]:
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
    session: AsyncSession
    bus: EventBus

    def __init__(self, session: AsyncSession, bus: EventBus) -> None:
        self.session = session
        self.bus = bus

    async def process_workflow_completed(self, workflow_manifest: Manifest, outputs: Dict[str, str]):
        loaders = resolve_entity_output_loaders(workflow_manifest)
        loader_futures = []
        for loader_config, loader in zip(workflow_manifest.output_loaders, loaders):
            args = {}
            for field in loader_config.fields:
                source, field_name = field.reference.split(".")
            if source == "output":
                args[field.name] = outputs[field_name]
            elif source == "input":
                raise Exception("TODO!")
            field = loader_config.fields[0]
            outputs = {item.name: outputs[f'{workflow_manifest.name}.{item.name}'] for item in loader_config.fields}
            loader_futures.append(loader.load(args))
        entities_lists = await asyncio.gather(*loader_futures)
        for entities in entities_lists:
            await create_entities(entities)

    async def main(self):
        while True:
            for event in await self.bus.poll():
                if isinstance(event, WorkflowSucceededMessage):

                    manifest = load_manifest(open("first_workflow_manifest.json").read())
                    _event: WorkflowSucceededMessage = event
                    # run = (await self.session.execute(
                    #     select(Run).where(Run.runner_assigned_id == _event.runner_id)
                    # )).scalar_one()
                    await self.process_workflow_completed(manifest, _event.outputs)
            await asyncio.sleep(1)
