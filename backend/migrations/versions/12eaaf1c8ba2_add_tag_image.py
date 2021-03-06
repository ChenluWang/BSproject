"""add tag-image

Revision ID: 12eaaf1c8ba2
Revises: c29e2ee7c099
Create Date: 2022-01-02 16:18:53.254724

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12eaaf1c8ba2'
down_revision = 'c29e2ee7c099'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag_name', sa.String(length=50), nullable=True),
    sa.Column('uuid', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_tag_tag_name'), 'tag', ['tag_name'], unique=True)
    op.create_table('image_tag',
    sa.Column('image_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['image.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('image_id', 'tag_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('image_tag')
    op.drop_index(op.f('ix_tag_tag_name'), table_name='tag')
    op.drop_table('tag')
    # ### end Alembic commands ###
