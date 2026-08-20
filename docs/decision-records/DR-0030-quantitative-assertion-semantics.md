# DR-0030 — Quantitative assertions preserve original semantics

**Category:** epistemology / architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W4-7, WP 0.5 §8/§10 | **Supersedes:** — | **Superseded by:** —

## Context

Record §43–44: "at least 17" must never become "exactly 17"; representational
precision is not accuracy; normalized values are derived data.

## Alternatives considered

1. Structured quantity objects preserving original semantics (chosen).
2. Plain numeric fields with footnotes (rejected: the semantics live outside
   the data and are lost on query).

## Decision

Quantitative assertions are structured objects preserving: **original
expression** (as stated, in original language where relevant), **semantic type**
(exact / approximate / at-least / at-most / range / greater-than / fewer-than),
**value(s) and units**, **significant precision**, **uncertainty** where stated,
and **derivation method** for computed values. Normalized/comparable values are
derived data linked by provenance (DR-0003) and **never overwrite** the
original expression.

## Consequences

- Casualty figures, shipment quantities, ownership percentages, and price data
  all inherit honest semantics.
- Aggregations must respect semantic type (a sum of at-leasts is an at-least).
- Derived ownership calculations (§71, DR-0015's layer) build on these objects.
