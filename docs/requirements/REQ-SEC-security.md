# REQ-SEC — Security & Sensitive Material Requirements

**Class:** REQ (DR-0046 control) | **Version:** 1.0 | **Status:** Approved — Effective
**Approval:** founder/principal editor, 2026-08-16 | **Effective:** 2026-08-16
**Supersedes:** — | **Superseded by:** —
**Entries:** SEC-001 … SEC-004

---

### SEC-001 — Confidential-source identity is architecturally separable from ordinary research data
**Sources:** §11 · **Satisfied by:** DR-0059, DR-0069, POL-0001 §5.6
**Verification:** *Inspection* — the confidential store is a distinct store with
its own access control. *Test* — research-graph queries cannot join to
confidential identity attributes; submissions reference pseudonymous
submitter IDs only.

### SEC-002 — Third-party submissions are quarantined and security-checked before entering the archive
**Sources:** §11 · **Satisfied by:** DR-0069, DR-0066
**Verification:** *Test* — no object enters an OCFL storage root without a
recorded Gate 1 passage including a security-check outcome. *Demonstration*
— a submission carrying a known-malicious test file is stopped in
quarantine.

### SEC-003 — Access control supports the §12 tier set without a universal is_public flag
**Sources:** §12 · **Satisfied by:** DR-0067, SPEC-0001
**Verification:** *Test* — no boolean `is_public` field exists in schema or
registry; every access-controlled object carries an access tier from the
registry vocabulary, with sensitivity, rights, and evidentiary disclosure as
separate dimensions.

### SEC-004 — Restricted graphic material is inaccessible below its access tier at every layer
**Sources:** §10, §12 · **Satisfied by:** DR-0054, DR-0067, POL-0001
**Verification:** *Test* — automated per-tier access tests across the canonical
store, every derived projection, the search index, and published surfaces. A
tier leak in any layer blocks release.
