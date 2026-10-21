# Runbook — one sitting at the archive server

**Status:** Operator runbook, not a Decision Record and not a controlled
document under DR-0046. It enacts nothing and authorises nothing new: it puts
the archive-server steps that already exist as separate board cards, in one
order, so they can be done in one trip. **It does not replace the cards.** Each
step names its card; the card is closed by a person, after the step, by
saying what was seen.
**Author:** AI assistant (Anthropic Claude Code agent session), 2026-10-12.

**Not verified.** The drafting session has never had access to the archive
server. Every command was written from the repository and, where a rehearsal is
claimed, rehearsed on a scratch PostgreSQL 16 cluster with synthetic rows. The
server is believed to run PostgreSQL **15**, not 16 (issue #76, confirmed
2026-09-22); the commands below use nothing newer than 15, but none has run on
15. Role names, paths and the database name (`uiw`, `~/uiw-archive`) are the
ones earlier records used; check them against `setup/install.sh` if the install
differs.

**Public repository.** Do not paste hostnames, addresses, logins, rows or
session cookies into a card, a commit or a record. Quote counts and column
names only.

## What is in it, and why in this order

| # | Step | Card | Writes to the live database? |
|---|---|---|---|
| 0 | Preconditions | — | no |
| 1 | Drift check, then fix the schema if it drifted | #57 (done), #76 | only if drift is found |
| 2 | Backfill the capture series for the first two holdings | #75 | yes, one table, after a plan |
| 3 | Baseline storage and bandwidth measurement | #54 | no |
| 4 | Check six regional Telegram channels' provenance | #61 (DR-0109 step 2) | no |
| 5 | Discharge the pre-fix quarantine copies | #152 | removes files, after a plan |

The order matters in one place: **step 1 before step 2**, because a schema
reload rebuilds the tables the backfill writes to, and the backfill is cheaper to
verify on the final schema. Steps 3 and 4 are read-only and can be done in either
order, or on another day.

