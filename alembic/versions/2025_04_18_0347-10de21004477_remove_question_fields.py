"""remove_question_fields

Revision ID: 10de21004477
Revises: c2f751fd2b7a
Create Date: 2025-04-18 03:47:19.554820

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "10de21004477"
down_revision: Union[str, None] = "c2f751fd2b7a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("users", "style")
    op.drop_column("users", "budget")


def downgrade() -> None:
    op.add_column("users", sa.Column("budget", sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column("users", sa.Column("style", sa.VARCHAR(), autoincrement=False, nullable=True))
