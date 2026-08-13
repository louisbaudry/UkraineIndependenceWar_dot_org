# DR-0052 — Public site revision history from the first page

**Category:** preservation / architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W7-7, WP 0.8 §3.6/§5 | **Supersedes:** — | **Superseded by:** —

## Context

Record §90: maintain page/content revision history from the beginning; create
whole-site snapshots at significant releases; public browsability may remain a
later product decision.

## Alternatives considered

1. Revision history from the first page + snapshots at releases (chosen).
2. Add history "when the site matters" (rejected: the beginning is the only
   moment history can start from the beginning).

## Decision

Every public page carries **revision history from its first publication**.
**Whole-site snapshots** are created at significant releases and enter the
release baseline as a configuration item (DR-0048). Snapshot mechanics (WARC
of the live site per DR-0006 vs static-build archive) are decided at the first
public release (WP 0.8 §6 Q5). Whether historical revisions are publicly
browsable remains a later product decision (§90).

## Consequences

- "What did the site say on date D" is answerable from launch (§86, §90).
- The publication layer's history composes with, but never substitutes for,
  the archival layer (Principle 18: the website is a projection).
