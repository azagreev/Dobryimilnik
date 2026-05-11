from enum import StrEnum
from uuid import UUID

from pydantic import Field

from app.core.pagination import PageParams
from app.core.schemas import APIModel
from app.domains.imports.csv_contract import CSV_CONTRACT_VERSION, ImportEntityType


class ImportBatchStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    COMPLETED_WITH_ERRORS = "completed_with_errors"
    FAILED = "failed"


class ImportErrorSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class ImportBatchCreate(APIModel):
    contract_version: str = CSV_CONTRACT_VERSION


class ImportBatchSummary(APIModel):
    batch_id: UUID
    status: ImportBatchStatus
    total_rows: int = Field(ge=0)
    staged_rows: int = Field(ge=0)
    skipped_rows: int = Field(ge=0)
    failed_rows: int = Field(ge=0)
    requires_review_rows: int = Field(ge=0)


class ImportErrorRow(APIModel):
    row_number: int = Field(ge=1)
    entity_type: ImportEntityType
    field: str
    code: str
    message: str
    severity: ImportErrorSeverity


class ImportErrorTable(APIModel):
    batch_id: UUID
    page: PageParams
    errors: list[ImportErrorRow]
