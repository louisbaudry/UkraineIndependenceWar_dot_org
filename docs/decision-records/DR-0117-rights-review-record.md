# DR-0117 — A rights review is one attributed, append-only record per source

**Category:** publication / rights | **Status:** **Approved**
**Decided:** 2026-10-29 by founder/principal editor, choosing the recommended option on each of three questions put one at a time
**Origin:** issue #155, opened 2026-10-14 as the follow-up to #60 | **Supersedes:** — | **Superseded by:** — | **Refines:** CDR-P3-45 (candidate; not enacted by this record)

> **AI provenance (§80).** Drafted 2026-10-29 by an AI assistant (Anthropic
> Claude Code agent session), recording three rulings the founder gave the same
> session, and the implementation choices the assistant made around them
> (Decisions 4 to 7, marked as such). Implemented and tested against fixtures in
> a throwaway database (`publication/tests/test_rights_review.py`, 33 checks,
> every rule shown to fail when removed). **Not run against the archive
> server**, whose schema does not have it yet, and **no review has been
> recorded**: this record authorises the mechanism, not any review.

## Context

CDR-P3-45 (candidate, implemented 2026-10-14, issue #60) made
`rights_review_state` a declared field on `source` and on `holding`, and has
Gate 3 refuse any holding that is not `reviewed`. It left one gap: **nothing
could set `reviewed`**, so no holding could ever be published. Issue #155 asked
the founder how that act should work, because it is a policy act, not plumbing:
who may record it and on what evidence, at what level, how it is recorded, and
how it reaches holdings the archive already holds.

Two facts shaped the answer. First, a holding has no direct link to its source
(its capture series id is a hash), so "the source's holdings" has to be worked
out. Second, `sources/register.py` let a candidate file declare
`rights_review_state: reviewed` at registration, which would have been a second,
unrecorded road to the same state.

## Alternatives considered

**Level.** (1) *Per source, one attributed record, existing holdings marked in
the same act and listed in it* (chosen). (2) Per holding: the most precise, but
the archive holds about 6,000 holdings and gains more every month; not workable
for the Telegram channels or monthly reports. (3) Per source, read at
publication time: simplest, a withdrawal acts at once, but it drops the "rights
position as admitted" snapshot that #60 deliberately kept.

**Who, and on what.** (1) *A person, on a named written basis: counsel's advice
or a Decision Record relying on it* (chosen). (2) Counsel's advice only:
strictest, but would make the project wait on counsel for a source whose rights
are plainly open. (3) A person with no evidence: fastest, but "reviewed" would
then mean only that someone said so, which is what the field replaced.

**Earlier holdings.** (1) *Mark them in the same act, listed in the record*
(chosen). (2) Only holdings admitted after the review: strands the first 6,000
holdings. (3) Only a named list: most flexible, more to get wrong each time.

## Decision

1. **A rights review is made per source, as one attributed, append-only
   record** (`rights_review`): who, when, which source, the action, the basis.
2. **Only a person records it** (§79), never software, and the database refuses
   one with no basis. The basis is **a named written reference**: counsel's
   written advice (`counsel-advice`) or a Decision Record that relies on it
   (`decision-record`). A review that names neither cannot be recorded.
3. **In the same act, the source's existing holdings are marked reviewed, and
   the record lists exactly which** (`rights_review_holding`). **Holdings
   admitted later inherit the source's state at admission**, as before.
4. **A withdrawal is its own record**, never an edit. It moves the source and
   the listed holdings back to `unreviewed`. *(Implementation, following from
   §77 and the ruling that the record is append-only.)*
5. **The state changes only through the database function
   `record_rights_review()`.** A plain `UPDATE` of `rights_review_state` on
   `source` or `holding` is refused, and a source cannot be inserted already
   reviewed. A registration candidate can no longer declare `reviewed`
   (`sources/register.py` refuses it). *(Implementation: closes the second
   road.)*
6. **Which holdings belong to a source is resolved by `publication/rights_review.py`**,
   not by a new column on `holding`: a holding's original representation names
   the locator it was captured from, and the successful acquisition attempts for
   that locator name the source. A holding is covered when exactly this source
   acquired it. **A locator also acquired under another source is ambiguous: it
   is left out of a review (it stays unreviewed, the safe state) and reported;
   a withdrawal includes it, because over-withdrawing is the safe error.** A
   holding with no traceable acquisition is left alone and counted. The plan
   prints all three before anything is written. *(Implementation.)*
7. **The two new tables are `confidential`** in the export tier policy
   (DR-0084): a basis can cite counsel's advice and the record names a person.
   *(Implementation; relaxing it later is a separate decision.)*

## Consequences

- **Gate 3 is unchanged.** It still reads `rights_review_state` and refuses
  anything not `reviewed`; this record only gives that state a lawful way to be
  set. Nothing is reviewed today: **no source and no holding is `reviewed`**, so
  nothing can yet be published, which is still the safe default.
- **The first review waits on its basis.** None can be recorded until there is
  written advice or a Decision Record relying on it (#40, Part A; Part B for
  the redistribution questions).
- **A review covers the source as collected so far.** A later capture inherits
  it only if the review has not been withdrawn; if the source's rights position
  changes (a publisher's terms change), the answer is a withdrawal and a new
  review, not an edit.
- **Cost:** a schema change. The archive server's database does not have the two
  tables, the function or the guards; it needs the `schema-reload.md` procedure
  before this can be used there.
- **Not done here:** recording any review; deciding which source is reviewed
  first; enacting CDR-P3-45 itself (it stays a candidate); the web or reporting
  surface for reviews.

## How to use it

On the archive server, after the schema reload, by the person who holds the
advice (plan first, nothing is written without `--commit`):

```bash
python3 publication/rights_review.py --dbname uiw --source-id <uuid> \
    --action reviewed --agent <person pipeline_agent id> \
    --basis-kind counsel-advice --basis-reference "<which advice, and its date>"
```
