# Phase 1: Foundation and Domain Skeleton - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-11
**Phase:** 01-foundation-and-domain-skeleton
**Areas discussed:** Локальная разработка, структура backend, база данных и миграции, CI и проверки качества, конфиг и секреты

---

## Выбор зон обсуждения

| Option | Description | Selected |
|--------|-------------|----------|
| Локальная разработка | Docker Compose vs local-first setup; required services on day one. | |
| Структура backend | Domain boundaries, API versioning, service/repository layers. | |
| База данных | Schemas, migration streams, staging/import timing, seed expectations. | |
| CI и проверки качества | CI strictness, migration checks, coverage, Docker smoke/build checks. | |
| Конфиг и секреты | Env conventions, local/prod/staging, Lockbox timing, Docker secrets. | |
| Все зоны | Discuss every gray area above. | ✓ |

**User's choice:** Все зоны.
**Notes:** Пользователь попросил далее вести все вопросы, ответы и диалоги на русском.

---

## Локальная разработка

| Option | Description | Selected |
|--------|-------------|----------|
| Docker Compose для всего | backend, frontend, Postgres, Redis, Meilisearch, Keycloak поднимаются одной командой. | ✓ |
| Гибрид | Инфраструктура в Docker Compose, backend/frontend локально. | |
| Минимальный старт | Сначала только backend + Postgres. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Полный набор | Postgres, Redis, Meilisearch, Keycloak, backend, frontend. | ✓ |
| Backend core | Postgres, Redis, backend; остальное позже. | |
| Только база | Postgres + backend. | |

| Option | Description | Selected |
|--------|-------------|----------|
| make dev | Единая точка входа. | ✓ |
| docker compose up | Стандартный Docker workflow. | |
| README-команды | Отдельные команды без единой обёртки. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Обязательны | Минимальные категории/товары/пользователи для smoke tests. | |
| Только технические | Healthcheck/test fixtures без бизнес-демо данных. | |
| Позже | Seed данные оставить на фазу импорта/каталога. | ✓ |

**User's choice:** `1.1 2.1 3.1 4.3`
**Notes:** Зафиксирован полный Docker Compose stack и `make dev`; бизнес seed данные отложены.

---

## Структура backend

| Option | Description | Selected |
|--------|-------------|----------|
| Строго по доменам | `catalog`, `orders`, `users`, `content`, `analytics` как отдельные modules. | ✓ |
| Умеренно | Доменные папки есть, общие модели/сервисы можно использовать свободно. | |
| Минимально | Простой FastAPI skeleton, домены позже. | |

| Option | Description | Selected |
|--------|-------------|----------|
| API -> service -> repository | Предсказуемая структура, удобно тестировать. | ✓ |
| API -> service | Без repository слоя. | |
| Просто routes | Минимально. | |

| Option | Description | Selected |
|--------|-------------|----------|
| /api/v1/... сразу | Соответствует PRD и стабильно для frontend. | ✓ |
| Без версии | Версионирование позже. | |
| Внутренний prefix отдельно | `/internal/...` и `/api/v1/...`. | |

| Option | Description | Selected |
|--------|-------------|----------|
| core module | config, db session, logging, errors, security, pagination, base schemas. | ✓ |
| shared module | Всё общее, включая DTO/helpers/domain utilities. | |
| Минимум общего кода | Только config/db, остальное в доменах. | |

**User's choice:** `1.1 2.1 3.1 4.1`
**Notes:** Backend должен стартовать со строгих доменных границ и явной слойности.

---

## База данных и миграции

| Option | Description | Selected |
|--------|-------------|----------|
| 5 схем из PRD | `catalog`, `orders`, `users`, `content`, `public`. | ✓ |
| 4 доменные схемы + audit | Отдельная `audit`. | |
| Одна public схема сначала | Разнести позже. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Единый Alembic поток | Один migration history. | |
| По доменам | Отдельные migration folders/streams на каждый домен. | ✓ |
| SQL files вручную | Без Alembic на старте. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Да, сразу | Создать `staging` schema и import batch tables. | |
| Только schema placeholder | Пустая `staging`, таблицы позже. | |
| Нет | Полностью оставить staging/import на Фазу 2. | ✓ |

