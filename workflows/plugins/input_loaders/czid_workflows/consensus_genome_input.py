import os
import sys

from sgqlc.operation import Operation

from database.models.workflow_version import WorkflowVersion
from manifest.manifest import EntityInput, Primitive
from platformics.client.entities_schema import (
    AccessionWhereClause,
    Query,
    ReferenceGenomeWhereClause,
    SequencingReadWhereClause,
    UUIDComparators,
)
from platformics.util.types_utils import JSONValue
from plugins.plugin_types import InputLoader

PUBLIC_REFERENCES_PREFIX = "s3://czid-public-references/consensus-genome"
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
    if protocol == "varskip":
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
        entity_inputs: dict[str, EntityInput | list[EntityInput]],
        raw_inputs: dict[str, Primitive | list[Primitive]],
        requested_outputs: list[str] = [],
    ) -> dict[str, JSONValue]:
        sars_cov_2 = raw_inputs.get("sars_cov_2") or raw_inputs.get("creation_source") == "SARS-CoV-2 Upload"

        sequencing_read_input = entity_inputs["sequencing_read"]
        assert isinstance(sequencing_read_input, EntityInput)
        op = Operation(Query)
        sequencing_reads = op.sequencing_reads(
            where=SequencingReadWhereClause(id=UUIDComparators(_eq=sequencing_read_input.entity_id))
        )
        sequencing_reads.protocol()  # type: ignore
        sequencing_reads.technology()  # type: ignore
        sequencing_reads.clearlabs_export()  # type: ignore
        sequencing_reads.medaka_model()  # type: ignore
        self._fetch_file(sequencing_reads.primer_file().file())  # type: ignore

        if not sars_cov_2:
            accession_input = entity_inputs["accession"]
            assert isinstance(accession_input, EntityInput)
            accessions = op.accessions(where=AccessionWhereClause(id=UUIDComparators(_eq=accession_input.entity_id)))
            accessions.accession_id()  # type: ignore

        reference_genome_input = entity_inputs.get("reference_genome")
        if reference_genome_input:
            assert isinstance(reference_genome_input, EntityInput)
            reference_genomes = op.reference_genomes(
                where=ReferenceGenomeWhereClause(id=UUIDComparators(_eq=reference_genome_input.entity_id))
            )
            self._fetch_file(reference_genomes.file())  # type: ignore

        resp = self._entities_gql(op)
        sequencing_read = resp["sequencingReads"][0]
        primer_bed_uri = sequencing_read.get("primerFile") and self._uri_file(sequencing_read["primerFile"].get("file"))

        reference_fasta_uri = None
        if reference_genome_input:
            reference_genome = resp["referenceGenomes"][0]
            reference_fasta_uri = self._uri_file(reference_genome.get("file"))

        inputs: dict[str, JSONValue] = {}
        if sars_cov_2:
            inputs["ref_fasta"] = f"{PUBLIC_REFERENCES_PREFIX}/{SARS_COV_2_ACCESSION_ID}.fa"
            if sequencing_read["technology"] == "Nanopore":
                inputs["apply_length_filter"] = not sequencing_read["clearlabsExport"]
                inputs["medaka_model"] = sequencing_read["medakaModel"]
                # Remove ref_fasta once it's changed to an optional wdl input for ONT runs.
                inputs["primer_set"] = nanopore_primer_set(sequencing_read["protocol"])
                inputs["primer_schemes"] = f"{PUBLIC_REFERENCES_PREFIX}/artic-primer-schemes_v6.tar.gz"
            else:
                inputs["primer_bed"] = f"{PUBLIC_REFERENCES_PREFIX}/{illumina_primer_file(sequencing_read['protocol'])}"
        else:
            accession = resp["accessions"][0]
            inputs["ref_accession_id"] = accession["accessionId"]
            assert sequencing_read["technology"] == "Illumina", "Nanopore only supports SARS-CoV-2"

            if reference_genome_input:
                if reference_fasta_uri:
                    inputs["ref_fasta"] = reference_fasta_uri
                # Default to empty primer file if the user does not provide a primer bed file (optional input)
                inputs["primer_bed"] = primer_bed_uri or f"{PUBLIC_REFERENCES_PREFIX}/{NA_PRIMER_FILE}"
                # This option filters all except SARS-CoV-2 at the moment:
                inputs["filter_reads"] = False
                # signal to workflow that we want to include the refseq and bedfile in zipoutputs
                inputs["output_refseq"] = True
                inputs["output_bed"] = bool(primer_bed_uri)
            else:
                # This option filters all except SARS-CoV-2 at the moment:
                inputs["filter_reads"] = False
                # Use empty primer file b/c the user does not specify a wetlab protocol when dispatching
                #   cg samples from an mngs report
                inputs["primer_bed"] = f"{PUBLIC_REFERENCES_PREFIX}/{NA_PRIMER_FILE}"

        inputs["ref_host"] = f"{PUBLIC_REFERENCES_PREFIX}/hg38.fa.gz"
        inputs["ercc_fasta"] = f"{PUBLIC_REFERENCES_PREFIX}/ercc_sequences.fasta"
        inputs["kraken2_db_tar_gz"] = f"{PUBLIC_REFERENCES_PREFIX}/kraken_coronavirus_db_only.tar.gz"

        if os.getenv("ENVIRONMENT") == "test":
            # This is a smaller human host so host filtering will run faster for local testing
            inputs["ref_host"] = f"{PUBLIC_REFERENCES_PREFIX}/human_chr1.fa"
            for k, v in inputs.items():
                if not isinstance(v, str):
                    continue
                # Our test environment uses a local version of S3 for it's S3 downloads. This is good for samples but
                #   we don't want to copy over some reference files we host publicly because they are way too big. So by
                #   using their http style paths we hit the real bucket instead of the local one. It's a bit of a hack
                #   but it's a pretty clean way to handle this.
                inputs[k] = v.replace(
                    PUBLIC_REFERENCES_PREFIX, "https://czid-public-references.s3.amazonaws.com/consensus-genome"
                )
        print(inputs, file=sys.stderr)
        return inputs
