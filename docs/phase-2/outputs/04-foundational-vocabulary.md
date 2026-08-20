# Phase II Output 4 — Candidate Foundational Vocabulary

Seed concept set for the semantic registry (DR-0050), derived from adopted
standards — not ad hoc schema design. One line per concept; full registry
definitions follow on approval. Grouped by layer.

## Pipeline / preservation layer (OAIS, PREMIS, PROV — DR-0001…0009)

| Concept | Sketch | Grounding |
|---|---|---|
| source | An origin of material the project collects from (site, feed, channel, dataset, person) | §8; OAIS producer |
| capture | A preserved acquisition of source content at a time, with fixity | WARC/Memento; DR-0006/0018 |
| preserved object | Representation/file/bitstream under archival custody | PREMIS; DR-0002 |
| preservation event | Dated action on a preserved object, with agent and outcome | PREMIS; DR-0002 |
| pipeline agent | Person/organization/software acting on the archive or pipeline | PREMIS/PROV; DR-0004 |
| derivation | Entity-to-entity lineage via an activity | PROV; DR-0003 |
| fixity record | Digest + algorithm + date for an object or package | DR-0005 |
| package | BagIt-enveloped set of files with manifest | DR-0007 |
| evidence package | Package assembled from holdings for a consumer, manifest-carrying | §92; DR-0007 |

## World layer (CIDOC CRM — DR-0010, 0012…0015, 0044)

| Concept | Sketch | Grounding |
|---|---|---|
| entity (world) | Person, group, physical object, or place with stable identity | CRM E21/E74/E19/E53 |
| world event | Historical occurrence with participants, time-span, place | CRM E5/E7 |
| period phenomenon | Extended spatiotemporal happening (campaign, occupation) | CRM E4; DR-0044 |
| appellation | A name as an object, assigned by an event | CRM E41; DR-0012 |
| identifier (external) | Typed external ID assigned by an event, provenance-bearing | §16; DR-0012 |
| role tenure | Temporal membership/office with role qualification | DR-0013 |
| product type / individual item | Model identity vs serial-numbered individual | DR-0014 |
| territorial status | Typed temporal relation: sovereignty claim, recognition, administration, occupation, de facto control | DR-0044 |

## Documentary layer (LRMoo, Web Annotation — DR-0011, 0017…0023)

| Concept | Sketch | Grounding |
|---|---|---|
| Work / Expression / Manifestation / Item | The four-level documentary identity stack | LRMoo; DR-0011 |
| derivative expression | OCR, transcript, translation, excerpt with PROV lineage | DR-0011/0003 |
| annotation | Body + selector-refined target(s), version-pinned | DR-0017/0018 |
| quotation | Typed annotation carrying exact passage, locus, omissions, translation links | DR-0019 |
| holdings statement | What the archive possesses of a document (original…metadata-only) | §26 |
| source lifecycle state | Published/edited/deleted/… as documentary events evidenced by captures | §24; WP 0.2 §4.5 |
| post / account / thread relation | Social-media mapping onto the stack | DR-0023 |

## Epistemic layer (CRMinf + extensions — DR-0024…0031)

| Concept | Sketch | Grounding |
|---|---|---|
| proposition | Content that can be asserted, believed, supported, attacked | CRMinf I4 |
| documentary assertion | What a source says, adopted with attribution, anchored to passages | DR-0024 layer 2 |
| project assertion | Belief held by the project/analyst via visible inference | DR-0024 layer 4 |
| evidence relation | Claim-relative supports/contradicts/bears-on link | DR-0024 layer 3 |
| epistemic category | observation, claim, assessment, hypothesis, finding, project conclusion | DR-0025 |
| likelihood band | Calibrated verbal probability expression with numeric range | DR-0026 |
| analytic confidence | Low/moderate/high judgment strength from evidence, corroboration, reasoning | DR-0026 |
| source grade | Two-axis triage-only reliability × credibility grade | DR-0027 |
| dependence relation | Typed source-dependence link (cites, reposts, shares-witness…) | DR-0028 |
| absence state | unknown / not-researched / no-evidence-found / … | DR-0029 |
| quantity object | Value with original expression, semantic type, precision, derivation | DR-0030 |

## Argument layer (AIF pattern, schemes — DR-0032…0037)

| Concept | Sketch | Grounding |
|---|---|---|
| argument structure | Propositions + typed scheme applications (inference/conflict/preference) | DR-0032 |
| defeater | Rebutting / undercutting / undermining attack | DR-0033 |
| argument scheme | Reusable reasoning pattern with critical questions | DR-0034 |
| hypothesis set | Competing hypotheses for a question, with typed evidence relations | DR-0035 |

## Legal layer (WS6 — DR-0038…0045)

| Concept | Sketch | Grounding |
|---|---|---|
| sanctions regime | Program under an enabling authority in a jurisdiction | DR-0038 |
| legal instrument | Versioned legal text with effective periods and amendment lineage | DR-0038 |
| designation record | Documentary record of a listing act, distinct from the entity | DR-0039 |
| legal effect | Typed restriction attached by instrument to designation or category | DR-0038 |
| rule-derived applicability | Computed, versioned conclusion (50% rule, EU control) with path | DR-0041 |
| interest statement | Typed ownership/control statement (BODS pattern) | DR-0040 |
| classification assertion | Contextual product classification (system, jurisdiction, authority, period) | DR-0042 |
| authorization | License/general license/denial/revocation as a legal act | DR-0042 |
| transaction / shipment / payment | The three distinct trade event types | DR-0043 |

## Governance layer (WS7 — DR-0046…0052)

| Concept | Sketch | Grounding |
|---|---|---|
| governance document | REQ/POL/PROC/DR/SPEC/METH under document control | DR-0046 |
| document status | draft / proposed / approved / effective / superseded / withdrawn | DR-0046 |
| configuration item | Independently versioned artifact participating in baselines | DR-0047 |
| release baseline | Named frozen set of configuration-item versions + manifest | DR-0048 |
| registry entry | 11179-patterned data element / SKOS concept with stewardship and status | DR-0050 |
| requirement | Category-prefixed, verifiable, traceable statement of need | DR-0051 |
