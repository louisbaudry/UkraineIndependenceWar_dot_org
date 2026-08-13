# DR-0022 — Adopt CSL for citation rendering

**Category:** architecture / editorial | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W3-6, WP 0.4 §5 | **Supersedes:** — | **Superseded by:** —

## Context

Record §15 requires stable citation of research objects; §61 separates canonical
semantics from presentation wording. Citation *data* belongs to the documentary
layer; citation *formatting* is presentation.

## Alternatives considered

1. CSL for rendering (chosen).
2. Hand-built citation formatting (rejected: §94; CSL is the established,
   style-rich standard used by Zotero/pandoc ecosystems).

## Decision

**CSL (Citation Style Language)** is adopted for citation rendering at the
presentation layer, driven by documentary-layer metadata. Identifier syntax and
resolvers for citable project objects remain a separate, later decision (§15's
warning against freezing custom identifier syntax stands).

## Consequences

- Published citations restyle without touching canonical data (§61).
- Dataset releases (WP 0.1 layer I, DataCite) gain standard citation output
  for free.
