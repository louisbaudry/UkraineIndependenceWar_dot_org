# Phase III / Study 8 — Incident, Harm and Person Model for Civilian Harm and War Crimes
## Working Paper 3.8

**Project:** Ukraine's Second War of Independence
**Status:** CANDIDATE — AI-drafted, awaiting founder review.
**Version:** 3.8 (draft 0.1)
**Mandate:** [DR-0109](../../decision-records/DR-0109-civilian-harm-and-memorial.md) Consequence 5 — design the model that Decisions 2 and 4 fix only in outline: how an incident, a crime type and a harm relate to the existing assertion and evidence layers; how per-source counts are held; how a named person is linked to an incident; how the same person across sources and scripts is reconciled by a human; which crime-type vocabulary is used; how allegation and court finding are told apart. Issue [#71](https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues/71), child of [#61](https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues/61).
**Constraints inherited:** DR-0109 (all ten decisions, above all 2, 3, 4, 6, 7); DR-0004 (pipeline/world boundary); DR-0010/0012 (CIDOC-CRM world layer, identification as events); DR-0024/0025/0026 (epistemic layers); DR-0027 (grades are triage only); DR-0028 (dependence); DR-0030 (quantities keep their semantics); DR-0055/0077 (append-only, governed redaction); DR-0062 (entity status); DR-0065 (likelihood bands); DR-0066 (three gates); DR-0071(b) (no automatic structuring of personal data); DR-0086 (tier restrictiveness is declared); POL-0001 §5.5–5.9, §8.1–8.3; SPEC-0001, SPEC-0002; record §62–63.

### AI provenance (record §80)

Drafted 2026-10-01 by an AI assistant (Anthropic Claude Code agent session) at the founder's direction, as the build card [#71](https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues/71). **What was checked:** the repository's own text — `schema/02-core.sql`, `schema/04-epistemic.sql`, SPEC-0001 §2 and §4, SPEC-0002 §2–5, DR-0030, DR-0086, DR-0109, POL-0001 §5 and §8, the Phase I record §62–63, the access-tier and quantity vocabularies. **What was not checked:** no external legal instrument was retrieved. Every reference below to the Rome Statute, the Geneva Conventions, Ukraine's Criminal Code or any UN monitoring terminology is **drafter's background knowledge, unverified in this session**, and must be verified against the primary text before any vocabulary entry is registered (§8.3). No source, person or incident was looked at; this paper contains no name and no row from any source. Nothing here is legal advice. Candidate until the founder rules; **design only — no schema change follows from this paper until the founder rules on its candidates** (§9).

---

## 1. What DR-0109 fixed, and what is left to this paper

DR-0109 decided the *shape*: an incident is the foundation; each source's count stays that source's claim; a person is added only when a source names them, by a reviewer's hand, at a restricted tier, linked to an incident; the model is built for every crime category and filled with civilian deaths first; allegation, investigation and court finding are distinguished (Decisions 2–4). It left five design questions open (Consequence 5). This paper answers them as **candidate decisions**, one per question (§9), each with alternatives and a recommendation, so the founder can rule on them separately as with WP 3.4 and WP 3.7.

## 2. What the archive already has — and what it does not

This matters because the cheapest correct design reuses what exists.

**Built in `schema/` (read 2026-10-01):**
- `world_actor` — a person or group, **deliberately with no name column**; names arrive as assignment assertions with provenance (`schema/02-core.sql`, DR-0012).
- `proposition`, `documentary_assertion` (what a source says: always a `claim`, never carrying a project likelihood or confidence), `evidence_relation` (`supports` / `contradicts` / `bears-on` / `discriminates`), and the editorial/argument layers above them (`project_assertion`, `hypothesis_set`, `argument`, …).
- Append-only enforcement and a governed redaction tombstone (DR-0055, DR-0077).
- `tier_restrictiveness()` / `most_restrictive_tier()` — restrictiveness is **declared**, never derived from an ordering (DR-0086).

**Named in SPEC-0001 §4 but not yet built:** `world-event`, `place`, `participation`, `role-tenure`, `appellation-assignment` and the other world-layer families. A grep of `schema/` and `registry/` finds `world-event` only in SPEC-0001 and one Phase II paper; **there is no DDL for it**. So "incident" does not need a new top-level idea: SPEC-0001 already provides `world-event` as an entity and `participation` as an assertion family. This paper's job is to say how to *use* them for this subject, not to invent a parallel model.

**Not present anywhere:** a crime-type vocabulary, a legal-lifecycle vocabulary, a harm-kind vocabulary. Those are new registry entries (§8).

## 3. Question 1 — how incident, crime and harm relate to the assertion and evidence layers

The principle already in force: an entity carries **no facts of its own**; facts are assertions with a source, a time and an asserter (`world_actor` has no name; DR-0012). The same discipline applied here:

| Thing | What it is | Where its content lives |
|---|---|---|
| **Incident** | A `world-event` entity: "something happened here". Carries only identity and entity status (DR-0062). | Nothing else. When, where, what kind — all assertions. |
| **Occurrence** | A *claim* about when and where the incident happened. | Documentary assertion, valid-time and place, per source. |
| **Harm** | A *claim* that some harm of some kind befell some population or person in the incident (killed, injured, missing, deported, detained, property or infrastructure destroyed). | `harm` assertion family, per source; counts are DR-0030 quantity objects (§4). |
| **Crime characterisation** | A *legal* classification of the incident or part of it, by a named authority, in a named system, at a named stage. Distinct from harm: a harm is a fact claim; a crime is a legal one. | `legal-characterisation` assertion family (§8). |
| **Same-incident link** | A claim that reports from different sources describe the same incident. | A SPEC-0002 match assertion (§6). |

**Alternatives considered.**

- **A. Incident as `world-event`; every fact an assertion family (recommended).** Consistent with the existing pattern; the incident is the join point for many sources without any source's version overwriting another's; adding a harm kind or a crime category is a vocabulary change, not a table change (which DR-0109 Decision 2 requires: "built for every category").
- **B. A dedicated `incident` / `victim` / `crime` relational schema with typed columns.** Easier to query; but it puts the facts in columns, outside the assertion pattern, so "who said this, when, on what basis" is lost for exactly the data where it matters most, and a conflict between two sources has nowhere to live.
- **C. A hybrid: typed columns for the "agreed" attributes, assertions for the contested ones.** Rejected: someone must decide what is agreed, which is the editorial act this archive reserves for review and keeps off the schema (Principle 5).

**Recommendation: A.** One refinement the founder should know about: **the same-incident question is as hard as the same-person one.** A UN monitoring report, a Prosecutor General count and an oblast Telegram post may describe one strike, two strikes, or half of one. Treating incident identity as a SPEC-0002 match lifecycle (proposed → reviewed → confirmed or rejected, with rejected matches kept) is not optional; it is what prevents one strike being counted three times, or three strikes being collapsed into one (§4).

## 4. Question 2 — per-source counts under DR-0030

DR-0030 already says what a count is: original expression, semantic type (exact / approximate / at-least / at-most / range / greater-than / fewer-than), value and units, precision, stated uncertainty, derivation method; normalised values are derived and never overwrite the original. DR-0109 Decision 4.1 adds: counts from different sources are **never averaged or merged**; the unnamed dead are always counted; **children are counted separately**.

**Proposal.** A `harm` assertion carries three independent facets plus the quantity object:
- **outcome** — a vocabulary (killed, injured, missing, deported, detained, …);
- **population** — civilian; or, per DR-0109 Decision 3, a person *hors de combat* killed as a victim of a war crime; the vocabulary names these and **does not include combatants killed in combat** (DR-0109 excludes them);
- **sub-population** — an optional, separate figure for children, never derived by subtraction from a total the source did not break down;
- **quantity** — the DR-0030 object, in the source's own words.

**Roll-ups.** A display of "what the sources say about this incident" lists each source's claim side by side. Two rules for anything derived:
1. **No cross-source figure is computed by default.** If a reviewer wishes to state a project view ("at least N killed"), it is a **project assertion** with an explicit derivation and a likelihood band (DR-0065), citing the evidence — a judgement, not an aggregation.
2. **Sources are not independent just because they are different.** A monitoring body's count may rest on the same official or emergency-service figures as the others; DR-0028 dependence relations apply, and agreement between dependent sources is not corroboration. A sum of at-least figures across *different incidents* is an at-least (DR-0030), but across *sources about one incident* it is not a sum at all.

**Source grades are triage only (DR-0027):** no count may be selected, ranked or weighted by a grade in any computed result.

**Alternatives.** (A) per-source facets and no default roll-up — **recommended**; (B) a "best estimate" column maintained by the system — rejected, it is the average DR-0109 forbids under another name; (C) per-source facets plus an automatically computed lower bound — tempting and cheap, but it hard-codes a dependence assumption the system cannot make.

## 5. Question 3 — linking a named person to an incident

DR-0109 Decision 4.2: a person is added only when a source names them; a reviewer creates the entry by hand; held at a restricted tier (DR-0086); linked to the incident. Within that, this paper proposes the following structure and flags two points the founder must rule on.

**Structure.**
- The person is a `world_actor` of kind `person` — **with no name or date on the row**. A name is an `appellation-assignment` assertion (each spelling, each script, each source, separately), consistent with DR-0012.
- The link to the incident is a `participation` assertion with a role from a small vocabulary (*victim — killed*, *victim — injured*, …), carrying its source and basis. **That a named person died as a result of the incident is itself a claim**, with a source and an evidence relation; it is never inferred from the person appearing in a list.
- **Every personal-data assertion carries its own declared tier** (DR-0086). The proposed default is `internal` for an entered name; `most_restrictive_tier()` then guarantees that a page combining a public incident with an internal name renders **without** the name. Moving anything to `public` is a Gate 3 act (DR-0066), and only after the DR-0072 successor is approved (DR-0109 Decision 7, stage 3).
- **No field is added "in case it helps".** Beyond name appellations and the participation link, the only person-level attributes proposed are those needed to tell two people apart (§6): date or year of birth, place, date of death, as assertions at the same restricted tier. Cause-of-death detail, medical detail and family details are **out of the model** unless a later decision admits them.

**Point A — minors. A conflict between two rulings, not resolved here.** POL-0001 §5.7 says a minor is **not structured** "except where a minor's identity is legally significant and unavoidable (e.g., a named deported child in an official record or ICC proceeding)". DR-0109 Decision 3 puts civilians generally, including children killed in strikes, in the memorial, and Decision 4.1 requires children to be counted separately. Counting children as a figure does not structure any individual and is not in conflict. **Whether a named child killed in a strike may be entered as a person at all** is, on a plain reading, governed by §5.7's exception — and whether a killed child's identity is "legally significant and unavoidable" is exactly the kind of question counsel was commissioned to answer (POL-0001 §10). Candidate (§9, CDR-P3-49) therefore proposes that **no named minor is entered until the founder rules**, with the incident-level count unaffected.

> **Founder ruling during review, 2026-10-01:** asked whether a named child killed in a strike may be entered as a person, with three options (not until the founder or counsel rules — recommended; allow now; never), the founder chose **not until the founder or counsel rules**. This is a ruling on this one point only; it is not yet recorded in a Decision Record, which is written when `CDR-P3-49` is ruled on as a whole. The other four candidates and the rest of this one remain unruled.

**Point B — living persons.** DR-0109 is centred on deaths. A deceased person is outside the GDPR (Recital 27) and inside the project's dignity standard (POL-0001 §5.9). **An injured person is alive**: the GDPR applies in full, POL-0001 §5.5 applies to living victims, and survivors and witnesses fall under §5.6 (no structuring by default). The proposal is that **the person layer in its first form holds deceased victims only**; naming an injured or surviving person is a separate decision, as are the gated categories of DR-0109 Decision 2.

**Alternatives for the person layer.** (A) a deliberately narrow layer — deceased adult victims, source-named, hand-entered, appellation + participation + tie-break attributes only — **recommended**; (B) a wider layer including injured persons and minors from the start — rejected: it decides, by data model, questions POL-0001 and counsel have not answered; (C) no person layer until counsel answers — safest, but DR-0109 Decision 4 chose layers precisely so that incident work could proceed while the person layer waits, and nothing about A requires entering any name before the review: **A is a model, not an instruction to populate it.**

## 6. Question 4 — reconciling the same person (and the same incident) across sources and scripts

SPEC-0002 already defines the process: a match assertion goes **proposed → under-review → confirmed | rejected**; automated matchers and AI **may only propose** (AI-001); confirmation is a human decision citing **at least one basis beyond name or transliteration similarity**; **name similarity alone can never confirm**; rejected matches are kept and consulted so they do not return; confirmation produces effect by assertion, not mutation; **false merges cost more than missed matches** (§16), so doubt keeps entities separate. Persons used in consequential project assertions are tier T2 (SPEC-0002 §4). Nothing here changes that. What is specific to this subject:

1. **Spellings are data, not noise.** One person may appear in Ukrainian, Russian-derived and English forms. Each is stored as its own appellation assertion with language, script and — for Latin forms — the transliteration scheme if the source states it. **Nothing is normalised in place.** DR-0109 Decision 9's reference form (the Ukrainian spelling, with Ukraine's official Latin transliteration in English) is a **display rule over the stored appellations**; other spellings are searchable and are never rewritten.
2. **The discriminating evidence is itself personal data.** Telling two people apart needs something beyond the name — an age or birth year, a place, a date of death, a document number, a family's confirmation. Each is an assertion at the person's tier and each is **minimised to what discriminates**. Where nothing discriminates, the two entries stay separate and the memorial shows the entry that is better evidenced (§7).
3. **An unresolved duplicate is a smaller harm than a wrong merge here.** A false merge can attach one death to a living person's record or erase a victim from the record; a missed merge shows a name twice. This is the §16 asymmetry made concrete, and it is why the recommended default for the person layer is that **two candidate entries remain two until a human confirms with discriminating evidence**.
4. **Incidents are reconciled the same way** (§3): a same-incident match assertion with the same states and the same prohibition on confirming by similarity alone (a place name and a date are *similar* across two strikes in one town on one day). Their review tier is **T3 or T2 by the founder's choice** — T3 (batch-confirmable) is defensible for incidents with no persons attached; once a named person is attached the incident match should be at least T2 (§9, CDR-P3-50).
5. **Lineage is permanent** (SPEC-0002 §5): a merge or split of persons or incidents re-homes every attached assertion by review, never by bulk move, and the old identifiers keep resolving to the lineage explanation. For a victim this means a correction never silently removes a person from the record; it is visible as a superseding assertion (DR-0055).

