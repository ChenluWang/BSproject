"""add tasks table

Revision ID: b16246790954
Revises: 6f6167c23303
Create Date: 2021-12-27 00:18:01.790847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b16246790954'
down_revision = '6f6167c23303'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('discription', sa.Text(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('finish_time', sa.DateTime(), nullable=True),
    sa.Column('IsFinished', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_title'), 'task', ['title'], unique=False)
    op.create_table('image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=250), nullable=True),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_image_address'), 'image', ['address'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_image_address'), table_name='image')
    op.drop_table('image')
    op.drop_index(op.f('ix_task_title'), table_name='task')
    op.drop_table('task')
    # ### end Alembic commands ###
