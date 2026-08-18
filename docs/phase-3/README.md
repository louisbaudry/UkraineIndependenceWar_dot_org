# Phase III — Conceptual Architecture

**Status:** Open — authorized 2026-08-16 by [DR-0053](../decision-records/DR-0053-phase-2-closure.md)
**Inherits:** DR-0001…0053, the approved Phase II outputs, document control (DR-0046), and the provenance discipline unchanged.

## Mandate

Turn the Phase II conceptual commitments into an implementable architecture —
without violating any enacted DR, and answering the open questions that gate
design (see [Phase II output 7](../phase-2/outputs/07-open-questions.md)).

## Entry question

**Q-01 — Canonical representation** (record §95): relational-first,
RDF/OWL-first, layered, or another model — decided by an architecture study
against actual requirements, "not because one technology sounds more
sophisticated."

## Planned studies and specifications (sequence, adjustable)

| # | Item | Gates |
|---|---|---|
| 1 | ✅ Canonical-representation study ([WP 3.1](working-papers/wp-3.1-canonical-representation-study.md)) — DR-0054…0058 enacted 2026-08-16 | Everything below |
| 2 | ✅ Conceptual data model — [SPEC-0001 v1.0 effective 2026-08-16](../specifications/SPEC-0001-conceptual-data-model.md); DR-0059…0061 enacted (Q-02, Q-07, Q-09 resolved) | Q-02, Q-07, Q-09 |
| 3 | ✅ Identity & entity-resolution workflow — [SPEC-0002 v1.0 effective 2026-08-16](../specifications/SPEC-0002-identity-entity-resolution.md); DR-0062…0064 enacted (Q-10 resolved) | Q-10 |
| 4 | Semantic-registry implementation (DR-0050) | Q-30 |
| 5 | ✅ Collection-pipeline architecture — [SPEC-0003 v1.0 effective 2026-08-16](../specifications/SPEC-0003-collection-pipeline.md); DR-0066…0071 enacted. Collection at scale remains gated on the personal-data policy (DR-0071, Q-35) | Q-25; LEGAL-009/Q-35 before scale-up |
| 6 | Storage & preservation layout (OCFL evaluation) | Q-03 |
| 7 | ✅ Likelihood-band scale — [WP 3.2](working-papers/wp-3.2-likelihood-band-scale.md); DR-0065 enacted 2026-08-16, ICD 203 canonical with PHIA mappings (Q-16 resolved, DR-0026 complete) | Q-16 |
| 8 | Requirements enactment as REQ-class documents (DR-0051) | — |

## Working conventions

Phase III working papers are numbered WP 3.x, live in
[working-papers/](working-papers/), carry AI-provenance blocks and SHA-256
deposits like Phase II papers, and produce candidate DRs for founder approval.
Specifications (SPEC class) come under DR-0046 document control.
