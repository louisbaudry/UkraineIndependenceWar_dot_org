# DR-0064 — Merge/split as lineage events with reviewed re-homing

**Category:** architecture / preservation | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-11, SPEC-0002 §5 | **Supersedes:** — | **Superseded by:** —

## Context

Record §17 requires merge history, split history, and identity lineage.
After a false merge is discovered, some attached assertions belonged only to
the error — recovery must not propagate it.

## Alternatives considered

1. Lineage events with explicitly reviewed re-homing and permanent redirects
   (chosen).
2. Bulk re-homing with sampling review (rejected: the dangerous minority of
   assertions is exactly what sampling misses; volume is expected to be low
   enough for explicit review).
3. In-place entity rewriting (rejected: destroys lineage; violates DR-0055).

## Decision

**Merge** and **split** are events: they create/designate successor
entities, mark predecessors per DR-0062, and leave **permanent redirects**
so every published identifier keeps resolving (§15) — a split's redirect
resolves to a disambiguation record. Every assertion attached to a
predecessor is **explicitly re-pointed or flagged by review — never silently
bulk-moved**. Lineage is permanently queryable ("what merges/splits produced
me, decided by whom, on what evidence"), and merge/split mappings ship in
release change sets (DR-0048, §91).

## Consequences

- False-merge recovery is a governed operation with an audit trail.
- Citations into merged/split entities never dead-end.
- Release consumers can mechanically follow identity changes between
  versions.
