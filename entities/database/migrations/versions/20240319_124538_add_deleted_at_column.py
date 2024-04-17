"""add deleted_at column

Create Date: 2024-03-19 19:45:39.201620

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20240319_124538"
down_revision = "20240228_115942"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("entity", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("entity", "deleted_at")
    # ### end Alembic commands ###