| Option | Description | Selected |
|--------|-------------|----------|
| Технические fixtures | Минимальные записи для tests/smoke. | |
| Небольшой демо-каталог | Несколько категорий/товаров. | |
| Без seed | Только миграции и healthchecks. | ✓ |

**User's choice:** `1.1 2.2 3.3 4.3`
**Notes:** Domain schemas нужны сразу, staging/import и seed данные отложены.

---

## CI и проверки качества

| Option | Description | Selected |
|--------|-------------|----------|
| Полный baseline | backend lint/type/test, frontend lint/type/build, migration checks, Docker smoke. | |
| Кодовые проверки | lint/type/test/build без Docker smoke и migration checks. | |
| Минимум | Только lint/type. | ✓ |

| Option | Description | Selected |
|--------|-------------|----------|
| Без gate в Фазе 1 | Coverage считать можно, но не блокировать. | |
| Мягкий gate | Блокировать только резкое падение. | |
| Жёсткий gate | Сразу минимальный порог покрытия. | ✓ |

| Option | Description | Selected |
|--------|-------------|----------|
| Upgrade check | Поднять тестовую БД и применить миграции. | |
| Upgrade + downgrade | Проверять применение и откат. | ✓ |
| Только syntax/import | Проверить Alembic config и migration files. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Да, backend и frontend | CI собирает оба образа. | |
| Только backend | Frontend image позже. | ✓ |
| Нет | Docker smoke только локально. | |

**User's choice:** `1.3 2.3 3.2 4.2`
**Notes:** Зафиксировано напряжение: минимальный CI и жёсткий coverage gate. Решение: coverage gate включается только после появления backend test scaffold, не блокируя пустой проект.

---

## Конфиг и секреты

| Option | Description | Selected |
|--------|-------------|----------|
| `.env.example + .env.local` | Пример коммитится, локальный файл игнорируется. | |
| `.env.example + env/*.example` | Отдельные примеры по сервисам/окружениям. | |
| Только документация | Без env template файлов в Фазе 1. | ✓ |

| Option | Description | Selected |
|--------|-------------|----------|
| local/staging/prod сразу | Config явно знает эти окружения. | |
| local/prod | staging добавить позже. | ✓ |
| Только local | Остальные окружения в фазе релиза. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Adapter boundary now | Интерфейс/настройки под Lockbox сразу. | |
| Document only | Описать, но не кодить границу. | |
| Ignore now | Вернуться к Lockbox ближе к production. | ✓ |

| Option | Description | Selected |
|--------|-------------|----------|
| Local env only | Compose читает локальные `.env.local`. | |
| Docker secrets pattern | Сразу моделировать prod-like secrets. | ✓ |
| Hardcoded dev defaults | Безопасные dev-only значения в compose. | |

**User's choice:** `1.3 2.2 3.3 4.2`
**Notes:** Env template files не создавать; секреты моделировать через Docker secrets pattern.

---

## Финальное подтверждение

| Option | Description | Selected |
|--------|-------------|----------|
| Готово | Записать CONTEXT.md и DISCUSSION-LOG.md для Фазы 1. | ✓ |
| Ещё обсудить | Есть неясные места по Фазе 1. | |

**User's choice:** `1`
**Notes:** Пользователь подтвердил запись контекста.

## the agent's Discretion

- Конкретные tooling choices внутри выбранных решений остаются на усмотрение planner/executor, если не противоречат CONTEXT.md.

## Deferred Ideas

- Business seed/demo data.
- `staging`/import schema.
- Frontend Docker image CI build.
- Yandex Lockbox integration.
- `staging` environment config.
