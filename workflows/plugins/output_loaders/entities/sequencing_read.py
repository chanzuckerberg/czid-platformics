import typing
from database.models.workflow_run import WorkflowRun
from sgqlc.operation import Operation
from manifest.manifest import EntityInput
from platformics.client.entities_schema import Mutation, SequencingReadCreateInput, SequencingTechnology, NucleicAcid
from plugins.plugin_types import OutputLoader


class SequencingReadOutputLoader(OutputLoader):
    async def load(
        self,
        workflow_run: WorkflowRun,
        entity_inputs: dict[str, EntityInput],
        raw_inputs: dict[str, typing.Any],
        workflow_outputs: dict[str, str],
    ) -> None:
        op = Operation(Mutation)
        sequencing_read = op.create_sequencing_read(
            input=SequencingReadCreateInput(
                collection_id=workflow_run.collection_id,
                sample_id=entity_inputs["sample"].entity_id,
                nucleic_acid=NucleicAcid("DNA"),
                technology=SequencingTechnology("Illumina"),
                clearlabs_export=False,
            )
        )
        sequencing_read.id()
        self._entities_gql(op)
