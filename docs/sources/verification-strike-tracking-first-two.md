# Verification record — first two strike-tracking candidates

**Status:** Verification record for two candidate registrations. Nothing
here is registered, nothing is collected. This category is the project's
central stated purpose, in the founder's own words (2026-09-21): "to come
the closest possible to record EVERY SINGLE MISSILE, DRONE, that fell on
each side and their effect" — not a side category alongside territorial
control, the actual point. Registering either candidate is the founder's
act, per source, same as every prior candidate.
**Verified:** 2026-09-21, from this session's container.
**Candidates:** `kpszsu`, `generalstaffzsu` in
[`sources/candidates/strike-tracking.yaml`](../../sources/candidates/strike-tracking.yaml)
— a new file, separate from `war-facts.yaml` (territorial control), since
the capture considerations (Telegram pagination) differ materially.

## 1. Why these two, and why together

The founder's ask is symmetric: strikes "on each side." Two official
Ukrainian government Telegram channels cover both directions:

- **`kpszsu`** (Air Force Command) — the **incoming** side: near-real-time
  tracking of individual drone/missile groups over Ukrainian territory.
- **`generalstaffzsu`** (General Staff) — the **outgoing** side: periodic
  summaries of Ukrainian strikes on Russian and Russian-occupied territory.

Neither channel is a Russian source — nothing here documents Russian
strikes from Russia's own reporting, or Russian claims about Ukrainian
strikes on Russia. Both channels are Ukraine's own official communications.
That asymmetry (only one side's official voice, on both directions of the
war) is worth naming, not implying away: a fuller record would eventually
need Russian-side sources too, independently verified given the obvious
incentive problems with wartime self-reporting on both sides.

## 2. The critical limitation: what registration does and does not get you

**This is the single most important thing in this record**, because the
founder's stated goal is completeness ("every single one"), and a plain
registration does not deliver that.

Telegram's public web preview (`t.me/s/<channel>`, used here because it
needs no authentication, unlike the Telegram Bot API or MTProto) shows
only the **most recent ~20-30 messages** by default. `kpszsu` alone has
roughly **79 000 posts** as of this verification (message ids in the
79,300s). Running the collector against the plain `t.me/s/kpszsu` locator,
now or on any future run, retrieves whatever is currently visible —
new posts since the last run, roughly — never the full backlog.

**The good news, confirmed this session:** the preview supports backward
pagination via `?before=<message_id>`. A fetch of
`https://t.me/s/kpszsu?before=79317` returned posts 79297-79299 — genuinely
earlier than what the live page shows. This means the full ~79 000-message
history **is** technically reachable, indefinitely (Telegram does not
appear to expire or hide it), just not via a single `run_locators` entry
the way every other source in this project works.

**What a full backfill would actually require**, not built here:
- A paginated crawl: starting from the current earliest known message id,
  repeatedly fetching `?before=<id>` and extracting the new earliest id
  from each response, continuing until no earlier posts are returned.
  For ~79 000 messages at ~20-30 per page, that is roughly **2 500-4 000
  sequential HTTP requests** for `kpszsu` alone, more for
  `generalstaffzsu` once its own total post count is known (not checked
  this session).
- A capture strategy that treats each page as its own preserved unit (most
  consistent with this project's existing `warc`/per-locator model), or a
  purpose-built bulk-ingest path closer to `Collector.ingest_warc` (A3,
  already built for WARC files from external archives) — an open design
  question, not decided here.
- A rate-limiting/politeness policy for thousands of sequential requests
  against a single Telegram channel — not addressed at all this session.

This is real, substantial, new engineering — closer in scope to a second
A3 (WARC bulk-ingest path) than to registering a normal source. **It should
not be assumed to follow automatically from registering these two
candidates.** Registering them now gets ongoing coverage of new posts;
the historical backfill is separate work this record flags but does not
do.

## 3. What was done, in order

1. Reachability-tested official Ukrainian channels for strike-relevant
   content: `www.zsu.gov.ua` (403, not pursued), `t.me/s/kpszsu` (initial
   connection reset, succeeded on retry), `t.me/s/GeneralStaffZSU` (200
   immediately), `www.facebook.com/CommandPS` (302, not pursued —
   Facebook's own access patterns are a separate problem from Telegram's),
   `mil.in.ua` (301, not pursued — a media outlet, not an official
   channel, out of scope for this pass).
2. Read each channel's most recent posts directly (not assumed from prior
   knowledge) to confirm on-topic content: `kpszsu` showed live UAV-group
   tracking with locations and shelter warnings; `generalstaffzsu` showed
   a weekly strike-summary post naming specific struck facilities in
   Russia with dates.
3. Confirmed `?before=` pagination works for `kpszsu` specifically (not
   re-tested for `generalstaffzsu`, though the same Telegram preview
   mechanism should apply).
4. **Rehearsal**, matching every prior candidate's precedent. A throwaway
   PostgreSQL database built from `schema/0*.sql`. Both sources inserted
   directly. The real `Collector` run with the real `HttpFetcher` against
   both locators, into a throwaway OCFL root. Both succeeded: 1
   discovered, 1 acquired, 0 failed each — `kpszsu` 112 688 bytes,
   `generalstaffzsu` 172 322 bytes. Database and storage destroyed.

## 4. What this does and does not settle

**Settled:** both sources exist, are reachable, carry on-topic content
matching the founder's stated goal, and a real `Collector` run against
them succeeds cleanly.

**Not settled, and not this session's to settle:**
- The historical-backfill engineering described in §2 — a real gap between
  what "register this source" means everywhere else in this project and
  what completeness actually requires here.
- Russian-side sources for the same two directions (Russian claims about
  strikes on Russia; Russian reporting on strikes on Ukraine), which a
  genuinely two-sided record would eventually need, independently
  verified against both governments' obvious incentives to over- or
  under-report.
- Whether `generalstaffzsu`'s mixed content (strike summaries alongside
  general operational updates and press-contact information) needs
  splitting into a narrower scope at some point, or whether that's an
  editorial (Gate 2) judgment to make later against preserved holdings,
  not a registration-time filter.
- Rights/redistribution basis for either — both UNVERIFIED, conservative
  `may-preserve` default, same posture as most sources in this project.
- Registration itself, per the standing ruling that this is the founder's
  act, per source.

## Sources

- [`sources/candidates/strike-tracking.yaml`](../../sources/candidates/strike-tracking.yaml) — both candidate entries, with the backfill limitation stated in the file's own header comment
- [`docs/sources/verification-war-facts-first-two.md`](verification-war-facts-first-two.md) — the territorial-control candidates verified the same day, before this redirection toward strike-level data
- `collector/README.md`, A3 (`Collector.ingest_warc`) — the closest existing precedent for a bulk-ingest path, if a Telegram backfill mechanism is built later
