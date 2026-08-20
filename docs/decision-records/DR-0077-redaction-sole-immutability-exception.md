# DR-0077 — Governed redaction is the sole exception to storage immutability

**Category:** preservation / legal | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-24, WP 3.3 §6 | **Supersedes:** — | **Superseded by:** —

## Context

DR-0055 permits deletion only as governed redaction with a tombstone;
POL-0001 §6 routes granted erasure requests through that path. OCFL's
guarantees assume content is never purged, so redaction is the one operation
that breaks them.

## Alternatives considered

1. Redaction as the single, governed exception (chosen).
2. No purging ever (rejected: legal and privacy obligations under §77 and
   POL-0001 can require removal).
3. Ordinary deletion capability (rejected: would make every immutability
   guarantee conditional).

## Decision

**Governed redaction is the only permitted exception** to OCFL
immutability. It requires: a recorded decision citing its ground (legal
restriction, privacy removal, or archival withdrawal per §77), content
purged and the inventory corrected, and a **preservation event plus
tombstone retained** recording the fact, date, authority, and grounds of
removal without the removed content.

No other operation removes or rewrites archived content. Redaction is never
silent, and its effect on published releases is recorded in change sets
(DR-0048, §91).

## Consequences

- Immutability guarantees hold except at one documented, auditable seam.
- Data-subject erasure (POL-0001 §6) has a defined technical path.
- A future auditor can enumerate every redaction the archive has performed.
