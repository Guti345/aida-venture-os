"""add password_hash to users

Revision ID: d2484e351b00
Revises: 8261c3862e5b
Create Date: 2026-04-21 12:13:51.406840

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2484e351b00'
down_revision: Union[str, Sequence[str], None] = '8261c3862e5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('password_hash', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'password_hash')
