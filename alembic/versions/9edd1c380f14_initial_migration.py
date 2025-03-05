"""initial_migration

Revision ID: 9edd1c380f14
Revises:
Create Date: 2025-02-27 18:58:48.307487

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9edd1c380f14"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("tg_id", sa.BigInteger(), nullable=False),
        sa.Column("fullname", sa.String(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("is_subscribed", sa.BOOLEAN(), nullable=False),
        sa.Column("expired_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("space_type", sa.Enum("INDOOR", "OUTDOOR", name="spacetype"), nullable=True),
        sa.Column("budget", sa.Integer(), nullable=True),
        sa.Column("geography", sa.String(), nullable=True),
        sa.Column("style", sa.String(), nullable=True),
        sa.Column("interests", sa.String(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tg_id"),
    )


def downgrade() -> None:
    op.drop_table("users")
