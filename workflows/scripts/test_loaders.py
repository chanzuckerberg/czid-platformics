from api.config import load_event_bus
from sqlalchemy.orm import joinedload, aliased
import argparse
from settings import APISettings
import asyncio
from plugins.plugin_types import WorkflowStartedMessage, WorkflowFailedMessage, WorkflowSucceededMessage
from test_infra.factories.workflow_run import WorkflowRunFactory
import json
from platformics.database.connect import init_sync_db
from test_infra.factories.main import SessionStorage

from database.models import WorkflowRun, WorkflowVersion, Workflow

message_type_map = {
    "started": WorkflowStartedMessage,
    "failed": WorkflowFailedMessage,
    "succeeded": WorkflowSucceededMessage,
}

# maps the message type to the status of the workflow run
# before the message is sent
message_type_prestatus_map = {"started": "PENDING", "failed": "RUNNING", "succeeded": "RUNNING"}


# TODO: split out seed function into its own module
def seed_workflow_runs(message_type: str, runner_id: str) -> None:
    settings = APISettings.model_validate({})
    app_db = init_sync_db(settings.SYNC_DB_URI)
    session = app_db.session()
    SessionStorage.set_session(session)
    # check if a workflow run with the same runner_id exists
    existing_workflow_run = session.query(WorkflowRun).filter(WorkflowRun.execution_id == runner_id).one_or_none()
    if existing_workflow_run:
        print(f"Workflow run with runner_id {runner_id} already exists")
    else:
        workflow_alias = aliased(Workflow)
        workflow_version = (
            session.query(WorkflowVersion)
            .join(workflow_alias, WorkflowVersion.workflow)
            .options(joinedload(WorkflowVersion.workflow))
            .filter(workflow_alias.name == "Simple Manifest")
            .first()
        )

        workflow_run = WorkflowRunFactory.create(
            execution_id=runner_id,
            workflow_version=workflow_version,
            status=message_type_prestatus_map[message_type],
            raw_inputs_json="{}",
            outputs_json=None,
        )

        session.add(workflow_run)
        session.commit()


async def main(message_type: str, runner_id: str, outputs_json: str, seed: bool) -> None:
    settings = APISettings.model_validate({})
    event_bus = load_event_bus(settings)

    if seed:
        seed_workflow_runs(message_type, runner_id)

    message = message_type_map[message_type]
    outputs = json.loads(outputs_json)
    await event_bus.send(message(runner_id=runner_id, outputs=outputs))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Script to test the loaders and listeners")
    parser.add_argument(
        "message_type", type=str, choices=["started", "failed", "succeeded"], help="Type of message to send"
    )
    parser.add_argument("--runner_id", type=str, default="11111", help="Runner ID to send")
    parser.add_argument("--outputs_json", type=str, default="{}", help="Outputs JSON to send")
    parser.add_argument("--seed", type=bool, default=False, help="Seed the database")
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.message_type, args.runner_id, args.outputs_json, args.seed))
