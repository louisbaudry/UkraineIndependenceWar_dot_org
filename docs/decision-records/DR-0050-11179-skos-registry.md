# DR-0050 — Semantic registry: ISO/IEC 11179 pattern, SKOS-expressed

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W7-5, WP 0.8 §2.3–2.4, §3.4/§5 | **Supersedes:** — | **Superseded by:** —

## Context

Record §101 requires a versioned semantic registry (one documented meaning per
consequential element); §102 a controlled vocabulary; §60 concept-oriented
multilingual terminology. WP 0.8 found the shapes solved: ISO/IEC 11179
registration + SKOS concept modeling.

## Alternatives considered

1. 11179-patterned registry, SKOS-expressed where conceptual (chosen).
2. Ad hoc data dictionary (rejected: §94; loses stewardship/status/deprecation
   semantics).
3. Full formal ontology now (rejected: §95 canonical-representation question
   is still open; SKOS does not prejudge it).

## Decision

One **semantic registry** following the ISO/IEC 11179 pattern: entries with
definitions, permissible values, stewardship, registration status, effective
dates, deprecation with replacement mappings. Conceptual content is expressed
in **SKOS**: per-language preferred/alternate labels (§60), definitions, scope
notes (including forbidden/misleading translations), broader/narrower/related
links, and mappings to external vocabularies (Wikidata, CRM classes, FtM,
BODS…). The registry hosts the vocabularies assigned by earlier DRs
(epistemic vocabulary, absence states, argument schemes, interest types,
territorial statuses, conflict-register resolutions). Routine entries follow a
lightweight registry process; **structural vocabulary changes require DRs**
(DR-0025's rule). **TBX** is studied when professional translation workflows
begin.

## Consequences

- Terminology governance (§60) and the controlled vocabulary (§102) share one
  home and one process.
- Registry tooling (files vs service) remains a Phase III choice; the pattern
  is tooling-independent.
