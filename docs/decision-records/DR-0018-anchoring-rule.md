# DR-0018 — Anchoring rule: evidential annotations target preserved captures

**Category:** architecture / preservation | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W3-2, WP 0.4 §3.2/§5 | **Supersedes:** — | **Superseded by:** —

## Context

Record §24: the same URL may later serve different content. An annotation
anchored to a live URL silently decays — for evidential use this is
unacceptable. WP 0.2 established capture preservation; WP 0.4 connects it to
evidence targeting.

## Alternatives considered

1. Target preserved expressions/captures, live origin as context (chosen).
2. Target live URLs with periodic re-verification (rejected: decay is silent
   between checks; evidence must not depend on external servers).
3. Target both with live as primary (rejected: inverts the priority §24 implies).

## Decision

**Evidential annotations target preserved expressions/captures held by the
archive** — never a live URL alone. Targets are version-pinned (State), use
selector redundancy (quote + position where applicable), and may record the
live-web origin as context. If material is not yet preserved, preservation
precedes evidential annotation.

## Consequences

- The evidence layer inherits the archive's fixity and immutability guarantees
  (DR-0005, DR-0003) automatically.
- "What exactly did this assertion point at?" remains answerable forever,
  independent of the live web (record §86, Principle 16).
- Annotation workflows gain a preservation-first step; this is a feature, not
  friction.
