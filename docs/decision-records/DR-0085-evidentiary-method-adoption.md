# DR-0085 — Adoption of the evidentiary method

**Category:** methodology / epistemology | **Status:** Approved | **Decided:** 2026-08-26 by founder/principal editor
**Origin:** [METH-0001](../methodology/METH-0001-evidentiary-method.md) §17; surfaced by the DR-0048 release-readiness check | **Supersedes:** — (closes DR-0065's retrospective-phrasing open item) | **Superseded by:** —

## Context

§97 requires methodology to be a first-class versioned artifact from the
beginning, and DR-0047 assigns it its own versioning regime. DR-0048 then
requires every release baseline to pin a methodology version. When the
release machinery was implemented, its readiness check reported the
consequence:

```
MISSING  methodology_version    ← no effective METH document exists
```

No release can be created until a METH document is effective. The epistemic
decisions themselves were settled long ago — DR-0008 and DR-0018 through
DR-0037 — but they are scattered across twenty-two records and none of them
is a method a person can follow end to end.

METH-0001 is drafted as that document. It **codifies** those decisions; it
does not originate method. Where it goes beyond them it says so and asks
(§15).

## Alternatives considered

1. **Adopt METH-0001 v1.0, ruling its five open questions** (recommended).
   Unblocks the release path with a method that states its own limits.
2. **Adopt with the open questions deferred** (rejected as a default: §15's
   questions are about how strict the method is on the analyst — Q2's
   confidence cap and Q3's mandatory hypothesis sets in particular. Leaving
   them open means the method is silent exactly where it constrains, which
   is where a method earns its keep. Available if the founder prefers to
   rule them against real cases.)
3. **Split into several METH documents before adopting any** (rejected for
   now: evidentiary method is one movement from source to claim, and
   splitting it before it has been used against real material would draw the
   seams in the wrong places. Later collection and security procedures are
   PROC-class work, not further METH splits.)
4. **Continue deferring** (rejected: no release is possible, and every
   conclusion produced meanwhile is produced under an unrecorded method —
   which is the state §97 exists to prevent.)

## Decision

1. **METH-0001 — Evidentiary Method is adopted as v1.0, Approved — Effective
   2026-08-26**, supplying the `methodology_version` that DR-0047 and
   DR-0048 require.

2. **The five open questions at METH-0001 §15 are ruled**, each put to the
   founder individually and answered individually:

   **Q1 — "Consequential" is a three-part test, any limb sufficing.** A
   conclusion is consequential if it names an identifiable person or entity
   (by name or by any identifier resolving to one), feeds a legal-layer
   conclusion, or would be materially relied on by others. The third limb is
   a judgment made on whether someone reasonably would rely on it, not on
   whether the project intends them to. Rejected: a names-only test, which
   lets through unattributed structural claims that are highly citable; a
   harm-based test, which requires the harm judgment before the review that
   would test it. Enacted at METH-0001 §1.5.

   **Q2 — Unanswered critical questions cap analytic confidence at
   `moderate`.** A hard rule, not a factor to weigh, and independent of the
   defeater type the question implies. It blocks nothing from publication;
   it forbids claiming the top of the scale while a check the scheme itself
   declared necessary stands unperformed. An argued dismissal counts as an
   answer. Rejected: capping only on undermining questions, which depends on
   every question being typed correctly and silently loses force when one is
   not; treating open questions as one input among several, which is the
   failure mode DR-0034 exists to prevent. Enacted at METH-0001 §6.2.

   **Q3 — Competing-hypothesis sets are mandatory in all three cases**,
   including where the project's prior expectation is strong. That case is
   where confirmation bias actually operates, and for a project with an
   explicit interpretive stance it is the trigger that most needs to bind.
   Rejected: mandatory for consequential conclusions only, which lets
   through the routine-looking claim one is certain about; attaching the
   obligation to the review tier, which would mean reconstructing
   alternatives after the conclusion is formed. Enacted at METH-0001 §7.

   **Q4 — A conclusion needing T1 or T2 review that received only
   self-review is recorded `unreviewed` at its tier and published carrying
   that qualification visibly.** Stricter than the drafted version, which
   kept the shortfall internal. §83 holds that a second look by the same
   mind is not an independent judgment; publishing without the caveat would
   quietly imply a review that did not happen, and the reader relying on the
   conclusion is the one person who would not be told. Publication is not
   blocked — presenting the conclusion as reviewed is. Rejected: deferring
   all T1 conclusions until independent review exists, which would silence
   the project for years on exactly the conclusions that matter most.
   Enacted at METH-0001 §10.1.

   **Q5 — One scale, with a registry scope note.** The seven ICD 203 bands
   are unchanged. The `likelihood-bands` entry gains a retrospective scope
   note stating that a band expresses the assessor's credence about a
   determinate past fact rather than a forecast, plus a forbidden
   translation covering renderings that read as prediction — checked
   specifically against Ukrainian and Russian. Rejected: a typed
   prospective/retrospective field on every assessment, near-constant data
   for real overhead; ruling it a non-issue, which ignores that "likely"
   carries a forward-looking sense in ordinary English and a stronger one in
   some other languages. Enacted at METH-0001 §5.4 and in the registry.
   This closes the open item DR-0065 carried forward.

3. **The registry change is editorial** in DR-0080's classification — a
   scope note added, no member, range, or mapping altered — and follows the
   registry process rather than requiring its own DR. Registry version
   0.1.0 → 0.1.1 with a changelog entry.

4. **Substantive method changes become release provenance** under §97: a
   major-version change to METH-0001 requires founder approval and is named
   in the changelog of the next baseline.

5. **Conclusions are not retroactively re-attributed.** Work produced under
   a prior method version keeps pointing at that version.

## Consequences

- The release path unblocks: `create_baseline()` can pin a methodology
  version, leaving `collector_version`, `pipeline_version`, and
  `dataset_snapshot` as the remaining gaps — all of which need a real
  collection run rather than a document.
- EDIT-005's verification (reproducing a published conclusion from its
  baseline, including its methodology version) becomes demonstrable.
- DR-0065's open item on retrospective phrasing is resolved by Q5 or
  explicitly carried forward.
- The method binds the founder as well as future contributors. That is the
  intended effect: a method only self-applied when convenient is not a
  method.
- **Three of the five rulings make the method stricter than the draft
  proposed, and Q4 stricter than was asked for.** The consistent direction
  is toward the reader being told what was and was not done — which is the
  posture §83 and §86 imply but do not spell out.
- **Two rulings create obligations the schema does not yet carry.** Q2's
  confidence cap needs critical-question answers to be recorded per
  assessment before it can be enforced rather than merely followed, and Q4
  needs an `unreviewed` state on a conclusion's review record plus a
  presentation-layer path to surface it. Both are Phase III implementation
  work and neither is built; until they are, both rulings bind as editorial
  discipline rather than as structural constraint. Recorded here rather than
  discovered later.

## Gap noticed while drafting

The requirement set enacted by DR-0082 covers *pinning* a methodology version
(OPS-002) but has **no requirement for §97 itself** — that methodology exist
as a versioned artifact with a version, effective date, changelog, and links
to the releases it governed. The obligation is stated in the record and
carried by DR-0047, but no REQ entry names it or its verification means.

Not added here: the requirement set is enacted, and adding to it is the
founder's act (DR-0051, DR-0082). Proposed as **OPS-007** for the next
requirements revision, verification *Inspection* — an effective METH document
exists carrying version, effective date, and change history, and the release
baseline pins it.
