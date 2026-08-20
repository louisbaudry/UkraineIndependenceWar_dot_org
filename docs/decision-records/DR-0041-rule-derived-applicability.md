# DR-0041 — Rule-derived applicability is computed, versioned, never stored as designation

**Category:** legal / architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W6-4, WP 0.7 §2.2/§6 | **Supersedes:** — | **Superseded by:** —

## Context

Record §73: "subject to restrictions" ≠ "named on a list." The OFAC 50 Percent
Rule and EU ownership/control criteria extend restrictions to undesignated
entities via computable rules over ownership/control data. Record §71 requires
derived ownership to preserve path, method, and rule.

## Alternatives considered

1. Derived applicability as computed, versioned assertions (chosen).
2. Writing derived hits into designation data (rejected: fabricates listings;
   precisely §73's confusion).
3. Not computing applicability (rejected: it is the professional-platform
   core, §3).

## Decision

Rule-derived applicability conclusions are **derived assertions** (DR-0003)
carrying: the ownership/control path (statements used, DR-0040), aggregated
percentages as quantity objects, the **rule and rule version** (jurisdiction-
specific), computation date, software version, and resulting applicability
with its validity period. Input epistemic status **propagates**: a path built
on contested statements yields a contested conclusion (DR-0024, DR-0026).
Derived applicability is never stored as, or displayed as, a designation.

## Consequences

- "Blocked under the 50 Percent Rule as of date D via path P" is fully
  auditable and recomputable.
- Rule changes trigger recomputation, with prior conclusions preserved (§63).
- Publication wording must distinguish designated from rule-derived (DR-0008's
  claims discipline extended to sanctions language).
