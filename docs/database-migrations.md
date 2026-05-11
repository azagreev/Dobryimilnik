# Database Migrations

Alembic migrations live under `backend/alembic/` and run from the backend directory through Makefile targets.

## Commands

- `make migrate-up` applies all migrations with `alembic upgrade head`.
- `make migrate-down` rolls migrations back to base with `alembic downgrade base`.
- `make migrate-revision message="describe change"` creates an autogenerate revision.

## Domain Sections

Phase 1 creates PostgreSQL schemas for these domain streams:

- `catalog`
- `orders`
- `users`
- `content`
- `public` for analytics, audit, and shared PostgreSQL objects

No import `staging` schema is created in Phase 1, and migrations do not insert business seed data.
