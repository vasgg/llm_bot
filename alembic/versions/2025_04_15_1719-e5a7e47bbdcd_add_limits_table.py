"""add_limits_table

Revision ID: e5a7e47bbdcd
Revises: 64184513b8b3
Create Date: 2025-04-15 17:19:16.829398

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e5a7e47bbdcd"
down_revision: Union[str, None] = "64184513b8b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_limits",
        sa.Column("tg_id", sa.BigInteger(), nullable=False),
        sa.Column("image_count", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["tg_id"], ["users.tg_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("user_limits")
