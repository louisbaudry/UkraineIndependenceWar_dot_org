# DR-0048 — Releases are configuration-management baselines

**Category:** architecture / preservation | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W7-3, WP 0.8 §2.2, §3.3/§5 | **Supersedes:** — | **Superseded by:** —

## Context

Record §88's release-manifest question list is, verbatim, a configuration-
management baseline definition. DR-0009 already separated releases from backup
and archive; this DR fixes what a release *is*.

## Alternatives considered

1. Release = CM baseline over named configuration items (chosen).
2. Release = tagged Git commit (rejected: covers code only; datasets,
   methodology, and terminology versions live outside Git history).
3. Ad hoc release notes (rejected: not reproducible, §88).

## Decision

A **release is a named, frozen baseline**: dataset snapshot, schema version,
ontology/registry version, collector and pipeline versions, methodology
version, terminology/localization version, code commit, and build
configuration — plus an **integrity manifest** (checksums, DR-0005), a
**coverage statement** (§57), known limitations, licensing, and a changelog.
**Merged/split/retracted object mappings ship from the first data release**
(§91). Release manifests are preserved, fixity-checked objects carrying PROV
provenance; epistemic assessments and manifests append under baseline
discipline, never rewrite (§63).

## Consequences

- §86's question — "what exactly did we say, on what evidence, on date Z?" —
  is answered by baseline lookup.
- Site snapshots (DR-0052) are one more configuration item.
- Reproducibility (Principle 16) becomes an auditable property per release.
