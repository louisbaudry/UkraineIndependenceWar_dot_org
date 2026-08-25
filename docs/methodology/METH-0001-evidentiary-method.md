# METH-0001 — Evidentiary Method

**Class:** METH (DR-0046 control) | **Version:** 0.1 | **Status:** Draft — Candidate for approval
**Approval:** — | **Effective:** —
**Supersedes:** — | **Superseded by:** —
**Change history:** 0.1 drafted 2026-08-25 as a candidate, at the founder's direction, after the DR-0048 release-readiness check reported that no METH document existed.
**Fulfils:** record §97 (methodology as a first-class versioned artifact); supplies the `methodology_version` that DR-0047 and DR-0048 require every release baseline to pin.
**Governed by:** DR-0024 (six layers), DR-0025 (epistemic vocabulary), DR-0026 + DR-0065 (two-dimensional uncertainty), DR-0027 (grading is triage), DR-0028 (dependence), DR-0029 (absence), DR-0030 (quantities), DR-0031/0032/0033/0034 (argumentation), DR-0035 (hypothesis competition), DR-0036 (no automatic adjudication), DR-0037 (Toulmin scaffold), DR-0008 (custody claims), DR-0018/0019 (anchoring, quotation), DR-0066 (three gates), DR-0055 (append-only), POL-0001 (personal data).
**Implemented by:** the registry vocabularies and argument schemes it cites; verification per §14.

### AI provenance (record §80)

Drafted 2026-08-25 by an AI assistant (Anthropic Claude Code agent session)
at the founder's direction. It **codifies decisions already taken** by the
founder in DR-0008 and DR-0018…DR-0037; it does not originate method. Where
it goes beyond enacted decisions it says so explicitly and marks the passage
as an open question for founder ruling (§15). Candidate until approved.

---

## 1. What this document is

This is the project's **evidentiary method**: the route by which preserved
material becomes something the project is willing to say, and the discipline
that route imposes at each step.

It exists because §97 requires methodology to be a first-class versioned
artifact from the beginning, and because §86 requires the project to be able
to answer *what exactly did we say about X, on date Z, and on what evidence
and methodology?* The second half of that question is unanswerable without a
versioned method to point at. Release baselines pin this document by version
(DR-0047, DR-0048); a significant change to it becomes release provenance.

### What it governs

The movement from a preserved holding to a published project conclusion —
verification, source handling, uncertainty, argument, hypothesis competition,
negative findings, review, and correction.

### What it does not govern

- **Collection.** What to collect and how to acquire it is SPEC-0003 and
  DR-0066/0067/0069; the personal-data limits are POL-0001 and DR-0071.
- **Storage.** DR-0073…0077 and SPEC-0006.
- **Identity resolution.** SPEC-0002 governs when two records are the same
  entity. This document uses its outputs and its review tiers; it does not
  restate its rules.
- **Legal conclusions.** The project does not reach them. §12 of this
  document states the boundary.

### Who it binds

Everyone producing project assertions, including the founder. AI agents
operate under §11 and never under their own authority (§79, AI-001).

---

## 2. The route from source to claim

The six layers of DR-0024 are not a filing scheme; they are the **stages of
this method**, and each transition is a distinct act that someone performs
and is accountable for.

| # | Stage | The act | Authority |
|---|---|---|---|
| 1 | Preserved holding | Acquisition and fixity | SPEC-0003, DR-0061 |
| 2 | Documentary assertion | Reading a source and recording *what it says*, anchored to an exact passage | DR-0017, DR-0018, DR-0019 |
| 3 | Evidence relation | Deciding this passage bears on this proposition, and how | DR-0024 layer 3 |
| 4 | Project assertion | Concluding something in the project's own voice | DR-0024 layer 4, §79 |
| 5 | Assessment | Attaching likelihood and confidence, with a basis | DR-0026, DR-0065 |
| 6 | Argument | Recording the inference and its defeaters | DR-0032, DR-0033 |