**Alternatives.** (A) apply SPEC-0002 unchanged, with spelling-preservation and minimisation rules above — **recommended**; (B) a dedicated, stricter T1 for every victim match — defensible and costly: T1 requires a recorded review and independence-of-evidence analysis (SPEC-0002 §4) per person, which a memorial of any size cannot sustain; (C) allow the matcher to auto-confirm above a threshold — **forbidden** (AI-001, DR-0071(b)), listed only so it is on the record as considered.

## 7. Question 5 and 6 — the crime-type vocabulary, and allegation versus court finding

These two questions are one design, because both are about *legal characterisation*, which is authority-specific and temporal (record §62–63).

**The failure to avoid.** A single flat list of "crime types" on each incident states, as a fact, a legal conclusion that usually no court has reached and that different authorities characterise differently. Record §62: "not proven guilty" is not "historically established not to have done it"; §63: legal characterisation is temporal and authority-specific, and earlier epistemic states are never rewritten.

**Proposal — three layers, kept apart.**

1. **A neutral act-and-harm vocabulary (project-owned).** What happened, in descriptive terms a historian can assert without a legal conclusion — an attack on a residential building, an attack on a hospital, an execution of a person who had surrendered, deportation of a child, … Built for **every category** (DR-0109 Decision 2), but each entry carries a registry marker **`gated`**, naming the decision that must exist before any person-level record may use it. Deportation of children, sexual violence and torture and illegal detention are entered as `gated` from the first day; **the marker is what lets the model be built for every category without any of them being collected or structured by default** (DR-0109 Decision 2, Consequence 1). The mechanism that enforces `gated` — a database constraint refusing a person-level assertion that cites a gated entry without an approved decision reference, plus the check in code — follows the repository's rule that policy lives in both (CLAUDE.md, "Policy is enforced in code and in the database"); the design of that constraint is a later schema step, not part of this paper.
2. **A legal-characterisation assertion family**, mirroring the pattern the registry already uses for regulatory classification (`classification-systems`, DR-0042): every characterisation records the **system** (an international instrument, a national code, a monitoring body's own categories), the **jurisdiction**, the **asserting authority**, a **validity period**, and a type — **official / declared / project-analytical** — exactly as DR-0042 requires of classification assertions. The set of systems is an **open vocabulary** extended by the registry process (DR-0080), because systems will be added. The drafter expects at least: the war-crimes, crimes-against-humanity and aggression provisions of the Rome Statute; the grave-breaches and protections provisions of the Geneva Conventions; Ukraine's criminal-code provisions on violations of the laws and customs of war; and the descriptive categories used by UN monitoring. **All of these are unverified background knowledge** (provenance block); registering any requires reading the primary text.
3. **A legal-status lifecycle carried by each characterisation**, taken directly from record §63 rather than invented: *allegation → investigation → charge → indictment → trial → judgment → appeal → conviction | acquittal*, and *administrative finding* and *sanctions designation* where they apply. Each state change is a **superseding assertion** with its authority, jurisdiction, standard of proof, procedural posture and appeal status (§62), and **earlier states are never rewritten** (§63, DR-0055). The memorial shows the current state honestly, as DR-0109 Decision 3 requires, and **no state decides who is remembered**.

**Two rules the model must enforce, not merely document.**
- A characterisation is **always attributed**: "authority X, in system Y, alleges Z" — never an unattributed "this was a war crime". A project's own legal view, if ever expressed, is a `project-analytical` characterisation, labelled as such, and belongs to a later decision with legal advice behind it.
- A source's own confidence vocabulary (for example a monitoring body's verification terms) is stored **as that source's attribute**, a triage signal only (DR-0027). It is not a legal state and it is never converted into one.

