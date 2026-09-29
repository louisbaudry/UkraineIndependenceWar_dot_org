# DR-pending-ua-pgo-registration — Register the Prosecutor General's monthly crime report

**Category:** operations / preservation | **Status:** Proposed | **Decided:** —
**Origin:** the founder's rulings of 2026-09-28 on three questions: collect all 20 listed reports (option C of three), prompt the monthly step through the existing reminder (A of three), and skip a separate collector rehearsal (A of three) | **Supersedes:** — | **Superseded by:** —

> **AI provenance (§80).** Drafted 2026-09-29 by an AI assistant (Anthropic
> Claude Code agent session) at the founder's direction. The three rulings
> are the founder's. Each was put as a question with three options and a
> recommendation. On the first question, the founder chose differently from
> the recommendation (B, January–August 2026 plus January–December 2025).
> The wording, reasons and consequences below are the drafter's. **This
> record is a proposal until the founder approves it.** Approval authorises
> the registration and runs described below. **Both are executed on the
> archive server by the founder, per *How to execute*, and have not been
> executed by this record.** This session cannot reach the office's site or
> the archive server's database.

## Context

[DR-0109](DR-0109-civilian-harm-and-memorial.md) Decision 5 puts UN
monitoring and Ukraine's Prosecutor General first in the civilian-harm area,
each source a separate decision. The UN half was registered by
[DR-0110](DR-0110-un-hrmmu-registration.md). This record is the other half.

The candidate `ua-pgo-crime-statistics` (in
[`sources/candidates/civilian-harm.yaml`](../../sources/candidates/civilian-harm.yaml))
is the office's monthly **Unified report on criminal offences (Form 1)**. It
is an Excel workbook of counts. Each edition is cumulative from January of
its year. Its Table 1.20 carries war crimes (Criminal Code Art. 438) and war
crimes that caused a death (Art. 438(2)). The count is of **registered
criminal proceedings**: investigations opened, not victims and not proven
crimes. It was verified between 2026-09-25 and 2026-09-28. The full record
is [`verification-ua-prosecutor-general.md`](../sources/verification-ua-prosecutor-general.md),
merged in PR #94.

What registration takes on, in short:

- **Counts, no names expected.** The workbook is aggregate tables. That
  was seen in the war-crimes lines only, not checked row by row.
- **Rights unverified.** The candidate claims `may-preserve` and nothing
  more (§14). Ukrainian copyright law Art. 8(1)(3) leaves official documents
  unprotected, but Art. 8(1)(6)'s database right may apply instead.
- **The site blocks this project's sessions and answers the archive
  server.** Every check has to go through the server or a browser.
- **The address changes each month.** Every report has a new `file_id` on
  `old.gp.gov.ua`, so each month's link must be read off the listing and
  committed before the run, as DR-0110 Decision 3 requires for the UN
  source.

### Relation to POL-0001 §10 and DR-0072

This is not the collection scale-up that DR-0072 and the 2026-09-08 ruling
suspend. It registers one source with a configured scope: one listing page
and named workbooks, about 400 KB each. The first run is 20 files, about
8 MB, and every later month adds one more. There is no crawl, no discovery
and no link-following (DR-0071(a)). Nothing is structured: DR-0066 holds, and
DR-0109 Decision 4's rule that a person enters data only by a reviewer's
hand is unaffected.

## Alternatives considered

On what the first run collects (the office resets its count every
January, so the newest report says nothing about the previous year):

1. **January–August 2026 only.** One file, in the shape of DR-0110. It
   leaves the archive without a full year. Not chosen.
2. **January–August 2026 plus January–December 2025.** Two files, giving
   2025's closed annual figure. This was the drafter's recommendation. Not
   chosen.
3. **All 20 reports listed: every month of 2025 and 2026** (chosen). Every
   monthly snapshot is kept, so a later revision of a month's figure by the
   office would be visible. It costs 18 more files and 18 more addresses,
   which have not been fetched yet.

On the monthly prompt: **a section in the existing reminder on the 17th**
(chosen), over a separate reminder around the 7th, and over a scheduled job
on the server that would need a credential there.

On rehearsal: **no separate rehearsal** (chosen), over a throwaway-database
rehearsal on the server, and over splitting the first run in two.

## Decision

On approval:

1. **`ua-pgo-crime-statistics` is registered** in the source registry, with
   its class `UA-state-civilian-harm` and the field values in the candidate
   file as of this record's approval, by
   `sources/register.py --commit --only ua-pgo-crime-statistics`.
2. **A first collection run is authorised** against the candidate's 21
   run locators: the listing page and all 20 reports it linked on
   2026-09-27 (January to January–December 2025, and January to
   January–August 2026). It runs after the check in *How to execute* step 1,
   then `--dry-run`, then a real run. No separate rehearsal.
3. **If step 1 finds a report that does not match**, meaning it is not a
   200 response or its served file name names a different month than its
   listing title, that address is removed from `run_locators` before
   registering, and the removal is recorded in *Executed*. It is not
   guessed at or replaced. The rest of the run goes ahead.
