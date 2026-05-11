"""Create Phase 2 import staging tables.

Revision ID: 0002_create_import_staging
Revises: 0001_create_domain_schemas
Create Date: 2026-05-11
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002_create_import_staging"
down_revision: str | None = "0001_create_domain_schemas"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS staging")

    op.create_table(
        "import_batches",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("source_system", sa.String(length=64), nullable=False),
        sa.Column("contract_version", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("total_rows", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("total_rows >= 0", name="import_batches_total_rows_non_negative"),
        schema="staging",
    )

    op.create_table(
        "import_rows",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "batch_id",
            sa.Uuid(),
            sa.ForeignKey("staging.import_batches.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("row_number", sa.Integer(), nullable=False),
        sa.Column("entity_type", sa.String(length=32), nullable=False),
        sa.Column("source_id", sa.String(length=255), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("raw_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("normalized_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("row_number >= 1", name="import_rows_row_number_positive"),
        sa.UniqueConstraint("batch_id", "row_number", name="uq_import_rows_batch_id_row_number"),
        sa.UniqueConstraint(
            "batch_id",
            "entity_type",
            "source_id",
            name="uq_import_rows_batch_id_entity_type_source_id",
        ),
        schema="staging",
    )

    op.create_table(
        "source_mappings",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("source_system", sa.String(length=64), nullable=False),
        sa.Column("entity_type", sa.String(length=32), nullable=False),
        sa.Column("source_id", sa.String(length=255), nullable=False),
        sa.Column(
            "batch_id",
            sa.Uuid(),
            sa.ForeignKey("staging.import_batches.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("content_hash", sa.String(length=64), nullable=True),
        sa.Column("canonical_id", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint(
            "source_system",
            "entity_type",
            "source_id",
            name="uq_source_mappings_source_system_entity_type_source_id",
        ),
        schema="staging",
    )

    op.create_table(
        "import_errors",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "batch_id",
            sa.Uuid(),
            sa.ForeignKey("staging.import_batches.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "row_id",
            sa.Uuid(),
            sa.ForeignKey("staging.import_rows.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column("row_number", sa.Integer(), nullable=False),
        sa.Column("entity_type", sa.String(length=32), nullable=False),
        sa.Column("field", sa.String(length=128), nullable=False),
        sa.Column("code", sa.String(length=128), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("row_number >= 1", name="import_errors_row_number_positive"),
        schema="staging",
    )

    op.create_index(
        "ix_import_rows_batch_id_status",
        "import_rows",
        ["batch_id", "status"],
        schema="staging",
    )
    op.create_index(
        "ix_import_errors_batch_id_severity",
        "import_errors",
        ["batch_id", "severity"],
        schema="staging",
    )
    op.create_index(
        "ix_import_errors_batch_id_row_id_severity",
        "import_errors",
        ["batch_id", "row_id", "severity"],
        schema="staging",
    )


def downgrade() -> None:
    op.drop_index("ix_import_errors_batch_id_row_id_severity", table_name="import_errors", schema="staging")
    op.drop_index("ix_import_errors_batch_id_severity", table_name="import_errors", schema="staging")
    op.drop_index("ix_import_rows_batch_id_status", table_name="import_rows", schema="staging")
    op.drop_table("import_errors", schema="staging")
    op.drop_table("source_mappings", schema="staging")
    op.drop_table("import_rows", schema="staging")
    op.drop_table("import_batches", schema="staging")
    op.execute("DROP SCHEMA IF EXISTS staging")
