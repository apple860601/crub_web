"""empty message

Revision ID: da2cf897ad19
Revises: 
Create Date: 2021-07-07 12:29:10.275258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da2cf897ad19'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Price',
    sa.Column('itemid', sa.String(length=100), nullable=False),
    sa.Column('minprice', sa.Integer(), nullable=True),
    sa.Column('maxprice', sa.Integer(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('itemid')
    )
    op.create_table('Shop',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('shop', sa.String(length=10), nullable=True),
    sa.Column('URLform', sa.String(length=150), nullable=True),
    sa.Column('IURLform', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('shop')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('Itemname',
    sa.Column('itemid', sa.String(length=30), nullable=False),
    sa.Column('itemname', sa.String(length=150), nullable=True),
    sa.Column('shopid', sa.Integer(), nullable=True),
    sa.Column('priceid', sa.String(length=100), nullable=True),
    sa.Column('imageurl', sa.String(length=100), nullable=True),
    sa.Column('itemurl', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['priceid'], ['Price.itemid'], ),
    sa.ForeignKeyConstraint(['shopid'], ['Shop.id'], ),
    sa.PrimaryKeyConstraint('itemid')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
    op.drop_table('Itemname')
    op.drop_table('roles')
    op.drop_table('Shop')
    op.drop_table('Price')
    # ### end Alembic commands ###