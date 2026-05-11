# Непрерывная интеграция

`make ci` - локальный эквивалент quality gate этапа 1.

## Контракт локальной команды

`make ci` выполняет эти команды по порядку:

1. `backend-lint` -> `cd backend && uv run ruff check .`
2. `backend-type` -> `cd backend && uv run mypy app tests`
3. `backend-test` -> `cd backend && uv run pytest --cov=app --cov-report=term-missing`
4. `frontend-lint` -> `cd frontend && npm run lint`
5. `frontend-type` -> `cd frontend && npm run typecheck`
6. `frontend-build` -> `cd frontend && npm run build`
7. `migrate-up` -> `cd backend && uv run alembic upgrade head`
8. `migrate-down` -> `cd backend && uv run alembic downgrade base`
9. `docker compose config`

## Job в GitHub Actions

Workflow GitHub Actions запускается на `push` и `pull_request`. Он поднимает сервис PostgreSQL 16, выполняет backend linting, backend type checks, backend tests with coverage, миграции upgrade и downgrade, проверки frontend lint/type/build, валидацию Compose config и `docker build -t dobryimilnik-backend:test backend`.

Сборка Docker-образа frontend отложена. На этапе 1 требуется только проверка сборки Docker-образа backend.

Backend tests включают проверку языка документации: тест сканирует `README.md`, `docs/*.md` и `doc/*.md` и падает, если опубликованный текст не является преимущественно русским.
