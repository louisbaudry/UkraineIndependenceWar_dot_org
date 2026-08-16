# DR-0063 — Match lifecycle and tiered confirmation

**Category:** architecture / methodology | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-10, SPEC-0002 §3–4 | **Supersedes:** — | **Superseded by:** —

## Context

Record §72: a sanctions-list identity must never be linked to a canonical
entity through fuzzy name matching alone. DATA-002: false merges are
costlier than missed matches. AI-001: AI never becomes canonical silently.

## Alternatives considered

1. Proposed→reviewed lifecycle with tiered human confirmation and a
   name-only prohibition (chosen).
2. Score-threshold auto-confirmation (rejected: violates §72 and AI-001 at
   the exact point of highest risk).
3. Per-item human review for everything including routine bibliographic
   identity (rejected: T3 batch confirmation preserves safety where stakes
   are low; per-item everywhere doesn't scale to a single-editor project).

## Decision

Match assertions follow the lifecycle **proposed → under-review → confirmed
| rejected (| withdrawn)** with SPEC-0002 §3's rules: automated matchers and
AI create `proposed` matches only, recording their feature basis; human
confirmation requires **discriminating evidence beyond name/transliteration
similarity — name similarity alone never confirms, at any tier**; rejections
are permanent, consultable records that matchers must consult. Confirmation
happens at the subject's review tier (SPEC-0002 §4): **T1** for
designation-record mappings and legal-layer identities (recorded review,
evidence-independence considered per DR-0028), **T2** for consequential
world actors and cross-registry links, **T3** batch-wise for routine
bibliographic and gazetteer identity.

## Consequences

- §72 and DATA-002 are mechanical properties of the workflow, not editorial
  aspirations.
- The tier table is the future team's identity rulebook (§78 applied).
- T3 batch audit sampling is an open POL/PROC item (SPEC-0002 §6 Q2).
