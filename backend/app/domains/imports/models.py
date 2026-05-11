from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.domains.imports.csv_contract import CSV_CONTRACT_VERSION
from app.domains.imports.schemas import ImportBatchStatus, ImportErrorSeverity


class ImportRowStatus(StrEnum):
    NEW = "new"
    UNCHANGED = "unchanged"
    CHANGED = "changed"
    SKIPPED = "skipped"
    FAILED = "failed"
    REQUIRES_REVIEW = "requires_review"


class ImportBatch(Base):
    __tablename__ = "import_batches"
    __table_args__ = {"schema": "staging"}

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    source_system: Mapped[str] = mapped_column(String(64), default="livemaster")
    contract_version: Mapped[str] = mapped_column(String(64), default=CSV_CONTRACT_VERSION)
    status: Mapped[str] = mapped_column(String(32), default=ImportBatchStatus.PENDING.value)
    total_rows: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    rows: Mapped[list[ImportRow]] = relationship(
        back_populates="batch",
        cascade="all, delete-orphan",
    )
    errors: Mapped[list[ImportError]] = relationship(
        back_populates="batch",
        cascade="all, delete-orphan",
    )


class ImportRow(Base):
    __tablename__ = "import_rows"
    __table_args__ = (
        UniqueConstraint("batch_id", "row_number", name="uq_import_rows_batch_id_row_number"),
        UniqueConstraint(
            "batch_id",
            "entity_type",
            "source_id",
            name="uq_import_rows_batch_id_entity_type_source_id",
        ),
        Index("ix_import_rows_batch_id_status", "batch_id", "status"),
        {"schema": "staging"},
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    batch_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("staging.import_batches.id", ondelete="CASCADE")
    )
    row_number: Mapped[int] = mapped_column(Integer)
    entity_type: Mapped[str] = mapped_column(String(32))
    source_id: Mapped[str] = mapped_column(String(255))
    content_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default=ImportRowStatus.NEW.value)
    raw_payload: Mapped[dict[str, Any]] = mapped_column(JSONB)
    normalized_payload: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    batch: Mapped[ImportBatch] = relationship(back_populates="rows")
    errors: Mapped[list[ImportError]] = relationship(
        back_populates="row",
        cascade="all, delete-orphan",
    )


class SourceMapping(Base):
    __tablename__ = "source_mappings"
    __table_args__ = (
        UniqueConstraint(
            "source_system",
            "entity_type",
            "source_id",
            name="uq_source_mappings_source_system_entity_type_source_id",
        ),
        {"schema": "staging"},
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    source_system: Mapped[str] = mapped_column(String(64))
    entity_type: Mapped[str] = mapped_column(String(32))
    source_id: Mapped[str] = mapped_column(String(255))
    batch_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("staging.import_batches.id", ondelete="SET NULL"),
        nullable=True,
    )
    content_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    canonical_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


class ImportError(Base):
    __tablename__ = "import_errors"
    __table_args__ = (
        Index("ix_import_errors_batch_id_severity", "batch_id", "severity"),
        Index("ix_import_errors_batch_id_row_id_severity", "batch_id", "row_id", "severity"),
        {"schema": "staging"},
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    batch_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("staging.import_batches.id", ondelete="CASCADE")
    )
    row_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("staging.import_rows.id", ondelete="CASCADE"),
        nullable=True,
    )
    row_number: Mapped[int] = mapped_column(Integer)
    entity_type: Mapped[str] = mapped_column(String(32))
    field: Mapped[str] = mapped_column(String(128))
    code: Mapped[str] = mapped_column(String(128))
    message: Mapped[str] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(32), default=ImportErrorSeverity.ERROR.value)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    batch: Mapped[ImportBatch] = relationship(back_populates="errors")
    row: Mapped[ImportRow | None] = relationship(back_populates="errors")
