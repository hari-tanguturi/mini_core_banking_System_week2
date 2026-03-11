"""make updated_by nullable

Revision ID: 3915f7351cc2
Revises: 78c1d7632162
Create Date: 2026-03-03 13:24:31.637068

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3915f7351cc2'
down_revision: Union[str, Sequence[str], None] = '78c1d7632162'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('savings_products', 'updated_by', existing_type=sa.String(length=100), nullable=True)


def downgrade() -> None:
    op.alter_column('savings_products', 'updated_by', existing_type=sa.String(length=100), nullable=False)
