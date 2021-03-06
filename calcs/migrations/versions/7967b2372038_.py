"""empty message

Revision ID: 7967b2372038
Revises: a59b8f3ba13d
Create Date: 2020-11-19 03:48:37.747048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7967b2372038'
down_revision = 'a59b8f3ba13d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('last_login', sa.DateTime(), nullable=False))
    op.drop_column('user', 'password_hash')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password_hash', sa.VARCHAR(length=80), autoincrement=False, nullable=False))
    op.drop_column('user', 'last_login')
    # ### end Alembic commands ###
