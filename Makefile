COMPOSE ?= docker compose -f compose.yml

.PHONY: dev down logs backend-lint backend-type backend-test frontend-lint frontend-type frontend-build ci prepare-local-secrets migrate-up migrate-down migrate-revision

dev: prepare-local-secrets
	$(COMPOSE) up --build

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

prepare-local-secrets:
	mkdir -p secrets/local
	test -f secrets/local/postgres_password.txt || printf '%s\n' local-postgres-password > secrets/local/postgres_password.txt
	test -f secrets/local/backend_secret_key.txt || printf '%s\n' local-backend-secret-key > secrets/local/backend_secret_key.txt

backend-lint:
	cd backend && uv run ruff check .

backend-type:
	cd backend && uv run mypy app tests

backend-test:
	cd backend && uv run pytest --cov=app --cov-report=term-missing

frontend-lint:
	cd frontend && npm run lint

frontend-type:
	cd frontend && npm run typecheck

frontend-build:
	cd frontend && npm run build

migrate-up:
	cd backend && uv run alembic upgrade head

migrate-down:
	cd backend && uv run alembic downgrade base

migrate-revision:
	cd backend && uv run alembic revision --autogenerate -m "$(message)"

ci: prepare-local-secrets backend-lint backend-type backend-test frontend-lint frontend-type frontend-build migrate-up migrate-down
	$(COMPOSE) config
