"""empty message

Revision ID: 630b0f17a609
Revises: 7df194ee31d3
Create Date: 2019-02-10 13:52:46.059235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '630b0f17a609'
down_revision = '7df194ee31d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('image', sa.String(length=255), nullable=True), schema='app')
    op.add_column('product', sa.Column('measure', sa.String(length=255), nullable=True), schema='app')
    op.drop_column('product', 'image1', schema='app')
    op.drop_column('product', 'measure1', schema='app')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('measure1', sa.VARCHAR(length=255), autoincrement=False, nullable=True), schema='app')
    op.add_column('product', sa.Column('image1', sa.VARCHAR(length=255), autoincrement=False, nullable=True), schema='app')
    op.drop_column('product', 'measure', schema='app')
    op.drop_column('product', 'image', schema='app')
    # ### end Alembic commands ###
