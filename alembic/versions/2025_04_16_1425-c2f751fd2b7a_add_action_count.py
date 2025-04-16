"""add_action_count

Revision ID: c2f751fd2b7a
Revises: e5a7e47bbdcd
Create Date: 2025-04-16 14:25:25.048981

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c2f751fd2b7a"
down_revision: Union[str, None] = "e5a7e47bbdcd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("action_count", sa.Integer(), nullable=False, server_default="0", default=0))


def downgrade() -> None:
    op.drop_column("users", "action_count")
