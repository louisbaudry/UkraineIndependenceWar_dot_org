# DR-0043 — The transaction / shipment / payment triad

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W6-6, WP 0.7 §4/§6 | **Supersedes:** — | **Superseded by:** —

## Context

Record §68: a commercial transaction, a physical shipment, and a payment are
different events. Record §67: customs declarations are documentary assertions,
separate from project conclusions about actual goods, destinations, and end
users.

## Alternatives considered

1. Three distinct, linkable event types (chosen).
2. One "trade event" with facets (rejected: a shipment without identified
   payment, or a payment spanning many shipments, breaks the merged shape
   immediately).

## Decision

- **Transactions** (commercial agreements: parties, goods/services, terms),
  **shipments** (physical movements with §69 legs: origin, destination,
  intermediate points, mode, carrier, vessel, ports, customs events,
  transshipment; observed vs inferred legs distinguished), and **payments**
  (§70: payer/payee, institutions, amounts as quantity objects, currency,
  intermediaries) are three event types, linkable into trade networks, never
  merged.
- **Customs and trade declarations are documentary assertions** (§67) about
  declared exporter/importer/commodity/value/origin/destination/classification
  — bridged to project conclusions about actual goods, routes, and end users
  only through evidence relations (DR-0024 layer 3).
- Financial-flow depth beyond this remains deliberately minimal until
  investigations require it (§70).

## Consequences

- Procurement-network analysis composes from typed parts: statements (DR-0040),
  applicability (DR-0041), classifications (DR-0042), and the triad.
- AIS and vessel data enter as machine observations (§49) evidencing shipment
  legs, with spoofing risk handled by the scheme library (DR-0034).
