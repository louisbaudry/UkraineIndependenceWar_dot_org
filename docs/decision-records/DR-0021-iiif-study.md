# DR-0021 — IIIF study before media-platform design

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W3-5, WP 0.4 §5 | **Supersedes:** — | **Superseded by:** —

## Context

Image and A/V evidence needs region/interval annotation (§21 component
identification, §48 imagery observations) and eventually public delivery. IIIF
Presentation 3.0 covers both and composes natively with Web Annotation
(DR-0017).

## Alternatives considered

1. Mandatory IIIF evaluation before the media platform is designed; adoption
   deferred until then (chosen).
2. Adopt IIIF now (rejected: no media platform exists to constrain; premature).
3. Ignore IIIF (rejected: risks a proprietary region model, §94).

## Decision

**IIIF (Presentation API 3.0) must be evaluated before the media delivery
platform is designed.** Adoption is deferred to that point. The evaluation
includes whether restricted material (§10) uses IIIF infrastructure under access
control or a simpler internal region model (WP 0.4 §6 Q4).

## Consequences

- Region/interval annotation work proceeds now on the Web Annotation vocabulary
  alone, which IIIF would consume unchanged.
- No media-delivery decision can bypass the IIIF evaluation.
