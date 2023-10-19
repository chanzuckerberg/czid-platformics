import asyncio
import json
import os
import subprocess
import sys
import tempfile
import threading
from typing import List
from uuid import uuid4
import re

from plugin_types import (
    EventBus,
    WorkflowFailedMessage,
    WorkflowRunner,
    WorkflowStartedMessage,
    WorkflowSucceededMessage,
)


def _search_group(pattern: str | re.Pattern[str], string: str, n: int) -> str:
    match = re.search(pattern, string)
    assert match
    group = match.group(n)
    assert isinstance(group, str)
    return group


class LocalWorkflowRunner(WorkflowRunner):
    def supported_workflow_types(self) -> List[str]:
        """Returns the supported workflow types, ie ["WDL"]"""
        return ["WDL"]

    def description(self) -> str:
        """Returns a description of the workflow runner"""
        return "Runs WDL workflows locally using miniWDL"

    def _detect_task_output(self, line: str) -> None:
        if "INFO output :: job:" in line:
            task = _search_group(r"job: (.*),", line, 1)
            outputs = json.loads(_search_group(r"values: (\{.*\})", line, 1))
            print(f"task complete: {task}")
            for key, output in outputs.items():
                print(f"{key}: {output}")

    async def _run_workflow_work(
        self,
        event_bus: EventBus,
        workflow_path: str,
        inputs: dict,
        runner_id: str,
    ) -> None:
        await event_bus.send(WorkflowStartedMessage(runner_id=runner_id))
        # Running docker-in-docker requires the paths to files and outputs to be the same between
        with tempfile.TemporaryDirectory(dir="/tmp") as tmpdir:
            try:
                p = subprocess.Popen(
                    ["miniwdl", "run", "--verbose", os.path.abspath(workflow_path)]
                    + [f"{k}={v}" for k, v in inputs.items()],
                    cwd=tmpdir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                while True:
                    assert p.stderr
                    line = p.stderr.readline().decode()
                    self._detect_task_output(line)
                    print(line, file=sys.stderr)
                    if not line:
                        break

                assert p.stdout
                outputs = json.loads(p.stdout.read().decode())["outputs"]
                await event_bus.send(WorkflowSucceededMessage(runner_id=runner_id, outputs=outputs))

            except subprocess.CalledProcessError as e:
                print(e.output)
                await event_bus.send(WorkflowFailedMessage(runner_id=runner_id))

    def _run_workflow_sync(
        self,
        event_bus: EventBus,
        workflow_path: str,
        inputs: dict,
        runner_id: str,
    ) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._run_workflow_work(event_bus, workflow_path, inputs, runner_id))
        loop.close()

    async def run_workflow(
        self,
        event_bus: EventBus,
        workflow_run_id: str,
        workflow_path: str,
        inputs: dict,
    ) -> str:
        runner_id = str(uuid4())
        # run workflow in a thread
        thread = threading.Thread(
            target=self._run_workflow_sync,
            args=(event_bus, workflow_path, inputs, runner_id),
        )
        thread.start()
        return runner_id