4. **One run per later month is authorised**, each against the listing page
   and that month's new report only. The run follows a person reading the
   newest report off the listing on the archive server, putting its address
   into `run_locators`, setting `locator_verified` and committing the
   change. A month whose report cannot be found is recorded as not
   collected.
5. **The monthly step is prompted by the existing reminder** on issue #82
   on the 17th (`.github/workflows/hrmmu-monthly-reminder.yml`). The
   reminder reads nothing from the office's site and gives the read-only
   server command that names the newest report.
6. **Earlier years are NOT authorised.** Reports before 2025 were not looked
   for, and collecting them is a separate decision. Nor are the office's
   other reports, its news, its Telegram channel, `warcrimes.gov.ua` or
   `childrenofwar.gov.ua`.
7. **Nothing from any run crosses Gate 2** (DR-0066, Principle 5). No figure
   is structured until DR-0109 Consequence 5's working paper and a Gate 2
   decision. Before any structuring, a person looks through the workbook
   for personal data (verification record §6).
8. The registration carries the obligations `register.py --dry-run`
   prints: permanent retention with DR-0005 fixity checking, reading
   capacity in Ukrainian at Gate 2, and the unverified `may-preserve` rights
   position. None of them is changed by this record.
9. **This decision is independent of every other pending registration**
   (`ua-nsdc-sanctions-*`, `isw-orca`, `deepstatemap`). It does not change
   DR-0110.

### How to execute

On the archive server, on current `main`, with `.venv` active. Reuse the
person `pipeline_agent` id from DR-0093's step 1.

```bash
# 1. read-only check of all 20 reports: status, served file name, size, SHA-256
python3 - <<'EOF'
import hashlib, re, urllib.request, yaml
UA = {"User-Agent": "UIW-collector/0.1 (+https://github.com/louisbaudry/UkraineIndependenceWar_dot_org)"}
src = next(s for s in yaml.safe_load(open("sources/candidates/civilian-harm.yaml"))["sources"]
           if s["key"] == "ua-pgo-crime-statistics")
for u in src["run_locators"][1:]:
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90); b = r.read()
        name = re.search(r'filename="([^"]+)"', r.headers.get("Content-Disposition") or "")
        print(u.rsplit("=", 1)[1], r.status, name.group(1) if name else "-", len(b), hashlib.sha256(b).hexdigest())
    except Exception as e:
        print(u.rsplit("=", 1)[1], "FAILED", e)
EOF

# 2. register (idempotent per source since #62's fix)
python3 sources/register.py --check
python3 sources/register.py --dry-run --only ua-pgo-crime-statistics
python3 sources/register.py --commit --dbname uiw \
        --agent <person agent id> --only ua-pgo-crime-statistics

# 3. the first run: listing page and 20 reports
python3 collector/run.py --source ua-pgo-crime-statistics \
        --dbname uiw --agent <agent id> --archive-root ~/uiw-archive --dry-run
python3 collector/run.py --source ua-pgo-crime-statistics \
        --dbname uiw --agent <agent id> --archive-root ~/uiw-archive

# 4. where the project now stands
PAGER=cat psql -d uiw -c "SELECT count(*) FROM documentary_assertion;"
PGDATABASE=uiw python3 storage/measure.py --archive-root ~/uiw-archive
python3 release/baseline.py --check --dbname uiw
```

Expected from step 1: 20 lines with status 200, each file name naming the
month its comment in the candidate file gives (`Forma_1_<month>_<year>.xlsx`,
where for example *serpen* is August). `292316` should show 418 672 bytes and
SHA-256 `7c5a33a8…7936`, unless the office has replaced the file. Expected
from step 3: 21 discovered, 21 acquired, 0 failed, about 8 MB, 0 documentary
assertions.

For each later month, follow the reminder on issue #82: run its server
command, paste its YAML, run `register.py --check`, commit, merge, pull on
the server, then repeat step 3.

## Consequences

1. The archive gains the Ukrainian state's own official count of war-crime
   investigations, beside the UN's verified casualty count. The two measure
   different things (investigations opened, victims verified), and neither
   is averaged into the other (DR-0109 Decision 4).
2. **Twenty monthly snapshots on day one.** Because every edition restates
   the year to date, the archive will hold several figures for the same
   months, each dated to its edition. That is intended, and any later
   structuring must say which edition a figure came from.
3. **A second monthly manual step exists,** done in the same sitting as the
   UN one. If nobody does it, the source silently stops growing. The board,
   not this record, tracks it.
4. **Checking always needs the archive server or a browser.** A session can
   prepare commands and read their output, and cannot fetch from the office
   itself.
5. Rights stay unverified. Citing figures with attribution is DR-0109's
   plan; anything more waits for Part B of the legal brief.

## Executed

Not yet. To be filled in when the founder runs *How to execute* on the
archive server.