Four rules bind the route as a whole.

**R1 — No stage is skipped.** A project assertion with no evidence relation
beneath it is not a conclusion; it is an opinion wearing a conclusion's
clothes. If the chain is not there, the claim is not made.

**R2 — Being in the corpus is never evidential use** (Principle 5, EVID-003).
Preserving a document asserts nothing about its contents. Sources that bear
no evidence relation are normal and expected.

**R3 — Stages are never conflated.** "The source says X", "X happened", and
"we conclude X" are permanently distinct objects (EVID-002). A documentary
assertion is never promoted to a project assertion by editing it; a project
assertion is a separate record with its own asserter.

**R4 — The chain runs downward, not upward.** Evidence supports conclusions.
A conclusion never justifies reinterpreting the evidence beneath it. Where a
conclusion requires a passage to mean something the passage does not say, the
conclusion fails — that is the finding.

---

## 3. Verification: six questions, not one flag

§81 forbids a single ambiguous `verified` flag. Six distinct questions exist,
each with its own answer, its own evidence, and its own failure mode. Confusing
them is the most common way evidence work goes wrong.

| Question | Establishes | Does **not** establish |
|---|---|---|
| **Extraction verification** | The text/data we hold matches what the object contains | That the object is genuine |
| **Copy integrity** | The bytes are unaltered since acquisition (DR-0005) | Anything about the original |
| **Source authenticity** | The object is what it purports to be, from whom it purports | That its contents are true |
| **Semantic validation** | Our structured representation is a correct reading | That the reading's subject matter is true |
| **Analytical review** | The reasoning has been examined by a second party | That the conclusion is correct |
| **Proposition truth** | An assessment of whether the claim holds | Certainty |

The rule that follows is §38's, and it is load-bearing: **authenticity of an
object and veracity of its content are separate questions, answered
separately.** An authentic document may contain a lie. A forgery may report a
true event. Neither answer transfers to the other.

Each verification act is recorded as a typed QA action (§82) naming which of
the six it is. No act is recorded as unqualified "verification".

### Custody

The archive documents custody history in PREMIS/PROV vocabulary as fully as
practical. It **never emits "chain of custody" as a status claim** about its
own holdings (DR-0008). The phrase appears only when describing what others
assert, or as documented custody history explicitly labelled as such.
Downloading, hashing, timestamping, and preserving a file is preservation
practice; it is not legal custody, and calling it that would be false.

---

## 4. Handling sources

### 4.1 Grading is triage and nothing else

A two-axis Admiralty-style grade (source reliability × item credibility) may
be recorded to decide **what to look at first and how hard to look**
(DR-0027). It is barred from propagating into any proposition's likelihood,
confidence, or status.

The reason is §37's and it is empirical, not squeamish: a propaganda outlet
can publish an authentic document, and a reputable institution can err. A
grade predicts how much scrutiny is warranted. It never predicts truth.

**An assessment that cites a grade as its basis is malformed** and is
rejected in review. Assessments cite evidence and reasoning.

### 4.2 Dependence is researched; independence is never assumed

Five publications repeating one original report are one line, not five
(§36). Where consequential, dependence is recorded as a typed relation:
`cites`, `reposts`, `syndicates`, `derives-from`,
`shares-underlying-document`, `shares-underlying-witness`,
`common-evidentiary-origin`.

**Independence is a researched conclusion — the established absence of
dependence — never a default.** The default runs the other way: sources
reporting the same thing at the same time are presumed possibly dependent
until someone has looked.

### 4.3 Counting corroboration

Corroboration counts **independent lines**. Before a corroboration claim is
made, the analyst states:

1. which lines are claimed independent;
2. what was done to establish that independence;
3. which dependence relations are known and how they were handled.

A corroboration claim that cannot answer (2) is a repetition count, and is
recorded as such.

**Convergence is not corroboration when the convergence has a common cause.**
Two accounts agreeing because both derive from one briefing agree about the
briefing.

