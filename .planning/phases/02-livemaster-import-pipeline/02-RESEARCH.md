# Phase 2: Livemaster Import Pipeline - Research

**Phase:** 02 — Livemaster Import Pipeline  
**Date:** 2026-05-11  
**Status:** Complete  

## Research Question

What needs to be known to plan Phase 2 well: a staging-only, single-CSV Livemaster import pipeline with source identity, row validation, idempotency, and backend error-table reporting?

## Executive Summary

Phase 2 should build a backend-only import foundation inside the existing FastAPI/PostgreSQL modular monolith. The safest plan is to create a dedicated `staging` schema plus an import domain package, persist each import as a batch with row-level staging records, validate rows independently, and expose API endpoints for upload/start, batch status, summary, and error-table review.

The phase should not publish into canonical `catalog`, `content`, `users`, or `orders` tables. Instead, it should preserve enough normalized staging data, source identity, and hashes to support canonical publication in later phases. Idempotency should be enforced by database constraints and repository logic around `source_mappings`, not by service-layer checks alone.

## Key Constraints From Context

- Input contract is one CSV file, not a multi-file package.
- Phase 2 is staging-only: no canonical publish.
- A shared `source_mappings` table is the locked source identity strategy.
- Row validation is strict per row: invalid rows fail, but the batch continues.
- Owner-facing review is a backend API that returns a detailed batch error table.
- Existing backend pattern is `API -> service -> repository` under `backend/app/domains`.
- Existing Alembic setup supports schema-qualified migrations through `include_schemas=True`.

## Relevant Existing Code

| Area | Current State | Planning Implication |
|------|---------------|----------------------|
| `backend/app/core/db.py` | SQLAlchemy `Base`, naming convention, async engine, session dependency | Reuse for staging models and repositories. |
| `backend/alembic/env.py` | Async Alembic, `include_schemas=True`, version table in `public` | Add a Phase 2 migration creating `staging` schema and tables. |
| `backend/app/api/v1/router.py` | Central API router only includes health | Add import/admin router here. |
| Domain packages | Empty `api/service/repository/models` skeletons | Add an `importing` or `imports` domain package following same pattern. |
| Tests | Pytest, migration source tests, health/settings/domain scaffold checks | Add focused unit/integration tests for CSV parsing, validation, idempotency, and API contracts. |

## Library and Framework Findings

### FastAPI File Uploads

FastAPI supports `UploadFile` for file uploads; it uses spooled storage and is better for larger files than reading a raw bytes parameter. For Phase 2, `UploadFile` is appropriate for a CSV upload endpoint. `BackgroundTasks` exists and integrates with dependency injection, but it runs after response handling in the web process; it is acceptable for a small first pipeline, while Celery remains better for production-grade long-running imports.

Planning implication: use a synchronous-in-request service path for deterministic tests or a simple background task only if the plan also includes status polling and clear error persistence. Avoid making Celery mandatory unless the phase explicitly adds worker wiring and tests.

### SQLAlchemy 2.0 and PostgreSQL Upsert

SQLAlchemy 2.0 supports PostgreSQL `INSERT ... ON CONFLICT DO UPDATE` through dialect insert constructs, including `excluded` values and `RETURNING`. This fits the `source_mappings` idempotency requirement. Schema-qualified SQLAlchemy models can be represented with table args and are compatible with the existing Alembic `include_schemas=True` setup.

Planning implication: source mapping writes should use database uniqueness constraints and PostgreSQL upserts, preferably returning the mapping row so service logic can classify new/unchanged/changed/skipped records consistently.

## Recommended Domain Shape

### Backend Package

Create a dedicated import domain package, for example:

- `backend/app/domains/imports/api.py`
- `backend/app/domains/imports/models.py`
- `backend/app/domains/imports/schemas.py`
- `backend/app/domains/imports/service.py`
- `backend/app/domains/imports/repository.py`
- optional `backend/app/domains/imports/csv_contract.py`
- optional `backend/app/domains/imports/validation.py`

Use `imports` rather than overloading `catalog` because Phase 2 includes products, variants, categories, media, blog posts, reviews, customers, and orders. The domain is a workflow/integration boundary, not only catalog.

### Database Schema

Create a `staging` PostgreSQL schema. Minimal tables to plan:

- `staging.import_batches`
- `staging.import_rows`
- `staging.source_mappings`
- `staging.import_errors`

Optional split tables can be deferred until real CSV shape demands them. For a one-CSV contract, `import_rows` can store normalized row data as JSONB with typed metadata columns (`entity_type`, `source_id`, `row_number`, `content_hash`, `status`) while later phases introduce entity-specific staging tables if needed.

### Core Enums

Useful enums:

