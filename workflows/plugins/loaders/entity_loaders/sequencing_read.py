from typing import TypedDict
from database.models import Run
from plugin_types import EntityInputLoader, Primitive
from entity_interface import Entity, SequencingRead

class EntityInputs(TypedDict):
    sequencing_read: SequencingRead


class SequencingReadInputLoader(EntityInputLoader):
    async def load(self, workflow_run: Run, entity_inputs: EntityInputs, raw_inputs):
        sequencing_read = entity_inputs["sequencing_read"]
        r2_file = sequencing_read.r2_file
        primer_file = sequencing_read.primer_file

        return {
            "r1": (await sequencing_read.r1_file.load()).path,
            "r2": r2_file and (await r2_file.load()).path,
            "primer_bed": primer_file and (await primer_file.load()).path,
        }

