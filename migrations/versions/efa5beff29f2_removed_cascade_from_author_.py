"""removed cascade from author relationship in book model

Revision ID: efa5beff29f2
Revises: d621682a6549
Create Date: 2022-07-23 13:39:54.215145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efa5beff29f2'
down_revision = 'd621682a6549'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
