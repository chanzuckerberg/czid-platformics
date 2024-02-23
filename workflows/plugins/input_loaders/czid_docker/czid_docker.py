import os

import boto3

from database.models.workflow_version import WorkflowVersion
from manifest.manifest import EntityInput
from platformics.util.types_utils import JSONValue
from plugins.plugin_types import InputLoader


class CZIDDockerInputLoader(InputLoader):
    """
    This loads docker images based on CZID's conventions
    """

    async def load(
        self,
        workflow_version: WorkflowVersion,
        entity_inputs: dict[str, EntityInput],
        raw_inputs: dict[str, JSONValue],
        requested_outputs: list[str] = [],
    ) -> dict[str, JSONValue]:
        name = f"consensus-genome:v{str(workflow_version.version)}"
        if os.getenv("ENVIRONMENT") == "test":
            return {"docker_image_id": name}
        sts = boto3.client("sts")
        account_id = sts.get_caller_identity()["Account"]
        aws_region = "us-west-2"  # CZID publishes images to this region

        return {
            "docker_image_id": f"{account_id}.dkr.ecr.{aws_region}.amazonaws.com/{name}",
        }
