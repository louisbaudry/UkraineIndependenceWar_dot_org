# DR-0066 — Three-gate pipeline model

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-13, SPEC-0003 §2 | **Supersedes:** — | **Superseded by:** —

## Context

Record §8 separates collection into stages and insists collection never
implies publication (OPS-001); Principle 11 separates preservation from
publication; §78–79 require human accountability at acceptance.

## Alternatives considered

1. Three distinct gates with separate criteria and records (chosen).
2. A single acceptance decision covering preservation and knowledge
   (rejected: merges decisions with different criteria, deciders, and risk
   profiles into one record).
3. Defer until collectors exist (rejected: the gate structure constrains
   collector design, not the reverse).

## Decision

The pipeline has three structural gates:

- **Gate 1 — Preservation:** does an acquired item become an archival object,
  at which retention tier (DR-0068)? Requires security checks cleared, fixity
  computed (DR-0005), acquisition provenance recorded. Failing Gate 1 still
  leaves a permanent acquisition-event trace (§28, PRES-007).
- **Gate 2 — Editorial acceptance:** does anything extracted become canonical
  knowledge? Nothing crosses on automated confidence alone; proposals become
  assertions only by human acceptance at the applicable risk tier (§78,
  DR-0063, AI-001). Material may be permanently preserved and never cross
  Gate 2 — the normal case for bulk collection.
- **Gate 3 — Publication:** does accepted knowledge or a preserved item reach
  a public surface, at which access tier (§12)?

Every stage transition is a PROV activity (DR-0003) with agent, inputs,
outputs, and version. The pipeline is restartable and idempotent: re-running
a stage produces a new derivative with new provenance, never an in-place
mutation (DR-0055).

## Consequences

- "Collection never implies publication" is enforced by architecture rather
  than by discipline.
- Each gate has its own audit trail, answering "who decided what, when, on
  what basis" at three distinct decision points.
