# REQ-AI — AI Involvement Requirements

**Class:** REQ (DR-0046 control) | **Version:** 1.0 | **Status:** Approved — Effective
**Approval:** founder/principal editor, 2026-08-16 | **Effective:** 2026-08-16
**Supersedes:** — | **Superseded by:** —
**Entries:** AI-001 … AI-003

---

### AI-001 — AI outputs never become canonical without human accountability
**Sources:** §79; Principle 14 · **Satisfied by:** DR-0036, DR-0063, DR-0066, DR-0081
**Verification:** *Test* — an assertion whose asserter is a software agent
cannot reach canonical status without a linked human acceptance record.
*Audit* — sampled canonical assertions of AI origin each carry an accepting
human agent and tier.

### AI-002 — Consequential AI outputs preserve model, instructions, inputs, output, pipeline version, and reviewer disposition
**Sources:** §80 · **Satisfied by:** DR-0003, SPEC-0003 §6
**Verification:** *Test* — consequential AI outputs carry provider, model and
version, instructions, input references, output, pipeline version,
structured-output schema, validation result, reviewer, and disposition.
*Inspection* — routine disposable model calls are exempt by documented rule,
not by omission.

### AI-003 — AI-proposed assertions are beliefs held by a software agent until adopted under human review
**Sources:** §79 · **Satisfied by:** DR-0031, DR-0063
**Verification:** *Test* — AI-generated assertions default to proposal state
with the software agent as asserter; adoption is a separate recorded act
that changes who holds the belief.
