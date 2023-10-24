"""optional_file_size

Create Date: 2023-09-29 18:06:21.469244

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20230929_110616"
down_revision = "20230921_114754"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("file", "entity_field_name", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("file", "size", existing_type=sa.INTEGER(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("file", "size", existing_type=sa.INTEGER(), nullable=False)
    op.alter_column("file", "entity_field_name", existing_type=sa.VARCHAR(), nullable=True)
    # ### end Alembic commands ###
