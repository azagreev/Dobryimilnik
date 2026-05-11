from uuid import UUID

from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.pagination import PageParams
from app.domains.imports.repository import ImportsRepository
from app.domains.imports.schemas import ImportBatchRunResponse, ImportBatchSummary, ImportErrorTable
from app.domains.imports.service import ImportsService

router = APIRouter()


def get_imports_service(session: AsyncSession = Depends(get_session)) -> ImportsService:
    return ImportsService(ImportsRepository(session))


@router.post("/batches", response_model=ImportBatchRunResponse)
async def run_import_batch(
    csv_content: str = Body(..., media_type="text/csv"),
    service: ImportsService = Depends(get_imports_service),
) -> ImportBatchRunResponse:
    return await service.run_csv_import(csv_content)


@router.get("/batches/{batch_id}", response_model=ImportBatchSummary)
async def get_import_batch(
    batch_id: UUID,
    service: ImportsService = Depends(get_imports_service),
) -> ImportBatchSummary:
    return await service.get_batch_summary(batch_id)


@router.get("/batches/{batch_id}/errors", response_model=ImportErrorTable)
async def get_import_errors(
    batch_id: UUID,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    service: ImportsService = Depends(get_imports_service),
) -> ImportErrorTable:
    return await service.get_error_table(batch_id, PageParams(limit=limit, offset=offset))
