# DR-pending-telegram-egress-timing — No egress service for Telegram collection until a named trigger

**Category:** operations / preservation | **Status:** **Approved**
**Decided:** 2026-10-07 by founder/principal editor, choosing option A of three put to them (rules `CDR-P3-59` of [WP 3.11](../phase-3/working-papers/wp-3.11-telegram-egress-options.md))
**Origin:** a founder question of 2026-10-07 about whether a bought service could remove the single-address risk recorded in [`docs/infrastructure.md`](../infrastructure.md) §2.5 and §4 item 7 | **Supersedes:** — | **Superseded by:** —

> **AI provenance (§80).** Drafted 2026-10-07 by an AI assistant (Anthropic
> Claude Code agent session) at the founder's direction, recording a ruling
> the founder gave the same session. The drafter has never had access to
> the archive server and read no log from it: "no signal" below means the
> **repository's records** (DR-0106, DR-0107) show none. If the server
> holds a run record that shows one, this record's factual premise is
> wrong and it should be superseded, not quietly ignored. No provider was
> evaluated and no network request was made in drafting it.

## Context

Every Telegram fetch is a plain HTTPS GET of `t.me/s/<channel>` from the
archive server's single address, with no account
([`docs/runbooks/telegram-channel-backfill.md`](../runbooks/telegram-channel-backfill.md)).
The repository records the risk that Telegram could rate-limit or block that
address, which would stop all Telegram collection at once, and the runbook
adds that the same address serves every other source
(`docs/infrastructure.md` §2.5, §4 item 7).

The record also shows that the risk has not occurred. `kpszsu`'s full
backfill was 3,960 page attempts across passes of 20, 100, 500, 2,000 and
1,340 pages, 3,959 preserved, **0 failures**, and bottomed out at post id 1
([`DR-0106`](DR-0106-strike-tracking-registration.md) *Executed*).
`generalstaffzsu` also reached post id 1, and [`DR-0107`](DR-0107-strike-tracking-full-backfill.md)
records no rate-limit signal in the bounded passes that preceded the full
run. Collection is started by hand, by a person, and can be stopped by one
(`docs/infrastructure.md` §3.1).

[WP 3.11](../phase-3/working-papers/wp-3.11-telegram-egress-options.md)
compared five ways to reach Telegram: a tunnel proxy, a fetch-on-your-behalf
service, a Telegram data API, a second address of the project's own, and
nothing. It put the timing to the founder as `CDR-P3-59`.

## Alternatives considered

1. **Buy on a named trigger.** Nothing is bought, contracted or built now.
   The events below make the founder rule on a proportionate fix, with the
   evidence then in hand. No recurring cost for a risk not observed; the
   risk stays recorded. **Chosen.** Recommended by the drafter.
2. **Buy now as insurance.** Closes the single point of failure today, at a
   recurring cost, for a risk that did not occur even in the heaviest case
   on record, and before any provider's address provenance, terms or Art. 28
   position has been checked.
3. **Never buy; decide when a problem appears.** No trigger is written down.
   The cost is that the first sign of trouble is a block, discovered after
   it has already stopped collection, with no agreed place to look for the
   next step.

## Decision

1. **No egress service is bought, contracted or built now.** The current
   position, direct requests from the archive server's own address, stands.
2. **Three named triggers.** Any one of them returns the question to the
   founder:
   1. **A signal from Telegram.** A collection or backfill run records a
      throttling or refusing response from `t.me` for a locator that
      succeeded earlier (for example a rate-limit status, or a refusal where
      the same page was served before). A person deciding whether a given
      response is such a signal is a judgment call; when in doubt it is
      treated as one.
   2. **A large new backfill.** A decision to run a Telegram backfill of
      **more than a few hundred pages**.
   3. **Unattended collection.** A decision to schedule Telegram collection
      to run without a person starting each run (OPS-001).
3. **A trigger does not buy anything.** It makes the founder rule. The
   first step is chosen then, with the evidence in hand, from the options of
   WP 3.11 §3 that fit the archive's rules: a second address of the
   project's own (option D) or a tunnel proxy (option A). Fetch-on-your-
   behalf services and Telegram data APIs (options B and C) do not fit and
   are not on the menu.
4. **Whoever meets a trigger stops and says so.** A session or person that
   sees a trigger event in a run, or is asked to plan something that meets
   trigger 2 or 3, raises it to the founder before continuing, and does not
   route requests through any intermediary on its own.
5. **The risk stays recorded.** `docs/infrastructure.md` §4 item 7 stays in
   the gap list and cites this record, so a reader sees that it was
   accepted with triggers, not overlooked.

## Consequences

1. **The single point of failure remains, accepted knowingly.** If Telegram
   blocks the server's address, all Telegram collection stops until the
   block lifts, for a duration this project does not control. Trigger 1 is
   meant to catch a *warning* first; it cannot guarantee one comes.
2. **Trigger 2 is deliberately conservative.** Passes of 500 and 2,000 pages
   already ran with no failure (DR-0106), so "a few hundred" is below what
   is known to be tolerated. The founder may set a number by superseding
   this record, if the wording proves too cautious in practice.
3. **`CDR-P3-58` (the eight requirements any egress service must meet) and
   `CDR-P3-60` (Telegram only) are not ruled by this record.** If a trigger
   fires and a tunnel proxy is wanted, `CDR-P3-58` needs a ruling first, and
   `CDR-P3-60` decides whether other sources may share it.
4. **DR-0071, DR-0072 and the 2026-09-08 ruling are untouched.** This record
   changes nothing about what may be collected or how much; it only fixes
   when the question of how requests travel is reopened.
5. **`CDR-P3-59` is discharged by this record.** WP 3.11's text is
   unchanged, so its recorded hash is too.
