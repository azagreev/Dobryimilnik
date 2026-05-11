---
phase: 02-livemaster-import-pipeline
plan: 04
subsystem: idempotency
tags: [imports, idempotency, staging, source-mapping]
requires:
  - phase: 02-03-validation-and-normalization-pipeline
    provides: Normalized rows and content hashes
provides:
  - Row classification for new, unchanged, and changed reruns
  - Source mapping upsert integration in the service
  - Rerun tests proving no duplicate source identities
affects: [phase-02-imports, phase-03-catalog]
tech-stack:
  added: []
  patterns: [source-id-plus-content-hash classification, staging-only rerun processing]
key-files:
  created:
    - backend/tests/test_imports_idempotency.py
  modified:
    - backend/app/domains/imports/repository.py
    - backend/app/domains/imports/service.py
    - backend/tests/test_imports_validation.py
key-decisions:
  - "Source mappings are keyed by source system, entity type, and source ID; content hash only classifies changed content."
  - "Reruns upsert the existing source mapping instead of creating duplicate identities."
  - "Phase 2 remains staging-only despite older roadmap canonical publish wording."
patterns-established:
  - "Import service classifies valid rows before staging them."
requirements-completed: [IMP-04, IMP-05]
duration: 14 min
completed: 2026-05-11
---

# Phase 02 Plan 04: Idempotent Staging Reruns and Classification Summary

**Reruns now classify rows without duplicating source identities or publishing canonical records**

## Performance

- **Duration:** 14 min
- **Started:** 2026-05-11T18:17:00Z
- **Completed:** 2026-05-11T18:31:00Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments

- Added service classification for `new`, `unchanged`, and `changed` rows based on source identity plus content hash.
- Updated repository staging to persist row content hashes and normalized payloads.
- Integrated source mapping upsert into the staging service path.
- Added idempotency tests for identical reruns, changed content, new source IDs, duplicate source IDs across batches, and deterministic hashing.
- Kept the implementation staging-only; no catalog/content/users/orders writes were added.

## Task Commits

1. **Task 1 and Task 2: Idempotent rerun classification and duplicate identity tests** - `4c36ef2` (`feat`)

**Plan metadata:** pending in docs commit

## Files Created/Modified

- `backend/app/domains/imports/repository.py` - Persists row `content_hash` and normalized payload.
- `backend/app/domains/imports/service.py` - Adds source mapping classification/upsert before staging valid rows.
- `backend/tests/test_imports_idempotency.py` - Covers rerun classification and non-duplication behavior.
- `backend/tests/test_imports_validation.py` - Updates test double for the service's source mapping contract.

## Decisions Made

- Treated source ID as the stable identity and content hash as the change detector.
- Tested source mapping non-duplication with an in-memory repository contract because no PostgreSQL test database is wired yet.
- Preserved the existing `canonical_id` placeholder in `source_mappings`, but did not write any canonical records.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Updated validation test double for idempotency service contract**
- **Found during:** Imports regression suite
- **Issue:** Existing `RecordingRepository` lacked `find_source_mapping` and `upsert_source_mapping` after the service gained rerun classification.
- **Fix:** Added those methods to the test double.
- **Files modified:** `backend/tests/test_imports_validation.py`
- **Verification:** `uv run pytest tests/test_imports_contract.py tests/test_imports_repository.py tests/test_imports_validation.py tests/test_imports_idempotency.py`
- **Committed in:** `4c36ef2`

---

**Total deviations:** 1 auto-fixed (Rule 3).
**Impact on plan:** Low. The fix keeps existing validation tests aligned with the service contract.

## Issues Encountered

- PostgreSQL-backed upsert execution remains covered by SQL compilation and service-contract tests, not by a live database fixture.

## User Setup Required

None - no external service configuration required.

## Verification

- `uv run pytest tests/test_imports_idempotency.py tests/test_imports_repository.py` - passed, 12 tests.
- `uv run pytest tests/test_imports_contract.py tests/test_imports_repository.py tests/test_imports_validation.py tests/test_imports_idempotency.py` - passed, 20 tests.
- `rg "catalog\\.|content\\.|orders\\.|users\\.|canonical" backend/app/domains/imports backend/tests/test_imports_idempotency.py` - only existing nullable `canonical_id` placeholder found.

## Self-Check: PASSED

- Same source ID and same content hash classifies as `unchanged`.
- Same source ID and different content hash classifies as `changed`.
- New source ID classifies as `new`.
- Rerun tests cover duplicate source IDs across batches.
- No canonical publish path exists.

## Next Phase Readiness

Plan 02-05 can expose batch summary and error-table APIs on top of the staged rows and structured errors.

---
*Phase: 02-livemaster-import-pipeline*
*Completed: 2026-05-11*
