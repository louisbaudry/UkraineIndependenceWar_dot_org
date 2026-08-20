# REQ-LEGAL — Legal Layer Requirements

**Class:** REQ (DR-0046 control) | **Version:** 1.0 | **Status:** Approved — Effective
**Approval:** founder/principal editor, 2026-08-16 | **Effective:** 2026-08-16
**Supersedes:** — | **Superseded by:** —
**Entries:** LEGAL-001 … LEGAL-009

---

### LEGAL-001 — No boolean sanctioned property exists anywhere in the system
**Sources:** §64 · **Satisfied by:** DR-0038
**Verification:** *Test* — automated scan of schema, registry, and projections
finds no boolean `sanctioned` / `is_sanctioned` field. Any occurrence blocks
release.

### LEGAL-002 — The system answers: which restrictions applied, under which authority and jurisdiction, to whom, during what period
**Sources:** §3 · **Satisfied by:** DR-0038, DR-0041
**Verification:** *Demonstration* — for a given entity and date, a query returns
applicable restrictions with authority, jurisdiction, instrument, effect,
and period, distinguishing direct designation from rule-derived
applicability.

### LEGAL-003 — Designation records are distinct from canonical entities; mapping is evidence-backed, never fuzzy-matched
**Sources:** §72 · **Satisfied by:** DR-0039, DR-0063
**Verification:** *Test* — designation→entity mappings require an evidence
reference and a confirming human agent at tier T1. *Audit* — sampled
confirmed mappings show discriminating evidence beyond name or
transliteration similarity.

### LEGAL-004 — Rule-derived applicability is computed, versioned, path-preserving, and never displayed as designation
**Sources:** §71, §73 · **Satisfied by:** DR-0041, DR-0040
**Verification:** *Test* — every applicability conclusion carries its ownership
path, source statements, rule identity and version, jurisdiction,
computation date, and software version; applicability conclusions cannot be
written into designation records. *Audit* — published wording distinguishes
designated from rule-derived.

### LEGAL-005 — Export-control state decomposes into classification, requirement, authorization, and violation-as-finding
**Sources:** §65–66 · **Satisfied by:** DR-0042, DR-0014
**Verification:** *Inspection* — distinct object families exist for
classification assertions, licensing requirements, authorizations, and legal
findings. *Test* — no field conflates "license required" with "license
absent" or "violation established".

### LEGAL-006 — Legal findings carry jurisdiction, authority, standard of proof, and procedural posture; never merged with project conclusions
**Sources:** §62 · **Satisfied by:** DR-0024, DR-0042
**Verification:** *Test* — legal-finding records require jurisdiction, authority,
and posture; no merge path exists between legal findings and project
assertions.

### LEGAL-007 — The project never asserts legal chain of custody as a status
**Sources:** §6 · **Satisfied by:** DR-0008
**Verification:** *Test* — automated scan of published text and API surfaces for
"chain of custody" outside permitted framings (describing others' claims, or
labelled documented custody history). *Inspection* — publication templates
carry no such claim.

### LEGAL-008 — Preservation rights and republication rights are recorded separately per §14's permission set
**Sources:** §14 · **Satisfied by:** DR-0002, DR-0067
**Verification:** *Test* — rights statements carry the §14 permission set (may
preserve / display / redistribute / provide to subscribers) with `unknown`
as an explicit registry value, never a null.

### LEGAL-009 — A formal personal-data policy exists before broad automated collection begins
**Sources:** §13 · **Satisfied by:** POL-0001, DR-0071, DR-0072
**Verification:** *Inspection* — POL-0001 is effective **and** its §10 external
legal review is recorded before collection scope expands beyond DR-0071's
limits.
**Current state:** **partially satisfied** — POL-0001 effective 2026-08-16;
the §10 legal review is outstanding, so DR-0071's interim constraints
continue to bind collection scope.
