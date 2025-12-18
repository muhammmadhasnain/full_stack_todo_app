"""add name field to user table

Revision ID: 090a539480a7
Revises: 4e2e1a3839c0
Create Date: 2025-12-15 17:58:20.238562

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers
revision = '090a539480a7'
down_revision = '4e2e1a3839c0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add the name column to the existing user table
    op.add_column('user', sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False, server_default=''))
    op.create_index(op.f('ix_user_name'), 'user', ['name'], unique=False)


def downgrade() -> None:
    # Remove the name column and index
    op.drop_index(op.f('ix_user_name'), table_name='user')
    op.drop_column('user', 'name')