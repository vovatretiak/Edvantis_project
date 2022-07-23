"""added column authors_id

Revision ID: ff956349abb2
Revises: 1f15f7153877
Create Date: 2022-07-23 10:29:42.159759

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff956349abb2'
down_revision = '1f15f7153877'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'author_book', 'books', ['book_id'], ['id'])
    op.add_column('books', sa.Column('authors_id', sa.ARRAY(sa.Integer()), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'authors_id')
    op.drop_constraint(None, 'author_book', type_='foreignkey')
    # ### end Alembic commands ###