- `ImportBatchStatus`: `pending`, `running`, `completed`, `completed_with_errors`, `failed`
- `ImportRowStatus`: `new`, `unchanged`, `changed`, `skipped`, `failed`, `requires_review`
- `ImportSeverity`: `info`, `warning`, `error`
- `ImportEntityType`: `product`, `variant`, `category`, `media`, `post`, `review`, `customer`, `order`

## CSV Contract Guidance

The one-CSV contract still needs structure:

- Required global columns: `entity_type`, `source_id`.
- Strongly recommended columns: `parent_source_id`, `sku`, `slug`, `name`, `price`, `stock`, `category_path`, `media_url`, `seo_title`, `seo_description`.
- The service should reject a file missing required headers at batch level.
- Row-level validation should depend on `entity_type`; for example, products require name/source identity, variants require parent/product identity, media requires a source reference/path/url.
- Preserve the raw row payload for audit and future reprocessing.

Planning implication: Plan 02-01 should define a contract object and tests before table-heavy implementation proceeds.

## Idempotency Architecture

Recommended constraints:

- `source_mappings`: unique on `(source_system, entity_type, source_id)`.
- `import_rows`: unique on `(batch_id, row_number)` and possibly `(batch_id, entity_type, source_id)`.
- `import_errors`: index on `(batch_id, row_id, severity)` for table filtering.

Recommended classification:

- `new`: source mapping did not exist before this batch.
- `unchanged`: source mapping exists and content hash matches.
- `changed`: source mapping exists and content hash differs.
- `failed`: row has critical validation errors.
- `requires_review`: row is structurally valid but has ambiguity the owner must inspect.
- `skipped`: duplicate or unsupported row that is intentionally not processed.

## API Contract Guidance

Minimum endpoints:

- `POST /api/v1/imports/batches` or `/api/v1/admin/imports/batches` — create/run import from CSV upload.
- `GET /api/v1/imports/batches/{batch_id}` — batch status and summary.
- `GET /api/v1/imports/batches/{batch_id}/errors` — detailed error table with pagination.

The exact admin prefix can be decided by the planner. Since RBAC is later, Phase 2 may expose backend endpoints without final auth but should name them so they can be protected later.

## Validation Architecture

Validation should be layered so tests can target each layer independently:

1. CSV contract validation: file readable, required headers present, supported encoding, row numbers preserved.
2. Row parsing: each row becomes a typed internal object or structured parse error.
3. Entity-specific validation: required fields by `entity_type`, numeric fields, source ID format, parent/source references when present.
4. Idempotency classification: repository checks/upserts `source_mappings` and compares content hashes.
5. Error-table projection: API returns stable fields: row number, entity type, field, error code, message, severity.

Automated validation should cover:

- Missing required headers fail the batch.
- Invalid row fails only that row and creates an `import_errors` record.
- Duplicate source IDs in a rerun do not create duplicate source mappings.
- Changed content hash is classified as changed rather than duplicated.
- Error table API paginates and returns stable fields.

## Plan Split Recommendation

Keep the five roadmap plans but adjust the wording internally for the staging-only decision:

1. `02-01 Source file contracts and import batch model`
   - CSV contract, import domain package, batch API skeleton, batch model.
2. `02-02 Staging tables and source identity preservation`
   - `staging` schema, import rows, source mappings, constraints, repository.
3. `02-03 Validation and normalization pipeline`
   - CSV parser, row validation, normalized staging payload, structured errors.
4. `02-04 Idempotent staging reruns and classification`
   - Rerun behavior, content hashes, new/unchanged/changed/skipped classification.
   - Do not publish to canonical despite roadmap's older "publish" wording.
5. `02-05 Import audit report and failure review`
   - Batch summary API, error table API, pagination, owner-readable messages.

## Security and Data Risks

- CSV upload is an untrusted input path. Validate file type/size, avoid formula-injection output patterns in any future CSV export, and never execute content.
- Source rows may contain customer/order data. Avoid logging raw PII in application logs; keep raw payloads in database audit tables where access can later be restricted.
- Staging data may include SEO slugs and media URLs. Preserve but do not trust them until validation.
- Idempotency must be backed by unique constraints because service-level checks can race.

## Open Issues for Planner

- Decide whether to introduce Celery now or keep imports synchronous/background-light for Phase 2.
- Decide exact route prefix (`/api/v1/imports` vs `/api/v1/admin/imports`) while noting future RBAC.
- Decide whether `import_rows.normalized_payload` is enough for Phase 2 or whether entity-specific staging tables are required now.
- Decide test database strategy: source-level migration tests are already present, but real repository idempotency tests may need a PostgreSQL-backed test path.

## Research Complete

The phase is ready for planning. The main correction to preserve is that Plan 02-04 must become idempotent staging reruns/classification, not canonical publish, because `02-CONTEXT.md` locks Phase 2 as staging-only.
