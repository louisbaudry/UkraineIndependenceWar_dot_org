# DR-0059 — Two agent registries, linked

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-6, SPEC-0001 §3.1 | **Supersedes:** — (resolves Q-07, narrowing completed from DR-0004) | **Superseded by:** —

## Context

DR-0004 fixed the semantic separation of pipeline agents and world actors but
left storage design open (Q-07): one registry with roles, or two with links.

## Alternatives considered

1. Two registries with evidence-backed links (chosen).
2. One registry with role flags (rejected: mixes lifecycles — software
   versions vs biographies — and access sensitivities; weakens the DR-0004
   boundary at the exact point it must hold).

## Decision

**Pipeline agents** (persons, organizations, software acting on the archive)
and **world actors** (historical persons/groups) are **separate registries**.
A real person appearing in both receives an explicit, evidence-backed
`same-person` link — an identity assertion under DR-0012, never a merge.
World-layer queries cannot silently traverse into pipeline data.

## Consequences

- Confidential-source separability (§11, SEC-001) gains structural support.
- The identity-workflow specification (Q-10) governs `same-person` links like
  any other identity assertion.
