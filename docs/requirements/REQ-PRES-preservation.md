# REQ-PRES — Preservation Requirements

**Class:** REQ (DR-0046 control) | **Version:** 1.0 | **Status:** Approved — Effective
**Approval:** founder/principal editor, 2026-08-16 | **Effective:** 2026-08-16
**Supersedes:** — | **Superseded by:** —
**Entries:** PRES-001 … PRES-012

---

### PRES-001 — Originals are preserved immutably, separate from all derivatives
**Sources:** §7; Principle 1 · **Satisfied by:** DR-0003, DR-0055, DR-0074
**Verification:** *Test* — no write path mutates an OCFL `v1` content file or a
canonical original-representation record outside the DR-0077 redaction path.
*Audit* — annual sample of 20 holdings: `v1` content digest matches the
digest recorded at ingestion.

### PRES-002 — Every preserved object has a SHA-256 digest recorded at ingestion
**Sources:** §7 · **Satisfied by:** DR-0005, DR-0075
**Verification:** *Test* — every preserved object carries a non-null SHA-256 in
both the canonical store and the OCFL fixity block. Zero exceptions; blocks
release.
**Current state:** satisfied for the two documents ingested to date.

### PRES-003 — Periodic fixity checks are performed and recorded as events with outcomes
**Sources:** §7 · **Satisfied by:** DR-0005
**Verification:** *Inspection* — the check cadence is defined in an effective
SPEC. *Test* — every permanent-tier object has a fixity-check event within
the current cadence window; failures are recorded events, never silent
re-copies.

### PRES-004 — Every preserved object is answerable against the five OAIS PDI components
**Sources:** DR-0001 · **Satisfied by:** DR-0001, DR-0073
**Verification:** *Audit* — sample of 20 preserved objects; each answers
provenance, context, reference, fixity, and access-rights information.

### PRES-005 — High-value web sources are captured in WARC
**Sources:** §7 · **Satisfied by:** DR-0006, DR-0067
**Verification:** *Test* — every source whose registry entry sets WARC capture
has WARC-format captures. *Inspection* — the WACZ evaluation is recorded
before the capture toolchain is frozen (DR-0006).

### PRES-006 — Packages that move between systems carry per-file checksum manifests
**Sources:** DR-0005, DR-0007 · **Satisfied by:** DR-0007
**Verification:** *Test* — every exported or transferred package validates as a
BagIt bag with a complete payload manifest.

### PRES-007 — Failed acquisitions are recordable; historically significant failures are preserved permanently
**Sources:** §28 · **Satisfied by:** DR-0002, DR-0060, DR-0070
**Verification:** *Demonstration* — a failed fetch produces a recorded
acquisition event with outcome and error detail. *Audit* — collector-run
failure counts reconcile with recorded failure events.

### PRES-008 — Backup, archival preservation, and releases are governed and stored separately
**Sources:** §7 · **Satisfied by:** DR-0009, DR-0048, DR-0076
**Verification:** *Inspection* — three distinct mechanisms with distinct
retention policies; no shared version identifier across the three.

### PRES-009 — The archive is reconstructible without the public website
**Sources:** §7; Principle 18 · **Satisfied by:** DR-0058, DR-0073
**Verification:** *Demonstration* — from an OCFL storage root plus a canonical
dump alone, and without project code, holdings with their metadata and
provenance are reconstructed. Exercised at each major release.

### PRES-010 — Archival holdings are transferable to a successor archive with PDI intact
**Sources:** §7 · **Satisfied by:** DR-0001, DR-0073
**Verification:** *Inspection* — AIP structure conforms to OCFL and carries
PDI. *Demonstration* — a sample transfer package validates independently of
project software.

### PRES-011 — Retention is multi-stage and source-specific; not everything is archived equally
**Sources:** §9 · **Satisfied by:** DR-0068, DR-0067, DR-0076
**Verification:** *Test* — every acquired item carries a retention tier drawn
from the registry vocabulary; no untiered items exist.

### PRES-012 — Graphic material can be preserved while restricted
**Sources:** §10 · **Satisfied by:** DR-0067, POL-0001 §5.9
**Verification:** *Test* — items flagged graphic default to an access tier above
public and are inaccessible below that tier in the canonical store, every
projection, the search index, and published surfaces. *Audit* — sampled
cross-layer access check.
