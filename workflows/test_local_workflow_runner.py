from api.config import load_event_bus, load_workflow_runners
from settings import APISettings
import asyncio
from plugins.plugin_types import (
    WorkflowStartedMessage,
)

inputs_json = {}


async def main() -> None:
    settings = APISettings.model_validate({})
    load_workflow_runners()["local"]
    event_bus = load_event_bus(settings)
    print("hello")
    await event_bus.send(WorkflowStartedMessage(runner_id="1111"))
    await event_bus.send(WorkflowStartedMessage(runner_id="1111"))
    await event_bus.send(WorkflowStartedMessage(runner_id="1111"))
    await event_bus.send(WorkflowStartedMessage(runner_id="1111"))
    await event_bus.send(WorkflowStartedMessage(runner_id="1111"))
    print("world")

    await event_bus.send(WorkflowStartedMessage(runner_id="1111"))


if __name__ == "__main__":
    loop2 = asyncio.get_event_loop()
    loop2.run_until_complete(main())
