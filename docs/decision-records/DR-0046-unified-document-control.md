# DR-0046 — Unified document control for the six governance document classes

**Category:** architecture / methodology | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W7-1, WP 0.8 §3.1/§5 | **Supersedes:** — | **Superseded by:** —

## Context

Record §100 defines six document classes (REQ, POL, PROC, DR, SPEC, METH) and
requires document-control semantics researched before freezing. WP 0.8 grounded
them in records-management/document-control practice (ISO 15489 tradition). The
DR system already practices the pattern.

## Alternatives considered

1. One control pattern across all six classes, generalizing DR practice (chosen).
2. Per-class ad hoc conventions (rejected: same lifecycle needs everywhere).
3. Git history as implicit status (rejected: a commit is not an approval).

## Decision

All governance documents carry: **stable ID** (class-prefixed), class, title,
**status** (draft / proposed / approved / effective / superseded / withdrawn),
**approval authority and date** (founder, per §78), **effective date** where
distinct from approval, **supersession links in both directions**, and change
history. Git stores the documents; **status is explicit document metadata,
never inferred from Git state**.

## Consequences

- The DR register pattern extends to REQ/POL/PROC/SPEC/METH as those classes
  come into use.
- Superseded documents remain in place, marked (per §77; consistent with
  existing practice).
