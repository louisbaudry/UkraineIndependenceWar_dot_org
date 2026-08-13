# DR-0038 — Sanctions modeled as instruments, regimes, designations, and effects with full lifecycle

**Category:** legal / architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W6-1, WP 0.7 §2/§6 | **Supersedes:** — | **Superseded by:** —

## Context

Record §64: sanctions are legal instruments/regimes, never a boolean. WP 0.7
mapped the UN/EU/US/UK instrument hierarchies and confirmed every lifecycle
state in §64 is legally real — the EU annulment-then-redesignation cycle being
the sharpest test.

## Alternatives considered

1. Full legal-temporal model (chosen).
2. Flattened designation intervals (FtM-style) as canonical (rejected: loses
   instrument lineage, amendment history, and challenge outcomes the record
   requires; retained as export mapping, DR-0045).
3. Boolean/status flags (rejected: §64 prohibition).

## Decision

The sanctions layer models: **enabling authority → regime/program → legal
instrument (with amendment lineage and effective periods) → measures/effects →
designation acts**, per jurisdiction. The full lifecycle is representable:
amendment, suspension, expiry, delisting, annulment, redesignation, legal
challenge, judgment, replacement (§64). **No boolean `sanctioned` property
exists anywhere in the system.** "Which restrictions applied, under which
authority, to whom, during what period" (§3) is the layer's defining query.

## Consequences

- Instrument texts are documentary objects (DR-0011) acquired and preserved
  like any source.
- Effects and applicability decompose per DR-0041.
- Historical epistemic states are never rewritten by later legal events (§63).
