"""add friends table

Revision ID: f1e0b0395129
Revises: dc8511ad7c78
Create Date: 2025-08-10 21:35:46.815943

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1e0b0395129'
down_revision: Union[str, Sequence[str], None] = 'dc8511ad7c78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create friends table."""
    op.create_table('friends',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('friends_pkey'))
    )


def downgrade() -> None:
    """Drop friends table."""
    op.drop_table('friends')
