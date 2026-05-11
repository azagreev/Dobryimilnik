from __future__ import annotations

import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from app.domains.imports.api import get_imports_service
from app.domains.imports.csv_contract import ImportEntityType
from app.domains.imports.schemas import (
    ImportBatchRunResponse,
    ImportBatchStatus,
    ImportBatchSummary,
    ImportErrorRow,
    ImportErrorSeverity,
    ImportErrorTable,
)
from app.main import app
from app.core.pagination import PageParams


class ImportsServiceStub:
    def __init__(self) -> None:
        self.batch_id = uuid.uuid4()
        self.received_csv: str | None = None

    async def run_csv_import(self, content: str) -> ImportBatchRunResponse:
        self.received_csv = content
        return ImportBatchRunResponse(
            batch_id=self.batch_id,
            status=ImportBatchStatus.COMPLETED_WITH_ERRORS,
            total_rows=3,
            staged_rows=2,
            skipped_rows=0,
            failed_rows=1,
            requires_review_rows=0,
        )

    async def get_batch_summary(self, batch_id: uuid.UUID) -> ImportBatchSummary:
        return ImportBatchSummary(
            batch_id=batch_id,
            status=ImportBatchStatus.COMPLETED_WITH_ERRORS,
            total_rows=3,
            staged_rows=2,
            skipped_rows=0,
            failed_rows=1,
            requires_review_rows=0,
        )

    async def get_error_table(self, batch_id: uuid.UUID, page: PageParams) -> ImportErrorTable:
        return ImportErrorTable(
            batch_id=batch_id,
            page=page,
            errors=[
                ImportErrorRow(
                    row_number=3,
                    entity_type=ImportEntityType.VARIANT,
                    field="parent_source_id",
                    code="required",
                    message="parent_source_id is required for variant rows.",
                    severity=ImportErrorSeverity.ERROR,
                )
            ],
        )


@pytest.fixture
def service_stub() -> ImportsServiceStub:
    stub = ImportsServiceStub()
    app.dependency_overrides[get_imports_service] = lambda: stub
    return stub


@pytest.fixture(autouse=True)
def clear_dependency_overrides() -> None:
    yield
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_import_run_endpoint_accepts_csv_and_returns_batch_summary(
    service_stub: ImportsServiceStub,
) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post(
            "/api/v1/imports/batches",
            content="entity_type,source_id,name\nproduct,p-1,Soap\n",
            headers={"content-type": "text/csv"},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["batch_id"] == str(service_stub.batch_id)
    assert payload["status"] == "completed_with_errors"
    assert payload["staged_rows"] == 2
    assert payload["failed_rows"] == 1
    assert payload["requires_review_rows"] == 0
    assert service_stub.received_csv == "entity_type,source_id,name\nproduct,p-1,Soap\n"


@pytest.mark.anyio
async def test_batch_status_endpoint_returns_summary_counts(service_stub: ImportsServiceStub) -> None:
    batch_id = uuid.uuid4()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get(f"/api/v1/imports/batches/{batch_id}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["batch_id"] == str(batch_id)
    assert payload["status"] == "completed_with_errors"
    assert payload["total_rows"] == 3
    assert payload["staged_rows"] == 2
    assert payload["skipped_rows"] == 0
    assert payload["failed_rows"] == 1
    assert payload["requires_review_rows"] == 0


@pytest.mark.anyio
async def test_error_table_endpoint_returns_stable_paginated_fields(
    service_stub: ImportsServiceStub,
) -> None:
    batch_id = uuid.uuid4()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get(f"/api/v1/imports/batches/{batch_id}/errors?limit=10&offset=20")

    assert response.status_code == 200
    payload = response.json()
    assert payload["batch_id"] == str(batch_id)
    assert payload["page"] == {"limit": 10, "offset": 20}
    assert payload["errors"] == [
        {
            "row_number": 3,
            "entity_type": "variant",
            "field": "parent_source_id",
            "code": "required",
            "message": "parent_source_id is required for variant rows.",
            "severity": "error",
        }
    ]
    assert "raw" not in payload["errors"][0]
    assert "raw_payload" not in payload["errors"][0]
