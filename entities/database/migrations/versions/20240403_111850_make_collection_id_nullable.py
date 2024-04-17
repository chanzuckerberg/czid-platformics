"""make collection_id nullable

Create Date: 2024-04-03 18:18:51.311681

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20240403_111850"
down_revision = "20240325_134907"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("entity", "collection_id", existing_type=sa.Integer(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("entity", "collection_id", existing_type=sa.Integer(), nullable=False)
    # ### end Alembic commands ###
