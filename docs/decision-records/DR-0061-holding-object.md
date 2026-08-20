# DR-0061 — The holding object

**Category:** architecture / preservation | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-8, SPEC-0001 §3.3 | **Supersedes:** — (resolves Q-09) | **Superseded by:** —

## Context

One preserved holding has two identities: documentary (which manifestation's
exemplar it is — LRMoo Item, DR-0011) and preservation (the preserved bytes —
PREMIS representations, DR-0002/0060). Q-09 asked how they bridge.

## Alternatives considered

1. First-class holding object (chosen).
2. Direct Item↔representation links (rejected: nowhere to put the §26
   completeness statement or a non-project custodian; anchoring resolution
   becomes ambiguous with multiple representations).

## Decision

A **holding** links **exactly one LRMoo Item** to **one or more PREMIS
representations** (original plus derivatives) and carries the **§26
completeness statement** as typed content: original / archival copy /
derivative / screenshot / transcript / fragment / metadata-only. External
custodians' copies (§26) are holdings with a non-project `custodian` and no
representation link. **Annotation targets (DR-0018) resolve through holdings**
to version-pinned representations.

## Consequences

- "What does the archive actually possess, and how completely" is a typed
  query (§26; never implied possession).
- Evidence anchoring has one stable resolution path from annotation to bytes.
