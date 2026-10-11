# DR-0116 — The per-run locator check on `eur-lex-sanctions` becomes a recorded gate

**Category:** operations / preservation | **Status:** **Approved**
**Decided:** 2026-10-11 by founder/principal editor, choosing the first of four options put to them
**Origin:** issue #58, opened 2026-09-22 after [`DR-0105`](DR-0105-eur-lex-sanctions-registration.md) was executed | **Supersedes:** — | **Superseded by:** — | **Refines:** DR-0105 Decision 4 (does not change it)

> **AI provenance (§80).** Drafted 2026-10-11 by an AI assistant (Anthropic
> Claude Code agent session), recording a ruling the founder gave the same
> session. The gate was tested against fixtures in a throwaway database. It
> has not been run against the archive server, and EUR-Lex could not be read
> from the drafting session (every request got an empty HTTP 202, a bot
> challenge), so the live check it protects was not rehearsed.

## Context

`eur-lex-sanctions` is the one registered source whose `run_locators` carry a
date that goes stale. The two locators end in the consolidation date of the
regulation and the decision (`20260807` at the last verification), and the
Council moves it roughly monthly. **A stale dated locator still resolves**:
EUR-Lex returns the older consolidated text, no error. A skipped check
therefore collects a superseded consolidation without any signal.

DR-0105 Decision 4 (founder ruling 2026-09-21) requires whoever runs the
collector to re-verify the suffix first, each time, by hand, and records
that no new tooling was built for it. The check has been made, by hand, on
the one run so far. Issue #58 asked whether a step that one person knows
about, written in a decision record and a YAML comment, is enough.

## Alternatives considered

1. **Keep the check manual, make it a recorded hard gate** (chosen). The
   candidate declares `recheck_before_run`; `collector/run.py` refuses a
   real run of such a source unless `--locator-checked YYYY-MM-DD` names a
   date no more than two days old, and records that date on the run.
2. **Automate the check and fail the run if the date moved.** The collector
   would read EUR-Lex's current consolidated date itself. Rejected: it
   depends on parsing a page EUR-Lex fronts with a bot challenge (the
   drafting session could not read it at all), so it would fail for reasons
   unrelated to a stale date, and DR-0105 had already ruled against tooling
   of this kind.
3. **Re-register on an undated locator.** Would remove the problem if an
   always-current URL exists that satisfies DR-0067. Rejected for now: none
   was verified, and a new registration is a new decision.
4. **Leave it as DR-0105 left it.** Free, but the step stays in two places
   that one person knows about.

## Decision

1. **A candidate may declare `recheck_before_run`**, the plain-language check
   a person makes against the live publisher before every run. It is not
   stored in the registry, like the other verification fields.
2. **For a source that declares it, `collector/run.py` refuses a real run
   unless `--locator-checked YYYY-MM-DD` is given**, the date is a valid ISO
   date, is not in the future, and is today or at most two days earlier.
   A dry run needs no date and prints the check to make.
3. **The date is recorded** as `locator_checked` in the run's `configuration`
   (DR-0070). A date given for a source that does not declare the field is
   validated and recorded the same way.
4. **`eur-lex-sanctions` declares it** in `sources/candidates/`. No other source
   does, and none is made to by this record.
5. **The gate is a record, not a proof.** It cannot tell whether the check was
   made. What it changes is that skipping the check is a deliberate act that
   appears in the run's configuration. This record does not claim a
   superseded consolidation can no longer be collected.
6. **The steps live in** [`docs/runbooks/eur-lex-sanctions-run.md`](../runbooks/eur-lex-sanctions-run.md).
7. DR-0105 Decision 4 stands unchanged: the check remains manual, by a
   person, before each run.

## Consequences

1. Running `eur-lex-sanctions` now takes one more flag, and the first
   operator to forget it is refused before anything is fetched.
2. A run made without a real check is detectable afterwards only by a
   `locator_checked` date that does not match the day of the run; the
   record shows the claim, not the fact.
3. If a second source with a stale-prone locator is registered, it gets the
   same one-line field. Revisit option 2 or 3 only if the manual check is
   skipped in practice or EUR-Lex becomes readable by the collector.
