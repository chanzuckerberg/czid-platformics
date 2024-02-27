"""
Loader functions
"""

import asyncio
import json
import sys
from platformics.util.types_utils import JSONValue


from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from api.config import resolve_output_loader

from plugins.plugin_types import EventBus, WorkflowFailedMessage, WorkflowStartedMessage, WorkflowSucceededMessage
from database.models import WorkflowVersion, WorkflowRun
from manifest.manifest import EntityInput, Manifest
from support.enums import WorkflowRunStatus


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
        self,
        workflow_version: WorkflowVersion,
        workflow_run: WorkflowRun,
        entity_inputs: dict[str, EntityInput],
        outputs: dict[str, JSONValue],
    ) -> None:
        """
        After workflow completes run output loaders
        """

        raw_inputs = json.loads(workflow_run.raw_inputs_json) if workflow_run.raw_inputs_json else {}

        loader_futures = []
        workflow_manifest = Manifest.from_yaml(workflow_version.manifest)
        for output_loader_specifier in workflow_manifest.output_loaders:
            loader_entity_inputs = {
                k: entity_inputs[v] for k, v in output_loader_specifier.inputs.items() if v in entity_inputs
            }
            loader_raw_inputs = {k: raw_inputs[v] for k, v in output_loader_specifier.inputs.items() if v in raw_inputs}
            loader_workflow_outputs = {
                k: outputs[v] for k, v in output_loader_specifier.workflow_outputs.items() if v in outputs
            }
            output_loader = resolve_output_loader(output_loader_specifier.name, output_loader_specifier.version)
            if not output_loader:
                raise Exception(f"Output loader {output_loader_specifier.name} not found")
            loader_futures.append(
                output_loader.load(workflow_run, loader_entity_inputs, loader_raw_inputs, loader_workflow_outputs)
            )
        await asyncio.gather(*loader_futures)

    async def main(self) -> None:
        """Waits for events and if a workflow completes, runs the loaders"""
        print("Running listener")
        while True:
            for event in await self.bus.poll():
                print("event", event, file=sys.stderr)
                if isinstance(event, WorkflowStartedMessage):
                    workflow_run = (
                        await self.session.execute(
                            select(WorkflowRun).where(WorkflowRun.execution_id == event.runner_id)
                        )
                    ).scalar_one()
                    workflow_run.status = WorkflowRunStatus.RUNNING
                    await self.session.commit()

                if isinstance(event, WorkflowSucceededMessage):
                    _event: WorkflowSucceededMessage = event
                    result = await self.session.execute(
                        select(WorkflowRun)
                        .options(
                            joinedload(WorkflowRun.workflow_version),
                            selectinload(WorkflowRun.entity_inputs),
                        )
                        .where(WorkflowRun.execution_id == _event.runner_id)
                    )
                    workflow_run = result.scalar_one()

                    workflow_version = workflow_run.workflow_version

                    entity_inputs = {
                        entity_input.field_name: EntityInput(
                            entity_type=entity_input.type, entity_id=str(entity_input.input_entity_id)
                        )
                        for entity_input in workflow_run.entity_inputs
                    }
                    await self.process_workflow_completed(workflow_version, workflow_run, entity_inputs, _event.outputs)
                    workflow_run.status = WorkflowRunStatus.SUCCEEDED
                    await self.session.commit()

                if isinstance(event, WorkflowFailedMessage):
                    workflow_run = (
                        await self.session.execute(
                            select(WorkflowRun).where(WorkflowRun.execution_id == event.runner_id)
                        )
                    ).scalar_one()
                    workflow_run.status = WorkflowRunStatus.FAILED
                    await self.session.commit()
            await asyncio.sleep(1)
