# DR-0049 — DCAT for release description; DataCite DOIs when release practice is mature

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W7-4, WP 0.8 §2.5/§5 | **Supersedes:** — | **Superseded by:** —

## Context

Record §89 requires dataset releases with documentation, checksums, manifests,
licensing, and eventually DOIs "where mature and appropriate." WP 0.1 set
DataCite's disposition as adopt-for-release-layer.

## Alternatives considered

1. DCAT immediately for release description; DataCite DOIs when mature (chosen).
2. DOIs from the first release (rejected: premature; registration route not
   yet chosen).
3. No standard release description (rejected: §94).

## Decision

The release register is expressed in **DCAT** (datasets and distributions) from
the first release, making releases machine-readable and harvestable. **DataCite
DOIs** are minted for public dataset releases **once release practice is
mature**; the registration route (direct membership vs institutional partner)
is an operational decision recorded when taken (WP 0.8 §6 Q2). Citation
rendering uses CSL (DR-0022); web discovery uses Schema.org mapping
(publication layer only, per WP 0.1).

## Consequences

- Releases are citable and discoverable without waiting on DOI operations.
- The DOI decision cannot be made silently — it requires a recorded
  operational decision.
