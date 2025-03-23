"""change_budget_field_type

Revision ID: a7901916a6ff
Revises: f90b5b4482da
Create Date: 2025-02-28 05:33:54.901809

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a7901916a6ff"
down_revision: str | None = "f90b5b4482da"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "budget",
        existing_type=sa.INTEGER(),
        type_=sa.String(),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "budget",
        existing_type=sa.String(),
        type_=sa.INTEGER(),
        existing_nullable=True,
    )
