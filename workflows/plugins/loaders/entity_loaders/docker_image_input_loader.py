from database.models import Run
from plugin_types import EntityInputLoader, Primitive
from entity_interface import Entity, Sample


class DockerImageInputLoader(EntityInputLoader):
    async def load(self, workflow_run: Run, entity_inputs: dict[str, Entity], raw_inputs: dict[str, Primitive]) -> dict[str, Primitive]:
        return {
            "docker_image_id": f"{workflow_run.workflow_version.manifest.version}",
        }
