"""empty message

Revision ID: 390124097051
Revises: 87fda7b5f1a9
Create Date: 2021-08-18 22:00:41.116679

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '390124097051'
down_revision = '87fda7b5f1a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('confirmed', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('confirmed')

    # ### end Alembic commands ###
