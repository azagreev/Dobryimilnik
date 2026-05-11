# Roadmap: Dobryimilnik E-Commerce Platform

## Overview

This roadmap builds the owned Dobryimilnik platform from the backend outward. It starts with infrastructure and data migration, stabilizes catalog/admin/commerce/fiscal contracts, then adds content, SEO, storefront, and production readiness. The sequence reflects the selected backend-first v1 and fine granularity.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Foundation and Domain Skeleton** - Establish services, schemas, CI, config, and baseline app structure.
- [ ] **Phase 2: Livemaster Import Pipeline** - Load, validate, audit, and re-run migrated marketplace data safely.
- [ ] **Phase 3: Catalog Core and Search APIs** - Build canonical catalog, variants, categories, public APIs, and search indexing.
- [ ] **Phase 4: Admin Catalog Operations** - Give admin practical CRUD, bulk edit, stock, and import issue workflows.
- [ ] **Phase 5: Commerce Core** - Implement cart, checkout, orders, inventory reservation, and order lifecycle.
- [ ] **Phase 6: Payment, Shipping, and 54-FZ Fiscalization** - Add payment, delivery calculation, fiscal receipts, and retry/idempotency handling.
- [ ] **Phase 7: Users, RBAC, and Order Admin** - Add customer accounts, addresses, RBAC, order operations, shipment updates, and audit logs.
- [ ] **Phase 8: Content and SEO Migration Backend** - Add content/reviews APIs, admin content tools, SEO metadata, redirects, and sitemaps.
- [ ] **Phase 9: Public Storefront Contract** - Build SSR-ready storefront surfaces against stable backend contracts.
- [ ] **Phase 10: Observability and Release Readiness** - Add health checks, logs, metrics, dashboards, deployment, backups, and launch hardening.

## Phase Details

### Phase 1: Foundation and Domain Skeleton
**Goal:** Establish the technical base for a modular FastAPI/PostgreSQL/Next.js commerce platform.
**Depends on:** Nothing (first phase)
**Requirements:** [FND-01, FND-02, FND-03, FND-04]
**Success Criteria** (what must be TRUE):
  1. Developer can start all local services using documented commands.
  2. Database migrations create the required domain schemas.
  3. CI validates code quality and migrations on every change.
  4. Environment config and secrets are separated from committed code.
**Plans:** 4 plans

Plans:
**Wave 1**
- [x] 01-01: Repository structure, service scaffold, and local development workflow

**Wave 2** *(blocked on Wave 1 completion)*
- [x] 01-02: PostgreSQL schemas, migration tooling, and baseline models
- [x] 01-03: Configuration, secrets, and environment management

**Wave 3** *(blocked on Wave 2 completion)*
- [x] 01-04: CI quality gates and smoke tests

### Phase 2: Livemaster Import Pipeline
**Goal:** Import source marketplace data into auditable staging and canonical structures without duplication.
**Depends on:** Phase 1
**Requirements:** [IMP-01, IMP-02, IMP-03, IMP-04, IMP-05]
**Success Criteria** (what must be TRUE):
  1. Admin can run an import that preserves source IDs and batch metadata.
  2. Admin can inspect validation errors before records are published.
  3. Re-running the same import does not duplicate products, variants, categories, media, orders, customers, posts, or reviews.
  4. Import reports clearly identify success, skipped rows, failures, and manual-review items.
**Plans:** 5 plans

Plans:
- [x] 02-01: Source file contracts and import batch model
- [x] 02-02: Staging tables and source identity preservation
- [x] 02-03: Validation and normalization pipeline
- [x] 02-04: Idempotent staging reruns and classification
- [x] 02-05: Import audit report and failure review

