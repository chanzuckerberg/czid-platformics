import json
import subprocess
import sys
import tempfile
import os
from typing import List
from uuid import uuid4
import re

from plugin_types import EventBus, WorkflowFailedMessage, WorkflowRunner, WorkflowStartedMessage, WorkflowStepMessage, WorkflowSucceededMessage


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
    
    async def detect_task_input_output(self, event_bus, runner_id, line):
        if ("INFO output :: job:" in line) or ("INFO input :: job:" in line):
            type = _search_group(r"INFO (\w+) ::", line, 1)
            task = _search_group(r"job: \"(.*)\",", line, 1)
            values = json.loads(_search_group(r"values: (\{.*\})", line, 1))
            print(f"task complete: {task}")
            for key, output in values.items():
                print(f"{key}: {output}")
            status = "STARTED" if type == "input" else "SUCCEEDED"
            await event_bus.send(WorkflowStepMessage(status=status, runner_id=runner_id, task=task, outputs=values))


    async def run_workflow(
        self,
        event_bus: EventBus,
        workflow_run_id: str,
        workflow_path: str,
        inputs: dict,
    ) -> str:
        runner_id = str(uuid4())
        await event_bus.send(WorkflowStartedMessage(runner_id, "WORKFLOW_STARTED"))
        # Running docker-in-docker requires the paths to files and outputs to be the same between 
        with tempfile.TemporaryDirectory(dir='/tmp') as tmpdir:
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
                    await self.detect_task_input_output(event_bus, runner_id, line)
                    print(line, file=sys.stderr)
                    if not line: break

                assert p.stdout
                outputs = json.loads(p.stdout.read().decode())["outputs"]
                await event_bus.send(WorkflowSucceededMessage(runner_id, outputs))

            except subprocess.CalledProcessError as e:
                print(e.output)
                await event_bus.send(WorkflowFailedMessage(runner_id, "WORKFLOW_FAILURE"))
        return runner_id
