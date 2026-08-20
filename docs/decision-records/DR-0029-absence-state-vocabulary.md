# DR-0029 — Adopt the absence-state vocabulary

**Category:** epistemology / architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W4-6, WP 0.5 §8/§10 | **Supersedes:** — | **Superseded by:** —

## Context

Record §41 (Principle 8): a missing value must never silently mean "no."
Explicit negative assertions require provenance.

## Alternatives considered

1. Typed absence states (chosen).
2. Nullable fields with documentation (rejected: null is exactly the ambiguity
   §41 forbids).
3. Single "unknown" marker (rejected: collapses §41's distinct absence kinds).

## Decision

The absence-state vocabulary is adopted: **unknown / not-researched /
no-evidence-found / unavailable / withheld / redacted / lost-or-destroyed /
not-applicable / indeterminate** — entered in the semantic registry with
definitions. A missing value never defaults to a negative. Explicit negative
assertions ("X did not occur", "no license was issued") are assertions like any
other: attributed, dated, evidence-backed.

## Consequences

- "We searched and found nothing" (a finding with scope and method, §76) is
  representable and distinct from "we never looked."
- Negative-observation semantics for machine sources (coverage-aware "sensor
  looked and did not see") remain an open question (WP 0.5 §11 Q6) built on
  this vocabulary.
- Schema design in Phase III must expose these states, not bury them in nulls.
