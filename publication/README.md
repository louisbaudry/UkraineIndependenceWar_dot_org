# Gate 3 — the publication decision

Implements SPEC-0003 §2 (DR-0066): does accepted knowledge, or a preserved
item, appear on a public surface, and at which access tier (§12)?

```
discovery → acquisition → [QUARANTINE] → GATE 1: preservation
    → preserved holding → normalization → enrichment → classification
    → GATE 2: editorial acceptance → canonical knowledge
    → GATE 3: publication decision → published surface       ← this module
```

With this the pipeline is complete end to end.

## Why it is a separate gate

Accepting something as true and deciding to say it in public are **different
decisions with different consequences**. Collapsing them is how archives end
up publishing what they merely believe. Preservation status and access status
stay independent throughout (Principle 11): material can be permanently
preserved, accepted as true, and never published — and that is a normal
outcome, not a failure.

## What this is not

**Not a website.** It records publication decisions and the revisions that
resulted. Rendering, routing and serving are a later product concern; the
record has to exist first, because §90's history can only start from the
beginning (DR-0052).

**Not the archive.** The site is a projection (Principle 18). Every revision
pins the baseline, methodology, terminology and template it was built from,
so §86's question is answerable — but the answer is *reconstructed* from the
archive, never substituted for it.

## What is enforced

| Rule | Where | Source |
|---|---|---|
| Only a person publishes | `publication_person_check` | §79 |
| No path to a surface without both gates | `publication_person_check`, `revision_respects_tiers` | OPS-001 |
| No universal `is_public` flag; four dimensions | `publication_decision` columns | SEC-003, §12 |
| A page renders nothing above its tier | `revision_*_tier_check` | SEC-004 |
| `confidential` / `private-preservation` are not publication targets | `tier_admits`, `PUBLICATION_TIERS` | SEC-001, §12 |
| A consequential conclusion carries its review qualification | `revision_qualification_check` | METH-0001 §10.1 |
| Published text never asserts a legal finding | `revision_legal_finding_check` | §62 |
| A revision pins what it was built from | `page_revision` NOT NULLs | §86 |
| History from the first publication | `first_revision_is_initial` | §90, DR-0052 |
| Corrections and retractions say what changed | `corrections_explain_themselves` | §77 |
| Nothing is edited in place | `make_append_only` | DR-0055 |

## The §62 check is deliberately crude

A word list cannot police prose. `revision_legal_finding_check` catches the
specific formulations that assert judicial status — "is guilty of", "found
guilty", "constitutes a war crime" — and review catches everything else.

It permits reporting what an authority alleges, because that is a documentary
assertion carrying *their* standard of proof, not the project's conclusion
(§62, METH-0001 §12). The check is a floor, not a substitute for the
editorial discipline above it.

## A tier-resolution defect this work exposed

Writing `tier_admits()` prompted a check of how the existing export policy
resolved "several tiers apply; which governs?" It used `min()` over the tier
text. **That is alphabetical, and `min('public', 'subscriber')` is
`'public'`** — the *less* restrictive of the two.

`export/tiers.py` said, in its own rationale, that "bytes are as restricted
as the most restricted holding that references them." The code did not do
that, and the divergence ran toward disclosure: a preserved object referenced
by both a public and a subscriber-only holding resolved to `public`.

Neither the enum order nor the alphabetical order ranks these tiers by
restrictiveness, and no ordering the database supplies could — the restricted
tiers are lateral grants to different named parties, not rungs on a ladder.
Restrictiveness is now **declared**, in `tier_restrictiveness()` and
`most_restrictive_tier()` (schema) and `RESTRICTIVENESS` /
`most_restrictive()` (Python), with the test suite checking the two agree
rather than trusting them to stay aligned. Where two lateral grants tie,
resolution escalates to `internal`, because neither grant covers the other's
material.

Recorded as **DR-0086**.

## Two places where "absent" is not "restricted"

`most_restrictive_tier()` fails closed on an empty set, returning
`confidential`. That is right for classification and wrong for detection: it
made "this revision has no publication decision at all" indistinguishable
from "this revision is very restricted", and a revision rendering no holdings
would have slipped through. The two are now checked separately — DR-0029's
rule (a missing value never quietly means something) applied to tiers.

## Verification

45 tests. Every enforcement checked by sabotage:

| Sabotage | Tests that failed |
|---|---|
| `tier_admits` made permissive | 2 |
| OPS-001 "no live decision" check removed | 1 |
| `most_restrictive_tier` reverted to min() semantics | 1 |
| Review-qualification check removed | 1 |
| Legal-finding check removed | 3 |

Removing the `revision_holding` tier trigger alone changed nothing, because
`revision_assertion`'s trigger calls the same function — genuine redundancy,
found by sabotage rather than assumed.

**EDIT-005 is demonstrated, not asserted:** the suite publishes a
consequential conclusion, then reproduces it from the record — exact text,
verified digest, pinned methodology and terminology versions, named baseline,
and the assertions it rendered.

**Not verified:** nothing here has served a page to anyone. There is no
renderer, no routing, no HTTP. The record of what would be published is
correct; whether the site built from it reads well is a product question this
layer does not answer.