---

## 5. Assigning uncertainty

Two dimensions, never collapsed (DR-0026). They answer different questions
and can move independently.

- **Likelihood** — about the *proposition*. One of the seven ICD 203 bands
  (DR-0065), stored as the band identifier.
- **Analytic confidence** — about the *judgment*. `low` / `moderate` /
  `high`, derived from evidence quality, corroboration weighted by
  independence, and reasoning strength.

High confidence that something is very unlikely is coherent and common. So is
low confidence in a "likely" judgment — it means the evidence is thin, not
that the estimate should be softened.

### 5.1 Procedure for a likelihood band

1. State the proposition precisely enough that it could be wrong. A
   proposition that cannot fail cannot be assessed.
2. List the evidence relations bearing on it, in both directions.
3. Apply the relevant argument scheme(s) and answer their critical questions
   (§6).
4. Select the band whose numeric range matches the judgment. **The range is
   the anchor; the words are labels** rendered at the presentation layer.
5. Record the basis. **No band without a stated basis** (DR-0065 §6).

### 5.2 Procedure for confidence

Confidence is derived, and the derivation is stated: evidence quality;
corroboration and the independence of the lines counted; whether raised
defeaters have been answered; whether the reasoning has been reviewed. An
assessment must be able to say *why* its confidence is what it is.

### 5.3 Prohibited

- Bare numeric confidence scores.
- Probability values detached from their band.
- **Averaging contradictory assessments** (§40). Contradiction is preserved
  and displayed, not resolved by arithmetic. Two analysts disagreeing is a
  fact about the state of knowledge and is recorded as one.
- Inheriting another body's estimative language as a project judgment.
  Reporting that an agency assessed something "highly likely" is a
  documentary assertion carrying *their* scale (DR-0065 §5) — mapped, never
  converted.
- Attaching a band to a bare data field. Bands belong to assessments.

### 5.4 Keeping the dimensions apart in prose

Published wording derives from the typed values (EDIT-004). A common error is
prose that reads confidence as likelihood — "we are fairly sure" for a
`roughly-even-chance` band with `high` confidence. The rendering states both
or states neither.

---

## 6. Building an argument

Every consequential conclusion carries a recorded argument: premises, the
scheme relied on, and any defeaters raised, with their type (EVID-012).

### 6.1 Select a scheme

The registry holds the seed scheme library (DR-0034): witness testimony,
expert opinion, sign/indicator, document authenticity, geolocation,
image/video verification, coordination/attribution. Each carries **critical
questions** — the structured form of "what would make this reasoning fail?"

If no scheme fits, the argument is recorded with explicit premises and
warrant anyway, and the gap is proposed to the registry (DR-0080). A missing
scheme is not a licence to reason unstructured.

### 6.2 Answer the critical questions

Each critical question is answered, or recorded as unanswered with the
defeater type it implies if left so. **An unanswered critical question is not
a neutral silence** — the scheme declares in advance what kind of doubt it
leaves open.

Unanswered critical questions cap confidence. A conclusion resting on a
scheme whose distinctiveness or provenance questions are open does not carry
`high` confidence.

### 6.3 Type every defeater

- **Rebutting** — attacks the conclusion (counter-evidence for the opposite).
- **Undercutting** — attacks the inference link, premises intact: the
  document is authentic but does not show what is claimed.
- **Undermining** — attacks a premise: the document is forged; the witness
  was not present.

Authenticity challenges enter as undermining; interpretation challenges as
undercutting (DR-0033). The distinction determines what an answer must do —
answering a forgery claim with more counter-evidence about the event
addresses nothing.

**"Unresolved" is a legitimate end-state** (§40). A contested conclusion
stays visibly contested. The method has no step that makes a live objection
go away.

### 6.4 Draft against the Toulmin slots