### Phase 3: Catalog Core and Search APIs
**Goal:** Provide a complete canonical catalog backend with public read APIs and reliable search.
**Depends on:** Phase 2
**Requirements:** [CAT-01, CAT-02, CAT-03, CAT-04, CAT-05, CAT-06, CAT-07, CAT-08]
**Success Criteria** (what must be TRUE):
  1. Product, variant, category, and SEO fields are persisted and queryable.
  2. Product and category APIs support list/detail use cases needed by the storefront.
  3. Search works through Meilisearch and falls back to PostgreSQL when unavailable.
  4. Catalog changes update search indexes reliably.
**Plans:** 5 plans

Plans:
- [ ] 03-01: Product, variant, category, attribute, media, and SEO models
- [ ] 03-02: Product and category public read APIs
- [ ] 03-03: Filtering, pagination, and slug lookups
- [ ] 03-04: Meilisearch integration and pg_trgm fallback
- [ ] 03-05: Search reindexing and catalog API tests

### Phase 4: Admin Catalog Operations
**Goal:** Give the owner safe operational tools for catalog maintenance after migration.
**Depends on:** Phase 3
**Requirements:** [ADM-01, ADM-02]
**Success Criteria** (what must be TRUE):
  1. Admin can create, update, soft-delete, restore, and review products.
  2. Admin can safely bulk-edit catalog fields and stock.
  3. Admin can inspect import issues in the same operational flow as catalog editing.
**Plans:** 4 plans

Plans:
- [ ] 04-01: Admin catalog API and permissions boundary
- [ ] 04-02: Product CRUD, soft-delete, restore, and validation
- [ ] 04-03: Bulk edit and stock update workflows
- [ ] 04-04: Import issue review inside admin catalog tools

### Phase 5: Commerce Core
**Goal:** Implement cart, checkout, order creation, inventory reservation, and order lifecycle before external payment/fiscal wiring.
**Depends on:** Phase 4
**Requirements:** [COM-01, COM-02, COM-03, COM-04, COM-05, COM-06, COM-07]
**Success Criteria** (what must be TRUE):
  1. Customer can add, update, view, and remove cart items with stock validation.
  2. Customer can create an order from a valid cart.
  3. Checkout cannot oversell inventory under concurrent order attempts.
  4. Orders move through a consistent lifecycle with traceable state changes.
**Plans:** 5 plans

Plans:
- [ ] 05-01: Cart model, APIs, totals, and validation
- [ ] 05-02: Checkout and order creation workflow
- [ ] 05-03: Inventory reservation and stock mutation log
- [ ] 05-04: Order lifecycle state machine
- [ ] 05-05: Commerce concurrency and lifecycle tests

### Phase 6: Payment, Shipping, and 54-FZ Fiscalization
**Goal:** Connect checkout to payment, delivery calculation, and legally required receipt workflows.
**Depends on:** Phase 5
**Requirements:** [PAY-01, PAY-02, PAY-03, FIS-01, FIS-02, FIS-03, SHP-01, SHP-02]
**Success Criteria** (what must be TRUE):
  1. Customer can initiate payment for an order.
  2. Duplicate payment callbacks do not create duplicate side effects.
  3. Paid orders trigger receipt creation and expose fiscal status to admin.
  4. Checkout stores selected delivery method, address, price, and provider metadata.
**Plans:** 5 plans

Plans:
- [ ] 06-01: YouKassa payment initiation and payment records
- [ ] 06-02: Idempotent payment callback handling
- [ ] 06-03: Shipping calculation and order delivery metadata
- [ ] 06-04: 54-FZ fiscal receipt request, retry, and status tracking
- [ ] 06-05: Payment, shipping, and fiscal admin visibility

### Phase 7: Users, RBAC, and Order Admin
**Goal:** Add customer identity, address management, protected admin access, and complete order operations.
**Depends on:** Phase 6
**Requirements:** [ADM-03, ADM-04, ADM-06, SHP-03, USR-01, USR-02, USR-03, USR-04, USR-05]
**Success Criteria** (what must be TRUE):
  1. Customer can register, log in, refresh session, log out, manage profile, and manage addresses.
  2. Admin access is protected by RBAC.
  3. Admin can inspect and update orders through allowed transitions.
  4. Admin catalog, stock, order, shipment, and settings changes are audit logged.
