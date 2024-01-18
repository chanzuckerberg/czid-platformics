"""update metadata schema

Create Date: 2024-01-18 17:27:45.080812

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20240118_122742"
down_revision = "20240109_152706"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("metadatum", sa.Column("field_name", sa.String(), nullable=False))
    op.drop_constraint("fk_metadatum_metadata_field_id_metadata_field", "metadatum", type_="foreignkey")
    op.execute(
        """UPDATE metadatum md SET field_name = mf.field_name FROM
           metadata_field mf WHERE md.metadata_field_id = mf.entity_id"""
    )
    op.drop_column("metadatum", "metadata_field_id")
    op.drop_table("metadata_field_project")
    op.drop_table("metadata_field")
    op.execute("""CREATE COLLATION natural_sort (provider = icu, locale = 'en@colNumeric=yes')""")
    op.execute("""ALTER TABLE metadatum ALTER COLUMN value TYPE VARCHAR COLLATE natural_sort""")
    op.create_index("metadatum_search", "metadatum", ["sample_id", "field_name", "value"])
    op.create_index("metadatum_unique", "metadatum", ["sample_id", "field_name"], unique=True)


def downgrade() -> None:
    op.execute("""ALTER TABLE metadatum ALTER COLUMN value TYPE VARCHAR COLLATE "default" """)
    op.execute("""DROP COLLATION natural_sort""")
    op.add_column("metadatum", sa.Column("metadata_field_id", sa.UUID(), autoincrement=False, nullable=False))
    op.create_foreign_key(
        "fk_metadatum_metadata_field_id_metadata_field",
        "metadatum",
        "metadata_field",
        ["metadata_field_id"],
        ["entity_id"],
    )
    op.drop_column("metadatum", "field_name")
    op.create_table(
        "metadata_field",
        sa.Column("field_name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("description", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("field_type", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("is_required", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("options", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("default_value", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("entity_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(["entity_id"], ["entity.id"], name="fk_metadata_field_entity_id_entity"),
        sa.PrimaryKeyConstraint("entity_id", name="pk_metadata_field"),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "metadata_field_project",
        sa.Column("project_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("metadata_field_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("entity_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(["entity_id"], ["entity.id"], name="fk_metadata_field_project_entity_id_entity"),
        sa.ForeignKeyConstraint(
            ["metadata_field_id"],
            ["metadata_field.entity_id"],
            name="fk_metadata_field_project_metadata_field_id_metadata_field",
        ),
        sa.PrimaryKeyConstraint("entity_id", name="pk_metadata_field_project"),
    )
