"""add status enum

Create Date: 2023-09-01 22:17:04.686898

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20230901_151704"
down_revision = "20230828_141240"
branch_labels = None
depends_on = None


def upgrade() -> None:
    sa.Enum("AWAITING_UPLOAD", "UPLOAD_COMPLETE", "UPLOAD_FAILURE", "UPLOAD_SUCCESS", name="filestatus").create(
        op.get_bind()
    )
    op.drop_column("file", "status")
    op.add_column(
        "file",
        sa.Column(
            "status",
            postgresql.ENUM(
                "AWAITING_UPLOAD", "UPLOAD_COMPLETE", "UPLOAD_FAILURE", "UPLOAD_SUCCESS", name="filestatus"
            ),
            nullable=True,
        ),
    )
    update_file_status_sql = sa.sql.text("UPDATE file SET status = 'AWAITING_UPLOAD'")
    op.get_bind().execute(update_file_status_sql)
    op.alter_column("file", "entity_id", existing_type=postgresql.ENUM(name="filestatus"), nullable=False)
    op.alter_column("file", "entity_id", existing_type=sa.UUID(), nullable=False)
    op.alter_column("file", "entity_field_name", existing_type=sa.VARCHAR(), nullable=False)


def downgrade() -> None:
    op.drop_column("file", "status")
    op.add_column("file", sa.Column("status", sa.VARCHAR(), autoincrement=False, nullable=False))
    op.alter_column("file", "entity_field_name", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("file", "entity_id", existing_type=sa.UUID(), nullable=True)
    sa.Enum("AWAITING_UPLOAD", "UPLOAD_COMPLETE", "UPLOAD_FAILURE", "UPLOAD_SUCCESS", name="filestatus").drop(
        op.get_bind()
    )
