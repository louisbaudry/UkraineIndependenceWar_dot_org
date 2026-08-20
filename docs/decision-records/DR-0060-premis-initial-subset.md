# DR-0060 — Initial PREMIS subset

**Category:** preservation / architecture | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-7, SPEC-0001 §3.2 | **Supersedes:** — (resolves Q-02 under DR-0002) | **Superseded by:** —

## Context

DR-0002 adopted PREMIS 3.0 conceptually and deferred the implementation
subset (Q-02).

## Alternatives considered

1. Focused subset with recorded revisit triggers (chosen).
2. Full dictionary (rejected: unused machinery).
3. Include bitstream now (rejected: no current sub-file addressing need).

## Decision

The initial PREMIS scope is:

- **Objects:** representation and file levels — fixity, size, format,
  originalName, storage location.
- **Events:** ingestion, message-digest calculation, fixity check, format
  identification, virus check, capture, migration/normalization — with date,
  agents, linked objects, outcome (including failure), and detail.
- **Agents:** the pipeline-agent registry (DR-0059) serves as PREMIS agents.
- **Rights:** rights-basis statements as an assertion family (§14 permission
  set).
- **Deferred with revisit triggers** (recorded in the registry): bitstream
  level (trigger: sub-file addressing need), environments (trigger:
  format-migration planning at scale), preservation-level semantics.

## Consequences

- Collector and ingestion design (Phase III item 5) has a fixed metadata
  contract.
- Deferrals are visible registry entries, not silent omissions (§41 spirit).
