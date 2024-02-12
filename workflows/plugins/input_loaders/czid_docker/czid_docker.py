import typing

import boto3

from database.models.workflow_version import WorkflowVersion
from manifest.manifest import EntityInput
from plugins.plugin_types import InputLoader


class CZIDDockerImageInputLoader(InputLoader):
    """
    This loads docker images based on CZID's conventions
    """
    async def load(
        self,
        workflow_version: WorkflowVersion,
        entity_inputs: dict[str, EntityInput],
        raw_inputs: dict[str, typing.Any],
        requested_outputs: list[str] = [],
    ) -> dict[str, str]:
        sts = boto3.client("sts")
        account_id = sts.get_caller_identity()["Account"]
        aws_region = "us-west-2"  # CZID publishes images to this region

        return {
            "docker_image_id": f"{account_id}.dkr.ecr.{aws_region}.amazonaws.com/consensus-genome:v{str(workflow_version.version)}",
        }
