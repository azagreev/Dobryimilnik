# Dobryimilnik

Dobryimilnik - это e-commerce платформа, которую мы строим для переноса долгоживущего магазина с Livemaster в собственный канал продаж. Первый этап ориентирован на backend: надежный импорт каталога, сохранение целостности данных и создание базы для заказов, клиентов, контента, доставки, фискализации и административных процессов.

## Стек

- Backend: FastAPI на Python 3.12
- База данных: PostgreSQL 16
- Frontend: Next.js 14
- Сопутствующие сервисы: Redis, Meilisearch, Keycloak
- Локальная оркестрация: Docker Compose

## Структура репозитория

- `backend/` - сервис FastAPI, миграции Alembic и backend-тесты
- `frontend/` - приложение Next.js
- `docs/` - документация по локальной разработке, CI, секретам и миграциям
- `compose.yml` - локальный стек разработки
- `Makefile` - основная поверхность команд для разработки

## Локальная разработка

Основная точка входа - `Makefile`.

```bash
make dev
```

Запускает локальный стек:

- `postgres`
- `redis`
- `meilisearch`
- `keycloak`
- `backend`
- `frontend`

Полезные команды:

- `make down` - остановить локальный стек
- `make logs` - смотреть логи сервисов
- `make ci` - запустить локальный quality gate

## Точки доступа

- Health backend: http://localhost:8000/api/v1/health
- Frontend: http://localhost:3000
- Keycloak: http://localhost:8080
- Meilisearch: http://localhost:7700

## Конфигурация

Локальные секреты создаются по запросу командой `make dev` и намеренно не коммитятся. Точные пути к файлам и схема подключения описаны в [docs/environment-and-secrets.md](docs/environment-and-secrets.md).

## Документация

- [Локальная разработка](docs/local-development.md)
- [Окружение и секреты](docs/environment-and-secrets.md)
- [Непрерывная интеграция](docs/ci.md)
- [Миграции базы данных](docs/database-migrations.md)

## Текущее состояние

Backend уже публикует версионированный API под `/api/v1`, а frontend пока содержит только начальный каркас публичной оболочки. Проект находится на стадии базовой платформы, поэтому документация выше сосредоточена на запуске и локальной проверке системы.
