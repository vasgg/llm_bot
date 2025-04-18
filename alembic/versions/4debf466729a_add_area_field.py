"""add_area_field

Revision ID: 4debf466729a
Revises: 9edd1c380f14
Create Date: 2025-02-28 04:20:20.418170

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4debf466729a"
down_revision: str | None = "9edd1c380f14"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("area", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "area")
