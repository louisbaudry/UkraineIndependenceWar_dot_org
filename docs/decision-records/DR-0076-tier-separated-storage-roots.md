# DR-0076 — Retention-tier-separated storage roots

**Category:** preservation / operations | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-23, WP 3.3 §5.3 | **Supersedes:** — | **Superseded by:** —

## Context

DR-0068 established four retention tiers, of which `medium-term` items are
re-decided at a review date and may be disposed of. OCFL's model is
append-only; routine disposition must not operate anywhere near permanently
preserved material.

## Alternatives considered

1. Separate OCFL storage roots per retention tier (chosen).
2. A single root with tier recorded in metadata (rejected: disposition
   operations would run against the same root that holds the permanent
   archive — an unnecessary standing risk).

## Decision

- Only `permanent` and `medium-term` items (DR-0068) have bytes in OCFL;
  `metadata-only` has none and `discard` never enters.
- `permanent` and `medium-term` live in **separate OCFL storage roots**, so
  disposition at a medium-term review date is an operation on the
  medium-term root and **can never touch the permanent archive**.
- **Promotion** from medium-term to permanent is a recorded preservation
  event moving the object between roots.
- Storage roots use a **hashed n-tuple** object-ID-to-path layout, avoiding
  directory-size limits and keeping identifiers (which may echo source URLs)
  out of directory names.

## Consequences

- The permanent archive is structurally insulated from routine disposition.
- Tier promotion is visible in the preservation record rather than implicit.
- Per-root backup and replication policies may differ (DR-0009).
