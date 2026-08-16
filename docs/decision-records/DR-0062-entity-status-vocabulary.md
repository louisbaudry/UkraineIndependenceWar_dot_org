# DR-0062 — Entity-status vocabulary

**Category:** architecture / epistemology | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-9, SPEC-0002 §2 | **Supersedes:** — | **Superseded by:** —

## Context

Record §17 requires that fabricated entities, impersonations, and disproved
identities eventually be representable; entity resolution (Q-10) needs a
status model distinguishing settled referents from provisional clusters.

## Alternatives considered

1. Four statuses: canonical / candidate / fabricated / disproved (chosen).
2. Canonical/candidate only (rejected: leaves impersonation and duplicate
   history unrepresentable).
3. Defer until real cases (rejected: the propaganda corpus makes fabricated
   personas an early, not late, need).

## Decision

Every world-layer entity carries one registry-governed status: **canonical**
(treated as a real, distinct referent), **candidate** (provisionally
distinct, not yet consolidated), **fabricated** (concluded never to have
referred to a real distinct referent — invented persona, sockpuppet
identity), **disproved** (shown to be a duplicate or error, superseded via
merge/split lineage). **Fabricated and disproved entities are preserved as
referents, never deleted** — claims about them exist and remain citable
(§17, §54).

## Consequences

- Status changes are assertions with evidence (a "this persona is
  fabricated" conclusion is a project assertion under DR-0024).
- Impersonation analysis links a fabricated identity to the real person it
  imitates without merging them.
