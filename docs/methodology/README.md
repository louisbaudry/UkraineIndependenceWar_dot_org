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
| [METH-0001](METH-0001-evidentiary-method.md) | Evidentiary Method | 0.1 | **Draft — Candidate for approval** |

## Why the release path is still blocked

`python3 release/baseline.py --check` reports:

```
MISSING  methodology_version    ← no effective METH document exists
```

and will continue to, because METH-0001 is a **candidate**. The readiness
check reads a METH document's status and refuses a draft deliberately
([DR-0046](../decision-records/DR-0046-unified-document-control.md)): pinning
a draft would claim a release rests on a document carrying no authority.
Approval, not the file's existence, is what clears the gap.

Adoption is proposed in
[DR-0085](../decision-records/DR-0085-evidentiary-method-adoption.md), which
also puts METH-0001 §15's five open questions to the founder for ruling.

## Provenance

| Document | SHA-256 at deposit | Deposited | Origin |
|---|---|---|---|
| METH-0001 v0.1 (draft) | `bd9dce9dfc65dbe1229eec9c2e0cda19979c464110fd2b8f795ecf6554dbd710` | 2026-08-25 | AI-drafted (Anthropic Claude Code agent session) at the founder's direction. Codifies DR-0008 and DR-0018…DR-0037; originates no method. Passages exceeding those decisions are marked as open questions at §15 |

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
