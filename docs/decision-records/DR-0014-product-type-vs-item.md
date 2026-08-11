# DR-0014 — Product-type vs individual-item distinction for physical objects

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W2-5, WP 0.3 §7 | **Supersedes:** — | **Superseded by:** —

## Context

Record §21: distinguish product/model identity from individual physical item
identity — a drone model vs the recovered airframe with a serial number; a
component type vs the chip photographed in wreckage. Central to export-control
and component-tracing work (§65–66).

## Alternatives considered

1. Two-level pattern: product type vs individual object (CRM E99 vs E22) (chosen).
2. Single object table with optional serials (rejected: conflates class and
   instance; breaks component-identification workflows).

## Decision

Physical-object modeling distinguishes **product types** (models, part numbers,
regulated product identities) from **individual items** (serial-numbered,
photographed, seized, or otherwise individuated objects). Individuals link to
their type; production, movement, custody, seizure, and identification are events
on individuals; regulatory classification (§66) attaches to types and, where
evidence requires, to individuals.

## Consequences

- Component identification ("this chip type appears in this weapon") and item
  tracing ("this serial passed through these hands") stay separate, joinable
  claims.
- Workstream 6 builds export-control classification on the type side without
  disturbing item-level evidence.
