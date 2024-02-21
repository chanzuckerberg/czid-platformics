from database.models.workflow_run import WorkflowRun
from sgqlc.operation import Operation
from manifest.manifest import EntityInput
from platformics.client.entities_schema import (
    AccessionWhereClause,
    Query,
    Mutation,
    ConsensusGenomeCreateInput,
    FileCreate,
    TaxonWhereClause,
    StrComparators,
    ID,
)
from platformics.util.types_utils import JSONValue
from plugins.plugin_types import OutputLoader


SARS_COV_2_TAXON_ID = "2697049"
SARS_COV_2_ACCESSION_ID = "MN908947.3"


class ConsensusGenomeOutputLoader(OutputLoader):
    async def load(
        self,
        workflow_run: WorkflowRun,
        entity_inputs: dict[str, EntityInput],
        raw_inputs: dict[str, JSONValue],
        workflow_outputs: dict[str, JSONValue],
    ) -> None:
        if raw_inputs.get("sars_cov_2"):
            op = Operation(Query)
            # Get the taxon id for SARS-CoV-2
            taxa = op.taxa(where=TaxonWhereClause(upstream_database_identifier=StrComparators(_eq=SARS_COV_2_TAXON_ID)))
            taxa.id()
            accessions = op.accessions(
                where=AccessionWhereClause(accession_id=StrComparators(_eq=SARS_COV_2_ACCESSION_ID))
            )
            accessions.id()
            res = self._entities_gql(op)
            taxon_id = res["data"]["taxa"][0]["id"]
            accession_id = res["data"]["accessions"][0]["id"]
        else:
            taxon_id = entity_inputs["taxon"].entity_id
            accession_id = entity_inputs["accession"].entity_id
        op = Operation(Mutation)
        consensus_genome = op.create_consensus_genome(
            input=ConsensusGenomeCreateInput(
                collection_id=int(workflow_run.collection_id),
                taxon_id=ID(taxon_id),
                sequence_read_id=ID(entity_inputs["sequencing_read"].entity_id),
                reference_genome_id=entity_inputs.get("reference_genome")
                and ID(entity_inputs["reference_genome"].entity_id),
                accession_id=ID(accession_id),
            )
        )
        consensus_genome.id()
        res = self._entities_gql(op)
        consensus_genome_id = res["data"]["createConsensusGenome"]["id"]
        op = Operation(Mutation)
        sequence_path = workflow_outputs["sequence"]
        assert isinstance(sequence_path, str)
        sequence_file = op.create_file(
            entity_id=consensus_genome_id,
            entity_field_name="sequence",
            file=FileCreate(name="sequence", file_format="fasta", **self._parse_uri(sequence_path)),
        )
        sequence_file.id()
        self._entities_gql(op)
        op = Operation(Mutation)
        intermediate_outputs_path = workflow_outputs["intermediate_outputs"]
        assert isinstance(intermediate_outputs_path, str)
        intermediate_outputs = op.create_file(
            entity_id=consensus_genome_id,
            entity_field_name="intermediate_outputs",
            file=FileCreate(
                name="intermediate_outputs", file_format="fasta", **self._parse_uri(intermediate_outputs_path)
            ),
        )
        intermediate_outputs.id()
        self._entities_gql(op)
