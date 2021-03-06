"""users jwt

Revision ID: c63c8b643478
Revises: 5e43a1e2ae92
Create Date: 2021-12-26 01:11:47.316464

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c63c8b643478'
down_revision = '5e43a1e2ae92'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_token', table_name='users')
    op.drop_column('users', 'token')
    op.drop_column('users', 'token_expiration')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('token_expiration', mysql.DATETIME(), nullable=True))
    op.add_column('users', sa.Column('token', mysql.VARCHAR(length=32), nullable=True))
    op.create_index('ix_users_token', 'users', ['token'], unique=False)
    # ### end Alembic commands ###
