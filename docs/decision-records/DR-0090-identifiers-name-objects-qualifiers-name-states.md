# DR-0090 — Identifiers name objects; `.vN` qualifiers name states

**Category:** architecture / preservation | **Status:** Approved | **Decided:** 2026-09-09 by founder/principal editor
**Origin:** CDR-P3-34, [WP 3.4](../phase-3/working-papers/wp-3.4-identifier-design.md) §3.7, §5 rule 4 | **Supersedes:** — | **Superseded by:** —

## Context

The canonical store is append-only (DR-0055), so every object has a
current state at the head of a supersession chain, and the Phase I record
warns that "the same URL may later serve different content". Pages already
keep numbered revisions (`page_revision`) and preserved holdings keep OCFL
versions (DR-0073). §77's correction trail and DR-0048's release baselines
both need a citation that points at what the project said on a given date.

## Alternatives considered

1. **One ARK per object; a `.vN` qualifier for an explicitly versioned
   state** (chosen).
2. One ARK per state (rejected: the register grows with every edit,
   citations of "the page" fragment across identifiers, and merge/split
   redirects multiply).
3. Object ARK only, no state citation (rejected: cannot cite what the
   project said on a given date).

## Decision

1. **An ARK names the object across all its states.** The bare ARK
   resolves to the object's current state with links to its history.
2. **An explicitly versioned thing is cited as the same ARK with a `.vN`
   qualifier** — page revision N, OCFL holding version N — using the ARK
   draft's own `.` variant syntax. Qualifiers are resolved by the
   project's resolver; they are not separate register entries.
3. The resolver **may additionally offer Memento datetime negotiation**
   (RFC 7089) over `page_revision` and the bitemporal `asserted_at`
   column. That is implementation, not identity (WP 3.4 §8 Q5).

## Consequences

- Citations remain stable across corrections while still able to pin a
  state, which §77 and DR-0048 require.
- SPEC-0007 fixes the qualifier grammar and which classes are "explicitly
  versioned".
- A merge or split redirects the object ARK; qualified citations of a
  predecessor's states resolve through the same redirect to the lineage
  explanation (DR-0064).
