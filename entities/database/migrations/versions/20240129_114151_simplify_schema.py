"""simplify schema

Create Date: 2024-01-29 19:41:52.303789

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20240129_114151"
down_revision = "20240129_100617"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "bulk_download",
        sa.Column(
            "download_type", sa.Enum("concatenate", "zip", name="bulkdownloadtype", native_enum=False), nullable=False
        ),
        sa.Column("file_id", sa.UUID(), nullable=True),
        sa.Column("entity_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["entity_id"], ["entity.id"], name=op.f("fk_bulk_download_entity_id_entity")),
        sa.ForeignKeyConstraint(["file_id"], ["file.id"], name=op.f("fk_bulk_download_file_id_file")),
        sa.PrimaryKeyConstraint("entity_id", name=op.f("pk_bulk_download")),
    )
    op.create_table(
        "host_organism",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("version", sa.String(), nullable=False),
        sa.Column("host_filtering_id", sa.UUID(), nullable=True),
        sa.Column("sequence_id", sa.UUID(), nullable=True),
        sa.Column("entity_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["entity_id"], ["entity.id"], name=op.f("fk_host_organism_entity_id_entity")),
        sa.ForeignKeyConstraint(
            ["host_filtering_id"], ["file.id"], name=op.f("fk_host_organism_host_filtering_id_file")
        ),
        sa.ForeignKeyConstraint(["sequence_id"], ["file.id"], name=op.f("fk_host_organism_sequence_id_file")),
        sa.PrimaryKeyConstraint("entity_id", name=op.f("pk_host_organism")),
    )
    op.drop_index("sequence_alignment_index_index_file", table_name="sequence_alignment_index")
    op.drop_index("sequence_alignment_index_reference_genome", table_name="sequence_alignment_index")
    op.drop_table("sequence_alignment_index")
    op.add_column("consensus_genome", sa.Column("metrics_id", sa.UUID(), nullable=True))
    op.drop_index("consensus_genome_intermediate_outputs", table_name="consensus_genome")
    op.drop_index("consensus_genome_reference_genome", table_name="consensus_genome")
    op.drop_index("consensus_genome_sequence", table_name="consensus_genome")
    op.drop_index("consensus_genome_sequence_read", table_name="consensus_genome")
    op.create_foreign_key(
        op.f("fk_consensus_genome_metrics_id_metric_consensus_genome"),
        "consensus_genome",
        "metric_consensus_genome",
        ["metrics_id"],
        ["entity_id"],
    )
    op.drop_index("contig_sequencing_read", table_name="contig")
    op.add_column(
        "entity", sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False)
    )
    op.add_column("entity", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("entity", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    op.drop_index("entity_workflow", table_name="entity")
    op.drop_index("file_entity", table_name="file")
    op.alter_column("genomic_range", "reference_genome_id", existing_type=sa.UUID(), nullable=True)
    op.drop_index("genomic_range_file", table_name="genomic_range")
    op.drop_index("genomic_range_reference_genome", table_name="genomic_range")
    op.drop_index("metadatum_search", table_name="metadatum")
    op.drop_index("metadatum_unique", table_name="metadatum")
    op.add_column("metric_consensus_genome", sa.Column("coverage_breadth", sa.Float(), nullable=True))
    op.add_column("metric_consensus_genome", sa.Column("coverage_bin_size", sa.Float(), nullable=True))
    op.add_column("metric_consensus_genome", sa.Column("coverage_total_length", sa.Integer(), nullable=True))
    op.add_column(
        "metric_consensus_genome", sa.Column("coverage_viz", postgresql.JSONB(astext_type=sa.Text()), nullable=True)
    )
    op.drop_index("metric_consensus_genome_consensus_genome", table_name="metric_consensus_genome")
    op.drop_index("metric_consensus_genome_coverage_viz_summary", table_name="metric_consensus_genome")
    op.drop_constraint(
        "fk_metric_consensus_genome_coverage_viz_summary_file_id_file", "metric_consensus_genome", type_="foreignkey"
    )
    op.drop_column("metric_consensus_genome", "coverage_viz_summary_file_id")
    op.drop_index("phylo_tree_tree", table_name="phylogenetic_tree")
    op.drop_index("reference_genome_file", table_name="reference_genome")
    op.drop_index("reference_genome_file_index", table_name="reference_genome")
    op.drop_index("reference_genome_taxon", table_name="reference_genome")
    op.drop_constraint("fk_reference_genome_file_index_id_file", "reference_genome", type_="foreignkey")
    op.drop_column("reference_genome", "file_index_id")
    op.drop_column("reference_genome", "name")
    op.drop_column("reference_genome", "description")
    op.add_column("sample", sa.Column("rails_sample_id", sa.Integer(), nullable=True))
    op.alter_column("sample", "collection_date", existing_type=postgresql.TIMESTAMP(), nullable=False)
    op.drop_index("sample_host_taxon_id", table_name="sample")
    op.add_column("sequencing_read", sa.Column("clearlabs_export", sa.Boolean(), nullable=False))
    op.alter_column("sequencing_read", "protocol", existing_type=sa.VARCHAR(length=20), nullable=True)
    op.drop_index("sequencing_read_primer", table_name="sequencing_read")
    op.drop_index("sequencing_read_r1_file", table_name="sequencing_read")
    op.drop_index("sequencing_read_r2_file", table_name="sequencing_read")
    op.drop_index("sequencing_read_sample", table_name="sequencing_read")
    op.drop_index("sequencing_read_taxon", table_name="sequencing_read")
    op.drop_column("sequencing_read", "has_ercc")
    op.drop_index("taxon_class", table_name="taxon")
    op.drop_index("taxon_common_name", table_name="taxon")
    op.drop_index("taxon_family", table_name="taxon")
    op.drop_index("taxon_genus", table_name="taxon")
    op.drop_index("taxon_kingdom", table_name="taxon")
    op.drop_index("taxon_name", table_name="taxon")
    op.drop_index("taxon_order", table_name="taxon")
    op.drop_index("taxon_parent", table_name="taxon")
    op.drop_index("taxon_phylum", table_name="taxon")
    op.drop_index("taxon_species", table_name="taxon")
    op.drop_index("taxon_subspecies", table_name="taxon")
    op.drop_index("taxon_superkingdom", table_name="taxon")
    op.drop_index("taxon_upstream_database", table_name="taxon")
    op.drop_index("upstream_database_name", table_name="upstream_database")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index("upstream_database_name", "upstream_database", ["name"], unique=False)
    op.create_index("taxon_upstream_database", "taxon", ["upstream_database_id"], unique=False)
    op.create_index("taxon_superkingdom", "taxon", ["tax_superkingdom_id"], unique=False)
    op.create_index("taxon_subspecies", "taxon", ["tax_subspecies_id"], unique=False)
    op.create_index("taxon_species", "taxon", ["tax_species_id"], unique=False)
    op.create_index("taxon_phylum", "taxon", ["tax_phylum_id"], unique=False)
    op.create_index("taxon_parent", "taxon", ["tax_parent_id"], unique=False)
    op.create_index("taxon_order", "taxon", ["tax_order_id"], unique=False)
    op.create_index("taxon_name", "taxon", ["name"], unique=False)
    op.create_index("taxon_kingdom", "taxon", ["tax_kingdom_id"], unique=False)
    op.create_index("taxon_genus", "taxon", ["tax_genus_id"], unique=False)
    op.create_index("taxon_family", "taxon", ["tax_family_id"], unique=False)
    op.create_index("taxon_common_name", "taxon", ["common_name"], unique=False)
    op.create_index("taxon_class", "taxon", ["tax_class_id"], unique=False)
    op.add_column("sequencing_read", sa.Column("has_ercc", sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.create_index("sequencing_read_taxon", "sequencing_read", ["taxon_id"], unique=False)
    op.create_index("sequencing_read_sample", "sequencing_read", ["sample_id"], unique=False)
    op.create_index("sequencing_read_r2_file", "sequencing_read", ["r2_file_id"], unique=False)
    op.create_index("sequencing_read_r1_file", "sequencing_read", ["r1_file_id"], unique=False)
    op.create_index("sequencing_read_primer", "sequencing_read", ["primer_file_id"], unique=False)
    op.alter_column("sequencing_read", "protocol", existing_type=sa.VARCHAR(length=20), nullable=False)
    op.drop_column("sequencing_read", "clearlabs_export")
    op.create_index("sample_host_taxon_id", "sample", ["host_taxon_id"], unique=False)
    op.alter_column("sample", "collection_date", existing_type=postgresql.TIMESTAMP(), nullable=True)
    op.drop_column("sample", "rails_sample_id")
    op.add_column("reference_genome", sa.Column("description", sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column("reference_genome", sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column("reference_genome", sa.Column("file_index_id", sa.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key(
        "fk_reference_genome_file_index_id_file", "reference_genome", "file", ["file_index_id"], ["id"]
    )
    op.create_index("reference_genome_taxon", "reference_genome", ["taxon_id"], unique=False)
    op.create_index("reference_genome_file_index", "reference_genome", ["file_index_id"], unique=False)
    op.create_index("reference_genome_file", "reference_genome", ["file_id"], unique=False)
    op.create_index("phylo_tree_tree", "phylogenetic_tree", ["tree_id"], unique=False)
    op.add_column(
        "metric_consensus_genome",
        sa.Column("coverage_viz_summary_file_id", sa.UUID(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "fk_metric_consensus_genome_coverage_viz_summary_file_id_file",
        "metric_consensus_genome",
        "file",
        ["coverage_viz_summary_file_id"],
        ["id"],
    )
    op.create_index(
        "metric_consensus_genome_coverage_viz_summary",
        "metric_consensus_genome",
        ["coverage_viz_summary_file_id"],
        unique=False,
    )
    op.create_index(
        "metric_consensus_genome_consensus_genome", "metric_consensus_genome", ["consensus_genome_id"], unique=False
    )
    op.drop_column("metric_consensus_genome", "coverage_viz")
    op.drop_column("metric_consensus_genome", "coverage_total_length")
    op.drop_column("metric_consensus_genome", "coverage_bin_size")
    op.drop_column("metric_consensus_genome", "coverage_breadth")
    op.create_index("metadatum_unique", "metadatum", ["sample_id", "field_name"], unique=False)
    op.create_index("metadatum_search", "metadatum", ["sample_id", "field_name", "value"], unique=False)
    op.create_index("genomic_range_reference_genome", "genomic_range", ["reference_genome_id"], unique=False)
    op.create_index("genomic_range_file", "genomic_range", ["file_id"], unique=False)
    op.alter_column("genomic_range", "reference_genome_id", existing_type=sa.UUID(), nullable=False)
    op.create_index("file_entity", "file", ["entity_id"], unique=False)
    op.create_index("entity_workflow", "entity", ["collection_id", "producing_run_id", "owner_user_id"], unique=False)
    op.drop_column("entity", "deleted_at")
    op.drop_column("entity", "updated_at")
    op.drop_column("entity", "created_at")
    op.create_index("contig_sequencing_read", "contig", ["sequencing_read_id"], unique=False)
    op.drop_constraint(
        op.f("fk_consensus_genome_metrics_id_metric_consensus_genome"), "consensus_genome", type_="foreignkey"
    )
    op.create_index("consensus_genome_sequence_read", "consensus_genome", ["sequence_read_id"], unique=False)
    op.create_index("consensus_genome_sequence", "consensus_genome", ["sequence_id"], unique=False)
    op.create_index("consensus_genome_reference_genome", "consensus_genome", ["reference_genome_id"], unique=False)
    op.create_index(
        "consensus_genome_intermediate_outputs", "consensus_genome", ["intermediate_outputs_id"], unique=False
    )
    op.drop_column("consensus_genome", "metrics_id")
    op.create_table(
        "sequence_alignment_index",
        sa.Column("index_file_id", sa.UUID(), autoincrement=False, nullable=True),
        sa.Column("reference_genome_id", sa.UUID(), autoincrement=False, nullable=True),
        sa.Column("tool", sa.VARCHAR(length=21), autoincrement=False, nullable=False),
        sa.Column("entity_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("version", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(["entity_id"], ["entity.id"], name="fk_sequence_alignment_index_entity_id_entity"),
        sa.ForeignKeyConstraint(["index_file_id"], ["file.id"], name="fk_sequence_alignment_index_index_file_id_file"),
        sa.ForeignKeyConstraint(
            ["reference_genome_id"],
            ["reference_genome.entity_id"],
            name="fk_sequence_alignment_index_reference_genome_id_referen_f08b",
        ),
        sa.PrimaryKeyConstraint("entity_id", name="pk_sequence_alignment_index"),
    )
    op.create_index(
        "sequence_alignment_index_reference_genome", "sequence_alignment_index", ["reference_genome_id"], unique=False
    )
    op.create_index("sequence_alignment_index_index_file", "sequence_alignment_index", ["index_file_id"], unique=False)
    op.drop_table("host_organism")
    op.drop_table("bulk_download")
    # ### end Alembic commands ###
