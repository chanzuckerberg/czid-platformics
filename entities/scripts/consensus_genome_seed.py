"""
Populate the database with mock data for local development
"""
import json
import os
import shutil
import subprocess
import tempfile
from datetime import datetime
from os.path import join
from typing import Any, TypeVar

import boto3
from botocore.client import Config, UNSIGNED
from botocore.compat import urlparse
from database.models.accession import Accession
from database.models.genomic_range import GenomicRange
from database.models.reference_genome import ReferenceGenome

from platformics.database.connect import init_sync_db
from platformics.database.models.base import Entity
from platformics.settings import CLISettings
from database.models import File, Sample, SequencingRead, Taxon, UpstreamDatabase, IndexFile, HostOrganism


TEST_USER_ID = "111"
TEST_COLLECTION_ID = "444"
LOCAL_BUCKET = "local-bucket"


class TempGitRepo:
    def __init__(self, repo_url: str, tag: str):
        self.repo_url = repo_url
        self.tag = tag
        self.temp_dir = tempfile.mkdtemp()
        # Clone the repo at the specific tag into the temporary directory
        subprocess.check_call(['git', 'clone', '--branch', tag, '--depth', '1', repo_url, self.temp_dir])

    def __enter__(self):
        return self.temp_dir

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.temp_dir)


