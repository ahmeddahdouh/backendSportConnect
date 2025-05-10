"""add_latitude_longitude_to_users

Revision ID: 59a8177aa630
Revises: d7e4ac5e6f0c
Create Date: 2024-03-19

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = '59a8177aa630'
down_revision = 'd7e4ac5e6f0c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Get inspector to check existing columns
    inspector = inspect(op.get_bind())
    columns = [col['name'] for col in inspector.get_columns('users')]
    
    # Add latitude and longitude columns if they don't exist
    if 'latitude' not in columns:
        op.add_column('users', sa.Column('latitude', sa.Float(), nullable=True))
    if 'longitude' not in columns:
        op.add_column('users', sa.Column('longitude', sa.Float(), nullable=True))


def downgrade() -> None:
    # Get inspector to check existing columns
    inspector = inspect(op.get_bind())
    columns = [col['name'] for col in inspector.get_columns('users')]
    
    # Remove latitude and longitude columns if they exist
    if 'longitude' in columns:
        op.drop_column('users', 'longitude')
    if 'latitude' in columns:
        op.drop_column('users', 'latitude')
