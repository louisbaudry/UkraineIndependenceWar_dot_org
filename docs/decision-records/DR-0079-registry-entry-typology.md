# DR-0079 — Registry entry typology and structure

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-26, SPEC-0004 §3–4 | **Supersedes:** — | **Superseded by:** —

## Context

The registry must hold several kinds of thing (concepts, enumerations, data
elements, relationship types, argument schemes, identifier types) with one
consistent governance shape; DATA-008 requires every consequential data
element to have one documented meaning.

## Alternatives considered

1. Six typed entry kinds sharing a common structure (chosen).
2. One undifferentiated entry shape (rejected: argument schemes carry
   critical questions, vocabularies carry members, identifier types carry
   issuing authorities — flattening these loses required structure).

## Decision

The registry holds six entry types — `concept`, `vocabulary`,
`data-element`, `relationship-type`, `argument-scheme`, `identifier-type` —
each carrying:

- **Identity:** stable registry ID (never reused, never re-pointed), type,
  layer.
- **Meaning:** definition, scope notes, usage notes, and *what it is not*
  where a conflict-register entry applies.
- **Labels:** `prefLabel`/`altLabel` per language, plus **explicit
  forbidden/misleading translation notes** (§60).
- **Structure:** broader/narrower/related; vocabulary members with their own
  definitions; schemes' critical questions.
- **Mappings:** `exactMatch`/`closeMatch`/`relatedMatch` to external
  vocabularies (CIDOC CRM, PREMIS, PROV, FtM, BODS, Wikidata, PHIA bands…)
  with notes where fit is imperfect.
- **Governance:** registration status, effective date, stewardship,
  **links to the DRs, SPECs, and REQs that authorize or depend on it**,
  version history, and `replacedBy` where deprecated.

## Consequences

- DATA-008 becomes auditable: every element traces to the decision that
  created it.
- Terminology governance (§60) has a concrete home, including negative
  guidance.
