"""
Supported GraphQL queries for files and entities

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/queries.py.j2 instead.
"""

import strawberry
from strawberry import relay
from typing import Sequence, List
from api.files import File, resolve_files
from api.types.sample import Sample, resolve_samples
from api.types.sequencing_read import SequencingRead, resolve_sequencing_reads
from api.types.genomic_range import GenomicRange, resolve_genomic_ranges
from api.types.reference_genome import ReferenceGenome, resolve_reference_genomes
from api.types.sequence_alignment_index import SequenceAlignmentIndex, resolve_sequence_alignment_indices
from api.types.metadatum import Metadatum, resolve_metadatas
from api.types.metadata_field import MetadataField, resolve_metadata_fields
from api.types.metadata_field_project import MetadataFieldProject, resolve_metadata_field_projects
from api.types.consensus_genome import ConsensusGenome, resolve_consensus_genomes
from api.types.metric_consensus_genome import MetricConsensusGenome, resolve_metrics_consensus_genomes, MetricConsensusGenomeAggregate, resolve_metrics_consensus_genomes_aggregate
from api.types.coverage_viz import CoverageViz, resolve_coverage_vizes
from api.types.taxon import Taxon, resolve_taxa
from api.types.upstream_database import UpstreamDatabase, resolve_upstream_databases
from api.types.contig import Contig, resolve_contigs
from api.types.phylogenetic_tree import PhylogeneticTree, resolve_phylogenetic_trees


@strawberry.type
class Query:
    # Allow relay-style queries by node ID
    node: relay.Node = relay.node()
    nodes: List[relay.Node] = relay.node()
    # Query files
    files: Sequence[File] = resolve_files

    # Query entities
    samples: Sequence[Sample] = resolve_samples
    sequencing_reads: Sequence[SequencingRead] = resolve_sequencing_reads
    genomic_ranges: Sequence[GenomicRange] = resolve_genomic_ranges
    reference_genomes: Sequence[ReferenceGenome] = resolve_reference_genomes
    sequence_alignment_indices: Sequence[SequenceAlignmentIndex] = resolve_sequence_alignment_indices
    metadatas: Sequence[Metadatum] = resolve_metadatas
    metadata_fields: Sequence[MetadataField] = resolve_metadata_fields
    metadata_field_projects: Sequence[MetadataFieldProject] = resolve_metadata_field_projects
    consensus_genomes: Sequence[ConsensusGenome] = resolve_consensus_genomes
    metrics_consensus_genomes: Sequence[MetricConsensusGenome] = resolve_metrics_consensus_genomes
    aggregate_metrics_consensus_genomes: Sequence[MetricConsensusGenomeAggregate] = resolve_metrics_consensus_genomes_aggregate
    coverage_vizes: Sequence[CoverageViz] = resolve_coverage_vizes
    taxa: Sequence[Taxon] = resolve_taxa
    upstream_databases: Sequence[UpstreamDatabase] = resolve_upstream_databases
    contigs: Sequence[Contig] = resolve_contigs
    phylogenetic_trees: Sequence[PhylogeneticTree] = resolve_phylogenetic_trees
