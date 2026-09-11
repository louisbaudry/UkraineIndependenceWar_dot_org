# DR-0095 — Decision Records are drafted unnumbered; the number is assigned at merge

**Category:** architecture / methodology | **Status:** Approved | **Decided:** 2026-09-11 by founder/principal editor
**Origin:** raised by Claude after the second independent "DR-0087" collision (DR-0093, then DR-0094) surfaced only at merge time; put to the founder directly with three options and a recommendation | **Supersedes:** — | **Superseded by:** —

## Context

Two branches drafting a Decision Record concurrently have now collided on
the same number twice: DR-0093 (against DR-0087…0092) and, separately,
DR-0094 (drafted as "DR-0087" against a branch that had already merged
DR-0087…0093 under a different topic). Both were caught only when the
losing branch was reconciled with `main`, requiring a file rename, a
register edit, and a provenance note explaining the renumbering — cheap
each time, but avoidable.

`docs/decision-records/README.md` instructs "check the register, never
assume" for the next free number, and CLAUDE.md's onboarding notes now tell
every session to diff against `origin/main` before trusting its own view of
the register. Both are necessary but insufficient: checking the register on
a branch only tells a session what was free *when that branch was cut*.
Two branches cut close together, or one long-lived branch beside a fast-
moving `main`, can both check correctly and still collide, because the
check and the draft happen before either branch's number is real. Neither
DR-0080 (registry lifecycle) nor the DR README states a rule for this case,
which is what left the two prior collisions to be resolved ad hoc.

## Alternatives considered

1. **Placeholder naming until merge: no branch ever writes a number that
   might not be free** (chosen). A DR is drafted and reviewed as
   `DR-pending-<slug>.md`, with `DR-pending-<slug>` in its own title and
   every internal self-reference, and is renamed to its real number only
   at the point of merging into `main`, when the register is unambiguous.
2. **A light process note only**: document that collisions get resolved by
   renumbering at merge time, and change nothing about drafting. Rejected
   as the sole fix — it is cheapest but leaves a third collision equally
   possible; the founder chose to remove the race instead of documenting
   it.
3. **A number-reservation mechanism**: a branch claims the next number in a
   small tracked file before drafting, and later branches check it too.
   Rejected for now: it adds bookkeeping infrastructure (a claims file,
   a rule for stale or abandoned claims) to solve a problem that placeholder
   naming solves with no infrastructure at all, since an unnumbered draft
   cannot collide with anything by construction.

## Decision

**A Decision Record is drafted, reviewed, and carries AI provenance under a
placeholder name, never a guessed number.**

1. The file is named `docs/decision-records/DR-pending-<slug>.md`, using the
   same `<slug>` its eventual real filename will keep. Its title reads
   `# DR-pending-<slug> — <title>`, and any place the draft would otherwise
   reference its own number (an AI provenance note, a "numbered out of
   sequence" remark, a cross-reference from a sibling document drafted on
   the same branch) uses `DR-pending-<slug>` instead of a number.
2. The draft is not added to `docs/decision-records/README.md`'s numbered
   register while pending. A working paper or session may still list it by
   slug in prose (as candidate DRs already are, per CDR-numbered items in
   working papers) — the numbered register is the one place a real number
   must never be guessed into.
3. **The real number is assigned exactly once, at merge time**, by whoever
   is reconciling the branch against `main`'s current register: grep the
   register on `origin/main` for the highest `DR-nnnn`, take the next
   integer, rename the file, fix its title and self-references, and add its
   register row in the same commit that completes the merge. This is the
   same mechanical step DR-0093 and DR-0094 each already needed — this
   decision makes it the *only* time a number is written, rather than a
   correction after a guess.
4. This applies to Decision Records specifically. It does not change how
   CDR-numbered candidates inside working papers are numbered (DR-0080 and
   the working-paper convention already handle that continuation-numbering
   case without collision, because CDR numbers are scoped to the working
   paper that mints them) or how SPEC/POL/REQ/METH documents are versioned.

## Consequences

- **A DR number can no longer be wrong before merge**, because none is
  written until merge. The failure mode this closes is structural, not
  procedural: there is nothing left to check that could still be stale.
- **One extra rename step is required at merge for every DR**, not only the
  colliding ones. This is a strictly smaller cost than what the two prior
  collisions each already paid, since there is never a wrong guess to
  unwind — only a placeholder to resolve, exactly once.
- `docs/decision-records/README.md`'s register-and-provenance text and
  CLAUDE.md's "Documents: where things go and how they are made" section
  are updated in the same change that enacts this DR, so the instruction a
  session reads matches the rule in force.
- Existing DRs are unaffected; this governs drafting going forward only.
  The provenance notes on DR-0093 and DR-0094 explaining their own
  renumbering remain in place as the historical record of why this DR
  exists.
