# DR-0083 — Adoption of the registry projection mapping (SPEC-0005)

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-20 by founder/principal editor
**Origin:** CDR-P3-29, SPEC-0005 | **Supersedes:** — | **Superseded by:** —

## Context

DR-0056 requires each standards surface to have a versioned SPEC-class
mapping document specifying the canonical→surface mapping, its generator
version, and documented export losses. The registry compiler
(`registry/compile.py`) produces two surfaces — a runtime JSON projection
and a SKOS/RDF interchange projection — and shipped alongside SPEC-0005 as
its mapping document.

## Alternatives considered

1. Adopt SPEC-0005 with §5's losses accepted as documented (chosen).
2. Require the compiler to mitigate a loss before adoption — e.g. a JSON-LD
   context to recover L2's missing numeric ranges for RDF consumers
   (not chosen now; retained as SPEC-0005 §7 open question 2).
3. Leave SPEC-0005 at draft (rejected: the implementation is live, so
   DR-0056 would stand unsatisfied for a surface already in use).

## Decision

**SPEC-0005 v1.0 is adopted, effective 2026-08-20.** DR-0056 is satisfied
for the registry's JSON and SKOS/RDF surfaces.

The **seven export losses of §5 are accepted as documented**, most
consequentially:

- **L2** — a pure-SKOS consumer sees the label "likely" without the 55–80%
  range that DR-0065 establishes as the anchor of its meaning;
- **L5** — governance metadata has no SKOS equivalent, so a pure-SKOS
  consumer cannot distinguish an effective entry from a deprecated one;
- **L6** — forbidden translations are deliberately not emitted, since
  publishing them as notes would risk a consumer harvesting them as valid
  labels, the harm DR-0081 records them to prevent.

Consumers requiring what SKOS cannot carry read the JSON projection or the
YAML source, both of which retain everything.

## Consequences

- The registry's interchange behaviour is specified, auditable, and its
  limits are stated rather than discovered by a consumer downstream.
- Adding a third surface (a JSON-LD context, a published registry site)
  requires its own mapping document under DR-0056.
- The provisional RDF namespace (record §15, Q-12) remains open; changing it
  once an external consumer exists becomes a structural change requiring a
  Decision Record (DR-0080).
