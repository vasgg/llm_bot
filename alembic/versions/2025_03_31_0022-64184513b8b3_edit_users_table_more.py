"""edit_users_table_more

Revision ID: 64184513b8b3
Revises: 5d83ca9562cf
Create Date: 2025-03-31 00:22:48.186199

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "64184513b8b3"
down_revision: Union[str, None] = "5d83ca9562cf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("ai_thread", sa.String(), nullable=True))
    op.drop_column("users", "ai_tread")


def downgrade() -> None:
    op.add_column("users", sa.Column("ai_tread", sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column("users", "ai_thread")
