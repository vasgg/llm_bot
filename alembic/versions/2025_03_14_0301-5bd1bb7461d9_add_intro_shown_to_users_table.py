"""add_intro_shown_to_users_table

Revision ID: 5bd1bb7461d9
Revises: 305aa287a264
Create Date: 2025-03-14 03:01:39.673710

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5bd1bb7461d9"
down_revision: str | None = "305aa287a264"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("is_intro_shown", sa.BOOLEAN(), nullable=False))


def downgrade() -> None:
    op.drop_column("users", "is_intro_shown")
