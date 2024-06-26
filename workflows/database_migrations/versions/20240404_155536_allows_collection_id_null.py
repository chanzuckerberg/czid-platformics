"""allows collection id null

Revision ID: 20240404_155536
Revises: 20240319_125200
Create Date: 2024-04-04 22:55:41.701986

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20240404_155536"
down_revision = "20240319_125200"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("entity", "collection_id", existing_type=sa.INTEGER(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("entity", "collection_id", existing_type=sa.INTEGER(), nullable=False)
    # ### end Alembic commands ###
