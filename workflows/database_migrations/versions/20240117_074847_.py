"""

Revision ID: 20240117_074847
Revises: 20231205_155329
Create Date: 2024-01-17 15:48:49.512125

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20240117_074847"
down_revision = "20231205_155329"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("workflow_version", sa.Column("workflow_uri", sa.String(), nullable=True))
    op.add_column("workflow_version", sa.Column("version", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("workflow_version", "version")
    op.drop_column("workflow_version", "workflow_uri")
    # ### end Alembic commands ###
