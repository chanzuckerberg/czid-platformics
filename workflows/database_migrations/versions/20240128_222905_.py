"""

Revision ID: 20240128_222905
Revises: 20240117_074847
Create Date: 2024-01-29 06:29:07.718340

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20240128_222905"
down_revision = "20240117_074847"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "workflow_run",
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("ended_at", sa.DateTime(), nullable=True),
        sa.Column("execution_id", sa.String(), nullable=True),
        sa.Column("outputs_json", sa.String(), nullable=True),
        sa.Column("workflow_runner_inputs_json", sa.String(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "SUCCEEDED", "FAILED", "PENDING", "STARTED", "RUNNING", name="workflowrunstatus", native_enum=False
            ),
            nullable=True,
        ),
        sa.Column("workflow_version_id", sa.UUID(), nullable=True),
        sa.Column("raw_inputs_json", sa.String(), nullable=True),
        sa.Column("deprecated_by_id", sa.UUID(), nullable=True),
        sa.Column("entity_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["deprecated_by_id"], ["workflow_run.entity_id"], name=op.f("fk_workflow_run_deprecated_by_id_workflow_run")
        ),
        sa.ForeignKeyConstraint(["entity_id"], ["entity.id"], name=op.f("fk_workflow_run_entity_id_entity")),
        sa.ForeignKeyConstraint(
            ["workflow_version_id"],
            ["workflow_version.entity_id"],
            name=op.f("fk_workflow_run_workflow_version_id_workflow_version"),
        ),
        sa.PrimaryKeyConstraint("entity_id", name=op.f("pk_workflow_run")),
    )
    op.create_table(
        "workflow_run_entity_input",
        sa.Column("input_entity_id", sa.UUID(), nullable=True),
        sa.Column("field_name", sa.String(), nullable=True),
        sa.Column("workflow_run_id", sa.UUID(), nullable=True),
        sa.Column("entity_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["entity_id"], ["entity.id"], name=op.f("fk_workflow_run_entity_input_entity_id_entity")
        ),
        sa.ForeignKeyConstraint(
            ["workflow_run_id"],
            ["workflow_run.entity_id"],
            name=op.f("fk_workflow_run_entity_input_workflow_run_id_workflow_run"),
        ),
        sa.PrimaryKeyConstraint("entity_id", name=op.f("pk_workflow_run_entity_input")),
    )
    op.create_table(
        "workflow_run_step",
        sa.Column("workflow_run_id", sa.UUID(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("ended_at", sa.DateTime(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("RUNNING", "SUCCEEDED", "FAILED", name="workflowrunstepstatus", native_enum=False),
            nullable=True,
        ),
        sa.Column("entity_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["entity_id"], ["entity.id"], name=op.f("fk_workflow_run_step_entity_id_entity")),
        sa.ForeignKeyConstraint(
            ["workflow_run_id"],
            ["workflow_run.entity_id"],
            name=op.f("fk_workflow_run_step_workflow_run_id_workflow_run"),
        ),
        sa.PrimaryKeyConstraint("entity_id", name=op.f("pk_workflow_run_step")),
    )
    op.drop_table("run_step")
    op.drop_table("run_entity_input")
    op.drop_table("run")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "run",
        sa.Column("started_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.Column("ended_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.Column("execution_id", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("outputs_json", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("inputs_json", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("status", sa.VARCHAR(length=9), autoincrement=False, nullable=True),
        sa.Column("workflow_version_id", sa.UUID(), autoincrement=False, nullable=True),
        sa.Column("entity_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(["entity_id"], ["entity.id"], name="fk_run_entity_id_entity"),
        sa.ForeignKeyConstraint(
            ["workflow_version_id"], ["workflow_version.entity_id"], name="fk_run_workflow_version_id_workflow_version"
        ),
        sa.PrimaryKeyConstraint("entity_id", name="pk_run"),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "run_entity_input",
        sa.Column("new_entity_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("field_name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("run_id", sa.UUID(), autoincrement=False, nullable=True),
        sa.Column("entity_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(["entity_id"], ["entity.id"], name="fk_run_entity_input_entity_id_entity"),
        sa.ForeignKeyConstraint(["run_id"], ["run.entity_id"], name="fk_run_entity_input_run_id_run"),
        sa.PrimaryKeyConstraint("entity_id", name="pk_run_entity_input"),
    )
    op.create_table(
        "run_step",
        sa.Column("run_id", sa.UUID(), autoincrement=False, nullable=True),
        sa.Column("started_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.Column("ended_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.Column("status", sa.VARCHAR(length=9), autoincrement=False, nullable=True),
        sa.Column("entity_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(["entity_id"], ["entity.id"], name="fk_run_step_entity_id_entity"),
        sa.ForeignKeyConstraint(["run_id"], ["run.entity_id"], name="fk_run_step_run_id_run"),
        sa.PrimaryKeyConstraint("entity_id", name="pk_run_step"),
    )
    op.drop_table("workflow_run_step")
    op.drop_table("workflow_run_entity_input")
    op.drop_table("workflow_run")
    # ### end Alembic commands ###
