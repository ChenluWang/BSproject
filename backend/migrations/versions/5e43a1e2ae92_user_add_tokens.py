"""user add tokens

Revision ID: 5e43a1e2ae92
Revises: defa890119f7
Create Date: 2021-12-25 23:14:54.398144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e43a1e2ae92'
down_revision = 'defa890119f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('token', sa.String(length=32), nullable=True))
    op.add_column('users', sa.Column('token_expiration', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_users_token'), 'users', ['token'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_token'), table_name='users')
    op.drop_column('users', 'token_expiration')
    op.drop_column('users', 'token')
    # ### end Alembic commands ###
