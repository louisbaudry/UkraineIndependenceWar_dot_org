# DR-0017 — Adopt W3C Web Annotation as the passage/region targeting vocabulary

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W3-1, WP 0.4 §5 | **Supersedes:** — | **Superseded by:** —

## Context

Record §59 and §29 require assertions, quotations, and research notes to point at
exact paragraphs, image regions, pages, and audio/video intervals — not merely at
whole documents (WP 0.1 layer E).

## Alternatives considered

1. W3C Web Annotation Data Model (chosen).
2. Custom locus model (rejected: §94; Web Annotation is the established, IIIF-
   compatible standard).
3. Plain fragment URLs (rejected: no selector redundancy, no version pinning,
   weak media support).

## Decision

The **W3C Web Annotation Data Model** (W3C Recommendation 2017) is adopted as
the targeting vocabulary: annotations carry bodies and targets, targets are
refined by selectors (text-quote, text-position, fragment/media-fragment for A/V
intervals, SVG/geometric for image regions, XPath for structured documents),
with State specifiers for version pinning. Selector combinations for redundancy
are standard practice.

Annotation identity, storage, and protocol serving remain Phase III matters
(WP 0.4 §6 Q1).

## Consequences

- Quotation machinery (DR-0019), evidence targeting (WS4), and IIIF media work
  (DR-0021) all build on one targeting vocabulary.
- Passage-level citation (§15) gains its technical substrate.
