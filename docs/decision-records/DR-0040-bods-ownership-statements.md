# DR-0040 — Ownership and control follow the BODS statement pattern

**Category:** legal / architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W6-3, WP 0.7 §3–4/§6 | **Supersedes:** — | **Superseded by:** —

## Context

Record §19 requires distinguishing legal, direct, indirect, beneficial, voting,
managerial, contractual, de facto, nominee, and ultimate ownership/control.
DR-0015 assigned this modeling here. The Beneficial Ownership Data Standard
(Open Ownership) independently chose statement-based, provenance-bearing
representation — the project's own assertion architecture.

## Alternatives considered

1. BODS-patterned interest statements (chosen).
2. Ownership edges with percentage fields (rejected: loses interest type,
   validity period, and provenance; merges §19's distinct senses).
3. GLEIF relationship model as base (rejected: covers only accounting
   consolidation; retained as a documentary source).

## Decision

Ownership and control are recorded as **typed interest statements**: interest
type (per §19's senses, aligned with BODS interest types), interested party,
subject, share/percentage as quantity objects (DR-0030), validity period, and
full provenance. Registry filings, GLEIF relationship records, disclosures, and
investigative findings enter as **documentary sources** for statements
(§32). Conflicting statements coexist under the epistemic layer (DR-0024) —
never averaged (§40).

## Consequences

- Derived ownership computation (DR-0041) consumes statements and preserves
  paths.
- Corporate history events (§20) and interest statements cross-reference
  without merging.
- BODS export becomes a mapping, aiding interoperability with the
  beneficial-ownership ecosystem.
