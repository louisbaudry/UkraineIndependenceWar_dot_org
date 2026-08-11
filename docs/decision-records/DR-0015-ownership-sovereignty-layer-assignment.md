# DR-0015 — Ownership/control and sovereignty relations assigned outside the CRM layer

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W2-6, WP 0.3 §7 | **Supersedes:** — | **Superseded by:** —

## Context

Phase I §19–20 requires rich corporate ownership/control semantics (legal,
beneficial, nominee, voting, de facto; temporal; typed addresses). §46 requires
sovereignty, territorial claim, administration, occupation, and de facto control
as separate relationships. Workstream 2 found CIDOC CRM does not — and should
not be stretched to — model these.

## Alternatives considered

1. Assign ownership/control to the sanctions/legal layer (WS6) and
   sovereignty/occupation to a joint WS2/WS6 vocabulary grounded in CRM periods
   (chosen).
2. Extend CRM with custom ownership/sovereignty properties now (rejected:
   invents what mature domain models may already provide; violates §94).
3. Treat as out of scope indefinitely (rejected: both are core Phase I
   requirements).

## Decision

- **Corporate ownership/control networks** (§19–20) are modeled in the
  sanctions/export-control legal layer. Workstream 6 must study purpose-built
  models — the **OpenSanctions/FollowTheMoney schema** and corporate-registry
  models (GLEIF/LEI relationship data, BODS/Open Ownership) — before any
  vocabulary is fixed.
- **Sovereignty/occupation/administration/de facto control** (§46) get a joint
  WS2/WS6 vocabulary grounded in the CRM period concept (an occupation is a
  spatiotemporal phenomenon) with typed, evidence-backed relationship assertions.
- The CRM world layer holds the *entities and events* these relations refer to;
  the relations themselves live in their assigned layers, linked across.

## Consequences

- CRM adoption (DR-0010) stays clean; no custom ownership properties pollute it.
- Workstream 6's scope now explicitly includes ownership-network modeling with
  named study candidates.
- Derived ownership calculations (§71) will sit on the legal layer with full
  derivation provenance (DR-0003).