**Plans:** 5 plans

Plans:
- [ ] 07-01: Keycloak integration and customer auth flows
- [ ] 07-02: Profile and address APIs
- [ ] 07-03: Admin RBAC and protected routes
- [ ] 07-04: Order admin, status transitions, shipment tracking
- [ ] 07-05: Admin audit log coverage

### Phase 8: Content and SEO Migration Backend
**Goal:** Preserve content and SEO continuity through backend-managed content, metadata, redirects, and sitemaps.
**Depends on:** Phase 7
**Requirements:** [CNT-01, CNT-02, CNT-03, CNT-04, SEO-01, SEO-02, SEO-03, SEO-04]
**Success Criteria** (what must be TRUE):
  1. Blog and review data can be served through public APIs.
  2. Admin can manage blog posts, reviews, and static pages.
  3. SEO metadata and stable owned-platform URLs exist for migrated entities.
  4. Redirects and XML sitemaps can be generated from migrated content.
**Plans:** 5 plans

Plans:
- [ ] 08-01: Content and review models and public APIs
- [ ] 08-02: Admin content, review, and page management
- [ ] 08-03: SEO metadata model and canonical URL handling
- [ ] 08-04: Livemaster slug mapping and redirect generation
- [ ] 08-05: XML sitemap generation

### Phase 9: Public Storefront Contract
**Goal:** Build SSR-ready public storefront pages on stable backend contracts.
**Depends on:** Phase 8
**Requirements:** [SEO-05]
**Success Criteria** (what must be TRUE):
  1. Product, category, search, blog, and review pages render SEO-critical content server-side.
  2. Storefront uses backend APIs without duplicating commerce logic.
  3. Customer can browse products, view product details, search, and enter checkout from the public UI.
  4. Metadata, canonical tags, and structured navigation are rendered for SEO-sensitive pages.
**Plans:** 5 plans

Plans:
- [ ] 09-01: Next.js app shell, routing, and API client
- [ ] 09-02: Category, listing, search, and product detail pages
- [ ] 09-03: Cart and checkout UI integration
- [ ] 09-04: Blog, review, and static content pages
- [ ] 09-05: SSR metadata, sitemap links, and storefront smoke tests

### Phase 10: Observability and Release Readiness
**Goal:** Harden the platform for production operations and launch.
**Depends on:** Phase 9
**Requirements:** [ADM-05, OPS-01, OPS-02, OPS-03, OPS-04, OPS-05]
**Success Criteria** (what must be TRUE):
  1. Health checks cover backend, database, Redis, search, auth, and external integrations.
  2. Logs and metrics make imports, checkout, payment, fiscalization, and admin actions diagnosable.
  3. Admin dashboard exposes order, revenue, stock, import, and system alert metrics.
  4. Deployment, backup, and restore procedures are documented and verified.
**Plans:** 5 plans

Plans:
- [ ] 10-01: Health checks and readiness endpoints
- [ ] 10-02: Structured logs for critical workflows
- [ ] 10-03: Metrics, dashboards, and admin operational dashboard
- [ ] 10-04: Deployment pipeline and environment promotion
- [ ] 10-05: Backup, restore, and launch readiness verification

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 -> 10

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation and Domain Skeleton | 0/4 | Not started | - |
| 2. Livemaster Import Pipeline | 5/5 | Complete | 2026-05-11 |
| 3. Catalog Core and Search APIs | 0/5 | Not started | - |
| 4. Admin Catalog Operations | 0/4 | Not started | - |
| 5. Commerce Core | 0/5 | Not started | - |
| 6. Payment, Shipping, and 54-FZ Fiscalization | 0/5 | Not started | - |
| 7. Users, RBAC, and Order Admin | 0/5 | Not started | - |
| 8. Content and SEO Migration Backend | 0/5 | Not started | - |
| 9. Public Storefront Contract | 0/5 | Not started | - |
| 10. Observability and Release Readiness | 0/5 | Not started | - |