def main() -> tuple[list[dict[str, str]], dict[str, Any]]:
    """
    An idempotent seed script to create the minimum viable set of entities to run consensus genomes

    It also creates entity and raw inputs to run the consensus genome workflow
    """
    settings = CLISettings.model_validate({})
    app_db = init_sync_db(settings.SYNC_DB_URI)
    session = app_db.session()
    s3_local = boto3.client('s3', endpoint_url=os.getenv("BOTO_ENDPOINT_URL"), config=Config(s3={'addressing_style': 'path'}))
    s3_remote = boto3.client('s3', config=Config(signature_version=UNSIGNED))

    T = TypeVar('T', bound=Entity)
    def create_or_fetch(entity_type: type[T], **kwargs) -> T:
        entity = session.query(entity_type).filter_by(**kwargs).first() or entity_type()
        entity.owner_user_id = TEST_USER_ID
        entity.collection_id = TEST_COLLECTION_ID
        for name, value in kwargs.items():
            setattr(entity, name, value)
        return entity

    def uri_file(uri: str, maybe_file: File | None, entity_field_name: str, file_format: str) -> File:
        parsed = urlparse(uri)
        file = maybe_file or File()
        file.entity_field_name = entity_field_name
        file.status = "SUCCESS"
        file.protocol = parsed.scheme
        file.namespace = parsed.netloc
        file.path = parsed.path.lstrip("/")
        file.file_format = file_format
        return file

    def create_bucket(bucket: str) -> None:
        if any(bucket["Name"] == bucket for bucket in s3_local.list_buckets().get("Buckets", [])):
            return
        s3_local.create_bucket(Bucket=bucket)

    def transfer_to_local(s3_path: str) -> None:
        parsed = urlparse(s3_path)
        bucket, key = parsed.netloc, parsed.path.lstrip("/")
        create_bucket(bucket)

        if s3_local.list_objects_v2(Bucket=bucket, Prefix=key)["KeyCount"] > 0:
            return

        with tempfile.NamedTemporaryFile() as f:
            print(f"Transfering {s3_path}")
            s3_remote.download_file(bucket, key, f.name)
            s3_local.upload_file(f.name, bucket, key)

    def entity_input(name: str, entity_type: str, entity_id: str) -> dict[str, str]:
        return { "name": name, "entity_type": entity_type, "entity_id": entity_id }

    create_bucket(LOCAL_BUCKET)

    # Transfer some S3 reference files to our local version of the public references bucket
    #   These are not associated with entities
    transfer_to_local("s3://czid-public-references/consensus-genome/vadr-models-sarscov2-1.2-2.tar.gz")
    transfer_to_local("s3://czid-public-references/consensus-genome/kraken_coronavirus_db_only.tar.gz")
    transfer_to_local("s3://czid-public-references/consensus-genome/artic-primer-schemes_v2.tar.gz")
    transfer_to_local("s3://czid-public-references/consensus-genome/na_primers.bed")

    entity_inputs = []
    raw_inputs = {}

    """
    System entities
    """
    upstream_database = create_or_fetch(UpstreamDatabase, name="ncbi")

    sars_cov2_accession = create_or_fetch(Accession, accession_id="MN908947.3")
    sars_cov2_accession.accession_name = "Severe acute respiratory syndrome coronavirus 2 isolate Wuhan-Hu-1, complete genome"
    upstream_database.accessions = [sars_cov2_accession]
    entity_inputs.append(entity_input("accession", "accession", str(sars_cov2_accession.entity_id)))

    sars_cov2_taxon = create_or_fetch(Taxon, upstream_database_identifier="2697049")
    sars_cov2_taxon.name = "Severe acute respiratory syndrome coronavirus 2"
    sars_cov2_taxon.is_phage = False
    sars_cov2_taxon.level = "level_subspecies"
    upstream_database.taxa = [sars_cov2_taxon]
    entity_inputs.append(entity_input("taxon", "taxon", str(sars_cov2_taxon.entity_id)))

    ncbi_index_version = "2021-01-22"
    for n_ in ["nr", "nt"]:
        database_index_file = create_or_fetch(IndexFile, name=n_, version="2021-01-22")
        # These are way too large to download but they are passed to the WDL as strings and only ranges
        #   of them are downloaded through a different mechanism than the WDL file downloads. This
        #   mechanism doesn't use mocked local S3 and the object is public so we can use the original S3 path
        #   without transfering it to local S3.
        database_index_file.file = uri_file(
            f"s3://czid-public-references/ncbi-indexes-prod/2021-01-22/index-generation-2/{n_}",
            database_index_file.file,
            "file",
            "fasta",
        )
        upstream_database.indexes.append(database_index_file)

        # These are too large to transfer to moto's local S3, it crashes when attempted but they are downloaded
        #   via WDL so if they were S3 paths they would not be found. By using HTTP WDL will use the non-mocked
        #   http downloader. These objects are also public.
        loc_path = f"https://czid-public-references.s3.amazonaws.com/ncbi-indexes-prod/2021-01-22/index-generation-2/{n_}_loc.marisa"
        loc_index_file = create_or_fetch(IndexFile, name=f"{n_}_loc", version=ncbi_index_version)
        loc_index_file.file = uri_file(loc_path, loc_index_file.file, "file", "marisa")
        upstream_database.indexes.append(loc_index_file)
    # set this as a raw input
    raw_inputs["ncbi_index_version"] = ncbi_index_version



    session.add(upstream_database)

    human_host = create_or_fetch(HostOrganism, name="human")
    human_host.version = "v1-hg38"
    human_host.category = ""
    human_host.is_deuterostome = True
    human_host.sequence = uri_file(
        "https://czid-public-references.s3.amazonaws.com/consensus-genome/hg38.fa.gz",
        human_host.sequence,
        "sequence",
        "fasta",
    )
    session.add(human_host)

    sars_cov2_reference = create_or_fetch(ReferenceGenome, name="MN908947.3")
    sars_cov2_reference.file = uri_file(
        "https://czid-public-references.s3.amazonaws.com/consensus-genome/MN908947.3.fa",
        sars_cov2_reference.file,
        "file",
        "fasta",
    )
    session.add(sars_cov2_reference)

    session.commit()


    with TempGitRepo('https://github.com/chanzuckerberg/czid-workflows.git', 'main') as temp_dir:
        shutil.copy(join(temp_dir, "workflows/consensus-genome/integration_test/sample_sars-cov-2_paired_r1.fastq.gz"), "sample_sars-cov-2_paired_r1.fastq.gz")
        shutil.copy(join(temp_dir, "workflows/consensus-genome/integration_test/sample_sars-cov-2_paired_r2.fastq.gz"), "sample_sars-cov-2_paired_r2.fastq.gz")
        s3_local.upload_file("sample_sars-cov-2_paired_r1.fastq.gz", "local-bucket", "consensus-genome-test/sample_sars-cov-2_paired_r1.fastq.gz")
        s3_local.upload_file("sample_sars-cov-2_paired_r2.fastq.gz", "local-bucket", "consensus-genome-test/sample_sars-cov-2_paired_r2.fastq.gz")

        sars_cov2_paired_name = "sample_sars-cov-2_paired"
        sars_cov2_paired_sample = session.query(Sample).filter_by(name=sars_cov2_paired_name).first() or Sample()
        sars_cov2_paired_sample.owner_user_id=TEST_USER_ID
        sars_cov2_paired_sample.collection_id=TEST_COLLECTION_ID
        sars_cov2_paired_sample.name=sars_cov2_paired_name
        sars_cov2_paired_sample.sample_type="nasal"
        sars_cov2_paired_sample.water_control=False
        sars_cov2_paired_sample.collection_date=datetime(2021, 1, 1)
        sars_cov2_paired_sample.collection_location="California, USA"
        entity_inputs.append(entity_input("sample", "sample", str(sars_cov2_paired_sample.entity_id)))

        sars_cov2_paired_sequencing_read = SequencingRead()
        if sars_cov2_paired_sample.entity_id:
            sars_cov2_paired_sequencing_read = session.query(SequencingRead).filter_by(sample_id=sars_cov2_paired_sample.entity_id).first() or SequencingRead()
        sars_cov2_paired_sequencing_read.owner_user_id = TEST_USER_ID
        sars_cov2_paired_sequencing_read.collection_id = TEST_COLLECTION_ID
        sars_cov2_paired_sequencing_read.protocol = "artic_v3"
        sars_cov2_paired_sequencing_read.technology = "Illumina"
        sars_cov2_paired_sequencing_read.nucleic_acid = "DNA"
        sars_cov2_paired_sequencing_read.clearlabs_export = False
        sars_cov2_paired_sequencing_read.medaka_model = "r941_min_high_g360"
        sars_cov2_paired_sequencing_read.taxon = sars_cov2_taxon
        sars_cov2_paired_sample.sequencing_reads = [sars_cov2_paired_sequencing_read]
        entity_inputs.append(entity_input("sequencing_read", "sequencing_read", str(sars_cov2_paired_sequencing_read.entity_id)))

        sars_cov2_paired_genomic_range = GenomicRange()
        if sars_cov2_paired_sequencing_read.entity_id:
            sars_cov2_paired_genomic_range = session.query(GenomicRange).filter_by(sequencing_read_id=sars_cov2_paired_sequencing_read.entity_id).first() or GenomicRange()
        sars_cov2_paired_genomic_range.file = uri_file(
            "https://czid-public-references.s3.amazonaws.com/consensus-genome/artic_v3_primers.bed",
             sars_cov2_paired_genomic_range.file,
            "file",
            "bed",
        )
        sars_cov2_paired_sequencing_read.primer_file = sars_cov2_paired_genomic_range
        session.add(sars_cov2_paired_sample)

    session.commit()
    return entity_inputs, raw_inputs


if __name__ == "__main__":
    print("Seeding database")
    entity_inputs, raw_inputs = main()
    print("entityInputs", json.dumps(entity_inputs, indent=2))
    print("rawInputs", json.dumps(raw_inputs, indent=2))
    print("Seeding complete")
