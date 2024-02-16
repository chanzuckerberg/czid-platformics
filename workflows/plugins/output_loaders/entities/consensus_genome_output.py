import typing
from database.models.workflow_run import WorkflowRun
from sgqlc.operation import Operation
from manifest.manifest import EntityInput
from platformics.client.entities_schema import Query, Mutation, ConsensusGenomeCreateInput, FileCreate, TaxonWhereClause
from plugins.plugin_types import OutputLoader



class ConsensusGenomeOutputLoader(OutputLoader):
    async def load(
        self,
        workflow_run: WorkflowRun,
        entity_inputs: dict[str, EntityInput],
        raw_inputs: dict[str, typing.Any],
        workflow_outputs: dict[str, str],
    ) -> None:
        if raw_inputs.get('sars_cov_2'):
            op = Operation(Query)
            # Get the taxon id for SARS-CoV-2
            op.taxa(where=TaxonWhereClause(upstream_database_identifier="2697049"))
            res = self._entities_gql(op)
            taxon_id = res["data"]["taxa"][0]["id"]
        else:
            taxon_id = entity_inputs["taxon"].entity_id
        op = Operation(Mutation)
        consensus_genome = op.create_sequencing_read(
            input=ConsensusGenomeCreateInput(
                owner_user_id=workflow_run.owner_user_id,
                collection_id=workflow_run.collection_id,
                producing_workflow_run_id=workflow_run.id,
                # inputs
                taxon_id=taxon_id,
                sequencing_read_id=entity_inputs["sequence_read"].entity_id,
                reference_genome_id=entity_inputs["reference_genome"].entity_id,
                accession_id=entity_inputs["accession"].entity_id,
                # outputs
                # metrics_id="",
            )
        )
        consensus_genome.id()
        res = self._entities_gql(op)
        consensus_genome_id = res["data"]["createConsensusGenome"]["id"]
        op = Operation(Mutation)
        sequence_path = workflow_outputs["sequence"]
        op.create_file(
            entity_id=consensus_genome_id,
            entity_field_name="sequence_id",
            file=FileCreate(
                file_format="fasta",
                **self._parse_uri(sequence_path)
            )
        )
        intermediate_outputs_path = workflow_outputs["intermediate_outputs"]
        op.create_file(
            entity_id=consensus_genome_id,
            entity_field_name="intermediate_outputs_id",
            file=FileCreate(
                file_format="fasta",
                **self._parse_uri(intermediate_outputs_path)
            )
        )
        self._entities_gql(op)
