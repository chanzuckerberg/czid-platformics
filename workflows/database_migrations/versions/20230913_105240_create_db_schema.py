"""create db schema

Revision ID: 20230913_105240
Revises: 
Create Date: 2023-09-13 17:52:41.279976

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '20230913_105240'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('workflow',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('default_version', sa.String(), nullable=False),
    sa.Column('minimum_supported_version', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_workflow'))
    )
    op.create_table('workflow_version',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('workflow_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['workflow_id'], ['workflow.id'], name=op.f('fk_workflow_version_workflow_id_workflow')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_workflow_version'))
    )
    op.create_table('run',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('started_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('ended_at', sa.DateTime(), nullable=True),
    sa.Column('execution_id', sa.String(), nullable=False),
    sa.Column('inputs_json', sa.String(), nullable=False),
    sa.Column('outputs_json', sa.String(), nullable=True),
    sa.Column('status', sa.Enum('PENDING', 'STARTED', 'RUNNING', 'SUCCEEDED', 'FAILED', name='runstatus'), nullable=False),
    sa.Column('workflow_version_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['workflow_version_id'], ['workflow_version.id'], name=op.f('fk_run_workflow_version_id_workflow_version')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_run'))
    )
    op.create_table('run_entity_input',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('run_id', sa.Integer(), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('field_name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['run_id'], ['run.id'], name=op.f('fk_run_entity_input_run_id_run')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_run_entity_input'))
    )
    op.create_table('run_step',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('run_id', sa.Integer(), nullable=False),
    sa.Column('started_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('ended_at', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('SUCCEEDED', 'FAILED', name='runstepstatus'), nullable=True),
    sa.ForeignKeyConstraint(['run_id'], ['run.id'], name=op.f('fk_run_step_run_id_run')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_run_step'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('run_step')
    op.drop_table('run_entity_input')
    op.drop_table('run')
    op.drop_table('workflow_version')
    op.drop_table('workflow')
    # ### end Alembic commands ###