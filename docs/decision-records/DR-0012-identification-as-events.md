# DR-0012 — Names and identifiers attach via assignment events

**Category:** architecture / epistemology | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W2-3, WP 0.3 §7 | **Supersedes:** — | **Superseded by:** —

## Context

Record §16: "Identifiers are provenance-bearing relationships, not merely
timeless fields." §17 requires aliases, transliterations, historical names,
candidate/confirmed/rejected matches, and merge/split lineage. §72 makes
sanctions-designation identity the hard case: never linked by fuzzy name match
alone.

## Alternatives considered

1. Assignment-as-event pattern (E15 Identifier Assignment / E13 Attribute
   Assignment) (chosen).
2. Name/ID columns on entities (rejected: destroys provenance and temporality).
3. Names as separate records but without assignment provenance (rejected: keeps
   multiplicity, loses who-says-so).

## Decision

Names, aliases, and external identifiers (Wikidata, OpenSanctions, registry
numbers, IMO/MMSI, …) attach to entities via **assignment events** carrying
actor, time, basis/evidence, and status. Candidate, confirmed, and rejected
identity matches are all recordable as assertions with provenance; false merges
remain costlier than missed matches (§16), so confirmation requires evidence,
not string similarity.

The full entity-resolution vocabulary (merge/split lineage, §17) is developed in
Workstream 4 on this grounding.

## Consequences

- No bare `name` or `external_id` field ever carries canonical identity.
- Sanctions-designation→entity mapping (§72) inherits this rule automatically.
- Identity assertions become subject to the same epistemic treatment as any
  other assertion (Workstream 4).
