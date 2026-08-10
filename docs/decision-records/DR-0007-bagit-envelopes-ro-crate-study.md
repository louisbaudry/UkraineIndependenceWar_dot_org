# DR-0007 — BagIt envelopes; RO-Crate study before evidence-package design

**Category:** preservation | **Status:** Approved | **Decided:** 2026-08-10 by founder/principal editor
**Origin:** CDR-W1-7, WP 0.2 §4.9/§7 | **Supersedes:** — | **Superseded by:** —

## Context

Phase I §92 requires exportable evidence/research packages using "established
archival/forensic packaging standards … rather than inventing a proprietary
package." Packages must self-verify in transfer and at rest.

## Alternatives considered

1. BagIt envelopes now; RO-Crate studied before designing the §92 manifest
   (chosen).
2. BagIt alone, manifest designed ad hoc when needed (rejected: exactly the
   proprietary-package path §92 forbids).
3. Defer everything until packages are needed (rejected: BagIt costs nothing and
   disciplines transfers immediately).

## Decision

**BagIt (RFC 8493)** is the envelope for stored/transferred packages, with BagIt
profiles used to define project package types as they emerge. The design of the
§92 evidence/research-package manifest is **blocked on a study of RO-Crate**
(machine-readable research-object manifests); METS is compared as a structural
alternative in that study.

## Consequences

- Anything leaving or entering the archive travels as a bag with checksum
  manifests (integrates with DR-0005).
- The evidence-package format decision is deferred, deliberately, behind an
  established-standards study — not behind convenience.
- OAIS DIP is the conceptual frame: packages are assembled *from* archival
  holdings for a defined consumer (court, researcher, partner archive).
