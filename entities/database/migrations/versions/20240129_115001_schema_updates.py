"""schema updates

Create Date: 2024-01-29 19:50:02.582750

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20240129_115001"
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
    op.create_foreign_key(
        op.f("fk_consensus_genome_metrics_id_metric_consensus_genome"),
        "consensus_genome",
        "metric_consensus_genome",
        ["metrics_id"],
        ["entity_id"],
    )
    op.add_column(
        "entity", sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False)
    )
    op.add_column("entity", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("entity", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    op.alter_column("genomic_range", "reference_genome_id", existing_type=sa.UUID(), nullable=True)
    op.add_column("metric_consensus_genome", sa.Column("coverage_breadth", sa.Float(), nullable=True))
    op.add_column("metric_consensus_genome", sa.Column("coverage_bin_size", sa.Float(), nullable=True))
    op.add_column("metric_consensus_genome", sa.Column("coverage_total_length", sa.Integer(), nullable=True))
    op.add_column(
        "metric_consensus_genome", sa.Column("coverage_viz", postgresql.JSONB(astext_type=sa.Text()), nullable=True)
    )
    op.drop_index("metric_consensus_genome_coverage_viz_summary", table_name="metric_consensus_genome")
    op.drop_constraint(
        "fk_metric_consensus_genome_coverage_viz_summary_file_id_file", "metric_consensus_genome", type_="foreignkey"
    )
    op.drop_column("metric_consensus_genome", "coverage_viz_summary_file_id")
    op.drop_index("reference_genome_file_index", table_name="reference_genome")
    op.drop_constraint("fk_reference_genome_file_index_id_file", "reference_genome", type_="foreignkey")
    op.drop_column("reference_genome", "description")
    op.drop_column("reference_genome", "file_index_id")
    op.drop_column("reference_genome", "name")
    op.add_column("sample", sa.Column("rails_sample_id", sa.Integer(), nullable=True))
    op.alter_column("sample", "collection_date", existing_type=postgresql.TIMESTAMP(), nullable=False)
    op.add_column("sequencing_read", sa.Column("clearlabs_export", sa.Boolean(), nullable=False))
    op.alter_column("sequencing_read", "protocol", existing_type=sa.VARCHAR(length=20), nullable=True)
    op.drop_column("sequencing_read", "has_ercc")
    # ### end Alembic commands ###


def downgrade() -> None:
    # sequence_alignment_index_index_file
    # sequence_alignment_index_reference_genome
    # metric_consensus_genome_coverage_viz_summary
    # reference_genome_file_index

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("sequencing_read", sa.Column("has_ercc", sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.alter_column("sequencing_read", "protocol", existing_type=sa.VARCHAR(length=20), nullable=False)
    op.drop_column("sequencing_read", "clearlabs_export")
    op.alter_column("sample", "collection_date", existing_type=postgresql.TIMESTAMP(), nullable=True)
    op.drop_column("sample", "rails_sample_id")
    op.add_column("reference_genome", sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column("reference_genome", sa.Column("file_index_id", sa.UUID(), autoincrement=False, nullable=True))
    op.add_column("reference_genome", sa.Column("description", sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_foreign_key(
        "fk_reference_genome_file_index_id_file", "reference_genome", "file", ["file_index_id"], ["id"]
    )
    op.create_index("reference_genome_file_index", "reference_genome", ["file_index_id"], unique=False)
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
    op.drop_column("metric_consensus_genome", "coverage_viz")
    op.drop_column("metric_consensus_genome", "coverage_total_length")
    op.drop_column("metric_consensus_genome", "coverage_bin_size")
    op.drop_column("metric_consensus_genome", "coverage_breadth")
    op.alter_column("genomic_range", "reference_genome_id", existing_type=sa.UUID(), nullable=False)
    op.drop_column("entity", "deleted_at")
    op.drop_column("entity", "updated_at")
    op.drop_column("entity", "created_at")
    op.drop_constraint(
        op.f("fk_consensus_genome_metrics_id_metric_consensus_genome"), "consensus_genome", type_="foreignkey"
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