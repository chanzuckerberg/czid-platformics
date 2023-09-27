"""make outputs_json nullable

Revision ID: 20230914_095805
Revises: 20230913_105933
Create Date: 2023-09-14 16:58:08.065217

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20230914_095805"
down_revision = "20230913_105933"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("run", "outputs_json", existing_type=sa.VARCHAR(), nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("run", "outputs_json", existing_type=sa.VARCHAR(), nullable=True)
    # ### end Alembic commands ###
