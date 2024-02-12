import typing
from database.models.workflow_version import WorkflowVersion
from manifest.manifest import EntityInput
from plugins.plugin_types import InputLoader


class ConsensusGenomeInputLoader(InputLoader):
    async def load(
        self,
        workflow_version: WorkflowVersion,
        entity_inputs: dict[str, EntityInput],
        raw_inputs: dict[str, typing.Any],
        requested_outputs: list[str] = [],
    ) -> dict[str, str]:
        return {
            "docker_image_id": "732052188396.dkr.ecr.us-west-2.amazonaws.com/consensus-genome:v3.4.18",
            "ercc_fasta": "https://czid-public-references.s3.amazonaws.com/consensus-genome/ercc_sequences.fasta",
            "fastqs_0": "s3://local-bucket/sample_sars-cov-2_paired_r1.fastq.gz",
            "fastqs_1": "s3://local-bucket/sample_sars-cov-2_paired_r2.fastq.gz",
            "kraken2_db_tar_gz": "https://czid-public-references.s3.amazonaws.com/consensus-genome/kraken_coronavirus_db_only.tar.gz",
            "nr_loc_db": "https://czid-public-references.s3.amazonaws.com/ncbi-indexes-prod/2021-01-22/index-generation-2/nr_loc.marisa",
            "nr_s3_path": "s3://czid-public-references/ncbi-indexes-prod/2021-01-22/index-generation-2/nr",
            "nt_loc_db": "https://czid-public-references.s3.amazonaws.com/ncbi-indexes-prod/2021-01-22/index-generation-2/nt_loc.marisa",
            "nt_s3_path": "s3://czid-public-references/ncbi-indexes-prod/2021-01-22/index-generation-2/nt",
            "primer_bed": "https://czid-public-references.s3.amazonaws.com/consensus-genome/artic_v3_primers.bed",
            "primer_set": "nCoV-2019/V1200",
            "ref_fasta": "https://czid-public-references.s3.amazonaws.com/consensus-genome/MN908947.3.fa",
            "ref_host": "https://czid-public-references.s3.amazonaws.com/consensus-genome/human_chr1.fa",
            "sample": "test_sample",
            "technology": "Illumina",
            # defaults
            "vadr_model": "https://czid-public-references.s3.amazonaws.com/consensus-genome/vadr-models-sarscov2-1.2-2.tar.gz",
            "primer_schemes": "https://czid-public-references.s3.amazonaws.com/consensus-genome/artic-primer-schemes_v2.tar.gz",
        }
