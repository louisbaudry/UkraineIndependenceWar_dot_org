# DR-0065 — Likelihood band scale: ICD 203 canonical, PHIA mapped

**Category:** epistemology / methodology | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-12, WP 3.2 | **Supersedes:** — (completes DR-0026; resolves Q-16) | **Superseded by:** —

## Context

DR-0026 adopted a two-dimensional uncertainty model and deliberately left the
likelihood scale unset, ruling that no probability wording was canonical
until a further DR fixed it. WP 3.2 compared the two mature scales against
primary texts.

## Alternatives considered

1. ICD 203 canonical, PHIA mapped (chosen).
2. PHIA canonical (rejected: its deliberate gaps leave judgments between
   bands with no expressible value under DR-0029's no-silent-nulls rule, and
   it has no even-odds term, which historical and attribution work needs).
3. A hybrid scale (rejected: bespoke wording no reader community recognizes
   on sight).
4. Continue deferring (rejected: assessments cannot be recorded honestly
   without a scale).

## Decision

The canonical likelihood vocabulary is the **ICD 203 seven-band contiguous
scale**:

| Band identifier | Term | Range |
|---|---|---|
| `almost-no-chance` | almost no chance | 01–05% |
| `very-unlikely` | very unlikely | 05–20% |
| `unlikely` | unlikely | 20–45% |
| `roughly-even-chance` | roughly even chance | 45–55% |
| `likely` | likely | 55–80% |
| `very-likely` | very likely | 80–95% |
| `almost-certain` | almost certain | 95–99% |

Adopted with it:

1. **PHIA equivalences are recorded as SKOS mapping relations** in the
   registry (DR-0050), so UK-sourced assessments ingest and compare without
   silent translation loss.
2. **The band identifier is stored; the range is the anchor; words are
   labels rendered at the presentation layer** (§61) — the band means the
   same thing in every language.
3. **One synonym row only.** ICD 203's primary row is the project's; the
   alternative row (remote / highly improbable / … / nearly certain) is
   registered as synonyms and never mixed into a single product.
4. **Multilingual governance under §60** with per-language preferred terms
   and **forbidden-translation notes** — including renderings that turn
   "likely" into near-certainty, or "roughly even chance" into "possible."
5. **Bands are never inherited.** Reporting another body's estimative
   language is a documentary assertion carrying *their* scale (§32,
   DR-0024), mapped but never converted into a project judgment.
6. **No band without a stated basis.** A band belongs to an assessment
   (DR-0026) with its evidence and reasoning; bands never attach to bare
   data fields.

## Consequences

- DR-0026 is complete; project outputs may now carry canonical probability
  wording.
- Analytic confidence (low/moderate/high) remains a separate dimension and
  is unaffected by this DR.
- Whether public outputs display the numeric range alongside the term is a
  presentation-layer question, left open (WP 3.2 §5).
- Retrospective phrasing (a band as credence about a past fact, not a
  forecast) needs a registry scope note — open item from WP 3.2 §5.
