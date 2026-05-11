---
phase: 02-livemaster-import-pipeline
plan: 03
subsystem: validation
tags: [csv, validation, imports, staging]
requires:
  - phase: 02-02-staging-tables-and-source-identity-preservation
    provides: Staging repository primitives
provides:
  - Normalized CSV import rows
  - Entity-specific row validation
  - Batch-continuing service path for failed rows
affects: [phase-02-imports, phase-04-admin-catalog]
tech-stack:
  added: []
  patterns: [structured validation result, tolerant service parser, row-level error persistence]
key-files:
  created:
    - backend/app/domains/imports/validation.py
    - backend/tests/test_imports_validation.py
  modified:
    - backend/app/domains/imports/csv_contract.py
    - backend/app/domains/imports/service.py
key-decisions:
  - "Strict contract parsing remains available while service validation uses a tolerant raw-row parser."
  - "Unsupported entity types and missing entity-specific fields become row-level structured errors."
  - "Failed rows are staged with failed status and batch processing continues."
patterns-established:
  - "Validation returns typed result objects instead of raising for row-level failures."
requirements-completed: [IMP-02, IMP-05]
duration: 16 min
completed: 2026-05-11
---

# Phase 02 Plan 03: Validation and Normalization Pipeline Summary

**CSV rows now normalize into auditable staging inputs with strict row-level validation**

## Performance

- **Duration:** 16 min
- **Started:** 2026-05-11T18:00:00Z
- **Completed:** 2026-05-11T18:16:00Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments

- Extended CSV row parsing with normalized payloads, parent source ID extraction, and deterministic content hashes.
- Added tolerant raw-row parsing for service workflows so malformed rows can become structured row errors.
- Added entity-specific validation for products, variants, categories, media, posts, reviews, customers, and orders.
- Wired service logic to stage valid rows, stage failed rows as failed, persist structured errors, and continue processing later rows.
- Added tests for row numbers, raw payload preservation, supported entity types, structured errors, and batch-continuing behavior.

## Task Commits

Each task was committed atomically:

1. **Task 1: Build row parser and normalized internal row representation** - `bb66d06` (`feat`)
2. **Task 2: Implement entity-specific strict row validation** - `ef9c8b3` (`feat`)

**Plan metadata:** pending in docs commit

## Files Created/Modified

- `backend/app/domains/imports/csv_contract.py` - Adds normalized payload, content hash, parent source ID, and raw-row parser.
- `backend/app/domains/imports/validation.py` - Adds row validation result types and entity-specific rules.
- `backend/app/domains/imports/service.py` - Adds validation/staging service methods.
- `backend/tests/test_imports_validation.py` - Covers parser, validation, structured errors, and batch continuation.

## Decisions Made

- Kept `parse_csv_rows` strict for the existing CSV contract tests.
- Added `parse_raw_csv_rows` for batch processing so row-level validation can continue after bad rows.
- Used explicit field/code/message/severity errors suitable for the later owner-facing error table.

## Deviations from Plan

None - plan executed exactly as written.

**Total deviations:** 0 auto-fixed.
**Impact on plan:** None.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Verification

- `uv run pytest tests/test_imports_validation.py` - passed, 4 tests.
- `uv run pytest tests/test_imports_contract.py tests/test_imports_repository.py tests/test_imports_validation.py` - passed, 14 tests.

## Self-Check: PASSED

- Parser preserves original CSV row numbers.
- Parser recognizes supported entity types and keeps raw payloads.
- Invalid rows produce structured errors and do not stop the batch.
- Valid rows are passed to staging persistence.
- No canonical write path exists.

## Next Phase Readiness

Plan 02-04 can now classify reruns and changed/unchanged rows using content hashes and source mappings.

---
*Phase: 02-livemaster-import-pipeline*
*Completed: 2026-05-11*