**Not in this sitting**, because each needs its own decision or act: registering
the `ua-nsdc-sanctions` candidates (#46, one source at a time), executing
DR-0114 or DR-0115, the monthly runs (#82), the retrospective WARC pull (#55,
new acquisition), and any collection run.

---

## 0. Preconditions

```bash
cd ~/UkraineIndependenceWar_dot_org          # the server's checkout; adjust
git fetch origin main && git status -sb      # expect: on main, not behind
git pull --ff-only origin main
source .venv/bin/activate                    # psycopg lives here
psql --version; pg_dump --version            # note the versions
psql -d uiw -Atc "select version()"
```

Nothing may be writing to the database during steps 1 and 2: no collector run,
no registration, no Telegram backfill in progress.

```bash
psql -d uiw -Atc "SELECT pid, state, left(query, 60) FROM pg_stat_activity \
    WHERE datname = 'uiw' AND pid <> pg_backend_pid()"       # expect: no rows
```

## 1. Is the live schema behind `main`? (card #76; procedure from #57)

```bash
python3 schema/check_drift.py --dbname uiw | tee ~/uiw-backups/drift-$(date +%F).txt
echo "exit=$?"
```

From the commit log the server is probably behind: at least
`source_identity_unique` (#76) and the DR-0094 `acquisition_attempt` columns
(issues #50-#52, #74). Read the exit code, not the absence of output:

| Exit | Do |
|---|---|
| 0 | Nothing to do; say so on #76 and close it. |
| 1, and **every** difference is a missing constraint or index | **Path A** in [`schema-reload.md`](schema-reload.md) step 2 (this is #76's statement, with a duplicate check first). |
| 1, anything else (a missing column, table, enum value, trigger) | The full procedure in [`schema-reload.md`](schema-reload.md), steps 3-8. Expect this. |
| 2 | The check could not run (usually a role without `CREATEDB`: run it as `postgres`). It is **not** "no drift". |

Afterwards, and before step 2, the check must exit 0:

```bash
python3 schema/check_drift.py --dbname uiw; echo "exit=$?"     # expect: exit=0
```

Say on #76 what the first run printed (counts of differences by kind, not
rows) and what you did.

## 2. Backfill the capture series (card #75)

Only after step 1 is clean. It reads the database and prints a plan first; it
writes only with `--commit`, in one transaction, and refuses and writes nothing
if any holding cannot be traced to exactly one source.

```bash
python3 collector/backfill_series.py --dbname uiw
```

Read the plan. Each line names a holding, its series and the time it was
captured. They should all be from **2026-09-09**, the day before the fix: the
card says two holdings, while DR-0093 records five files collected that day, so
the count may be anywhere in that range. A line dated after 2026-09-10 would be
unexpected (such a holding already has its row); a count or a date you cannot
explain, or any `CANNOT PLACE`, is a stop: say so on #75 rather than committing.
When the plan is what you expected:

```bash
python3 collector/backfill_series.py --dbname uiw --commit
python3 collector/backfill_series.py --dbname uiw          # expect: 0 holding(s)
```

Close #75 when the second run reports 0 and the next real capture of either
locator is confirmed unchanged rather than stored again. That second part
happens at the next scheduled run, not tonight; say so on the card.

## 3. Baseline measurement (card #54)

Read-only. Follow step 1 of
[`A7-storage-bandwidth-measurement.md`](A7-storage-bandwidth-measurement.md):

```bash
export PGDATABASE=uiw      # measure.py takes no --dbname; it reads the libpq environment
python3 storage/measure.py --archive-root ~/uiw-archive --json \
    > ~/uiw-backups/a7-baseline-$(date +%F).json
python3 storage/measure.py --archive-root ~/uiw-archive
```

The runbook was written for **two** sources; the numbers now cover ten. Its
"close to 2x" duplication expectation is out of date: since issue #51 a
quarantine copy is removed after admission, but the 2026-09-09 captures predate
that, so expect a ratio between 1x and 2x, nearer 1x as later collection
dominates. That is an expectation, not a measurement; a ratio near 2x across
recent runs would mean the discharge is not running, and is worth saying.

Record it as the runbook's *Recording the results* says, in
`docs/sources/a7-measurement-results-YYYY-MM-DD.md`, quoting
`measure.py`'s output (counts and sizes only). Step 2 of that runbook (the
retrospective pull, #55) is **not** part of this sitting.

## 4. Provenance of the six unconfirmed regional Telegram channels (DR-0109 step 2)

Read-only, and no bytes are kept: the output goes to the terminal. The question
for each is whether the administration's own site links the channel handle,
which is what separates an official channel from an impostor (the lesson of the
rejected `sumy_oda`). From the sessions that wrote
`docs/sources/verification-ua-regional-administration-telegram.md`, four of the
sites blocked them with a 403 and two loaded with no Telegram link.

```bash
UA="$(python3 -c "import sys; sys.path.insert(0,'collector'); from run import DEFAULT_USER_AGENT as u; print(u)")"
for site in cg.gov.ua dp.gov.ua ck-oda.gov.ua kr-admin.gov.ua dn.gov.ua voladm.gov.ua; do
  echo "== $site"
  curl -sSL --max-time 40 -A "$UA" -o /dev/null -w "%{http_code}\n" "https://$site/"
  curl -sSL --max-time 40 -A "$UA" "https://$site/" | grep -oE 'https?://t\.me/[A-Za-z0-9_]+' | sort -u
done
```

For each site, write down one of: **links handle X** (and whether X is the
handle the verification record lists: `chernigivskaODA`, `dnipropetrovskaODA`,
`cherkaskaODA`, `kirovohradskaODA`, `donetskaODA`, `volynskaODA`), **loads, no
Telegram link**, or **blocked (status)**. A site that links a different handle
than the candidate's is the useful finding.

Append the result to `docs/sources/verification-ua-regional-administration-telegram.md`
as a dated section (handles and statuses only; no hostnames of the server). It
**registers nothing**: registering any of them is a separate founder decision,
per source, and DR-0072's suspension still frames the scale question the record
puts to you.

## 5. Discharge the pre-fix quarantine copies (card #152)

Frees the roughly 1.05 GB that the 2026-10-14 measurement found duplicated
(`docs/sources/a7-measurement-results-2026-10-14.md`). Not urgent. **Do the
next real collection run first** if one is due: it shows that new captures are
discharged by the pipeline (issue #51), and this step should only be about the
old ones. It never touches rejected items or ones admitted but not stored.

```bash
python3 collector/discharge_backlog.py --dbname uiw --archive-root ~/uiw-archive
```

Read the first line. Expect about 5,970 copies "verified against the archive",
`0 problem(s)`, and the number "left" equal to the items admitted under a
`discard` or `metadata-only` tier (probably 0). Any `PROBLEM` line is a stop:
the tool exits 2 and has removed nothing; say what it printed on #152 rather
than working around it. When the plan is what you expected:

```bash
python3 collector/discharge_backlog.py --dbname uiw --archive-root ~/uiw-archive --commit
python3 collector/discharge_backlog.py --dbname uiw --archive-root ~/uiw-archive   # expect: 0 quarantine copies verified
python3 storage/measure.py --archive-root ~/uiw-archive                           # PGDATABASE=uiw; ratio should now read about 1.01x
```

Each removal is a `deletion` preservation event naming the collector software
agent. Keep the old database backups until this has run once and `measure.py`
agrees; the files are gone for good, but every one was checked byte-for-byte
against the OCFL copy first.

## First sitting, 2026-10-13

Steps 0, 1 and 2 were done by the founder with an assistant: the drift check
found 20 differences, the full reload followed `schema-reload.md` and passed
every check, and the backfill linked **five** holdings (the five files of
2026-09-09: three OFAC, two EU), not two as issue #75 said. Step 3 was done on 2026-10-14
(results: [`a7-measurement-results-2026-10-14.md`](../sources/a7-measurement-results-2026-10-14.md)); step 4 was
not done. What the server taught is folded into `schema-reload.md`
("First use, 2026-10-13"). One more thing from this sitting: a new SSH session
needs `source .venv/bin/activate` again before any `python3` command here.

## Second sitting, 2026-10-15

Step 5 was done by the founder with an assistant: the plan verified 5,970
copies with 0 problems, `--commit` removed all of them, a second plan found
nothing, and `measure.py` read 1.01x. The checkout was updated first
(`git pull --ff-only` then `source .venv/bin/activate`). Steps 3 and 4 had not
changed. One thing the pull brought that the sitting did not handle: `main`
now carries a schema change the server's database does not have (issue #158; the
`rights_review_state` columns and the Gate 3 checks, #60), so **the drift check
of step 1 must be run, and the schema brought up to date, before the next
collection run**; the collector reads the new column. That was done on
2026-10-21 (`schema-reload.md`, "Second use"): the drift check found exactly
those six differences and the reload brought the server current.

## After the sitting

- Close the cards the steps finished (#76, #75, #54) and comment on #61 with the
  step 4 result. Cards close by a person saying what was seen.
- Keep `~/uiw-backups/<timestamp>/` and any `uiw_prev_*` database until one
  real collection run has succeeded on the new schema (`schema-reload.md` step 8).
- Anything surprising goes on the relevant card as a finding, not into a commit
  message about a hostname or a row.
