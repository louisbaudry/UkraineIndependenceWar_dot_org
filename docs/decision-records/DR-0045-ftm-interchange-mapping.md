# DR-0045 — FollowTheMoney/OpenSanctions as interchange mapping and identifier spine

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W6-8, WP 0.7 §3/§6 | **Supersedes:** — | **Superseded by:** —

## Context

FollowTheMoney (FtM) is the investigative ecosystem's de-facto interchange
schema; OpenSanctions aggregates designation data with stable identifiers.
Record §16 requires typed external identifiers; WP 0.7 found FtM cannot carry
the full legal lifecycle (DR-0038) and must not become the canonical model.

## Alternatives considered

1. Map-to disposition: FtM as interchange, OpenSanctions IDs as external
   identifiers (chosen).
2. FtM as canonical internal model (rejected: flattens lifecycle, effects, and
   rule-derived applicability).
3. Ignore FtM (rejected: isolates the project from the ecosystem's data and
   tooling).

## Decision

The project maintains **mappings to FtM** entity and sanction shapes for data
exchange, and consumes **OpenSanctions identifiers as typed external
identifiers** attached via assignment events (DR-0012) — to designation
records (DR-0039) and, where identity is confirmed, to canonical entities.
FtM is **not** the canonical internal model; export losses (lifecycle
flattening) are documented per package type (open question WP 0.7 §7 Q5).

## Consequences

- Ecosystem interoperability (imports, cross-referencing, tooling) without
  modeling capture.
- OpenSanctions becomes both a collection source (§8) and an identity-
  resolution aid — always via evidence-backed assertions, never fuzzy
  auto-merge (§72, DR-0039).
