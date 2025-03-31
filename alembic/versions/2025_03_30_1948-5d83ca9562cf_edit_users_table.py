"""edit_users_table

Revision ID: 5d83ca9562cf
Revises: 5bd1bb7461d9
Create Date: 2025-03-30 19:48:56.602185

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5d83ca9562cf"
down_revision: Union[str, None] = "5bd1bb7461d9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("is_context_added", sa.BOOLEAN(), nullable=False, server_default="false"))
    op.drop_column("users", "is_intro_shown")


def downgrade() -> None:
    op.add_column("users", sa.Column("is_intro_shown", sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column("users", "is_context_added")
