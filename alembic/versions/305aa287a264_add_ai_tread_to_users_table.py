"""add_ai_tread_to_users_table

Revision ID: 305aa287a264
Revises: ca13d5b6e156
Create Date: 2025-03-13 04:08:01.842541

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "305aa287a264"
down_revision: str | None = "ca13d5b6e156"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("ai_tread", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "ai_tread")
