# DR-pending-civilian-harm-incident-model — The incident, harm and person model for civilian harm and war crimes

**Category:** data model / personal data / legal characterisation | **Status:** **Approved**
**Decided:** 2026-10-03 by founder/principal editor — five rulings made one at a time, and this record's text approved the same session. One of them (Decision 3's minors point) was first ruled 2026-10-01.
**Origin:** [WP 3.8](../phase-3/working-papers/wp-3.8-civilian-harm-incident-model.md), the design paper DR-0109 Consequence 5 called for; issue [#71](https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues/71) | **Supersedes:** — | **Superseded by:** —

> **AI provenance (§80).** Drafted 2026-10-03 by an AI assistant (Anthropic
> Claude Code agent session) at the founder's direction. The founder was
> asked the five candidate questions of WP 3.8 §9 one at a time, each with
> named options and a recommendation, and chose the recommended option
> each time. The rulings are the founder's; the wording, the reasons and
> the consequences are the drafter's and are what approval of this record
> confirms. **Nothing was verified outside the repository**: no external
> legal instrument was retrieved, and every reference to the Rome Statute,
> the Geneva Conventions, Ukraine's Criminal Code or UN monitoring
> terminology is background knowledge that must be checked against primary
> text before registration (Decision 5). Nothing here is legal advice.

## Context

[DR-0109](DR-0109-civilian-harm-and-memorial.md) made civilian harm and war
crimes a subject area and fixed ten rulings, among them that the model is
built for every category, that counts from different sources are never
merged, and that a person enters only by a reviewer's hand. It left the
shape of the model to a working paper. WP 3.8 drafted five candidate
records, `CDR-P3-47…51`, each with alternatives. This record enacts the
founder's rulings on them. It is a model, not an instruction to populate it:
it authorises no schema change, no source registration, no collection and no
publication.

## Alternatives considered

Each is set out with its reasoning in WP 3.8 §3–§7 and is not repeated here.
In brief, for each decision the founder chose the first-listed option of
the paper over the ones named:

| Decision | Chosen | Rejected |
|---|---|---|
| 1 Model shape | Fact-free `world-event` plus assertion families | Typed relational schema; hybrid with "agreed" columns |
| 2 Counts | Per-source figures, no default roll-up | A maintained "best estimate"; an automatic lower bound |
| 3 Person layer | Narrow: deceased adult victims only | A wider layer from the start; no layer until counsel answers |
| 4 Reconciliation | SPEC-0002 unchanged plus three rules | A stricter T1 for every victim; threshold auto-confirmation (forbidden) |
| 5 Vocabulary | Three layers kept apart | One international taxonomy; one national classification |

## Decision

1. **An incident is a `world-event` that carries no facts of its own**
   (CDR-P3-47). When, where, what harm, what legal characterisation and
   which same-incident links are assertion families, each with source, time
   and asserter. Harm and legal characterisation are separate families.
   **No new top-level relational tables** are created for this subject; a new
   harm kind or crime category is a vocabulary change. Same-incident links
   are SPEC-0002 match assertions, reviewed by a person.

2. **Counts are per-source and have no default cross-source figure**
   (CDR-P3-48). A `harm` assertion carries an outcome, a population, an
   optional separate sub-population (children, never derived by subtraction
   from a total the source did not break down) and a DR-0030 quantity in
   the source's own words. The population vocabulary does not include
   combatants killed in combat. Any project figure ("at least N") is a
   reviewed project assertion with a derivation and a likelihood band
   (DR-0065). Dependence between sources is recorded (DR-0028), and
   agreement between dependent sources is not corroboration. No count is
   selected, ranked or weighted by a source grade (DR-0027).

3. **The person layer is deliberately narrow** (CDR-P3-49). In its first
   form it holds **deceased adult victims only**, source-named and
   hand-entered. A person is a `world_actor` of kind `person` with no name
   or date on the row; each name spelling is an appellation assertion; the
   link to the incident is a `participation` assertion with source and
   basis, and that the person died in the incident is itself a claim,
   never inferred from appearing on a list. Every personal-data assertion
   carries its own declared tier (DR-0086), default `internal`. The only
   person-level attributes are those needed to tell two people apart:
   birth date or year, place, date of death, at the same tier. Cause-of-death,
   medical and family detail are out of the model. **Not in this layer,
   each needing its own later decision:** any injured or surviving person,
   and each gated category of Decision 5. **No named minor is entered
   until the founder or counsel rules** (founder ruling 2026-10-01, now
   recorded here); the incident-level child count is unaffected. Defining
   the layer enters no name.

4. **SPEC-0002 applies unchanged to persons and incidents** (CDR-P3-50),
   with three added rules. Each spelling is stored as its own appellation
   with language, script and, where stated, transliteration scheme, and
   nothing is normalised in place (DR-0109 Decision 9's reference form is a
   display rule). The evidence that tells two people apart is itself
   personal data and is minimised to what discriminates. Two entries stay
   two until a human confirms with evidence beyond name similarity. Incident
   matches are reviewed at tier T3 while no person is attached and at least
   T2 once one is. Auto-confirmation above any threshold is forbidden
   (AI-001, DR-0071(b)).

5. **The vocabulary has three layers kept apart** (CDR-P3-51). (a) A
   project-owned neutral act-and-harm vocabulary in which each entry
   carries a `gated` marker naming the decision required before any
   person-level record may use it; deportation of children, sexual violence
   and torture and illegal detention are `gated` from the first day. (b) An
   attributed legal-characterisation family following DR-0042's pattern,
   recording system, jurisdiction, asserting authority, validity period and
   official, declared or project-analytical type, never an unattributed
   "this was a war crime"; its set of systems is an open vocabulary
   extended through the registry (DR-0080). (c) A legal-status lifecycle
   from record §63 (allegation through conviction or acquittal, plus
   administrative finding and sanctions designation), each change a
   superseding assertion and earlier states never rewritten. A source's own
   confidence vocabulary is stored as that source's attribute and is never
   converted into a legal state. **Registry entries for legal systems are
   registered only after being checked against the primary text.**

## Consequences

1. **Nothing is built by this record.** Schema, vocabularies and the
   database constraint that enforces `gated` (policy lives in the DDL and
   the code, CLAUDE.md) are later build cards, each against this record.
2. **Nothing is collected, entered or published.** No person is entered
   before the DR-0072 successor is approved and then only under POL-0001
   §8.1; the memorial still adds no facts (DR-0109 Decisions 1, 7).
3. **Open items this record does not close:** what SPEC-0007's citable
   classes permit for persons (a public identifier for a person is itself a
   disclosure and must not exist before names are published); verification
   of every legal-system entry against primary text; the minors question
   beyond the 2026-10-01 interim ruling's terms; the gated categories.
4. **Nothing here reopens a DR-0109 ruling.**
5. `CDR-P3-47…51` are discharged by this record. WP 3.8 stays as the
   reasoning and is not edited.
