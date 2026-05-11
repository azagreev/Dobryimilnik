# Requirements: Dobryimilnik E-Commerce Platform

**Defined:** 2026-05-11
**Core Value:** The owner can operate sales independently from Livemaster while preserving catalog integrity, SEO continuity, and legally compliant checkout.

## v1 Requirements

### Foundation

- [ ] **FND-01**: Developer can run the backend, database, cache, search, auth, and frontend services locally through documented commands.
- [ ] **FND-02**: Developer can create and apply PostgreSQL migrations for domain schemas.
- [ ] **FND-03**: CI runs linting, type checks, tests, and migration checks before deployment.
- [ ] **FND-04**: Application configuration and secrets are separated by environment and never committed.

### Import

- [ ] **IMP-01**: Admin can import Livemaster catalog data into staging tables with source IDs preserved.
- [ ] **IMP-02**: Admin can validate imported products, variants, categories, attributes, prices, stock, media, and SEO fields before publishing.
- [ ] **IMP-03**: Admin can view an import audit report showing imported, skipped, failed, and manually required records.
- [ ] **IMP-04**: System can re-run imports idempotently without duplicating products, variants, categories, or media.
- [ ] **IMP-05**: System can import blog posts, reviews, customer records, and historical orders into appropriate staging or canonical tables when source data is available.

### Catalog

- [ ] **CAT-01**: Admin can manage products with name, slug, description, SKU, price, old price, stock, active state, imported state, and SEO fields.
- [ ] **CAT-02**: Admin can manage product variants such as fragrance package sizes with separate price, SKU, stock, and active state.
- [ ] **CAT-03**: Admin can manage category tree and assign products to categories.
- [ ] **CAT-04**: Customer-facing API returns paginated and filterable product lists.
- [ ] **CAT-05**: Customer-facing API returns product detail by slug.
- [ ] **CAT-06**: Customer-facing API returns category tree and category product listings by slug.
- [ ] **CAT-07**: Search returns relevant products through Meilisearch and falls back to PostgreSQL pg_trgm when search service is unavailable.
- [ ] **CAT-08**: System maintains search indexes after catalog changes.

### Admin

- [ ] **ADM-01**: Admin can view, create, update, soft-delete, and restore products.
- [ ] **ADM-02**: Admin can perform bulk catalog and stock updates safely.
- [ ] **ADM-03**: Admin can view order list and order detail with payment, delivery, fiscal, and customer context.
- [ ] **ADM-04**: Admin can update order status through allowed lifecycle transitions.
- [ ] **ADM-05**: Admin can view dashboard metrics for orders, revenue, stock issues, import status, and system alerts.
- [ ] **ADM-06**: System records audit log entries for admin changes to catalog, stock, orders, and settings.

### Commerce

- [ ] **COM-01**: Customer can add product variants to cart.
- [ ] **COM-02**: Customer can view cart totals, quantities, stock availability, and validation errors.
- [ ] **COM-03**: Customer can remove or update cart items.
- [ ] **COM-04**: Customer can create an order from a valid cart.
- [ ] **COM-05**: System reserves or validates inventory during checkout to prevent oversell.
- [ ] **COM-06**: Customer can view order details after creation.
- [ ] **COM-07**: System handles order lifecycle states consistently from created through paid, shipped, cancelled, and refunded where applicable.

### Payments and Fiscalization

- [ ] **PAY-01**: Customer can initiate payment for an order through YouKassa.
- [ ] **PAY-02**: System processes YouKassa callbacks idempotently.
- [ ] **PAY-03**: System records payment status, provider IDs, amounts, and callback payload references.
- [ ] **FIS-01**: System creates fiscal receipt requests for paid orders according to 54-FZ needs.
- [ ] **FIS-02**: System records receipt status, provider IDs, errors, retries, and final receipt links or identifiers.
- [ ] **FIS-03**: Admin can see payment and fiscalization status on each order.

### Shipping

- [ ] **SHP-01**: Customer can request delivery calculation during checkout.
- [ ] **SHP-02**: System stores selected delivery method, address, price, and provider metadata on the order.
- [ ] **SHP-03**: Admin can update shipment status and tracking information.

### Users

- [ ] **USR-01**: Customer can register with email and password.
- [ ] **USR-02**: Customer can log in, refresh session, and log out.
- [ ] **USR-03**: Customer can view and update profile details.
- [ ] **USR-04**: Customer can manage delivery addresses.
- [ ] **USR-05**: Admin access is protected by RBAC.

### Content

- [ ] **CNT-01**: Customer-facing API returns blog post list and blog post detail by slug.
- [ ] **CNT-02**: Customer-facing API returns migrated reviews.
- [ ] **CNT-03**: Customer can submit a review when review creation is enabled.
- [ ] **CNT-04**: Admin can manage blog posts, reviews, and static pages.

### SEO

