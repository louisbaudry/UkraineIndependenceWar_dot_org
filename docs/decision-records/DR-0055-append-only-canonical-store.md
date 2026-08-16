# DR-0055 — Append-only canonical store with governed redaction

**Category:** architecture / preservation | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-2, WP 3.1 §4 | **Supersedes:** — | **Superseded by:** —

## Context

Record §63 forbids rewriting earlier epistemic states; §77 forbids silent
overwriting while allowing legal/privacy removals; DR-0048 requires baselines
that never mutate.

## Alternatives considered

1. Append-only assertions; supersession for correction; governed redaction
   with tombstones (chosen).
2. In-place updates with audit log (rejected: the audit log becomes the real
   store; queries against history become second-class).

## Decision

Canonical assertions are **append-only**: corrections and revisions are
superseding statements linked to what they supersede; nothing is edited in
place. **Deletion exists only as governed redaction** for the cases §77
recognizes (legal restriction, privacy removal, archival withdrawal),
executed under a recorded decision, leaving a **tombstone** that preserves
the fact, date, authority, and grounds of removal without the removed
content. Redaction mechanics are specified in the conceptual data model SPEC
(WP 3.1 §5 Q4).

## Consequences

- "What did we believe at time T" is a query, never a reconstruction.
- Redaction is visible as an event, never silent (§77).
- Storage growth is accepted as the cost of honesty; archiving policies for
  cold assertions are an operational matter, not a semantic one.
