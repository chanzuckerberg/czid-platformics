import os

import boto3

from plugins.plugin_types import InputLoader


class CZIDDockerInputLoader(InputLoader):
    """
    This loads docker images based on CZID's conventions
    """

    async def load(self, workflow_version, entity_inputs, raw_inputs, requested_outputs = []):
        name = f"consensus-genome:v{str(workflow_version.version)}"
        if os.getenv("ENVIRONMENT") == "test":
            return {"docker_image_id": name}
        sts = boto3.client("sts")
        account_id = sts.get_caller_identity()["Account"]
        aws_region = "us-west-2"  # CZID publishes images to this region

        return {
            "docker_image_id": f"{account_id}.dkr.ecr.{aws_region}.amazonaws.com/{name}",
        }
