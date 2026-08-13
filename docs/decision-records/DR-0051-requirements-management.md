# DR-0051 — Requirements management per record §99

**Category:** architecture / methodology | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W7-6, WP 0.8 §3.5/§5 | **Supersedes:** — | **Superseded by:** —

## Context

Record §99: important requirements need stable IDs, categories, status,
verification criteria, and traceability along objective → requirement → DR →
specification → implementation → verification → methodology → release.

## Alternatives considered

1. §99 model adopted as stated, REQ documents under DR-0046 control (chosen).
2. Issue-tracker-only requirements (rejected: no lifecycle control, no
   traceability guarantees).

## Decision

Requirements are REQ-class governance documents (DR-0046) with **stable
category-prefixed IDs** (PRES, EVID, SEC, LEGAL, DATA, ARCH, EDIT, AI, I18N,
OPS), status, verification criteria, and traceability links per §99. The
**candidate requirement set is Phase II output 6**, extracted from the Phase I
record and the enacted DRs in the consolidation step, and submitted for
founder approval like every other candidate output.

## Consequences

- Every enacted DR becomes traceable to the requirements it satisfies, and
  later to specifications and tests.
- Requirement verification criteria give Phase III its acceptance tests.
