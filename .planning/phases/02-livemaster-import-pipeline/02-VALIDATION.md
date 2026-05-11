---
phase: 02
slug: livemaster-import-pipeline
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-05-11
---

# Phase 02 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | `backend/pyproject.toml` |
| **Quick run command** | `cd backend && uv run pytest tests/test_imports*.py` |
| **Full suite command** | `cd backend && uv run pytest` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `cd backend && uv run pytest tests/test_imports*.py`
- **After every plan wave:** Run `cd backend && uv run pytest`
- **Before `$gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds for focused import tests

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 02-01-01 | 02-01 | 1 | IMP-01 | T-02-01 | Reject malformed CSV headers without unsafe processing | unit/API | `cd backend && uv run pytest tests/test_imports_contract.py` | ❌ W0 | ⬜ pending |
| 02-02-01 | 02-02 | 1 | IMP-01, IMP-04 | T-02-02 | Enforce source identity uniqueness in database | migration/repository | `cd backend && uv run pytest tests/test_imports_repository.py tests/test_migrations.py` | ❌ W0 | ⬜ pending |
| 02-03-01 | 02-03 | 2 | IMP-02 | T-02-03 | Invalid rows fail individually with structured errors | unit/service | `cd backend && uv run pytest tests/test_imports_validation.py` | ❌ W0 | ⬜ pending |
| 02-04-01 | 02-04 | 2 | IMP-04, IMP-05 | T-02-04 | Reruns classify rows without duplicate mappings | repository/service | `cd backend && uv run pytest tests/test_imports_idempotency.py` | ❌ W0 | ⬜ pending |
| 02-05-01 | 02-05 | 3 | IMP-03 | T-02-05 | Error table does not expose unsafe raw logs and remains paginated | API | `cd backend && uv run pytest tests/test_imports_api.py` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/test_imports_contract.py` — CSV contract and batch-level failure stubs.
- [ ] `backend/tests/test_imports_validation.py` — row-level validation and structured error stubs.
- [ ] `backend/tests/test_imports_repository.py` — source mapping uniqueness/upsert stubs.
- [ ] `backend/tests/test_imports_idempotency.py` — rerun classification stubs.
- [ ] `backend/tests/test_imports_api.py` — batch summary and error-table API stubs.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Owner readability of Russian/import error messages | IMP-03 | Automated tests can verify fields, but not whether messages are operationally useful for the owner | Review sample error responses during UAT before execution is accepted |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s for focused tests
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
