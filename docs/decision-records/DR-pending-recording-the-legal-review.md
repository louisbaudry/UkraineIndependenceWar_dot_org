# DR-pending-recording-the-legal-review — What "the review's outcome is recorded" means

**Category:** legal / methodology | **Status:** **Approved**
**Decided:** 2026-09-15 by founder/principal editor (option C of three: rule on this now, hold CDR-P3-45 until Gate 3 work starts)
**Origin:** CDR-P3-44, [the A6 legal-review brief](../legal/legal-review-brief.md) §11 | **Supersedes:** — | **Superseded by:** —

> **AI provenance (§80).** Drafted 2026-09-15 by an AI assistant (Anthropic
> Claude Code agent session) at the founder's direction, and approved by the
> founder the same day. The proposal it enacts was raised while drafting the
> A6 brief and revised twice that day as the founder's rulings on the brief's
> §9.4 and §9.5 changed what it had to cover. Nothing here is legal advice,
> and nothing here anticipates what counsel will say — it fixes the *form* of
> the record, deliberately before the advice exists.

## Context

[POL-0001](../policies/POL-0001-personal-data.md) §10 ends: *"The review's
outcome is recorded, and this policy is revised to match it. **Until that
review is recorded, §9's releases do not take effect** — the DR-0071
constraints continue to bind."* LEGAL-009's verification method says the same
thing in the same words.

**Neither says what recording is.** No document states what act constitutes
it, who performs it, or what it must contain. The most consequential
conditional in the project's personal-data policy turns on an undefined term.

The failure mode is specific and easy to predict. Advice arrives. It is
read, it is persuasive, and everybody now *knows* the answer. Scale-up
begins because the question feels settled, with the record catching up
afterwards — or not. DR-0046 already refuses the analogous move for document
status ("status is document metadata, never inferred from Git state — a
commit is not an approval, and a merge is not an enactment"); this record
refuses it for the review.

Fixing the act **now, before the advice exists**, is the only moment it can
be fixed disinterestedly. Afterwards there is a specific answer in hand and
an obvious temptation to define "recorded" as whatever has already happened.

Two later rulings of 2026-09-15 add things this record must also pin. The
engagement was **split** (brief §9.5): Part A (Q1–Q6) goes to French
data-protection counsel, Part B (Q7–Q12) to IP/media counsel later — so which
advice discharges §10 needs saying. And counsel will answer **for two states
with the deltas named** (brief §9.4, §3.5) — so those deltas need a home that
is not prose.

## Alternatives considered

1. **Leave "recorded" undefined** and rely on judgment when the advice
   arrives. Rejected: the moment of judgment is the moment of maximum
   pressure to act, and the person judging will be the person who just paid
   for the answer.

2. **Treat receipt of counsel's written advice as the recording.** Rejected:
   receipt is not a decision. The project's entire gate architecture holds
   that a human decision at the appropriate tier moves state, never the
   arrival of an input (DR-0066). It would also leave POL-0001 v1.0 formally
   in force while the project acted on v2.0 reasoning.

3. **A Decision Record superseding DR-0072, carrying POL-0001 to v2.0 in the
   same act, with §9's releases taking effect on that record's approval**
   (chosen).

4. **Two records — one recording the review, one revising the policy.**
   Rejected: POL-0001 §10 ties them together in one sentence, and splitting
   them creates an interval in which the review is recorded but the policy
   still says something the advice contradicts. One act leaves no such gap.

## Decision

1. **The review is recorded by a Decision Record that supersedes DR-0072**,
   approved by the founder/principal editor. Nothing else records it.

2. **That record states, per question Q1–Q6:** what counsel concluded; the
   settledness marking the brief's §8 asks for — settled law, counsel's
   judgement on an unsettled point, or a matter to keep under review; and,
   where counsel's conclusion differs from a position in the brief's §4, the
   divergence **named as such**, with what changed.

3. **The §3.5 deltas are recorded as named POL-0001 §11 review triggers**,
   not as prose. Each trigger states the fact that would change and which
   conclusion it would move. A delta buried in a paragraph is not a trigger;
   it is something a future session has to notice.

4. **The same record carries POL-0001 to v2.0** — status block, change
   history, and the substantive revisions the advice requires — in the same
   act.

5. **POL-0001 §9's releases take effect on that record's approval and not
   before.** Not on receipt of the advice. Not on the founder reading it.
   Not on a commit and not on a merge (DR-0046).

6. **§10 is discharged by Part A alone.** Its six topics are the whole of
   what §10 requires. **Part B's answers, whenever they arrive, are recorded
   separately, supersede nothing, and move neither DR-0072 nor LEGAL-009** —
   they are not a second §10 review. What they do govern is whether specific
   acquisition steps may proceed: until Part B is answered, retrospective
   recovery from third-party archives (Q8), any `robots.txt` override (Q9)
   and named-channel platform capture (Q10) stay unauthorised **whatever
   Part A concludes**. A lifted §9 is not a licence to take a step whose own
   question is still open.

7. **LEGAL-009 moves from "partially satisfied" to satisfied in the same
   commit**, or the record states why it does not.

8. **A failed or partial review is also recorded.** If the advice cannot be
   obtained, or comes back qualified in a way that does not answer §10's six
   topics, that outcome is recorded as a Decision Record which **does not**
   supersede DR-0072 and **does not** lift §9. This follows the project's
   standing convention that failures are outcomes with explanations rather
   than absences (§28, PRES-007) — an unanswered review must not look the
   same as a review nobody commissioned.

## Consequences

1. **Nothing changes today.** No policy is revised, no release takes effect,
   LEGAL-009 stays partially satisfied, DR-0071 still binds collection, and
   Track B does not start. This record fixes a form, not a state.

2. **The session that receives the advice has a template, not a judgment
   call.** That is the point: the shape of the successor record was settled
   while nobody knew what the advice would say.

3. **CDR-P3-44 is discharged.** The brief's §11 says so and keeps the number
   struck through, since a spent CDR number is not reused.

4. **CDR-P3-45 is untouched and deliberately held** (founder ruling, same
   day): a rights position marked unreviewed cannot reach Gate 3. Its trigger
   is the start of Gate 3 work, not this record. Nothing is published, Gate 3
   has never run, and its fix touches the schema, `publication/gate3.py` and
   a test suite that must be shown to fail — work worth scheduling rather
   than bolting on.

5. **The advice's own access tier is not decided here.** Whether counsel's
   document is privileged, held at a restricted tier, or publishable is the
   open question at the brief's §12 item 1, to be settled on counsel's
   recommendation. Decision 2 concerns what the *record* states, which is
   public, not what the advice document's own status is.

6. **If Part B later contradicts a Part A conclusion**, that is a material
   change under POL-0001 §11 and is handled by §11's route — a recorded
   review — never by amending the superseding record after the fact.

7. **Numbering happens at merge**, per DR-0095: this file stays
   `DR-pending-recording-the-legal-review` until then.
