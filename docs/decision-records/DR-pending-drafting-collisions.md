# DR-pending-drafting-collisions — Collision discipline: CDR numbers are assigned at merge, and unmerged branches are checked before starting

**Category:** architecture / methodology | **Status:** **Approved**
**Decided:** 2026-09-15 by founder/principal editor (option A of three)
**Origin:** proposed in [DR-0100](DR-0100-jurisdiction-controller-and-hosting.md) Consequence 6, after the third collision of this kind | **Supersedes:** [DR-0095](DR-0095-dr-numbering-placeholder-until-merge.md) | **Superseded by:** —

> **AI provenance (§80).** Drafted 2026-09-15 by an AI assistant (Anthropic
> Claude Code agent session) at the founder's direction, and approved the
> same day. The session that drafted it was itself the second half of the
> third collision, which is how DR-0095's clause 4 came to be re-read
> closely enough to find the false premise at §1.2.

## Context

### 1.1 Three collisions, not one

| When | What collided | Caught by |
|---|---|---|
| 2026-09-08…10 | Two branches each drafted an unrelated **"DR-0087"** | Merge |
| 2026-09-08/09 | WP 3.4 and WP 3.5 each used **CDR-P3-31…35** | Merge (see the working-papers PROVENANCE entry for WP 3.5) |
| 2026-09-14/15 | Two sessions each drafted the **A6 legal-review brief at the same path**, each obtained the same founder ruling on establishment jurisdiction, and each took **CDR-P3-42** | The founder asking whether anything was in flight |

[DR-0095](DR-0095-dr-numbering-placeholder-until-merge.md) was written after
the first and fixed it. The second and third are still open.

### 1.2 DR-0095's clause 4 rests on a premise that is not true

Clause 4 excludes CDR numbers from its rule, reasoning that they need no
protection "because CDR numbers are scoped to the working paper that mints
them". **They are not.** CLAUDE.md's working-paper section says a paper's
candidates are numbered "**CDR-P3-nn** continuing from the last one used
anywhere in `docs/` (grep for it)" — a single global sequence, minted by
whichever paper is drafted next. Two papers drafted the same week therefore
collide by construction, which is exactly what WP 3.4/WP 3.5 did and what
WP 3.6 and the A6 brief did again.

The rule was right; the carve-out was reasoned from a misreading of the
convention it was carving out.

### 1.3 The check that would have caught the third one does not exist

