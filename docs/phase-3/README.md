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
| 4 | ✅ Semantic-registry implementation — [SPEC-0004 v1.0 effective 2026-08-16](../specifications/SPEC-0004-semantic-registry.md); DR-0078…0081 enacted (Q-30 resolved) | Q-30 |
| 5 | ✅ Collection-pipeline architecture — [SPEC-0003 v1.0 effective 2026-08-16](../specifications/SPEC-0003-collection-pipeline.md); DR-0066…0071 enacted. Collection at scale remains gated on the personal-data policy (DR-0071, Q-35) | Q-25; LEGAL-009/Q-35 before scale-up |
| 6 | ✅ Storage & preservation layout — [WP 3.3](working-papers/wp-3.3-storage-preservation-layout.md); DR-0073…0077 enacted 2026-08-16 (Q-03 resolved; OCFL adopted, holding-as-object, dual digests, tier-separated roots, redaction as sole exception) | Q-03 |
| 7 | ✅ Likelihood-band scale — [WP 3.2](working-papers/wp-3.2-likelihood-band-scale.md); DR-0065 enacted 2026-08-16, ICD 203 canonical with PHIA mappings (Q-16 resolved, DR-0026 complete) | Q-16 |
| 8 | ✅ Requirements enactment — [ten REQ documents effective 2026-08-16](../requirements/README.md); DR-0082 enacted (73 requirements with completed verification criteria) | — |
| 9 | ✅ Personal data policy — [POL-0001 v1.0 effective 2026-08-16](../policies/POL-0001-personal-data.md); DR-0072 enacted (record §13, LEGAL-009, Q-35). **Collection-scope releases suspended pending external legal review** | Q-35 |
| 10 | 🟡 Foundational corpus acquisition strategy — [WP 3.4](working-papers/wp-3.4-foundational-corpus-acquisition.md) deposited 2026-09-08; CDR-P3-31…35 candidate. Founder ruling 2026-09-08: no collection scale-up before the POL-0001 §10 review is recorded; preparatory Track A proceeds under DR-0071. Track A item **A6 done 2026-09-15** — [the legal-review brief](../legal/legal-review-brief.md) v0.4, written against French law, all five of its founder decisions closed; CDR-P3-43 and 44 discharged into decision records, 45 held with a trigger; commissioning is a separate founder act | LEGAL-009 / Q-35 before Track B |
| 11 | ✅ Identifier design — [WP 3.5](working-papers/wp-3.5-identifier-design.md); DR-0087…0091 enacted 2026-09-09 (Q-12 resolved; ARK scheme, minting at publication, five-disposition register, `.vN` qualifiers, ARK-derived namespace); DR-0092 enacted the same day, ruled directly (split byline as a computed public title, never the agent's own id). [SPEC-0007 v0.4](../specifications/SPEC-0007-public-identifiers-and-resolution.md) drafted and **implemented** 2026-09-09 (`schema/08-identifiers.sql`, `identifiers/`, Gate 3 minting, tier rules; 77 checks). Candidate pending founder approval; a NAAN must be requested before anything can be minted | Q-12; SPEC-0005 §7 Q1 |
| 12 | 🟡 WACZ evaluation — [WP 3.6](working-papers/wp-3.6-wacz-evaluation.md) deposited 2026-09-15 (WP 3.4 Track A item A4); CDR-P3-42 candidate. Finding: the WACZ container format is stable (v1.1.1) but its signing layer is a pre-1.0 working draft (v0.1.0); recommends deferring adoption of both, WARC via `collector/pipeline.py` unchanged, on two stated revisit triggers | Q-04 (WP 0.2 §8, Phase II output 7); DR-0006's evaluation precondition |
| 13 | ✅ Registration classes — [WP 3.7](working-papers/wp-3.7-registration-classes.md) (WP 3.4 Track A item A5), design for CDR-P3-32 (deposited in WP 3.4 §8, 2026-09-08); enacted as [DR-0103](../decision-records/DR-0103-registration-classes.md). Authorization scale reduced from per-source (thousands) to per-class plus exceptions (tens); no schema change, merged values frozen at registration time. Implemented and tested (`sources/register.py`, `sources/tests/test_register_classes.py`, 18 checks). **Initial classes named 2026-09-17**: jurisdiction first, topic second (WP 3.7 §7's recommendation); six classes, all seven candidates wired (`sources/README.md`). Next: execution of the three pending A1 registrations on the archive server | CDR-P3-32 |
| 14 | 🟡 Incident / harm / person model for civilian harm and war crimes — [WP 3.8](working-papers/wp-3.8-civilian-harm-incident-model.md) (DR-0109 Consequence 5, issue #71); five candidate DRs named `CDR-P3-47…51`, numbered at merge. Design only: incident as a fact-free world-event with every fact an assertion; per-source counts with no default roll-up; a deliberately narrow person layer; SPEC-0002 reconciliation with spellings kept as data; a three-layer crime vocabulary with a `gated` marker and the record §63 legal lifecycle. All five candidates ruled option A on 2026-10-03 and enacted in `DR-0112` (named minors stay out until the founder or counsel rules) |
| 15 | 🟡 External place and period vocabularies (PLATO, PeriodO, HISTO) — [WP 3.9](working-papers/wp-3.9-external-place-and-period-vocabularies.md), a founder question of 2026-10-03; one candidate DR named `CDR-P3-52`, numbered CDR-P3-52 at merge. Evaluation only: PLATO is the nearest design reference for the future `place` entity but is an unstable draft; PeriodO holds authority-attributed period definitions, citable as an identifier and never as a definition; HISTO is not recommended. Recommends integrating none now. No schema or registry change |  |
| 16 | 🟡 The `place` and `period-phenomenon` entities — [WP 3.10](working-papers/wp-3.10-place-and-period-phenomenon-model.md) (build card #109, follow-on to WP 3.9); five candidate DRs `CDR-P3-53…57`, numbered at merge. Read PLATO's ontology (v0.9.0-alpha.1) and PeriodO's full dataset directly: PLATO's timespan rule turns out compatible with SPEC-0001; PeriodO holds nothing for 2014 onward, so no `periodo` identifier type is recommended. Proposes identity-only `place` and `period-phenomenon` with assertion families, and a control-area extent as a `place`. Design only: no schema or registry change |  |
| 17 | 🟡 Reaching Telegram without a single point of failure — [WP 3.11](working-papers/wp-3.11-telegram-egress-options.md), a founder question of 2026-10-07; three candidate DRs `CDR-P3-58…60`, numbered at merge. Evaluation and requirements only: compares a tunnel proxy, a fetch service, a Telegram data API, a second own address and doing nothing; finds the recorded single-address risk did not materialise in the worst case (both full backfills, 0 failures), so recommends no purchase now and a purchase on a named trigger, with eight requirements any egress service must meet (raw bytes unchanged, no circumvention of a refusal, no secret committed). No code, purchase or schema change. `CDR-P3-59` ruled option A on 2026-10-07 and enacted in `DR-0113` (no purchase until a named trigger); `CDR-P3-58` and `CDR-P3-60` unruled | CDR-P3-59 |

## Working conventions

Phase III working papers are numbered WP 3.x, live in
[working-papers/](working-papers/), carry AI-provenance blocks and SHA-256
deposits like Phase II papers, and produce candidate DRs for founder approval.
Specifications (SPEC class) come under DR-0046 document control.
