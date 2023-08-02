"""initial_commit

Revision ID: 20230724_215129
Revises: 
Create Date: 2023-07-24 21:51:29.973699

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '20230724_215129'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('workflow',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('version', sa.String(), nullable=False),
    sa.Column('minimum_supported_version', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_workflow'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('workflow')
    # ### end Alembic commands ###