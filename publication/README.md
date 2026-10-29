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

**A second public surface is planned: the memorial site** (DR-0109). It is
a publication surface of this gate, not a separate source of facts: every
page is generated from records this gate has approved, and nothing flows
back into the archive. Its first stage publishes incident pages without
names; names wait for the DR-0072 successor and then follow POL-0001 §8.1.
Nothing for it is built yet.

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
| A holding whose rights position is unreviewed is not published, by decision or on a page | `publication_person_check`, `revision_respects_tiers`, `Publisher._require_reviewed_rights` | CDR-P3-45 (candidate), POL-0001 §10 |

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

Enacted as **DR-0086**, approved 2026-08-26. Its open item — whether
`researcher-restricted` and `investigator-restricted` should remain
distinct at all, given that they never compose — is a §12 vocabulary
question, not a resolution one, and stays open.

## Two places where "absent" is not "restricted"

`most_restrictive_tier()` fails closed on an empty set, returning
`confidential`. That is right for classification and wrong for detection: it
made "this revision has no publication decision at all" indistinguishable
from "this revision is very restricted", and a revision rendering no holdings
would have slipped through. The two are now checked separately — DR-0029's
rule (a missing value never quietly means something) applied to tiers.

## Rights review (CDR-P3-45, candidate)

`rights_basis` on a decision is free text, and registered sources carried
`may-redistribute` on a basis whose own words said "NOT LEGALLY REVIEWED".
Nothing stopped a publication resting on it. The review state is now a
declared field (`rights_review_state`, `unreviewed` by default) on `source`
and on `holding`, copied at admission because a holding has no direct link
back to its source. Two schema checks refuse an unreviewed holding: the
`publication_decision` trigger and `revision_respects_tiers`, the latter
because `revision_holding` is the path that actually puts a holding on a page
and needs no decision row. `Publisher` refuses the same early, with the
reason. Every holding admitted so far is `unreviewed`, so no holding can be
published until a person records a review. If the founder amends the
candidate, this changes with it.

### Recording a review (issue #155, DR-0117)

The one act that sets the state, ruled 2026-10-29. `python3
publication/rights_review.py` plans a review (nothing is written without
`--commit`) and records it through the database function
`record_rights_review()`:

- **Per source, one attributed append-only record** (`rights_review`): who, when,
  which source, `reviewed` or `withdrawn`, and the basis. **Only a person**, and
  the database refuses one with no named written basis: counsel's advice
  (`counsel-advice`) or a Decision Record relying on it (`decision-record`).
- **The source's existing holdings are marked in the same act, and the record
  lists exactly which** (`rights_review_holding`). Later holdings inherit the
  source's state at admission. A **withdrawal is its own record** and moves the
  same holdings back; nothing is edited or deleted (§77).
- **Nothing else changes the state.** A plain `UPDATE` of `rights_review_state`
  on `source` or `holding` is refused, a source cannot be inserted already
  reviewed, and `sources/register.py` refuses a candidate that declares it.
- **Which holdings are the source's** is worked out from each holding's
  original locator and the successful acquisition attempts for it (a holding
  has no direct link to its source). A locator also acquired under another
  source is **ambiguous**: left out of a review, included in a withdrawal, and
  reported. A holding no source can be named for is counted and left alone.
- The two tables are `confidential` in the export tier policy (DR-0084).

No review has been recorded. The archive server's schema does not have this yet
(it needs `docs/runbooks/schema-reload.md`).

## Verification

51 tests in `test_gate3.py` (45 before CDR-P3-45), and 33 in
`test_rights_review.py` (issue #155). Every enforcement checked by sabotage:

| Sabotage | Tests that failed |
|---|---|
| `tier_admits` made permissive | 2 |
| OPS-001 "no live decision" check removed | 1 |
| `most_restrictive_tier` reverted to min() semantics | 1 |
| Review-qualification check removed | 1 |
| Legal-finding check removed | 3 |
| CDR-P3-45: decision-trigger guard removed | 1 |
| CDR-P3-45: `revision_respects_tiers` guard removed | 1 |
| CDR-P3-45: `_require_reviewed_rights` neutered | 2 |

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

**`test_rights_review.py` — 33 tests**, against the real pipeline, PostgreSQL
and OCFL. Fourteen sabotages, each turning it red (a fifteenth, `record()`
skipping its own person check, is caught by a crash: the database refuses it):

| Sabotage | Tests that failed |
|---|---|
| person check on `rights_review` removed | 7 |
| the non-empty basis check removed | 7 |
| `rights_review` made editable | 1 |
| its holding list made editable | 1 |
| the guard on `source.rights_review_state` removed | 2 |
| the guard on `holding.rights_review_state` removed | 2 |
| a source may be inserted already reviewed | 1 |
| the function stops updating holdings | 9 |
| the function stops listing the holdings it covered | 2 |
| a review reaches ambiguous holdings | 5 |
| a review reaches another source's holdings | 7 |
| a withdrawal ignores the current state | 3 |
| a repeated review is allowed | 2 |
| the plan-only default removed | 2 |
