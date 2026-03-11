"""update interest range to 0-20

Revision ID: 78c1d7632162
Revises: 0d9e78616edd
Create Date: 2026-03-03 12:33:13.603702

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78c1d7632162'
down_revision: Union[str, Sequence[str], None] = '0d9e78616edd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop the old 50% constraint and apply the new 20% constraint
    op.drop_constraint('chk_savings_product_interest_rate', 'savings_products', type_='check')
    op.create_check_constraint(
        'chk_savings_product_interest_rate',
        'savings_products',
        'interest_rate_percent >= 0.00 AND interest_rate_percent <= 20.00'
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Revert back to the old 50% constraint
    op.drop_constraint('chk_savings_product_interest_rate', 'savings_products', type_='check')
    op.create_check_constraint(
        'chk_savings_product_interest_rate',
        'savings_products',
        'interest_rate_percent >= 0.01 AND interest_rate_percent <= 50.00'
    )
