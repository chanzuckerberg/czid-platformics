import os
import sys

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
            assert isinstance(consensus_genome_input, EntityInput)

            op = Operation(Query)
            consensus_genome = op.consensus_genomes(
                where=ConsensusGenomeWhereClause(id=UUIDComparators(_eq=consensus_genome_input.entity_id))
            )
            consensus_genome.sequencing_read()
            consensus_genome.sequencing_read.sample()
            consensus_genome.sequencing_read.sample.id()
            consensus_genome.sequencing_read.sample.name()
            consensus_genome.accession()
            consensus_genome.accession.accession_id()
            if raw_inputs.get("bulk_download_type") == CG_BULK_DOWNLOAD_OUTPUT:
                consensus_genome.intermediate_output_files()
                consensus_genome.intermediate_output_files.download_link()
                consensus_genome.intermediate_output_files.download_link.url()
            elif raw_inputs.get("bulk_download_type") == CG_BULK_DOWNLOAD_CONSENSUS:
                consensus_genome.sequence()
                consensus_genome.sequence.download_link()
                consensus_genome.sequence.download_link.url()    
            res = self._entities_gql(op)
            inputs["files"] = []
            for cg_res in res["consensusGenomes"]:
                sample_name = f"{cg_res['sequencingRead']['sample']['name']}"
                sample_id = f"{cg_res['sequencingRead']['sample']['id']}"
                accession = f"{cg_res['accession']['accessionId']}"
                if accession:
                    output_name = f"{sample_name}_{sample_id}_{accession}"
                else:
                    output_name = f"{sample_name}_{sample_id}"

                if raw_inputs.get("bulk_download_type") == CG_BULK_DOWNLOAD_OUTPUT:
                    download_link = cg_res["intermediateOutputFiles"]["downloadLink"]["url"]
                    suffix = ".zip"
                elif raw_inputs.get("bulk_download_type") == CG_BULK_DOWNLOAD_CONSENSUS:
                    download_link = cg_res["sequence"]["downloadLink"]["url"]
                    suffix = ".fa"
                inputs["files"].append(
                    {
                        "output_name": output_name + suffix,
                        "file_path": download_link,
                    }
                )
        return inputs
