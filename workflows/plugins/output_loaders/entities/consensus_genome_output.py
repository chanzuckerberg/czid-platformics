import csv
import json

from database.models.workflow_run import WorkflowRun
from sgqlc.operation import Operation
from manifest.manifest import EntityInput
from platformics.client.entities_schema import (
    AccessionWhereClause,
    Query,
    MetricConsensusGenomeCreateInput,
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
    def _s3_json(self, path: str):
        parsed = self._parse_uri(path)
        return json.loads(
            self._s3_client.get_object(
                Bucket=parsed["namespace"],
                Key=parsed["path"],
            ).read()
        )

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
            taxon_id = res["taxa"][0]["id"]
            accession_id = res["accessions"][0]["id"]
        else:
            taxon_id = entity_inputs["taxon"].entity_id
            accession_id = entity_inputs["accession"].entity_id
        op = Operation(Mutation)
        consensus_genome = op.create_consensus_genome(
            input=ConsensusGenomeCreateInput(
                producing_run_id = ID(workflow_run.id),
                collection_id=int(workflow_run.collection_id),
                taxon_id=ID(taxon_id),
                sequencing_read_id=ID(entity_inputs["sequencing_read"].entity_id),
                reference_genome_id=entity_inputs.get("reference_genome")
                and ID(entity_inputs["reference_genome"].entity_id),
                accession_id=ID(accession_id),
            )
        )
        consensus_genome.id()
        res = self._entities_gql(op)
        consensus_genome_id = res["createConsensusGenome"]["id"]
        op = Operation(Mutation)

        stats_path = workflow_outputs["compute_stats_out_output_stats"]
        assert isinstance(stats_path, str), f"Expected string, got {type(stats_path)}"
        stats = json.loads(self._s3_object_data(stats_path))
        quast_path = workflow_outputs["quast_out_quast_tsv"]
        assert isinstance(quast_path, str), f"Expected string, got {type(quast_path)}"
        quast_data = next(csv.DictReader(self._s3_object_data(quast_path), delimiter="\t"))

        metric_consensus_genome = op.create_metric_consensus_genome(
            input=MetricConsensusGenomeCreateInput(
                producing_run_id = ID(workflow_run.id),
                collection_id = int(workflow_run.collection_id),
                consensus_genome_id = ID(consensus_genome_id),
                reference_genome_length = int(quast_data["Reference length"]),
                percent_genome_called = round((stats["n_actg"] / float(quast_data['Reference length']) * 100), 1),
                percent_identity = round(((stats['n_actg'] - stats['ref_snps']) / float(stats['n_actg']) * 100), 1),
                gc_percent = round(float(quast_data["GC (%)"]), 1),
                total_reads = stats["total_reads"],
                mapped_reads = stats["mapped_reads"],
                ref_snps = stats["ref_snps"],
                n_actg = stats["n_actg"],
                n_missing = stats["n_missing"],
                n_ambiguous = stats["n_ambiguous"],
                coverage_depth = stats["depth_avg"],
                coverage_breadth = stats["coverage_breadth"],
                coverage_bin_size = stats["coverage_bin_size"],
                coverage_total_length = stats["total_length"],
                coverage_viz = stats["coverage"],
            )
        )
        metric_consensus_genome.id()

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
