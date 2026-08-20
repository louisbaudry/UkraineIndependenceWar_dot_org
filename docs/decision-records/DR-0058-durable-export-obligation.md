# DR-0058 — Durable export is a standing obligation

**Category:** preservation / architecture | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-5, WP 3.1 §4 | **Supersedes:** — | **Superseded by:** —

## Context

PRES-009: the archive must be reconstructible without the public website —
and, by extension, without the original database software. OAIS
designated-community reasoning (DR-0001) requires holdings to remain
interpretable by future users with future tools.

## Alternatives considered

1. Documented complete dump format exercised at every baseline (chosen).
2. Rely on engine-native backups (rejected: engine-native formats are exactly
   the dependency PRES-009 guards against — they are backup, not archive,
   per DR-0009).

## Decision

The canonical store ships a **documented, complete, software-independent dump
format** — JSONL + CSV with a schema descriptor documenting every element
against the semantic registry (DR-0050) — and the dump is **generated,
fixity-checked, and preserved at every release baseline** (DR-0048,
DR-0005). The dump format specification is a SPEC-class controlled document.

## Consequences

- The archive outlives the database product; succession (DR-0001) and
  institutional deposit receive data in archival formats.
- Dump generation failures block a release the way test failures block a
  deploy — reproducibility is part of release acceptance.
