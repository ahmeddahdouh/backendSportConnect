"""add_date_of_birth_to_users

Revision ID: 7be656f94d91
Revises: 842dc94e27de
Create Date: 2024-03-19

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = '7be656f94d91'
down_revision = '842dc94e27de'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Get inspector to check existing columns
    inspector = inspect(op.get_bind())
    columns = [col['name'] for col in inspector.get_columns('users')]
    
    # Add date_of_birth column if it doesn't exist
    if 'date_of_birth' not in columns:
        op.add_column('users', sa.Column('date_of_birth', sa.Date(), nullable=True))


def downgrade() -> None:
    # Get inspector to check existing columns
    inspector = inspect(op.get_bind())
    columns = [col['name'] for col in inspector.get_columns('users')]
    
    # Remove date_of_birth column if it exists
    if 'date_of_birth' in columns:
        op.drop_column('users', 'date_of_birth')
