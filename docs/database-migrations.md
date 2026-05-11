# Миграции базы данных

Миграции Alembic находятся в `backend/alembic/` и запускаются из каталога backend через цели `Makefile`.

## Команды

- `make migrate-up` применяет все миграции через `alembic upgrade head`.
- `make migrate-down` откатывает миграции до базы через `alembic downgrade base`.
- `make migrate-revision message="описание изменения"` создает ревизию с автогенерацией.

## Доменные схемы

На этапе 1 создаются схемы PostgreSQL для следующих доменных потоков:

- `catalog`
- `orders`
- `users`
- `content`
- `public` для аналитики, аудита и общих объектов PostgreSQL

На этапе 1 схема `staging` для импорта не создается, а миграции не вставляют бизнесовые seed-данные.
