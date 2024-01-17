from typing import TypedDict
from plugin_types import EntityInputLoader
from entity_interface import Sample


class EntityInputs(TypedDict):
    sample: Sample


class SampleInputLoader(EntityInputLoader):
    async def load(self, workflow_run, entity_inputs: EntityInputs, raw_inputs):
        sample = entity_inputs["sample"]
        return {
            "name": sample.name,
        }
