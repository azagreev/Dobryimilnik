---
phase: 01-foundation-and-domain-skeleton
status: warnings
depth: standard
files_reviewed: 67
findings:
  critical: 0
  warning: 1
  info: 0
  total: 1
reviewed_at: 2026-05-11
---

# Phase 01 Code Review

## Summary

Reviewed the Phase 1 scaffold, backend settings/migration code, frontend package configuration, Docker/Compose files, and CI workflow. Two secret-handling issues were fixed before this report was finalized:

- `cc2ca17` removed the committed PostgreSQL password from backend `DATABASE_URL` and derived it from `POSTGRES_PASSWORD_FILE`.
- `1fb613d` URL-encoded the injected password with `quote(..., safe="")`.

## Findings

### WR-01: Next.js 14 remains flagged by npm audit

**Severity:** Warning  
**File:** `frontend/package.json`  
**Evidence:** `npm audit --omit=dev` reports advisories against `next` and `postcss`; npm's available fix is `npm audit fix --force`, which would install `next@16.2.6`.

**Risk:** The project stack currently calls for Next.js 14, but the package audit database now flags the Next 14 line. Public storefront work is not implemented in Phase 1, so exposure is limited to the scaffold, but this should be resolved before public storefront deployment.

**Recommendation:** Decide in a later frontend/security planning step whether to upgrade the stack to a supported Next.js major or pin a patched Next.js 14 release if one becomes available. Do not apply `npm audit fix --force` blindly because it changes the major framework version.

## Checks Reviewed

- `UV_CACHE_DIR=/tmp/uv-cache make backend-lint` passed.
- `UV_CACHE_DIR=/tmp/uv-cache make backend-type` passed.
- `UV_CACHE_DIR=/tmp/uv-cache make backend-test` passed with 84% coverage.
- `make frontend-lint` passed.
- `make frontend-type` passed.
- `make frontend-build` passed.
- `make migrate-up` could not complete locally because PostgreSQL is not running in this WSL environment.
- `docker compose config` and `docker build -t dobryimilnik-backend:test backend` could not run because Docker is unavailable in this WSL distro.

## Verdict

Phase 1 source changes are acceptable for the backend-first scaffold. The remaining warning is a dependency lifecycle/security decision tied to the project-level Next.js version constraint.
