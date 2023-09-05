import asyncio
from typing import Any, Dict, List
from importlib.metadata import entry_points

from sqlalchemy import select
from workflows.database.models.workflow import WorkflowVersion, Run

from semver import Version
from sqlalchemy.ext.asyncio import AsyncSession
from workflows.entity_interface import create_entities

from workflows.plugin_types import EventListener, Loader, LoaderInput, WorkflowSucceededMessage


def load_output_loaders() -> List[Loader]:
    loaders: List[Loader] = []
    for plugin in entry_points(group="czid.plugin.loader"):
        loader = plugin.load()()
        assert isinstance(loader, Loader)
        loaders.append(loader)
    return loaders


loaders = load_output_loaders()
listener: EventListener 

class WorkflowOutput:
    name: str
    output_type_version: Version

class EntityOutput:
    workflow_outputs: List[str]
    entity_type: str
    loader_inputs: List[LoaderInput]

class LoaderDriver:
    session: AsyncSession
    loader_cache: Dict[Any, List[Loader]] = {}

    def resolve_loaders(self, workflow_version: WorkflowVersion) -> List[Loader]:
        if workflow_version.id in self.loader_cache:
            return self.loader_cache[workflow_version.id]

        loaders = []
        for entity in workflow_version.entity_outputs:
            for loader in loaders:
                if loader.satisfies(entity.loader_inputs):
                    loaders.append(loader)
                    break
            else:
                raise Exception(f"Could not find loader for {entity.loader_inputs}")
        self.loader_cache[workflow_version.id] = loaders
        return loaders

    async def process_workflow_completed(self, workflow_version: WorkflowVersion):
        loaders = self.resolve_loaders(workflow_version)
        entities_lists = await asyncio.gather(*[loader.load() for loader in loaders])
        for entities in entities_lists:
            await create_entities(entities)


    async def main(self):
        while True:
            for event in await listener.poll():
                if isinstance(event, WorkflowSucceededMessage):
                    _event: WorkflowSucceededMessage = event
                    run = (await self.session.execute(
                        select(Run).where(Run.runner_assigned_id == _event.runner_id)
                    )).scalar_one()
                    await self.process_workflow_completed(run.workflow_version)


