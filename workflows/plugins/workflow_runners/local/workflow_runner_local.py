"""
Plugin that runs a workflow locally using miniwdl
"""

import asyncio
import json
import os
from os.path import basename
import subprocess
import sys
import tempfile
import threading
from typing import List
from urllib.parse import urlparse
from uuid import uuid4
from pathlib import Path
import re

import boto3

from plugins.plugin_types import (
    EventBus,
    WorkflowFailedMessage,
    WorkflowRunner,
    WorkflowStartedMessage,
    WorkflowSucceededMessage,
)
from settings import LocalWorkflowRunnerSettings


def _search_group(pattern: str | re.Pattern[str], string: str, n: int) -> str:
    """helper to return a match of a pattern"""
    match = re.search(pattern, string)
    assert match
    group = match.group(n)
    assert isinstance(group, str)
    return group


class LocalWorkflowRunner(WorkflowRunner):
    """Class to run a workflow locally"""

    def __init__(self, settings: LocalWorkflowRunnerSettings):
        self.s3_endpoint_url = settings.S3_ENDPOINT

    def supported_workflow_types(self) -> List[str]:
        """Returns the supported workflow types, ie ["WDL"]"""
        return ["WDL"]

    def description(self) -> str:
        """Returns a description of the workflow runner"""
        return "Runs WDL workflows locally using miniWDL"

    def _detect_task_output(self, line: str) -> None:
        """Given the output of miniwdl detects if a task is complete its outputs"""
        if "INFO output :: job:" in line:
            task = _search_group(r"job: (.*),", line, 1)
            outputs = json.loads(_search_group(r"values: (\{.*\})", line, 1))
            print(f"task complete: {task}")
            for key, output in outputs.items():
                print(f"{key}: {output}")

    def config_file(self, dir_path: str) -> str:
        config_file_str = """
[download_awscli]
host_credentials = true

[task_runtime]
defaults = {
  "docker_network": "czidnet" }

[docker_swarm] 
allow_networks = ["czidnet"]"""
        file_path = str(Path(dir_path) / "miniwdl.cfg")
        with open(file_path, "w+") as f:
            f.write(config_file_str)
        return file_path

    async def _run_workflow_work(
        self,
        event_bus: EventBus,
        workflow_path: str,
        inputs: dict,
        runner_id: str,
    ) -> None:
        """Run miniwdl workflows locally"""
        # sleep to simulate time before the workflow starts running
        await asyncio.sleep(1)
        await event_bus.send(WorkflowStartedMessage(runner_id=runner_id))
        with tempfile.TemporaryDirectory(dir="/tmp") as tmpdir:
            # download workflow path from s3
            s3 = boto3.client("s3", endpoint_url=self.s3_endpoint_url)

            parsed_workflow_path = urlparse(workflow_path)
            bucket, key = parsed_workflow_path.netloc, parsed_workflow_path.path.lstrip("/")
            local_workflow_path = os.path.join(tmpdir, basename(key))
            s3.download_file(bucket, key, local_workflow_path)

            config_path = self.config_file(tmpdir)
            cmd = [
                "miniwdl",
                "run",
                "--verbose",
            ]
            if self.s3_endpoint_url:
                cmd += ["--env", f"AWS_ENDPOINT_URL={self.s3_endpoint_url}"]
            if config_path:
                cmd += [
                    "--cfg",
                    config_path,
                ]
            cmd += [os.path.abspath(local_workflow_path)]
            cmd += [f"{k}={v}" for k, v in inputs.items()]
            try:
                p = subprocess.Popen(
                    cmd,
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
        """Wrapper around async function to run synchronously"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._run_workflow_work(event_bus, workflow_path, inputs, runner_id))
        loop.close()

    async def run_workflow(
        self,
        event_bus: EventBus,
        workflow_path: str,
        inputs: dict,
    ) -> str:
        """Creates runner id and runs workflow asynchronously"""
        runner_id = str(uuid4())
        # run workflow in a thread, we are doing something a bit weird where we want to run the workflow
        #   asynchronously and not wait for the result. Instead the listener will be informed that it
        #   has terminated through the event bus. However, the event bus API is async so we need to call
        #   it from an async function. This is why we spawn a thread to run a synchronous wrapper around
        #   an async function.
        thread = threading.Thread(
            target=self._run_workflow_sync,
            args=(event_bus, workflow_path, inputs, runner_id),
        )
        thread.start()
        return runner_id
