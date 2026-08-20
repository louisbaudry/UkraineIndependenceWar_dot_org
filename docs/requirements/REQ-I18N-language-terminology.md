# REQ-I18N — Language & Terminology Requirements

**Class:** REQ (DR-0046 control) | **Version:** 1.0 | **Status:** Approved — Effective
**Approval:** founder/principal editor, 2026-08-16 | **Effective:** 2026-08-16
**Supersedes:** — | **Superseded by:** —
**Entries:** I18N-001 … I18N-003

---

### I18N-001 — Original-language material is primary; translations are derived expressions with provenance
**Sources:** §58 · **Satisfied by:** DR-0011, DR-0003
**Verification:** *Test* — every translation expression references its source
expression and carries translator or provider, human-vs-machine, review
status, translation version, and the source version translated.
*Test* — quotation, paraphrase, and summary remain distinct types.

### I18N-002 — Important concepts have per-language preferred terms, definitions, and forbidden-translation notes in the registry
**Sources:** §60 · **Satisfied by:** DR-0050, DR-0079, DR-0081
**Verification:** *Test* — registry entries in `effective` status carry an
English `prefLabel` and definition; translated labels carry translator, date,
and review status. *Inspection* — forbidden-translation notes exist for
terms whose mistranslation would collapse a conflict-register distinction or
shift a likelihood band's meaning.

### I18N-003 — Canonical semantics and user-facing wording are separate; presentation resources are versioned
**Sources:** §61 · **Satisfied by:** DR-0047, DR-0054, DR-0065
**Verification:** *Test* — the canonical store holds identifiers, not display
strings, for registry-governed values. *Inspection* — localization and
presentation resources carry versions, and release baselines pin the
terminology and localization versions used.
