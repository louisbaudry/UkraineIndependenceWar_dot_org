# DR-0100 — Establishment jurisdiction confirmed; controller identity and archive hosting location

**Category:** legal / operations | **Status:** **Approved**
**Decided:** 2026-09-15 by founder/principal editor — shape (option B of three) and both outstanding facts supplied the same day
**Origin:** CDR-P3-43, [the A6 legal-review brief](../legal/legal-review-brief.md) §11 | **Supersedes:** [`DR-0099`](DR-0099-establishment-jurisdiction.md) (2026-09-14) — extends it, does not contradict it | **Superseded by:** —

> **AI provenance (§80).** Drafted 2026-09-15 by an AI assistant (Anthropic
> Claude Code agent session) at the founder's direction, and approved the
> same day. The founder supplied both facts directly; neither was inferred.
> Nothing here is legal advice; the drafter is not a lawyer, and
> Consequence 8 states a question for counsel, not an answer.

## Context

### What the 2026-09-14 record already decided

[`DR-0099`](DR-0099-establishment-jurisdiction.md)
named France as the project's **interim** establishment jurisdiction — the
founder's own personal jurisdiction, no separate legal entity existing — and
amended POL-0001 to v1.1 so §10 names it. That ruling stands. This record
does not revisit it; the word *interim* is kept deliberately, because it is
the more accurate word and because nothing since has made incorporation
settled.

### Why a second record exists

Two agent sessions drafted the A6 legal-review brief in parallel, on
2026-09-14 and 2026-09-15, without either being aware of the other: one on
`claude/common-crawl-fk1bw8`, which remained unmerged, and one on
`claude/upbeat-dirac-6xksc2`. Each reached the same gap independently — that
POL-0001 §10 presumes an establishment jurisdiction the record never named —
and each put it to the founder, who answered both times. The result was two
approved records for one decision, at the same path.

That is recorded here rather than tidied away. CLAUDE.md's session-start
check is to fetch `origin/main` and diff against it; it catches merged work
and, by construction, cannot catch an unmerged branch. This is the third
collision of its kind (DR-0093 and DR-0094 each drafted an unrelated
"DR-0087"; WP 3.4 and WP 3.5 each used CDR-P3-31…35), and the first where
two sessions produced two versions of the same *document*, not merely the
same number. DR-0095 fixed number assignment for DRs; it does not reach CDR
numbers or duplicated documents, which remains an open gap — see
Consequence 6.

### What this record adds

The 2026-09-14 ruling settled the jurisdiction. It did not record **who the
controller is**, **where the archive server is**, or **what happens when
either changes** — and all three are load-bearing. The controller's identity
governs the DPIA, DPO and Art. 27 questions the brief puts at Q1–Q6; the
hosting location bears on establishment and on whether any transfer analysis
arises; and without a stated trigger, a later incorporation would silently
invalidate advice the project had paid for.

## Alternatives considered

Three were put to the founder on 2026-09-15, before the facts were supplied.

1. **Record all three facts in one Decision Record now** — jurisdiction,
   controller form, and hosting — before any counsel is briefed. Rejected:
   it forces the entity question now, and if the founder intends to
   incorporate later but has not chosen where, the record would carry a
   placeholder dressed as a decision.

2. **Record the jurisdiction and the hosting location, with the controller
   stated as the founder as a natural person**, and treat later
   incorporation as a POL-0001 §11 material change (**chosen**). Smallest
   commitment the founder has to stand behind; records what is true today
   rather than what is intended; the policy already has machinery for the
   later change. Accepted cost: if an entity is later formed in a different
   jurisdiction, a second and probably smaller legal spend may be needed.

3. **Commission counsel first and let them advise on jurisdiction and form
   together.** Rejected as circular: counsel qualified in a jurisdiction
   cannot be selected before the jurisdiction is named, and the Art. 85
   question is unanswerable without it.

## Decision

