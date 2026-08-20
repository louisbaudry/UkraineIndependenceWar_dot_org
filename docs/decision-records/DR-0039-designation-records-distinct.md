# DR-0039 — Designation records are distinct from canonical entities

**Category:** legal / architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W6-2, WP 0.7 §4/§6 | **Supersedes:** — | **Superseded by:** —

## Context

Record §72: designation records exist independently from canonical entities;
mapping is an evidence-backed identity assertion; a sanctions-list identity must
never be linked by fuzzy name matching alone. §64: authority rationales are
authority-attributed assertions.

## Alternatives considered

1. Designation record / mapping assertion / canonical entity as three objects
   (chosen).
2. Designations as attributes of entities (rejected: collapses exactly what
   §72 separates; breaks on mistaken-identity listings and homonyms).

## Decision

A **designation record** is a documentary-legal object carrying what the
authority published: names, aliases, DOBs, addresses, identifiers, stated
rationale. **Designation→canonical-entity mapping is an identity assertion**
under DR-0012 with candidate/confirmed/rejected states, evidence, and
authority-correction history. The authority's rationale remains an
authority-attributed assertion (§32) unless independently established by the
project. Delistings and corrections update the record and the mapping's
history — never silently rewrite either.

## Consequences

- Mistaken listings, transliteration collisions, and impersonations are
  representable without corrupting canonical entities (§17).
- OpenSanctions and official list IDs attach to designation records as typed
  external identifiers (DR-0045).
