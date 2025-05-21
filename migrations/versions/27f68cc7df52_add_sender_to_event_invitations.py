"""add_sender_to_event_invitations

Revision ID: 27f68cc7df52
Revises: f4f759568e84
Create Date: 2024-03-19 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27f68cc7df52'
down_revision: Union[str, None] = 'f4f759568e84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add sender_id column as nullable first
    op.add_column('event_invitations', sa.Column('sender_id', sa.Integer(), nullable=True))
    
    # Create foreign key constraint
    op.create_foreign_key(
        'fk_event_invitations_sender_id_users',
        'event_invitations', 'users',
        ['sender_id'], ['id']
    )
    
    # Update existing records to use event manager as sender
    op.execute("""
        UPDATE event_invitations ei
        SET sender_id = e.id_gestionnaire
        FROM events e
        WHERE ei.event_id = e.id
    """)
    
    # Make the column non-nullable
    op.alter_column('event_invitations', 'sender_id',
                    existing_type=sa.Integer(),
                    nullable=False)


def downgrade() -> None:
    # Remove foreign key constraint
    op.drop_constraint('fk_event_invitations_sender_id_users', 'event_invitations', type_='foreignkey')
    
    # Remove the column
    op.drop_column('event_invitations', 'sender_id')
