"""added book, author, review models

Revision ID: cbbb57c7a858
Revises: 
Create Date: 2022-07-27 17:02:39.419208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbbb57c7a858'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
    op.add_column('author_book', sa.Column('book_id', sa.Integer(), nullable=True))
    op.drop_constraint('author_book_books_id_fkey', 'author_book', type_='foreignkey')
    op.create_foreign_key(None, 'author_book', 'books', ['book_id'], ['id'])
    op.drop_column('author_book', 'books_id')
    op.add_column('reviews', sa.Column('username', sa.String(), nullable=False))
    op.drop_constraint('reviews_user_id_fkey', 'reviews', type_='foreignkey')
    op.drop_column('reviews', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reviews', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('reviews_user_id_fkey', 'reviews', 'users', ['user_id'], ['id'])
    op.drop_column('reviews', 'username')
    op.add_column('author_book', sa.Column('books_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'author_book', type_='foreignkey')
    op.create_foreign_key('author_book_books_id_fkey', 'author_book', 'books', ['books_id'], ['id'])
    op.drop_column('author_book', 'book_id')
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='users_pkey')
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    # ### end Alembic commands ###
