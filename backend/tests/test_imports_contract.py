import pytest
from pydantic import TypeAdapter

from app.domains.imports.csv_contract import CsvContractError, ImportEntityType, parse_csv_rows
from app.domains.imports.schemas import (
    ImportBatchCreate,
    ImportBatchStatus,
    ImportBatchSummary,
    ImportErrorRow,
    ImportErrorSeverity,
)


def test_csv_contract_accepts_required_headers_and_preserves_row_numbers() -> None:
    content = "entity_type,source_id,name\nproduct,lm-1,Soap base\nvariant,lm-2,10g\n"

    rows = parse_csv_rows(content)

    assert [row.row_number for row in rows] == [2, 3]
    assert rows[0].entity_type is ImportEntityType.PRODUCT
    assert rows[0].source_id == "lm-1"
    assert rows[0].raw["name"] == "Soap base"


def test_csv_contract_rejects_missing_required_headers_before_rows() -> None:
    content = "entity_type,name\nproduct,Soap base\n"

    with pytest.raises(CsvContractError, match="source_id"):
        parse_csv_rows(content)


def test_csv_contract_rejects_unsupported_entity_type() -> None:
    content = "entity_type,source_id\ncoupon,lm-1\n"

    with pytest.raises(CsvContractError, match="Unsupported entity_type"):
        parse_csv_rows(content)


def test_import_schemas_expose_batch_status_and_error_table_fields() -> None:
    batch = ImportBatchCreate()
    assert batch.contract_version == "livemaster-single-csv-v1"

    summary_adapter = TypeAdapter(ImportBatchSummary)
    schema = summary_adapter.json_schema()
    for field in (
        "batch_id",
        "status",
        "total_rows",
        "staged_rows",
        "skipped_rows",
        "failed_rows",
        "requires_review_rows",
    ):
        assert field in schema["properties"]

    error = ImportErrorRow(
        row_number=2,
        entity_type=ImportEntityType.PRODUCT,
        field="source_id",
        code="required",
        message="source_id is required",
        severity=ImportErrorSeverity.ERROR,
    )
    assert error.severity is ImportErrorSeverity.ERROR
    assert ImportBatchStatus.PENDING.value == "pending"
