# Dobryimilnik E-Commerce Platform

## What This Is

Dobryimilnik is a custom e-commerce platform for IP Vlasyuk A.N. to migrate a long-running Livemaster shop into an owned sales channel. The project moves a 1,966-SKU catalog, order flow, customer base, content, reviews, SEO equity, and fiscalization requirements into a modular monolith built around FastAPI, PostgreSQL, and Next.js.

The first milestone is backend-first: build a reliable import, catalog, inventory, commerce, payment, delivery, fiscal, and admin foundation before investing heavily in the public storefront experience.

## Core Value

The owner can operate sales independently from Livemaster while preserving catalog integrity, SEO continuity, and legally compliant checkout.

## Requirements

### Validated

(None yet - ship to validate)

### Active

- [ ] Import the full Livemaster catalog, media, category structure, and SEO metadata without data loss.
- [ ] Provide a normalized catalog backend with variants, attributes, stock, search, and admin CRUD.
- [ ] Support cart, checkout, order lifecycle, payment, delivery calculation, and inventory reservation.
- [ ] Integrate 54-FZ fiscalization and receipt handling for legal Russian online sales.
- [ ] Preserve SEO continuity through slug strategy, redirects, metadata, sitemap, and SSR-ready product/category surfaces.
- [ ] Provide operational admin tools for catalog, orders, stock, import audits, and basic analytics.

### Out of Scope

- Native mobile applications - web-first launch is enough for v1 and keeps scope focused.
- Real-time chat and complex CRM - not required to migrate the core sales flow.
- Marketplace seller automation for Ozon/Wildberries - existing marketplace presence can remain external until after owned-channel launch.
- Advanced marketing automation and loyalty mechanics - defer until the transaction core is stable.
- Headless microservices architecture - modular monolith is the intended v1 architecture for speed and operational simplicity.

## Context

The current shop runs on Livemaster at `https://www.livemaster.ru/dobryimilnik` and sells components for handmade candles, soap, and cosmetics. The business has 13 years of marketplace history, 11,652 reviews with a 5.0 average, 6,198 subscribers, 283 blog posts, and around 10,900 monthly marketplace clicks.

The catalog is large for a small merchant: 1,966 SKUs, 40+ categories, and strong concentration in fragrances, molds, cosmetic components, bottles/packaging, labels, hydrolats, tools, bases, extracts, and emulsifiers. Fragrance products require variants by volume such as 10g, 30g, 45g, and 100g.

The commercial reason for the project is material: Livemaster commission exposure is estimated at 3.1-9.4M RUB per year, while owned-platform operating costs are estimated around 38,400 RUB per year plus development and infrastructure. The platform needs to reduce dependency on marketplace economics without losing SEO and trust signals built over years.

## Constraints

- **Legal/Fiscal**: Checkout must support Russian 54-FZ fiscalization and receipt lifecycle because the client is an IP on USN 6% without VAT.
- **SEO**: Product/category/blog URLs, metadata, redirects, and SSR behavior are launch-critical because organic continuity is part of the migration value.
- **Data migration**: Import must preserve 1,966 SKUs, media, variants, inventory, categories, customer/order history, reviews, and content where available.
- **Architecture**: Use a modular monolith with FastAPI backend and PostgreSQL schemas instead of distributed microservices.
- **Frontend**: Use Next.js SSR/CSR for SEO-sensitive catalog and product pages.
- **Operations**: Admin workflows must be practical for a small business owner, not an enterprise back office.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Backend-first v1 | The user selected backend/import/API reliability before storefront polish. | - Pending |
| Interactive GSD mode | The user wants review checkpoints before major steps. | - Pending |
| Fine phase granularity | The project has legal, migration, SEO, and commerce risks that benefit from smaller phases. | - Pending |
| Parallel execution enabled | Independent plans may run concurrently once phases are planned. | - Pending |
| Balanced model profile | Good default for quality/cost on planning agents. | - Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `$gsd-transition`):
1. Requirements invalidated? -> Move to Out of Scope with reason
2. Requirements validated? -> Move to Validated with phase reference
3. New requirements emerged? -> Add to Active
4. Decisions to log? -> Add to Key Decisions
5. "What This Is" still accurate? -> Update if drifted

**After each milestone** (via `$gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check - still the right priority?
3. Audit Out of Scope - reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-11 after initialization*
