"""add relationship indexes

Create Date: 2024-01-29 15:06:17.946251

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "20240129_100617"
down_revision = "20240118_122742"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index("entity_workflow", "entity", ["collection_id", "producing_run_id", "owner_user_id"], unique=False)

    op.create_index("sample_host_taxon_id", "sample", ["host_taxon_id"], unique=False)

    op.create_index("sequencing_read_r1_file", "sequencing_read", ["r1_file_id"], unique=False)
    op.create_index("sequencing_read_r2_file", "sequencing_read", ["r2_file_id"], unique=False)
    op.create_index("sequencing_read_taxon", "sequencing_read", ["taxon_id"], unique=False)
    op.create_index("sequencing_read_primer", "sequencing_read", ["primer_file_id"], unique=False)
    op.create_index("sequencing_read_sample", "sequencing_read", ["sample_id"], unique=False)

    op.create_index("consensus_genome_sequence_read", "consensus_genome", ["sequence_read_id"], unique=False)
    op.create_index("consensus_genome_reference_genome", "consensus_genome", ["reference_genome_id"], unique=False)
    op.create_index("consensus_genome_sequence", "consensus_genome", ["sequence_id"], unique=False)
    op.create_index(
        "consensus_genome_intermediate_outputs", "consensus_genome", ["intermediate_outputs_id"], unique=False
    )

    op.create_index("contig_sequencing_read", "contig", ["sequencing_read_id"], unique=False)

    op.create_index("file_entity", "file", ["entity_id"], unique=False)

    op.create_index("genomic_range_file", "genomic_range", ["file_id"], unique=False)
    op.create_index("genomic_range_reference_genome", "genomic_range", ["reference_genome_id"], unique=False)

    op.create_index(
        "metric_consensus_genome_coverage_viz_summary",
        "metric_consensus_genome",
        ["coverage_viz_summary_file_id"],
        unique=False,
    )
    op.create_index(
        "metric_consensus_genome_consensus_genome", "metric_consensus_genome", ["consensus_genome_id"], unique=False
    )

    op.create_index("phylo_tree_tree", "phylogenetic_tree", ["tree_id"], unique=False)

    op.create_index("reference_genome_file", "reference_genome", ["file_id"], unique=False)
    op.create_index("reference_genome_file_index", "reference_genome", ["file_index_id"], unique=False)
    op.create_index("reference_genome_taxon", "reference_genome", ["taxon_id"], unique=False)

    op.create_index("sequence_alignment_index_index_file", "sequence_alignment_index", ["index_file_id"], unique=False)
    op.create_index(
        "sequence_alignment_index_reference_genome", "sequence_alignment_index", ["reference_genome_id"], unique=False
    )

    op.create_index("upstream_database_name", "upstream_database", ["name"], unique=False)

    op.create_index("taxon_name", "taxon", ["name"], unique=False)
    op.create_index("taxon_common_name", "taxon", ["common_name"], unique=False)
    op.create_index("taxon_upstream_database", "taxon", ["upstream_database_id"], unique=False)
    op.create_index("taxon_parent", "taxon", ["tax_parent_id"], unique=False)
    op.create_index("taxon_subspecies", "taxon", ["tax_subspecies_id"], unique=False)
    op.create_index("taxon_species", "taxon", ["tax_species_id"], unique=False)
    op.create_index("taxon_genus", "taxon", ["tax_genus_id"], unique=False)
    op.create_index("taxon_family", "taxon", ["tax_family_id"], unique=False)
    op.create_index("taxon_order", "taxon", ["tax_order_id"], unique=False)
    op.create_index("taxon_class", "taxon", ["tax_class_id"], unique=False)
    op.create_index("taxon_phylum", "taxon", ["tax_phylum_id"], unique=False)
    op.create_index("taxon_kingdom", "taxon", ["tax_kingdom_id"], unique=False)
    op.create_index("taxon_superkingdom", "taxon", ["tax_superkingdom_id"], unique=False)


def downgrade() -> None:
    op.drop_index("entity_workflow", "entity")

    op.drop_index("sample_host_taxon_id", "sample")

    op.drop_index("sequencing_read_r1_file", "sequencing_read")
    op.drop_index("sequencing_read_r2_file", "sequencing_read")
    op.drop_index("sequencing_read_taxon", "sequencing_read")
    op.drop_index("sequencing_read_primer", "sequencing_read")
    op.drop_index("sequencing_read_sample", "sequencing_read")

    op.drop_index("consensus_genome_sequence_read", "consensus_genome")
    op.drop_index("consensus_genome_reference_genome", "consensus_genome")
    op.drop_index("consensus_genome_sequence", "consensus_genome")
    op.drop_index("consensus_genome_intermediate_outputs", "consensus_genome")

    op.drop_index("contig_sequencing_read", "contig")

    op.drop_index("file_entity", "file")

    op.drop_index("genomic_range_file", "genomic_range")
    op.drop_index("genomic_range_reference_genome", "genomic_range")

    op.drop_index(
        "metric_consensus_genome_coverage_viz_summary",
        "metric_consensus_genome",
    )
    op.drop_index("metric_consensus_genome_consensus_genome", "metric_consensus_genome")

    op.drop_index("phylo_tree_tree", "phylogenetic_tree")

    op.drop_index("reference_genome_file", "reference_genome")
    op.drop_index("reference_genome_file_index", "reference_genome")
    op.drop_index("reference_genome_taxon", "reference_genome")

    op.drop_index("sequence_alignment_index_index_file", "sequence_alignment_index")
    op.drop_index("sequence_alignment_index_reference_genome", "sequence_alignment_index")

    op.drop_index("upstream_database_name", "upstream_database")

    op.drop_index("taxon_name", "taxon")
    op.drop_index("taxon_common_name", "taxon")
    op.drop_index("taxon_upstream_database", "taxon")
    op.drop_index("taxon_parent", "taxon")
    op.drop_index("taxon_subspecies", "taxon")
    op.drop_index("taxon_species", "taxon")
    op.drop_index("taxon_genus", "taxon")
    op.drop_index("taxon_family", "taxon")
    op.drop_index("taxon_order", "taxon")
    op.drop_index("taxon_class", "taxon")
    op.drop_index("taxon_phylum", "taxon")
    op.drop_index("taxon_kingdom", "taxon")
    op.drop_index("taxon_superkingdom", "taxon")
