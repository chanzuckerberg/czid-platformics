from database.models import Run
from plugin_types import EntityInputLoader, Primitive
from entity_interface import Entity, Sample


class SampleInputLoader(EntityInputLoader):
    async def load(self, workflow_run: Run, entity_inputs: dict[str, Entity], raw_inputs: dict[str, Primitive]) -> dict[str, Primitive]:
        sample = entity_inputs["sample"]
        assert isinstance(sample, Sample)
        assert len(sample.sequencing_reads) > 0, "Sample must have at least one sequencing read"
        sequencing_read = await sample.sequencing_reads[0].load()
        r2_file = sequencing_read.r2_file

        return {
            "name": sample.name,
            "r1": (await sequencing_read.r1_file.load()).path,
            "r2": r2_file and (await r2_file.load()).path,
        }

class PrimerInputLoader(EntityInputLoader):
    async def load(self, workflow_run: Run, entity_inputs: dict[str, Entity], raw_inputs: dict[str, Primitive]) -> dict[str, Primitive]:
        sample = entity_inputs["sample"]
        assert isinstance(sample, Sample)
        assert len(sample.sequencing_reads) > 0, "Sample must have at least one sequencing read"
        sequencing_read = await sample.sequencing_reads[0].load()
        primer_file = sequencing_read.primer_file
        return {
            "primer_set": "",
            "primer_schemes": "",
            "primer_bed": primer_file and (await primer_file.load()).path,
        }
