from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.domains.imports.csv_contract import CsvImportRow, parse_raw_csv_rows
from app.domains.imports.models import ImportRowStatus, SourceMapping
from app.domains.imports.repository import DEFAULT_SOURCE_SYSTEM, ImportsRepository
from app.domains.imports.schemas import (
    ImportBatchRunResponse,
    ImportBatchStatus,
    ImportBatchSummary,
    ImportErrorRow,
    ImportErrorTable,
)
from app.core.pagination import PageParams
from app.domains.imports.validation import ImportRowValidationResult, validate_raw_rows


@dataclass(frozen=True)
class ImportValidationOutcome:
    results: list[ImportRowValidationResult]

    @property
    def valid_rows_count(self) -> int:
        return sum(1 for result in self.results if result.is_valid)

    @property
    def failed_rows_count(self) -> int:
        return sum(1 for result in self.results if not result.is_valid)


class ImportsService:
    def __init__(self, repository: ImportsRepository) -> None:
        self.repository = repository

    def validate_csv_content(self, content: str) -> ImportValidationOutcome:
        raw_rows = parse_raw_csv_rows(content)
        return ImportValidationOutcome(results=validate_raw_rows(raw_rows))

    async def classify_row(self, row: CsvImportRow) -> ImportRowStatus:
        mapping = await self.repository.find_source_mapping(
            source_system=DEFAULT_SOURCE_SYSTEM,
            entity_type=row.entity_type,
            source_id=row.source_id,
        )
        status = classify_source_mapping(mapping, row.content_hash)
        await self.repository.upsert_source_mapping(
            batch_id=getattr(row, "batch_id", None),
            entity_type=row.entity_type,
            source_id=row.source_id,
            content_hash=row.content_hash,
            source_system=DEFAULT_SOURCE_SYSTEM,
        )
        return status

    async def stage_csv_content(self, content: str) -> ImportValidationOutcome:
        summary = await self.run_csv_import(content)
        return ImportValidationOutcome(
            results=getattr(summary, "_validation_results", []),
        )

    async def run_csv_import(self, content: str) -> ImportBatchRunResponse:
        raw_rows = parse_raw_csv_rows(content)
        results = validate_raw_rows(raw_rows)
        batch = await self.repository.create_batch(total_rows=len(raw_rows))

        for result in results:
            if result.row is not None:
                status = await self.classify_row_for_batch(result.row, batch.id)
                await self.repository.add_import_rows(batch_id=batch.id, rows=[result.row], status=status)
                continue

            first_error = result.errors[0]
            failed_row = error_to_failed_row(first_error.row_number, first_error.entity_type.value)
            persisted_rows = await self.repository.add_import_rows(
                batch_id=batch.id,
                rows=[failed_row],
                status=ImportRowStatus.FAILED,
            )
            row_id = getattr(persisted_rows[0], "id", None) if persisted_rows else None
            for error in result.errors:
                await self.repository.add_error(
                    batch_id=batch.id,
                    row_id=row_id,
                    row_number=error.row_number,
                    entity_type=error.entity_type,
                    field=error.field,
                    code=error.code,
                    message=error.message,
                    severity=error.severity,
                )

        failed_rows = sum(1 for result in results if not result.is_valid)
        staged_rows = sum(1 for result in results if result.is_valid)
        status = (
            ImportBatchStatus.COMPLETED_WITH_ERRORS
            if failed_rows
            else ImportBatchStatus.COMPLETED
        )
        response = ImportBatchRunResponse(
            batch_id=batch.id,
            status=status,
            total_rows=len(results),
            staged_rows=staged_rows,
            skipped_rows=0,
            failed_rows=failed_rows,
            requires_review_rows=0,
        )
        object.__setattr__(response, "_validation_results", results)
        return response

    async def classify_row_for_batch(self, row: CsvImportRow, batch_id: object) -> ImportRowStatus:
        mapping = await self.repository.find_source_mapping(
            source_system=DEFAULT_SOURCE_SYSTEM,
            entity_type=row.entity_type,
            source_id=row.source_id,
        )
        status = classify_source_mapping(mapping, row.content_hash)
        await self.repository.upsert_source_mapping(
            batch_id=batch_id,
            entity_type=row.entity_type,
            source_id=row.source_id,
            content_hash=row.content_hash,
            source_system=DEFAULT_SOURCE_SYSTEM,
        )
        return status

    async def get_batch_summary(self, batch_id: UUID) -> ImportBatchSummary:
        row = await self.repository.fetch_batch_summary_row(batch_id)
        batch = row[0]
        return ImportBatchSummary(
            batch_id=batch.id,
            status=ImportBatchStatus(batch.status),
            total_rows=batch.total_rows,
            staged_rows=row.staged_rows or 0,
            skipped_rows=row.skipped_rows or 0,
            failed_rows=row.failed_rows or 0,
            requires_review_rows=row.requires_review_rows or 0,
        )

    async def get_error_table(self, batch_id: UUID, page: PageParams) -> ImportErrorTable:
        errors = await self.repository.list_errors(
            batch_id=batch_id,
            limit=page.limit,
            offset=page.offset,
        )
        return ImportErrorTable(
            batch_id=batch_id,
            page=page,
            errors=[
                ImportErrorRow(
                    row_number=error.row_number,
                    entity_type=error.entity_type,
                    field=error.field,
                    code=error.code,
                    message=error.message,
                    severity=error.severity,
                )
                for error in errors
            ],
        )


def classify_source_mapping(
    mapping: SourceMapping | None,
    content_hash: str | None,
) -> ImportRowStatus:
    if mapping is None:
        return ImportRowStatus.NEW
    if mapping.content_hash == content_hash:
        return ImportRowStatus.UNCHANGED
    return ImportRowStatus.CHANGED


def error_to_failed_row(row_number: int, entity_type: str) -> object:
    from app.domains.imports.csv_contract import CsvImportRow, ImportEntityType

    parsed_entity_type = ImportEntityType(entity_type)
    return CsvImportRow(
        row_number=row_number,
        entity_type=parsed_entity_type,
        source_id=f"invalid-row-{row_number}",
        raw={"entity_type": entity_type, "source_id": ""},
        normalized_payload={},
    )
