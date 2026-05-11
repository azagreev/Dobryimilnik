# Local Development

Use the Makefile as the developer command surface.

## Commands

- `make dev` starts Docker Compose with `postgres`, `redis`, `meilisearch`, `keycloak`, `backend`, and `frontend`.
- `make down` stops the local stack.
- `make logs` follows service logs.
- `make ci` runs the local quality gate.

## URLs

- Backend: http://localhost:8000/api/v1/health
- Frontend: http://localhost:3000
- Keycloak: http://localhost:8080
- Meilisearch: http://localhost:7700

## Services

The local stack contains exactly these Phase 1 services: `postgres`, `redis`, `meilisearch`, `keycloak`, `backend`, and `frontend`.

Environment and secret-file rules are documented in [environment-and-secrets.md](environment-and-secrets.md).
