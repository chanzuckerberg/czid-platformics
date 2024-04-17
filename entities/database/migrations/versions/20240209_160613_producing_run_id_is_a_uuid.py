"""Producing run ID is a uuid

Create Date: 2024-02-09 21:14:55.260756

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20240209_160613"
down_revision = "20240209_112845"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("entity", "producing_run_id")
    op.add_column("entity", sa.Column("producing_run_id", sa.UUID(), nullable=True))


def downgrade() -> None:
    op.drop_column("entity", "producing_run_id")
    op.add_column("entity", sa.Column("producing_run_id", sa.INTEGER(), nullable=True))
