# Continuous Integration

`make ci` is the local equivalent of the Phase 1 CI quality gate.

## Local Command Contract

`make ci` runs these commands in order:

1. `backend-lint` -> `cd backend && uv run ruff check .`
2. `backend-type` -> `cd backend && uv run mypy app tests`
3. `backend-test` -> `cd backend && uv run pytest --cov=app --cov-report=term-missing`
4. `frontend-lint` -> `cd frontend && npm run lint`
5. `frontend-type` -> `cd frontend && npm run typecheck`
6. `frontend-build` -> `cd frontend && npm run build`
7. `migrate-up` -> `cd backend && uv run alembic upgrade head`
8. `migrate-down` -> `cd backend && uv run alembic downgrade base`
9. `docker compose config`

## GitHub Actions Job

The GitHub Actions workflow runs on pushes and pull requests. It starts a PostgreSQL 16 service, runs backend linting, backend type checks, backend tests with coverage, migration upgrade and downgrade, frontend lint/type/build checks, Compose config validation, and `docker build -t dobryimilnik-backend:test backend`.

Frontend Docker image build is deferred. Phase 1 only requires the backend Docker image build check.
