# Phase II / Workstream 2 — Historical & Event Knowledge Concept Map
## Working Paper 0.3

**Project:** Ukraine's Second War of Independence
**Status:** CANDIDATE — AI-drafted, awaiting founder review and approval. Nothing in this paper is canonical.
**Version:** 0.3 (first draft of Workstream 2)
**Mandate:** WP 0.1 research sequence item 2 — deep study of CIDOC CRM, its extensions, and LRMoo for the historical/event knowledge layer (WP 0.1 layer C) and its boundary with documentary identity (layer D).
**Constraint inherited:** DR-0004 (pipeline/world layer boundary) governs this study.

### AI provenance (per Phase I record §80)

| Field | Value |
|---|---|
| Drafted by | AI assistant (Anthropic Claude Code agent session), at the founder's request |
| Date | 2026-08-10 |
| Inputs | Phase I record; WP 0.1; WP 0.2; DR-0001…0009; web verification of current model versions (sources at end) |
| Human review | **Pending** — founder is final editor (record §78) |
| Disposition | Candidate working paper; all candidate Decision Records herein are proposals |

---

## 1. Scope and method

This paper maps **CIDOC CRM** (community version 7.1.3; ISO 21127:2023), selected
**CRM-family extensions** (CRMinf, CRMsci, CRMdig, CRMgeo, CRMsoc), and **LRMoo 1.0**
(IFLA-endorsed April 2024, successor to FRBRoo) against the Phase I requirements for
the historical world layer: entities, identity, names, roles, organizations,
physical objects, events, time, place, and observations (record §16–§21, §45–§50),
and the documentary-identity requirements (§22–§23, §58).

As with Workstream 1: concepts, not tables. CIDOC CRM is studied as a *conceptual
reference model* — WP 0.1 and record §95 forbid equating it with the physical
schema, and this paper maintains that discipline.

## 2. Conceptual cores

### 2.1 CIDOC CRM 7.1.3 / ISO 21127:2023

An event-centric ontology from the museum/cultural-heritage world, ISO-standardized
since 2006 and renewed as ISO 21127:2023. Its central intuition matches the
project's needs precisely: **historical knowledge is knowledge of events** —
things happen; actors participate; objects, places, and time-spans are bound
together *through* events, not through static attributes.

Concepts that matter most here:

- **E5 Event / E7 Activity / E4 Period** — occurrences, intentional activities,
  and extended spatiotemporal phenomena (campaigns, occupations), with `P9 consists
  of` for parent/child structures (§47).
- **E39 Actor / E21 Person / E74 Group** — actors individual and collective.
- **E52 Time-Span** with **fuzzy boundaries** (`P81 ongoing throughout` /
  `P82 at some time within`) — native support for approximate dates and ranges
  (§45) without false precision (§42–43).
- **E53 Place** as *identity*, distinct from geometric expression (§46).
- **E41 Appellation / E42 Identifier** — names and identifiers as first-class
  objects, not string fields.
- **E15 Identifier Assignment / E13 Attribute Assignment** — the act of naming,
  identifying, or attributing is itself an **event with an actor and a time**.
  This is exactly record §16: "identifiers are provenance-bearing relationships,
  not merely timeless fields."
- **E85 Joining / E86 Leaving** — group membership as temporal events; with
  `P14.1 in the role of`, role-qualified participation (§18: roles are temporal
  relationships; acting capacity matters).
- **E12 Production, E9 Move, E8 Acquisition** — object lifecycle events (§21).
- **E99 Product Type vs E22 Human-Made Object** — the model/type vs individual
  physical item distinction of §21, ready-made.
- **E55 Type** — controlled-vocabulary typing throughout (§102).

### 2.2 CRM-family extensions

