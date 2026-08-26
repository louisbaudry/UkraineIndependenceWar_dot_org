# Methodology (METH class)

Controlled documents under [DR-0046](../decision-records/DR-0046-unified-document-control.md):
stable IDs, explicit status, approval and effective dates, supersession links.
Status is document metadata, never inferred from Git.

Record §97 makes methodology **a first-class versioned artifact from the
beginning**, with a version, an effective date, a changelog, and links to the
dataset and release versions it governed. [DR-0047](../decision-records/DR-0047-versioning-regime-per-dimension.md)
gives it its own versioning regime; [DR-0048](../decision-records/DR-0048-releases-are-baselines.md)
requires every release baseline to pin it.

| ID | Title | Version | Status |
|---|---|---|---|
| [METH-0001](METH-0001-evidentiary-method.md) | Evidentiary Method | 1.0 | **Approved — Effective 2026-08-26** |

## The five rulings taken on approval

METH-0001 v0.1 went beyond enacted decisions in five places and said so. The
founder ruled each individually on 2026-08-26, enacted by
[DR-0085](../decision-records/DR-0085-evidentiary-method-adoption.md):

| | Question | Ruling |
|---|---|---|
| Q1 | The test for "consequential" | Three-part test, any limb sufficing (METH-0001 §1.5) |
| Q2 | Do unanswered critical questions cap confidence? | Hard cap at `moderate` (§6.2) |
| Q3 | Are competing-hypothesis sets mandatory? | Mandatory in all three cases, strong prior included (§7) |
| Q4 | Self-review while the project is one person | Recorded `unreviewed` at tier and **published carrying that qualification** (§10.1) |
| Q5 | Retrospective likelihood phrasing | One scale, registry scope note; closes DR-0065's open item (§5.4) |

Three made the method stricter than the draft proposed; Q4 made it stricter
than was asked for.

**Two of them are not yet enforceable.** Q2's cap needs critical-question
answers recorded per assessment, and Q4 needs an `unreviewed` state on a
conclusion's review record plus a presentation path to surface it. Neither is
built. Until they are, both bind as editorial discipline rather than as
structural constraint — recorded in DR-0085 rather than left to be discovered.

## Effect on the release path

`python3 release/baseline.py --check` now pins `methodology_version 1.0`. The
remaining unpinned items — `collector_version`, `pipeline_version`,
`dataset_snapshot` — need a real collection run rather than a document.

## Provenance

| Document | SHA-256 at deposit | Deposited | Origin |
|---|---|---|---|
| METH-0001 v0.1 (draft) | `bd9dce9dfc65dbe1229eec9c2e0cda19979c464110fd2b8f795ecf6554dbd710` | 2026-08-25 | AI-drafted (Anthropic Claude Code agent session) at the founder's direction. Codifies DR-0008 and DR-0018…DR-0037; originates no method. Passages exceeding those decisions were marked as open questions at §15 |
| METH-0001 v1.0 (approved) | `e11f61ec306da61de963ed1078b9f553353170b0b38d0ccd3630b3ff1c716106` | 2026-08-26 | v0.1 approved by the founder with the five §15 questions ruled individually (DR-0085); §1.5, §5.4, §6.2, §7 and §10.1 aligned to the rulings |

## Scope of this class

METH documents state **how the project reasons**. They are distinct from:

- **SPEC** — how a system is built (SPEC-0001…0006);
- **POL** — what the project permits and forbids (POL-0001);
- **PROC** — step-by-step operating procedures, none yet written;
- **REQ** — what must be true, with verification means;
- **DR** — the decisions everything else rests on.

Collection procedure written against Berkeley Protocol guidance
([DR-0008](../decision-records/DR-0008-custody-claims-discipline.md)) is
PROC-class work and does not belong here.
