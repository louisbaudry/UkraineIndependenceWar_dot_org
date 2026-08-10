# DR-0005 — Fixity policy

**Category:** preservation | **Status:** Approved | **Decided:** 2026-08-10 by founder/principal editor
**Origin:** CDR-W1-5, WP 0.2 §4.3/§7 | **Supersedes:** — | **Superseded by:** —

## Context

Phase I §7: hash originals at ingestion; introduce periodic fixity checking as the
archive grows. OAIS makes fixity information mandatory PDI; PREMIS provides the
fixity semantic unit and fixity-check events; BagIt provides package manifests.

## Alternatives considered

1. SHA-256 at ingestion + event-recorded periodic checks + package manifests
   (chosen).
2. Dual-algorithm digests from the start (not chosen now; may be added by a
   future DR without contradiction — SHA-256 remains the baseline).
3. Defer until infrastructure design (rejected: fixity is already being practiced
   and should be policy, not habit).

## Decision

- Every preserved object receives a **SHA-256 digest at ingestion**, recorded in
  its provenance/preservation metadata.
- **Periodic fixity verification** is introduced as the archive grows; every check
  is recorded as an event with date, agent, and outcome — including failures.
- Any package that **moves between systems or custodians** carries a per-file
  checksum manifest (BagIt-style).

## Consequences

- Existing practice (both deposited documents carry ingestion SHA-256) is
  ratified as policy.
- Fixity failure is a recordable preservation event, never a silent re-copy.
- Fixity success is a bit-level statement only — it never implies authenticity
  or veracity (record §38; DR-0008's claims discipline applies).
