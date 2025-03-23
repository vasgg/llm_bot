"""change_users_table

Revision ID: ca13d5b6e156
Revises: a7901916a6ff
Create Date: 2025-03-12 23:54:02.403671

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ca13d5b6e156"
down_revision: str | None = "a7901916a6ff"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("space", sa.String(), nullable=True))
    op.drop_column("users", "indoor_room")
    op.drop_column("users", "area")
    op.drop_column("users", "space_type")
    op.drop_column("users", "interests")


def downgrade() -> None:
    op.add_column("users", sa.Column("interests", sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column(
        "users",
        sa.Column(
            "space_type", postgresql.ENUM("INDOOR", "OUTDOOR", name="spacetype"), autoincrement=False, nullable=True
        ),
    )
    op.add_column("users", sa.Column("area", sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column("users", sa.Column("indoor_room", sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column("users", "space")
