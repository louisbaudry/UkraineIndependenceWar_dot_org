# DR-0054 — Layered canonical representation

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-1, WP 3.1 §3–4 | **Supersedes:** — (answers record §95 / Q-01) | **Superseded by:** —

## Context

Record §95 required an architecture study comparing relational-first,
RDF/OWL-first, layered, and other canonical-representation models against
actual requirements. WP 3.1 derived eight requirement demands from
DR-0001…0053 and evaluated four models against them.

## Alternatives considered

1. Layered: relational canonical + derived projections (chosen).
2. RDF/OWL-first (rejected: statement-level provenance is RDF's weak point;
   no standard bitemporality; open-world semantics vs closed-world
   validation; thin operational base for a decades-horizon single-founder
   project; its distinctive payoff — reasoning — is constrained by DR-0036).
3. Property-graph-first (rejected: no standards alignment; vendor risk;
   traversal needs are bounded and served by projections).
4. Document/event-store canonical (rejected: validation and integrity land on
   application code; the append-only *discipline* is kept without the
   product).

## Decision

The canonical representation is **layered**: a **relational,
assertion-centric canonical store** holds all canonical knowledge; every
semantic (RDF under the adopted ontologies), interchange (FtM, BODS, DCAT),
search, graph-analysis, and publication surface is a **derived, rebuildable
projection** whose generator is versioned (DR-0047) and provenance-recorded
(DR-0003). Principle 18 generalizes: everything outside the canonical store
is a projection of it.

## Consequences

- Record §95 / Q-01 is answered; Phase III design work is unblocked.
- OWL reasoning never sits in the canonical path; a graph database remains
  possible later as a projection (WP 3.1 §5 Q3).
- Projection-mapping obligations are governed by DR-0056.
