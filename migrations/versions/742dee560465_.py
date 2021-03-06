"""empty message

Revision ID: 742dee560465
Revises: 37471f553d52
Create Date: 2019-02-10 13:49:27.581006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '742dee560465'
down_revision = '37471f553d52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('name1', sa.String(length=255), nullable=True), schema='app')
    op.drop_column('product', 'name', schema='app')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('name', sa.CHAR(length=255), autoincrement=False, nullable=True), schema='app')
    op.drop_column('product', 'name1', schema='app')
    # ### end Alembic commands ###
