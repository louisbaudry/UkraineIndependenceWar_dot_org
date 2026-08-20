# REQ-OPS — Operations Requirements

**Class:** REQ (DR-0046 control) | **Version:** 1.0 | **Status:** Approved — Effective
**Approval:** founder/principal editor, 2026-08-16 | **Effective:** 2026-08-16
**Supersedes:** — | **Superseded by:** —
**Entries:** OPS-001 … OPS-006

---

### OPS-001 — Collection runs automatically on a configurable source registry; collection never implies publication
**Sources:** §8; Principle 11 · **Satisfied by:** DR-0066, DR-0067
**Verification:** *Test* — collection executes from registry configuration
without code changes per source. *Test* — no path leads from Gate 1 to a
public surface without recorded Gate 2 and Gate 3 decisions.

### OPS-002 — Every release is a baseline with integrity manifest, coverage statement, and changelog
**Sources:** §88–89 · **Satisfied by:** DR-0048, DR-0049
**Verification:** *Test* — release creation fails without an integrity manifest,
coverage statement, changelog, licensing, and pinned versions for every
configuration item (code, schema, registry, collectors, pipelines,
methodology, terminology).

### OPS-003 — Merged/split/retracted object mappings ship with every data release
**Sources:** §91 · **Satisfied by:** DR-0048, DR-0064
**Verification:** *Test* — every data release includes merged, split, and
retracted object mappings; the mappings may be empty but must be present and
machine-readable.

### OPS-004 — Public pages carry revision history from first publication; site snapshots join release baselines
**Sources:** §90 · **Satisfied by:** DR-0052, DR-0048
**Verification:** *Test* — every public page has at least one revision record
dating from its first publication. *Inspection* — site snapshots are
configuration items in release baselines.

### OPS-005 — Independent backups exist and evolve toward geographic and provider redundancy
**Sources:** §7 · **Satisfied by:** DR-0009, DR-0076
**Verification:** *Inspection* — backups exist on infrastructure independent of
the primary. *Demonstration* — an annual restore test is performed and its
outcome recorded, including restoration of an OCFL root and a canonical
dump.

### OPS-006 — Collector coverage, outages, and known gaps are recorded
**Sources:** §57 · **Satisfied by:** DR-0070
**Verification:** *Test* — every collector run produces a coverage record with
items discovered, acquired, skipped with reasons, failed with errors, and
bytes preserved. *Inspection* — per-source coverage statements name outages,
exclusions, and known gaps, and ship with releases.
