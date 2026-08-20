# DR-0031 — CRMinf adopted as epistemic reification grounding, with extensions

**Category:** epistemology / architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W4-8, WP 0.5 §4/§10 | **Supersedes:** — (fulfills the evaluation ordered by DR-0016) | **Superseded by:** —

## Context

DR-0016 designated CRMinf the starting candidate for the epistemic layer and
ordered its evaluation against the record's requirements. WP 0.5 §4 performed
the evaluation: the reification core matches; five gaps were identified, all
bounded and extensible.

## Alternatives considered

1. Adopt CRMinf as grounding + named project extensions (chosen).
2. Reject CRMinf, design a bespoke assertion model (rejected: the core match is
   genuine; §94).
3. Full CRMinf adoption without extensions (rejected: leaves §36, §41, §42, §44
   unserved).

## Decision

**CRMinf is adopted conceptually** as the reification grounding of the epistemic
layer: beliefs held by agents over time (I2), proposition sets (I4), inference
making with visible premises (I5), belief adoption for documentary assertions
entering the graph (I7), argumentation activities (I1) as the bridge to the
argument layer.

**Five project extensions** are adopted alongside it, as specified by WP 0.5
and enacted in DR-0026…0030: calibrated likelihood/confidence vocabulary,
typed source-dependence relations, quantitative-assertion semantics,
absence-state vocabulary, and explicit negative propositions with provenance.

The **argumentation formalism** (structure inside I1: schemes, defeaters,
hypothesis matrices) is deferred to Workstream 5.

## Consequences

- The epistemic layer composes natively with the CRM world layer (DR-0010),
  LRMoo documents (DR-0011), and annotation targeting (DR-0017/0018).
- AI-proposed assertions (§79–80) are beliefs held by a software agent until
  adopted under human accountability — the accountability rule becomes
  structurally expressible.
- DR-0016's evaluation obligation is discharged.
