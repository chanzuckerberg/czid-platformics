from api.config import load_event_bus
import argparse
from settings import APISettings
import asyncio
from plugins.plugin_types import WorkflowStartedMessage, WorkflowFailedMessage, WorkflowSucceededMessage
import json
from dev_seeder import DevSeeder

message_type_map = {
    "started": WorkflowStartedMessage,
    "failed": WorkflowFailedMessage,
    "succeeded": WorkflowSucceededMessage,
}


async def main(
    collection_id: int, user_id: int, message_type: str, runner_id: str, outputs_json: str, seed: bool, workflow_name: str
) -> None:
    settings = APISettings.model_validate({})
    event_bus = load_event_bus(settings)

    if seed:
        ds = DevSeeder(user_id=user_id, collection_id=collection_id)
        ds.seed_workflow_runs(message_type, runner_id, workflow_name)

    message = message_type_map[message_type]
    outputs = json.loads(outputs_json)
    await event_bus.send(message(runner_id=runner_id, outputs=outputs))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Script to test the loaders and listeners")
    parser.add_argument(
        "message_type", type=str, choices=["started", "failed", "succeeded"], help="Type of message to send"
    )
    parser.add_argument("--collection_id", type=int, default=444, help="Runner ID to send")
    parser.add_argument("--user_id", type=int, default=111, help="Runner ID to send")
    parser.add_argument("--runner_id", type=str, default="11111", help="Runner ID to send")
    parser.add_argument("--outputs_json", type=str, default="{}", help="Outputs JSON to send")
    parser.add_argument("--seed", type=bool, default=False, help="Seed the database")
    parser.add_argument("--workflow_name", type=str, default="Simple Manifest", help="Name of the workflow to run")
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        main(args.collection_id, args.user_id, args.message_type, args.runner_id, args.outputs_json, args.seed, args.workflow_name)
    )
