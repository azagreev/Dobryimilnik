# Phase 2: Livemaster Import Pipeline - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-11
**Phase:** 2-Livemaster Import Pipeline
**Areas discussed:** Source CSV contract, staging boundary, source identity and idempotency, validation behavior, import error table

---

## Source CSV Contract

| Option | Description | Selected |
|--------|-------------|----------|
| One CSV | Single CSV file as the initial import contract. | ✓ |
| Set of CSV files | Separate CSV files for products, variants, categories, media, posts, reviews, customers, and orders. | |
| CSV plus media folder | CSV data plus a local folder/archive for images. | |

**User's choice:** One CSV.
**Notes:** The user explicitly selected CSV and then chose the one-file contract.

---

## Staging Boundary

| Option | Description | Selected |
|--------|-------------|----------|
| Stage then publish | Validate in staging and publish valid records into basic canonical tables in this phase. | |
| Only staging | Load, validate, audit, and report imported data without publishing into canonical tables. | ✓ |
| Full canonical | Build all canonical models for every imported entity in this phase. | |

**User's choice:** Only staging.
**Notes:** The staging/canonical distinction was clarified: staging is for raw/validated import data and audit; canonical is the working store model. User chose to keep Phase 2 staging-only.

---

## Source Identity and Idempotency

| Option | Description | Selected |
|--------|-------------|----------|
| Source map | Shared `source_mappings` table for source system, entity type, source ID, batch, content hash, and future canonical link. | ✓ |
| Fields per table | Store Livemaster/source IDs directly on each staging/canonical table. | |
| Hash matching | Use content hashes as the primary identity strategy. | |

**User's choice:** Source map.
**Notes:** The user asked for options and selected the shared source mapping strategy. Hashes remain useful as change detection, not as the primary key.

---

## Validation Behavior

| Option | Description | Selected |
|--------|-------------|----------|
| Strict row validation | Critical row errors fail that row, but the batch continues. | ✓ |
| Fail fast | First critical error stops the whole import batch. | |
| Lenient import | Store as many rows as possible even with errors and report issues later. | |

**User's choice:** Strict row validation.
**Notes:** This keeps the owner from losing a whole batch because of one bad row while still preventing invalid rows from being treated as valid.

---

## Import Error Table

| Option | Description | Selected |
|--------|-------------|----------|
| Batch error table | Backend API returns row number, entity type, field, error code, message, and severity. | ✓ |
| CSV export only | Backend produces a downloadable CSV error report only. | |
| Summary plus details | Batch summary plus drill-down API for errors. | |

**User's choice:** Batch error table.
**Notes:** The user initially requested "таблица ошибок"; this was locked as a backend API contract for a detailed error table.

---

## the agent's Discretion

- Concrete SQLAlchemy model names, table names, enum names, API route names, and service/repository boundaries.
- Whether Celery/background jobs are introduced now or deferred, as long as the import remains idempotent and testable.
- Exact validation code taxonomy, provided row-level errors remain structured and owner-readable.

## Deferred Ideas

- Multi-file CSV import packages.
- CSV plus local media folder/archive import.
- Canonical publication into catalog/content/users/orders tables.
- Full admin UI for import issue review.
