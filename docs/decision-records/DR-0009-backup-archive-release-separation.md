# DR-0009 — Backup, archival preservation, and releases are separate

**Category:** preservation | **Status:** Approved | **Decided:** 2026-08-10 by founder/principal editor
**Origin:** CDR-W1-9, WP 0.2 §4.10/§7 | **Supersedes:** — | **Superseded by:** —

## Context

Phase I §7 requires distinguishing "backup, archival preservation, and frozen
research releases." The three are routinely conflated in practice ("we have
backups" ≠ "we preserve" ≠ "we published a citable snapshot").

## Alternatives considered

1. Three-way separation in governance, storage, and versioning (chosen).
2. Treat archive-plus-backups as sufficient, releases as website exports
   (rejected: releases lose identity, citability, and reproducibility; §88–89).
3. Defer until storage design (rejected: the distinction shapes storage design,
   not the reverse).

## Decision

- **Backup** — bit-level disaster recovery of storage; infrastructure below the
  archival layer; no preservation semantics of its own.
- **Archival preservation** — OAIS-managed holdings under preservation planning,
  fixity monitoring (DR-0005), and format watch.
- **Frozen research release** — a versioned, citable snapshot with its own
  identity, manifest, coverage statement, and provenance (DataCite layer per
  WP 0.1 §I; details in Workstream 7).

By default the three never share a mechanism, a version number, or a retention
policy.

## Consequences

- "We have backups" can never satisfy a preservation requirement, nor vice versa.
- Release manifests are themselves preserved, fixity-checked objects with PROV
  provenance (WP 0.2 §4.12).
- Versioning dimensions (§87) develop independently per layer in Workstream 7.
