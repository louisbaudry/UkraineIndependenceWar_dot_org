# Phase III / Study 10 — The `place` and `period-phenomenon` Entities
## Working Paper 3.10

**Project:** Ukraine's Second War of Independence
**Status:** CANDIDATE — AI-drafted, awaiting founder review.
**Version:** 3.10 (draft 0.1)
**Mandate:** build card [#109](https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues/109), the follow-on design work that [WP 3.9](wp-3.9-external-place-and-period-vocabularies.md) (CDR-P3-52) named: design `place` and `period-phenomenon`, read PLATO and a PeriodO sample directly, say whether and when external identifier types are added, and state the relation to `world-event` and to WP 3.8's incident model. **Design only: no schema, registry or code change follows from this paper.**
**Constraints inherited:** DR-0010 and DR-0012 (CIDOC-CRM world layer; names and identifiers as assertions); DR-0044 (territorial status as typed relations grounded in period phenomena; geometry attaches per DR-0010's place model with temporal validity); DR-0045 and DR-0080 (external identifiers; open-vocabulary registry process); DR-0004 (nothing external becomes a project assertion by being cited); DR-0112 (incident model: an incident is a `world-event` carrying no facts of its own); SPEC-0001 §2.1, §2.2, §4; SPEC-0002 (identifier agreement never confirms identity on its own); POL-0001 (personal data); WP 3.9 §7 (CDR-P3-52).

### AI provenance (record §80)

Drafted 2026-10-05 by an AI assistant (Anthropic Claude Code agent session) at the founder's direction. **What was read directly on 2026-10-05:** the PLATO ontology itself, as Turtle fetched from `https://w3id.org/plato` (186,693 bytes, declaring `owl:versionInfo "0.9.0-alpha.1"`, issued 2026-10-04), and the PLATO repository's `README.md` and `CITATION.cff` from `raw.githubusercontent.com`; PeriodO's complete dataset, `https://data.perio.do/d.jsonld` (7,806,284 bytes: 501 authorities, 9,446 periods), which was searched programmatically; and PeriodO's home page for its licence statement. Everything in §2 and §3 about those two resources comes from those files, not from summaries. **What was not checked:** PLATO's worked-example files and its published guide (only the ontology and README); whether PLATO's imports resolve; PeriodO's licence beyond the home page's words "public domain gazetteer" (no licence deed was found, so "CC0", which a secondary source gave in WP 3.9, is **not** confirmed); HISTO, not revisited. **Not verified, background knowledge only:** anything said in §4 about Ukrainian administrative-territorial codes and about renamings of Ukrainian places is the drafter's unverified background knowledge and is marked as such there. No source, person, incident or place in the archive's holdings was looked at. Candidate until the founder rules.

---

## 1. The question

SPEC-0001 §4 names `place` and `period-phenomenon` as world-layer entities; `schema/` has no DDL for either (WP 3.8 §2). Every war-fact this archive will model sits on one of them: where a strike fell, what a front line enclosed on a date, which territory an actor administered. WP 3.9 asked whether to adopt an outside vocabulary; this paper asks what the archive's own two entities should be, using the outside resources as design references where they help.

## 2. What reading the primary files closed

**PLATO's version (WP 3.9 open question 2).** Closed, and the answer is "it moves daily". WP 3.9 saw 0.5.0 on Zenodo (2026-09-28) and 0.7.1 on GitHub (2026-09-30). The ontology file read today declares **0.9.0-alpha.1, issued 2026-10-04**, with `owl:priorVersion` 0.8.0, and the README's status line reads "experimental — published for discussion and review; not yet stable". Four releases in about a week. WP 3.9's recommendation not to bind to it stands, now with evidence.

**PLATO's timespan rule (WP 3.9 open question 1).** Closed, and the conflict is **narrower than WP 3.9 feared.** PLATO keeps the two times apart, as SPEC-0001 does:

- `plato:attests_timespan` is "the historical timespan being asserted, not when the assertion was made": the world-time of the claim. Its "no wider than the source can witness" clause is a **limit on what a source may support**, not a redefinition of the field. A source that shows a name in use only in its own day supports only that day.
- `plato:source_timespan` dates the *source as a document* (an annal for 921 read in a manuscript of c. 925: attested 921, source c. 925). That is the evidence side.
- `plato:timespan_role` lets an attestation say its dates are an **evidence span** (earliest and latest document mentioning the entity), not a period of existence, and the ontology states that such a span "does not say that the entity existed, or bore any name, throughout".

In SPEC-0001's terms: `valid_time` is the world-time of what is asserted; the source's own date belongs to the source or holding; and the "no wider than the source can witness" rule is the existing `basis` discipline (an assertion's `valid_time` may not claim more than its basis supports), which the archive already requires. The one thing worth taking is the explicit **evidence-span role**: a gazetteer that dates a place by first and last mention is making a *different claim* (about documents), and must not be loaded into `valid_time`.

**PLATO's time bounds.** `Timespan` carries `start_earliest`, `start_latest`, `end_earliest`, `end_latest` and a label; any may be null (open). This is the same four-bound shape as SPEC-0001 §2.1's at-least/at-most bounds on each end, so the two are structurally compatible. Years of four or more digits and ISO dates are allowed. Conversion would need only a rule for precision, not a change of model.

**PLATO and uncertainty.** `plato:certainty` is a number from 0.0 to 1.0, "the contributor's confidence", with a note that it is distinct from *fuzziness* (the referent has no sharp boundary) and from `spatial_precision` (how finely a location is given). `plato:CertaintyLevel` declares three levels from the Linked Places Format. **It must not be read as a substitute for the archive's likelihood bands (DR-0026) or confidence (DR-0065).** The useful idea is the three-way separation (confidence in the claim / the referent's own vagueness / the precision of the location), which a front-line geometry needs.

**PLATO's `Period`.** An `Authority` subtype, "a named historical period, optionally linked to PeriodO or defined locally", with a `has_timespan` link and `periodo_uri` / `period_periodo_uri` / `period_label` properties. It is a **labelled interval used to date things**, not a happening. It confirms WP 3.9's reading: PLATO's `Period` is not the archive's `period-phenomenon`.

**PLATO and CIDOC-CRM.** The ontology has no alignment to CIDOC-CRM classes or properties beyond mentions in comments (about delegating typing to CRM, and a note that CRM separates a text from its witness). Mapping PLATO to DR-0010's world layer would be the archive's own work.

**PeriodO's coverage (WP 3.9 open question 3).** Closed, and **weak for this subject.** A search of all 9,446 periods for Ukraine, Russia, Crimea, Donbas, Kyiv, Cossack, Soviet, World War and Cold War finds 259 hits, but almost all are one authority: a Ukrainian-language archaeological and historical set (`p06v8w4`, 212 periods, spatial coverage "Ukraine", from the Palaeolithic through "Новітня доба" 1914–2000). **No period in PeriodO covers 2014 onward in Ukraine**, and none is named for the Russo-Ukrainian war (the only "Russo-" periods are the Russo-Turkish and Russo-Japanese wars). The dataset's periods that start in 1991 or later (40) are unrelated: fictional-future labels, other countries' conflicts. PeriodO is a gazetteer of *scholars' labels for eras*; this war's phases have no such definition there.

**PeriodO's licence.** The home page calls PeriodO "a public domain gazetteer"; the downloads are served from `data.perio.do`. No licence deed was found, so CC0 stays unconfirmed.

## 3. Proposed model

### 3.1 `place`

A `place` is an entity with **identity and entity status only** (SPEC-0001 §2.2, DR-0062), the same rule WP 3.8 applied to the incident. Everything said about it is an assertion family sharing the §2.1 core (`subject`, `content`, `valid_time`, `asserter`, `basis`):

| Family | What it says | Notes |
|---|---|---|
| `appellation-assignment` (exists in SPEC-0001) | a name, with script and language, valid over a span | Renamings, transliterations and occupation-era names are separate appellations, never normalised in place (WP 3.8 §6 applied to places). |
| `place-geometry` | a geometry, with a **role**, a **precision** and its own `valid_time` | Role (extent, central point, proxy, label anchor) is taken from PLATO's `geometry_role`; without it two geometries for one entity cannot be told apart. Precision is distinct from the claim's confidence. |
| `place-type` | a classification, through the open classification registry (DR-0042's pattern) | Settlement, administrative unit, region, water, infrastructure and so on. Open vocabulary, DR-0080. |
| `place-containment` | one place is part of another, over a span | The administrative hierarchy as typed relations, never a column. Competing hierarchies (Ukrainian law, occupation authorities' claims) coexist as separate attributed assertions. |
| `identifier-assignment` (exists) | an external gazetteer identifier | Never a merge basis on its own (SPEC-0002). |

Two consequences the founder should see:

- **Sovereignty is not a place attribute.** DR-0044 rejected territory attributes. A place's geometry says where it is; who administers it, claims it or occupies it is a `territorial-status` relation between an actor and the place over time. Crimea is one place with several attributed status relations, not a place that "belongs" to anyone in the table.
- **Control areas.** DR-0044 says front-line mapping over time "becomes a sequence of evidence-backed relations, not overwritten geometry". The model must say what the *object* of such a relation is. §3.3 puts that as a real choice.

### 3.2 `period-phenomenon`

A `period-phenomenon` is a CRM E4 **happening with a place and a time-span**: an occupation, an administration, a campaign, a phase of the war (DR-0044; Phase II conflict C-11). Like `place` it carries **identity and entity status only**. What it was, when it began and ended, where, and by whose account are assertions, each source-attributed and each allowed to compete with another's (§40).

It is the grounding entity for DR-0044's statuses: "occupation of place P by actor A from T1 to T2" is a `territorial-status` assertion, and the occupation itself, where it needs to be spoken of as a thing (so that evidence about it can point at it), is a `period-phenomenon`.

**It is not a label.** A named era ("Новітня доба", "Early Modern") is a *definition by an authority*, which is what PeriodO and PLATO's `Period` hold. That is a `documentary-assertion` shape (what a source says about a label), not a `period-phenomenon`. The model keeps the two apart.

### 3.3 The object of a territorial-status relation (the real fork)

| | Meaning | Cost |
|---|---|---|
| **A. A `place` of type `territorial-extent`** (recommended) | A control area or claimed territory is a place whose geometry is asserted by a named source over time. One extent per source-and-series (for example one for each source's control-area series), with its geometry versions as `place-geometry` assertions carrying `valid_time`. | Consistent with the identity-only pattern and with DR-0044; no new entity. Needs a rule that an extent's *identity* is the source's series, not a territory, so two sources' extents are never merged. |
| **B. A geometry held directly on the status relation** | The relation carries its own polygon. | No extent entity; but the same geometry cannot be cited by two relations, and DR-0044's "not overwritten geometry" becomes a per-row convention. |
| **C. A separate `territorial-extent` entity** | A new top-level entity. | Cleanest in isolation; adds an entity SPEC-0001 does not list, for a distinction A already expresses. |

### 3.4 Time

Per §2: `valid_time` on every place and period assertion is **world-time**. A source's own date lives on its holding. A date that is only the span of the documents mentioning something is a distinct, labelled claim and is never written into `valid_time`. The four-bound form of SPEC-0001 §2.1 is kept; PLATO's four bounds are compatible with it. Where a source gives an approximate date ("c. 925"), the approximation is carried in the bounds and the source's own wording kept as text, as PLATO does with its source label.

### 3.5 External identifiers (DR-0080)

`identifier-types.yaml` lists `wikidata` and `opensanctions`; no gazetteer or period authority. Candidate types, each added **only when a `place` or `period-phenomenon` first needs one**, never ahead of use (WP 3.9 option B's own caution):

| Candidate type | Used for | Note |
|---|---|---|
| `geonames` | places | A widely used open gazetteer; not read for this paper. |
| `whg` (World Historical Gazetteer) | places | Natural for PLATO-shaped data; only if the archive ever aligns to WHG, which is an outward-facing act and a founder decision (WP 3.9 open question 4). |
| a Ukrainian official administrative-territorial code | places | The state keeps an official code list for administrative-territorial units; *unverified here*: which list is current, whether its codes survive the 2020 reform of districts and communities, and its licence. **Do not register one before it is checked against the issuing body.** |
| `periodo` | periods | **Not recommended** (§2): PeriodO holds nothing for 2014 onward. Add only if a project concept later matches a PeriodO definition. |

SPEC-0002 already rates "places with authoritative gazetteer IDs" as tier T3. That stays true only where the identifier is **stable and issuer-scoped** (WP 3.5 §2.3); a code that is reissued after a merger of units would break it. The rating is therefore conditional on the check above, which this paper does not do.

### 3.5a Naming and renaming (unverified background)

Ukrainian places have, within living memory, been renamed (including by the decommunisation laws of 2015–16, which the drafter recalls as affecting many names, though this was not checked here) and carry names in several scripts and in the occupation authorities' usage. The model handles this through appellations with `valid_time`, language and script. **No specific renaming is asserted anywhere in this paper.**

## 4. Relation to `world-event` and to WP 3.8

- `world-event` is a happening at a place and time; DR-0112 already made the incident one, carrying no facts of its own. **Where it happened is an assertion family**, `located-at`, linking event to place, with source, `valid_time` and asserter.
- **Its content is either a reference to a `place` or a geometry with a precision, and the model must allow the second without the first.** A strike on a road, a field or an unnamed point has no gazetteer entry, and forcing one would invent a place. Precision is declared, as `place-geometry` declares it.
- Two sources can locate one incident at different places and different precisions. Both stand (DR-0112: counts and facts are per source, no default roll-up); a project location is a reviewed project assertion.
- **A period-phenomenon is not an incident.** An occupation is a long, spatially extended phenomenon that *contains* many incidents; the relation is a containment or "part of" assertion between events and phenomena, source-attributed.
- WP 3.8 open question 7 (are a strike in the strike-tracking sources and an incident the same entity) **is not decided here.** This paper only notes that `place` is the common join key either way, and that no strike-tracking source was examined for what location detail it gives.

## 5. Cross-cutting constraints, stated once

1. **Collection creates no canonical knowledge** (DR-0066). Nothing here is populated by a collector run; entries are hand-entered, human-reviewed assertions.
2. **Personal data.** A place is not personal data, but a **precise geometry for a private dwelling, joined to a named victim or an incident, can be** (POL-0001). The model therefore needs a rule, open question 3, that the precision shown for civilian-harm incidents is capped by tier. This paper raises it and does not decide it.
3. **External identifiers and external geometries are never assertions by being cited** (DR-0004).
4. **Preserve, structure and publish remain three decisions** (POL-0001 §1). Publishing a place's geometry is a separate act from storing it.
5. **Nothing here reopens DR-0010, DR-0012, DR-0044 or DR-0112.** The paper applies them.

## 6. Candidate Decision Records

Drafted as `CDR-pending-<slug>` and **numbered at merge** (DR-0102): each takes the next free `CDR-P3-nn`, in the order listed. Each is put to the founder separately.

### CDR-pending-place-model
**Recommended:** `place` carries identity and entity status only; names, geometry (with a declared role and precision and its own `valid_time`), type, containment and external identifiers are assertion families; sovereignty is never a place attribute (§3.1). PLATO is a **concept-level design reference** (geometry roles, the separation of confidence, fuzziness and precision) and **no formal mapping to it is published** until it reaches a stable release (§2). *Alternatives:* adopt PLATO's attestation bundle wholesale (a different granularity from SPEC-0001, and bound to a draft ontology that changed four times in a week); a flat place table with columns (rejected by DR-0012's pattern).

### CDR-pending-period-phenomenon-model
**Recommended:** `period-phenomenon` is a CRM E4 happening carrying identity and entity status only, grounding DR-0044's relations; a named era defined by an authority is a documentary assertion, never a `period-phenomenon` (§3.2). *Alternatives:* model every named era as a period entity (conflates a definition with a happening, contrary to DR-0044 and C-11).

### CDR-pending-territorial-extent
**Recommended: A.** An extent that a territorial-status relation points at is a `place` of type `territorial-extent`, whose identity is a source's series and whose geometry versions are `place-geometry` assertions with `valid_time`; two sources' extents are never merged (§3.3). *Alternatives:* B (geometry on the relation); C (a new entity).

### CDR-pending-time-semantics
**Recommended:** `valid_time` is the world-time of what is asserted, for places and periods as for every family; a source's own date is held on the source; a span of documents mentioning something is a distinct labelled claim and never `valid_time`; PLATO's four-bound timespan is accepted as compatible and not adopted as a field (§2, §3.4). *Alternatives:* adopt PLATO's "no wider than the source can witness" as a stored rule (redundant with the existing `basis` discipline).

### CDR-pending-gazetteer-identifier-types
**Recommended:** register **no** external place or period identifier types now; add `geonames`, and a Ukrainian official administrative code only after it is verified against its issuer, at the moment the first `place` needs one; **do not register `periodo`** unless a project concept later matches one of its definitions; registering `whg`, or publishing any alignment to WHG or PeriodO, is a separate outward-facing decision (§3.5). This supersedes WP 3.9's CDR-P3-52 only in closing its three "steps before this is built". *Alternatives:* register them now (unused vocabulary, and unverified codes); never register any (loses T3 batch confirmation for places).

## 7. Open questions raised

1. **Which Ukrainian official place code, if any, is stable enough** to be a T3 identifier, checked against the issuing body (§3.5).
2. **The shape of control-area series** (§3.3): how many extents one source's front-line series produces, and whether one place per dated snapshot or one per series with versioned geometry; the recommendation says per series, but it has not been tried against a real series.
3. **Precision caps by tier** for incident locations that identify a private dwelling (§5.2): a founder or counsel question, linked to WP 3.8 open question 3.
4. **PLATO re-check.** It should be read again at its first stable release, or when the `place` DDL is about to be written, whichever is first; the 0.9.0-alpha.1 text here may not survive.
5. **Whether any strike-tracking source gives coordinates or only place names**; unexamined, and it decides how often a location is a bare geometry (WP 3.8 open question 7).
6. **Order of work after the founder rules:** vocabulary registry entries (place types, geometry roles) → DDL for the families → hand-entry and review tooling. None starts before its candidate is ruled on.

## 8. Sources

Internal: SPEC-0001 §2.1, §2.2, §4; SPEC-0002; DR-0004, DR-0010, DR-0012, DR-0026, DR-0042, DR-0044, DR-0045, DR-0062, DR-0065, DR-0066, DR-0080, DR-0112; WP 3.5 §2.3; WP 3.8 §2, §6, §10; WP 3.9; POL-0001 §1; `registry/vocabularies/identifier-types.yaml`.

External, **retrieved 2026-10-05 as primary files**: the PLATO ontology, `https://w3id.org/plato` (Turtle, version 0.9.0-alpha.1, CC BY 4.0 per its README); the PLATO repository's `README.md` and `CITATION.cff` (`https://raw.githubusercontent.com/pelagios/place-attestation-ontology/main/`); PeriodO's `https://data.perio.do/d.jsonld`; PeriodO's home page, `https://perio.do/en/`.
