"""update schema

Create Date: 2023-12-14 18:32:29.297622

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20231214_104536"
down_revision = "20231129_095753"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "phylogenetic_tree",
        sa.Column("tree_id", sa.UUID(), nullable=True),
        sa.Column(
            "format",
            sa.Enum("newick", "auspice_v1", "auspice_v2", name="phylogenetictreeformat", native_enum=False),
            nullable=False,
        ),
        sa.Column("entity_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["entity_id"], ["entity.id"], name=op.f("fk_phylogenetic_tree_entity_id_entity")),
        sa.ForeignKeyConstraint(["tree_id"], ["file.id"], name=op.f("fk_phylogenetic_tree_tree_id_file")),
        sa.PrimaryKeyConstraint("entity_id", name=op.f("pk_phylogenetic_tree")),
    )
    op.drop_column("consensus_genome", "is_reverse_complement")
    op.add_column(
        "file",
        sa.Column(
            "upload_client",
            sa.Enum("browser", "cli", "s3", "basespace", name="fileuploadclient", native_enum=False),
            nullable=True,
        ),
    )
    op.add_column("file", sa.Column("upload_error", sa.String(), nullable=True))
    op.alter_column(
        "file",
        "status",
        existing_type=postgresql.ENUM("SUCCESS", "FAILED", "PENDING", name="filestatus"),
        type_=sa.Enum("SUCCESS", "FAILED", "PENDING", name="filestatus", native_enum=False),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("phylogenetic_tree")
    op.alter_column(
        "file",
        "status",
        existing_type=sa.Enum("SUCCESS", "FAILED", "PENDING", name="filestatus", native_enum=False),
        type_=postgresql.ENUM("SUCCESS", "FAILED", "PENDING", name="filestatus"),
        existing_nullable=False,
    )
    op.drop_column("file", "upload_error")
    op.drop_column("file", "upload_client")
    op.add_column(
        "consensus_genome", sa.Column("is_reverse_complement", sa.BOOLEAN(), autoincrement=False, nullable=False)
    )
    # ### end Alembic commands ###