**Alternatives (vocabulary).** (A) the three layers above — **recommended**; (B) one international legal taxonomy (the Rome Statute's list) as the only vocabulary — widely understood, but it makes every harm a legal claim at the moment of entry, excludes harms no instrument names, and bakes one authority's categories into the data; (C) Ukraine's national classification only — matches how Ukrainian prosecutors count, but is a single national authority's view and would not serve an international reader or a later external proceeding.

## 8. Cross-cutting constraints, stated once

1. **Collection creates no canonical knowledge** (DR-0066, Principle 5). Everything in this paper is a model for human-reviewed assertions; no collector run produces any of it.
2. **No automatic structuring of personal data** (DR-0071(b), POL-0001 §4). A person enters only by a reviewer's hand; no extraction populates `world_actor`, appellations or participation.
3. **The memorial adds no facts** (DR-0109 Decision 1): every fact on it points to an archive record, via approved, published records only, as static pages (Decision 8). The model therefore needs a **per-tier export projection**; building it is out of scope here.
4. **Public identifiers.** SPEC-0007 gives identifiers to cited things. **A public identifier for a person is itself a disclosure** and must not exist before stage 3 (names). This paper did not verify what SPEC-0007's citable classes currently permit for persons; it is an open item (§10) to be checked before any person-level work begins.
5. **Nothing here reopens a DR-0109 ruling.** If a candidate below would, it says so.

## 9. Candidate Decision Records

Each is put to the founder separately. Drafted as `CDR-pending-<slug>` and **numbered at merge** (DR-0102): `origin/main`'s highest was CDR-P3-46, so these are CDR-P3-47…51, in the order listed.

### CDR-P3-47
**Recommended:** an incident is a `world-event` that carries no facts of its own; when, where, what harm, what characterisation and which same-incident links are assertion families with source, time and asserter; harm and legal characterisation are separate families; no new top-level relational tables for this subject (§3). *Alternatives:* typed relational schema (B); hybrid (C).

### CDR-P3-48
**Recommended:** per-source harm assertions with outcome, population and sub-population facets and a DR-0030 quantity; no default cross-source figure; any project figure is a reviewed project assertion with a derivation and a likelihood band; dependence between sources is recorded (DR-0028) (§4). *Alternatives:* a maintained "best estimate" (B); a computed lower bound (C).

### CDR-P3-49
**Recommended:** a deliberately narrow person layer — **deceased adult victims only**, source-named, hand-entered, appellation + participation + minimal discriminating attributes, each at a declared restricted tier (default `internal`); **no named minor, no injured or surviving person, and no gated category** until the founder rules on each separately (§5). **This candidate puts one question to the founder that no document answers: whether a named child killed in a strike may be entered under POL-0001 §5.7's exception.** The recommendation is "not until counsel's advice or a founder ruling"; the incident-level child count is unaffected. *Alternatives:* a wider layer from the start (B); no person layer until counsel answers (C).

### CDR-P3-50
**Recommended:** SPEC-0002 applied unchanged to persons and to incidents, with spellings stored as separate appellations and never normalised in place, discriminating evidence minimised, and two entries staying two until a human confirms (§6); incident matches T3 while no person is attached and at least T2 once one is. *Alternatives:* a stricter T1 for every victim match (B); threshold auto-confirmation (C, forbidden).

### CDR-P3-51
**Recommended:** the three-layer vocabulary — a neutral act-and-harm vocabulary with a `gated` marker; an attributed, open-system legal-characterisation family following DR-0042's pattern; the §63 lifecycle as the legal-status vocabulary (§7). Registry entries for legal systems are verified against primary text **before** registration. *Alternatives:* one international taxonomy (B); one national classification (C).

## 10. Open questions raised

1. **Minors** (§5, Point A) — a conflict between POL-0001 §5.7 and DR-0109 Decision 3 that this paper surfaces and does not resolve. **Interim ruling 2026-10-01: no named minor until the founder or counsel rules** (see the note in §5). Counsel's advice may settle it.
2. **Injured and surviving persons** (§5, Point B) — the GDPR applies in full; a separate decision is needed before any is structured.
3. **Public identifiers for persons** (§8.4) — SPEC-0007 not checked against this subject; must be before person-level work.
4. **Where `gated` is enforced** (§7) — database constraint, code, or both, and how the "approved decision" reference is held; a schema-design step after the founder rules.
5. **Incident-match review tier** (§6.4) — T3 versus T2 is the founder's call.
6. **The legal-systems list** (§7) — verified against primary text before registration; the drafter did not retrieve any.
7. **Relationship to strike tracking.** DR-0106 collects reports of strikes and their effects without structuring anything. An incident here and a strike there will often be the same event; **whether they are one entity** is a decision for when both are modelled, not for this paper.
8. **Order of work after the founder rules:** vocabulary registry entries → DDL for the families → hand-entry tooling and review screens → the per-tier export projection. None starts before the corresponding candidate is ruled on.

## 11. Sources

All internal: DR-0109, DR-0106, DR-0030, DR-0086, DR-0042 (as described in `registry/vocabularies/classification-systems.yaml`); SPEC-0001 §2 and §4; SPEC-0002 §2–5; POL-0001 §5.4–5.9, §8.1–8.3; Phase I record §62–63; `schema/02-core.sql`, `schema/04-epistemic.sql`; `registry/vocabularies/access-tiers.yaml`, `quantity-semantic-types.yaml`, `classification-systems.yaml`. **No external source was retrieved.**
