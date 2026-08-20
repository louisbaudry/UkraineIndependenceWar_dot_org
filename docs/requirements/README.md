# Requirements (REQ class)

Controlled documents under [DR-0046](../decision-records/DR-0046-unified-document-control.md),
managed per [DR-0051](../decision-records/DR-0051-requirements-management.md).
Enacted 2026-08-16 from [Phase II output 6](../phase-2/outputs/06-candidate-requirements.md),
with verification criteria completed at enactment.

**73 requirements across the ten record §99 categories.**

| Document | Category | Count |
|---|---|---|
| [REQ-PRES](REQ-PRES-preservation.md) | Preservation | 12 |
| [REQ-EVID](REQ-EVID-evidence-epistemics.md) | Evidence & epistemics | 15 |
| [REQ-SEC](REQ-SEC-security.md) | Security & sensitive material | 4 |
| [REQ-LEGAL](REQ-LEGAL-legal-layer.md) | Legal layer | 9 |
| [REQ-DATA](REQ-DATA-data-identity.md) | Data & identity | 10 |
| [REQ-ARCH](REQ-ARCH-architecture.md) | Architecture | 6 |
| [REQ-EDIT](REQ-EDIT-editorial.md) | Editorial | 5 |
| [REQ-AI](REQ-AI-ai-involvement.md) | AI involvement | 3 |
| [REQ-I18N](REQ-I18N-language-terminology.md) | Language & terminology | 3 |
| [REQ-OPS](REQ-OPS-operations.md) | Operations | 6 |

## Document structure

One controlled document per category; each requirement is an entry with its
own stable ID, statement, sources, satisfying decisions, and verification
criteria. Requirement IDs are permanent and never reused. A requirement is
superseded by recording it in its entry and in the document's change
history — the entry is never deleted (consistent with DR-0080's registry
discipline).

## In force vs satisfied

**A requirement is in force from its effective date regardless of whether
anything yet implements it.** Verification happens when there is something
to verify. Entries carry a *Current state* note only where it is presently
notable — satisfied, partially satisfied, or blocked. Absence of a note
means: in force, not yet verifiable, no implementation exists.

## Verification methods

| Method | Meaning |
|---|---|
| **Test** | Automated check. Failure blocks a release baseline (DR-0048) |
| **Inspection** | Documented check that a controlled document, schema, or configuration says what is required |
| **Audit** | Periodic sampled review with a recorded outcome |
| **Demonstration** | The system is shown to perform the behaviour end to end |

## Traceability

Each entry cites its **Sources** (Phase I record sections and principles)
and the **decisions that satisfy it** (DRs, SPECs, POLs), completing the
record §99 chain: objective → requirement → Decision Record → specification
→ implementation → verification → methodology → release.
