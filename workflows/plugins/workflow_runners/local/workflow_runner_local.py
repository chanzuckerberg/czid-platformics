import json
import subprocess
import tempfile
import os
import asyncio
from typing import Callable, Coroutine, Any, List
from uuid import uuid4

from plugin_types import WorkflowRunner, WorkflowStatusMessage


class LocalWorkflowRunner(WorkflowRunner):
    def supported_workflow_types(self) -> List[str]:
        """Returns the supported workflow types, ie ["WDL"]"""
        return ["WDL"]
    
    def description(self) -> str:
        """Returns a description of the workflow runner"""
        return "Runs WDL workflows locally using miniWDL"

    def _run_workflow_blocking(self, on_complete: Callable[[WorkflowStatusMessage], Coroutine[Any, Any, Any]], workflow_run_id: str, workflow_path: str, inputs: dict, workflow_runner_id: str):
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                p = subprocess.run(["miniwdl", "run", "--verbose", os.path.abspath(workflow_path)] + [f"{k}={v}" for k, v in inputs.items()], check=True, cwd=tmpdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                outputs = json.loads(p.stdout.decode())["outputs"]
                asyncio.run(on_complete({
                    "runner_id": workflow_runner_id,
                    "status": "SUCCESS",
                    "outputs": outputs,
                    "error": None,
                }))
                print(outputs)
            except subprocess.CalledProcessError as e:
                print(e)
                asyncio.run(on_complete({
                    "runner_id": workflow_runner_id,
                    "status": "FAILURE",
                    "outputs": None,
                    "error": e.stderr.decode(),
                }))

    def run_workflow(self, on_complete: Callable[[WorkflowStatusMessage], Coroutine[Any, Any, Any]], workflow_run_id: str, workflow_path: str, inputs: dict) -> str:
        runner_id = str(uuid4())
        # TODO: Does not work yet, do I want to deal with docker-in-docker? 
        with tempfile.TemporaryDirectory() as tmpdir:
            try: 
                p = subprocess.run(["miniwdl", "run", "--verbose", os.path.abspath(workflow_path)] + [f"{k}={v}" for k, v in inputs.items()], check=True, cwd=tmpdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except Exception as e:
                import pdb; pdb.set_trace()
                print(e)
        return runner_id