| Extension | Domain | Relevance |
|---|---|---|
| **CRMinf** | Argumentation & inference: I1 Argumentation, I2 Belief, I4 Proposition Set, belief adoption, inference making | Established candidate basis for the epistemic/argument layers (WP 0.1 F/G) — a major finding; study belongs to Workstreams 4–5 |
| **CRMsci** | Scientific observation: S4 Observation, S21 Measurement | §48–50 observations and derived measurements |
| **CRMdig** | Provenance of digitization/digital objects | Overlaps PROV/PREMIS territory — must be reconciled with DR-0003 mapping, not adopted blindly |
| **CRMgeo** | Spatiotemporal modeling: phenomenal vs declarative place | §46's identity-vs-geometry and uncertainty-of-location distinctions |
| **CRMsoc** | Social phenomena, rights, social bonds (draft status) | Possible home for social/legal relationships; maturity must be assessed |

### 2.3 LRMoo 1.0

The object-oriented formulation of IFLA LRM, endorsed April 2024, expressed as a
CIDOC CRM extension — which makes the documentary layer (D) and world layer (C)
natively compatible. Core stack:

- **F1 Work** — the intellectual creation as such;
- **F2 Expression** — a realization (a language version, an edition's text — and a
  *translation is a new expression*, matching §58's "translations are derived
  scholarly objects");
- **F3 Manifestation** — the published embodiment;
- **F5 Item** — the individual exemplar.

This is precisely the §22 requirement ("do not collapse all documentary layers
into 'a file'"), with creation/publication modeled as events carrying agents and
roles — supporting §23's stated-author / actual-author / signer / publisher /
issuing-authority distinctions.

## 3. Requirement-by-requirement mapping (world layer)

### 3.1 Identity, names, aliases (§17)

Multiple names, multilingual names, transliterations, historical names: all are
E41 Appellations linked by identified-by relations, each attachable to time-spans
and — critically — assignable via E15 events with actors and evidence. Candidate
matches vs confirmed matches vs rejected matches (§17) are *not* native CRM;
they belong to the entity-resolution layer, which can use E13/E15's reified-
assertion pattern as its grounding. Merge/split history (§17) likewise requires a
project vocabulary over the CRM base — flagged as a gap with a natural extension
point, not a contradiction.

### 3.2 Roles, offices, acting capacity (§18)

E85/E86 membership events + role-qualified participation (`P14.1`) cover tenure,
joining, leaving, and acting-in-capacity. Disputed and de facto roles are
representable as attribute assignments (E13) carrying their asserting source —
which aligns with §32's documentary-vs-world assertion split rather than deciding
it. Fit: strong, with the epistemic status of contested roles deferred to
Workstream 4.

### 3.3 Organizations and corporate identity (§19–20)

Formation, dissolution, renaming, membership: covered by E74/E66/E68 + naming
events. **Not covered:** legal ownership percentages, beneficial ownership, voting
rights, nominee arrangements, control networks (§19), and typed corporate
addresses (§20). This is the paper's most important negative finding: **CIDOC CRM
is not, and should not be forced to become, a corporate-registry or
ownership-network model.** That belongs to the sanctions/export-control layer
(Workstream 6), where purpose-built vocabularies (e.g. the OpenSanctions/
FollowTheMoney schema, corporate-registry models) must be studied. CRMsoc may
eventually carry some social/legal bonds; its draft status makes reliance
premature.

### 3.4 Physical objects (§21)

E22 individuals vs E99 product types; production, movement, acquisition,
part-decomposition events; serial numbers as E42 identifiers assigned by events.
Custody and seizure chains are event sequences. Fit: strong and direct.

### 3.5 Events, processes, campaigns (§47)

Bounded events (E5), activities (E7), extended processes and occupations (E4
Period), parent/child composition (`P9`), motivation links (`P17 was motivated
by`) and continuation. The §47 relation set (before/after/part_of/response_to/
continuation_of/same_underlying_event_as) maps onto CRM temporal and dependency
properties, with `same_underlying_event_as` handled by identity assertions —
again the entity-resolution pattern. Causation remains an assertion requiring
evidence (§47), never derivable from chronology: CRM's motivation property
expresses a *claim*, and the epistemic layer must carry its support.

### 3.6 Time (§45)

E52 Time-Spans with at-least/at-most bounds natively express approximate dates,
ranges, and open intervals. The multiple time dimensions of §45 (event time vs
publication vs acquisition vs legal-effective time) resolve cleanly under
DR-0004: event time lives here; acquisition/processing times live in the
pipeline layer (PROV/PREMIS); legal-effective time lives in the legal layer
(Workstream 6). Conflicting date assertions are competing attribute assignments —
carried, not averaged (§40).

### 3.7 Place (§46)

E53 Place = stable identity; geometries are expressions attached to it. CRMgeo's
phenomenal/declarative distinction covers "where it actually happened" vs "the
coordinates someone declared" — matching source-derived vs analyst-derived
locations. **Not covered:** sovereignty, occupation, administration, and de facto
control (§46) as political-legal relationships. Candidate approach: model these as
E4 Periods (an occupation *is* a spatiotemporal phenomenon) plus typed,
evidence-backed relationship assertions — with the precise vocabulary developed
jointly by Workstreams 2 and 6. Flagged open, not improvised here.

### 3.8 Observations and measurements (§48–50)

CRMsci S4 Observation / S21 Measurement give observations first-class standing
with observer, method, and time. Machine observations (§49) add
provider/precision/spoofing-risk metadata — project vocabulary over the CRMsci
base. Negative observation ("we did not observe X" ≠ "X was absent", §48) is an
epistemic matter: the observation event is recordable here; its evidential force
belongs to Workstream 4. Derived measurements chain to inputs via PROV (DR-0003)
— the two layers meet exactly as DR-0004 prescribes.

## 4. Documentary identity mapping (LRMoo)

- **§22 layer stack:** Work/Expression/Manifestation/Item maps one-to-one; OCR
  outputs, transcripts, translations, excerpts are derivative expressions with
  their own provenance (PROV, DR-0003).
- **§23 authorship:** creation events with typed roles distinguish drafter,
  signer, publisher, issuing authority; "signed by X ≠ written by X" is
  representable without strain.
- **§24 source lifecycle:** publication, withdrawal, replacement are events on
  manifestations — confirming WP 0.2 §4.5's boundary finding: lifecycle lives
  here (layer D), evidenced by captures (pipeline layer).
- **§26 holdings:** the archive's preserved copy is the bridge point: an LRMoo
  F5 Item (documentary identity) whose digital substance is a PREMIS
  representation (preservation identity). These are two views of one holding,
  linked but governed by different vocabularies — a boundary to fix explicitly
  in the semantic registry.
- **§58–59 translation/quotation:** translations as expressions; quotations
  target exact expression + locus — where **W3C Web Annotation** (WP 0.1 layer E)
  supplies the targeting vocabulary. Study deferred to Workstream 3 as planned.

## 5. Candidate conflict-register entries (additions)

| Term | Colliding senses | Resolution direction (candidate) |
|---|---|---|
| **work** | LRMoo F1 (intellectual creation) vs colloquial "work" vs "body of work" | Reserve "Work" (capitalized, F1 sense) in technical documents |
| **item** | LRMoo F5 (exemplar) vs PREMIS object/file vs colloquial | "Item" = documentary exemplar only; preserved digital substance = PREMIS vocabulary |
| **document** | CRM E31 Document (anything that documents) vs colloquial document | Qualify in registry; E31's breadth noted |
| **actor** | CRM E39 (world) vs pipeline agent (PROV/PREMIS) | Already fixed by DR-0004; registry cross-reference |
| **period** | CRM E4 (spatiotemporal phenomenon) vs colloquial time period | E4 sense includes the *happening*, not just the interval |
| **observation** | CRMsci S4 vs intelligence-analysis "observation" vs record §30 epistemic category | To be reconciled in Workstream 4 before the epistemic vocabulary freezes |

## 6. Gaps summary

1. **Entity resolution mechanics** (candidate/confirmed/rejected matches, merge/
   split lineage, §17) — CRM supplies the reified-assertion grounding (E13/E15);
   the resolution vocabulary itself is project/Workstream-4 work.
2. **Corporate ownership/control networks** (§19–20) — out of CRM scope by
   design; Workstream 6 with FollowTheMoney and registry models as study
   candidates.
3. **Sovereignty/occupation/control relations** (§46) — E4 Period grounding plus
   joint WS2/WS6 vocabulary; open.
4. **Quantitative assertion semantics** (§44: "at least 17") — not a CRM
   strength; belongs to the epistemic layer (WS4).
5. **Social-media-native structures** (§25: accounts, posts, forwards, threads)
   — accounts are appellations/identifiers of actors; posts are manifestations/
   expressions; forward/reply chains are documentary relations — a mapping to be
   made explicit in Workstream 3.
6. **CRMdig vs PROV/PREMIS overlap** — must be reconciled under DR-0003 rather
   than adopted in parallel.

## 7. Candidate Decision Records (proposals only — require founder approval)

- **CDR-W2-1:** Adopt CIDOC CRM (7.1.3 / ISO 21127:2023) **conceptually** as the
  reference model for the historical world layer — actors, events, objects,
  places, time-spans, appellations, identifiers — explicitly *not* as the physical
  schema (record §95 reserved to Phase III).
- **CDR-W2-2:** Adopt LRMoo 1.0 **conceptually** for documentary identity:
  Work / Expression / Manifestation / Item, with translations and other
  derivatives as expressions carrying PROV provenance.
- **CDR-W2-3:** Naming and identification are **events**: names, aliases, and
  external identifiers attach to entities via assignment events with actor, time,
  and evidence (E15/E13 pattern), satisfying record §16–17's provenance-bearing
  identity requirement.
- **CDR-W2-4:** Roles and memberships are **temporal events** (joining/leaving
  with role qualification), never mutable person attributes (record §18).
- **CDR-W2-5:** The **product-type vs individual-item** distinction (E99 vs E22
  pattern) is adopted for physical objects (record §21).
- **CDR-W2-6:** Corporate ownership/control networks and sovereignty/occupation
  relations are **explicitly out of scope for the CRM world layer** and assigned:
  ownership/control → Workstream 6 (sanctions/legal layer, with FollowTheMoney
  and corporate-registry models as mandatory study items); sovereignty/occupation
  → joint WS2/WS6 vocabulary grounded in E4 Period.
- **CDR-W2-7:** **CRMinf becomes the starting candidate** (not an adoption) for
  the epistemic/argumentation layers; Workstreams 4–5 must evaluate it against
  intelligence-analysis and legal-evidence requirements before any commitment.

## 8. Unresolved research questions (feed Phase II output 7)

1. Which CRM extension subset (CRMsci, CRMgeo, CRMdig, CRMsoc) earns adoption,
   and how is CRMdig reconciled with DR-0003's PROV/PREMIS mapping?
2. How exactly do LRMoo F5 Items and PREMIS representations link for a single
   preserved holding (one bridge relation? registry rule?)?
3. Can CRMinf carry the record's epistemic vocabulary (§30: observation, claim,
   assessment, hypothesis, finding, conclusion) without distortion? (WS4)
4. What is the entity-resolution vocabulary (candidate/confirmed/rejected match,
   merge/split lineage) over the E13/E15 grounding? (WS4, with §72 sanctions
   identity as the hard test case)
5. Sovereignty/occupation/de facto control: period-based, relation-based, or
   both? (WS2+WS6)
6. Is CRMsoc mature enough to matter, or is it watched and deferred?
7. How are §25's social-media structural relations (reply, forward, thread)
   expressed in the LRMoo/Web-Annotation frame? (WS3)

## 9. Sources

- CIDOC CRM: [cidoc-crm.org](https://cidoc-crm.org/) — [version 7.1.3](https://cidoc-crm.org/Version/version-7.1.3); [ISO 21127:2023 release note](https://cidoc-crm.org/Event/iso-211272023-has-been-released)
- LRMoo: [LRMoo 1.0 definition (PDF)](https://cidoc-crm.org/sites/default/files/LRMoo_V1.0.pdf); [IFLA endorsement announcement](https://www.ifla.org/news/newly-available-object-oriented-lrm-conceptual-model/); [LRMoo home](https://cidoc-crm.org/lrmoo)
- CRM family extensions: CRMinf, CRMsci, CRMdig, CRMgeo, CRMsoc pages at cidoc-crm.org
