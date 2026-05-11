# Phase 1: Foundation and Domain Skeleton - Context

**Gathered:** 2026-05-11
**Status:** Ready for planning

<domain>
## Phase Boundary

Эта фаза создаёт технический фундамент проекта: локальный запуск всех базовых сервисов, каркас FastAPI/Next.js, PostgreSQL domain schemas, миграции, минимальный CI, правила конфигурации и секретов. Фаза не должна добавлять бизнес-демо данные, импорт Livemaster, публичный каталог, корзину, оплату или storefront-функции.

</domain>

<decisions>
## Implementation Decisions

### Локальная разработка
- **D-01:** Локальный запуск должен быть через Docker Compose для всего набора сервисов.
- **D-02:** Уже в Фазе 1 `make dev` должен поднимать полный набор: `Postgres`, `Redis`, `Meilisearch`, `Keycloak`, `backend`, `frontend`.
- **D-03:** Основная команда разработчика: `make dev`. Makefile должен быть единой точкой входа поверх Docker/uv/npm.
- **D-04:** Бизнес seed/demo данные в Фазе 1 не нужны. Их следует оставить для фаз импорта и каталога.

### Структура backend
- **D-05:** Backend с самого начала делится строго по доменам: `catalog`, `orders`, `users`, `content`, `analytics`.
- **D-06:** Внутри домена использовать структуру `API -> service -> repository`.
- **D-07:** API сразу версионировать через `/api/v1/...`.
- **D-08:** Общий код держать в `core`: config, db session, logging, errors, security, pagination, base schemas.

### База данных и миграции
- **D-09:** PostgreSQL должен использовать 5 схем из PRD: `catalog`, `orders`, `users`, `content`, `public` для analytics/audit.
- **D-10:** Миграции вести отдельными domain migration streams/folders по доменам.
- **D-11:** `staging`/import schema не создавать в Фазе 1; полностью оставить staging/import на Фазу 2.
- **D-12:** Seed данные в Фазе 1 не нужны. Достаточно миграций и healthchecks.

### CI и проверки качества
- **D-13:** Первый CI должен начинаться минимально: `lint` и `type` checks.
- **D-14:** Coverage gate должен быть жёстким, но не должен блокировать пустой scaffold. Как только backend tests заведены в рамках фазы, coverage становится обязательным gate.
- **D-15:** Миграции в CI проверять через `upgrade + downgrade`.
- **D-16:** Docker image build check в Фазе 1 нужен только для backend. Frontend image build добавить позже.

### Конфиг и секреты
- **D-17:** В Фазе 1 не создавать `.env.example`; правила env-файлов описать документацией.
- **D-18:** Config structure должна различать `local` и `prod`; `staging` добавить позже.
- **D-19:** Yandex Lockbox не учитывать в Фазе 1; вернуться ближе к production/release readiness.
- **D-20:** Docker Compose должен моделировать `Docker secrets pattern`, а не хранить секреты в git.

### the agent's Discretion
Planner может сам выбрать конкретные Python/JS tooling details, если они не противоречат решениям выше: например, `ruff`/`mypy`/`pytest`, npm package manager, Alembic layout details, Dockerfile layering, naming conventions внутри выбранных доменных границ.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project scope
- `.planning/PROJECT.md` — project vision, backend-first v1 decision, constraints, and out-of-scope boundaries.
- `.planning/REQUIREMENTS.md` — Phase 1 requirements `FND-01` through `FND-04` plus full roadmap traceability.
- `.planning/ROADMAP.md` — Phase 1 goal, success criteria, and planned plan split.
- `.planning/STATE.md` — current project state and session continuity.

### Source PRD
- `doc/PRD.md` — original Russian PRD defining stack, architecture, domain schemas, and target platform context.

### Research summary
- `.planning/research/STACK.md` — PRD-derived stack decisions.
- `.planning/research/ARCHITECTURE.md` — modular monolith boundaries and suggested build order.
- `.planning/research/SUMMARY.md` — initialization research summary and risk framing.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- No application code exists yet. This is a greenfield scaffold phase.

### Established Patterns
- Planning artifacts establish backend-first sequencing and modular monolith boundaries.
- No `.planning/codebase/*.md` maps exist yet because no implementation code has been created.

### Integration Points
- New code should connect to the project root via `make dev`, Docker Compose, backend scaffold, frontend scaffold, migration commands, and CI workflows.

</code_context>

<specifics>
## Specific Ideas

- The developer-facing happy path should be simple: clone repo, read docs, run `make dev`, and get all core services running.
- The phase should prefer operational correctness over demo data or visual storefront progress.
- The frontend service is part of the local stack in Phase 1, but frontend production image checks are deferred.

</specifics>

<deferred>
## Deferred Ideas

- Business seed/demo catalog data belongs in Phase 2 or Phase 3.
- `staging`/import schema and import batch tables belong in Phase 2.
- Frontend Docker image CI build belongs after frontend structure is meaningful.
- Yandex Lockbox integration belongs closer to production/release readiness.
- `staging` environment config belongs after `local` and `prod` structure is stable.

</deferred>

---

*Phase: 1-Foundation and Domain Skeleton*
*Context gathered: 2026-05-11*
