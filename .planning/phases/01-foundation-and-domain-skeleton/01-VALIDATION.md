---
phase: 01
slug: foundation-and-domain-skeleton
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-05-11
---

# Phase 01 - Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest for backend; npm scripts for frontend |
| **Config file** | `backend/pyproject.toml`, `frontend/package.json`, `.github/workflows/ci.yml` |
| **Quick run command** | `make backend-test` |
| **Full suite command** | `make ci` |
| **Estimated runtime** | ~120 seconds locally after dependencies are installed |

## Sampling Rate

- **After every task commit:** Run the task's fastest relevant command: `make backend-test`, `make backend-lint`, `make backend-type`, `docker compose config`, or a frontend npm script.
- **After every plan wave:** Run `make ci`.
- **Before `$gsd-verify-work`:** Full suite must be green.
- **Max feedback latency:** 120 seconds for quick checks, excluding first dependency install.

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 01-01-01 | 01-01 | 1 | FND-01 | T-01-01 | Local services expose only documented local ports and do not require committed secrets | smoke | `docker compose config` | no | pending |
| 01-01-02 | 01-01 | 1 | FND-01 | T-01-02 | Backend scaffold imports without loading secret values from git | unit | `make backend-test` | no | pending |
| 01-02-01 | 01-02 | 2 | FND-02 | T-01-03 | Migrations create only approved schemas and are reversible | integration | `make migrate-up && make migrate-down` | no | pending |
| 01-03-01 | 01-03 | 2 | FND-04 | T-01-04 | Secret files are ignored and documented instead of committed | source | `git check-ignore .env .env.local secrets/local/postgres_password.txt` | no | pending |
| 01-04-01 | 01-04 | 3 | FND-03 | T-01-05 | CI runs lint, type, tests, migrations, and backend image build | CI | `make ci` | no | pending |

## Wave 0 Requirements

- [ ] `backend/tests/test_health.py` - backend import and health endpoint coverage.
- [ ] `backend/tests/test_settings.py` - settings load from environment without committed secrets.
- [ ] `backend/tests/test_domain_packages.py` - domain package import coverage.
- [ ] `backend/tests/test_migrations.py` or CI migration script - schema upgrade/downgrade proof.
- [ ] `backend/pyproject.toml` - pytest, ruff, mypy, and coverage configuration.

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| `make dev` starts all long-running local services | FND-01 | Requires developer Docker runtime and may keep foreground processes open | Run `make dev`, confirm PostgreSQL, Redis, Meilisearch, Keycloak, backend, and frontend containers start |
| Backend and frontend ports respond in local Compose | FND-01 | Requires live containers | Open documented backend health URL and frontend URL after `make dev` |

## Validation Sign-Off

- [x] All tasks have automated verify commands or Wave 0 dependencies.
- [x] Sampling continuity: no 3 consecutive tasks without automated verify.
- [x] Wave 0 covers all currently missing test infrastructure.
- [x] No watch-mode flags in automated verification commands.
- [x] Feedback latency target < 120s after dependencies are installed.
- [x] `nyquist_compliant: true` set in frontmatter.

**Approval:** pending
