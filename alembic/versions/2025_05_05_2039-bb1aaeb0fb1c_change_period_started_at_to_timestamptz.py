"""change period_started_at to timestamptz

Revision ID: bb1aaeb0fb1c
Revises: 94dd16ebce46
Create Date: 2025-05-05 20:39:06.713112

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bb1aaeb0fb1c"
down_revision: Union[str, None] = "94dd16ebce46"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE user_counters ALTER COLUMN period_started_at TYPE TIMESTAMP WITH TIME ZONE;")


def downgrade() -> None:
    op.execute("ALTER TABLE user_counters ALTER COLUMN period_started_at TYPE TIMESTAMP WITHOUT TIME ZONE;")
