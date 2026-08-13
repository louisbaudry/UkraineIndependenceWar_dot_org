# DR-0032 — Argument representation: CRMinf grounding with AIF-patterned structure

**Category:** epistemology / architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W5-1, WP 0.6 §3/§6 | **Supersedes:** — | **Superseded by:** —

## Context

DR-0031 grounded the argument layer in CRMinf argumentation/inference activities
and deferred the internal structure. WP 0.6 surveyed the argumentation field;
AIF (Argument Interchange Format) is its established interchange ontology.

## Alternatives considered

1. CRMinf activities carrying AIF-patterned structure, mapped to AIF for
   interchange (chosen).
2. Bespoke argument graph model (rejected: §94; AIF exists).
3. Raw AIF without CRMinf grounding (rejected: loses agent/time/provenance
   integration with the adopted stack).

## Decision

Arguments are represented as **CRMinf argumentation/inference activities whose
content follows the AIF pattern**: propositions (information nodes) connected by
typed scheme applications — inference (support), conflict (attack), preference
(priority). The structure **maps to AIF** for interchange and evidence-package
export; it is not reinvented.

## Consequences

- Argument structures carry agents, time, and provenance like every other
  activity (DR-0003, DR-0031).
- Export of reasoning in evidence packages (DR-0007) has a standard target.
- Defeater typing (DR-0033) and schemes (DR-0034) plug into the conflict and
  inference application slots respectively.
