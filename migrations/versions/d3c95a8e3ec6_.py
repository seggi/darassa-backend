"""empty message

Revision ID: d3c95a8e3ec6
Revises: fe690fac17ef
Create Date: 2022-09-14 22:07:49.695822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3c95a8e3ec6'
down_revision = 'fe690fac17ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('classes', sa.Column('name', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('classes', 'name')
    # ### end Alembic commands ###
