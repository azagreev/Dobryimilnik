<!-- GSD:project-start source:PROJECT.md -->
## Project

**Dobryimilnik E-Commerce Platform**

Dobryimilnik is a custom e-commerce platform for IP Vlasyuk A.N. to migrate a long-running Livemaster shop into an owned sales channel. The project moves a 1,966-SKU catalog, order flow, customer base, content, reviews, SEO equity, and fiscalization requirements into a modular monolith built around FastAPI, PostgreSQL, and Next.js.

The first milestone is backend-first: build a reliable import, catalog, inventory, commerce, payment, delivery, fiscal, and admin foundation before investing heavily in the public storefront experience.

**Core Value:** The owner can operate sales independently from Livemaster while preserving catalog integrity, SEO continuity, and legally compliant checkout.

### Constraints

- **Legal/Fiscal**: Checkout must support Russian 54-FZ fiscalization and receipt lifecycle because the client is an IP on USN 6% without VAT.
- **SEO**: Product/category/blog URLs, metadata, redirects, and SSR behavior are launch-critical because organic continuity is part of the migration value.
- **Data migration**: Import must preserve 1,966 SKUs, media, variants, inventory, categories, customer/order history, reviews, and content where available.
- **Architecture**: Use a modular monolith with FastAPI backend and PostgreSQL schemas instead of distributed microservices.
- **Frontend**: Use Next.js SSR/CSR for SEO-sensitive catalog and product pages.
- **Operations**: Admin workflows must be practical for a small business owner, not an enterprise back office.
<!-- GSD:project-end -->

<!-- GSD:stack-start source:research/STACK.md -->
## Technology Stack

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
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

## Communication

- Always respond to the user in Russian.



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
