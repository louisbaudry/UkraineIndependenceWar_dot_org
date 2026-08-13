# Phase II / Workstream 4 — Epistemology & Evidence Concept Map
## Working Paper 0.5

**Project:** Ukraine's Second War of Independence
**Status:** CANDIDATE — AI-drafted, awaiting founder review and approval. Nothing in this paper is canonical.
**Version:** 0.5 (first draft of Workstream 4)
**Mandate:** WP 0.1 research sequence item 4 — source assertions, project conclusions, uncertainty, verification; plus the CRMinf evaluation ordered by DR-0016.
**Constraints inherited:** DR-0004 (layer boundary), DR-0012 (identity assertions), DR-0016 (CRMinf as starting candidate), DR-0017/0018 (evidence targeting and anchoring); WP 0.1 no-go list (no universal reliability scores, no arbitrary numeric confidence).

### AI provenance (per Phase I record §80)

| Field | Value |
|---|---|
| Drafted by | AI assistant (Anthropic Claude Code agent session), continuing the founder-directed workstream sequence |
| Date | 2026-08-11 |
| Inputs | Phase I record (§29–§44 centrally); WP 0.1–0.4; DR-0001…0023 |
| Human review | **Pending** — founder is final editor (record §78) |
| Disposition | Candidate working paper; all candidate Decision Records herein are proposals |

---

## 1. Scope and method