Consequential conclusions are drafted and reviewed against claim, grounds,
**warrant**, **qualifier**, and anticipated rebuttals (DR-0037). The warrant
and the qualifier are the two elements most often left implicit, which is why
the scaffold names them. The scaffold is for drafting and review; the stored
representation remains the argument structure of DR-0032, from which the
Toulmin rendering is derivable.

### 6.5 Nothing computes a conclusion

Consistency checkers, defeater-coverage analysis, and formal acceptability
semantics may run as **analytic aids**: they surface unanswered critical
questions, unattacked assumptions, and inconsistencies. Their outputs are
advisory inputs to human judgment and are never written as a conclusion's
status (DR-0036, EVID-014). Tooling may rank, flag, and warn. It may never
conclude.

---

## 7. Competing hypotheses

For any investigation designated important, competing hypotheses are
first-class objects, not a prose aside (DR-0035).

**When required.** Any question where a single explanation is being built
toward, where the conclusion would be consequential, or where the project's
prior expectation is strong. The third case is the point: the instrument
exists to counter confirmation bias, so a strong prior is a reason to use it,
not a reason to skip it.

**How.** A hypothesis set for a defined question, with at least two
hypotheses including a genuine alternative. Evidence relations to each
hypothesis are typed: `supports` / `contradicts` / `discriminates` /
`neutral`. ACH matrices are derived views over these relations, never
separate data.

**Discriminating evidence is the object of the exercise.** Evidence
consistent with every hypothesis distinguishes nothing, however voluminous.
The analytically useful question is *what would tell these apart* — which is
also the research-gap inventory (§74–75).

Absence states and negative findings participate as evidence: "we looked for
the records this hypothesis predicts and they are not there" is
discriminating evidence when the search was adequate.

Hypothesis status changes are versioned assessments. Prior states are never
rewritten (§63, EVID-015).

---

## 8. Absence, negative findings, and quantities

### 8.1 A missing value never means "no"

Absence is typed: `unknown`, `not-researched`, `no-evidence-found`,
`unavailable`, `withheld`, `redacted`, `lost-or-destroyed`,
`not-applicable`, `indeterminate` (DR-0029). "We never looked" and "we
searched and found nothing" are different facts and are recorded differently.

Explicit negatives — "X did not occur", "no licence was issued" — are
assertions like any other: attributed, dated, evidence-backed.

### 8.2 Negative findings state scope and method

"We searched and found insufficient evidence" is **not** "we proved
non-occurrence" (§76). A consequential negative finding records:

1. the question searched;
2. the sources and holdings searched, and the period covered;
3. the method — search terms, languages, coverage limits;
4. what would have been found had the proposition been true;
5. what the finding therefore does and does not support.

Item (4) is what makes a negative finding evidential rather than merely
discouraging. Absent it, the finding records an effort, not a result.

Negative findings are published (§76). A project that publishes only what it
confirmed misrepresents its own evidence base.

### 8.3 Quantities keep their original semantics

"At least 17" never becomes "17" (§43–44). Quantitative assertions preserve
the original expression, semantic type (`exact`, `approximate`, `at-least`,
`at-most`, `range`, `greater-than`, `fewer-than`), value and units, stated
precision, stated uncertainty, and derivation method for computed values.

**Aggregation respects semantic type: a sum of at-leasts is an at-least.**
Normalized values are derived data and never overwrite the original.

Casualty figures are the case where this matters most and where the pressure
to round is strongest. The pressure is resisted structurally, not by
discipline.

---

## 9. Quotation

A project quotation targets the preserved original-language expression at an
exact locus and carries the exact passage, marked omissions, the locus,
linked translations where present, and transcription/OCR derivation where
the text passed through such a step (DR-0019).

**No quotation is minted from a paraphrase or a summary.** Quotation,
paraphrase, and summary are distinct types and are never silently converted
into one another. Back-translating a translated passage into the original
language does not produce a quotation; it produces a reconstruction, and is
typed as one.

