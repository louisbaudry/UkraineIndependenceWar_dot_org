# DR-0020 — TEI P5 selective adoption

**Category:** architecture / editorial | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W3-4, WP 0.4 §5 | **Supersedes:** — | **Superseded by:** —

## Context

TEI P5 provides mature scholarly text encoding (diplomatic transcription, damage/
illegibility, variant readings, editorial apparatus) but is heavy. WP 0.1 set the
disposition "selective adoption"; this DR fixes the selection rule.

## Alternatives considered

1. Selective: deep TEI only for high-value transcripts/critical editions, subset
   defined at first real corpus (chosen).
2. Blanket TEI for all transcripts (rejected: cost without benefit for routine
   material).
3. No TEI (rejected: reinvents critical apparatus when it becomes needed; §94).

## Decision

Deep **TEI P5 encoding is reserved for high-value transcripts and critical
editions** where variant readings, damage, illegibility, or editorial apparatus
carry evidential or scholarly weight. The project TEI subset is defined **when
the first such corpus is processed**, not speculatively. Routine transcripts
remain plain derivative expressions with PROV lineage (DR-0003, DR-0011).

## Consequences

- No premature TEI infrastructure; no loss of the option.
- The trigger question — which corpus first warrants deep encoding — is carried
  in the Phase II open-questions register (WP 0.4 §6 Q2).
