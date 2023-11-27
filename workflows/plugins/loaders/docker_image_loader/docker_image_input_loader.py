import os
from database.models import Run
from plugin_types import EntityInputLoader, Primitive
from entity_interface import Entity

AWS_ACCOUNT_ID = os.environ["AWS_ACCOUNT_ID"]
AWS_REGION = os.environ["AWS_REGION"]


class DockerImageInputLoader(EntityInputLoader):
    async def load(self, workflow_run: Run, entity_inputs, raw_inputs):
        return {
            "docker_image_id": f"{AWS_ACCOUNT_ID}.dkr.ecr.{AWS_REGION}.amazonaws.com/{workflow_run.workflow_version.workflow.name}:v{workflow_run.workflow_version.manifest.version}",
        }
