"""Create Phase 1 domain schemas.

Revision ID: 0001_create_domain_schemas
Revises: None
Create Date: 2026-05-11
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0001_create_domain_schemas"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS catalog")
    op.execute("CREATE SCHEMA IF NOT EXISTS orders")
    op.execute("CREATE SCHEMA IF NOT EXISTS users")
    op.execute("CREATE SCHEMA IF NOT EXISTS content")
    op.execute("CREATE SCHEMA IF NOT EXISTS public")


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS content CASCADE")
    op.execute("DROP SCHEMA IF EXISTS users CASCADE")
    op.execute("DROP SCHEMA IF EXISTS orders CASCADE")
    op.execute("DROP SCHEMA IF EXISTS catalog CASCADE")
