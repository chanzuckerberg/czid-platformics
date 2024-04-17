"""

Create Date: 2023-11-16 22:30:49.667820

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20231116_143049"
down_revision = "20231113_092015"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("consensus_genome", "sequence_id", existing_type=sa.UUID(), nullable=True)
    op.alter_column("coverage_viz", "coverage_viz_file_id", existing_type=sa.UUID(), nullable=True)
    op.alter_column("genomic_range", "file_id", existing_type=sa.UUID(), nullable=True)
    op.alter_column("metric_consensus_genome", "coverage_viz_summary_file_id", existing_type=sa.UUID(), nullable=True)
    op.alter_column("reference_genome", "file_id", existing_type=sa.UUID(), nullable=True)
    op.alter_column("sequence_alignment_index", "index_file_id", existing_type=sa.UUID(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("sequence_alignment_index", "index_file_id", existing_type=sa.UUID(), nullable=False)
    op.alter_column("reference_genome", "file_id", existing_type=sa.UUID(), nullable=False)
    op.alter_column("metric_consensus_genome", "coverage_viz_summary_file_id", existing_type=sa.UUID(), nullable=False)
    op.alter_column("genomic_range", "file_id", existing_type=sa.UUID(), nullable=False)
    op.alter_column("coverage_viz", "coverage_viz_file_id", existing_type=sa.UUID(), nullable=False)
    op.alter_column("consensus_genome", "sequence_id", existing_type=sa.UUID(), nullable=False)
    # ### end Alembic commands ###
