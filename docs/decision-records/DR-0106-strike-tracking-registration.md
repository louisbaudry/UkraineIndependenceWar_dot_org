# DR-0106 — Fifth and sixth source registrations: kpszsu and generalstaffzsu

**Category:** operations / preservation | **Status:** Approved | **Decided:** 2026-09-21 by founder/principal editor
**Origin:** founder's direction of 2026-09-21 ("Yes, register both and run a bounded backfill"), following the redirection of the project's central purpose toward strike-level completeness and the 2026-09-21 verification/rehearsal of both candidates | **Supersedes:** — | **Superseded by:** —

> **AI provenance (§80).** Drafted by Claude (model: `claude-sonnet-5`) on
> 2026-09-21 at the founder's direction, and **approved by the founder the
> same day**, matching every prior registration's pattern. Approval is
> what authorises the registrations and the bounded backfill pass
> described below; both are executed on the archive server by the
> founder, per *How to execute*, and have not been executed by this
> record.

## Context

The founder redirected the project's central purpose mid-session on
2026-09-21: not territorial control, but strike-level completeness — "to
come the closest possible to record EVERY SINGLE MISSILE, DRONE, that fell
on each side and their effect." `kpszsu` (Ukraine's Air Force — incoming
strikes over Ukraine) and `generalstaffzsu` (Ukraine's General Staff —
outgoing Ukrainian strikes into Russia) were identified, fetched live, and
rehearsed end to end through the real collector the same day: 1 discovered,
1 acquired, 0 failed each, 112 688 and 172 322 bytes respectively
([verification record](../sources/verification-strike-tracking-first-two.md)).

Both are official Ukrainian government Telegram channels, captured via
Telegram's public preview (`t.me/s/<channel>`), which needs no
authentication. Neither has a verified rights/redistribution basis;
`may-preserve`/UNVERIFIED is the class default, same posture as most
sources this project has registered.

A companion mechanism, `collector/telegram_backfill.py`
(`CDR-P3-46`, still candidate, built and tested the
same day), walks a channel's pagination backward to reach posts older than
the live page shows. This record authorises registering both sources
**and** running one bounded backfill pass per channel (`--max-pages 20`,
roughly 400-600 posts each) — a cautious first real-scale exercise of the
backfill mechanism, not a full historical backfill. A full backfill (an
estimated 2 500-4 000 requests for `kpszsu` alone) is explicitly **not**
authorised by this record and needs a separate founder decision once the
bounded pass's results (rate-limit behaviour, storage footprint, content
quality) are known.

### Relation to POL-0001 §10 and DR-0072

Neither this record nor its execution is a collection scale-up of the kind
DR-0072 and the founder's ruling of 2026-09-08 suspend. That ruling permits
preparatory work that "collects nothing, or collects only from registered
sources with configured scope"; both channels are registered here first, their
`run_locators` name two specific channels, and the backfill is bounded to
twenty pages each by this record's own step 3. No crawl, no open-web
discovery, no third source reached by following a link (DR-0071(a)).

**What is genuinely new, and is flagged here rather than resolved.** Every
source registered before these two was an institutional sanctions publisher
whose material is structured, official, and close to free of personal data —
the reason `CLAUDE.md` gives for choosing them first. These two are free-text
reports about missile and drone strikes and their effects, a category that can
name places, casualties and individuals. Nothing here structures any of it:
DR-0066 holds, verified rather than assumed (zero documentary assertions, see
*Executed*), and POL-0001 §4 with DR-0071(b) forbid automatic structuring of
personal data in any case. Preservation without structuring is what this
record authorises, and all that it authorises.

