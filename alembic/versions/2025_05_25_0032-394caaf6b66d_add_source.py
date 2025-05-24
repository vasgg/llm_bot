"""add_source

Revision ID: 394caaf6b66d
Revises: 699696ca56e9
Create Date: 2025-05-25 00:32:16.718717

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "394caaf6b66d"
down_revision: Union[str, None] = "699696ca56e9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("source", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "source")
