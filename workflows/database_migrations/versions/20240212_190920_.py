"""schema changes

Revision ID: 20240212_190920
Revises: 20240204_202551
Create Date: 2024-02-13 00:09:21.350560

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20240212_190920"
down_revision = "20240204_202551"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("entity", "producing_run_id")
    op.add_column("entity", sa.Column("producing_run_id", sa.UUID(), nullable=True))


def downgrade() -> None:
    op.drop_column("entity", "producing_run_id")
    op.add_column("entity", sa.Column("producing_run_id", sa.INTEGER(), nullable=True))
