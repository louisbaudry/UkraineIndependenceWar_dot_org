# DR-0003 — Adopt W3C PROV as the cross-pipeline derivation/agency model

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-10 by founder/principal editor
**Origin:** CDR-W1-3, WP 0.2 §7 | **Supersedes:** — | **Superseded by:** —

## Context

Phase I requires end-to-end transformation lineage (§7, §22, §50, §58) and AI
provenance (§80) across activities far beyond preservation: OCR, translation,
AI enrichment, entity-resolution decisions, editorial review, dataset generation,
publication. Every derived object must answer "what was I derived from?" (§50).

## Alternatives considered

1. Adopt W3C PROV as the general model, PREMIS mapped into it (chosen).
2. Extend PREMIS events to cover all pipeline activity (rejected: stretches a
   preservation vocabulary beyond its discipline).
3. Custom lineage model (rejected: §94).

## Decision

W3C PROV (Entity / Activity / Agent; `wasGeneratedBy`, `used`, `wasDerivedFrom`,
`wasAttributedTo`, `actedOnBehalfOf`) is adopted as the **cross-pipeline
derivation and agency model**. PROV's native entity immutability (change = new
entity + derivation) is the conceptual anchor for "originals are immutable" (§7).

Boundary rule: every PREMIS event is expressible as a PROV activity; not every
PROV activity is a preservation event. PREMIS is mapped into PROV via the
published **PREMIS-3 OWL alignment** — no custom bridge is invented.

## Consequences

- AI outputs (§80) carry PROV attribution: model/tool as agent, prompt/inputs as
  used entities, output as generated entity.
- PROV bundles are the candidate mechanism for release-level reproducibility
  (§86–88); details fall to Workstream 7.
- The graph "what did the project know/use/conclude at time T" is expressible
  without new invention.
