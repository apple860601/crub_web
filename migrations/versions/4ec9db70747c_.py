"""empty message

Revision ID: 4ec9db70747c
Revises: da2cf897ad19
Create Date: 2021-07-21 01:53:05.893128

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4ec9db70747c'
down_revision = 'da2cf897ad19'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('itemname', schema=None) as batch_op:
        batch_op.alter_column('imageurl',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=150),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('itemname', schema=None) as batch_op:
        batch_op.alter_column('imageurl',
               existing_type=sa.String(length=150),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=True)

    # ### end Alembic commands ###