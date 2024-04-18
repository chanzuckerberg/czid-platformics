"""add error label to workflow run

Revision ID: 20240418_151754
Revises: 20240404_155536
Create Date: 2024-04-18 22:17:57.238944

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '20240418_151754'
down_revision = '20240404_155536'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('workflow_run', sa.Column('error_label', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('workflow_run', 'error_label')
    # ### end Alembic commands ###
