# DR-0008 — Custody claims discipline; Berkeley Protocol guides practice

**Category:** legal / methodology | **Status:** Approved | **Decided:** 2026-08-10 by founder/principal editor
**Origin:** CDR-W1-8, WP 0.2 §4.4/§7 | **Supersedes:** — | **Superseded by:** —

## Context

Phase I §6 distinguishes ordinary provenance from **legal chain of custody**, which
"must never be falsely claimed merely because a file was downloaded, timestamped,
hashed, and preserved." No metadata standard confers legal custody status; courts
and legal frameworks assess it.

## Alternatives considered

1. Document custody history; never assert "legal chain of custody" as a status;
   Berkeley Protocol guides practice (chosen).
2. Claim chain of custody where internal procedures seem strong (rejected:
   overclaims legal status; precisely what §6 forbids).
3. Avoid custody documentation until legal review exists (rejected: loses
   unrecoverable early-acquisition metadata).

## Decision

The archive **documents custody history** — acquisition, transfers, handling — in
PREMIS/PROV vocabulary, as fully as practical. The project **never emits "chain of
custody" as a status claim** about its holdings; the phrase may appear only when
describing what others assert, or as documented custody history explicitly labeled
as such.

The **Berkeley Protocol on Digital Open Source Investigations** guides collection,
preservation, verification, security, and ethics practice, to maximize future
evidentiary utility without overstating legal status. It informs methodology
(record §97); it does not become the historical ontology (WP 0.1).

## Consequences

- Publication and API surfaces must respect the claims discipline in wording.
- Collection procedures are written against Berkeley Protocol guidance as the
  methodology matures (Workstream 7 / METH documents).
- Maximum future evidentiary utility, zero overstated legal status — the §6
  balance, made operational.
