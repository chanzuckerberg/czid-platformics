import asyncio
import sys
from typing import Dict, List, Literal, Tuple, Type, TypeVar
from importlib.metadata import entry_points

from sqlalchemy import select
from database.models.workflow import Run

from semver import Version
from sqlalchemy.ext.asyncio import AsyncSession
from entity_interface import create_entities

from plugin_types import EventBus, EntityInputLoader, EntityOutputLoader, WorkflowSucceededMessage, WorkflowStepMessage
from manifest import Manifest, load_manifest


import json
from miniwdl_viz.mermaid_wdl import ParsedWDLToMermaid

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

class ShowPipelineViz:
    def __init__(self, viz_string):
        # Replace with workflow run json 
        with open("static_sample.json") as f:
            self.viz_string = json.load(f)

        self.pwm = ParsedWDLToMermaid()
        
    def plot_viz(self):
        mermaid_list = self.pwm.create_mermaid_flowchart(
            "static_sample", 
            self.viz_string["nodes"], 
            self.viz_string["edges"]
        )
        self.pwm.show_mermaid_flowchart(mermaid_list=mermaid_list, file_output=True)


class LoaderDriver:
    session: AsyncSession
    bus: EventBus

    def __init__(self, session: AsyncSession, bus: EventBus) -> None:
        self.session = session
        self.bus = bus
        self.viz = ShowPipelineViz('')
        self.viz.plot_viz()

    async def process_workflow_completed(self, user_id: int, collection_id: int, workflow_manifest: Manifest, outputs: Dict[str, str]):
        loaders = resolve_entity_output_loaders(workflow_manifest)
        loader_futures = []
        for loader_config, loader in zip(workflow_manifest.output_loaders, loaders):
            args = {}
            print("loader_config", loader_config.fields, file=sys.stderr)
            for field in loader_config.fields:
                source, field_name = field.reference.split(".")
                if source == "outputs":
                    args[field.name] = outputs[f"{workflow_manifest.name}.{field_name}"]
                elif source == "inputs":
                    raise Exception("TODO!")
                
            # field = loader_config.fields[0]
            # outputs = {item.name: outputs[f'{workflow_manifest.name}.{item.name}'] for item in loader_config.fields}
            print("args", args, file=sys.stderr)
            print("outputs", outputs, file=sys.stderr)
            loader_futures.append(loader.load(args))
        entities_lists = await asyncio.gather(*loader_futures)
        for entities in entities_lists:
            await create_entities(user_id, collection_id, entities)

    async def main(self):
        while True:
            for event in await self.bus.poll():
                if isinstance(event, WorkflowSucceededMessage):

                    manifest = load_manifest(open("sequence_manifest.json").read())
                    _event: WorkflowSucceededMessage = event
                    # run = (await self.session.execute(
                    #     select(Run).where(Run.runner_assigned_id == _event.runner_id)
                    # )).scalar_one()
                    user_id = 111
                    collection_id = 444
                    await self.process_workflow_completed(user_id, collection_id, manifest, _event.outputs)

                if isinstance(event, WorkflowStepMessage):
                    self.viz.pwm.py_mermaid.set_node_class(event.task)
                    self.viz.plot_viz()

            await asyncio.sleep(1)
