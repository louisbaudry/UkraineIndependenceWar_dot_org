# Runbook — Telegram channel historical backfill

**Status:** Operator runbook, not a Decision Record and not a controlled
document under DR-0046. It proposes no policy and enacts nothing; it is
instructions for running tooling that already exists and is already tested,
on the archive server, and writing down what comes back.
**Author:** AI assistant (Anthropic Claude Code agent session), at the
founder's direction, 2026-09-21. `collector/telegram_backfill.py` was
rehearsed against the real, live `kpszsu` channel this session (2 pages,
0 failures, correct pagination — `docs/sources/verification-strike-tracking-first-two.md`
has the details) but no full backfill has been run against the archive
server's real database.

## Read this before running anything

**This is CDR-pending-telegram-backfill** — candidate, not decided. The
mechanism itself (walking `?before=` pagination, preserving each page
through the normal `Collector.run()` path) is built and tested. Whether
and how far to actually run it against a given registered channel is a
separate founder decision per channel, same as every registration in this
project (§78). Registering `kpszsu`/`generalstaffzsu` authorises *ongoing*
collection (OPS-001); it does not by itself authorise a multi-thousand-
request historical backfill. Ask before running this at scale against a
channel the founder has not specifically approved a backfill for.

**Rate-limit and block risk is real, not theoretical.** A full `kpszsu`
backfill is an estimated 2 500-4 000 sequential requests to Telegram. If
Telegram rate-limits or blocks the requesting IP, that IP — the archive
server's — loses access to Telegram entirely, including whatever ongoing
`t.me/s/...` collection other registered channels depend on, until the
block lifts (unknown duration, not controlled by this project). Mitigate,
do not eliminate, by:
- a generous `--delay` (the tool defaults to 3 seconds; consider more for
  a first run against a channel this large);
- `--max-pages` on every run except a final, deliberate full pass, so a
  problem shows up after tens of pages, not thousands;
- running one channel's backfill at a time, never both channels'
  concurrently from the same host.

**This does not achieve "every single missile and drone."** It achieves
completeness *relative to what these two channels posted*. See
`docs/sources/verification-strike-tracking-first-two.md` §2 and the
founder's own conversation record for the fuller caveats (no Russian-side
source yet, "effect" data still needs Gate 2/3 editorial work this
backfill does not do).

## Before running

1. The channel must be **registered** (`sources/register.py --commit`)
   first — this runbook does not register anything.
2. Confirm you have the archive-server checkout on current `main`, with a
   current schema (see `docs/decision-records/DR-0105-eur-lex-sanctions-registration.md`'s
   *Executed* section for what "current" meant as of 2026-09-21 and why
   it mattered).
3. Decide `--max-pages` for this run. Recommended for a genuinely first
   run against a channel this size: start with `--max-pages 20` (roughly
   400-600 posts), confirm it behaved as expected (see "What to check
   after," below), before running further.

## Running it

```bash
# 0. dry run first -- confirms registration, agent, and the channel's
#    current locator, fetches and preserves nothing.
python3 collector/telegram_backfill.py --source kpszsu --channel kpszsu \
        --dbname uiw --agent <person pipeline_agent id> \
        --archive-root ~/uiw-archive --dry-run

# 1. a bounded first pass.
python3 collector/telegram_backfill.py --source kpszsu --channel kpszsu \
        --dbname uiw --agent <person pipeline_agent id> \
        --archive-root ~/uiw-archive --max-pages 20 --delay 3

# the run prints, at the end:
#   pages attempted N  preserved N  failed N
#   earliest id seen: <id>
#   stopped because: reached --max-pages 20
#   to resume from here later: --stop-before-id <id>

# 2. to continue from where it stopped, on a later day/session:
python3 collector/telegram_backfill.py --source kpszsu --channel kpszsu \
        --dbname uiw --agent <person pipeline_agent id> \
        --archive-root ~/uiw-archive --start-before <earliest id from step 1> \
        --stop-before-id <some earlier target, or omit to keep going to the bottom> \
        --max-pages 20 --delay 3
```

For `generalstaffzsu`, the same commands with `--source generalstaffzsu
--channel GeneralStaffZSU` (the `--source` is the registry key; `--channel`
is the actual Telegram channel name as it appears in `data-post`
attributes — they differ for this source, lowercase key vs. the channel's
own capitalization).

## What to check after

```bash
# how many pages/runs this backfill has produced so far:
psql -d uiw -c "SELECT count(*) FROM collector_run cr JOIN source s ON s.id=cr.source_id WHERE s.name LIKE '%kpszsu%' OR s.name LIKE '%Air Force%'"

# total bytes preserved:
psql -d uiw -c "SELECT sum(bytes_preserved) FROM collector_run cr JOIN source s ON s.id=cr.source_id WHERE s.name LIKE '%Air Force%'"

# confirm zero documentary assertions, as always (DR-0066):
psql -d uiw -c "SELECT count(*) FROM documentary_assertion"

# storage footprint, using the tooling A7 already built:
python3 storage/measure.py --dbname uiw
```

If a page fetch fails partway, the tool's own output names the exact
`--start-before` value to resume from — use that, do not restart from
the channel's live head, which would re-walk (and re-preserve, wastefully,
though not incorrectly — OCFL content-addressing deduplicates identical
bytes) pages already covered.

## Known gaps, not addressed by this runbook

- No total post-count check for `generalstaffzsu` was done this session —
  its actual backlog size (and therefore the total request estimate) is
  unknown until a first bounded run against it.
- No storage-cost projection for a full backfill exists yet; run
  `storage/measure.py` after the first bounded pass and extrapolate before
  committing to a full run, per WP 3.4 §5.3's own reasoning for A7.
- This mechanism is specific to Telegram's public `t.me/s/` preview
  pagination. It is not a general web-crawling tool and must not become
  one (POL-0001 §9(a) excludes open-web crawling); it only walks one
  registered channel's own declared history.
