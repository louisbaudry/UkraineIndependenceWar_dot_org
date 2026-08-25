# DR-0085 — Adoption of the evidentiary method

**Category:** methodology / epistemology | **Status:** Proposed — awaiting founder decision
**Origin:** [METH-0001](../methodology/METH-0001-evidentiary-method.md) §17; surfaced by the DR-0048 release-readiness check | **Supersedes:** — | **Superseded by:** —

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

*Proposed, not yet decided.*

1. **METH-0001 — Evidentiary Method is adopted as v1.0, Approved — Effective**,
   supplying the `methodology_version` that DR-0047 and DR-0048 require.
2. **The five open questions at METH-0001 §15 are ruled** as part of
   approval:
   - **Q1** the test for "consequential";
   - **Q2** whether unanswered critical questions cap analytic confidence;
   - **Q3** whether competing-hypothesis sets are required or recommended
     where the project's prior expectation is strong;
   - **Q4** how self-review is recorded while the project is one person;
   - **Q5** whether retrospective likelihood phrasing needs a distinct
     registry scope note (DR-0065's open item).
3. **Substantive method changes become release provenance** under §97:
   a major-version change to METH-0001 requires founder approval and is
   named in the changelog of the next baseline.
4. **Conclusions are not retroactively re-attributed.** Work produced under
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
