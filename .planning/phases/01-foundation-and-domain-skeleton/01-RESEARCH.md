# Phase 1: Foundation and Domain Skeleton - Research

**Researched:** 2026-05-11
**Status:** Ready for planning
**Phase:** 01 - Foundation and Domain Skeleton

## Research Goal

Answer: what must be known to plan Phase 1 well enough that execution can create a reliable FastAPI/PostgreSQL/Next.js foundation without leaking later-phase scope into the scaffold.

## Source Inputs

- `.planning/phases/01-foundation-and-domain-skeleton/01-CONTEXT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `.planning/PROJECT.md`
- `doc/PRD.md`
- Official documentation references queried through Context7:
  - FastAPI docs: settings, lifespan, APIRouter, bigger applications, testing dependency overrides.
  - Next.js 14 docs/examples: local dev, Docker Compose, Docker build.
  - Alembic docs: migration script structure, upgrade, downgrade, schema/data migration separation.

## Phase Boundary Findings

Phase 1 should create an executable platform skeleton, not business functionality. It must prove that a developer can start the full local service set, run migrations for the required PostgreSQL schemas, run quality checks in CI, and keep configuration/secrets out of committed code.

In scope:
- Repository scaffold for backend, frontend, infrastructure, docs, and CI.
- `make dev` as the main entry point over Docker Compose.
- Docker Compose services for PostgreSQL 16, Redis, Meilisearch, Keycloak, backend, and frontend.
- FastAPI app shell with `/api/v1` routing boundary and health endpoint.
- Domain package skeletons for `catalog`, `orders`, `users`, `content`, and `analytics`.
- Shared backend `core` package for config, DB session, logging, errors, security placeholder, pagination, and base schemas.
- Alembic migration setup that creates schemas `catalog`, `orders`, `users`, `content`, and uses `public` for analytics/audit.
- Minimal frontend Next.js 14 service scaffold sufficient for local service orchestration.
- CI checks for backend lint/type/test, migration upgrade+downgrade, backend Docker image build, and frontend lint/type/build if scaffolded.
- Documentation for environment file handling and secrets pattern.

Out of scope:
- Livemaster import staging schema/tables.
- Business seed/demo data.
- Catalog, cart, checkout, payment, fiscalization, storefront, or admin feature implementation.
- Yandex Lockbox integration.
- Frontend production Docker image check.
- `staging` environment config.

## Technical Approach

### Repository Layout

Use a simple monorepo with explicit service boundaries:

- `backend/` - FastAPI app, Python tooling, tests, Alembic.
- `frontend/` - Next.js 14 app scaffold.
- `infra/docker/` or root Compose files - local service orchestration.
- `docs/` - local development and environment/secrets documentation.
- `.github/workflows/ci.yml` - first quality gate.
- `Makefile` - stable developer command surface.

The planner should keep paths concrete so executors can create the scaffold without inventing structure during implementation.

### Backend Scaffold

FastAPI official guidance supports modular applications through `APIRouter` and `app.include_router(...)` with prefixes. The backend should expose a central `create_app()` or `app` entrypoint that includes an API v1 router under `/api/v1`.

Recommended app shape:

- `backend/app/main.py`
- `backend/app/api/v1/router.py`
- `backend/app/core/config.py`
- `backend/app/core/db.py`
- `backend/app/core/logging.py`
- `backend/app/core/errors.py`
- `backend/app/core/security.py`
- `backend/app/core/pagination.py`
- `backend/app/core/schemas.py`
- `backend/app/domains/catalog/`
- `backend/app/domains/orders/`
- `backend/app/domains/users/`
- `backend/app/domains/content/`
- `backend/app/domains/analytics/`

Each domain should start with empty but importable `api.py`, `service.py`, `repository.py`, and `models.py` modules or equivalent package skeleton. Do not add real business endpoints beyond health/root readiness probes in this phase.

FastAPI lifecycle work should use the `lifespan` pattern rather than deprecated startup/shutdown handlers. Configuration should use `pydantic-settings` `BaseSettings` and expose a dependency override pattern for tests.

### Local Services

`make dev` should invoke Docker Compose and bring up:

- `postgres`
- `redis`
- `meilisearch`
- `keycloak`
- `backend`
- `frontend`

Compose should model secrets through file-mounted secrets or local-only secret files ignored by git, not committed plaintext credentials. For local development, checked-in files may include non-secret defaults and documentation, but not `.env.example` because `D-17` explicitly forbids it in Phase 1.

Recommended command surface:

- `make dev`
- `make down`
- `make logs`
- `make backend-lint`
- `make backend-type`
- `make backend-test`
- `make migrate-up`
- `make migrate-down`
- `make ci`

### Database and Migrations

Use Alembic in `backend/` with a migration environment that can create and downgrade baseline schemas:

- `catalog`
- `orders`
- `users`
- `content`
- `public` retained for analytics/audit

The first migration should create schemas and minimal baseline tables only when needed for proving the scaffold. If no business tables are needed yet, schema creation plus `public.audit_log` or a narrowly scoped `public.schema_migrations_probe` table can prove migration mechanics. Avoid catalog/products and order tables until their later phases unless required by tests.

CI must run both:

- `alembic upgrade head`
- `alembic downgrade base` or at least `alembic downgrade -1` against a disposable PostgreSQL service

This directly satisfies `D-15` and prevents one-way migrations from entering the scaffold.

### Frontend Scaffold

Next.js 14 should be scaffolded as a service that can run in local development on port `3000`. It only needs an app shell and a simple health/status surface in Phase 1. SEO-sensitive pages are out of scope until later.

The Docker/Compose setup should mount source for local development and run `npm run dev` or an equivalent package-manager command. If the project chooses npm for simplicity, keep that consistent in Makefile and CI.

### CI Quality Gates

Minimal CI should be useful immediately but not overfit the empty scaffold:

- Backend lint with `ruff`.
- Backend type check with `mypy` or `pyright`; choose one and configure it.
- Backend tests with `pytest`.
- Migration upgrade+downgrade against PostgreSQL service.
- Backend Docker image build.
- Frontend lint/type/build if the frontend scaffold is created in the same phase.

Coverage should be configured once backend tests exist, but it should not block an empty scaffold before meaningful tests are present. A practical Phase 1 plan can add `pytest --cov` with an initial low threshold or defer the hard threshold to the first plan that creates testable backend code, matching `D-14`.

## Architecture Decisions for Planning

- The first backend route should be health-oriented, not business-oriented.
- Keep `/api/v1` present from the first app assembly.
- Keep domain package names aligned with PRD schemas: `catalog`, `orders`, `users`, `content`, `analytics`.
- Use `orders` as the database schema for commerce/order data because this is already locked in PRD and context.
- Use `public` for analytics/audit because PostgreSQL already has the public schema and the context explicitly maps analytics there.
- Defer Celery worker implementation unless Compose needs a placeholder; Redis can exist as a service without queue code in Phase 1.
- Keycloak should be a running local service, but app auth integration can be a placeholder until the users/RBAC phase.

## Risks and Mitigations

| Risk | Why It Matters | Mitigation in Plan |
|------|----------------|--------------------|
| Scaffold becomes fake and cannot run end-to-end | Phase success requires local services to start | Include `make dev` plus smoke checks for backend and frontend containers |
| Migrations only work upward | CI success can hide downgrade failures | Include explicit upgrade+downgrade task and CI job |
| Secrets accidentally committed | FND-04 is a foundation requirement | Add `.gitignore`, docs, Compose secrets pattern, and checks for forbidden env files |
| Domain boundaries drift early | Later phases depend on stable module/schema names | Create domain package skeletons and migration folders in Phase 1 |
| CI blocks on unrealistic coverage | Empty scaffold cannot satisfy high coverage honestly | Add tests for actual scaffold behavior and make coverage gate conditional or initially calibrated |
| Frontend work expands into storefront | Storefront is Phase 9 | Limit frontend to service scaffold, status page, lint/type/build |

## Suggested Plan Split

Use the roadmap's four planned slices:

1. `01-01`: Repository structure, service scaffold, and local development workflow.
2. `01-02`: PostgreSQL schemas, migration tooling, and baseline models.
3. `01-03`: Configuration, secrets, and environment management.
4. `01-04`: CI quality gates and smoke tests.

Dependency order:

- `01-01` first because it creates paths, service commands, and app shells.
- `01-02` after `01-01` because migrations depend on backend tooling and database service.
- `01-03` can run after `01-01`; it must coordinate with Compose and backend settings.
- `01-04` after `01-01`, `01-02`, and `01-03` because CI needs final command names and migration/config behavior.

## Validation Architecture

Phase 1 needs validation that samples the actual scaffold and command surface, not just file existence.

Recommended automated checks:

- `make backend-lint`
- `make backend-type`
- `make backend-test`
- `make migrate-up`
- `make migrate-down`
- `make ci`
- `docker compose config`
- `docker compose build backend`
- `npm run lint`, `npm run typecheck`, and `npm run build` from `frontend/` if frontend scaffold exists.

Recommended test files:

- `backend/tests/test_health.py` verifies the backend app exposes a health endpoint and can be imported.
- `backend/tests/test_settings.py` verifies settings load from environment and do not require committed secrets.
- `backend/tests/test_domain_packages.py` verifies domain packages are importable.
- Migration CI verifies schemas exist after upgrade and are removed or reverted after downgrade.

Manual verification:

- Developer can run `make dev`.
- Backend responds on its documented port.
- Frontend responds on its documented port.
- Keycloak, Redis, Meilisearch, and PostgreSQL containers are present and healthy or documented as starting.

Nyquist sampling rule:

- Every plan must include at least one automated command.
- No three consecutive implementation tasks should rely only on manual verification.
- Final phase verification must run `make ci` plus local Compose config validation.

## Planner Constraints

- Every plan must include a `<threat_model>` block because security enforcement is enabled by default.
- Every plan must include concrete `<read_first>` entries.
- Every task must include checkable `<acceptance_criteria>`.
- Every Phase 1 requirement ID must appear in at least one plan frontmatter `requirements` field:
  - `FND-01`
  - `FND-02`
  - `FND-03`
  - `FND-04`

## Open Questions for Execution

These can be resolved by the executor without another planning discussion:

- Use `uv` or another Python dependency manager. Context allows planner discretion; `uv` is a good default because Makefile can wrap it cleanly.
- Use npm or pnpm. Context allows planner discretion; npm is the lowest-friction default for a new Next.js scaffold.
- Whether to create a tiny `public.audit_log` baseline table in Phase 1. Prefer schema-only plus a migration smoke query unless tests need a table.

## RESEARCH COMPLETE
