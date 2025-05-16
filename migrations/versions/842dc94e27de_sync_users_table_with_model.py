"""sync users table with model

Revision ID: 842dc94e27de
Revises: 59a8177aa630
Create Date: 2025-05-10 22:01:07.949006

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision: str = '842dc94e27de'
down_revision: Union[str, None] = '59a8177aa630'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Get inspector to check existing columns
    inspector = inspect(op.get_bind())
    events_columns = [col['name'] for col in inspector.get_columns('events')]
    users_columns = [col['name'] for col in inspector.get_columns('users')]
    
    # Add columns to events table if they don't exist
    if 'start_time' not in events_columns:
        op.add_column('events', sa.Column('start_time', sa.Time(), nullable=True))
    if 'end_time' not in events_columns:
        op.add_column('events', sa.Column('end_time', sa.Time(), nullable=True))
    if 'event_image' not in events_columns:
        op.add_column('events', sa.Column('event_image', sa.String(), nullable=True))
    if 'longitude' not in events_columns:
        op.add_column('events', sa.Column('longitude', sa.Float(), nullable=True))
    if 'latitude' not in events_columns:
        op.add_column('events', sa.Column('latitude', sa.Float(), nullable=True))
    
    # Modify existing columns in events table
    op.alter_column('events', 'id_gestionnaire',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('events', 'event_ville',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=200),
               existing_nullable=False)
    op.alter_column('events', 'event_date',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.Date(),
               existing_nullable=False)
    op.alter_column('events', 'event_age_min',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('events', 'event_age_max',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('events', 'nombre_utilisateur_min',
               existing_type=sa.INTEGER(),
               nullable=True)
    
    # Add columns to users table if they don't exist
    if 'profile_image' not in users_columns:
        op.add_column('users', sa.Column('profile_image', sa.String(), nullable=True))
    if 'bibliography' not in users_columns:
        op.add_column('users', sa.Column('bibliography', sa.String(), nullable=True))
    if 'interests' not in users_columns:
        op.add_column('users', sa.Column('interests', sa.ARRAY(sa.String()), nullable=True))
    
    # Modify existing columns in users table
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=30),
               existing_nullable=False)
    op.alter_column('users', 'firstname',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=100),
               existing_nullable=False)
    op.alter_column('users', 'familyname',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=100),
               existing_nullable=False)
    op.alter_column('users', 'phone',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=15),
               existing_nullable=False)
    
    # Update and modify date_of_birth column
    op.execute("UPDATE users SET date_of_birth = '1970-01-01' WHERE date_of_birth IS NULL")
    op.alter_column('users', 'date_of_birth', existing_type=sa.DATE(), nullable=False)
    
    # Drop columns if they exist
    if 'age' in users_columns:
        op.drop_column('users', 'age')
    if 'profileImage' in users_columns:
        op.drop_column('users', 'profileImage')


def downgrade() -> None:
    # Get inspector to check existing columns
    inspector = inspect(op.get_bind())
    events_columns = [col['name'] for col in inspector.get_columns('events')]
    users_columns = [col['name'] for col in inspector.get_columns('users')]
    
    # Add back columns to users table if they don't exist
    if 'profileImage' not in users_columns:
        op.add_column('users', sa.Column('profileImage', sa.VARCHAR(), autoincrement=False, nullable=True))
    if 'age' not in users_columns:
        op.add_column('users', sa.Column('age', sa.INTEGER(), autoincrement=False, nullable=False))
    
    # Modify columns back to original state
    op.alter_column('users', 'date_of_birth',
               existing_type=sa.DATE(),
               nullable=True)
    op.alter_column('users', 'phone',
               existing_type=sa.String(length=15),
               type_=sa.VARCHAR(length=200),
               existing_nullable=False)
    op.alter_column('users', 'familyname',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=200),
               existing_nullable=False)
    op.alter_column('users', 'firstname',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=200),
               existing_nullable=False)
    op.alter_column('users', 'username',
               existing_type=sa.String(length=30),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
    
    # Drop columns if they exist
    if 'interests' in users_columns:
        op.drop_column('users', 'interests')
    if 'bibliography' in users_columns:
        op.drop_column('users', 'bibliography')
    if 'profile_image' in users_columns:
        op.drop_column('users', 'profile_image')
    
    # Modify columns back in events table
    op.alter_column('events', 'nombre_utilisateur_min',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('events', 'event_age_max',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('events', 'event_age_min',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('events', 'event_date',
               existing_type=sa.Date(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False)
    op.alter_column('events', 'event_ville',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
    op.alter_column('events', 'id_gestionnaire',
               existing_type=sa.INTEGER(),
               nullable=False)
    
    # Drop columns if they exist
    if 'latitude' in events_columns:
        op.drop_column('events', 'latitude')
    if 'longitude' in events_columns:
        op.drop_column('events', 'longitude')
    if 'event_image' in events_columns:
        op.drop_column('events', 'event_image')
    if 'end_time' in events_columns:
        op.drop_column('events', 'end_time')
    if 'start_time' in events_columns:
        op.drop_column('events', 'start_time')
