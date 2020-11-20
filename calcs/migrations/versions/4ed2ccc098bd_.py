"""empty message

Revision ID: 4ed2ccc098bd
Revises: d1ebafbd5d3a
Create Date: 2020-11-19 03:57:31.972834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ed2ccc098bd'
down_revision = 'd1ebafbd5d3a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password_hash',
               existing_type=sa.TEXT(),
               type_=sa.String(length=120),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password_hash',
               existing_type=sa.String(length=120),
               type_=sa.TEXT(),
               existing_nullable=False)
    # ### end Alembic commands ###