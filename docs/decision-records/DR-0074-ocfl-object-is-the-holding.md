# DR-0074 — The OCFL object is the holding

**Category:** preservation / architecture | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-21, WP 3.3 §5.1 | **Supersedes:** — (answers WP 3.1 §5 Q5) | **Superseded by:** —

## Context

Adopting OCFL (DR-0073) requires deciding what an OCFL object corresponds
to. WP 3.1 had also left open whether OCFL's versioning conflicts with the
rule that originals are immutable and derivatives are separate objects.

## Alternatives considered

1. The holding (DR-0061) as the OCFL object (chosen).
2. One object per preserved representation (rejected: scatters a holding
   across storage, losing natural grouping without conceptual gain).
3. One object per capture series (rejected: buries evidentially distinct
   captures inside version history).

## Decision

**An OCFL object corresponds to a holding** (DR-0061):

- `v1` holds the original preserved representation as acquired;
- later versions add derivative representations (OCR, transcripts,
  normalized formats, extracted media) as they are produced;
- the holding's canonical-store record remains the authority on what each
  representation is; OCFL is where the bytes live.

**Successive captures of the same URL are different holdings** and therefore
different OCFL objects, related by the capture-series relation in the
canonical store (Memento pattern, DR-0023) — a data-model relationship, not
a storage-layout artifact.

**On immutability:** OCFL *implements* the rule rather than conflicting with
it. Versions are immutable once written; adding a derivative never alters
the original, and forward-delta references rather than copies it. The
apparent tension dissolves under DR-0054's layering: **storage identity is
not conceptual identity** — a derivative is a distinct object in the
canonical store with its own PREMIS identity and PROV lineage, and may still
live as a later version inside the same storage container.

## Consequences

- Everything the archive holds of one documentary item stays together in
  storage, without merging conceptual identities.
- Each capture retains its evidential distinctness as its own object.
- PRES-001's immutability requirement is satisfied by the layout itself.
