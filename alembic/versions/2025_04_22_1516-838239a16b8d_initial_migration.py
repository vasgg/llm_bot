"""initial_migration

Revision ID: 838239a16b8d
Revises:
Create Date: 2025-04-22 15:16:55.649496

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "838239a16b8d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("tg_id", sa.BigInteger(), nullable=False),
        sa.Column("fullname", sa.String(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("ai_thread", sa.String(), nullable=True),
        sa.Column("action_count", sa.Integer(), nullable=False),
        sa.Column("is_subscribed", sa.BOOLEAN(), nullable=False),
        sa.Column("is_context_added", sa.BOOLEAN(), nullable=False),
        sa.Column("expired_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("space", sa.String(), nullable=True),
        sa.Column("geography", sa.String(), nullable=True),
        sa.Column("request", sa.String(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tg_id"),
    )
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
    op.drop_table("users")
