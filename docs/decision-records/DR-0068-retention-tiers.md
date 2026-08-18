# DR-0068 — Retention tiers

**Category:** preservation | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-15, SPEC-0003 §4 | **Supersedes:** — | **Superseded by:** —

## Context

Record §9 requires multi-stage retention with source-specific policy, allows
comprehensive preservation of fragile or high-value sources before
item-level relevance is known, and warns against archiving everything
equally (PRES-011).

## Alternatives considered

1. Four tiers with escalate-freely semantics (chosen).
2. Binary keep/discard (rejected: loses the metadata-only and review-later
   cases §9 names).

## Decision

Every acquired item receives a retention decision at Gate 1 (DR-0066),
defaulting from its source (DR-0067):

- **`discard`** — not retained; the acquisition event and outcome are still
  recorded (§28).
- **`metadata-only`** — descriptive record retained, content not stored
  (rights, sensitivity, or volume grounds).
- **`medium-term`** — retained with a review date, then re-decided.
- **`permanent`** — archival preservation under full OAIS/PREMIS treatment.

Tiers **escalate freely**; a **downgrade is a governed disposition decision**
with recorded rationale. Fragile or high-value sources may be collected at
`permanent` before item-level relevance is known, and a source's escalation
may trigger retrospective recovery from external archives (§9).

## Consequences

- Volume is managed without pretending discarded material never existed.
- Tier decisions are auditable and reversible upward without loss.
