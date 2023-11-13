"""

Create Date: 2023-11-13 17:20:16.846615

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '20231113_092015'
down_revision = '20231109_103318'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sequencing_read', 'r1_file_id',
               existing_type=sa.UUID(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sequencing_read', 'r1_file_id',
               existing_type=sa.UUID(),
               nullable=False)
    # ### end Alembic commands ###
