---
phase: 02-livemaster-import-pipeline
plan: 02
subsystem: persistence
tags: [postgresql, alembic, sqlalchemy, imports]
requires:
  - phase: 02-01-source-file-contract-and-import-batch-model
    provides: Imports domain package and CSV identity contract
provides:
  - Staging schema migration
  - Import batch, row, source mapping, and error models
  - Async repository primitives for import persistence
affects: [phase-02-imports, phase-03-catalog, phase-04-admin-catalog]
tech-stack:
  added: []
  patterns: [schema-qualified SQLAlchemy models, Alembic staging migration, PostgreSQL upsert]
key-files:
  created:
    - backend/alembic/versions/0002_create_import_staging.py
    - backend/tests/test_imports_repository.py
  modified:
    - backend/app/domains/imports/models.py
    - backend/app/domains/imports/repository.py
    - backend/tests/test_migrations.py
key-decisions:
  - "Import persistence is isolated in the staging schema."
  - "Source identity uniqueness is enforced by source_system, entity_type, and source_id."
  - "Repository upsert intent uses PostgreSQL ON CONFLICT against the source identity key."
patterns-established:
  - "Staging models use schema-qualified SQLAlchemy tables under the imports domain."
  - "Repository query builders isolate PostgreSQL-specific statements for unit verification."
requirements-completed: [IMP-01, IMP-04]
duration: 18 min
completed: 2026-05-11
---

# Phase 02 Plan 02: Staging Tables and Source Identity Preservation Summary

**Staging persistence now preserves Livemaster source identity with database-backed uniqueness**

## Performance

- **Duration:** 18 min
- **Started:** 2026-05-11T17:41:00Z
- **Completed:** 2026-05-11T17:59:00Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments

- Added Alembic revision `0002_create_import_staging.py`.
- Created `staging.import_batches`, `staging.import_rows`, `staging.source_mappings`, and `staging.import_errors`.
- Added schema-qualified SQLAlchemy models for import batches, rows, source mappings, and structured errors.
- Added uniqueness for source mappings across `source_system`, `entity_type`, and `source_id`.
- Implemented repository methods to create batches, add rows, add structured errors, find/upsert source mappings, and build summary/error-table queries.
- Added migration and repository tests for staging-only behavior, source identity uniqueness, and PostgreSQL upsert SQL.

## Task Commits

Each task was committed atomically:

1. **Task 1: Add staging schema migration and SQLAlchemy models** - `5fa4e47` (`feat`)
2. **Task 2: Implement repository methods for batches, rows, source mappings, and errors** - `07d9bcb` (`feat`)

**Plan metadata:** pending in docs commit

## Files Created/Modified

- `backend/alembic/versions/0002_create_import_staging.py` - Creates and reverses Phase 2 staging schema objects.
- `backend/app/domains/imports/models.py` - Adds import persistence models and row status enum.
- `backend/app/domains/imports/repository.py` - Adds async persistence methods and query builders.
- `backend/tests/test_migrations.py` - Extends migration source checks for Phase 2.
- `backend/tests/test_imports_repository.py` - Covers repository contracts and upsert SQL.

## Decisions Made

- Kept Phase 2 persistence staging-only; no canonical catalog/content/user/order tables are touched.
- Stored raw and normalized row payloads as JSONB to preserve auditability while later phases define canonical models.
- Tested PostgreSQL upsert behavior through SQL compilation because no PostgreSQL test container is wired yet.

## Deviations from Plan

None - plan executed exactly as written.

**Total deviations:** 0 auto-fixed.
**Impact on plan:** None.

## Issues Encountered

- Repository upsert execution still needs PostgreSQL-backed integration coverage when a test database fixture is introduced. The statement construction is unit-tested against the PostgreSQL dialect.

## User Setup Required

None - no external service configuration required.

## Verification

- `uv run pytest tests/test_migrations.py` - passed, 5 tests.
- `uv run pytest tests/test_imports_repository.py` - passed, 6 tests.
- `uv run pytest tests/test_migrations.py tests/test_imports_repository.py` - passed, 11 tests.

## Self-Check: PASSED

- Staging schema migration exists and creates all four required tables.
- Source mapping uniqueness is present in migration, model, and tests.
- Repository methods persist batch, row, error, and source mapping primitives.
- No canonical publish code exists.

## Next Phase Readiness

Plan 02-03 can now build validation and normalization on top of durable staging rows and structured error persistence.

---
*Phase: 02-livemaster-import-pipeline*
*Completed: 2026-05-11*
