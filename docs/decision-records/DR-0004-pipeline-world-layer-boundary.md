# DR-0004 — Hard boundary between pipeline and historical-world layers

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-10 by founder/principal editor
**Origin:** CDR-W1-4, WP 0.2 §5/§7 | **Supersedes:** — | **Superseded by:** —

## Context

"Event" and "agent" mean different things in preservation metadata (actions on
archived objects; collectors, reviewers, software) and in the historical world
model (strikes, designations, occupations; persons, organizations, states).
Collapsing them would violate record Principle 1 (preserve distinctions) and
poison both layers.

## Alternatives considered

1. Permanent separation, with explicit links where one party appears in both
   (chosen).
2. Unified event/agent model with type flags (rejected: invites silent conflation;
   a capture would sit in the same table as a missile strike).
3. Decide after the CIDOC CRM study (rejected: the boundary is prior to, and a
   constraint on, that study).

## Decision

Pipeline/preservation events and agents are **permanently separate** from
historical world events and actors. A capture is never a world event; a collector
is never a historical actor. The same real person may appear in both registries,
**linked but never merged**.

Open question preserved (WP 0.2 §8 Q2): one agent registry with roles vs two
registries with links — to be resolved with Workstream 2. This DR fixes the
*semantic* separation, not the storage design.

## Consequences

- The conceptual conflict register carries the event/agent term collisions.
- Workstream 2 (CIDOC CRM) studies the world layer under this constraint.
- Source-lifecycle states (§24) are world/documentary assertions evidenced by
  captures — never preservation metadata (WP 0.2 §4.5).
