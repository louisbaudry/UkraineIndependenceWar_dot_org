# DR-0073 — Adopt OCFL as the at-rest archival storage layout

**Category:** preservation / architecture | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-20, WP 3.3 | **Supersedes:** — (resolves Q-03) | **Superseded by:** —

## Context

Preserved bytes need an at-rest layout. PRES-009 requires the archive to be
reconstructible without the project's software; DR-0001 requires AIP
containers transferable to a successor archive.

## Alternatives considered

1. OCFL 1.1.1 (chosen).
2. A project-specific filesystem convention (rejected: bespoke work plus
   undocumented tacit knowledge — the opposite of PRES-009; §94).
3. BagIt at rest (rejected: a transfer convention with no versioning or
   forward-delta; correct for transfer per DR-0007, wrong at rest).
4. Object storage with application-managed metadata (rejected: layout
   meaning lives in the application database — the dependency PRES-009
   forbids; note OCFL itself runs on object storage).
5. A repository platform (rejected for now: operational surface for one
   founder; several such platforms use OCFL underneath, so adopting the
   layout preserves the option).

## Decision

**OCFL (Oxford Common File Layout), version 1.1.1**, is adopted as the
at-rest archival storage layout for preserved bytes. **OCFL objects are the
project's AIP containers** (DR-0001).

The decisive property is OCFL's design principle that an object can be
understood, validated, and reconstructed **from the files alone** — no
database, no originating software — which is exactly PRES-009's
requirement. Its content is plain files, replicable by ordinary means.

## Consequences

- Preservation storage is standards-based and inspectable without the
  project's code.
- Successor deposit (PRES-010) becomes a transfer of OCFL objects, not a
  migration.
- Implementation choices (library vs direct implementation; filesystem vs
  object storage) remain open (WP 3.3 §8).
