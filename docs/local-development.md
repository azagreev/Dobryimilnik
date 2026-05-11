# Локальная разработка

Используйте `Makefile` как основную поверхность команд для разработки.

## Команды

- `make dev` запускает Docker Compose со службами `postgres`, `redis`, `meilisearch`, `keycloak`, `backend` и `frontend`.
- `make down` останавливает локальный стек.
- `make logs` показывает логи сервисов.
- `make import-catalog` загружает архив `doc/dobryimilnik_catalog.zip` в staging-слой базы данных.
- `make ci` запускает локальный quality gate.

## Адреса

- Backend: http://localhost:8000/api/v1/health
- Frontend: http://localhost:3000
- Keycloak: http://localhost:8080
- Meilisearch: http://localhost:7700

## Сервисы

Локальный стек содержит ровно эти сервисы этапа 1: `postgres`, `redis`, `meilisearch`, `keycloak`, `backend` и `frontend`.

Правила по окружению и секретным файлам описаны в [environment-and-secrets.md](environment-and-secrets.md). Репозиторий намеренно не содержит `.env.example`; локальные секретные файлы создаются разработчиком и игнорируются.
