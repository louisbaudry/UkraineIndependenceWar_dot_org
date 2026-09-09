# DR-0088 — Public identifiers are minted as assignment events at publication

**Category:** architecture / editorial | **Status:** Approved | **Decided:** 2026-09-09 by founder/principal editor
**Origin:** CDR-P3-32, [WP 3.4](../phase-3/working-papers/wp-3.4-identifier-design.md) §3.4–3.6, §5 rule 2 | **Supersedes:** — | **Superseded by:** —

## Context

Record §15 says internal implementation objects "do not automatically
require public identifiers". DR-0012 models every name and identifier as
an assignment event with provenance, and ARCH-001 forbids a shared identity
between the pipeline and world registries. The project's own public
identifier is a fact about an object — "the project assigned this name on
this date" — and Q-12 asked whether annotations are independently citable.

## Alternatives considered

1. **Mint at first publication or explicit citation, as an
   `identifier-assignment` assertion; annotations included** (chosen).
2. Mint at creation for every object in a citable class (rejected:
   millions of identifiers the project never committed to publicly;
   unpublished pipeline internals in the public register; contradicts
   §15's "not automatically").
3. Mint at publication but exclude annotations (rejected: the Web
   Annotation model expects every serialised annotation to have an IRI;
   Q-12 would remain half open).

## Decision

1. **A public ARK is an `identifier-assignment` assertion** (DR-0012) with
   the project as asserter and a registry identifier-type for the
   project's own ARKs. The register of public identifiers is therefore
   ordinary provenance-bearing data that ships in dumps and change sets.
2. **Minting happens at the object's first Gate 3 publication decision**
   (DR-0066), or **by explicit editorial act** for an object cited in a
   publication without a page of its own (an assertion, quotation,
   holding, annotation).
3. **Eligible classes:** the §15 list — persons, organisations, events,
   assertions, source captures and holdings, quotations, investigations,
   legal records, dataset releases — **plus annotations and published
   pages**. Annotations are citable objects under the same scheme and the
   same rule; there is no separate annotation resolver. Serving them over
   the Web Annotation Protocol is a later product decision (WP 3.4 §8 Q4).
4. **Internal UUIDs are never published as identifiers.**

This resolves the annotation half of Q-12 (WP 0.4 §6 Q1).

## Consequences

- Gate 3 gains a minting hook; the editorial workflow gains a "cite"
  action. Both are specified in SPEC-0007.
- `published_page.path` becomes a resolver target of the page's ARK, not
  the citation identifier its schema comment currently claims.
- Unpublished material has no public identifier. Whether citation by a
  subscriber-tier product counts as publication for minting is open
  (WP 3.4 §8 Q3).
