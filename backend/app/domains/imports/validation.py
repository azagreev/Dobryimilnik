from __future__ import annotations

from dataclasses import dataclass

from app.domains.imports.csv_contract import (
    CsvImportRow,
    CsvRawRow,
    ImportEntityType,
    build_import_row,
)
from app.domains.imports.schemas import ImportErrorSeverity


@dataclass(frozen=True)
class ImportRowValidationError:
    row_number: int
    entity_type: ImportEntityType
    field: str
    code: str
    message: str
    severity: ImportErrorSeverity = ImportErrorSeverity.ERROR


@dataclass(frozen=True)
class ImportRowValidationResult:
    row_number: int
    row: CsvImportRow | None
    errors: tuple[ImportRowValidationError, ...]

    @property
    def is_valid(self) -> bool:
        return self.row is not None and not self.errors


ENTITY_REQUIRED_FIELDS: dict[ImportEntityType, frozenset[str]] = {
    ImportEntityType.PRODUCT: frozenset({"name"}),
    ImportEntityType.VARIANT: frozenset({"parent_source_id", "sku"}),
    ImportEntityType.CATEGORY: frozenset({"name"}),
    ImportEntityType.MEDIA: frozenset({"parent_source_id", "media_url"}),
    ImportEntityType.POST: frozenset({"name"}),
    ImportEntityType.REVIEW: frozenset({"parent_source_id"}),
    ImportEntityType.CUSTOMER: frozenset({"name"}),
    ImportEntityType.ORDER: frozenset(),
}


def validate_raw_row(raw_row: CsvRawRow) -> ImportRowValidationResult:
    raw = raw_row.raw
    fallback_entity_type = ImportEntityType.PRODUCT
    errors: list[ImportRowValidationError] = []

    try:
        entity_type = ImportEntityType(raw.get("entity_type", ""))
    except ValueError:
        entity_type = fallback_entity_type
        errors.append(
            ImportRowValidationError(
                row_number=raw_row.row_number,
                entity_type=entity_type,
                field="entity_type",
                code="unsupported_entity_type",
                message="Unsupported import entity type.",
            )
        )

    source_id = raw.get("source_id", "").strip()
    if not source_id:
        errors.append(
            ImportRowValidationError(
                row_number=raw_row.row_number,
                entity_type=entity_type,
                field="source_id",
                code="required",
                message="Source ID is required.",
            )
        )

    for field in sorted(ENTITY_REQUIRED_FIELDS[entity_type]):
        if not raw.get(field, "").strip():
            errors.append(
                ImportRowValidationError(
                    row_number=raw_row.row_number,
                    entity_type=entity_type,
                    field=field,
                    code="required",
                    message=f"{field} is required for {entity_type.value} rows.",
                )
            )

    if errors:
        return ImportRowValidationResult(
            row_number=raw_row.row_number,
            row=None,
            errors=tuple(errors),
        )

    row = build_import_row(
        raw_row.row_number,
        raw,
        entity_type=entity_type,
        source_id=source_id,
    )
    return ImportRowValidationResult(row_number=raw_row.row_number, row=row, errors=())


def validate_raw_rows(raw_rows: list[CsvRawRow]) -> list[ImportRowValidationResult]:
    return [validate_raw_row(raw_row) for raw_row in raw_rows]
