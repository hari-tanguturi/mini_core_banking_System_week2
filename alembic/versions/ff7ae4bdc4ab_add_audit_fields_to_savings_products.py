"""Add audit fields to savings products

Revision ID: ff7ae4bdc4ab
Revises: b311730f7ab2
Create Date: 2026-03-03 04:37:47.590574

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff7ae4bdc4ab'
down_revision: Union[str, Sequence[str], None] = 'b311730f7ab2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
