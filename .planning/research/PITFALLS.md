# Pitfalls Research: Dobryimilnik

**Source:** Synthesized from `doc/PRD.md` during `$gsd-new-project`. No external web research was run in this Codex session.

## Critical Pitfalls

| Pitfall | Warning Signs | Prevention |
|---------|---------------|------------|
| Import loses source identity | Products import but cannot be traced back to Livemaster IDs. | Keep source IDs, import batches, row-level status, and audit reports. |
| SEO continuity is treated as frontend-only | Redirects and metadata are added late after catalog slugs drift. | Design slug/redirect/metadata model during catalog import. |
| Inventory race conditions | Orders and admin edits can oversell popular SKUs. | Use transactions, reservation states, idempotency, and explicit stock mutation logs. |
| Payment/fiscal callbacks are not idempotent | Duplicate callbacks create duplicate status changes or receipts. | Store provider event IDs and make callback handlers idempotent. |
| Admin is too generic | Owner needs spreadsheets/manual edits because admin cannot handle real catalog operations. | Build import issue review, bulk edits, stock management, and order ops early. |
| Search hides catalog data quality issues | Search works for clean products but fails on migrated attributes. | Validate attributes/categories before indexing and keep pg_trgm fallback. |
| Public storefront starts before backend contracts settle | UI churns while APIs and data model keep changing. | Backend-first sequencing, then stable frontend contracts. |

## Phase Mapping

- Import audit and source identity: Phases 1-3
- SEO data model: Phases 2, 8
- Inventory/order consistency: Phases 5-6
- Payment/fiscal idempotency: Phase 6
- Admin operational fit: Phases 4, 7
- Storefront contract stability: Phase 9
