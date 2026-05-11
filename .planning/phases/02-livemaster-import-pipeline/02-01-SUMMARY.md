---
phase: 02-livemaster-import-pipeline
plan: 01
subsystem: api
tags: [fastapi, csv, imports, pydantic]
requires:
  - phase: 01-foundation-and-domain-skeleton
    provides: FastAPI app, API v1 router, domain package pattern
provides:
  - Imports domain package scaffold
  - Versioned single-CSV import contract
  - Batch summary and error-table schemas
affects: [phase-02-imports, phase-04-admin-catalog]
tech-stack:
  added: []
  patterns: [FastAPI APIRouter domain package, Pydantic response schemas, CSV contract parser]
key-files:
  created:
    - backend/app/domains/imports/__init__.py
    - backend/app/domains/imports/api.py
    - backend/app/domains/imports/csv_contract.py
    - backend/app/domains/imports/models.py
    - backend/app/domains/imports/repository.py
    - backend/app/domains/imports/schemas.py
    - backend/app/domains/imports/service.py
    - backend/tests/test_imports_contract.py
  modified:
    - backend/app/api/v1/router.py
    - backend/tests/test_domain_packages.py
key-decisions:
  - "Imports are a dedicated backend domain rather than being folded into catalog."
  - "The first Livemaster import contract is one versioned CSV requiring entity_type and source_id."
patterns-established:
  - "Import domain follows existing API/service/repository/models layering."
  - "CSV contract parsing preserves source row numbers before persistence exists."
requirements-completed: [IMP-01, IMP-03]
duration: 10 min
completed: 2026-05-11
---

# Phase 02 Plan 01: Source File Contract and Import Batch Model Summary

**Imports domain scaffold with a versioned single-CSV contract and owner-facing error-table schemas**

## Performance

- **Duration:** 10 min
- **Started:** 2026-05-11T17:30:00Z
- **Completed:** 2026-05-11T17:40:00Z
- **Tasks:** 2
- **Files modified:** 10

## Accomplishments

- Added `app.domains.imports` as an importable domain package following the Phase 1 layering pattern.
- Registered the imports router under `/api/v1/imports`.
- Added a versioned single-CSV contract that requires `entity_type` and `source_id`, preserves row numbers, and validates supported import entity types.
- Added Pydantic schemas for import batch summaries and detailed error-table rows.
- Added tests for domain importability and CSV contract behavior.

## Task Commits

Each task was committed atomically:

1. **Task 1: Add imports domain package and router integration** - `172e998` (`feat`)
2. **Task 2: Define single CSV contract and batch request/response schemas** - `dfb2252` (`feat`)

**Plan metadata:** pending in docs commit

## Files Created/Modified

- `backend/app/domains/imports/__init__.py` - Imports domain package marker.
- `backend/app/domains/imports/api.py` - Imports API router scaffold.
- `backend/app/domains/imports/csv_contract.py` - Single-CSV contract, supported entity types, and parser.
- `backend/app/domains/imports/models.py` - Placeholder for Phase 2 staging models.
- `backend/app/domains/imports/repository.py` - Placeholder repository class.
- `backend/app/domains/imports/schemas.py` - Batch status, summary, and error-table schemas.
- `backend/app/domains/imports/service.py` - Placeholder service class.
- `backend/app/api/v1/router.py` - Includes imports router.
- `backend/tests/test_domain_packages.py` - Covers imports domain modules.
- `backend/tests/test_imports_contract.py` - Covers accepted headers, missing headers, row numbers, unsupported entity type, and schema fields.

## Decisions Made

- Used a dedicated `imports` domain because Phase 2 crosses catalog, content, customers, orders, and reviews.
- Required `entity_type` and `source_id` as the minimum CSV identity contract.
- Kept persistence and business execution out of this plan; later plans own staging schema and validation pipeline.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Added schema content during router scaffold**
- **Found during:** Task 1 (imports domain package)
- **Issue:** `schemas.py` needed to be importable as part of the domain package, and later tests needed stable schema names.
- **Fix:** Added the initial Pydantic schema definitions before the CSV contract commit.
- **Files modified:** `backend/app/domains/imports/schemas.py`
- **Verification:** `uv run pytest tests/test_domain_packages.py tests/test_imports_contract.py`
- **Committed in:** `172e998` and completed with `dfb2252`

---

**Total deviations:** 1 auto-fixed (Rule 3).
**Impact on plan:** Low. The schema file was already in the plan scope and the final behavior matches acceptance criteria.

## Issues Encountered

- Sandbox initially blocked `uv` cache writes under `/home/azagreev/.cache/uv`; reran pytest with approved elevated execution.

## User Setup Required

None - no external service configuration required.

## Verification

- `uv run pytest tests/test_domain_packages.py tests/test_imports_contract.py` — passed, 5 tests.

## Next Phase Readiness

Plan 02-02 can now add staging schema models and repositories against the imports domain package and CSV identity contract.

---
*Phase: 02-livemaster-import-pipeline*
*Completed: 2026-05-11*
