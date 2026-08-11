# DR-0011 — Adopt LRMoo 1.0 conceptually for documentary identity

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W2-2, WP 0.3 §7 | **Supersedes:** — | **Superseded by:** —

## Context

Phase I §22 forbids collapsing documentary layers into "a file": intellectual
work, language/version, published form, individual copy, and derivatives must
stay distinct. §58 requires translations to be derived scholarly objects.

## Alternatives considered

1. LRMoo 1.0 (IFLA-endorsed 2024, CRM-compatible successor to FRBRoo) (chosen).
2. BIBFRAME as master model (rejected as master; retained as compare/map per
   WP 0.1 matrix).
3. Flat document model with type flags (rejected: exactly what §22 forbids).

## Decision

LRMoo 1.0 is adopted **conceptually** for documentary identity:
**Work / Expression / Manifestation / Item**, with creation and publication as
events carrying agents and typed roles (supporting §23's stated-author /
actual-author / signer / publisher / issuing-authority distinctions).
Translations, OCR outputs, transcripts, and excerpts are **expressions/derivatives
with their own PROV provenance** (DR-0003). Source-lifecycle states (§24) are
events on manifestations in this layer, evidenced by pipeline captures.

## Consequences

- Being a CRM extension, LRMoo keeps layers C and D natively compatible.
- The preserved copy is one holding with two linked views: LRMoo Item
  (documentary) and PREMIS representation (preservation); the bridge rule goes to
  the semantic registry (WP 0.3 §8 Q2).
- Quotation/passage targeting builds on expressions (Workstream 3).
