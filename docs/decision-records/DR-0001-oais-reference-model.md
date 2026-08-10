# DR-0001 — Adopt OAIS (ISO 14721:2025) as the archival reference model

**Category:** preservation | **Status:** Approved | **Decided:** 2026-08-10 by founder/principal editor
**Origin:** CDR-W1-1, WP 0.2 §7 | **Supersedes:** — | **Superseded by:** —

## Context

Phase I (§6–§7) requires durable archival custody: immutable originals, acquisition
metadata, reconstructibility independent of the public website, eventual
institutional deposit. A reference model for archival *responsibility* was needed
before any implementation design.

## Alternatives considered

1. Adopt OAIS conceptually (chosen).
2. Define a project-specific archival responsibility model (rejected: violates the
   standards-first principle, record §94).
3. Defer until later workstreams (rejected: preservation obligations shape all
   subsequent design).

## Decision

OAIS (ISO 14721:2025 / CCSDS 650.0-M-3) is adopted **conceptually** as the model of
archival responsibility and lifecycle: SIP/AIP/DIP package separation, preservation
planning (including Preservation Watch), designated-community interpretability
(Preservation Objectives), and succession planning. Preservation Description
Information — provenance, context, reference, fixity, access rights — is the
completeness checklist for every preserved object.

No implementation, storage, or serialization commitment is made by this DR.

## Consequences

- Acquisition, preservation, and dissemination remain structurally separate
  (aligned with record Principle 11 and §8).
- Every preserved object must eventually be answerable against the five PDI
  components.
- Succession/institutional deposit (§7) is designed for from the start.
