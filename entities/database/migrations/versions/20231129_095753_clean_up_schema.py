"""clean up schema

Create Date: 2023-11-29 17:57:54.448640

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20231129_095753"
down_revision = "20231128_095750"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("coverage_viz")
    op.drop_constraint("fk_consensus_genome_genomic_range_id_genomic_range", "consensus_genome", type_="foreignkey")
    op.drop_column("consensus_genome", "genomic_range_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("consensus_genome", sa.Column("genomic_range_id", sa.UUID(), autoincrement=False, nullable=False))
    op.create_foreign_key(
        "fk_consensus_genome_genomic_range_id_genomic_range",
        "consensus_genome",
        "genomic_range",
        ["genomic_range_id"],
        ["entity_id"],
    )
    op.create_table(
        "coverage_viz",
        sa.Column("accession_id", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("coverage_viz_file_id", sa.UUID(), autoincrement=False, nullable=True),
        sa.Column("entity_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["coverage_viz_file_id"], ["file.id"], name="fk_coverage_viz_coverage_viz_file_id_file"
        ),
        sa.ForeignKeyConstraint(["entity_id"], ["entity.id"], name="fk_coverage_viz_entity_id_entity"),
        sa.PrimaryKeyConstraint("entity_id", name="pk_coverage_viz"),
    )
    # ### end Alembic commands ###
