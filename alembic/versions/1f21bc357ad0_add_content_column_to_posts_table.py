"""add content column to posts table

Revision ID: 1f21bc357ad0
Revises: b73e03dc1599
Create Date: 2025-02-10 19:58:06.807503

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1f21bc357ad0"
down_revision: Union[str, None] = "b73e03dc1599"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
