# DR-0013 — Roles and memberships are temporal events

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W2-4, WP 0.3 §7 | **Supersedes:** — | **Superseded by:** —

## Context

Record §18: roles are temporal relationships, not mutable person attributes;
acting/interim capacity, disputed appointments, and de facto roles must be
representable; association with an organization does not make all of a person's
actions organizational.

## Alternatives considered

1. Membership/role as joining/leaving events with role qualification (chosen).
2. Role fields with validity dates on persons (rejected: loses provenance, breaks
   under disputed/parallel/acting roles).

## Decision

Organizational membership, office-holding, and roles are modeled as **temporal
events** (joining/leaving pattern) with typed role qualification (acting,
interim, de facto, disputed), tenure time-spans, and source provenance. Disputed
and de facto roles are attribute assertions carrying their asserting source —
their truth status is an epistemic matter (Workstream 4), not a data-entry
choice.

## Consequences

- "Who held what role when, according to whom" is always answerable.
- Presence, participation, responsibility, and liability stay distinct (§18, §52).
- Person-level attributes never silently encode organizational capacity.
