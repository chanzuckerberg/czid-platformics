"""add collection id to entities

Create Date: 2023-08-09 18:16:34.638266

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20230809_181634"
down_revision = "20230801_223219"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("entity", sa.Column("collection_id", sa.Integer(), nullable=False))
    op.alter_column("entity", "owner_user_id", existing_type=sa.INTEGER(), nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("entity", "owner_user_id", existing_type=sa.INTEGER(), nullable=True)
    op.drop_column("entity", "collection_id")
    # ### end Alembic commands ###
