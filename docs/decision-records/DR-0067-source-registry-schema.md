# DR-0067 — Source registry schema

**Category:** architecture / operations | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-14, SPEC-0003 §3 | **Supersedes:** — | **Superseded by:** —

## Context

Record §8 requires a configurable source list driving automated collection;
§9 makes collection policy source-specific; §12/§14 require access,
sensitivity, and rights dimensions; §36/DR-0028 require dependence to be
explicit where consequential.

## Alternatives considered

1. Registry entries carrying identity, context, collection policy,
   preservation policy, access/sensitivity defaults, rights, triage grade,
   declared dependence, and lifecycle (chosen).
2. Minimal URL list with per-item decisions (rejected: forces every policy
   judgment to be re-made per item).

## Decision

Collection is driven by a source registry whose entries carry the field
groups specified in SPEC-0003 §3: identity; context (jurisdiction, language,
coverage start); collection policy (method, cadence, scope, exclusions, rate
constraints); preservation policy (capture format per DR-0006, default
retention tier, fixity cadence); default access tier and sensitivity (§12);
rights assessment per §14 with `unknown` as an explicit value (DR-0029);
optional triage grade (**triage only**, DR-0027); **declared dependence** on
other sources (DR-0028); and lifecycle with outage history.

**Declared dependence at registry level** means known republishing and
syndication relationships are stated once and inherited as a dependence
hypothesis by every item, rather than rediscovered per article (§36).

## Consequences

- Per-source defaults make item-level decisions the exception.
- Corroboration analysis (DR-0028) starts from declared relationships.
- Registry entries are governance data: changes are recorded, not silent.
