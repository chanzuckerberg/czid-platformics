import json
import subprocess
import sys
import tempfile
import os
import asyncio
from typing import Callable, Coroutine, Any, List
from uuid import uuid4
import re

from plugin_types import EventListener, WorkflowRunner, WorkflowStatusMessage, WorkflowSucceededMessage

local_runner_folder = os.environ["LOCAL_RUNNER_FOLDER"]


class LocalWorkflowRunner(WorkflowRunner):
    def supported_workflow_types(self) -> List[str]:
        """Returns the supported workflow types, ie ["WDL"]"""
        return ["WDL"]

    def description(self) -> str:
        """Returns a description of the workflow runner"""
        return "Runs WDL workflows locally using miniWDL"

    def _run_workflow_blocking(
        self,
        on_complete: Callable[[WorkflowStatusMessage], Coroutine[Any, Any, Any]],
        workflow_run_id: str,
        workflow_path: str,
        inputs: dict,
        workflow_runner_id: str,
        listener: EventListener,
    ):
        local_runner_folder = os.environ["LOCAL_RUNNER_FOLDER"]
        with tempfile.TemporaryDirectory(dir=local_runner_folder) as tmpdir:
            try:
                p = subprocess.run(
                    ["miniwdl", "run", "--verbose", os.path.abspath(workflow_path)]
                    + [f"{k}={v}" for k, v in inputs.items()],
                    check=True,
                    cwd=tmpdir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                outputs = json.loads(p.stdout.decode())["outputs"]
                asyncio.run(
                    on_complete(
                        {
                            "runner_id": workflow_runner_id,
                            "status": "SUCCESS",
                            "outputs": outputs,
                            "error": None,
                        }
                    )
                )
                listener.send(WorkflowSucceededMessage(runner_id=workflow_runner_id))
            except subprocess.CalledProcessError as e:
                print(e)
                asyncio.run(
                    on_complete(
                        {
                            "runner_id": workflow_runner_id,
                            "status": "FAILURE",
                            "outputs": None,
                            "error": e.stderr.decode(),
                        }
                    )
                )

    def detect_task_output(self, line):
        if "INFO output :: job:" in line:
            task = re.search(r"job: (.*),", line).group(1)
            outputs = json.loads(re.search(r"values: (\{.*\})", line).group(1))
            breakpoint()
            print(f"task complete: {task}")
            for key, output in outputs.items():
                print(f"{key}: {output}")

    def run_workflow(
        self,
        on_complete: Callable[[WorkflowStatusMessage], Coroutine[Any, Any, Any]],
        workflow_run_id: str,
        workflow_path: str,
        inputs: dict,
        listener: EventListener,
    ) -> str:
        runner_id = str(uuid4())
        # Running docker-in-docker requires the paths to files and outputs to be the same between
        with tempfile.TemporaryDirectory(dir=local_runner_folder) as tmpdir:
            try:
                p = subprocess.Popen(
                    ["miniwdl", "run", "--verbose", os.path.abspath(workflow_path)]
                    + [f"{k}={v}" for k, v in inputs.items()],
                    cwd=tmpdir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                while True:
                    line = p.stderr.readline().decode()
                    self.detect_task_output(line)
                    print(line, file=sys.stderr)
                    if not line:
                        break

            except subprocess.CalledProcessError as e:
                print(e.output)
                breakpoint()
                print("hello world")
        return runner_id
