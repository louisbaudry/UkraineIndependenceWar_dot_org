# DR-0084 — Adoption of the durable export format, with unfiltered dumps blocked

**Category:** architecture / security | **Status:** Approved | **Decided:** 2026-08-21 by founder/principal editor
**Origin:** CDR-P3-30, SPEC-0006 | **Supersedes:** — | **Superseded by:** —

## Context

DR-0058 made durable export a standing obligation and required its format to
be a SPEC-class controlled document. SPEC-0006 was drafted alongside the
implementation and recorded an unresolved risk at its §9: a dump of
everything is a dump of confidential material too (§12, SEC-001), including
submitter pseudonyms and anything else at confidential tier.

## Alternatives considered

1. Adopt the format, blocking unfiltered dumps until access-tier filtering
   exists (**chosen by the founder**).
2. Adopt as-is with the limitation documented and dumps treated as carrying
   the highest tier present (rejected: a documented caveat is a request that
   operators remember something, and the cost of forgetting is disclosure of
   a confidential source).
3. Leave SPEC-0006 a draft (rejected: DR-0058 would stand unsatisfied for a
   format already implemented).

## Decision

**SPEC-0006 v1.0 is adopted, effective 2026-08-21**, on the condition that
**no dump may be produced without a declared purpose**. The condition is
enforced in code, not by convention:

- **`preservation`** — complete, nothing filtered, because succession
  (PRES-010) and reconstruction (PRES-009) need the whole archive. The
  manifest names the highest tier present and states that the dump is not a
  disclosure export.
- **`disclosure`** — filtered to an explicitly named access tier, with
  per-table omission counts and a completeness statement saying it is not
  the whole archive.

There is **no default purpose and no default tier**; the exporter refuses
without them.

Supporting rules:

1. **Tiers are not a ladder.** `researcher-restricted` and
   `investigator-restricted` are lateral grants, not steps above `internal`;
   `private-preservation` is disclosed to nobody. Containment is declared
   explicitly rather than derived from an ordering.
2. **`confidential` and `private-preservation` are not disclosure targets.**
   Material at those tiers reaches a recipient through a preservation dump
   under an explicit arrangement, never a routine export (SEC-001).
3. **Fail closed.** Every table must carry a declared tier rule; an
   unclassified table halts the dump rather than being exported at a
   convenient tier. With SPEC-0006 §3's catalogue-derived table list, a
   forgotten table both appears and stops the run.
4. **Unresolvable means withheld.** A row whose tier cannot be determined is
   omitted, never published.
5. **Omission is stated.** Filtered dumps record what they left out (§57
   applied to exports).

## Consequences

- Preservation and reconstruction remain available; PRES-009's demonstration
  is unaffected.
- Sharing or depositing a dump now requires an explicit, recorded choice
  about who may hold it.
- Whether disclosure dumps should eventually **redact** rather than omit —
  keeping the row and substituting the `withheld` absence state (DR-0029) so
  a reader can see that something exists without seeing it — remains open
  (SPEC-0006 §9B), pending column-level classification.
- The founder's choice of the stricter option is recorded because it changed
  the work: filtering was built immediately rather than deferred, and the
  prohibition took the enduring form "no dump without a declared purpose"
  rather than a temporary block that would later be lifted.
