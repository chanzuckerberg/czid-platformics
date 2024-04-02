"""add deleted_at column

Revision ID: 20240319_125200
Revises: 20240314_095049
Create Date: 2024-03-19 19:52:01.144691

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20240319_125200"
down_revision = "20240314_095049"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("entity", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("entity", "deleted_at")
    # ### end Alembic commands ###
