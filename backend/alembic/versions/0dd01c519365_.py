
"""add note timestamps

Revision ID: 0dd01c519365
Revises: ed47fabdc5ef
Create Date: 2026-09-15 12:14:43.796876

"""
from typing import Sequence, Union
from datetime import datetime, timezone

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0dd01c519365"
down_revision: Union[str, Sequence[str], None] = "ed47fabdc5ef"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add the columns as nullable first because SQLite does not allow
    # adding a NOT NULL column to an existing table without a constant default.
    op.add_column(
        "notes",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True
        )
    )

    op.add_column(
        "notes",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True
        )
    )

    # Give existing notes a timestamp.
    current_time = datetime.now(timezone.utc)

    notes_table = sa.table(
        "notes",
        sa.column("created_at", sa.DateTime(timezone=True)),
        sa.column("updated_at", sa.DateTime(timezone=True)),
    )

    op.execute(
        notes_table.update().values(
            created_at=current_time,
            updated_at=current_time
        )
    )

    # SQLite does not support changing an existing column from
    # nullable=True to nullable=False using ALTER COLUMN.
    # Therefore, we leave the database columns nullable here.
    #
    # The SQLAlchemy model enforces nullable=False for all newly created
    # notes, and future PostgreSQL migration work can enforce the
    # database-level constraint properly.


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("notes", "updated_at")
    op.drop_column("notes", "created_at")