Evidential annotations target preserved captures, never a live URL
(DR-0018). Where material is not yet preserved, preservation precedes
evidential annotation.

---

## 10. Review

### 10.1 Present authority

The founder is final editorial authority (§78, EDIT-001). The tiered model
below is the standing structure; while the project is one person it operates
as self-applied discipline, with the tier recorded so that later independent
review knows what was and was not done.

### 10.2 Tiers

Review depth tracks consequence (§78), using the registry review tiers:

| Tier | Applies to | Requires |
|---|---|---|
| **T1 — highest** | Conclusions naming individuals or entities in wrongdoing; anything feeding a legal-layer conclusion; identity mappings to designation records | Independent reassessment (§10.3); critical-question coverage; independence of evidence lines established, not assumed |
| **T2 — elevated** | Consequential project conclusions generally; cross-registry identity links | Second-party review of argument structure and qualifier; recorded disposition |
| **T3 — routine** | Bibliographic identity, gazetteer-anchored places, low-stakes alignment | Review, which may be batch-wise |

### 10.3 Independent reassessment

Second-person review is not automatically independent review (§83). At T1,
independence means **the reviewer examines the evidence and forms a judgment
before seeing the original conclusion.** Two signatures do not necessarily
mean two independent judgments, and the record states which kind was obtained.

### 10.4 Conflicts of interest

Conflicts are case-relative and are declared, managed, reviewed, or met with
recusal (§84). A conflict does not itself prove research wrong; it raises the
review tier. Undeclared conflicts are the failure, not conflicts.

### 10.5 Personal data

Publishing a conclusion about a person is a separate decision from
concluding it, and from preserving the material behind it. POL-0001's three
gates govern; this method does not create an exception to them. Where
POL-0001 §9's releases remain suspended pending its §10 legal review, the
DR-0071 interim constraints bind.

---

## 11. AI within the method

AI may collect, extract, translate, classify, summarize, and **propose**
assertions, matches, and relationships (§79). What it may not do is become
canonical knowledge without a human accepting it.

| Stage | AI may | Boundary |
|---|---|---|
| 1 — Preservation | Fetch, checksum, characterise | None; mechanical |
| 2 — Documentary assertion | Propose extractions and anchors | Proposal state; a human accepts |
| 3 — Evidence relation | Suggest candidate relevance | A human decides that this passage bears on this proposition |
| 4 — Project assertion | Draft | Never asserts. The asserter is a human |
| 5 — Assessment | Surface the inputs to a band or a confidence | Never selects either |
| 6 — Argument | Surface unanswered critical questions and inconsistencies | Never adjudicates (DR-0036) |

**The adoption boundary.** An AI-proposed assertion is a belief held by a
software agent until a human adopts it, and adoption is a separate recorded
act that changes who holds the belief (DR-0031, AI-003). Adoption is not a
formality: the accepting human is accountable for the content as if they had
authored it, which is the only thing that makes the accountability real.

**Provenance.** Consequential AI outputs preserve provider, model and
version, instructions, input references, output, pipeline version,
structured-output schema, validation result, reviewer, and disposition
(§80, AI-002). Routine disposable model calls are exempt by documented rule,
never by omission.

**Low-risk factual enrichment may be automated** under defined controls
(§79) — normalization to registry vocabularies, format conversion,
deduplication of identical strings. The control is that the class is defined
in advance and the automated act is logged, not that the act is small.

---

## 12. What this method does not claim

Stated plainly, because each of these is a claim the project could drift into
making by implication.

- **Not legal chain of custody.** §3, DR-0008.
- **Not legal findings.** The project does not determine that a crime
  occurred, that a person is guilty, or that a sanction was breached. It may
  record and assess what competent authorities have found, always qualified
  as theirs (§62).
- **Not proof of non-occurrence.** §8.2.
- **Not truth by corroboration count.** §4.3.
- **Not resolution by computation.** §6.5.
- **Not completeness.** The archive's coverage is what it is; collector-run
  coverage records what was sought, acquired, and missed (DR-0070), and
  frequency in the archive is not frequency in the world.
