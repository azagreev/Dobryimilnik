# Phase 01 - Pattern Map

**Created:** 2026-05-11
**Scope:** Foundation and Domain Skeleton

## Codebase State

No application code exists yet. The repository currently contains planning artifacts, GSD tooling, `AGENTS.md`, and `doc/PRD.md`.

Because this is a greenfield scaffold phase, there are no local implementation analogs to copy. Executors should follow the concrete structure in `01-CONTEXT.md`, `01-RESEARCH.md`, and the plan files instead of inferring patterns from unrelated GSD internals.

## Planned File Families

| File family | Role | Closest existing analog | Planning guidance |
|-------------|------|-------------------------|-------------------|
| `Makefile` | Developer command entry point | None | Define stable wrappers for Docker, backend, frontend, migrations, and CI commands. |
| `compose.yml` / `docker-compose.yml` | Local service orchestration | None | Include PostgreSQL, Redis, Meilisearch, Keycloak, backend, and frontend services. |
| `backend/app/main.py` | FastAPI app entrypoint | None | Assemble app with lifespan and include API v1 router. |
| `backend/app/api/v1/router.py` | API version boundary | None | Include only scaffold/health routes in Phase 1. |
| `backend/app/core/*.py` | Shared backend primitives | None | Create config, DB, logging, errors, security placeholder, pagination, and base schemas. |
| `backend/app/domains/*` | Domain module skeletons | None | Use `catalog`, `orders`, `users`, `content`, and `analytics`; preserve API -> service -> repository layering. |
| `backend/alembic/*` | Migration environment | None | Support PostgreSQL schema creation and upgrade/downgrade checks. |
| `backend/tests/*` | Scaffold validation | None | Verify importability, settings behavior, health endpoint, and migration mechanics. |
| `frontend/*` | Next.js 14 service scaffold | None | Keep to minimal app shell/status surface; storefront features are out of scope. |
| `.github/workflows/ci.yml` | Quality gate | None | Run lint, type, tests, migration upgrade/downgrade, and backend image build. |
| `docs/*` | Developer operations documentation | None | Document local startup and env/secrets rules without adding `.env.example`. |

## Data Flow Anchors

1. `make dev` calls Docker Compose.
2. Docker Compose starts infrastructure and app services.
3. Backend settings load environment and secret file paths.
4. Backend creates DB sessions using PostgreSQL URL from local runtime config.
5. Alembic applies schema migrations to PostgreSQL.
6. CI reuses Makefile commands to avoid drift between local and automated checks.

## Risk-Sensitive Patterns to Enforce

- Keep all service names stable: `postgres`, `redis`, `meilisearch`, `keycloak`, `backend`, `frontend`.
- Keep API prefix stable: `/api/v1`.
- Keep database schema names stable: `catalog`, `orders`, `users`, `content`, `public`.
- Do not add `.env.example` in Phase 1.
- Do not commit secret values or local secret files.
- Do not add business seed/demo data.
- Do not implement Livemaster import, catalog CRUD, checkout, payment, fiscalization, or storefront pages in Phase 1.

## PATTERN MAPPING COMPLETE
