# Feature Research: Dobryimilnik

**Source:** Synthesized from `doc/PRD.md` during `$gsd-new-project`. No external web research was run in this Codex session.

## Table Stakes

- Catalog import for products, variants, attributes, categories, inventory, images, SEO fields, and source IDs.
- Product/category APIs with pagination, filtering, product detail, and category browsing.
- Search with typo-tolerant search engine and database fallback.
- Admin CRUD for products, categories, stock, orders, imports, and content.
- Cart, checkout, order creation, payment initiation, delivery calculation, and order status updates.
- 54-FZ fiscal receipt workflow for legal checkout.
- User registration/login/profile/address management.
- SEO migration support: stable slugs, redirects, metadata, sitemap, canonical URLs.
- Blog/review/content migration surfaces.
- Operational audit logs and basic analytics.

## Differentiators

- High-quality migration audit reports that show exactly what imported, failed, or needs manual review.
- Category/attribute model tailored to craft supply products, especially fragrances by volume.
- SEO continuity dashboard for imported pages, redirects, and missing metadata.
- Admin workflows optimized for a small owner-operated shop rather than a generic enterprise catalog.

## Anti-Features

- Building marketplace automation before the owned sales channel works.
- Premature microservices split.
- Heavy personalization, loyalty, or marketing automation before transaction reliability.
- Custom auth implementation when Keycloak is already selected.

## Complexity Notes

- The riskiest features are import correctness, inventory consistency, fiscalization, payment callbacks, and SEO redirects.
- Public storefront can be staged after backend APIs and operational admin are stable.
