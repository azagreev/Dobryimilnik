# Stack Research: Dobryimilnik

**Source:** Synthesized from `doc/PRD.md` during `$gsd-new-project`. No external web research was run in this Codex session.

## Recommended Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Backend | Python 3.12 + FastAPI | Async APIs, strong typing, good fit for modular monolith boundaries. |
| Frontend | Next.js 14 | SSR for SEO-sensitive catalog, React ecosystem for admin and storefront. |
| Database | PostgreSQL 16 | ACID commerce data, schemas per domain, JSONB, pg_trgm, reporting queries. |
| Search | Meilisearch with pg_trgm fallback | Fast product search with reliable database fallback. |
| Cache/Jobs | Redis + Celery | Cart/session caching, imports, image processing, fiscal/payment retries. |
| Auth | Keycloak | Production-ready auth/RBAC to avoid custom auth risk. |
| Storage | Yandex Object Storage | Product photos, backups, CDN-friendly object storage. |
| Secrets | Yandex Lockbox | Centralized secret storage for payment/fiscal credentials. |
| Observability | Prometheus + Grafana + Loki | Metrics, dashboards, logs, alerting. |
| Deployment | Docker Swarm | Simpler than Kubernetes for the target scale and team size. |
| CI/CD | GitHub Actions | Automated checks and deployment pipeline. |

## Stack Notes

- Keep FastAPI modules aligned to domain schemas: `catalog`, `orders`, `users`, `content`, and analytics/audit in `public`.
- Use async IO at API boundaries, but keep long-running imports and external callbacks in background jobs.
- Treat fiscalization, payment, delivery, and import as retryable workflows with idempotency keys.
- Prefer server-rendered public catalog/category/product pages for SEO; admin screens can be client-heavy.

## Confidence

High for the stack because it is explicitly defined in the PRD and matches the project constraints.
