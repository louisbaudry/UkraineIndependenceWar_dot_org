# DR-0082 — Enactment of the requirement set

**Category:** architecture / methodology | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** DR-0051; Phase II output 6 | **Supersedes:** — | **Superseded by:** —

## Context

DR-0051 established requirements management per record §99 and deferred the
candidate requirement set's enactment to a consolidation step. Phase II
output 6 delivered the candidates with verification criteria marked as
sketches to be completed at enactment.

## Alternatives considered

1. One REQ-class controlled document per category, requirements as entries
   with individual IDs (chosen).
2. One controlled document per requirement — 73 documents (rejected:
   disproportionate ceremony for entries of a few lines each; category
   documents match established requirements practice while preserving
   per-requirement identity and supersession).
3. A single requirements document (rejected: category-level status and
   change history are useful and cheap).

## Decision

The **73 requirements** across the ten record §99 categories are enacted as
**ten REQ-class controlled documents**, effective 2026-08-16:
REQ-PRES (12), REQ-EVID (15), REQ-SEC (4), REQ-LEGAL (9), REQ-DATA (10),
REQ-ARCH (6), REQ-EDIT (5), REQ-AI (3), REQ-I18N (3), REQ-OPS (6).

Each entry carries a stable, never-reused ID, its statement, sources
(record sections and principles), the decisions that satisfy it, and
**completed verification criteria** drawn from four methods: Test
(automated, failure blocks a release baseline), Inspection, Audit, and
Demonstration.

**In force ≠ satisfied.** A requirement binds from its effective date
regardless of whether anything yet implements it; entries carry a *current
state* note only where presently notable.

Superseding a requirement is recorded in its entry and the document's change
history; entries are never deleted.

## Consequences

- The record §99 traceability chain is closed from objective through
  requirement, Decision Record, and specification, with verification
  criteria defined in advance of implementation.
- Two current states are recorded at enactment: **ARCH-004 satisfied**
  (canonical representation decided against requirements, DR-0054), and
  **LEGAL-009 partially satisfied** (POL-0001 effective; its §10 legal
  review outstanding, so DR-0071's collection constraints continue to bind).
- **Correction:** Phase II output 6 was described at delivery as containing
  63 requirements; the register contains 73. The count was corrected in the
  Phase II index and WP 3.1 at enactment. No requirement content changed.
