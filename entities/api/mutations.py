"""
GraphQL mutations for files and entities

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/mutations.py.j2 instead.
"""

import strawberry
from typing import Sequence
from api.files import (
    File,
    create_file,
    upload_file,
    mark_upload_complete,
    concatenate_files,
    SignedURL,
    MultipartUploadResponse,
)
from api.types.sample import Sample, create_sample, update_sample, delete_sample
from api.types.sequencing_read import (
    SequencingRead,
    create_sequencing_read,
    update_sequencing_read,
    delete_sequencing_read,
)
from api.types.genomic_range import GenomicRange, create_genomic_range, delete_genomic_range
from api.types.reference_genome import (
    ReferenceGenome,
    create_reference_genome,
    update_reference_genome,
    delete_reference_genome,
)
from api.types.accession import Accession, create_accession, update_accession, delete_accession
from api.types.host_organism import HostOrganism, create_host_organism, update_host_organism, delete_host_organism
from api.types.metadatum import Metadatum, create_metadatum, update_metadatum, delete_metadatum
from api.types.consensus_genome import ConsensusGenome, create_consensus_genome, delete_consensus_genome
from api.types.metric_consensus_genome import (
    MetricConsensusGenome,
    create_metric_consensus_genome,
    delete_metric_consensus_genome,
)
from api.types.taxon import Taxon, create_taxon, update_taxon, delete_taxon
from api.types.upstream_database import (
    UpstreamDatabase,
    create_upstream_database,
    update_upstream_database,
    delete_upstream_database,
)
from api.types.index_file import IndexFile, create_index_file, update_index_file, delete_index_file
from api.types.bulk_download import BulkDownload, create_bulk_download, delete_bulk_download


@strawberry.type
class Mutation:
    # File mutations
    create_file: File = create_file
    upload_file: MultipartUploadResponse = upload_file
    mark_upload_complete: File = mark_upload_complete
    concatenate_files: SignedURL = concatenate_files

    # Sample mutations
    create_sample: Sample = create_sample
    update_sample: Sequence[Sample] = update_sample
    delete_sample: Sequence[Sample] = delete_sample

    # SequencingRead mutations
    create_sequencing_read: SequencingRead = create_sequencing_read
    update_sequencing_read: Sequence[SequencingRead] = update_sequencing_read
    delete_sequencing_read: Sequence[SequencingRead] = delete_sequencing_read

    # GenomicRange mutations
    create_genomic_range: GenomicRange = create_genomic_range
    delete_genomic_range: Sequence[GenomicRange] = delete_genomic_range

    # ReferenceGenome mutations
    create_reference_genome: ReferenceGenome = create_reference_genome
    update_reference_genome: Sequence[ReferenceGenome] = update_reference_genome
    delete_reference_genome: Sequence[ReferenceGenome] = delete_reference_genome

    # Accession mutations
    create_accession: Accession = create_accession
    update_accession: Sequence[Accession] = update_accession
    delete_accession: Sequence[Accession] = delete_accession

    # HostOrganism mutations
    create_host_organism: HostOrganism = create_host_organism
    update_host_organism: Sequence[HostOrganism] = update_host_organism
    delete_host_organism: Sequence[HostOrganism] = delete_host_organism

    # Metadatum mutations
    create_metadatum: Metadatum = create_metadatum
    update_metadatum: Sequence[Metadatum] = update_metadatum
    delete_metadatum: Sequence[Metadatum] = delete_metadatum

    # ConsensusGenome mutations
    create_consensus_genome: ConsensusGenome = create_consensus_genome
    delete_consensus_genome: Sequence[ConsensusGenome] = delete_consensus_genome

    # MetricConsensusGenome mutations
    create_metric_consensus_genome: MetricConsensusGenome = create_metric_consensus_genome
    delete_metric_consensus_genome: Sequence[MetricConsensusGenome] = delete_metric_consensus_genome

    # Taxon mutations
    create_taxon: Taxon = create_taxon
    update_taxon: Sequence[Taxon] = update_taxon
    delete_taxon: Sequence[Taxon] = delete_taxon

    # UpstreamDatabase mutations
    create_upstream_database: UpstreamDatabase = create_upstream_database
    update_upstream_database: Sequence[UpstreamDatabase] = update_upstream_database
    delete_upstream_database: Sequence[UpstreamDatabase] = delete_upstream_database

    # IndexFile mutations
    create_index_file: IndexFile = create_index_file
    update_index_file: Sequence[IndexFile] = update_index_file
    delete_index_file: Sequence[IndexFile] = delete_index_file

    # BulkDownload mutations
    create_bulk_download: BulkDownload = create_bulk_download
    delete_bulk_download: Sequence[BulkDownload] = delete_bulk_download
