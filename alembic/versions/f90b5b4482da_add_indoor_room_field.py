"""add_indoor_room_field

Revision ID: f90b5b4482da
Revises: 4debf466729a
Create Date: 2025-02-28 04:43:09.161863

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f90b5b4482da"
down_revision: str | None = "4debf466729a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("indoor_room", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "indoor_room")
