# DR-0056 — Projection mappings are controlled artifacts

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-3, WP 3.1 §4 | **Supersedes:** — | **Superseded by:** —

## Context

Under DR-0054 every standards surface is a projection. Unmaintained mappings
silently rot interchange; DR-0045 already required documenting FtM export
losses.

## Alternatives considered

1. Versioned SPEC-class mapping documents per surface (chosen).
2. Mappings as code comments/implementation detail (rejected: mappings are
   semantic commitments, not implementation trivia).

## Decision

Each standards surface — RDF (CIDOC CRM, CRMinf, PROV, SKOS, Web Annotation),
FollowTheMoney, BODS, DCAT, and any future interchange format — has a
**versioned SPEC-class mapping document** (DR-0046 control) specifying the
canonical→surface mapping, its generator version, and **documented export
losses** per surface (generalizing DR-0045's obligation). A projection
regenerated under a changed mapping records the mapping version in its
provenance (DR-0003).

## Consequences

- Interchange claims are auditable: "our CRM export means X" has a controlled
  document behind it.
- Mapping changes are visible governance events, not silent drift.
