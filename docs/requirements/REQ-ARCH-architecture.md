# REQ-ARCH — Architecture Requirements

**Class:** REQ (DR-0046 control) | **Version:** 1.0 | **Status:** Approved — Effective
**Approval:** founder/principal editor, 2026-08-16 | **Effective:** 2026-08-16
**Supersedes:** — | **Superseded by:** —
**Entries:** ARCH-001 … ARCH-006

---

### ARCH-001 — Pipeline and world layers are permanently separate; cross-appearing parties are linked, never merged
**Sources:** Principle 1 · **Satisfied by:** DR-0004, DR-0059
**Verification:** *Test* — no foreign key or shared identity exists between the
pipeline-agent and world-actor registries except explicit link assertions.
*Inspection* — no world-layer query path traverses into pipeline data
implicitly.

### ARCH-002 — The six-layer epistemic architecture governs all knowledge modeling
**Sources:** §31 · **Satisfied by:** DR-0024, SPEC-0001 §4
**Verification:** *Inspection* — every canonical object family maps to a named
layer in SPEC-0001; new families require a layer assignment.

### ARCH-003 — Documentary identity follows Work / Expression / Manifestation / Item
**Sources:** §22 · **Satisfied by:** DR-0011, DR-0061
**Verification:** *Inspection* — the four documentary families exist and are
used; derivatives are expressions with PROV lineage, and holdings bridge
Items to preserved representations.

### ARCH-004 — The canonical-representation decision is made against requirements, not technology preference
**Sources:** §95; Principle 17 · **Satisfied by:** WP 3.1, DR-0054
**Verification:** *Inspection* — WP 3.1 records the requirement-derived
comparison of the alternatives, and DR-0054 records the decision and its
rationale.
**Current state:** **satisfied** — decided 2026-08-16 (DR-0054).

### ARCH-005 — A first-class API remains possible; no API contract freezes before the ontology stabilizes
**Sources:** §93 · **Satisfied by:** DR-0054, DR-0056
**Verification:** *Inspection* — no API contract is published before the
ontology and registry stabilize; projections capable of serving one exist
and are versioned.

### ARCH-006 — Access tiers never create competing versions of historical truth
**Sources:** §4; Principle 11 · **Satisfied by:** DR-0054, SEC-003
**Verification:** *Test* — all tiers read the same canonical assertions; tier
affects visibility only, never values. No tier-specific assertion store
exists.
