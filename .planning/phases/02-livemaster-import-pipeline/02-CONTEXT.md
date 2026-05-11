# Phase 2: Livemaster Import Pipeline - Context

**Gathered:** 2026-05-11
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase creates the Livemaster import staging, validation, idempotency, and audit foundation. It accepts owner-provided CSV import data, stores source identity and batch metadata, validates rows without stopping the whole batch, and exposes a backend error table for review. This phase does not publish imported records into canonical catalog, content, users, or orders tables; canonical publication and operational admin editing remain for later phases.

</domain>

<decisions>
## Implementation Decisions

### Source CSV Contract
- **D-01:** The phase should support a single CSV file as the initial import contract.
- **D-02:** The CSV contract should be explicit and versioned enough that later plans can validate required columns, entity type, and row-level source identity before writing staging records.
- **D-03:** Multi-file import packages and media-folder archive workflows are deferred. The single CSV path is the owner-facing minimum for the first import pipeline.

### Staging Boundary
- **D-04:** Phase 2 is staging-only: load, validate, audit, and report imported records, but do not publish into canonical domain tables.
- **D-05:** Staging tables should still be shaped for future canonical publication by preserving entity type, normalized fields, validation status, and source identifiers.
- **D-06:** Canonical product, variant, category, media, post, review, customer, and order models belong to future phases unless the planner needs tiny placeholder structures solely to keep staging foreign keys or tests coherent.

### Source Identity and Idempotency
- **D-07:** Use a shared `source_mappings` model/table for import identity instead of scattering Livemaster IDs across every future canonical table.
- **D-08:** `source_mappings` should track at minimum `source_system`, `entity_type`, `source_id`, `batch_id`, `content_hash`, and a future nullable `canonical_id` or equivalent link.
- **D-09:** Idempotency should primarily use stable source IDs plus content hashes. Hash matching alone is not acceptable as the main identity strategy.
- **D-10:** Re-running the same CSV should not duplicate staging identities for the same source entity. The pipeline should record whether rows are new, unchanged, changed, skipped, failed, or require review.

### Validation and Error Handling
- **D-11:** Use strict row validation: a critical error fails the affected row, but the batch continues processing.
- **D-12:** Batch-level failure should be reserved for unreadable files, invalid CSV structure, missing required global headers, or infrastructure/runtime failures that prevent safe processing.
- **D-13:** Row-level validation should produce structured errors with field, code, message, severity, row number, and entity context.

### Owner-Facing Import Report
- **D-14:** The owner-facing review surface for Phase 2 is a backend API that returns a batch error table.
- **D-15:** The error table must include CSV row number, entity type, field, machine-readable error code, human-readable message, and severity.
- **D-16:** A high-level batch summary is useful for API responses and tests, but the locked requirement is the detailed error table rather than a download-only CSV report.

### the agent's Discretion
The planner may choose concrete SQLAlchemy model names, table names, enum names, API route names, and internal service boundaries if they follow the Phase 1 `API -> service -> repository` pattern and keep Phase 2 staging-only. The planner may also decide whether Celery is introduced now or deferred, as long as the resulting plan keeps imports idempotent, testable, and practical for local development.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project scope and phase contract
- `.planning/PROJECT.md` — project vision, backend-first v1, migration constraints, and out-of-scope boundaries.
- `.planning/REQUIREMENTS.md` — import requirements `IMP-01` through `IMP-05` and full requirement traceability.
- `.planning/ROADMAP.md` — Phase 2 goal, dependencies, success criteria, and planned plan split.
- `.planning/STATE.md` — current project state and Phase 2 planning position.

### Prior phase decisions
- `.planning/phases/01-foundation-and-domain-skeleton/01-CONTEXT.md` — locked foundation decisions: domain schemas, API versioning, `API -> service -> repository`, and staging/import deferred to Phase 2.
- `.planning/phases/01-foundation-and-domain-skeleton/01-VERIFICATION.md` — Phase 1 verification result and current foundation status.

### Source PRD and research
- `doc/PRD.md` — original Russian PRD defining Livemaster migration scope, catalog size, content/review migration, SEO concerns, and target platform context.
- `.planning/research/STACK.md` — selected stack and import/job notes.
- `.planning/research/ARCHITECTURE.md` — modular monolith boundaries, staging-to-canonical import flow, and analytics/audit role.
- `.planning/research/FEATURES.md` — import features and owner-facing audit/report expectations.
- `.planning/research/PITFALLS.md` — import source identity, SEO continuity, and admin workflow risks.
- `.planning/research/SUMMARY.md` — initialization research summary and risk framing.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/app/core/db.py` — SQLAlchemy `Base`, naming convention, async engine, and session dependency to use for staging models and repositories.
- `backend/alembic/env.py` — Alembic is configured with `include_schemas=True` and `version_table_schema="public"`.
- `backend/app/api/v1/router.py` — central API v1 router where import/admin routes can be included.
- `backend/app/domains/*/{api,service,repository,models}.py` — existing domain package skeleton establishes the Phase 1 layering pattern.
- `backend/tests/test_migrations.py` — existing migration tests are simple source checks and should be extended or complemented for Phase 2 migration behavior.

### Established Patterns
- Backend code is a FastAPI modular monolith with domain packages under `backend/app/domains`.
- Domain implementation should follow `API -> service -> repository`.
- Public route versioning uses `/api/v1`.
- The baseline migration intentionally excludes `staging`; Phase 2 owns staging/import schema creation.
- CI and local quality gates already expect lint, type checks, tests, and migration checks.

### Integration Points
- New import code should connect through the backend API router, likely under an import/admin-facing route namespace.
- New staging migrations should build on the existing Alembic setup rather than introducing a separate migration tool.
- Tests should fit the existing `backend/tests` pytest structure and maintain strict typing/lint compatibility.

</code_context>

<specifics>
## Specific Ideas

- Start with one CSV file because that is the chosen owner-facing import contract for Phase 2.
- Treat the detailed batch error table as the practical owner workflow: the owner needs to see what failed and what must be fixed before later publication.
- Keep the Phase 2 data model future-proof for catalog/content/users/orders publication without implementing the publication step now.

</specifics>

<deferred>
## Deferred Ideas

- Multi-file CSV packages are deferred until the single CSV path is working or real source exports require a richer package.
- CSV plus local media-folder/archive import is deferred; media may be represented as source references/paths in staging for now.
- Canonical publication into catalog, content, users, and orders tables is deferred to later phases.
- Full admin UI for import issue review is deferred; Phase 2 locks the backend error-table contract.

</deferred>

---

*Phase: 2-Livemaster Import Pipeline*
*Context gathered: 2026-05-11*
