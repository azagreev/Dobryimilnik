---
phase: 01-foundation-and-domain-skeleton
plan: 04
subsystem: ci
tags: [github-actions, docker, pytest, mypy, ruff, nextjs]
requires:
  - phase: 01-01
    provides: Backend and frontend scaffold
  - phase: 01-02
    provides: Alembic migration commands
  - phase: 01-03
    provides: Settings and secrets contract
provides:
  - Local quality gate command surface
  - GitHub Actions CI workflow
  - Backend Docker image build check
  - Scaffold smoke tests with coverage gate
affects: [phase-01, ci, backend, frontend]
tech-stack:
  added: [GitHub Actions, Dockerfile]
  patterns:
    - CI invokes Makefile targets.
    - Backend image build is required; frontend image build is deferred.
key-files:
  created:
    - .github/workflows/ci.yml
    - backend/Dockerfile
    - docs/ci.md
    - backend/tests/test_core_scaffold.py
  modified:
    - Makefile
    - backend/pyproject.toml
    - frontend/package.json
key-decisions:
  - "Use Next.js 14.2.35 instead of 14.2.5 because npm reported a security warning for 14.2.5."
  - "Keep frontend Docker image build out of Phase 1 CI."
patterns-established:
  - "Local CI and GitHub Actions share Makefile command names."
requirements-completed: [FND-01, FND-02, FND-03, FND-04]
duration: 50 min
completed: 2026-05-11
---

# Phase 01 Plan 04: CI Quality Gates and Smoke Tests Summary

**GitHub Actions and local Makefile quality gates validate backend lint/type/tests, frontend lint/type/build, migrations, and backend image build**

## Performance

- **Duration:** 50 min
- **Started:** 2026-05-11T12:15:20Z
- **Completed:** 2026-05-11T13:05:31Z
- **Tasks:** 3
- **Files modified:** 11

## Accomplishments

- Added GitHub Actions workflow with PostgreSQL 16 service, backend checks, migration upgrade/downgrade, frontend checks, Compose config validation, and backend Docker build.
- Added backend Dockerfile using Python 3.12 and uvicorn for `app.main:app`.
- Added frontend lockfile/config needed for deterministic lint, typecheck, and build.
- Added core scaffold smoke coverage so `pytest --cov` passes the configured coverage gate.

## Task Commits

1. **Task 1: Normalize local quality commands** - `d37e552`
2. **Task 2: Add backend image build and GitHub Actions workflow** - `b390578`
3. **Task 3: Run final scaffold smoke verification** - `d6c8f6b`

## Files Created/Modified

- `.github/workflows/ci.yml` - Pull request and push CI workflow.
- `backend/Dockerfile` - Backend service image build.
- `docs/ci.md` - Local and GitHub CI command contract.
- `backend/tests/test_core_scaffold.py` - Core smoke coverage test.
- `frontend/package-lock.json` - Deterministic frontend dependency resolution.
- `frontend/.eslintrc.json` - Next.js lint configuration.
- `frontend/next-env.d.ts` - Next.js type environment declarations.

## Decisions Made

- Updated Next.js from `14.2.5` to `14.2.35` after npm reported a security warning for `14.2.5`.
- Did not add a frontend image build to CI; Phase 1 only requires backend Docker image validation.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Raised backend coverage above the configured gate**
- **Found during:** Task 3 (backend-test)
- **Issue:** Coverage was 67%, below the configured 70% threshold.
- **Fix:** Added `backend/tests/test_core_scaffold.py`.
- **Files modified:** `backend/tests/test_core_scaffold.py`
- **Verification:** `UV_CACHE_DIR=/tmp/uv-cache make backend-test`
- **Committed in:** `d6c8f6b`

**2. [Rule 2 - Missing Critical] Updated vulnerable Next.js patch version**
- **Found during:** Task 1 (npm install)
- **Issue:** npm reported a security warning for `next@14.2.5`.
- **Fix:** Updated `next` and `eslint-config-next` to `14.2.35`.
- **Files modified:** `frontend/package.json`, `frontend/package-lock.json`
- **Verification:** `make frontend-lint`, `make frontend-type`, `make frontend-build`
- **Committed in:** `d37e552`

---

**Total deviations:** 2 auto-fixed (coverage gate and dependency security).
**Impact on plan:** No scope expansion; both fixes strengthen the planned quality gate.

## Issues Encountered

- `make migrate-up` timed out locally because no PostgreSQL service is running in this WSL environment.
- `docker compose config` and `docker build -t dobryimilnik-backend:test backend` could not run because Docker is not available in this WSL distro.
- npm dependency installation required network access and took several minutes.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Phase 1 has the backend/frontend scaffold, migrations, settings, and CI contract needed for the Livemaster import pipeline planning and execution.

---
*Phase: 01-foundation-and-domain-skeleton*
*Completed: 2026-05-11*
