import sys

import typing
from database.models.workflow_run import WorkflowRun
from sgqlc.operation import Operation
from manifest.manifest import EntityInput
from platformics.client.entities_schema import Mutation, ConsensusGenomeCreateInput, SequencingTechnology, NucleicAcid
from plugins.plugin_types import OutputLoader



class ConsensusGenomeOutputLoader(OutputLoader):
    async def load(
        self,
        workflow_run: WorkflowRun,
        entity_inputs: dict[str, EntityInput],
        raw_inputs: dict[str, typing.Any],
        workflow_outputs: dict[str, str],
    ) -> None:
        print("AAAAAAAAAAAAA", workflow_outputs, file=sys.stderr)
        op = Operation(Mutation)
        consensus_genome = op.create_sequencing_read(
            input=ConsensusGenomeCreateInput(
                collection_id=workflow_run.collection_id,
                # inputs
                taxon_id=entity_inputs["taxon"].entity_id,
                sequencing_read_id=entity_inputs["sequence_read"].entity_id,
                reference_genome_id=entity_inputs["reference_genome"].entity_id,
                accession_id=entity_inputs["accession"].entity_id,
                # outputs
                # sequence_id="",
                # metrics_id="",
                # intermediate_outputs_id="",
            )
        )
        consensus_genome.id()
        self._entities_gql(op)
