"""change tag-image

Revision ID: 2071b6c72252
Revises: ddd38fefd0e0
Create Date: 2022-01-02 16:51:23.320448

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2071b6c72252'
down_revision = 'ddd38fefd0e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('imagetotag', sa.Column('tag_count', sa.Integer(), nullable=False))
    op.drop_column('imagetotag', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('imagetotag', sa.Column('id', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('imagetotag', 'tag_count')
    # ### end Alembic commands ###
