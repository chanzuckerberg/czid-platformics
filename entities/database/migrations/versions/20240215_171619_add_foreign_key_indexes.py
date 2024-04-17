"""add foreign key indexes

Create Date: 2024-02-15 22:16:21.182335

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "20240215_171619"
down_revision = "20240215_134243"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f("ix_accession_upstream_database_id"), "accession", ["upstream_database_id"], unique=False)
    op.create_index(op.f("ix_bulk_download_file_id"), "bulk_download", ["file_id"], unique=False)
    op.create_index(op.f("ix_consensus_genome_accession_id"), "consensus_genome", ["accession_id"], unique=False)
    op.create_index(
        op.f("ix_consensus_genome_intermediate_outputs_id"),
        "consensus_genome",
        ["intermediate_outputs_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_consensus_genome_reference_genome_id"), "consensus_genome", ["reference_genome_id"], unique=False
    )
    op.create_index(op.f("ix_consensus_genome_sequence_id"), "consensus_genome", ["sequence_id"], unique=False)
    op.create_index(
        op.f("ix_consensus_genome_sequence_read_id"), "consensus_genome", ["sequence_read_id"], unique=False
    )
    op.create_index(op.f("ix_consensus_genome_taxon_id"), "consensus_genome", ["taxon_id"], unique=False)
    op.create_index(op.f("ix_genomic_range_file_id"), "genomic_range", ["file_id"], unique=False)
    op.create_index(op.f("ix_host_organism_sequence_id"), "host_organism", ["sequence_id"], unique=False)
    op.create_index(op.f("ix_index_file_file_id"), "index_file", ["file_id"], unique=False)
    op.create_index(op.f("ix_index_file_host_organism_id"), "index_file", ["host_organism_id"], unique=False)
    op.create_index(op.f("ix_index_file_upstream_database_id"), "index_file", ["upstream_database_id"], unique=False)
    op.create_index(op.f("ix_metadatum_sample_id"), "metadatum", ["sample_id"], unique=False)
    op.create_index(
        op.f("ix_metric_consensus_genome_consensus_genome_id"),
        "metric_consensus_genome",
        ["consensus_genome_id"],
        unique=False,
    )
    op.create_index(op.f("ix_phylogenetic_tree_tree_id"), "phylogenetic_tree", ["tree_id"], unique=False)
    op.create_index(op.f("ix_reference_genome_file_id"), "reference_genome", ["file_id"], unique=False)
    op.create_index(op.f("ix_sample_host_organism_id"), "sample", ["host_organism_id"], unique=False)
    op.create_index(op.f("ix_sequencing_read_primer_file_id"), "sequencing_read", ["primer_file_id"], unique=False)
    op.create_index(op.f("ix_sequencing_read_r1_file_id"), "sequencing_read", ["r1_file_id"], unique=False)
    op.create_index(op.f("ix_sequencing_read_r2_file_id"), "sequencing_read", ["r2_file_id"], unique=False)
    op.create_index(op.f("ix_sequencing_read_sample_id"), "sequencing_read", ["sample_id"], unique=False)
    op.create_index(op.f("ix_sequencing_read_taxon_id"), "sequencing_read", ["taxon_id"], unique=False)
    op.create_index(op.f("ix_taxon_tax_class_id"), "taxon", ["tax_class_id"], unique=False)
    op.create_index(op.f("ix_taxon_tax_family_id"), "taxon", ["tax_family_id"], unique=False)
    op.create_index(op.f("ix_taxon_tax_genus_id"), "taxon", ["tax_genus_id"], unique=False)
    op.create_index(op.f("ix_taxon_tax_kingdom_id"), "taxon", ["tax_kingdom_id"], unique=False)
    op.create_index(op.f("ix_taxon_tax_order_id"), "taxon", ["tax_order_id"], unique=False)
    op.create_index(op.f("ix_taxon_tax_parent_id"), "taxon", ["tax_parent_id"], unique=False)
    op.create_index(op.f("ix_taxon_tax_phylum_id"), "taxon", ["tax_phylum_id"], unique=False)
    op.create_index(op.f("ix_taxon_tax_species_id"), "taxon", ["tax_species_id"], unique=False)
    op.create_index(op.f("ix_taxon_tax_subspecies_id"), "taxon", ["tax_subspecies_id"], unique=False)
    op.create_index(op.f("ix_taxon_tax_superkingdom_id"), "taxon", ["tax_superkingdom_id"], unique=False)
    op.create_index(op.f("ix_taxon_upstream_database_id"), "taxon", ["upstream_database_id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_taxon_upstream_database_id"), table_name="taxon")
    op.drop_index(op.f("ix_taxon_tax_superkingdom_id"), table_name="taxon")
    op.drop_index(op.f("ix_taxon_tax_subspecies_id"), table_name="taxon")
    op.drop_index(op.f("ix_taxon_tax_species_id"), table_name="taxon")
    op.drop_index(op.f("ix_taxon_tax_phylum_id"), table_name="taxon")
    op.drop_index(op.f("ix_taxon_tax_parent_id"), table_name="taxon")
    op.drop_index(op.f("ix_taxon_tax_order_id"), table_name="taxon")
    op.drop_index(op.f("ix_taxon_tax_kingdom_id"), table_name="taxon")
    op.drop_index(op.f("ix_taxon_tax_genus_id"), table_name="taxon")
    op.drop_index(op.f("ix_taxon_tax_family_id"), table_name="taxon")
    op.drop_index(op.f("ix_taxon_tax_class_id"), table_name="taxon")
    op.drop_index(op.f("ix_sequencing_read_taxon_id"), table_name="sequencing_read")
    op.drop_index(op.f("ix_sequencing_read_sample_id"), table_name="sequencing_read")
    op.drop_index(op.f("ix_sequencing_read_r2_file_id"), table_name="sequencing_read")
    op.drop_index(op.f("ix_sequencing_read_r1_file_id"), table_name="sequencing_read")
    op.drop_index(op.f("ix_sequencing_read_primer_file_id"), table_name="sequencing_read")
    op.drop_index(op.f("ix_sample_host_organism_id"), table_name="sample")
    op.drop_index(op.f("ix_reference_genome_file_id"), table_name="reference_genome")
    op.drop_index(op.f("ix_phylogenetic_tree_tree_id"), table_name="phylogenetic_tree")
    op.drop_index(op.f("ix_metric_consensus_genome_consensus_genome_id"), table_name="metric_consensus_genome")
    op.drop_index(op.f("ix_metadatum_sample_id"), table_name="metadatum")
    op.drop_index(op.f("ix_index_file_upstream_database_id"), table_name="index_file")
    op.drop_index(op.f("ix_index_file_host_organism_id"), table_name="index_file")
    op.drop_index(op.f("ix_index_file_file_id"), table_name="index_file")
    op.drop_index(op.f("ix_host_organism_sequence_id"), table_name="host_organism")
    op.drop_index(op.f("ix_genomic_range_file_id"), table_name="genomic_range")
    op.drop_index(op.f("ix_consensus_genome_taxon_id"), table_name="consensus_genome")
    op.drop_index(op.f("ix_consensus_genome_sequence_read_id"), table_name="consensus_genome")
    op.drop_index(op.f("ix_consensus_genome_sequence_id"), table_name="consensus_genome")
    op.drop_index(op.f("ix_consensus_genome_reference_genome_id"), table_name="consensus_genome")
    op.drop_index(op.f("ix_consensus_genome_intermediate_outputs_id"), table_name="consensus_genome")
    op.drop_index(op.f("ix_consensus_genome_accession_id"), table_name="consensus_genome")
    op.drop_index(op.f("ix_bulk_download_file_id"), table_name="bulk_download")
    op.drop_index(op.f("ix_accession_upstream_database_id"), table_name="accession")
    # ### end Alembic commands ###
