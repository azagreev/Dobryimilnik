# Phase 2: Livemaster Import Pipeline - Patterns

**Generated:** 2026-05-11  
**Scope:** Existing backend scaffold patterns relevant to Phase 2 planning.

## Closest Existing Analogs

| New Phase 2 Area | Closest Existing Pattern | Notes |
|------------------|--------------------------|-------|
| Import API router | `backend/app/api/v1/health.py`, `backend/app/api/v1/router.py` | Define an `APIRouter`, include it from the v1 router, and test through `httpx.AsyncClient` with `ASGITransport`. |
| Import domain package | `backend/app/domains/{catalog,orders,users,content,analytics}/` | Existing domain modules use `api.py`, `service.py`, `repository.py`, `models.py`. Phase 2 should add an `imports` package with the same layering. |
| SQLAlchemy models | `backend/app/core/db.py` | Use shared `Base`, metadata naming convention, async sessions, and schema-qualified table definitions. |
| Alembic migration | `backend/alembic/versions/0001_create_domain_schemas.py` | Add a new migration for `staging` schema and import tables. Keep upgrade/downgrade explicit and reversible. |
| Migration checks | `backend/tests/test_migrations.py` | Extend source-level checks and add behavior-level tests where possible. |
| API tests | `backend/tests/test_health.py` | Use `pytest.mark.anyio`, `ASGITransport`, and `AsyncClient` for route tests. |
| Domain importability tests | `backend/tests/test_domain_packages.py` | Add `imports` to domain package coverage after the package exists. |

## Established Constraints

- Keep backend code under `backend/app`.
- Keep API routes under `/api/v1`.
- Preserve strict typing: `mypy` runs in strict mode.
- Preserve lint style: Ruff rules `E`, `F`, `I`, `UP`, `B`; line length 100.
- Use pytest under `backend/tests`; avoid watch-mode commands in plans.
- Avoid direct committed secrets or local credentials in tests/fixtures.

## Recommended File Mapping

| Planned File | Pattern Source | Purpose |
|--------------|----------------|---------|
| `backend/app/domains/imports/api.py` | `backend/app/api/v1/health.py` | Import batch upload/status/error routes. |
| `backend/app/domains/imports/service.py` | domain service skeletons | CSV orchestration, validation flow, row classification. |
| `backend/app/domains/imports/repository.py` | domain repository skeletons + `core/db.py` | Batch, row, source mapping, and error persistence. |
| `backend/app/domains/imports/models.py` | `core/db.py` + Alembic setup | SQLAlchemy models for staging tables. |
| `backend/app/domains/imports/schemas.py` | FastAPI/Pydantic project style | Response/request schemas for batch summary and error table. |
| `backend/app/domains/imports/csv_contract.py` | no existing analog | Single CSV headers, parsing, and row-number preservation. |
| `backend/app/domains/imports/validation.py` | no existing analog | Entity-specific validation and structured error codes. |
| `backend/alembic/versions/0002_create_import_staging.py` | `0001_create_domain_schemas.py` | `staging` schema, import tables, indexes, constraints. |
| `backend/tests/test_imports_*.py` | existing pytest files | Contract, validation, repository, idempotency, and API coverage. |

## Integration Notes

- Include the imports router from `backend/app/api/v1/router.py`.
- If an `imports` domain is added, update `backend/tests/test_domain_packages.py`.
- Migration tests should assert `staging` is introduced only in Phase 2 migrations, preserving the Phase 1 invariant.
- If repository tests need real PostgreSQL behavior for `ON CONFLICT`, planner should explicitly decide whether to add a test database fixture or limit the first tests to SQL/source-level checks.

## Risks for Planning

- `source_mappings` idempotency should rely on database unique constraints, not only service logic.
- A one-CSV contract can still become ambiguous; the plan must define required columns before implementing parser behavior.
- Error table API should be stable enough for future admin UI but should not build the full UI in Phase 2.
- Background processing should stay testable. Introducing Celery without worker/test wiring would increase execution risk.
