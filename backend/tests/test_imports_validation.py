from __future__ import annotations

import uuid
from typing import Any

import pytest

from app.domains.imports.csv_contract import (
    ImportEntityType,
    parse_csv_rows,
    parse_raw_csv_rows,
)
from app.domains.imports.models import ImportRowStatus
from app.domains.imports.service import ImportsService
from app.domains.imports.validation import validate_raw_rows


class BatchStub:
    def __init__(self) -> None:
        self.id = uuid.uuid4()


class RecordingRepository:
    def __init__(self) -> None:
        self.batch = BatchStub()
        self.rows: list[tuple[uuid.UUID, list[Any], ImportRowStatus]] = []
        self.errors: list[dict[str, Any]] = []

    async def create_batch(self, *, total_rows: int) -> BatchStub:
        self.total_rows = total_rows
        return self.batch

    async def add_import_rows(
        self,
        *,
        batch_id: uuid.UUID,
        rows: list[Any],
        status: ImportRowStatus = ImportRowStatus.NEW,
    ) -> list[Any]:
        self.rows.append((batch_id, rows, status))
        return rows

    async def add_error(self, **kwargs: Any) -> object:
        self.errors.append(kwargs)
        return object()


def test_parser_preserves_row_numbers_raw_payload_and_hashes() -> None:
    rows = parse_csv_rows(
        "entity_type,source_id,parent_source_id,sku,name\n"
        "product,lm-1,,SOAP-1,Soap\n"
        "variant,lm-2,lm-1,SOAP-1-BLUE,Blue Soap\n"
    )

    assert [row.row_number for row in rows] == [2, 3]
    assert rows[0].entity_type is ImportEntityType.PRODUCT
    assert rows[0].raw["name"] == "Soap"
    assert rows[0].normalized_payload is not None
    assert rows[0].normalized_payload["sku"] == "SOAP-1"
    assert rows[0].content_hash
    assert rows[1].parent_source_id == "lm-1"


def test_validation_accepts_supported_key_entity_rows() -> None:
    raw_rows = parse_raw_csv_rows(
        "entity_type,source_id,parent_source_id,sku,name,media_url\n"
        "product,p-1,,SKU-1,Soap,\n"
        "variant,v-1,p-1,SKU-1-BLUE,Blue Soap,\n"
        "category,c-1,,,Soap Category,\n"
        "media,m-1,p-1,,,https://example.test/image.jpg\n"
    )

    results = validate_raw_rows(raw_rows)

    assert all(result.is_valid for result in results)
    assert [result.row.entity_type for result in results if result.row] == [
        ImportEntityType.PRODUCT,
        ImportEntityType.VARIANT,
        ImportEntityType.CATEGORY,
        ImportEntityType.MEDIA,
    ]


def test_validation_returns_structured_errors_per_failed_row() -> None:
    raw_rows = parse_raw_csv_rows(
        "entity_type,source_id,parent_source_id,sku,name\n"
        "product,p-1,,,Soap\n"
        "variant,v-1,,,Variant without parent or SKU\n"
        "unknown,u-1,,,Unsupported\n"
    )

    results = validate_raw_rows(raw_rows)

    assert results[0].is_valid
    assert not results[1].is_valid
    assert not results[2].is_valid
    assert [(error.field, error.code, error.row_number) for error in results[1].errors] == [
        ("parent_source_id", "required", 3),
        ("sku", "required", 3),
    ]
    assert results[2].errors[0].field == "entity_type"
    assert results[2].errors[0].code == "unsupported_entity_type"


@pytest.mark.anyio
async def test_service_records_failed_rows_and_continues_batch() -> None:
    repository = RecordingRepository()
    service = ImportsService(repository)  # type: ignore[arg-type]

    outcome = await service.stage_csv_content(
        "entity_type,source_id,parent_source_id,sku,name\n"
        "product,p-1,,,Soap\n"
        "variant,v-1,,,Variant without parent or SKU\n"
        "category,c-1,,,Categories still continue\n"
    )

    assert outcome.valid_rows_count == 2
    assert outcome.failed_rows_count == 1
    assert repository.total_rows == 3
    assert len(repository.rows) == 3
    assert repository.rows[0][2] is ImportRowStatus.NEW
    assert repository.rows[1][2] is ImportRowStatus.FAILED
    assert repository.rows[2][2] is ImportRowStatus.NEW
    assert [error["field"] for error in repository.errors] == ["parent_source_id", "sku"]
