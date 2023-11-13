from database.models import Run
from plugin_types import EntityInputLoader, Primitive
from entity_interface import Entity


class PassthroughInputLoader(EntityInputLoader):
    async def load(self, workflow_run: Run, entity_inputs: dict[str, Entity], raw_inputs: dict[str, Primitive]) -> dict[str, Primitive]:
        return {
            "value": raw_inputs["value"],
        }

