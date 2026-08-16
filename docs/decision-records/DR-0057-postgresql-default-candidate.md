# DR-0057 — PostgreSQL as default implementation candidate

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-4, WP 3.1 §3–4 | **Supersedes:** — | **Superseded by:** —

## Context

DR-0054 fixes the representation (relational, assertion-centric, layered)
independently of any engine. An implementation default is still needed so
Phase III specification work has a concrete target, without welding the
representation to a product.

## Alternatives considered

1. PostgreSQL as default candidate, binding choice recorded in the SPEC with
   a revisit trigger (chosen).
2. Decide the engine now by DR (rejected: engine choice is implementation,
   not representation; WP 3.1 kept them separable deliberately).
3. No default (rejected: specifications need a concrete dialect for
   constraints, temporal patterns, and recursive queries).

## Decision

**PostgreSQL is the default implementation candidate** for the canonical
store: open source, three decades of history, universal operational
knowledge — the "boring technology" property WP 3.1 identified as a
preservation requirement (requirement 8). The **binding engine decision is
recorded in the conceptual data model SPEC** with an explicit revisit
trigger; representation commitments (DR-0054/0055) survive any engine
change.

## Consequences

- Phase III SPECs may use PostgreSQL-dialect examples without prejudice to
  the representation.
- An engine change would be a SPEC revision, not a DR supersession.
