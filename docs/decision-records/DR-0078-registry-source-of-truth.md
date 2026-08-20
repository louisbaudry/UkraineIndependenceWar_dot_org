# DR-0078 — Registry source of truth: files in Git, runtime as projection

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-25, SPEC-0004 §2 | **Supersedes:** — (resolves Q-30) | **Superseded by:** —

## Context

DR-0050 adopted the ISO/IEC 11179 registration pattern with SKOS
expression, leaving implementation open (Q-30): files in Git versus a
registry service.

## Alternatives considered

1. YAML files in Git as source of truth, other forms derived (chosen).
2. A registry service owning the data (rejected: an always-on component a
   single-founder project must maintain for decades, for a dataset of
   hundreds of entries).
3. Authoring directly in SKOS/Turtle (rejected: RDF-native but diffs poorly
   in review, which is where registry changes are actually scrutinized).

## Decision

The registry's **source of truth is YAML files under version control**. The
**SKOS/RDF, JSON, and human-readable forms are derived projections** —
DR-0054's layering applied to the registry itself.

- Registry changes are governance events (DR-0025/DR-0050) and Git already
  carries governance documents (DR-0046) with review, diff, and permanent
  history.
- The **compiled registry projection enforces enumerations** in the
  canonical store: a value absent from the registry cannot enter the data.
- The compiled registry carries its **version**, which is a configuration
  item in every release baseline (DR-0047/0048).
- The SKOS/RDF generation is a controlled mapping under DR-0056.

## Consequences

- Zero operational surface for the registry; source readable without the
  project's software (PRES-009's spirit).
- Enumeration violations become impossible rather than merely discouraged.
- A dataset release names the registry version that makes it interpretable.