1. **The establishment jurisdiction is FRANCE, confirming the interim
   position** recorded on 2026-09-14 and left unchanged here, *interim*
   included. The applicable framework is the GDPR as applied in France
   together with the **Loi n° 78-17 du 6 janvier 1978** ("Loi Informatique
   et Libertés", LIL) as amended; the expected supervisory authority is the
   **CNIL**.

2. **The controller, for data-protection purposes, is the founder/principal
   editor as a natural person.** No legal entity exists and none is assumed.
   This states what is true as at 2026-09-15; it is not a commitment to
   remain unincorporated, and the superseded record's open question — whether
   entity formation should itself be a preliminary question for the review —
   stays open and is carried into the brief.

3. **The archive server is hosted with IONOS, in SPAIN.** IONOS is a
   processor acting on the project's instructions; the project is the
   controller. Both the controller's establishment and the hosting location
   are inside the EEA.

4. **Incorporation, or a change of either the establishment jurisdiction or
   the archive server's hosting country, is a material change under
   POL-0001 §11** and triggers a recorded policy review. Where the §10 legal
   review has by then been obtained, its continued applicability is
   reassessed as part of that review, and the reassessment is recorded
   whether or not it changes anything.

5. **POL-0001 is carried to v1.2, so §10 names this record and states its
   facts.** *(Revised 2026-09-15, the same day, by founder ruling — see the
   revision note below.)* §10 now names DR-0100 as the operative record and
   restates the establishment jurisdiction, the controller's identity, the
   hosting location and the §11 trigger in the policy itself, so a reader of
   §10 is not left to follow the supersession chain to find them. No §8
   ruling changes, §9's suspension is untouched, and what the review must
   cover is unchanged.

6. **This record is the source of the controller and hosting facts**, and
   the brief is filled from it. A later correction happens by superseding
   this record, never by editing the brief.

## Revision note (2026-09-15, same day)

**Decision 5 originally read:** *"POL-0001 stays at v1.1. Its §10 text as
amended on 2026-09-14 — France, interim, no entity formed, entity formation
an open question — remains accurate after this record, so no further
amendment is made. A controlled document is not re-versioned to restate facts
it already states correctly."*

The founder ruled otherwise the same day, on the objection that §10 would go
on citing DR-0099 while DR-0100 was the operative record, leaving a reader of
the policy alone without the controller and hosting facts and dependent on
following the supersession chain to find them. Decision 5 above replaces it.

**Why this is a revision and not a supersession.** The project's discipline is
that approved records change by supersession, never in-place edit (§77,
DR-0046). This revision was made before any rule permitted it, on the
drafter's own reasoning, and the drafter said so; the founder's answer was to
bound the exception rather than undo it. It is now governed by
[DR-0102](DR-0102-drafting-discipline-before-merge.md)
Decision 7, whose four conditions this satisfies: **same session** (approved
and revised on 2026-09-15, hours apart); **never merged** (the record had not
reached `main`, so nothing downstream relied on the original Decision 5);
**the founder ruled the change** (it was not the drafter's call); and **the
original survives** (quoted in full above).

That record's Decision 7 is explicit that "not merged yet" is a bound rather
than the reason — the other three conditions do the work — and that no
session may infer from Git state alone that a record is open to revision.
This is the worked example it names.

## Consequences

1. **The A6 brief's §9.1–9.3 are closed.** §9.4 and §9.5 were closed by
   separate founder rulings the same day and are unaffected by this record.

2. **Counsel can be selected** — a French practice, advising on the GDPR as
   applied in France and on the LIL. Selecting counsel is not commissioning;
   commissioning is a separate founder act that this record does not
   authorise.

3. **The controller question becomes answerable but not simpler.** A
   natural-person controller does not avoid the DPIA question and may make
   the DPO and Art. 27 questions sharper rather than moot. Counsel is asked
   about the controller as recorded at Decision 2 **and told that
   incorporation is contemplated** — otherwise the advice answers a question
   the project may stop asking.

4. **A risk is accepted, deliberately.** If an entity is later formed
   elsewhere, part of the review may need redoing. Decision 4 is the
   mechanism that catches it; the alternative was deciding the entity
   question now, which the founder declined for good reason.

5. **The superseded record keeps its place.** It is not deleted, edited or
   folded in: it recorded a real founder ruling on a real date, and §77's
   supersession discipline applies to decision records as much as to the
   Phase I record. POL-0001 v1.1's §10 cited it as the record that named
   France, which remains correct history; v1.2 names this record as the
   operative one (Decision 5).

6. **CDR numbering is an open gap.** Both sessions numbered candidate DRs
   from the same starting point: the other branch's WP 3.6 used CDR-P3-42,
   and so did this line of work. This branch renumbers its own to
   CDR-P3-43…45, leaving WP 3.6's CDR-P3-42 standing, since it is the older.
   DR-0095 prevents this for DR numbers and does not reach CDR numbers.
   **Extending it is proposed, not decided here** — it is the founder's call
   and is raised as such.

7. **Hosting in Spain raises no Chapter V transfer question** on these
   facts: France and Spain are both in the EEA. Two things do follow, noted
   so they are not mistaken for counsel's work. **(a)** IONOS is a processor,
   so GDPR Art. 28 requires a written processor contract with the prescribed
   terms — the project should establish whether one is in place, which IONOS
   contracting entity it is with, and what it says about sub-processors and
   support access from outside the EEA. That is an administrative check, not
   a legal opinion. **(b)** The project holds no establishment in Spain
   merely by renting servers there, so the CNIL is expected to be the
   competent authority — an expectation to confirm, not a conclusion.

8. **Naming France makes one of POL-0001's own rulings a live question.**
   The LIL's **Article 46** restricts processing of data relating to criminal
   convictions, offences and connected security measures to a closed list of
   actors; its **Article 78** frames the archiving-in-the-public-interest
   derogation from GDPR Arts. 15, 16 and 18–21 around *services publics
   d'archives*; its **Article 80** disapplies Article 46 for university,
   artistic or literary expression and for professional journalism. This
   project is a private archive, not a public archive service, and its
   material is squarely criminal-offence-adjacent. Whether it can rely on the
   archiving/research route at all in France — and whether the expression
   route is what actually unlocks Article 46 for it — is exactly what
   POL-0001 §8.3's ruling (archiving/research primary, expression secondary)
   presumes an answer to. **This record does not answer it and must not be
   read as doing so:** the drafter is not a lawyer, the articles were read
   from the CNIL's consolidated text (Légifrance was unreachable), and their
   interaction is what counsel is engaged to resolve. The brief's Q1–Q3 put
   it to them directly.

9. **Nothing about collection changes.** No source becomes registrable, no
   run becomes authorised, Track B does not start, and LEGAL-009 stays
   "partially satisfied" — a recorded jurisdiction is not a recorded review.
