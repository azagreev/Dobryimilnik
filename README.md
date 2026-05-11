# Dobryimilnik

Dobryimilnik is an e-commerce platform being built to migrate a long-running Livemaster shop into an owned sales channel. The first milestone is backend-first: import the catalog reliably, preserve data integrity, and establish the foundation for orders, customers, content, delivery, fiscalization, and admin workflows.

## Stack

- Backend: FastAPI on Python 3.12
- Database: PostgreSQL 16
- Frontend: Next.js 14
- Supporting services: Redis, Meilisearch, Keycloak
- Local orchestration: Docker Compose

## Repository Layout

- `backend/` - FastAPI service, Alembic migrations, and backend tests
- `frontend/` - Next.js application
- `docs/` - project documentation for local development, CI, secrets, and migrations
- `compose.yml` - local development stack
- `Makefile` - developer command surface

## Local Development

The Makefile is the main entry point.

```bash
make dev
```

Starts the local stack with:

- `postgres`
- `redis`
- `meilisearch`
- `keycloak`
- `backend`
- `frontend`

Useful commands:

- `make down` - stop the local stack
- `make logs` - follow service logs
- `make ci` - run the local quality gate

## Endpoints

- Backend health: http://localhost:8000/api/v1/health
- Frontend: http://localhost:3000
- Keycloak: http://localhost:8080
- Meilisearch: http://localhost:7700

## Configuration

Local secrets are created on demand by `make dev` and are intentionally not committed. See [docs/environment-and-secrets.md](docs/environment-and-secrets.md) for the exact file locations and runtime wiring.

## Documentation

- [Local development](docs/local-development.md)
- [Environment and secrets](docs/environment-and-secrets.md)
- [Continuous integration](docs/ci.md)
- [Database migrations](docs/database-migrations.md)

## Current State

The backend exposes a versioned API under `/api/v1`, and the frontend currently contains the initial scaffold for the public app shell. The project is still in foundation work, so the documentation above focuses on how to run and verify the platform locally.