CLAUDE.md's session-start step 3 says to fetch `origin/main` and diff against
it. That is the right instruction and it was followed. It cannot catch a
parallel session, because **unmerged work is not on `origin/main`** — the
2026-09-14 branch had been merged once (PR #26) and then had three further
commits stacked on it, so it was invisible to every check the file
prescribes.

The cost was not the duplicated number. It was a duplicated **day of work**,
two approved records for one decision, and a founder asked the same question
twice.

## Alternatives considered

1. **Leave it.** Three collisions in five weeks, each caught before harm.
   Rejected: the third was caught by the founder's question, not by any
   process, and the next one has no reason to be luckier.

2. **Amend CLAUDE.md only**, adding the unmerged-branch check and leaving
   numbering as it is. Cheapest, and it addresses the expensive half — a
   duplicated document costs far more than a duplicated number. Rejected as
   *insufficient on its own*: CLAUDE.md is guidance a session can skip, the
   CDR carve-out would stay wrong in an enacted record, and DR-0095 would go
   on stating a false premise about how CDR numbers work.

3. **Supersede DR-0095**, carrying its DR rule forward unchanged, extending
   it to CDR numbers, and adding the unmerged-branch check (**chosen**).

4. **A central lock or claim file** (`docs/NUMBERS.md`) that branches edit to
   reserve numbers. Rejected: it moves the collision rather than removing it.
   Two branches editing the same line conflict at merge — which is arguably
   the point — but it adds a mandatory write to every draft, and it does
   nothing at all about the duplicated *document*, which was the real cost
   here.

## Decision

**Nothing is numbered while it is being drafted, and no session starts work
without looking at what is already in flight.**

1. **Decision Records — DR-0095's rule, carried forward unchanged.** The file
   is `docs/decision-records/DR-pending-<slug>.md`, titled `# DR-pending-<slug>
   — <title>`, with every self-reference using the slug. It is not added to
   the numbered register while pending. **The real number is assigned exactly
   once, at merge**, by grepping the register on `origin/main` for the
   highest `DR-nnnn`, taking the next integer, renaming the file, fixing its
   title and self-references, and adding its register row in the same commit
   that completes the merge.

2. **Candidate Decision Records are numbered the same way.** DR-0095's
   clause 4 carve-out is withdrawn. A candidate is drafted as
   **`CDR-pending-<slug>`** throughout its working paper and in anything that
   cites it on the same branch. **The real `CDR-P3-nn` is assigned at merge**,
   in the same commit and by the same method: grep `docs/` on `origin/main`
   for the highest `CDR-P3-nn`, take the next integers in the order the paper
   lists them.

3. **A working paper's deposit hash is computed after its numbers are
   assigned**, so the SHA-256 in
   [`PROVENANCE.md`](../phase-3/working-papers/PROVENANCE.md) covers the text
   as merged rather than a pre-numbering draft. Where a paper was deposited
   earlier under a pre-numbering hash, the existing rule applies unchanged:
   keep the original hash, add the new one, and state the reason — never
   silently.

4. **Before starting work, a session checks the unmerged branches**, not only
   `origin/main`:

   ```bash
   git fetch origin -q
   comm -13 <(git branch -r --merged origin/main | sed 's/^ *//' | sort) \
            <(git branch -r | sed 's/^ *//' | sort)
   git diff --stat origin/main...<branch>
   ```

   If an unmerged branch already holds the document path, the working paper,
   or the Track A item the session is about to start, **the session says so
   and asks before duplicating it**. This is a starting check, not a merging
   check: by merge time the duplicated work already exists.

5. **Where a duplicate is found after the fact, both records are kept and one
   supersedes the other.** Neither is deleted, rewritten, or folded into the
   other: each recorded a real decision on a real date, and §77's
   supersession discipline applies to decision records as much as to the
   Phase I record. DR-0099 and DR-0100 are the worked example.

6. This does not change how SPEC/POL/REQ/METH documents are versioned, and it
   **renumbers nothing already assigned**. CDR-P3-42 stays with WP 3.6;
   CDR-P3-43…45 stay with the A6 brief.

## Consequences

1. **CLAUDE.md is amended in the same commit** — session-start step 3 gains
   the unmerged-branch check with the commands above (verified to run in this
   environment), and the working-paper section gains the `CDR-pending-<slug>`
   rule and the deposit-hash ordering.

2. **DR-0095 is superseded, not deleted.** Its rule survives verbatim at
   Decision 1; what changes is the carve-out its clause 4 made and the
   premise that carve-out rested on. Its register row records the
   supersession at merge.

3. **A cost is accepted.** `CDR-pending-<slug>` is more awkward to discuss
   with the founder than "CDR-P3-42", and the numbering step at merge is one
   more thing to get right. That is the same trade DR-0095 already made for
   DR numbers, and the same one the WP 3.4/WP 3.5 renumbering paid for
   after the fact rather than before.

4. **The starting check will sometimes find nothing**, and it costs two
   commands. When it finds something, it saves a day. The third collision was
   found this way and cost a reconciliation merge that would not have been
   needed had the check existed.

5. **This record does not fix the underlying cause**, which is that parallel
   sessions cannot see each other's work in progress at all. It makes the
   collision visible early instead of at merge. If parallel sessions become
   routine rather than occasional, a real coordination mechanism is a
   separate question — raised here, not answered.

6. **Nothing about collection changes.** LEGAL-009 stays "partially
   satisfied", DR-0071 still binds, Track B does not start.
