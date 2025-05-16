"""Initial database schema

Revision ID: d7e4ac5e6f0c
Revises: 
Create Date: 2025-05-10 21:44:20.326773

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'd7e4ac5e6f0c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=30), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=128), nullable=False),
        sa.Column('firstname', sa.String(length=100), nullable=False),
        sa.Column('familyname', sa.String(length=100), nullable=False),
        sa.Column('phone', sa.String(length=15), nullable=False),
        sa.Column('date_of_birth', sa.Date(), nullable=False),
        sa.Column('profile_image', sa.String(), nullable=True),
        sa.Column('bibliography', sa.String(), nullable=True),
        sa.Column('interests', sa.ARRAY(sa.String()), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    # Create events table
    op.create_table('events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('event_name', sa.String(length=100), nullable=False),
        sa.Column('event_description', sa.Text(), nullable=False),
        sa.Column('event_date', sa.Date(), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=True),
        sa.Column('end_time', sa.Time(), nullable=True),
        sa.Column('event_ville', sa.String(length=200), nullable=False),
        sa.Column('event_age_min', sa.Integer(), nullable=True),
        sa.Column('event_age_max', sa.Integer(), nullable=True),
        sa.Column('nombre_utilisateur_min', sa.Integer(), nullable=True),
        sa.Column('event_image', sa.String(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('id_gestionnaire', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['id_gestionnaire'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create event_participants table
    op.create_table('event_participants',
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('event_id', 'user_id')
    )


def downgrade() -> None:
    op.drop_table('event_participants')
    op.drop_table('events')
    op.drop_table('users')
