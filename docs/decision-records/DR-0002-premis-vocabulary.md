# DR-0002 — Adopt PREMIS 3.0 as the preservation-metadata vocabulary

**Category:** preservation | **Status:** Approved | **Decided:** 2026-08-10 by founder/principal editor
**Origin:** CDR-W1-2, WP 0.2 §7 | **Supersedes:** — | **Superseded by:** —

## Context

Phase I (§7, §26, §28) requires recording what the archive holds, at what level of
completeness, what was done to it, by whom, with what outcome — including failed
acquisitions.

## Alternatives considered

1. Adopt PREMIS 3.0 as vocabulary (chosen).
2. Design a custom preservation-metadata dictionary (rejected: §94).
3. Use PROV alone (rejected: PROV lacks preservation-specific semantics — fixity,
   object levels, rights bases, event outcome vocabulary).

## Decision

PREMIS 3.0 (Library of Congress) is adopted as the **conceptual vocabulary** for
preservation metadata: intellectual entities; objects at representation/file/
bitstream levels; typed events with dates, agents, and outcomes (including
failure); agents including software; rights statements with bases.

Serialization and implementation (XML, OWL, relational) are **deferred to
Phase III** (open question WP 0.2 §8 Q1: which subset of the dictionary the
project actually needs).

## Consequences

- Failed acquisitions (§28) are recordable as first-class events with outcomes.
- Holdings-completeness distinctions (§26: original/fragment/metadata-only) map to
  PREMIS object descriptions.
- The PREMIS rights entity carries the rights dimension of §12/§14; the other
  access dimensions (tier, sensitivity, evidentiary disclosure) are explicitly
  **not** PREMIS's job.
