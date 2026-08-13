# Phase II Output 7 — Unresolved Research Questions (candidate, consolidated)

Consolidated and deduplicated from WP 0.2–0.8. Questions resolved during
Phase II are listed at the end for the record. **"Blocks"** marks what the
question gates.

## The Phase III entry question

| ID | Question | Origin | Blocks |
|---|---|---|---|
| Q-01 | **Canonical representation:** relational-first, RDF/OWL-first, layered, or other — decided against actual requirements (§95) | Record §95; WP 0.1 | All Phase III schema/storage work |

## Preservation & storage

| ID | Question | Origin | Blocks |
|---|---|---|---|
| Q-02 | Which PREMIS subset does the project actually implement? | WP 0.2 Q1 | Phase III preservation schema |
| Q-03 | Does OCFL implement or conflict with the immutability rule? | WP 0.2 Q5 | Storage layout choice |
| Q-04 | Is WACZ signing mature and jurisdictionally meaningful for evidentiary packaging? | WP 0.2 Q4 | Capture toolchain freeze (DR-0006) |
| Q-05 | Which ISO 16363 subset is meaningful for a single-editor project, and when does self-assessment start? | WP 0.2 Q7 | Succession readiness |
| Q-06 | Site-snapshot mechanics: WARC of own site vs static-build archive | WP 0.8 Q5 | First public release (DR-0052) |

## World & documentary layers

| ID | Question | Origin | Blocks |
|---|---|---|---|
| Q-07 | One agent registry with roles, or two registries with links? | WP 0.3 Q2 (as constrained by DR-0004) | Phase III identity design |
| Q-08 | Which CRM extensions (CRMsci/CRMgeo/CRMdig/CRMsoc) earn adoption; CRMdig reconciled with PROV/PREMIS | WP 0.3 Q1 | Phase III world-layer detail |
| Q-09 | The LRMoo Item ↔ PREMIS representation bridge rule for one preserved holding | WP 0.3 Q2 / WP 0.4 | Registry entry; Phase III |
| Q-10 | Entity-resolution vocabulary (candidate/confirmed/rejected, merge/split lineage) over the E13/E15 grounding, tested on §72 sanctions identity | WP 0.3 Q4 | Phase III identity workflows |
| Q-11 | Sovereignty/occupation detail: period-based, relation-based, or both, per case | WP 0.3 Q5 / DR-0044 | Registry refinement |
| Q-12 | Annotation identity/storage: are annotations independently citable objects, and via what resolver? | WP 0.4 Q1 | §15 identifier design (Phase III) |
| Q-13 | Minimal TEI subset, and which corpus first triggers deep encoding | WP 0.4 Q2 | First critical edition (DR-0020) |
| Q-14 | Translation alignment granularity (sentence, passage, ad hoc) | WP 0.4 Q3 | Parallel-text tooling |
| Q-15 | Restricted media: IIIF under access control vs simpler internal region model | WP 0.4 Q4 | Media platform (DR-0021) |

## Epistemics & argumentation

| ID | Question | Origin | Blocks |
|---|---|---|---|
| Q-16 | Exact likelihood-band boundaries and wording (ICD 203 vs PHIA vs hybrid), plus multilingual renderings | WP 0.5 Q1 | Vocabulary-enactment DR (DR-0026) |
| Q-17 | Does the project ever compute Bayesian posteriors, or remain verbal-band only? | WP 0.5 Q3 / WP 0.6 Q4 | Revisit at first quantitative investigation |
| Q-18 | Who may set which epistemic status — risk-tiered editorial roles applied to statuses | WP 0.5 Q5 | POL/PROC drafting |
| Q-19 | Coverage-aware negative observation for machine sources ("looked and didn't see") | WP 0.5 Q6 | Sensor-data modeling |
| Q-20 | Initial argument-scheme contents and critical-question sets | WP 0.6 Q1 / DR-0034 | METH drafting; first investigations |
| Q-21 | Inference reification granularity — candidate rule: review tier determines required depth | WP 0.6 Q2 | PROC drafting |
| Q-22 | Is propaganda-narrative variant analysis (§54) an argument pattern or a documentary pattern? | WP 0.4 Q6 / WP 0.6 Q5 | Test on real cases |
| Q-23 | Whether evidential annotations are themselves assertions with epistemic status | WP 0.4 Q5 | Registry entry |

## Legal layer

| ID | Question | Origin | Blocks |
|---|---|---|---|
| Q-24 | Jurisdiction sequencing beyond UN/EU/US/UK (Switzerland and others) | WP 0.7 Q1 | Collection policy (§9) |
| Q-25 | Instrument-text collectors (OJ EU, Federal Register, legislation.gov.uk) | WP 0.7 Q2 | Phase III pipeline |
| Q-26 | Enforcement-action modeling depth at start (first-class vs documentary-only) | WP 0.7 Q3 | Phase III legal-layer scope |
| Q-27 | Cryptocurrency flows: confirm deferral until investigations require (§70) | WP 0.7 Q4 | — (deliberate deferral) |
| Q-28 | FtM export-loss documentation per package type | WP 0.7 Q5 / DR-0045 | First FtM export |
| Q-29 | AIS/vessel spoofing scheme and critical questions | WP 0.7 Q6 | Scheme library (Q-20) |

## Governance & operations

| ID | Question | Origin | Blocks |
|---|---|---|---|
| Q-30 | Registry tooling: files in Git vs a small registry service | WP 0.8 Q1 | Phase III |
| Q-31 | DOI registration route and timing | WP 0.8 Q2 / DR-0049 | Operational decision at maturity |
| Q-32 | Machine-readable change-set format | WP 0.8 Q3 | First data release |
| Q-33 | METH sub-versioning for investigation-specific methods | WP 0.8 Q4 | Methodology growth |
| Q-34 | TBX adoption trigger | WP 0.8 Q6 | First professional translation |
| Q-35 | Personal-data policy content (§13) — required before broad automated collection | Record §13; LEGAL-009 | Collection scale-up |

## Resolved during Phase II (for the record)

| Original question | Resolution |
|---|---|
| WP 0.3 Q7 — social-media structural mapping | DR-0023 |
| WP 0.3 Q3 — can CRMinf carry the epistemic vocabulary | DR-0031 (yes, with five extensions) |
| WP 0.5 Q2 — ACH representation | DR-0035 (derived views) |
| WP 0.5 Q4 — assessment versioning mechanics | DR-0048 (append under baseline discipline) |
| WP 0.6 Q3 — Dung checking as aid | DR-0036 (permitted as aid only; implementation timing open) |
| WP 0.2 Q2 / WP 0.3 — agent registries | Narrowed by DR-0004 to Q-07 (semantic separation fixed; storage design open) |
| WP 0.2 Q3 — where source-lifecycle states live | WP 0.2 §4.5 / DR-0011 (documentary layer, evidenced by captures) |
| WP 0.2 Q6 — PROV bundles vs release manifests | DR-0048 (manifests carry PROV; bundles available within) |
