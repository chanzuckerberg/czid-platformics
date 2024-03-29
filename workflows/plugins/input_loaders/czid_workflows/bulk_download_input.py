from sgqlc.operation import Operation

from database.models.workflow_version import WorkflowVersion
from manifest.manifest import EntityInput, Primitive
from platformics.client.entities_schema import (
    ConsensusGenomeWhereClause,
    Query,
    UUIDComparators,
)
from platformics.util.types_utils import JSONValue
from plugins.plugin_types import InputLoader

PUBLIC_REFERENCES_PREFIX = "s3://czid-public-references/consensus-genome"
CG_BULK_DOWNLOAD_OUTPUT = "consensus_genome_intermediate_output_files"
CG_BULK_DOWNLOAD_CONSENSUS = "consensus_genome"
CG_BULK_DOWNLOADS = [CG_BULK_DOWNLOAD_CONSENSUS, CG_BULK_DOWNLOAD_OUTPUT]


class BulkDownloadInputLoader(InputLoader):
    async def load(
        self,
        workflow_version: WorkflowVersion,
        entity_inputs: dict[str, EntityInput | list[EntityInput]],
        raw_inputs: dict[str, Primitive | list[Primitive]],
        requested_outputs: list[str] = [],
    ) -> dict[str, JSONValue]:
        inputs: dict[str, JSONValue] = {}
        if raw_inputs.get("bulk_download_type") in CG_BULK_DOWNLOADS:
            consensus_genome_input = entity_inputs["consensus_genomes"]
            op = Operation(Query)
            if isinstance(consensus_genome_input, EntityInput):
                # if single input
                consensus_genome = op.consensus_genomes(
                    where=ConsensusGenomeWhereClause(id=UUIDComparators(_eq=consensus_genome_input.entity_id))
                )
            else:
                # must be list of inputs
                consensus_genome = op.consensus_genomes(
                    where=ConsensusGenomeWhereClause(
                        id=UUIDComparators(_in=[cg.entity_id for cg in consensus_genome_input])
                    )
                )
            consensus_genome.sequencing_read()
            consensus_genome.sequencing_read.sample()
            consensus_genome.sequencing_read.sample.id()
            consensus_genome.sequencing_read.sample.name()
            consensus_genome.accession()
            consensus_genome.accession.accession_id()
            if raw_inputs.get("bulk_download_type") == CG_BULK_DOWNLOAD_OUTPUT:
                self._fetch_file(consensus_genome.intermediate_outputs())
            elif raw_inputs.get("bulk_download_type") == CG_BULK_DOWNLOAD_CONSENSUS:
                self._fetch_file(consensus_genome.sequence())
            res = self._entities_gql(op)
            files: list[dict[str, Primitive | None]] = []
            for cg_res in res["consensusGenomes"]:
                sample_name = f"{cg_res['sequencingRead']['sample']['name']}"
                sample_id = f"{cg_res['sequencingRead']['sample']['id']}"
                if cg_res["accession"]:
                    accession = f"{cg_res['accession']['accessionId']}"
                    output_name = f"{sample_name}_{sample_id}_{accession}"
                else:
                    output_name = f"{sample_name}_{sample_id}"

                if raw_inputs.get("bulk_download_type") == CG_BULK_DOWNLOAD_OUTPUT:
                    download_link = self._uri_file(cg_res["intermediateOutputs"])
                    suffix = ".zip"
                elif raw_inputs.get("bulk_download_type") == CG_BULK_DOWNLOAD_CONSENSUS:
                    download_link = self._uri_file(cg_res["sequence"])
                    suffix = ".fa"
                files.append(
                    {
                        "output_name": output_name + suffix,
                        "file_path": download_link,
                    }
                )
            inputs["files"] = files  # type: ignore
        return inputs
