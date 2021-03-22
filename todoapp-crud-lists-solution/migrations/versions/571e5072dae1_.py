"""empty message

Revision ID: 571e5072dae1
Revises: 
Create Date: 2019-08-07 15:14:56.911676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "571e5072dae1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("todolists")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "todolists",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="todolists_pkey"),
    )
    # ### end Alembic commands ###