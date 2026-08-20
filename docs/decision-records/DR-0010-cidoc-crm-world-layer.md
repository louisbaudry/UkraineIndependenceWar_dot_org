# DR-0010 — Adopt CIDOC CRM conceptually for the historical world layer

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W2-1, WP 0.3 §7 | **Supersedes:** — | **Superseded by:** —

## Context

The world layer (WP 0.1 layer C) needs a mature model for actors, events, objects,
places, time and identity. Phase I §16–21, §45–48 demand event-centric, temporal,
provenance-bearing modeling; record §94 demands established standards first.

## Alternatives considered

1. CIDOC CRM (7.1.3 / ISO 21127:2023) conceptually (chosen).
2. Custom event ontology (rejected: §94).
3. Wikidata-style generic statements (rejected as master model: weaker event
   semantics; retained as external mapping target per §16).

## Decision

CIDOC CRM is adopted **conceptually** as the reference model for the historical
world layer: events/activities/periods, actors (persons, groups), physical
objects, places (identity distinct from geometry), fuzzy-bounded time-spans,
appellations, identifiers, and typed participation.

Explicitly **not** adopted: CIDOC CRM as physical schema, serialization, or
storage model — record §95 stays reserved to Phase III. Extension subset
(CRMsci, CRMgeo, CRMdig, CRMsoc) remains open (WP 0.3 §8 Q1).

## Consequences

- World-layer concept work proceeds in CRM vocabulary; the conflict register
  carries CRM term senses (work, item, document, actor, period).
- CRMdig overlap with PROV/PREMIS must be reconciled under DR-0003.
- DR-0004's layer boundary now has named models on both sides.
