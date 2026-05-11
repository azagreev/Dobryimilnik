# Research Summary: Dobryimilnik

**Source:** Synthesized from `doc/PRD.md` during `$gsd-new-project`. No external web research was run in this Codex session.

## Stack

The PRD-selected stack is coherent for the target: FastAPI + PostgreSQL modular monolith, Next.js for SEO, Redis/Celery for async work, Meilisearch with pg_trgm fallback, Keycloak for auth, Yandex Object Storage/Lockbox, Prometheus/Grafana/Loki, Docker Swarm, and GitHub Actions.

## Table Stakes

The platform must support reliable catalog migration, product/category/search APIs, admin catalog and order operations, cart/checkout/orders, payment, delivery, 54-FZ fiscalization, SEO migration, content/review support, user profiles, audit logging, and basic analytics.

## Watch Outs

The biggest risks are import correctness, SEO continuity, inventory consistency, idempotent payment/fiscal workflows, and admin workflows that actually match owner operations. The roadmap should keep public storefront work behind stable backend contracts.

## Roadmap Implication

Use a backend-first sequence with fine-grained phases: foundation, import staging, catalog core, admin operations, commerce core, payment/fiscal/delivery, users/content, SEO migration, storefront, and production readiness.
