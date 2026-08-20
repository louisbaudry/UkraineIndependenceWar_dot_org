# Phase II / Workstream 5 — Argumentation Concept Map
## Working Paper 0.6

**Project:** Ukraine's Second War of Independence
**Status:** CANDIDATE — AI-drafted, awaiting founder review and approval. Nothing in this paper is canonical.
**Version:** 0.6 (first draft of Workstream 5)
**Mandate:** WP 0.1 research sequence item 5 — premises, conclusions, defeaters, competing hypotheses; the argumentation formalism deferred by DR-0031.
**Constraints inherited:** DR-0024 (layer 6 of the epistemic architecture), DR-0031 (CRMinf I1/I5 as the activity grounding), DR-0026 (uncertainty model), DR-0028 (dependence typing), record §79 (human accountability for consequential conclusions).

### AI provenance (per Phase I record §80)

| Field | Value |
|---|---|
| Drafted by | AI assistant (Anthropic Claude Code agent session), continuing the founder-directed workstream sequence |
| Date | 2026-08-11 |
| Inputs | Phase I record (§34–§36, §40, §52–§53, §76 centrally); WP 0.1–0.5; DR-0001…0031 |
| Human review | **Pending** — founder is final editor (record §78) |
| Disposition | Candidate working paper; all candidate Decision Records herein are proposals |

---

## 1. Scope and method

DR-0024 fixed layer 6 as "arguments — inference/defeater structure, formalism
per Workstream 5"; DR-0031 grounded it in CRMinf's argumentation/inference
activities. This paper selects the *structure inside* those activities: how
premises, conclusions, inference steps, defeaters, and competing hypotheses are
represented. It surveys argumentation theory and its computational tradition,
then composes a candidate that composes with everything already adopted.

Two disciplines' requirements dominate: intelligence analysis (competing
hypotheses, discriminating evidence — §35) and legal/evidential reasoning
(inference chains, defeaters, standards of support — §34, §62).

## 2. Discipline survey

### 2.1 Toulmin's model

Claim, grounds (data), warrant, backing, qualifier, rebuttal. Strengths: a
teachable editorial scaffold; the *qualifier* slot maps directly onto DR-0026's
likelihood bands; the *warrant* makes the usually-implicit inference rule
explicit. Weakness: informal, no compositional semantics, unsuited as a storage
model. Best role: **presentation and editorial discipline**, not data.

### 2.2 Wigmore charts

The legal tradition's evidence-marshalling graphs: propositions and evidential
force relations composed into trees supporting an ultimate probandum. Historical
ancestor of modern evidence mapping; validates the project's aim of *visible
inference chains for consequential conclusions* (§34). Its lesson is the
practice — chart the chain for the hard cases — more than the notation.

### 2.3 Abstract argumentation (Dung)

Arguments as nodes, *attack* as a relation, acceptability computed by semantics
(grounded, preferred, stable extensions). Strengths: rigorous treatment of
conflict; the attack relation cleanly represents unresolved contradiction (§40)
without averaging. Weakness for this project: abstract acceptability computation
deciding outcomes would violate §79 (human accountability) and §40 (do not
resolve contradictions mechanically). Role: **analytic aid at most, never
adjudicator**.

### 2.4 Structured argumentation (ASPIC+, ABA, defeasible logic)

Adds internal structure: strict vs defeasible rules, premises, and the
three-way defeater typology that legal and epistemological practice both use:

- **rebutting** — attacking the conclusion itself;
- **undercutting** — attacking the inference link (the warrant), leaving the
  premises intact;
- **undermining** — attacking a premise.

This typology is directly required by the record's cases: an authentic document
whose *interpretation* is challenged (undercut) differs from a forged document
(undermine) and from counter-evidence (rebut). §38's authenticity/veracity
split maps onto undermine-vs-rebut naturally.

### 2.5 AIF (Argument Interchange Format)

The established interchange ontology for argument structures: **I-nodes**
(information: propositions) and **S-nodes** (schemes applied), where S-nodes
divide into rule application (inference), conflict application (attack), and
preference application (priority). AIF is the field's answer to "how do
argument graphs interoperate" — the analogue of what PROV is for provenance.
It composes conceptually with CRMinf (both reify reasoning as typed nodes/
activities) and is the obvious *map-to* target for export.

### 2.6 Argument schemes (Walton)

Presumptive reasoning patterns with attached **critical questions** — argument
from witness testimony, from expert opinion, from sign/indicator, from
appearance, from precedent. The critical questions are structured defeater
prompts: for witness testimony — was the witness positioned to observe? is the
witness biased? is the account internally consistent? corroborated
independently? This is precisely OSINT verification practice (Berkeley
Protocol, DR-0008) rendered as reusable structure, and it operationalizes §53:
attributing deception requires answering *specific* critical questions with
evidence, not gesturing at falsity.

### 2.7 ACH (Analysis of Competing Hypotheses)

Hypothesis set × evidence matrix, scoring consistency/inconsistency, seeking
the hypothesis with least inconsistent evidence, and privileging
**discriminating evidence** (§35). Structurally: ACH cells are evidence-
proposition relations (DR-0024 layer 3) restricted to a hypothesis set — which
means ACH needs no separate data model, only first-class hypothesis sets and a
matrix *view*.

## 3. Composition (candidate)

