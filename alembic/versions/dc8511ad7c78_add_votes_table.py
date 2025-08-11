"""add votes table

Revision ID: dc8511ad7c78
Revises: 40470bd9718e
Create Date: 2025-08-10 21:20:21.990375

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'dc8511ad7c78'
down_revision: Union[str, Sequence[str], None] = '40470bd9718e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create votes table."""
    op.create_table('votes',
        sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name=op.f('votes_post_id_fkey'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('votes_user_id_fkey'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('post_id', 'user_id', name=op.f('votes_pkey'))
    )


def downgrade() -> None:
    """Drop votes table."""
    op.drop_table('votes')