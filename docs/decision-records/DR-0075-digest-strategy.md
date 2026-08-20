# DR-0075 — Digest strategy: SHA-512 content addressing, SHA-256 fixity block

**Category:** preservation | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-22, WP 3.3 §5.2 | **Supersedes:** — (refines DR-0005) | **Superseded by:** —

## Context

OCFL's default content-addressing digest is SHA-512; DR-0005 mandates
SHA-256 at ingestion, and every hash recorded in the project so far is
SHA-256.

## Alternatives considered

1. SHA-512 content addressing with SHA-256 in the fixity block (chosen).
2. SHA-256 for both (rejected: forgoes the specification default and the
   larger collision margin appropriate to a decades-horizon archive).
3. SHA-512 only (rejected: would break continuity with recorded practice and
   with DR-0005's literal requirement).

## Decision

Preserved content uses **SHA-512 as the OCFL content-addressing digest**,
with **SHA-256 recorded in the OCFL fixity block** and in the canonical
store.

This satisfies DR-0005 literally, preserves continuity with every hash
recorded to date, adopts the specification default, and yields
**independent cross-checking** — two algorithms disagreeing on the same
content is itself a signal worth acting on.

## Consequences

- Fixity checks may verify either or both algorithms; disagreement is a
  recorded preservation event requiring investigation.
- Migration to a future algorithm is an additive fixity-block change, not a
  re-addressing of content.