This is the first workstream with **no pre-selected standard** (WP 0.1 layer F).
The method is therefore different: survey the disciplines the record names
(§42, §103) — intelligence analysis, scientific uncertainty assessment, legal
evidence, historiographical source criticism — extract the load-bearing
instruments each has matured, evaluate CRMinf against the requirements
(DR-0016's order), and compose a candidate epistemic architecture. Argumentation
formalisms (Toulmin, Wigmore, AIF, computational argumentation) are noted where
they border this work but belong to Workstream 5.

## 2. The requirement core, compressed

The record's epistemic requirements (§29–§44) reduce to six demands:

1. **Attribution:** every proposition knows who asserts it, when, on what basis
   (§30, §32).
2. **Layering:** "the source says X," "X happened," and "the project concludes X"
   are different propositions with different owners (§32–33, Principles 3, 7, 10).
3. **Claim-relative evidence:** sources are evidence only *for particular
   propositions*, via explicit relationships (§29, Principle 6).
4. **Honest uncertainty:** typed, non-collapsed, never falsely precise
   (§40, §42–44, Principles 8–9).
5. **Contradiction without averaging:** disagreement is preserved, not blended
   (§40).
6. **Revision with memory:** epistemic states change without rewriting their
   history (§63, §77).

## 3. Discipline survey — instruments worth taking

### 3.1 Intelligence analysis

- **Estimative language.** From Sherman Kent's words of estimative probability
  to the current calibrated yardsticks — **US ICD 203** (seven ordered
  probability expressions mapped to percentage bands) and the **UK PHIA
  probability yardstick** — the mature practice is: a small, ordered, publicly
  defined set of verbal probability expressions, each bound to an explicit
  numeric range, used consistently. This satisfies §42's demand to resist false
  precision while remaining machine-comparable.
- **Probability ≠ confidence.** ICD 203 and allied doctrine separate the
  *likelihood of the proposition* from the *analytic confidence* in the
  judgment (a function of evidence quality, corroboration, and reasoning
  strength). The record demands exactly this separation (§42).
- **Source evaluation.** The **Admiralty/NATO system** grades source
  reliability (A–F) separately from item credibility (1–6) — structurally
  aligned with §37's insistence that source reputation and proposition truth
  are different questions. Its legitimate project role is **triage and review
  prioritization only** (§37).
- **Analysis of Competing Hypotheses (ACH)** and structured analytic
  techniques operationalize §35 (competing hypotheses, discriminating
  evidence); their representation is Workstream 5 material, but the epistemic
  layer must leave room for hypothesis sets and evidence-vs-hypothesis
  relations.

### 3.2 Scientific uncertainty (IPCC practice)

The IPCC's calibrated-uncertainty framework independently converged on the same
two-dimensional structure: a **likelihood scale** (verbal terms bound to
probability ranges) plus a **confidence scale** derived from *evidence* (type,
amount, quality) and *agreement* (consistency across sources). Two mature
disciplines agreeing on the shape of the solution is strong validation for
adopting that shape.

### 3.3 Legal evidence

Concepts the epistemic layer must not contradict (full study remains legal-
domain work, §103): relevance and probative value are **claim-relative** —
the legal tradition's version of Principle 6; **direct vs circumstantial**
evidence maps to the record's direct-evidence vs inferential-support
distinction (§34); **authentication** is a distinct assessment, already
handled by §38 and DR-0008's claims discipline; **standards of proof** are
jurisdiction- and forum-specific and must never be silently imported into
project conclusions (§62).

### 3.4 Historiographical source criticism

External criticism (is the source what it purports to be) vs internal
criticism (is its content credible) reproduces §38's authenticity/veracity
split. Testimony, transmission chains, and interdependence of witnesses
(§36's source-independence problem) have been core historiographical method
since the 19th century — the discipline confirms the requirement and offers
the vocabulary of *dependence* rather than *independence*: independence is
the researched absence of dependence, never a default assumption.

## 4. CRMinf evaluation (per DR-0016)

**What CRMinf provides, and how it fits:**

| CRMinf concept | Requirement served |
|---|---|
| **I2 Belief** — an agent holding a proposition set to be true/false/uncertain, over time | Attribution (§30): who asserts, when, with what status; belief revision with memory (§63) |
| **I4 Proposition Set** — the content believed | Propositions as first-class, distinct from their holders |
| **I5 Inference Making** — activity deriving a belief from premise beliefs by a logic | Inference visibility (§34, Principle 7); derived assertions carry their inputs and method |
| **I7 Belief Adoption** — taking over another's belief | Documentary assertions entering the project's graph *as adopted claims*, not truths (§32) |
| **I1 Argumentation** — the reasoning activity umbrella | Bridge to Workstream 5 |

This is a genuine match on the reification core: beliefs-held-by-agents-
over-time-on-a-basis is precisely the record's assertion model, and it is
CRM-native (composing with DR-0010/0011/0017 without translation).

**What CRMinf lacks (all bounded, all extensible):**

1. No calibrated estimative-probability vocabulary (§42) — supply from §3.1/3.2.
2. No source-independence/dependence typing (§36) — supply as typed relations
   between beliefs/sources.
3. No quantitative-assertion semantics (§44: at-least/at-most/range) — supply
   as structured value objects inside proposition content.
4. No absence-state vocabulary (§41) — supply as project vocabulary.
5. Negative observation (§48) underdeveloped — handle via explicit negative
   propositions with their own provenance, never via missing data.

**Verdict (candidate):** adopt CRMinf as the **reification grounding** of the
epistemic layer, with the five named project extensions; final argumentation
formalism (I1's internals, ACH representation, defeaters) awaits Workstream 5.

## 5. Candidate epistemic architecture (refining record §31)

The §31 six-layer working hypothesis survives contact with the disciplines,
refined as:

1. **World layer** — entities/events (DR-0010): what propositions are *about*.
2. **Documentary assertions** — what sources say, anchored to exact passages
   (DR-0017/0018); entering the graph via belief adoption (I7-pattern), owned
   by the *source*, not the project.
3. **Evidence relations** — explicit, claim-relative links: this
   capture/passage/observation *supports / contradicts / bears on* this
   proposition (§29; Principle 6). Being archived ≠ being evidence.
4. **Project assertions** — beliefs held by the *project* (or a named analyst),
   produced by inference activities with visible premises (I5-pattern), under
   human accountability for consequential conclusions (§79; DR-0016 boundary).
5. **Epistemic assessments** — the status/probability/confidence attached to
   assertions, versioned, never overwriting prior states (§63).
6. **Arguments** — inference/defeater structure (Workstream 5).

## 6. Candidate epistemic vocabulary v1 (per §30)

Six categories, defined in the semantic registry at enactment, expanded only by
DR (record §30: "expanded only when real cases require it"):

| Term | Definition sketch |
|---|---|
| **observation** | A recorded act of perceiving/measuring by a person or instrument, with observer, method, time (CRMsci-compatible; §48–49) |
| **claim** | A proposition asserted by a source or actor, held by them, adopted into the graph with attribution (§32) |
| **assessment** | An evaluative judgment about a proposition or source by a named assessor on stated basis |
| **hypothesis** | A candidate explanation under investigation, member of a competing-hypothesis set (§35) |
| **finding** | A conclusion of a defined investigation or review process, with its scope and method (incl. negative findings, §76) |
| **project conclusion** | An editorially accountable assertion published in the project's own voice (§33, §78–79) |

## 7. Uncertainty model (candidate)

Two dimensions, never collapsed (§42):

- **Likelihood** of the proposition: one ordered scale of verbal probability
  expressions, each bound to an explicit numeric range. The scale is fixed at
  vocabulary enactment, derived from ICD 203/PHIA practice; until then no
  probability wording in project outputs is canonical.
- **Analytic confidence** in the judgment: low / moderate / high, derived from
  stated evidence quality, corroboration (weighted by *independence*, §8 below),
  and reasoning strength.

Prohibitions (enforcing the WP 0.1 no-go list): no bare numeric confidence
scores; no probability values without their band; no averaging of
contradictory assessments (§40); measurement uncertainty, source disagreement,
and analytical uncertainty remain typed separately (§40).

## 8. Source grading, dependence, absence, and quantity (candidates)

- **Source grading** (§37): an Admiralty-style two-axis grade (source
  reliability × item credibility) may be recorded for **triage, scrutiny, and
  review-priority** decisions only. It is architecturally barred from
  propagating into proposition truth status. A graded-F outlet can supply an
  authentic document; grading never substitutes for assessment.
- **Dependence** (§36): typed relations — cites, reposts, syndicates,
  derives-from, shares-underlying-document/witness/origin — recorded where
  consequential. Corroboration counting uses *independent* lines only;
  independence is a researched conclusion, not a default.
- **Absence states** (§41): unknown / not-researched / no-evidence-found /
  unavailable / withheld / redacted / lost-or-destroyed / not-applicable /
  indeterminate. A missing value never means "no." Explicit negative assertions
  require provenance like any other assertion.
- **Quantitative assertions** (§43–44): values preserve original semantics —
  exact, approximate, at-least, at-most, range, greater/fewer-than — plus
  original expression and derivation. Normalized values are derived data and
  never overwrite the original. "At least 17" never becomes "17."

## 9. Candidate conflict-register entries (additions)

| Term | Colliding senses | Resolution direction (candidate) |
|---|---|---|
| **confidence** | Analytic confidence (judgment strength) vs probability vs statistical confidence interval | "Confidence" = analytic confidence only; likelihood and intervals named as such |
| **evidence** | Legal (admissible material) vs project (claim-relative support relation) vs colloquial (anything archived) | Registry: "evidence" requires a proposition; archived material without one is a *source* (§29) |
| **belief** | CRMinf I2 (technical: held proposition attitude) vs colloquial belief | Technical sense in modeling documents; publication layer avoids the word |
| **finding** | Project finding (§30 vocabulary) vs legal finding (§62) | Legal findings always jurisdiction-qualified; never bare "finding" |
| **verification** | Copy integrity vs extraction accuracy vs authenticity vs truth assessment (§81) | Never one flag; the §81 six-way split enters the registry with this workstream's vocabulary |
| **observation** (resolves WP 0.3 entry) | CRMsci S4 vs intelligence "observation" vs §30 category | §30 "observation" subsumes both: an act of perception/measurement with provenance; instrument observations add §49 metadata |

## 10. Candidate Decision Records (proposals only — require founder approval)

- **CDR-W4-1:** Adopt the **six-layer epistemic architecture** (§5 above) as
  the governing structure: world entities/events; documentary assertions;
  claim-relative evidence relations; project assertions; versioned epistemic
  assessments; arguments (WS5). "In the corpus" never implies "evidentially
  used."
- **CDR-W4-2:** Adopt **epistemic vocabulary v1** — observation, claim,
  assessment, hypothesis, finding, project conclusion — with registry
  definitions; expansion or change only by DR (record §30).
- **CDR-W4-3:** Adopt the **two-dimensional uncertainty model**: calibrated
  verbal likelihood bands (scale fixed at vocabulary enactment from ICD 203 /
  PHIA practice) plus low/moderate/high analytic confidence; bare numeric
  scores and contradiction-averaging are prohibited.
- **CDR-W4-4:** **Source grading is triage-only:** Admiralty-style two-axis
  grades may steer scrutiny and review priority; they are architecturally
  barred from determining proposition truth (§37).
- **CDR-W4-5:** **Dependence is explicit:** typed source-dependence relations;
  corroboration counts independent lines only; independence is a researched
  conclusion (§36).
- **CDR-W4-6:** Adopt the **absence-state vocabulary** (§41); missing values
  never default to negative; explicit negatives carry provenance.
- **CDR-W4-7:** **Quantitative assertions preserve original semantics**
  (exact/approximate/at-least/at-most/range/comparatives); normalized values
  are derived and never overwrite originals (§43–44).
- **CDR-W4-8:** **CRMinf verdict:** adopted as the reification grounding of
  the epistemic layer (beliefs, proposition sets, inference making, belief
  adoption), with the five named project extensions (probability vocabulary,
  dependence typing, quantity semantics, absence states, negative
  propositions); the argumentation formalism decision is deferred to
  Workstream 5.

## 11. Unresolved research questions (feed Phase II output 7)

1. Exact likelihood-band boundaries and wording (ICD 203 vs PHIA vs hybrid) —
   fixed at vocabulary enactment; multilingual renderings via §60 terminology
   governance.
2. ACH representation: dedicated hypothesis-matrix objects or general argument
   structures? (WS5.)
3. Bayesian aggregation: does the project ever compute posterior probabilities,
   or remain verbal-band only? (Defer; revisit with real investigations.)
4. Epistemic assessment versioning mechanics — how assessments append without
   rewriting (§63) — interacts with Workstream 7 versioning.
5. Who may set which epistemic status (analyst vs reviewer vs founder) — the
   §78 risk-tiered editorial model applied to statuses; POL/PROC documents, not
   ontology.
6. Negative-observation semantics for machine sources (§48–49): coverage-aware
   "not observed" (sensor was looking and didn't see) vs mere data absence.

## 12. Sources

- ICD 203 (Analytic Standards, ODNI) and ICD 206 (Sourcing Requirements) — public directives
- UK PHIA Probability Yardstick (Professional Head of Intelligence Assessment)
- Sherman Kent, "Words of Estimative Probability" (CIA Studies in Intelligence)
- Heuer, *Psychology of Intelligence Analysis* (ACH); Heuer & Pherson, *Structured Analytic Techniques*
- IPCC Guidance Note on Consistent Treatment of Uncertainties (calibrated likelihood/confidence language)
- NATO STANAG/AJP-2.1 Admiralty grading tradition
- CRMinf specification (cidoc-crm.org/crminf)
- Berkeley Protocol on Digital Open Source Investigations (verification chapters; per DR-0008)
