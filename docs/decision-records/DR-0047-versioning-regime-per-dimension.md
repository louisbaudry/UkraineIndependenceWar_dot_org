# DR-0047 — One versioning regime per dimension

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W7-2, WP 0.8 §3.2/§5 | **Supersedes:** — | **Superseded by:** —

## Context

Record §87 lists at least ten version dimensions and warns against imposing
SemVer everywhere. Practice confirms: version regimes should follow consumer
need, not uniformity.

## Alternatives considered

1. Per-dimension regimes per the WP 0.8 §3.2 table (chosen).
2. SemVer everywhere (rejected: §87's explicit warning; meaningless for
   datasets and governance documents).
3. Dates everywhere (rejected: loses compatibility semantics for code/APIs).

## Decision

- **Code / APIs / database schemas:** SemVer; API deprecation policy required
  when a public API exists (§93); schema migrations are first-class artifacts.
- **Ontology / vocabulary / registry:** explicit versions; meaning-changing
  edits require deprecation, replacement mappings, and migration notes (§96);
  structural changes by DR (DR-0025).
- **Dataset/content releases:** immutable snapshot identifiers (date-based
  sequence) with manifests (DR-0048).
- **Collectors / pipelines / prompts:** versioned configurations; every run
  records the versions used (§80, DR-0003).
- **Methodology (METH):** version + effective date + changelog (§97); a
  significant methodology change is release provenance.
- **Terminology/localization:** versioned resources; releases pin the version
  used (§60–61).
- **Governance documents:** document-control status and dates (DR-0046); no
  SemVer.

## Consequences

- "Which version?" is always answered per dimension; no single "website
  version" number exists (§87).
- Release baselines (DR-0048) reference one version per dimension.
