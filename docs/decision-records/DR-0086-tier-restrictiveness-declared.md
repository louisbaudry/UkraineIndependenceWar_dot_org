# DR-0086 — Access-tier restrictiveness is declared, never derived from an ordering

**Category:** security / architecture | **Status:** Proposed — awaiting founder decision
**Origin:** defect found while implementing Gate 3 (`schema/07-publication.sql`) | **Supersedes:** — | **Superseded by:** —

## Context

Several rules resolve the question *several tiers apply; which governs?* — a
preserved object referenced by more than one holding, a page rendering more
than one conclusion, an export deciding what a disclosure dump may contain.
The answer must always be the most restrictive tier.

`export/tiers.py` resolved it with `min()` over the tier text, and stated in
its own rationale that "bytes are as restricted as the most restricted
holding that references them."

**It did not do that.** `min()` over text is alphabetical:

```
confidential < internal < investigator-restricted < private-preservation
            < public < researcher-restricted < subscriber
```

so `min('public', 'subscriber')` is `'public'` — the *less* restrictive of
the two. A preserved object referenced by both a public holding and a
subscriber-only holding resolved to `public` and would have been included in
a public disclosure dump.

The PostgreSQL enum's own declaration order gives the same wrong answer, so
switching from text to enum comparison would not have fixed it. **No ordering
the database supplies ranks these tiers by restrictiveness**, and none could:
`researcher-restricted` and `investigator-restricted` are lateral grants to
different named parties, not rungs on a ladder, so restrictiveness is not a
total order over the vocabulary at all.

The defect was latent rather than exploited — the archive holds no real
material — but it sat in the code path SEC-004 names as blocking release.

## Alternatives considered

1. **Declare restrictiveness explicitly, in both the schema and the export
   policy, and test that the two agree** (chosen).
2. Reorder the `access_tiers` enum so its natural order ranks
   restrictiveness (rejected: it would make the ordering correct only until
   someone adds a tier, it cannot express the lateral grants at all, and
   changing an enumeration data depends on is a structural registry change
   under DR-0080).
3. Resolve in one place only — SQL or Python — and have the other call it
   (rejected: the export policy must be readable and runnable without a live
   database, and the schema must enforce independently of any application).
4. Leave it and rely on review (rejected: the rationale comment already said
   the right thing and the code still diverged from it, which is exactly the
   failure a comment cannot catch).

## Decision

*Proposed, not yet decided.*

1. **Restrictiveness is declared, never derived.** `tier_restrictiveness()`
   and `most_restrictive_tier()` in `schema/02-core.sql`; `RESTRICTIVENESS`
   and `most_restrictive()` in `export/tiers.py`. Neither the enum order nor
   alphabetical order is used for this question anywhere.

2. **Lateral grants share a rank, and a tie escalates.** Where
   `researcher-restricted` and `investigator-restricted` both apply, neither
   grant covers the other's material, so resolution returns `internal`
   rather than picking one.

3. **An empty set resolves to `confidential`.** Unclassified is not the same
   as safe.

4. **"No classification at all" is checked separately from resolution.**
   Because (3) fails closed, an absent decision is indistinguishable from a
   very restrictive one by its resolved value alone. Callers that need to
   detect absence — Gate 3's OPS-001 check is the first — must test for it
   directly. This is DR-0029's rule applied to tiers: a missing value never
   quietly means something.

5. **The two implementations are checked against each other by test**, not
   trusted to stay aligned. A rank present in one and absent from the other
   fails the suite.

## Consequences

- SEC-004's guarantee becomes true rather than intended. The previous
  behaviour would have leaked subscriber-tier material into a public dump
  once real holdings existed.
- Adding an access tier now requires a deliberate restrictiveness ruling in
  two places, and the suite fails until both are made. That friction is the
  point: a tier whose restrictiveness nobody decided cannot be resolved
  safely against others.
- The same resolution now governs Gate 3's page tiers, so a page is as
  restricted as its most restricted live publication decision.
- **Not addressed here:** whether `researcher-restricted` and
  `investigator-restricted` should remain distinct at all, given that they
  never compose. That is a §12 vocabulary question, not a resolution one.
