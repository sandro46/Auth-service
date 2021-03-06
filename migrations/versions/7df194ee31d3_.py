"""empty message

Revision ID: 7df194ee31d3
Revises: ade58ef0ee10
Create Date: 2019-02-10 13:52:11.660143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7df194ee31d3'
down_revision = 'ade58ef0ee10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('code', sa.String(length=255), nullable=True), schema='app')
    op.add_column('product', sa.Column('image1', sa.String(length=255), nullable=True), schema='app')
    op.add_column('product', sa.Column('measure1', sa.String(length=255), nullable=True), schema='app')
    op.drop_column('product', 'code1', schema='app')
    op.drop_column('product', 'image', schema='app')
    op.drop_column('product', 'measure', schema='app')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('measure', sa.CHAR(length=255), autoincrement=False, nullable=True), schema='app')
    op.add_column('product', sa.Column('image', sa.CHAR(length=255), autoincrement=False, nullable=True), schema='app')
    op.add_column('product', sa.Column('code1', sa.VARCHAR(length=255), autoincrement=False, nullable=True), schema='app')
    op.drop_column('product', 'measure1', schema='app')
    op.drop_column('product', 'image1', schema='app')
    op.drop_column('product', 'code', schema='app')
    # ### end Alembic commands ###
