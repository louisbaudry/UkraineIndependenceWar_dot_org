# REQ-DATA — Data & Identity Requirements

**Class:** REQ (DR-0046 control) | **Version:** 1.0 | **Status:** Approved — Effective
**Approval:** founder/principal editor, 2026-08-16 | **Effective:** 2026-08-16
**Supersedes:** — | **Superseded by:** —
**Entries:** DATA-001 … DATA-010

---

### DATA-001 — Names and identifiers attach via assignment events with provenance
**Sources:** §16–17; Principle 12 · **Satisfied by:** DR-0012, SPEC-0001 §2.2
**Verification:** *Test* — entity records carry no name or identifier columns;
all appellations and identifiers exist as assignment assertions with actor,
time, and basis.

### DATA-002 — Identity merges require evidence; merge/split history is preserved; false merges are costlier than missed matches
**Sources:** §16–17 · **Satisfied by:** DR-0012, DR-0063, DR-0064
**Verification:** *Test* — merge and split events require an evidence reference
and a human agent; confirmation on name similarity alone is rejected at
every tier. *Audit* — lineage is queryable for sampled merged entities, and
predecessors' assertions show explicit re-homing decisions.

### DATA-003 — Roles and memberships are temporal events, never mutable attributes
**Sources:** §18 · **Satisfied by:** DR-0013
**Verification:** *Test* — person records carry no role or office columns; role
tenures exist as events with time-spans and role qualification (acting,
interim, de facto, disputed).

### DATA-004 — Product types and individual items are distinct, linkable objects
**Sources:** §21 · **Satisfied by:** DR-0014
**Verification:** *Inspection* — distinct product-type and individual-item
families exist; items reference their type. *Test* — serial numbers and
individuating identifiers attach to items, not types.

### DATA-005 — Ownership and control are typed interest statements with provenance and validity periods
**Sources:** §19–20 · **Satisfied by:** DR-0040
**Verification:** *Test* — ownership records carry an interest type from the
registry vocabulary, a validity period, and provenance; percentages are
quantity objects per DR-0030. *Inspection* — legal, beneficial, voting, and
control variants are distinct types, never merged.

### DATA-006 — Transactions, shipments, and payments are distinct event types
**Sources:** §68 · **Satisfied by:** DR-0043
**Verification:** *Inspection* — three distinct event families exist and are
linkable without merging. *Test* — customs declarations are documentary
assertions, not conclusions about actual goods or destinations.

### DATA-007 — Territorial statuses are typed temporal relations; competing characterizations coexist
**Sources:** §46 · **Satisfied by:** DR-0044
**Verification:** *Test* — statuses are typed temporal relations with evidence;
multiple competing statuses over one territory and period store and retrieve
intact. *Audit* — authority-attributed characterizations are distinguished
from project assertions.

### DATA-008 — Every consequential data element has one registry-documented meaning
**Sources:** §101 · **Satisfied by:** DR-0050, DR-0078, DR-0079
**Verification:** *Test* — every canonical field maps to a registry entry;
unmapped fields block release. *Test* — enumerated values validate against
the compiled registry projection.

### DATA-009 — Stable public identifiers resolve permanently for citable research objects
**Sources:** §15 · **Satisfied by:** DR-0064
**Verification:** *Test* — the resolver returns a resource, or a documented
redirect or tombstone, for every identifier ever published — including
identifiers of merged, split, and redacted objects. No published identifier
dead-ends.

### DATA-010 — External identifier mappings are typed and provenance-bearing
**Sources:** §16 · **Satisfied by:** DR-0012, DR-0045, DR-0079
**Verification:** *Test* — every external identifier references a registry
identifier-type and carries an assignment assertion with source and date.
