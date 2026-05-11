from __future__ import annotations

import uuid
from typing import Any

import pytest
from sqlalchemy.dialects import postgresql

from app.domains.imports.csv_contract import CsvImportRow, ImportEntityType
from app.domains.imports.models import ImportRowStatus, SourceMapping
from app.domains.imports.repository import ImportsRepository
from app.domains.imports.schemas import ImportBatchStatus, ImportErrorSeverity


class RecordingSession:
    def __init__(self) -> None:
        self.added: list[Any] = []
        self.added_many: list[Any] = []
        self.flushed = 0
        self.refreshed: list[Any] = []

    def add(self, item: Any) -> None:
        self.added.append(item)

    def add_all(self, items: list[Any]) -> None:
        self.added_many.extend(items)

    async def flush(self) -> None:
        self.flushed += 1

    async def refresh(self, item: Any) -> None:
        self.refreshed.append(item)


@pytest.mark.anyio
async def test_repository_creates_import_batch_with_source_metadata() -> None:
    session = RecordingSession()
    repository = ImportsRepository(session)  # type: ignore[arg-type]

    batch = await repository.create_batch(total_rows=2)

    assert batch in session.added
    assert batch in session.refreshed
    assert session.flushed == 1
    assert batch.source_system == "livemaster"
    assert batch.status == ImportBatchStatus.PENDING.value
    assert batch.total_rows == 2


@pytest.mark.anyio
async def test_repository_adds_import_rows_without_canonical_publication() -> None:
    session = RecordingSession()
    repository = ImportsRepository(session)  # type: ignore[arg-type]
    batch_id = uuid.uuid4()
    csv_rows = [
        CsvImportRow(
            row_number=2,
            entity_type=ImportEntityType.PRODUCT,
            source_id="lm-1",
            raw={"entity_type": "product", "source_id": "lm-1", "name": "Soap"},
        )
    ]

    rows = await repository.add_import_rows(batch_id=batch_id, rows=csv_rows)

    assert session.flushed == 1
    assert rows == session.added_many
    assert rows[0].batch_id == batch_id
    assert rows[0].row_number == 2
    assert rows[0].entity_type == "product"
    assert rows[0].source_id == "lm-1"
    assert rows[0].status == ImportRowStatus.NEW.value
    assert rows[0].raw_payload["name"] == "Soap"


@pytest.mark.anyio
async def test_repository_adds_structured_import_errors() -> None:
    session = RecordingSession()
    repository = ImportsRepository(session)  # type: ignore[arg-type]
    batch_id = uuid.uuid4()

    error = await repository.add_error(
        batch_id=batch_id,
        row_number=4,
        entity_type=ImportEntityType.VARIANT,
        field="price",
        code="invalid_decimal",
        message="Price must be a decimal value.",
        severity=ImportErrorSeverity.ERROR,
    )

    assert error in session.added
    assert error.batch_id == batch_id
    assert error.row_number == 4
    assert error.entity_type == "variant"
    assert error.field == "price"
    assert error.code == "invalid_decimal"
    assert error.severity == "error"


def test_source_mapping_model_enforces_identity_uniqueness() -> None:
    constraints = {
        constraint.name
        for constraint in SourceMapping.__table__.constraints
        if constraint.name is not None
    }

    assert "uq_source_mappings_source_system_entity_type_source_id" in constraints


def test_source_mapping_upsert_uses_postgresql_on_conflict() -> None:
    statement = ImportsRepository.build_source_mapping_upsert(
        batch_id=uuid.uuid4(),
        entity_type=ImportEntityType.PRODUCT,
        source_id="lm-1",
        content_hash="abc123",
    )

    compiled = str(statement.compile(dialect=postgresql.dialect()))

    assert "ON CONFLICT" in compiled
    assert "source_system" in compiled
    assert "entity_type" in compiled
    assert "source_id" in compiled
    assert "DO UPDATE SET" in compiled


def test_repository_builds_batch_summary_and_error_table_queries() -> None:
    repository = ImportsRepository(object())  # type: ignore[arg-type]
    batch_id = uuid.uuid4()

    summary_sql = str(
        repository.build_batch_summary_statement(batch_id).compile(dialect=postgresql.dialect())
    )
    errors_sql = str(
        repository.build_error_table_statement(batch_id=batch_id, limit=20, offset=0).compile(
            dialect=postgresql.dialect()
        )
    )

    assert "staging.import_batches" in summary_sql
    assert "staging.import_rows" in summary_sql
    assert "skipped_rows" in summary_sql
    assert "failed_rows" in summary_sql
    assert "requires_review_rows" in summary_sql
    assert "staging.import_errors" in errors_sql
    assert "ORDER BY" in errors_sql
