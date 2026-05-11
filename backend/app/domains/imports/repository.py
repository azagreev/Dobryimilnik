from __future__ import annotations

import uuid
from collections.abc import Sequence

from sqlalchemy import Select, case, func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.imports.csv_contract import CSV_CONTRACT_VERSION, CsvImportRow, ImportEntityType
from app.domains.imports.models import (
    ImportBatch,
    ImportError,
    ImportRow,
    ImportRowStatus,
    SourceMapping,
)
from app.domains.imports.schemas import ImportBatchStatus, ImportErrorSeverity

DEFAULT_SOURCE_SYSTEM = "livemaster"


class ImportsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_batch(
        self,
        *,
        source_system: str = DEFAULT_SOURCE_SYSTEM,
        contract_version: str = CSV_CONTRACT_VERSION,
        total_rows: int = 0,
        status: ImportBatchStatus = ImportBatchStatus.PENDING,
    ) -> ImportBatch:
        batch = ImportBatch(
            source_system=source_system,
            contract_version=contract_version,
            total_rows=total_rows,
            status=status.value,
        )
        self.session.add(batch)
        await self.session.flush()
        await self.session.refresh(batch)
        return batch

    async def add_import_rows(
        self,
        *,
        batch_id: uuid.UUID,
        rows: Sequence[CsvImportRow],
        status: ImportRowStatus = ImportRowStatus.NEW,
    ) -> list[ImportRow]:
        import_rows = [
            ImportRow(
                batch_id=batch_id,
                row_number=row.row_number,
                entity_type=row.entity_type.value,
                source_id=row.source_id,
                status=status.value,
                raw_payload=row.raw,
                normalized_payload={},
            )
            for row in rows
        ]
        self.session.add_all(import_rows)
        await self.session.flush()
        return import_rows

    async def add_error(
        self,
        *,
        batch_id: uuid.UUID,
        row_number: int,
        entity_type: ImportEntityType,
        field: str,
        code: str,
        message: str,
        severity: ImportErrorSeverity = ImportErrorSeverity.ERROR,
        row_id: uuid.UUID | None = None,
    ) -> ImportError:
        error = ImportError(
            batch_id=batch_id,
            row_id=row_id,
            row_number=row_number,
            entity_type=entity_type.value,
            field=field,
            code=code,
            message=message,
            severity=severity.value,
        )
        self.session.add(error)
        await self.session.flush()
        return error

    async def find_source_mapping(
        self,
        *,
        source_system: str = DEFAULT_SOURCE_SYSTEM,
        entity_type: ImportEntityType,
        source_id: str,
    ) -> SourceMapping | None:
        statement = select(SourceMapping).where(
            SourceMapping.source_system == source_system,
            SourceMapping.entity_type == entity_type.value,
            SourceMapping.source_id == source_id,
        )
        return await self.session.scalar(statement)

    async def upsert_source_mapping(
        self,
        *,
        batch_id: uuid.UUID,
        entity_type: ImportEntityType,
        source_id: str,
        content_hash: str | None,
        source_system: str = DEFAULT_SOURCE_SYSTEM,
    ) -> SourceMapping:
        statement = self.build_source_mapping_upsert(
            batch_id=batch_id,
            entity_type=entity_type,
            source_id=source_id,
            content_hash=content_hash,
            source_system=source_system,
        )
        result = await self.session.execute(statement)
        return result.scalar_one()

    def build_batch_summary_statement(self, batch_id: uuid.UUID) -> Select[tuple[ImportBatch]]:
        staged_count = func.count(ImportRow.id).label("staged_rows")
        skipped_count = func.sum(
            case((ImportRow.status == ImportRowStatus.SKIPPED.value, 1), else_=0)
        ).label("skipped_rows")
        failed_count = func.sum(
            case((ImportRow.status == ImportRowStatus.FAILED.value, 1), else_=0)
        ).label("failed_rows")
        review_count = func.sum(
            case((ImportRow.status == ImportRowStatus.REQUIRES_REVIEW.value, 1), else_=0)
        ).label("requires_review_rows")

        return (
            select(
                ImportBatch,
                staged_count,
                skipped_count,
                failed_count,
                review_count,
            )
            .outerjoin(ImportRow, ImportRow.batch_id == ImportBatch.id)
            .where(ImportBatch.id == batch_id)
            .group_by(ImportBatch.id)
        )

    async def fetch_batch_summary_row(self, batch_id: uuid.UUID) -> object:
        result = await self.session.execute(self.build_batch_summary_statement(batch_id))
        return result.one()

    def build_error_table_statement(
        self,
        *,
        batch_id: uuid.UUID,
        limit: int,
        offset: int,
    ) -> Select[tuple[ImportError]]:
        return (
            select(ImportError)
            .where(ImportError.batch_id == batch_id)
            .order_by(ImportError.row_number.asc(), ImportError.id.asc())
            .limit(limit)
            .offset(offset)
        )

    async def list_errors(
        self,
        *,
        batch_id: uuid.UUID,
        limit: int,
        offset: int = 0,
    ) -> Sequence[ImportError]:
        result = await self.session.scalars(
            self.build_error_table_statement(batch_id=batch_id, limit=limit, offset=offset)
        )
        return result.all()

    @staticmethod
    def build_source_mapping_upsert(
        *,
        batch_id: uuid.UUID,
        entity_type: ImportEntityType,
        source_id: str,
        content_hash: str | None,
        source_system: str = DEFAULT_SOURCE_SYSTEM,
    ) -> object:
        statement = pg_insert(SourceMapping).values(
            id=uuid.uuid4(),
            source_system=source_system,
            entity_type=entity_type.value,
            source_id=source_id,
            batch_id=batch_id,
            content_hash=content_hash,
        )
        return statement.on_conflict_do_update(
            index_elements=[
                SourceMapping.source_system,
                SourceMapping.entity_type,
                SourceMapping.source_id,
            ],
            set_={
                "batch_id": batch_id,
                "content_hash": content_hash,
                "updated_at": func.now(),
            },
        ).returning(SourceMapping)
