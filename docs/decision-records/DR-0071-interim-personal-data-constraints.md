# DR-0071 — Interim personal-data constraints

**Category:** legal / operations | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-18, SPEC-0003 §9 | **Supersedes:** — | **Superseded by:** — (self-lifting; see Decision)

## Context

Record §13 requires a formal personal-data policy — covering civilians,
victims, witnesses, minors, public officials, combatants, investigative
subjects, and sanctioned persons — **before broad automated collection**
(LEGAL-009, Q-35). That policy does not yet exist, but collection design is
proceeding.

## Alternatives considered

1. Bind concrete interim constraints that lift when the policy takes effect
   (chosen).
2. Draft the policy first and collect nothing until it is effective
   (rejected: blocks all collection, including from official and
   institutional sources where the personal-data question is minimal, while
   evidence disappears from the live web).
3. Rely on §13 as an abstract warning (rejected: an unoperationalized
   requirement is not a constraint).

## Decision

Until a personal-data POL document is effective, collection is bound to:

- **(a) Registered sources only** — explicitly registered in the source
  registry (DR-0067) with human-configured scope. No open-ended crawling, no
  bulk social-media harvesting.
- **(b) No automatic promotion of personal data into structured, searchable
  fields** beyond what a registered source's purpose requires. Raw material
  will inevitably contain personal data; the enrichment pipeline must not
  convert it into queryable structure automatically (§13).
- **(c) No third-party submission intake at scale** beyond individually
  handled cases.

These constraints **lift on the terms of the personal-data policy** when it
becomes effective — no superseding DR is required, though the policy must
state explicitly which constraints it releases.

## Consequences

- Collection can begin now against official, institutional, and documentary
  sources without waiting on the policy.
- The hardest personal-data judgments are deferred to the document designed
  to make them, rather than being made implicitly by collector code.
- The personal-data policy (Q-35) remains the gate on collection at scale
  and is founder-led work.
