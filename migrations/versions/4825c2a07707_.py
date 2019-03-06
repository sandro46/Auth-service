"""empty message

Revision ID: 4825c2a07707
Revises: d5c58f100c61
Create Date: 2019-03-06 22:43:47.319907

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4825c2a07707'
down_revision = 'd5c58f100c61'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('phone', sa.String(length=255), nullable=True),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('discount', sa.Integer(), nullable=True),
    sa.Column('desc', sa.Text(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('client')
    # ### end Alembic commands ###
