# Runbook — running `eur-lex-sanctions` (the per-run locator check)

**Status:** Operator runbook, not a Decision Record and not a controlled
document under DR-0046. It enacts nothing; it is the steps for a person on
the archive server. The rule it carries is DR-0105 Decision 4, enforced by
DR-pending-locator-recheck-gate (issue #58).
**Author:** AI assistant (Anthropic Claude Code agent session), 2026-10-11.
**Not verified:** a real run of this source with the gate. The gate was
tested against fixtures in a throwaway database (`collector/tests/test_run.py`).
From the session that wrote this, EUR-Lex answered every request with an
empty HTTP 202 (a bot challenge), so the live check in step 1 could not be
rehearsed here.

## Why this source needs a check

`eur-lex-sanctions` lists two dated consolidated-text locators
(`CELEX:02014R0269-20260807` and `CELEX:02014D0145-20260807` at the last
verification). The suffix is the consolidation date and moves roughly monthly
when the Council amends the regime. **A stale suffix still resolves**: it
returns the older consolidated text with no error, so a skipped check means
silently collecting a superseded version.

## Steps

1. **Check the live publisher.** Open the base pages
   `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32014R0269` and
   `...CELEX:32014D0145` in a browser, follow each "Consolidated texts" link,
   and read the date of the newest consolidated version for each instrument.
   The server can fetch EUR-Lex (it did on 2026-09-21), but a browser is the
   reliable way to read the list.
2. **If either date moved,** edit `run_locators` in
   `sources/candidates/sanctions-authorities.yaml` (the `eur-lex-sanctions`
   entry) to the new dated CELEX, set `locator_verified` to today, and commit
   that change. If neither moved, change nothing.
3. **Dry run.** It prints the check to make and does not need the date:

   ```bash
   python3 collector/run.py --source eur-lex-sanctions --dbname uiw \
           --agent <person agent id> --archive-root ~/uiw-archive --dry-run
   ```
4. **Run, naming the date you checked.** Use the day you did step 1, which must
   be today or at most two days back:

   ```bash
   python3 collector/run.py --source eur-lex-sanctions --dbname uiw \
           --agent <person agent id> --archive-root ~/uiw-archive \
           --locator-checked $(date +%F)
   ```

   Without `--locator-checked` the run is refused before anything is fetched.
5. **Confirm it was recorded:**

   ```bash
   psql -d uiw -c "SELECT configuration->>'locator_checked', configuration->'run_locators' \
       FROM collector_run c JOIN source s ON s.id = c.source_id \
       WHERE s.name LIKE 'EUR-Lex%' ORDER BY started_at DESC LIMIT 1"
   ```

## What the gate does not do

It cannot tell whether step 1 was done, or done well; a person can type today's
date without looking. It makes skipping the check a deliberate act that shows in
the run's record, which is the point of the founder's 2026-10-11 ruling on
issue #58 (a manual check kept, made a recorded hard gate). Detecting a moved
date automatically, or registering an undated locator, were considered and not
chosen; see the Decision Record.
