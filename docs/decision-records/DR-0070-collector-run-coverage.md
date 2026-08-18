# DR-0070 — Collector-run coverage record

**Category:** operations / preservation | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-17, SPEC-0003 §8 | **Supersedes:** — | **Superseded by:** —

## Context

Record §57 requires preserving source scope, collector start/end dates,
outages, exclusions, sampling rules, and known coverage gaps, because
frequency in the archive is not frequency in the world (OPS-006). Record §28
makes failed acquisitions historically significant (PRES-007).

## Alternatives considered

1. Collector runs as the unit of coverage accounting (chosen).
2. Per-item records only (rejected: cannot express "the collector was down
   for six days" — an absence with no items to attach to).

## Decision

Each execution is a **collector run** recording: source, start and end,
collector version and configuration, items discovered, acquired, skipped
(with reasons), failed (with errors), and bytes preserved. Runs compose into
**per-source coverage statements** — what was collected, from when, with
which gaps.

- **Failed acquisitions are first-class** (§28): retries, later successes,
  and permanent losses are recorded events; historically significant failures
  are preserved permanently.
- **Outages and exclusions are recorded**, so "absent from the archive" never
  silently reads as "absent from the world" (§57, DR-0029).
- **Coverage statements ship with releases** (DR-0048).

## Consequences

- Corpus bias (§57) is measurable rather than assumed.
- Release consumers receive the coverage caveats with the data.
