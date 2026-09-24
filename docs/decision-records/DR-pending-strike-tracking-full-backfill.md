# DR-pending-strike-tracking-full-backfill — Authorizing full historical backfill of kpszsu and generalstaffzsu

**Category:** operations / preservation | **Status:** Approved | **Decided:** 2026-09-23 by founder/principal editor
**Origin:** founder's direction of 2026-09-23, choosing "Authorize and run the full backfill now" after two consecutive clean bounded backfill passes | **Supersedes:** `DR-pending-strike-tracking-registration.md` Decision 3's "a full backfill is NOT authorised by this record" clause, for these two sources only | **Superseded by:** —

> **AI provenance (§80).** Drafted by Claude (model: `claude-sonnet-5`) on
> 2026-09-23 at the founder's direction, and **approved by the founder the
> same session**, matching every prior registration/backfill decision's
> pattern.

## Context

`DR-pending-strike-tracking-registration.md` authorised registering
`kpszsu`/`generalstaffzsu` and running one bounded backfill pass each
(`--max-pages 20`), explicitly withholding authorisation for a full
backfill pending that pass's results. Executed 2026-09-22 (20/20 pages
each, 0 failed, no rate-limit signals). A second, larger bounded pass
(`--max-pages 100`, resumed from each channel's stop point) was run
2026-09-23 at the founder's direction as a further scale check: again
100/100 pages each, 0 failed, no rate-limit signals — 240 total backfill
requests across both channels and two passes, zero problems.

`kpszsu` has ~79 000 total posts (message ids); as of this record it has
been walked back to post id 77184, meaning roughly 1 900+ further pages
remain at the tool's current 3-second-delay, single-page-per-request
pace. `generalstaffzsu`'s total post count is still not independently
confirmed (never checked directly — only inferred from how far backward
paging has reached, 39618 so far), so its remaining page count is
unknown until its own history is exhausted.

Given two consecutive clean bounded passes at increasing scale (20 pages,
then 100 pages, both channels, 0 failures, 0 rate-limit signals), the
founder judged this sufficient evidence to authorise completing the
backfill for both channels now, rather than running further bounded
scale checks first.

### Relation to POL-0001 §10 and DR-0072

Added 2026-09-24 on the founder's ruling; see the Revision note. The record as
approved said nothing about this, which a reader could reasonably have read as
the question never having been considered.

**Why this sits inside the founder's ruling of 2026-09-08.** That ruling
suspends collection scale-up until the POL-0001 §10 review is recorded, and
permits preparatory work that "collects nothing, or collects only from
registered sources with configured scope". Both channels were registered first,
as their own separate decision
([`DR-pending-strike-tracking-registration.md`](DR-pending-strike-tracking-registration.md));
their `run_locators` name two specific channels; every pass is bounded and
resumable, from a configured start point, against those two locators only.
There is no crawl, no open-web discovery, and no third source reached by
following a link (DR-0071(a), which is excluded before and after the review
alike).

**Nothing here structures anything.** DR-0066 holds and is verified rather than
assumed — zero documentary assertions across every run to date. POL-0001 §4 and
DR-0071(b) forbid automatic structuring of personal data, and never of the
special-category list, for any person category; a backfill preserves bytes and
crosses no gate. Preservation without structuring is what this record
authorises and all that it authorises.

**What this record does not settle, and no session may.** This is a question of
degree as well as kind, and both halves are open:

- *Degree.* The six sources registered before these two amount to a handful of
  files. This authorises paging to the bottom of two channels' histories —
  ~79 300 posts for `kpszsu` alone. "Scale-up" is the ruling's own word, and
  whether a corpus of this size is inside the carve-out on volume as well as on
  form is not a question a session should answer. The founder authorised it
  twice, on the evidence of two clean bounded passes; that is a founder ruling,
  not a finding that the tension does not exist.
- *Kind.* Every earlier source is an institutional sanctions publisher whose
  material is structured, official and close to free of personal data — the
  reason `CLAUDE.md` gives for choosing them first. These are free-text reports
  of strikes and their effects, which can name places, casualties and
  individuals. POL-0001 §10's review is pending and §8.3's "archiving primary,
  expression secondary" ruling is itself in question under LIL Arts. 46 and 80
  (DR-0099, DR-0100, and the A6 brief's Q2 and Q3).

If Part A's advice, once recorded, bears on material of this kind, the
remediation surface is this corpus rather than six sanctions files. That is
stated here as a consequence a future reader must be able to find, not as a
reason to stop — the founder has ruled, and this record records the ruling.
Civilian-casualty data specifically remains deferred and unstarted.

## Alternatives considered

1. **Authorise the full backfill for both channels now** (chosen). Matches
   the founder's stated preference and the evidence in hand: two
   consecutive clean passes at increasing scale is a reasonable basis for
   confidence, and further incremental scale checks (e.g. a third pass at
   `--max-pages 500`) would mostly just delay reaching the same
   destination without changing the decision.
2. **Run one more, larger bounded pass before deciding** (e.g.
   `--max-pages 500`). Rejected as the next step: available if problems
   emerge during execution of the full backfill (this record does not
   preclude falling back to bounded passes if failures or rate-limit
   signals appear), but not chosen as a precondition given the founder's
   explicit choice.
3. **Defer full backfill indefinitely, register and collect only.**
   Rejected: the founder's stated core purpose is completeness
   ("EVERY SINGLE MISSILE, DRONE"), and both channels are known-reachable,
   known-paginable, with no problems found in 240 real requests.

## Decision

On approval:

1. **A full historical backfill of `kpszsu` and `generalstaffzsu` is
   authorised**, superseding `DR-pending-strike-tracking-registration.md`
   Decision 3's full-backfill withholding for these two sources only (no
   other source's authorisation is affected).
2. **Execution proceeds as a sequence of bounded, resumable passes**, not
   one unbounded run — matching the tool's own design
   (`collector/telegram_backfill.py --max-pages N --start-before <id>`)
   and the runbook's caution against running the whole thing unattended.
   Each pass reports its own stop point; the next pass resumes from
   there. This record authorises running these passes to completion (the
   bottom of each channel's history) across as many sessions/check-ins as
   it takes — a multi-thousand-request effort is not expected to
   complete in one sitting, per the runbook's own estimate (2 500-4 000
   requests for `kpszsu` alone).
3. **The delay and pass-size parameters remain the operator's per-pass
   choice** (this record does not fix them), but the runbook's existing
   guidance stands: never run both channels' backfills concurrently from
   the same host, and treat any fetch failure or unusual response as a
   signal to pause and check for rate-limiting before continuing, not to
   retry immediately.
4. **Nothing from any backfill pass crosses Gate 2** (DR-0066,
   Principle 5), unchanged from every other collection in this project.
5. **This decision is specific to these two sources.** It authorises no
   other source's backfill and sets no general policy for future
   Telegram-channel registrations, each of which remains its own
   decision per DR-0093 §3 and this project's standing per-source
   registration discipline.

### How to execute

On the archive server, continuing from the resume points recorded in
`DR-pending-strike-tracking-registration.md`'s *Executed* section
(`kpszsu` at `--start-before 77184`, `generalstaffzsu` at
`--start-before 39618` as of this record's drafting — check that
record's latest entry for the current resume point before each pass, as
it will have advanced).

```bash
# repeat per channel, resuming from the last pass's earliest-id-seen,
# until "stopped because: reached bottom of history" (not --max-pages).
python3 collector/telegram_backfill.py --source kpszsu --channel kpszsu \
        --dbname uiw --agent <agent id> --archive-root ~/uiw-archive \
        --start-before <last stop point> --max-pages <N> --delay 3

python3 collector/telegram_backfill.py --source generalstaffzsu \
        --channel GeneralStaffZSU --dbname uiw --agent <agent id> \
        --archive-root ~/uiw-archive --start-before <last stop point> \
        --max-pages <N> --delay 3
```

Record each pass's results in `DR-pending-strike-tracking-registration.md`'s
*Executed* section (not this record's), keeping the running account of
every pass in one place.

## Executed

Not yet — this record authorises the work; execution continues under
`DR-pending-strike-tracking-registration.md`'s *Executed* section, which
already tracks every pass to date and will continue to.

## Consequences

1. **kpszsu and generalstaffzsu's full histories become reachable**, once
   completed — the first sources in this project where completeness
   (not just ongoing coverage) is actually achieved for the founder's
   stated core purpose.
2. **A multi-session execution effort**, tracked across check-ins via the
   resume-point mechanism the tool already provides — no new tracking
   infrastructure needed.
3. **Storage footprint will grow substantially.** `storage/measure.py`
   after the first 120-page combined sample showed ~5.6MB preserved for
   240 requests; extrapolating linearly, `kpszsu`'s remaining ~1 900
   pages alone suggest tens of megabytes more — small in absolute terms,
   but worth re-checking with `storage/measure.py` periodically as the
   backfill proceeds, per WP 3.4 §5.3/A7's own reasoning.
4. **This does not itself achieve "every single missile and drone"** —
   only completeness relative to what these two channels posted. No
   Russian-side source exists yet for either direction, and "effect"
   data (casualties, damage) still needs Gate 2/3 editorial work no
   amount of collection substitutes for, unchanged from
   `DR-pending-strike-tracking-registration.md`'s own caveats.

## Revision note (2026-09-24, founder-ruled)

Revised **in place**, before this record ever reached `main`, under
[DR-0102](DR-0102-drafting-discipline-before-merge.md) Decision 7, on the
founder's express ruling of 2026-09-24.

The same three of Decision 7's four conditions held as for the registration
record revised the same day: never merged to `main`, the founder ruled the
change, and this note records it with its date and reason. The fourth —
revision in the same session as approval, which was 2026-09-23 — did not, and
the founder waived it **explicitly**, having been shown that it did not hold.
Decision 7 states that "not merged yet" is a bound on blast radius and **not**
a reason, so nothing here licenses a future session to infer revisability from
Git state. The alternatives offered and not chosen were to pause the backfill
until §10 is recorded, and to leave both records silent and let the DR that
eventually supersedes DR-0072 address the corpus.

**One change, additive.** A "Relation to POL-0001 §10 and DR-0072" subsection
was **added** at the end of *Context*. Nothing was deleted, altered or
reordered, so there is no replaced text to quote: *Decision*, *How to execute*,
*Executed* and *Consequences* are untouched, and what this record authorises is
exactly what it authorised on approval. The subsection **adds no authorisation
and removes none.**

It exists because the record as approved contained no reference to POL-0001,
DR-0072, personal data or the §10 review, and a reader could not tell whether
the still-pending review had been weighed. It states why registered sources
with configured scope sit inside the founder's ruling of 2026-09-08, records
that DR-0066 is verified at zero documentary assertions and that no structuring
occurs, and leaves the questions of degree and kind open rather than answering
them. Found by a review of the companion registration record on 2026-09-24,
which had the identical gap.
