"""add posts table

Revision ID: 40470bd9718e
Revises: d588d1a17507
Create Date: 2025-08-10 21:18:51.786170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '40470bd9718e'
down_revision: Union[str, Sequence[str], None] = 'd588d1a17507'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create posts table."""
    op.create_table('posts',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('published', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
        sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('posts_users_fk'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('posts_pkey'))
    )


def downgrade() -> None:
    """Drop posts table."""
    op.drop_table('posts')