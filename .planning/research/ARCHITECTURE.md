# Architecture Research: Dobryimilnik

**Source:** Synthesized from `doc/PRD.md` during `$gsd-new-project`. No external web research was run in this Codex session.

## Architecture Shape

Use a modular monolith:

- FastAPI backend owns domain modules and REST APIs.
- PostgreSQL stores transactional and content data in domain schemas.
- Redis and Celery handle cache/session needs and asynchronous jobs.
- Meilisearch indexes products while PostgreSQL pg_trgm provides fallback.
- Next.js serves SEO-sensitive storefront pages and admin UI.
- Fiscalization agent handles 54-FZ interactions separately enough to isolate legal/payment retry logic.

## Component Boundaries

- **Catalog**: products, variants, categories, attributes, images, stock fields, search indexing.
- **Commerce**: cart, checkout, orders, payment, delivery, inventory reservation, order status.
- **Users**: auth integration, profiles, addresses, RBAC.
- **Content**: blog, reviews, landing pages, SEO content.
- **Analytics/Audit**: event tracking, admin audit log, import audit, operational dashboards.
- **Integrations**: Livemaster import, YouKassa, delivery providers, OFD/fiscal provider, object storage.

## Data Flow

1. Import jobs load source data into staging tables.
2. Validation maps source data into canonical catalog/content/user/order tables.
3. Catalog mutations enqueue search reindex and media processing.
4. Checkout creates order/payment intents with idempotency.
5. Payment success reserves/commits inventory and triggers fiscal receipt creation.
6. Admin reviews operational dashboards, import issues, orders, and stock.

## Suggested Build Order

1. Foundation, schemas, migrations, local services, CI.
2. Import pipeline and canonical catalog model.
3. Catalog APIs, search, and admin catalog operations.
4. Commerce core: cart, checkout, orders, inventory.
5. Payment, delivery, and fiscalization.
6. SEO/content migration surfaces.
7. Frontend storefront once backend contracts are stable.