The shift in content class is nonetheless real, and this record does not
settle its consequences. POL-0001 §10's external review is still pending;
§8.3's "archiving primary, expression secondary" ruling is itself in question
under LIL Arts. 46 and 80 (DR-0099, DR-0100, and the A6 brief's Q2 and Q3). A
future session must not read this record as having found strike reporting
unproblematic under POL-0001 — only as having preserved it, without
structuring it, at the founder's express direction, while the review runs. The
"effect" half of the founder's stated goal, and civilian-casualty data
specifically, are the parts most exposed here, and both remain undecided.

**This analysis is scoped to what this record authorises — the bounded pass
alone.** The full historical backfill of both channels was authorised
separately on 2026-09-23 by
[`DR-0107-strike-tracking-full-backfill.md`](DR-0107-strike-tracking-full-backfill.md),
which supersedes Decision 3's withholding for these two sources; its passes so
far are *Executed* items 5 and 6. **That record carries no POL-0001 §10 or
DR-0072 analysis of its own, and this subsection does not supply one for it.**
The reasoning above was written for twenty pages per channel. A backfill run to
the bottom of each channel's history — an estimated ~67 000 posts still to come
for `kpszsu` alone, per *Executed* item 6 — is a question of degree that no
record yet puts to the founder in those terms, and the 2026-09-08 ruling's own
words are "no collection scale-up before the POL-0001 §10 legal review is
recorded". Flagged here, deliberately unresolved: a session must not settle it,
and a reader must not mistake the paragraphs above for having settled it.

## Alternatives considered

1. **Register both now, with a bounded backfill pass authorised in the same
   act** (chosen). Matches the founder's own stated preference this
   session; a cautious `--max-pages 20` pass is small enough (an estimated
   40-60 requests per channel at the tool's 3-second default delay, under
   five minutes each) to prove the pipeline works at real scale without
   approaching the rate-limit risk a full backfill carries.
2. **Register only, defer any backfill.** Available and offered to the
   founder as an option; not chosen. Ongoing collection alone does not
   advance the founder's stated completeness goal, which is specifically
   about reaching backward into each channel's existing history.
3. **Authorise a full backfill immediately**, skipping the bounded pass.
   Rejected: the mechanism has been rehearsed for exactly two pages against
   real infrastructure. Committing to thousands of requests before seeing
   how even twenty behave — timing, content variety, whether Telegram's
   preview changes behaviour under sustained pagination — is the kind of
   caution the runbook itself argues for, not an arbitrary throttle.

## Decision

On approval:

1. **`kpszsu` and `generalstaffzsu` are registered** into the source
   registry with the field values in the candidate file as of this
   record's approval, by `sources/register.py --commit --only kpszsu
   generalstaffzsu`. Accepted individually (§78) but registered together
   as a matter of session convenience, matching DR-0096's precedent for
   `uk-ofsi-consolidated`/`bis-entity-list`.
2. **A first, ordinary collection run against each** (the live head page,
   not backfill) is authorised, matching every other registered source's
   pattern — `--dry-run` first, then a real run.
3. **One bounded backfill pass per channel is authorised**:
   `collector/telegram_backfill.py --max-pages 20 --delay 3` (or more
   cautious), following
   [`docs/runbooks/telegram-channel-backfill.md`](../runbooks/telegram-channel-backfill.md).
   **A full backfill is NOT authorised by this record** — its own
   estimated request count and unresolved storage-cost question (per the
   runbook's "Known gaps") make it a separate decision, once this bounded
   pass's results are in.
4. **Nothing from any run crosses Gate 2** (DR-0066, Principle 5),
   unchanged from every other registered source.
5. The registrations carry the obligations `register.py --dry-run` prints:
   permanent retention with DR-0005 fixity checking, and the unverified
   `may-preserve` rights position, unchanged by this record.
6. **This decision is independent of every other pending registration**
   (`ua-nsdc-sanctions`, `isw-orca`, `deepstatemap`) — none is required,
   authorised, or affected by this record.

### How to execute

On the archive server, current `main` (schema already current as of
DR-0105's execution). Reuse the person `pipeline_agent` id from DR-0093's
step 1.

```bash
# 1. register both.
python3 sources/register.py --check
python3 sources/register.py --dry-run --only kpszsu generalstaffzsu
python3 sources/register.py --commit --dbname uiw \
        --agent <person agent id> --only kpszsu generalstaffzsu

# 2. a first ordinary run each (the live head, not backfill).
python3 collector/run.py --source kpszsu --dbname uiw \
        --agent <agent id> --archive-root ~/uiw-archive --dry-run
python3 collector/run.py --source kpszsu --dbname uiw \
        --agent <agent id> --archive-root ~/uiw-archive
python3 collector/run.py --source generalstaffzsu --dbname uiw \
        --agent <agent id> --archive-root ~/uiw-archive --dry-run
python3 collector/run.py --source generalstaffzsu --dbname uiw \
        --agent <agent id> --archive-root ~/uiw-archive

# 3. one bounded backfill pass per channel -- --dry-run first.
python3 collector/telegram_backfill.py --source kpszsu --channel kpszsu \
        --dbname uiw --agent <agent id> --archive-root ~/uiw-archive --dry-run
python3 collector/telegram_backfill.py --source kpszsu --channel kpszsu \
        --dbname uiw --agent <agent id> --archive-root ~/uiw-archive \
        --max-pages 20 --delay 3
python3 collector/telegram_backfill.py --source generalstaffzsu \
        --channel GeneralStaffZSU --dbname uiw --agent <agent id> \
        --archive-root ~/uiw-archive --dry-run
python3 collector/telegram_backfill.py --source generalstaffzsu \
        --channel GeneralStaffZSU --dbname uiw --agent <agent id> \
        --archive-root ~/uiw-archive --max-pages 20 --delay 3

# 4. see where the project now stands
python3 release/baseline.py --check --dbname uiw
python3 storage/measure.py --dbname uiw
```

Note `--channel` differs from `--source` for `generalstaffzsu`: the
registry key is lowercase, the actual Telegram channel name (as it
appears in `data-post` attributes) is `GeneralStaffZSU`.

## Executed

**2026-09-22, on the archive server**, by the founder, per *How to execute*.

1. **Registration.** `sources/register.py --commit --only kpszsu
   generalstaffzsu` was run, resulting in **two `source` rows per
   candidate** rather than one — a double invocation left duplicate rows
   for `kpszsu` (`8aad3518-…` and `dcb3a252-…`) and `generalstaffzsu`
   (`ef186f99-…` and `d835c0ee-…`), 12 seconds apart, both `active`,
   identical `name`/`locator`. This surfaced as `collector/run.py`
   refusing both sources: "matches 2 registered sources by name and
   locator; resolve the duplicate in the registry before running" —
   `resolve_registered_source`'s existing duplicate check working exactly
   as intended. Diagnosed with a read-only query confirming both rows had
   **zero** `collector_run` references before either was touched; the
   later-created duplicate of each pair was deleted
   (`dcb3a252-4c1d-4e6b-9643-ce95a52e6912`,
   `d835c0ee-bbd0-4c4f-a34a-6473b4d1ca21`), leaving one row per source.
   No code changes were needed — `register.py --commit` being safely
   re-runnable into duplicate rows (rather than upserting or refusing) is
   a real gap, not addressed here since it did not block this record's
   own execution once diagnosed.
2. **First ordinary collection run, each channel** (the live head, not
   backfill): `kpszsu` — 1 discovered, 1 acquired, 0 failed, 112 709
   bytes; `generalstaffzsu` — 1 discovered, 1 acquired, 0 failed, 135 349
   bytes. Both clean.
3. **Bounded backfill pass, each channel**
   (`collector/telegram_backfill.py --max-pages 20 --delay 3`), per this
   record's authorisation and the runbook:
   - `kpszsu`: 20 pages attempted, 20 preserved, 0 failed, earliest post
     id reached **79190** (resume point: `--stop-before-id 79190` — or
     `--start-before 79190` to continue backward from there).
   - `generalstaffzsu`: 20 pages attempted, 20 preserved, 0 failed,
     earliest post id reached **41903** (resume point:
     `--start-before 41903`).
   - No rate-limit signals observed on either channel across 40 total
     backfill requests plus 2 ordinary runs, at the tool's 3-second
     default delay.
4. **Verification.** `storage/measure.py --archive-root ~/uiw-archive`:
   `kpszsu` 21 runs / 21 items / 2 398 262 bytes preserved; `generalstaffzsu`
   21 runs / 21 items / 3 171 365 bytes preserved. `SELECT count(*) FROM
   documentary_assertion` = 0, confirming DR-0066 held across every run.
   `release/baseline.py --check` reports the expected `dataset_snapshot`
   gap only (no publication is being made here) — unrelated to this
   record.
5. **2026-09-23 — a second, larger bounded pass, each channel**
   (`--max-pages 100 --delay 3`, resumed from each channel's step-3 stop
   point), founder-directed as a scale check before deciding on a full
   backfill:
   - `kpszsu`: `--start-before 79190`, 100 pages attempted, 100 preserved,
     0 failed, earliest post id reached **77184** (resume point:
     `--start-before 77184`).
   - `generalstaffzsu`: `--start-before 41903`, 100 pages attempted, 100
     preserved, 0 failed, earliest post id reached **39618** (resume
     point: `--start-before 39618`).
   - Still **no rate-limit signals** on either channel, now across 240
     total backfill requests plus 2 ordinary runs. This is the evidence a
     full-backfill decision (§*Consequences* item 3) would be made
     against; that decision has still not been made.
6. **2026-09-23/24 — full backfill authorised and begun**, per
   `DR-0107-strike-tracking-full-backfill.md`. Executing as a sequence
   of `--max-pages 500 --delay 3` passes, each resumed from the prior
   pass's stop point:
   - `kpszsu`: `--start-before 77184` → 500/500 pages, 0 failed, reached
     post id **67174** (resume point: `--start-before 67174`).
   - `generalstaffzsu`: `--start-before 39618` → 500/500 pages, 0 failed,
     reached post id **28041** (resume point: `--start-before 28041`).
   - Running totals: `kpszsu` 620 pages backfilled since 2026-09-22
     (20+100+500), 0 failures throughout; `generalstaffzsu` 620 pages,
     0 failures throughout. Still no rate-limit signals across 740 total
     backfill requests plus 2 ordinary runs.
   - `kpszsu` has ~79 300 total posts; post 67174 means roughly
     12 100 posts back from the head, an estimated **~67 000 posts
     remaining** to reach the bottom of its history. `generalstaffzsu`'s
     total post count is still not independently known — its remaining
     distance is unmeasured until its own history bottoms out.

7. **2026-09-24 — `kpszsu`'s 500-page pass extended to 2 000 pages, and
   `generalstaffzsu` reached the bottom of its history**, continuing
   under `DR-0107-strike-tracking-full-backfill.md` at the founder's
   direction ("Keep going now, as many passes as we can fit" then "can we
   try larger batches?", raising `--max-pages` from 500 to 2000 to reduce
   round-trips):
   - `kpszsu`: `--start-before 67174` → 2000/2000 pages, 0 failed, reached
     post id **27066** (resume point: `--start-before 27066`). Running
     total: 2620 pages backfilled since 2026-09-22, 0 failures throughout.
   - `generalstaffzsu`: `--start-before 28041 --max-pages 2000` was
     started, but **the host running it lost power mid-run** before any
     summary was printed. Rather than trust an incomplete/guessed resume
     point, the true state was recovered directly from the database (the
     lowest post id among successful `acquisition_attempt` rows for the
     source, read-only, before any further command was issued):
     `MIN` post id **28**, **1972** successes recorded — the crashed run
     had in fact completed almost all 2000 pages before power was lost.
     A small follow-up pass, `--start-before 28 --max-pages 50`, then
     reported **"stopped because: ... bottom of history"** at post id 1
     (1 further page preserved) — **`generalstaffzsu`'s full historical
     backfill is complete**: 1973 total backfill pages since 2026-09-22
     (20+100+500+2000·[interrupted, recovered]+1), 0 failures throughout,
     0 posts lost to the outage (the tool's per-page-commit design meant
     the interruption cost only the unwritten remainder of one pass, not
     any already-preserved data).
   - This is the first time this project has needed to recover a
     backfill's true progress from the database rather than from the
     tool's own last printed summary — worth noting as a real instance of
     why `acquisition_attempt` records every attempt (§28, PRES-007): the
     recovery query would not have been possible without it. No code
     changes were needed; the tool's existing per-page durability meant
     recovery was a read, not a repair.
   - `kpszsu` is not yet at the bottom of its history: an estimated
     ~52 100 posts remain past post id 27066, unchanged in kind from the
     ~67 000-posts-remaining estimate in item 6, now reduced by the 2000
     pages just completed.

**A full historical backfill of both channels was authorised 2026-09-23**
by `DR-0107-strike-tracking-full-backfill.md`, superseding this
record's step 3 for these two sources only. `generalstaffzsu`'s full
backfill is now complete (item 7); `kpszsu`'s continues from
`--start-before 27066`.

## Consequences

1. **Eight of the project's eleven candidate sources are now registered and
   collected**: the six sanctions authorities, plus these two. The three
   remaining are `ua-nsdc-sanctions` (blocked on a Cloudflare challenge) and
   `isw-orca`/`deepstatemap` (territorial control — verified and rehearsed,
   undecided). Counted against the nine sanctions-plus-strike-tracking
   candidates alone, it is eight of nine. (Corrected 2026-09-24; see the
   Revision note.)
2. **This is the first registration whose collection run's content this
   project has not read in detail before registering** — every sanctions
   source's file format was inspected structurally (CSV columns, XML
   schema); these two are free-text Telegram posts, read for topical
   relevance but not parsed or structured in any way. That is expected and
   correct for this stage (DR-0066: collection creates no canonical
   knowledge), stated here so a future reader does not assume more
   scrutiny happened than did.
3. **The bounded backfill pass's results (timing, any rate-limit signals,
   actual bytes preserved) become the evidence a full-backfill decision
   is made against.** Record them in this DR's *Executed* section when run.

## Revision note (2026-09-24, founder-ruled)

Revised **in place**, before this record ever reached `main`, under
[DR-0102](DR-0102-drafting-discipline-before-merge.md) Decision 7, on the
founder's express ruling of 2026-09-24 following a review of this record the
same day.

**Three of Decision 7's four conditions held plainly**: the record had never
been merged to `main`, the founder ruled the change, and this note quotes the
replaced text in full with its date and reason. **The fourth did not** —
revision in the same session as approval, which was 2026-09-21. The founder
waived it *explicitly*, having been shown that it did not hold, rather than by
inference. Recorded this way deliberately: Decision 7 states that "not merged
yet" is a bound on blast radius and **not** a reason, so no future session
should read this revision as licence to infer revisability from Git state. The
alternative offered and not chosen was to merge as-is and supersede.

Two changes, both from the 2026-09-24 review:

1. **Consequence 1's candidate arithmetic was wrong.** Replaced text, in full:

   > 1. **Five of nine current candidates are now registered and collected**
   >    once executed (the six sanctions sources plus these two, minus
   >    `ua-nsdc-sanctions` still blocked) — actually six of the project's
   >    sanctions-plus-strike-tracking candidates registered, with
   >    `isw-orca`/`deepstatemap` (territorial control) and
   >    `ua-nsdc-sanctions` the only ones left undecided.

   The sentence corrected itself mid-clause, from five to six, and neither
   figure was right. Counted from `sources/candidates/*.yaml`: **eleven**
   candidates in total — seven sanctions authorities, two strike-tracking, two
   war-facts — of which **eight** are registered and collected.

2. **The record said nothing about POL-0001 §10 or DR-0072.** A
   "Relation to POL-0001 §10 and DR-0072" subsection was **added** at the end
   of *Context*; nothing was deleted for it, so there is no replaced text to
   quote. It **adds no authorisation and removes none**. It states why these
   registrations and the bounded pass sit inside the founder's ruling of
   2026-09-08, and flags the shift in content class — institutional sanctions
   data to free-text strike reporting — as an open caution rather than
   resolving it. The gap mattered because a reader of the record as approved
   could not tell whether the still-pending §10 review had been considered at
   all. **Scoped explicitly to the bounded pass** after this branch's parallel
   line of work was merged in: between the founder's ruling and this edit, a
   separate record authorised the full historical backfill and two further
   passes were executed (*Executed* items 5 and 6). The subsection therefore
   states what it does not cover, and names the full-backfill record's
   identical silence on POL-0001 as an open flag rather than filling it — that
   record is approved, is not this record, and was not part of the ruling.

Nothing in the *Decision*, *How to execute* or *Executed* sections was
touched: what was authorised, and what was done on 2026-09-22, are unchanged.
