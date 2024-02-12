import typing

from sgqlc.operation import Operation
from database.models.workflow_version import WorkflowVersion
from manifest.manifest import EntityInput
from platformics.client.entities_schema import AccessionWhereClause, Query, ReferenceGenomeWhereClause, SequencingReadWhereClause, UUIDComparators
from database.models.workflow_version import WorkflowVersion
from plugins.plugin_types import InputLoader


PUBLIC_REFERENCES_BUCKET = "czid-public-references"
SARS_COV_2_ACCESSION_ID = "MN908947.3"
NA_PRIMER_FILE = "na_primers.bed"


def nanopore_primer_set(protocol: str) -> str:
    if protocol == "artic":
        return "nCoV-2019/V3"
    if protocol == "midnight":
        return "nCoV-2019/V1200"
    if protocol == "artic_v4":
        return "nCoV-2019/V4"
    if protocol == "artic_v5":
        return "nCoV-2019/V5"
    if protocol == "varskip"
        return "NEB_VarSkip/V1a"
    raise ValueError(f"Unsupported protocol {protocol}")

def illumina_primer_file(protocol: str) -> str:
    if protocol == "ampliseq":
        return "ampliseq_primers.bed"
    if protocol == "artic":
        return "artic_v3_primers.bed"
    if protocol == "combined_msspe_artic":
        return "combined_msspe_artic_primers.bed"
    if protocol == "covidseq":
        return "covidseq_primers.bed"
    if protocol == "msspe":
        return "msspe_primers.bed"
    if protocol == "snap":
        return "snap_primers.bed"
    if protocol == "artic_short_amplicons":
        return "artic_v3_short_275_primers.bed"
    if protocol == "artic_v4":
        return "artic_v4_primers.bed"
    if protocol == "varskip":
        return "neb_vss1a.primer.bed"
    if protocol == "easyseq":
        return "easyseq.bed"
    if protocol == "midnight":
        return "midnight_primers.bed"
    if protocol == "artic_v5":
        return "SARs-CoV-2_v5.3.2_400.primer.bed"
    raise ValueError(f"Unsupported protocol {protocol}")


class ConsensusGenomeInputLoader(InputLoader):
    async def load(
        self,
        workflow_version: WorkflowVersion,
        entity_inputs: dict[str, EntityInput],
        raw_inputs: dict[str, typing.Any],
        requested_outputs: list[str] = [],
    ) -> dict[str, str]:
        sars_cov_2 = raw_inputs["sars_cov_2"]

        sequencing_read_input = entity_inputs["sequencing_read"]
        op = Operation(Query)
        sequencing_reads = op.sequencing_reads(where=SequencingReadWhereClause(id=UUIDComparators(_eq=sequencing_read_input.entity_id)))
        sequencing_reads.protocol()  # type: ignore
        sequencing_reads.technologu()  # type: ignore
        sequencing_reads.clearlabs_export()  # type: ignore
        sequencing_reads.medaka_model()  # type: ignore
        self._fetch_file(sequencing_reads.primer_file().file())  # type: ignore

        if not sars_cov_2:
            accession_input = entity_inputs["accession"]
            accessions = op.accessions(where=AccessionWhereClause(id=UUIDComparators(_eq=accession_input.entity_id)))
            accessions.accession_id()  # type: ignore

        reference_genome_input = entity_inputs["reference_genome"]
        if reference_genome_input:
            reference_genomes = op.reference_genomes(where=ReferenceGenomeWhereClause(id=UUIDComparators(_eq=reference_genome_input.entity_id)))
            self._fetch_file(reference_genomes.file())  # type: ignore

        resp = self._entities_gql(op)
        sequencing_read = resp["data"]["sequencing_reads"][0]
        primer_bed_uri = self._uri_file(sequencing_read.get("primer_file"))

        accession = resp["data"]["accessions"][0]

        reference_fasta_uri = None
        if reference_genome_input:
            reference_genome = resp["data"]["reference_genomes"][0]
            reference_fasta_uri = self._uri_file(reference_genome.get("file"))

        inputs = {}
        if sars_cov_2:
            inputs["ref_fasta"] = f"s3://{PUBLIC_REFERENCES_BUCKET}/consensus-genome/{SARS_COV_2_ACCESSION_ID}.fa"
            if sequencing_read.technology == "Nanopore":
                inputs.update({
                    "apply_length_filter": not sequencing_read.clearlabs_export,
                    "medaka_model": sequencing_read.medaka_model,
                    # Remove ref_fasta once it's changed to an optional wdl input for ONT runs.
                    "primer_set": nanopore_primer_set(sequencing_read.protocol),
                    "primer_schemes": f"s3://{PUBLIC_REFERENCES_BUCKET}/consensus-genome/artic-primer-schemes_v6.tar.gz",
              })
            else:
                inputs["primer_bed"] = f"s3://{PUBLIC_REFERENCES_BUCKET}/consensus-genome/{illumina_primer_file(sequencing_read.protocol)}",
        else:
            inputs["ref_accession_id"] = accession.accession_id
            assert sequencing_read.technology == "Illumina", "Nanopore only supports SARS-CoV-2"

            if reference_genome_input: 
                inputs.update({
                    "ref_fasta": reference_fasta_uri,
                    # Default to empty primer file if the user does not provide a primer bed file (optional input)
                    "primer_bed": primer_bed_uri or f"s3://{PUBLIC_REFERENCES_BUCKET}/consensus-genome/{NA_PRIMER_FILE}",
                    # This option filters all except SARS-CoV-2 at the moment:
                    "filter_reads": False,
                    # signal to workflow that we want to include the refseq and bedfile in zipoutputs
                    "output_refseq": True,
                    "output_bed": bool(primer_bed_uri),
                  })
            else:
                inputs.update({
                    # This option filters all except SARS-CoV-2 at the moment:
                    "filter_reads": False,
                    # Use empty primer file b/c the user does not specify a wetlab protocol when dispatching cg samples from an mngs report
                    "primer_bed": f"s3://{PUBLIC_REFERENCES_BUCKET}/consensus-genome/#{NA_PRIMER_FILE}",
                })

        inputs.update({
            "ref_host": f"s3://{PUBLIC_REFERENCES_BUCKET}/consensus-genome/hg38.fa.gz",
            "ercc_fasta": f"s3://{PUBLIC_REFERENCES_BUCKET}/consensus-genome/ercc_sequences.fasta",
            "kraken2_db_tar_gz": f"s3://{PUBLIC_REFERENCES_BUCKET}/consensus-genome/kraken_coronavirus_db_only.tar.gz",
        })
        return inputs