- [ ] **SEO-01**: System stores SEO title, description, canonical URL, and indexability settings for products, categories, blog posts, and pages.
- [ ] **SEO-02**: System preserves or maps Livemaster slugs into stable owned-platform URLs.
- [ ] **SEO-03**: System generates redirects for migrated product, category, blog, and page URLs.
- [ ] **SEO-04**: System generates XML sitemaps for products, categories, blog posts, and pages.
- [ ] **SEO-05**: Public product, category, and content pages render SEO-critical content server-side.

### Observability and Release

- [ ] **OPS-01**: System exposes health checks for backend, database, Redis, search, auth, and external integrations.
- [ ] **OPS-02**: System emits structured logs for imports, checkout, payments, fiscalization, and admin actions.
- [ ] **OPS-03**: System exposes metrics and dashboards for operational monitoring.
- [ ] **OPS-04**: Deployment pipeline can promote a verified build to the target environment.
- [ ] **OPS-05**: Backup and restore procedures exist for PostgreSQL and object storage.

## v2 Requirements

### Marketplace and Growth

- **MKT-01**: Admin can synchronize selected catalog data with Ozon.
- **MKT-02**: Admin can synchronize selected catalog data with Wildberries.
- **MKT-03**: Customer can use loyalty, promotions, or personalized offers.
- **MKT-04**: Admin can run advanced marketing automation and email campaigns.

### Advanced CRM

- **CRM-01**: Admin can segment customers by purchase behavior.
- **CRM-02**: Admin can manage support notes and customer communication history.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Native mobile apps | Web-first launch is enough for v1. |
| Real-time chat | Not needed for the backend-first sales migration. |
| Microservices split | Modular monolith is simpler and aligned with v1 needs. |
| Full marketplace automation | Owned-channel launch is the priority. |
| Advanced marketing automation | Defer until core commerce is stable. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| FND-01 | Phase 1 | Pending |
| FND-02 | Phase 1 | Pending |
| FND-03 | Phase 1 | Pending |
| FND-04 | Phase 1 | Pending |
| IMP-01 | Phase 2 | Pending |
| IMP-02 | Phase 2 | Pending |
| IMP-03 | Phase 2 | Pending |
| IMP-04 | Phase 2 | Pending |
| IMP-05 | Phase 2 | Pending |
| CAT-01 | Phase 3 | Pending |
| CAT-02 | Phase 3 | Pending |
| CAT-03 | Phase 3 | Pending |
| CAT-04 | Phase 3 | Pending |
| CAT-05 | Phase 3 | Pending |
| CAT-06 | Phase 3 | Pending |
| CAT-07 | Phase 3 | Pending |
| CAT-08 | Phase 3 | Pending |
| ADM-01 | Phase 4 | Pending |
| ADM-02 | Phase 4 | Pending |
| ADM-03 | Phase 7 | Pending |
| ADM-04 | Phase 7 | Pending |
| ADM-05 | Phase 10 | Pending |
| ADM-06 | Phase 7 | Pending |
| COM-01 | Phase 5 | Pending |
| COM-02 | Phase 5 | Pending |
| COM-03 | Phase 5 | Pending |
| COM-04 | Phase 5 | Pending |
| COM-05 | Phase 5 | Pending |
| COM-06 | Phase 5 | Pending |
| COM-07 | Phase 5 | Pending |
| PAY-01 | Phase 6 | Pending |
| PAY-02 | Phase 6 | Pending |
| PAY-03 | Phase 6 | Pending |
| FIS-01 | Phase 6 | Pending |
| FIS-02 | Phase 6 | Pending |
| FIS-03 | Phase 6 | Pending |
| SHP-01 | Phase 6 | Pending |
| SHP-02 | Phase 6 | Pending |
| SHP-03 | Phase 7 | Pending |
| USR-01 | Phase 7 | Pending |
| USR-02 | Phase 7 | Pending |
| USR-03 | Phase 7 | Pending |
| USR-04 | Phase 7 | Pending |
| USR-05 | Phase 7 | Pending |
| CNT-01 | Phase 8 | Pending |
| CNT-02 | Phase 8 | Pending |
| CNT-03 | Phase 8 | Pending |
| CNT-04 | Phase 8 | Pending |
| SEO-01 | Phase 8 | Pending |
| SEO-02 | Phase 8 | Pending |
| SEO-03 | Phase 8 | Pending |
| SEO-04 | Phase 8 | Pending |
| SEO-05 | Phase 9 | Pending |
| OPS-01 | Phase 10 | Pending |
| OPS-02 | Phase 10 | Pending |
| OPS-03 | Phase 10 | Pending |
| OPS-04 | Phase 10 | Pending |
| OPS-05 | Phase 10 | Pending |

**Coverage:**
- v1 requirements: 54 total
- Mapped to phases: 54
- Unmapped: 0

---
*Requirements defined: 2026-05-11*
*Last updated: 2026-05-11 after initialization*
