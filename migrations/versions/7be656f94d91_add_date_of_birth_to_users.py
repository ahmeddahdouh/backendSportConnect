"""add_date_of_birth_to_users

Revision ID: 7be656f94d91
Revises: 59a8177aa630
Create Date: 2024-03-19

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7be656f94d91'
down_revision: Union[str, None] = '59a8177aa630'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('date_of_birth', sa.Date(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'date_of_birth')
