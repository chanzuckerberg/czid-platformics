"""add tables to workflow schema

Revision ID: 20230810_235656
Revises: 20230724_215129
Create Date: 2023-08-10 23:57:31.583905

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '20230810_235656'
down_revision = '20230724_215129'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('workflow_version',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('version', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('package_uri', sa.String(), nullable=False),
    sa.Column('beta', sa.Boolean(), nullable=False),
    sa.Column('deprecated', sa.Boolean(), nullable=False),
    sa.Column('graph_json', sa.String(), nullable=True),
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
    op.create_table('workflow_version_input',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('workflow_version_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('entity_type', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['workflow_version_id'], ['workflow_version.id'], name=op.f('fk_workflow_version_input_workflow_version_id_workflow_version')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_workflow_version_input'))
    )
    op.create_table('workflow_version_output',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('workflow_version_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('output_type', sa.String(), nullable=False),
    sa.Column('output_type_version', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['workflow_version_id'], ['workflow_version.id'], name=op.f('fk_workflow_version_output_workflow_version_id_workflow_version')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_workflow_version_output'))
    )
    op.create_table('run_entity_input',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('run_id', sa.Integer(), nullable=False),
    sa.Column('workflow_version_input_id', sa.Integer(), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['run_id'], ['run.id'], name=op.f('fk_run_entity_input_run_id_run')),
    sa.ForeignKeyConstraint(['workflow_version_input_id'], ['workflow_version_input.id'], name=op.f('fk_run_entity_input_workflow_version_input_id_workflow_version_input')),
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
    op.add_column('workflow', sa.Column('default_version', sa.String(), nullable=False))
    op.drop_column('workflow', 'version')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('workflow', sa.Column('version', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('workflow', 'default_version')
    op.drop_table('run_step')
    op.drop_table('run_entity_input')
    op.drop_table('workflow_version_output')
    op.drop_table('workflow_version_input')
    op.drop_table('run')
    op.drop_table('workflow_version')
    # ### end Alembic commands ###
