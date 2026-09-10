# DR-0091 — Project URIs derive from ARKs; the registry namespace is the registry's ARK

**Category:** architecture | **Status:** Approved | **Decided:** 2026-09-09 by founder/principal editor
**Origin:** CDR-P3-40, [WP 3.5](../phase-3/working-papers/wp-3.5-identifier-design.md) §3.8, §5 rule 5 | **Supersedes:** — | **Superseded by:** —

## Context

SPEC-0005 §4 declares the SKOS/RDF namespace in `registry.yaml` as
provisional (`https://ukraineindependencewar.org/ns/registry#`) pending the
identifier design, and DR-0083 records that changing it once an external
consumer exists becomes a structural change under DR-0080. No external
consumer exists. The W3C note *Cool URIs for the Semantic Web* holds that
hash URIs suit "small and stable sets of resources that evolve together"
and slash URIs with content negotiation suit large, evolving datasets.

## Alternatives considered

1. **All project URIs derive from ARKs; the registry keeps hash URIs on
   its own ARK** (chosen).
2. Keep the domain namespace for the registry and use ARKs only for
   objects (rejected: the vocabulary's URIs stay bound to the domain while
   nothing else is; a re-hosting breaks every SKOS mapping that cites
   them).
3. Defer until the NAAN is issued (rejected: SPEC-0005 §7 Q1 and
   DR-0083's open item stay open, and a consumer appearing meanwhile turns
   the later change into a costly one).

## Decision

1. **The registry receives an ARK.** Its SKOS concept URIs are that ARK's
   resolver URL followed by `#entry-id` (and `#scheme-id--member-id` for
   members, preserving SPEC-0005 §4's pattern). The fragment is stripped
   before resolution, so the registry object's `?info` and content
   negotiation are untouched.
2. **Entities and other citable objects use slash URIs on their own ARKs**
   with content negotiation between HTML and RDF representations.
3. **DR-0049's DataCite DOIs for public dataset releases are external
   identifier assignments** on the release object; a DOI's landing page is
   the release's ARK resolver page. DR-0049 and Q-31 are unchanged.
4. This is a **structural change to the provisional namespace under
   DR-0080**, taken deliberately before any external consumer exists. The
   exact namespace string is fixed when the NAAN is issued; until then
   `registry.yaml` keeps its provisional value and its provisional flag.

Closes SPEC-0005 §7 Q1 and the open item recorded in DR-0083.

## Consequences

- `registry.yaml`'s namespace block and SPEC-0005 §4 are revised (SPEC-0005
  v1.1) when the NAAN exists; the compiler already reads the namespace
  from configuration, so no code change is needed.
- Every project URI survives re-hosting, which the SKOS mappings
  (DR-0050) and any future RDF consumer inherit.
- SPEC-0005 §7 Q3 (URIs for target vocabularies) is unaffected: those are
  other issuers' URIs.