- **Not legal advice, and not a legal compliance framework.** POL-0001 §10's
  external legal review is a condition of that layer, not of this one.

---

## 13. Correction and retraction

Substantive mistakes are never silently overwritten (§77, EDIT-002). The
supported acts are correction, retraction, supersession, merge, split, legal
restriction, privacy removal, and archival withdrawal.

A substantive correction records rationale, supporting evidence, the editor
or reviewer, and the effect on published outputs. Corrections are new
records; the prior state remains (DR-0055). Governed redaction is the sole
exception to immutability and follows DR-0077.

**A retraction is a finding.** It states what was concluded, what is now
concluded, and what went wrong in the reasoning — which is the part with
future value. Being wrong and correcting the record leaves a trace, and the
trace is part of the evidence base.

---

## 14. Verification of this method

A method that cannot be checked is an aspiration. This one is checked
through the requirements that already bind it, which name their own
verification means:

| Method section | Requirements verified against |
|---|---|
| §2 route | EVID-001, EVID-002, EVID-003 |
| §3 verification | PRES-002, EVID-004 |
| §4 sources | EVID-008, EVID-009 |
| §5 uncertainty | EVID-006, EVID-007 |
| §6 argument | EVID-012, EVID-014, EDIT-003 |
| §7 hypotheses | EVID-013 |
| §8 absence and quantities | EVID-010, EVID-011 |
| §9 quotation | EVID-005 |
| §10 review | EDIT-001, EDIT-004 |
| §11 AI | AI-001, AI-002, AI-003 |
| §13 correction | EDIT-002, EVID-015 |

The audit-verified requirements above cannot be discharged until real
investigations exist. That is not a gap in the method; it is the method
waiting for material.

---

## 15. Open questions for founder ruling

These are places where this draft goes beyond what an enacted DR settles.
Each needs a ruling; none blocks approval of the rest if ruled on approval.

**Q1 — The threshold for "consequential."** The record uses the word
throughout without defining it, deliberately. This draft treats a conclusion
as consequential if it names an identifiable person or entity, feeds a
legal-layer conclusion, or would be materially relied on by others. Is that
the test, or should it be narrower?

**Q2 — Whether unanswered critical questions cap confidence.** §6.2 asserts
they do, and that `high` confidence is unavailable while a scheme's
provenance or distinctiveness questions are open. This is a real constraint
on the analyst and is not enacted by any DR.

**Q3 — Mandatory hypothesis sets.** §7 requires them where the project's
prior expectation is strong. That is deliberately the uncomfortable case. Is
it a requirement or a recommendation?

**Q4 — Self-review while the project is one person.** §10.1 records the tier
even when review is self-applied. An alternative is to record such
conclusions as unreviewed at their tier and publish them qualified as such,
which is more honest and more restrictive.

**Q5 — Retrospective likelihood phrasing.** DR-0065's consequences left open
whether a band used as credence about a past fact ("it is very likely that X
occurred in 2023") needs distinct wording from a forecast. It affects every
historical assessment the project will make, and needs a registry scope note.

---

## 16. Versioning

Per DR-0047, this document versions on its own regime, not with code.

- **Editorial revisions** (clarity, examples, cross-references) increment the
  minor version and do not require re-approval of the whole.
- **Substantive method changes** — anything that would alter a past
  conclusion had it been in force — increment the major version, require
  founder approval, and become **release provenance** under §97.
- Superseded versions remain in place, marked (DR-0046).

A release baseline pins the version in force at build time. When this
document's major version changes, conclusions produced under the prior
version keep pointing at that prior version; they are not retroactively
re-attributed to the new method.

---

## 17. Decision Record arising

Approval of this document requires a DR enacting it and ruling §15's five
open questions. Drafted as **DR-0085 — Adoption of the evidentiary method**,
candidate alongside this document.
