from database.models import Run
from plugin_types import EntityInputLoader, Primitive
from entity_interface import Entity, ReferenceGenome


class ConsensusGenomeDefaultInputsLoader(EntityInputLoader):
    async def load(self, workflow_run: Run, entity_inputs: dict[str, Entity], raw_inputs: dict[str, Primitive]) -> dict[str, Primitive]:
        return {
            "filter_reads": "",
            "output_refseq": "",
            "output_bed": "",
            "ref_host": "",
            "kraken2_db_tar_gz": "",
            "ercc_fasta": "",
        }

