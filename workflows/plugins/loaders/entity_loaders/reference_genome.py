from database.models import Run
from plugin_types import EntityInputLoader, Primitive
from entity_interface import Entity, ReferenceGenome


class ReferenceGenomeInputLoader(EntityInputLoader):
    async def load(self, workflow_run: Run, entity_inputs: dict[str, Entity], raw_inputs: dict[str, Primitive]) -> dict[str, Primitive]:
        reference_genome = entity_inputs["reference_genome"]
        assert isinstance(reference_genome, ReferenceGenome)

        return {
            "ref_fasta": (await reference_genome.file.load()).path,
            "ref_accession_id": reference_genome.accession_id,
        }