| Layer | Element | Source |
|---|---|---|
| Activity grounding | Argumentation/inference-making activities by agents over time | CRMinf I1/I5 (DR-0031) |
| Argument structure | Propositions (I-nodes) + typed scheme applications: inference / conflict / preference | AIF pattern, mapped not reinvented |
| Inference typing | Strict vs defeasible support; three defeater types: rebut / undercut / undermine | Structured-argumentation tradition |
| Scheme library | Seed set of Walton-style schemes with critical questions, tuned to OSINT/legal/historical work | Walton; Berkeley Protocol practice |
| Hypothesis competition | First-class hypothesis sets; typed evidence relations (supports / contradicts / discriminates / neutral); ACH matrices as derived views | Heuer; record §35 |
| Editorial scaffold | Toulmin slots for drafting/presenting consequential conclusions | Toulmin |
| Qualifiers | DR-0026 likelihood/confidence, attached to conclusions | already adopted |

Design stance running through all of it: **arguments are recorded, never
auto-adjudicated.** Formal semantics may flag inconsistencies or unattacked
defeaters as *analytic aids*; no computation determines a project conclusion.
Consequential conclusions remain human inference-making records (§79) whose
argument structure is visible and attackable.

## 4. Requirement check

- **§34** inference chains preserved and visible → structure above; derived
  assertions cite their premises and scheme.
- **§35** competing hypotheses, discriminating evidence → hypothesis sets +
  typed relations; ACH as view; negative findings (§76) enter as evidence.
- **§36/DR-0028** dependence → corroboration arguments must cite independent
  lines; a dependence relation *undercuts* a corroboration argument — the
  defeater machinery and the dependence typing interlock.
- **§40** unresolved contradiction → standing conflict (attack) relations with
  no forced resolution; "unresolved" is a legitimate, visible end-state.
- **§52–53** capability/intent/attribution ladders; deception attribution →
  scheme-per-rung with critical questions; intent and coordination claims
  (§56) require their own schemes and evidence, never inference from capability
  or similarity alone.
- **§74–75** research notebooks, questions, gaps → hypothesis sets and open
  critical questions double as the structured research-question inventory.

## 5. Candidate conflict-register entries (additions)

| Term | Colliding senses | Resolution direction (candidate) |
|---|---|---|
| **argument** | Reasoning structure (technical) vs dispute (colloquial) | Technical sense only in modeling documents |
| **attack** | Argumentation-theoretic conflict relation vs military attack (world layer) | Layer-qualified always; conflict-relation vs world-event can never share a term unqualified (extends DR-0004's discipline) |
| **scheme** | Walton argument scheme vs generic "schema" | "Argument scheme" spelled out; "schema" reserved for data structures |
| **support** | Evidential support (layer 3) vs inferential support (layer 6) vs colloquial | Evidence-relation vs inference-relation named distinctly in the registry |
| **hypothesis** | §30 epistemic category (member of competing set) vs loose "guess" | §30 sense only; a hypothesis belongs to a hypothesis set with evidence relations |

## 6. Candidate Decision Records (proposals only — require founder approval)

- **CDR-W5-1:** Adopt the **argument representation**: CRMinf argumentation/
  inference activities carry AIF-patterned structure — propositions plus typed
  scheme applications (inference / conflict / preference) — mapped to AIF for
  interchange, not reinvented.
- **CDR-W5-2:** Adopt **defeater typing**: rebut (attacks conclusion), undercut
  (attacks inference), undermine (attacks premise) — with §38's authenticity
  challenges entering as undermining and interpretation challenges as
  undercutting.
- **CDR-W5-3:** Adopt a **seed argument-scheme library** with critical
  questions, tuned to the project's evidence types (witness testimony, expert
  opinion, sign/indicator, document authenticity, geolocation, image
  verification, coordination attribution); schemes live in the semantic
  registry; additions by registry process, not by DR each time.
- **CDR-W5-4:** **Hypothesis competition is first-class:** hypothesis sets with
  typed evidence relations (supports / contradicts / discriminates / neutral);
  ACH matrices are derived views over these relations, not separate data
  (record §35).
- **CDR-W5-5:** **No automatic adjudication:** formal acceptability semantics
  and consistency checks may serve as analytic aids; no computation determines
  a project conclusion; consequential conclusions are human inference-making
  records with visible, attackable structure (§79).
- **CDR-W5-6:** **Toulmin as editorial scaffold only:** consequential published
  conclusions are drafted/reviewed against the Toulmin slots (claim, grounds,
  warrant, qualifier, rebuttal), with the qualifier drawn from DR-0026;
  Toulmin is not a storage model.

## 7. Unresolved research questions (feed Phase II output 7)

1. Initial scheme-library contents and their critical-question sets — drafted
   with the methodology (METH) documents, tested on the first real
   investigations.
2. Reification granularity: which inferences are worth full argument structure
   vs a simple premise-list? (Candidate rule: risk-tiered per §78 — the review
   tier determines the required structure depth.)
3. Whether/when Dung-style consistency checking is worth implementing as an
   analytic aid (Phase III+; no commitment).
4. Bayesian/probabilistic argumentation — remains deferred with WP 0.5 §11 Q3.
5. Propaganda-narrative analysis (§54): are narrative variants and debunks
   argument structures, or a separate documentary pattern using conflict
   relations? (Test on real cases.)
6. Export shape: exact AIF serialization mapping for evidence packages
   (DR-0007's RO-Crate study is the natural carrier).

## 8. Sources

- Toulmin, *The Uses of Argument* (1958)
- Wigmore, *The Science of Judicial Proof* (evidence charting)
- Dung, "On the acceptability of arguments…" (1995) — abstract argumentation
- Prakken et al., ASPIC+; Dung/Kowalski/Toni, assumption-based argumentation
- Chesñevar et al. / Rahwan et al., Argument Interchange Format (AIF)
- Walton, Reed & Macagno, *Argumentation Schemes* (2008)
- Heuer, *Psychology of Intelligence Analysis* (ACH); Heuer & Pherson, *Structured Analytic Techniques*
- Berkeley Protocol on Digital Open Source Investigations (verification practice; DR-0008)
