"""empty message

Revision ID: 01418a0bdd97
Revises: 17f0f2e0b7a0
Create Date: 2019-03-01 15:44:13.940806

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01418a0bdd97'
down_revision = '17f0f2e0b7a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('office', sa.Column('name', sa.String(length=255), nullable=True), schema='app')
    op.drop_column('office', 'name1', schema='app')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('office', sa.Column('name1', sa.VARCHAR(length=255), autoincrement=False, nullable=True), schema='app')
    op.drop_column('office', 'name', schema='app')
    # ### end Alembic commands ###
