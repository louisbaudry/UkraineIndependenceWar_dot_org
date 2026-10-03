# Phase III / Study 9 — External Place and Period Vocabularies: PLATO, PeriodO and HISTO
## Working Paper 3.9

**Project:** Ukraine's Second War of Independence
**Status:** CANDIDATE — AI-drafted, awaiting founder review.
**Version:** 3.9 (draft 0.1)
**Mandate:** founder question of 2026-10-03 — whether the archive should integrate HISTO (Aalto University's Semantic Computing Research Group), PeriodO, and/or the World Historical Gazetteer's PLATO ontology; the founder asked for a short evaluation mapped against SPEC-0001 (option 2 of three put to the founder: do nothing now / this paper / a decision record). No issue card exists yet; one is needed before a build step follows (§7).
**Constraints inherited:** DR-0010 and DR-0012 (CIDOC-CRM world layer; identifiers and names as assertions); DR-0044 (territorial status as typed relations on period phenomena); DR-0045 (external identifiers); DR-0080 (registry process for open vocabularies); DR-0004 (nothing external becomes a project assertion by being cited); SPEC-0001 §2.1, §4; SPEC-0002 (identifier agreement never confirms identity on its own); WP 3.5 §2.3 (external identifiers are opaque and issuer-scoped).

### AI provenance (record §80)

Drafted 2026-10-03 by an AI assistant (Anthropic Claude Code agent session) at the founder's direction. **What was checked:** the repository's own text (SPEC-0001, SPEC-0002, DR-0044, `registry/vocabularies/identifier-types.yaml`, WP 3.5 §2.3, WP 3.8 §2); and, by web search and page fetch on 2026-10-03, the PLATO repository README, its Zenodo record and its v0.7.1 release notes, the HISTO page and project summaries at Aalto SeCo, and PeriodO's technical overview and project pages. The fetches returned summaries produced by a small model, not the primary files. **What was not checked:** PLATO's ontology file itself (so its exact timespan properties, its handling of uncertainty and any CIDOC-CRM alignment are **unknown**, not absent); HISTO's licence and its serialisation; PeriodO's licence on the live site (a secondary source states CC0) and whether it holds any period relevant to this archive. No source, person or incident was looked at. Candidate until the founder rules; **design only: no schema or registry change follows from this paper.**

---

## 1. The question

Three external resources deal with history and could be adopted, mapped to, or cited. This paper asks of each: what does it model, does it overlap what the archive already models, and is there a point in the build where it would be needed. It reads them against SPEC-0001, which already names `place`, `world-event` and `period-phenomenon` as world-layer entities and gives every assertion family a `valid_time` with approximations (§2.1).

## 2. What the archive already has

- **Entities carry no facts.** Names and identifiers are assertion families (`appellation-assignment`, `identifier-assignment`, SPEC-0001 §2.2, DR-0012). So any external vocabulary can only enter as an assertion with an asserter and a basis, never as a field.
- **Time.** `valid_time` is a span with at-least/at-most bounds on each end, possibly open (§2.1, DR-0010's E52 pattern), separate from `asserted_at`.
- **Periods are happenings.** A `period-phenomenon` is a CRM E4 spatiotemporal phenomenon (an occupation, a campaign), not an interval label (Phase II conflict C-11; DR-0044).
- **External identifiers.** `registry/vocabularies/identifier-types.yaml` is an open vocabulary governed by DR-0080. It lists `wikidata` and no gazetteer or period authority. SPEC-0002 already rates "places with authoritative gazetteer IDs" as tier T3 (batch confirmation, one strong shared identifier suffices).
- **Not built.** `place`, `world-event` and `period-phenomenon` have no DDL (WP 3.8 §2). Nothing today needs an external place or period vocabulary.

## 3. PLATO (Place Attestation Ontology)

**What it is.** An OWL ontology from the World Historical Gazetteer and the Pelagios Network Place Working Group (author given as Stephen Gadd), formalising WHG's v4 data model. The unit is the **Attestation**, a bundle linking a `SpatialEntity` to a `Name`, `Geometry`, `Timespan`, `Type`, `PropertyValue` and/or `Source` through properties such as `attests_about`, `attests_name`, `attests_timespan`, `sourced_by` and `has_citation`. `Authority` is an abstract class with subtypes including `Source`, `Dataset`, `Period`, `RelationType` and `CertaintyLevel`. The Linked Places Format (LPF) is defined as its single-object-attestation profile. Licence CC BY 4.0. It describes itself as an "early draft, published for discussion and review, not yet stable".

**Version discrepancy, unresolved.** The Zenodo record read as version 0.5.0 (28 September 2026); the GitHub release page read as 0.7.1 (30 September 2026). Both dates are days old. Whichever is current, the ontology is moving fast.

**Fit with SPEC-0001.**

| PLATO | Archive | Reading |
|---|---|---|
| `SpatialEntity` as a stable identity that attestations converge on | `place` with no facts of its own (§2.2) | Same idea. |
| `Attestation` bundling name, geometry, timespan, type, source | an assertion family sharing the §2.1 core (`subject`, `content`, `valid_time`, `asserter`, `basis`) | Close in spirit; PLATO bundles several facets in one node where the archive uses one family per kind of fact. A mapping is possible; a wholesale adoption would be a different granularity. |
| `Timespan` "with start/end bounds and precision metadata" | `valid_time` with at-least/at-most bounds | Probably compatible; **cannot be confirmed** without the ontology file. |
| "An attestation's timespan is no wider than its source can witness" (v0.7.1 notes) | `valid_time` is the world-time of the thing asserted, not of the source | **A real difference to resolve:** it bounds the timespan by what the source can witness, which blends world-time and evidence-time that SPEC-0001 keeps apart. |
| `CertaintyLevel` as an Authority subtype | likelihood bands and confidence (DR-0026, DR-0065), kept separate | Not described in what was read. It must not be read as a substitute for either. |
| `Period` as an Authority subtype | `period-phenomenon` | Not described in what was read; whether it points to PeriodO is **unknown**. |
| `RelationType` | `territorial-status` and other typed relations (DR-0044) | Would matter for a territory-over-time model; unverified. |

**Reading.** PLATO is the closest of the three to the archive's own pattern and the most useful *design reference* for how a gazetteer expresses attested names, geometries and dates. It is too young to bind to, and the one concrete semantic difference found (the timespan rule) shows a mapping is not mechanical.

## 4. PeriodO

**What it is.** A public-domain gazetteer of scholarly period definitions led by Adam Rabinowitz and Ryan Shaw, with Patrick Golden as lead developer. An **authority** (a source) is a `skos:ConceptScheme`; each **period** is a `skos:Concept` defined by that authority, with a start and a stop given both as text and as structured years (`periodo:earliestYear`, `periodo:latestYear`), a spatial coverage (text, plus `dcterms:spatial` links to gazetteers such as Wikidata, GeoNames and Pleiades), and an ARK identifier. Editorial history is published with PROV. The whole dataset is one JSON-LD download. A secondary source gives CC0.

**Fit with SPEC-0001.**

- It does **not** model a period as a happening. A PeriodO period is a *definition by an authority*: "source S says period P ran from A to B over region R". That is a documentary assertion about a label, the same shape as the archive's `documentary-assertion` (what a source says, never the project's own conclusion).
- That makes it a good match for citing, and a poor match for `period-phenomenon`. Competing definitions of the same label coexist, which fits §40's coexistence of competing characterisations.
- It uses ARKs, as the archive does (WP 3.5), so the identifier style is familiar.

**Coverage, not verified.** PeriodO is strongest for archaeological, art-historical and ancient and medieval history. Whether it holds any definition useful for the archive's subject was **not checked**. If it holds none, the case for it is weak.

**Reading.** At most an optional external reference: where a project period concept *has* an authority definition in PeriodO, record its ARK as an `identifier-assignment`, never as the concept's definition and never as a basis for merging concepts.

## 5. HISTO

**What it is.** The Finnish History Ontology, from the FinnONTO project at Aalto SeCo: a systematic model of history-oriented content with equivalences between old and modern Finnish. SeCo's related work includes WarSampo (the Finnish Second World War on the Semantic Web) and an ontology of historical events for semantic portals.

**Fit.** It is built around Finnish historical content and vocabulary and offers no identifiers for this archive's subject. It overlaps the event-and-period model the archive already has. Licence and serialisation were not checked.

**Reading.** Not recommended. The one reason to look again is methodological: WarSampo and the SeCo historical-events work are a precedent for modelling a war as linked events, and could inform the future incident model (WP 3.8). That is reading, not integration.

## 6. Options

| | What it means | Cost |
|---|---|---|
| **A. Integrate none now** | Record in the place work-item that PLATO is the reference to read when the `place` entity is designed, and that PeriodO is optional. | Nothing now. The risk is forgetting, which the note removes. |
| **B. Add open identifier types for external gazetteers and period authorities** | Register entries in `identifier-types.yaml` (for example a gazetteer ID for places, a PeriodO ARK for periods) through the DR-0080 registry process. | Small: the vocabulary is open. But with no place entity yet, nothing would use them; adding entries early invites unused vocabulary. |
| **C. Align the future `place` and `period-phenomenon` design with PLATO** | When those entities are designed, map the archive's assertion families to PLATO's attestation classes and publish the mapping. | Real design work; best done once PLATO is stable, with the ontology file read. |

## 7. Candidate decision records

### CDR-pending-external-place-period-vocabularies
**Recommended: A now, with C reconsidered when the `place` entity is designed or PLATO publishes a stable release, whichever is first; B only when a place or period entity first needs an external identifier.** HISTO is not adopted. PeriodO is cited only as an `identifier-assignment`, never as a definition and never as a merge basis (SPEC-0002). *Alternatives:* B now (the identifier types before any entity uses them); C now (a mapping against a draft ontology whose file has not been read).

**Steps before any of this is built:** a card on the board for the `place` work (none exists in this repository's issues as far as this session checked, which was not exhaustive); the PLATO ontology file and a PeriodO sample read directly; PeriodO's licence confirmed on its live site.

## 8. Open questions raised

1. **Timespan semantics.** PLATO's rule that an attestation's timespan is no wider than its source can witness blends world-time and evidence-time; SPEC-0001 keeps them apart. Which is right for a given use is a modelling question for the place design.
2. **Versions.** Which PLATO version is current (0.5.0 on Zenodo, 0.7.1 on GitHub).
3. **PeriodO coverage** for this archive's periods: unchecked.
4. **Whether the archive would ever publish alignments** to WHG or PeriodO. That would be an outward-facing act, so a founder decision, and out of scope here.

## 9. Sources

Internal: SPEC-0001 §2, §4; SPEC-0002; DR-0010, DR-0012, DR-0044, DR-0045; `registry/vocabularies/identifier-types.yaml`; WP 3.5 §2.3; WP 3.8 §2.

External, retrieved 2026-10-03 as page summaries, not primary files: [PLATO repository](https://github.com/pelagios/place-attestation-ontology); [PLATO on Zenodo](https://zenodo.org/records/23018199); [PLATO v0.7.1 release](https://github.com/pelagios/place-attestation-ontology/releases/tag/v0.7.1); [PeriodO](https://perio.do/en/) and its [technical overview](https://perio.do/technical-overview/); [HISTO](https://seco.cs.aalto.fi/ontologies/histo/); [SeCo, History on the Semantic Web](https://seco.cs.aalto.fi/projects/history/).
