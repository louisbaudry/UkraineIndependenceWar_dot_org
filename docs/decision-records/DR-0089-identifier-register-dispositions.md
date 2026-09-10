# DR-0089 — The identifier register and its five dispositions

**Category:** architecture / preservation / security | **Status:** Approved | **Decided:** 2026-09-09 by founder/principal editor
**Origin:** CDR-P3-38, [WP 3.5](../phase-3/working-papers/wp-3.5-identifier-design.md) §3.2, §5 rule 3 | **Supersedes:** — | **Superseded by:** —

## Context

DATA-009 requires that the resolver return a resource, a documented
redirect, or a tombstone for every identifier ever published, including
those of merged, split and redacted objects. DR-0064 requires permanent
redirects after a merge and a disambiguation record after a split;
DR-0077 requires a tombstone after governed redaction. SPEC-0006 §9A and
DR-0086 add a case none of these covers: an object whose access tier is
not public still exists and may already have been cited.

## Alternatives considered

1. **Five dispositions, including `restricted`** (chosen).
2. Four dispositions; restricted-tier objects return 404 (rejected: a
   cited identifier that later becomes restricted dead-ends, which
   DATA-009 forbids, and the object's existence is hidden).
3. Four dispositions; restricted objects served as tombstones (rejected:
   conflates "removed under §77" with "exists but you may not see it",
   which DR-0029 keeps apart as `redacted` versus `withheld`).

## Decision

1. Every minted identifier has **exactly one current disposition**:

   | Disposition | Meaning | Source rule |
   |---|---|---|
   | `active` | resolves to the object | — |
   | `redirect` | merged; resolves to the successor | DR-0064 |
   | `disambiguation` | split; resolves to a disambiguation record | DR-0064 |
   | `tombstone` | redacted; resolves to the tombstone | DR-0077 |
   | `restricted` | exists; resolves to an access-tier notice carrying the `withheld` absence state | SPEC-0006 §9A, DR-0029 |

2. **Dispositions only move forward.** An `active` identifier may become
   any of the others; nothing returns to `active` except by a recorded
   decision reversing a redaction under §77. **No identifier is ever
   deleted or reissued.**
3. The register is **data, not configuration**: it ships in every dump
   (SPEC-0006) and every release change set (DR-0048), so the resolver
   is reconstructible from the archive alone (PRES-009).
4. The resolver serves the disposition together with an ARK `?info`
   commitment statement.
5. **Disambiguation-record content** (closing SPEC-0002 §6 Q3): the split
   event's date, the deciding agent, the successor identifiers, and the
   grounds citation — nothing more.

## Consequences

- DATA-009 gains its verification object: the register, checked by test
  for the invariant that every identifier ever minted has a disposition
  and resolves.
- The resolver must know access tiers and applies DR-0086's declared
  restrictiveness; it never derives a tier from an ordering.
- SPEC-0006 will need a revision to carry the register in the dump
  format; SPEC-0007 specifies the register schema.
- Reversal of a redaction is a recorded decision, never an edit.
