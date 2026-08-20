# DR-0081 — Governed translation of registry terminology

**Category:** architecture / editorial | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-28, SPEC-0004 §8 | **Supersedes:** — | **Superseded by:** —

## Context

Record §60 requires concept-oriented multilingual terminology governance and
states that translation memory does not establish terminological authority;
I18N-002/003 require per-language preferred terms and separation of
canonical semantics from wording. AI-001 forbids AI output becoming
canonical silently.

## Alternatives considered

1. English authoring with governed, provenance-bearing translation (chosen).
2. Parallel multilingual authoring (rejected: no single authoritative
   definition to translate *from*; invites divergent meanings per language).
3. Machine translation of labels (rejected outright as an authority source:
   §60, AI-001).

## Decision

- **English is the registry's authoring language**; other languages are
  **governed translations, not derivations**.
- A translated label is **an entry with provenance**: translator, date, and
  review status. **Machine translation may propose; it never becomes an
  authoritative label without human review.**
- **Forbidden-translation notes are first-class** — including renderings
  that turn "likely" into near-certainty or "roughly even chance" into
  "possible" (DR-0065), and any rendering that collapses a conflict-register
  distinction (Phase II output 3).
- Which languages are carried, and in what order, is an operational
  decision; the subject matter makes Ukrainian and Russian the first
  priorities after English.

## Consequences

- Multilingual publication cannot silently change what a term means, because
  meaning lives in the band/identifier, not the word (DR-0065, §61).
- Terminology work is auditable per language and per translator.
