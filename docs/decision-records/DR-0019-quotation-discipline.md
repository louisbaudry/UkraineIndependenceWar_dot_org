# DR-0019 — Quotation discipline

**Category:** editorial / methodology | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W3-3, WP 0.4 §3.1/§5 | **Supersedes:** — | **Superseded by:** —

## Context

Record §59: important quotations preserve exact original-language passage, exact
source version, locus, translation, transcription/OCR origin, editorial context,
and omissions. "Do not manufacture quotations from paraphrases." §58: quotation,
paraphrase, and summary must remain distinct.

## Alternatives considered

1. Quotation as a typed annotation with the §59 checklist as required content
   (chosen).
2. Quotations as plain text fields with citations (rejected: loses locus,
   version, omissions, and derivation).

## Decision

A **project quotation** is an annotation (DR-0017) targeting the preserved
original-language expression (DR-0018) and carrying: the exact passage, marked
omissions, the locus, linked translation expression(s) where present, and
transcription/OCR derivation (DR-0003) where the text passed through such a
step.

**No quotation is minted from a paraphrase or summary.** Quotation, paraphrase,
and summary are distinct annotation types and are never silently converted into
one another.

## Consequences

- Every published quotation can be traced to preserved source bytes at an exact
  locus (record Principle 2, §86).
- Translation pairs stay passage-aligned and provenance-bearing (§58–59).
- Deep editorial apparatus, where warranted, uses TEI per DR-0020.
