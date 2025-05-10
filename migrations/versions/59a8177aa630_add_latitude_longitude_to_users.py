"""add_latitude_longitude_to_users

Revision ID: 59a8177aa630
Revises: d7e4ac5e6f0c
Create Date: 2024-03-19

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59a8177aa630'
down_revision = 'd7e4ac5e6f0c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add latitude and longitude columns to users table
    op.add_column('users', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('users', sa.Column('longitude', sa.Float(), nullable=True))


def downgrade() -> None:
    # Remove latitude and longitude columns from users table
    op.drop_column('users', 'longitude')
    op.drop_column('users', 'latitude')
