"""
Populate the database with mock data for local development
"""
import json
from datetime import datetime
from typing import Any
from urllib.parse import urlparse

from database.models.accession import Accession
from database.models.file import File
from database.models.genomic_range import GenomicRange
from database.models.host_organism import HostOrganism
from database.models.index_file import IndexFile
from database.models.reference_genome import ReferenceGenome
from database.models.sample import Sample
from database.models.sequencing_read import SequencingRead
from database.models.taxon import Taxon
from database.models.upstream_database import UpstreamDatabase

from platformics.util.seed_utils import (
    TEST_USER_ID,
    TEST_COLLECTION_ID,
    LOCAL_BUCKET,
    SeedSession,
    TempCZIDWorkflowFile,
)
from platformics.database.models.base import Entity
from support.enums import HostOrganismCategory, NucleicAcid, SequencingProtocol, SequencingTechnology, TaxonLevel


def main() -> tuple[list[dict[str, str]], dict[str, str]]:
    """
    An idempotent seed script to create the minimum viable set of entities to run consensus genomes

    It also creates entity and raw inputs to run the consensus genome workflow
    """
    session = SeedSession()

    def uri_file(uri: str, entity: Entity, entity_field_name: str, file_format: str) -> File:
        parsed = urlparse(uri)
        file = getattr(entity, entity_field_name) or File()
        file.entity_id = entity.id
        file.entity_field_name = entity_field_name
        file.status = "SUCCESS"
        file.protocol = parsed.scheme
        file.namespace = parsed.netloc
        file.path = parsed.path.lstrip("/")
        file.file_format = file_format
        return file

    def entity_input(name: str, entity_type: str, entity: Entity) -> tuple[dict[str, Any], Entity]:
        return {"name": name, "entity_type": entity_type}, entity

    entity_inputs: list[tuple[dict[str, str], Entity]] = []
    raw_inputs = {}

    """
    System entities
    """
    session.transfer_to_local("s3://czid-public-references/consensus-genome/vadr-models-sarscov2-1.2-2.tar.gz")
    session.transfer_to_local("s3://czid-public-references/consensus-genome/artic-primer-schemes_v2.tar.gz")
    session.transfer_to_local("s3://czid-public-references/consensus-genome/na_primers.bed")

    upstream_database = session.create_or_fetch_entity(UpstreamDatabase, name="ncbi")

    sars_cov2_accession = session.create_or_fetch_entity(Accession, accession_id="MN908947.3")
    sars_cov2_accession.accession_name = (
        "Severe acute respiratory syndrome coronavirus 2 isolate Wuhan-Hu-1, complete genome"
    )
    upstream_database.accessions = [sars_cov2_accession]
    entity_inputs.append(entity_input("accession", "accession", sars_cov2_accession))

    sars_cov2_taxon = session.create_or_fetch_entity(Taxon, upstream_database_identifier="2697049")
    sars_cov2_taxon.name = "Severe acute respiratory syndrome coronavirus 2"
    sars_cov2_taxon.is_phage = False
    sars_cov2_taxon.level = TaxonLevel.level_subspecies
    upstream_database.taxa = [sars_cov2_taxon]
    entity_inputs.append(entity_input("taxon", "taxon", sars_cov2_taxon))

    ncbi_index_version = "2021-01-22"
    for n_ in ["nr", "nt"]:
        database_index_file = session.create_or_fetch_entity(IndexFile, name=n_, version="2021-01-22")
        # These are way too large to download but they are passed to the WDL as strings and only ranges
        #   of them are downloaded through a different mechanism than the WDL file downloads. This
        #   mechanism doesn't use mocked local S3 and the object is public so we can use the original S3 path
        #   without transfering it to local S3.
        database_index_file.file = uri_file(
            f"s3://czid-public-references/ncbi-indexes-prod/2021-01-22/index-generation-2/{n_}",
            database_index_file,
            "file",
            "fasta",
        )
        upstream_database.indexes.append(database_index_file)

        # These are too large to transfer to moto's local S3, it crashes when attempted but they are downloaded
        #   via WDL so if they were S3 paths they would not be found. By using HTTP WDL will use the non-mocked
        #   http downloader. These objects are also public.
        loc_path = f"https://czid-public-references.s3.amazonaws.com/ncbi-indexes-prod/2021-01-22/index-generation-2/{n_}_loc.marisa"
        loc_index_file = session.create_or_fetch_entity(IndexFile, name=f"{n_}_loc", version=ncbi_index_version)
        loc_index_file.file = uri_file(loc_path, loc_index_file, "file", "marisa")
        upstream_database.indexes.append(loc_index_file)
    # set this as a raw input
    raw_inputs["ncbi_index_version"] = ncbi_index_version

    session.add(upstream_database)

    human_host = session.create_or_fetch_entity(HostOrganism, name="human")
    human_host.version = "v1-hg38"
    human_host.category = HostOrganismCategory.human
    human_host.is_deuterostome = True
    session.add(human_host)

    sars_cov2_reference = session.create_or_fetch_entity(ReferenceGenome, name="MN908947.3")
    sars_cov2_reference.file = uri_file(
        "https://czid-public-references.s3.amazonaws.com/consensus-genome/MN908947.3.fa",
        sars_cov2_reference,
        "file",
        "fasta",
    )
    session.add(sars_cov2_reference)
    session.commit()

    with TempCZIDWorkflowFile("integration_test/sample_sars-cov-2_paired_r1.fastq.gz", "consensus-genome") as temp_file:
        session.s3_local.upload_file(
            temp_file.name, LOCAL_BUCKET, "consensus-genome-test/sample_sars-cov-2_paired_r1.fastq.gz"
        )
    with TempCZIDWorkflowFile("integration_test/sample_sars-cov-2_paired_r2.fastq.gz", "consensus-genome") as temp_file:
        session.s3_local.upload_file(
            temp_file.name, LOCAL_BUCKET, "consensus-genome-test/sample_sars-cov-2_paired_r2.fastq.gz"
        )

    sars_cov2_paired_name = "sample_sars-cov-2_paired"
    sars_cov2_paired_sample = session.query(Sample).filter_by(name=sars_cov2_paired_name).first() or Sample()
    sars_cov2_paired_sample.owner_user_id = TEST_USER_ID
    sars_cov2_paired_sample.collection_id = TEST_COLLECTION_ID
    sars_cov2_paired_sample.name = sars_cov2_paired_name
    sars_cov2_paired_sample.sample_type = "nasal"
    sars_cov2_paired_sample.water_control = False
    sars_cov2_paired_sample.collection_date = datetime(2021, 1, 1)
    sars_cov2_paired_sample.collection_location = "California, USA"
    entity_inputs.append(entity_input("sample", "sample", sars_cov2_paired_sample))
    session.add(sars_cov2_paired_sample)
    session.commit()

    sars_cov2_paired_sequencing_read = (
        session.session.query(SequencingRead).filter_by(sample_id=sars_cov2_paired_sample.id).first()
        or SequencingRead()
    )
    sars_cov2_paired_sequencing_read.owner_user_id = TEST_USER_ID
    sars_cov2_paired_sequencing_read.collection_id = TEST_COLLECTION_ID
    sars_cov2_paired_sequencing_read.protocol = SequencingProtocol.artic
    sars_cov2_paired_sequencing_read.technology = SequencingTechnology.Illumina
    sars_cov2_paired_sequencing_read.nucleic_acid = NucleicAcid.DNA
    sars_cov2_paired_sequencing_read.clearlabs_export = False
    sars_cov2_paired_sequencing_read.medaka_model = "r941_min_high_g360"
    sars_cov2_paired_sequencing_read.taxon = sars_cov2_taxon
    sars_cov2_paired_sequencing_read.r1_file = uri_file(
        f"s3://{LOCAL_BUCKET}/consensus-genome-test/sample_sars-cov-2_paired_r1.fastq.gz",
        sars_cov2_paired_sequencing_read,
        "r1_file",
        "fasta",
    )
    sars_cov2_paired_sequencing_read.r2_file = uri_file(
        f"s3://{LOCAL_BUCKET}/consensus-genome-test/sample_sars-cov-2_paired_r2.fastq.gz",
        sars_cov2_paired_sequencing_read,
        "r2_file",
        "fasta",
    )
    sars_cov2_paired_sample.sequencing_reads = [sars_cov2_paired_sequencing_read]
    session.add(sars_cov2_paired_sequencing_read)
    entity_inputs.append(entity_input("sequencing_read", "sequencing_read", sars_cov2_paired_sequencing_read))

    sars_cov2_paired_genomic_range = sars_cov2_paired_sequencing_read.primer_file or GenomicRange()
    sars_cov2_paired_genomic_range.owner_user_id = TEST_USER_ID
    sars_cov2_paired_genomic_range.collection_id = TEST_COLLECTION_ID
    sars_cov2_paired_genomic_range.file = uri_file(
        "https://czid-public-references.s3.amazonaws.com/consensus-genome/artic_v3_primers.bed",
        sars_cov2_paired_genomic_range,
        "file",
        "bed",
    )
    sars_cov2_paired_sequencing_read.primer_file = sars_cov2_paired_genomic_range
    session.add(sars_cov2_paired_sample)
    session.flush()
    session.commit()

    return [dict(entity_id=str(entity.id), **d) for d, entity in entity_inputs], raw_inputs


if __name__ == "__main__":
    print("Seeding database for consensus genomes workflow")
    entity_inputs, raw_inputs = main()
    print("entityInputs", json.dumps(entity_inputs, indent=2))
    print("rawInputs", json.dumps(raw_inputs, indent=2))
    print("Seeding complete")
