# Runbook — bringing the live database's schema up to date (schema drift)

**Status:** Operator runbook, not a Decision Record and not a controlled
document under DR-0046. It enacts nothing; it is instructions for a person
on the archive server. **Ruling behind it:** on 2026-10-11 the founder chose,
for issue #57, *a runbook now and a migration mechanism later* (the
mechanism is its own board card, with a named trigger). Until that card is
done this is the only supported way to change the live schema.
**Author:** AI assistant (Anthropic Claude Code agent session), 2026-10-11.

**What was and was not verified.** Every command below was rehearsed
end to end on a scratch PostgreSQL 16 cluster, against a database built from
the DDL as of the 2026-09-21 reload (`7e45c5a`) holding synthetic rows, and
reloaded into a database built from current `main`: backup, rebuild alongside,
reload, row-count comparison, drift check, and the rename swap, including a
row present only in the old database's seeded `source_types` (kept, as
intended) and a DDL loaded by a non-superuser owner and reloaded by the
superuser. The rehearsal connected as the `postgres` role directly, so the
`sudo -u postgres` wrappers are untested. **Not verified:** anything on the
archive server itself (its role names, database
owner, disk headroom, and whether `pg_dump` and `psql` there are version 16);
a restore of a backup into a fresh cluster; the cost of the reload at the
real database's size. Where the server may differ, a step says what to
check first.

## What this is for

The schema is rebuilt from `schema/0*.sql`, never migrated (`CLAUDE.md`,
*Code conventions*). That is fine for a test database and impossible for one
holding real registered sources and preservation history. This runbook is
the procedure for the day the live database falls behind `main`, which it
did on 2026-09-21 (DR-0105 *Executed* §2: ~10 weeks behind, found only when
a run failed with `UndefinedColumn`) and again on 2026-09-25 (DR-0110:
`source_identity_unique` missing, found by reading the commit log).

The procedure differs from DR-0105's improvised one in two ways, both from
its lessons:

- **The new database is built alongside the old one and swapped in by
  rename**, instead of dropping the old one first. Until the swap nothing
  live has changed, and the rollback is a rename back.
- **The data reload uses `--column-inserts --on-conflict-do-nothing`**, not
  a plain data-only dump with every error waved through. A plain `COPY`
  of a seeded lookup table fails whole when one row collides, so a row
  that exists only in the live database would be lost without anyone
  noticing. Row by row, the DDL's seed row wins a collision and every
  other live row is kept. `--column-inserts` also names the columns, so
  columns added to the DDL since the dump simply take their defaults.

## When to run it

Run **step 1** (read-only) whenever any of these is true; run the rest only
if step 1 reports a difference:

- `git log` on the server's checkout shows a commit touching `schema/`
  since the last reload (`git log --oneline <last-reload-commit>..HEAD -- schema`).
  The last reload on record is `7e45c5a`, 2026-09-21 (DR-0105).
- A collection run or `register.py` fails with `UndefinedColumn`,
  `UndefinedTable`, or an enum value the database does not know.
- Before executing any registration or first collection run after pulling
  `main` (`docs/infrastructure.md` §3.2's standing rule).

**Never** run it while a collector run is in progress, and never with the
checkout on a stale branch: that was DR-0105's root cause. The checkout must
be on `main`, up to date.

## Step 0 — preconditions

```bash
cd ~/UkraineIndependenceWar_dot_org        # the server's checkout; adjust
git fetch origin main && git status -sb    # expect: on main, not behind origin/main
git pull --ff-only origin main
source .venv/bin/activate                  # psycopg is installed there (DR-0105 hit this)
pg_dump --version; psql --version          # note the versions
df -h ~ /var/lib/postgresql | cat          # room for two dumps plus a second copy of the database
```

Record the live database's owner before touching anything; the rebuilt
one must match it:

```bash
psql -d postgres -Atc "SELECT datname, pg_get_userbyid(datdba) FROM pg_database WHERE datname = 'uiw'"
```

## Step 1 — check for drift (read-only)

```bash
python3 schema/check_drift.py --dbname uiw
echo "exit=$?"
```

`schema/check_drift.py` builds a throwaway database from the checkout's DDL,
compares catalogs, and drops it. It reads the live database's catalogs
only, never its rows. The connecting role needs `CREATEDB`; if it does not,
run it as `postgres`. Exit codes:

| Exit | Meaning | Do |
|---|---|---|
| 0 | No structural difference on the compared objects | Stop. |
| 1 | Differences listed | Save the output (below) and continue. |
| 2 | The check could not run | Fix that first. **Not** "no drift". |

```bash
python3 schema/check_drift.py --dbname uiw | tee ~/uiw-backups/drift-$(date +%F).txt
```

Read the list. `missing-in-live` is the usual case: the DDL moved on. Two
others need a pause before continuing: **`extra-in-live`** (the live database
has something the DDL does not, meaning a hand edit or something the DDL
has since dropped) and **`differs`** on a constraint or column (the definition
changed). Neither is automatically a problem, but every one must be
understood before its data is carried over, because a data-only reload
cannot reload into a column that no longer exists.

Not compared: row data, so seed-table contents are not checked here.

## Step 2 — choose the path

**Path A, add one thing by hand.** Allowed only when *every* difference is
a missing constraint or index (the `source_identity_unique` case). Copy the
exact statement from the DDL, check the data satisfies it first, take the
step 4 backup, apply it, then re-run step 1 and require exit 0:

```bash
# example for source_identity_unique (schema/03-pipeline.sql); copy the real text from the DDL
psql -d uiw -Atc "SELECT name, locator, count(*) FROM source GROUP BY 1, 2 HAVING count(*) > 1"   # expect: no rows
psql -d uiw -v ON_ERROR_STOP=1 -c "ALTER TABLE source ADD CONSTRAINT source_identity_unique UNIQUE NULLS NOT DISTINCT (name, locator)"
```

If step 1 still reports anything, you have not fixed it: go to Path B.
Do not stack hand edits; two of them is a reload.

**Path B, rebuild alongside and swap.** Everything else: any missing or
changed column, table, enum value, trigger, function or view. Continue.

## Step 3 — freeze and count

Stop anything that writes: no `collector/run.py`, no `register.py`,
no `telegram_backfill.py`. Check:

```bash
psql -d uiw -Atc "SELECT pid, state, left(query, 60) FROM pg_stat_activity WHERE datname = 'uiw' AND pid <> pg_backend_pid()"   # expect: no rows
```

Count every table, before anything else, to a file kept with the backups.
`\gexec` runs one `SELECT count(*)` per table:

```bash
B=~/uiw-backups/$(date +%Y%m%dT%H%M%S); mkdir -p "$B"; cd "$B"
cat > counts.sql <<'SQL'
SELECT format('SELECT %L AS t, count(*) FROM %I', tablename, tablename)
FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename
\gexec
SQL
psql -d uiw -At -F' ' -f counts.sql > counts-before.txt
cat counts-before.txt | awk '$2 > 0'
```

## Step 4 — back up, twice, and prove the backup is the same twice

Two dumps, taken twice. The full dump is for restore; the data dump is
what step 6 reloads. Newer `pg_dump` writes a random `\restrict` token into
each dump, so strip those two lines before comparing (they are the only
expected difference; DR-0105 saw byte-identical dumps before that existed).

```bash
for i in 1 2; do
  pg_dump -d uiw --no-owner > full-$i.sql
  pg_dump -d uiw --data-only --column-inserts --on-conflict-do-nothing \
          --disable-triggers --no-owner > data-$i.sql 2> dump-$i.log
done
for f in full data; do
  a=$(grep -v '^\\\(un\)\?restrict' $f-1.sql | sha256sum); b=$(grep -v '^\\\(un\)\?restrict' $f-2.sql | sha256sum)
  [ "$a" = "$b" ] && echo "$f dumps identical" || echo "$f DUMPS DIFFER - stop"
done
ls -l; sha256sum full-1.sql data-1.sql > SHA256SUMS
```

`pg_dump` prints "circular foreign-key constraints" warnings for several
tables (nine in rehearsal) during the data dump. They are expected; they are why the reload
(step 6) is run as a superuser with triggers disabled.

**These backups sit on the same server.** There is no off-server copy until
the association exists (DR-0108, `docs/infrastructure.md` §3.3). If any
other copy is possible tonight, make it; the reload is lossless in
rehearsal but a rehearsal is not the server.

## Step 5 — build the new database alongside

Create the database as the `postgres` superuser, owned by the role recorded
in step 0, then **load the DDL as that owner**, so the tables belong to
the role the collector connects as. (Loading the DDL as `postgres` would
leave `postgres` owning every table, and the collector's role without
access.) Only the data reload in step 6 needs the superuser, to disable
foreign-key triggers, which `root` could not do (DR-0105).

```bash
sudo -u postgres psql -v ON_ERROR_STOP=1 -c "CREATE DATABASE uiw_new OWNER <owner-from-step-0>"
for f in schema/0*.sql; do
  psql -q -U <owner-from-step-0> -d uiw_new -v ON_ERROR_STOP=1 -f "$f" > /dev/null || { echo "FAILED: $f"; break; }
done
psql -d uiw_new -Atc "SELECT count(*) FROM pg_tables WHERE schemaname = 'public' AND tableowner <> '<owner-from-step-0>'"   # expect: 0
```

Any failure here is a defect in the DDL on `main`, not in the live
database. Stop; `uiw` is untouched. Drop `uiw_new` and report the file.

## Step 6 — reload, then prove it

```bash
sudo -u postgres psql -d uiw_new -v ON_ERROR_STOP=1 -q -f "$B/data-1.sql" > reload.log 2>&1; echo "rc=$?"
grep -c ERROR reload.log      # expect: 0
```

Unlike the plain-`COPY` reload this one has no expected errors. Any
`ERROR` means stop: most often a column the DDL dropped (step 1 would have
shown it as `extra-in-live`) or a new `NOT NULL` column with no default.
Do not edit the dump by hand to get past it; that needs a decision.

Then three checks, all of which must pass before the swap:

```bash
sudo -u postgres psql -d uiw_new -At -F' ' -f counts.sql > counts-after.txt
diff counts-before.txt counts-after.txt && echo "COUNTS IDENTICAL"
python3 schema/check_drift.py --dbname uiw_new          # expect exit 0
psql -d uiw_new -Atc "SELECT count(*) FROM source"     # spot check against counts-before
```

The count diff must be empty for **every** table, seed tables included. A
difference in a seed table means the DDL and the live database disagreed
about a lookup row (the DDL's seed row won); read the diff and decide whether
that is the point of the change or a loss. The data tables are the ones
that matter: `source`, `source_dependence`, `collector_run`, `holding`,
`pipeline_agent`, `preservation_event`, `acquisition_attempt`, and whatever
was added since.

## Step 7 — swap, with the old database kept

Renaming needs every connection closed, which is why step 3 froze writes.

```bash
sudo -u postgres psql -v ON_ERROR_STOP=1 \
  -c "ALTER DATABASE uiw RENAME TO uiw_prev_$(date +%Y%m%d)" \
  -c "ALTER DATABASE uiw_new RENAME TO uiw"
python3 schema/check_drift.py --dbname uiw     # expect exit 0
python3 release/baseline.py --check --dbname uiw   # DR-0105 ran this afterward
```

If the first rename fails with "being accessed by other users", something
still holds a connection: find it with the `pg_stat_activity` query in
step 3 and stop it. Do not use `WITH (FORCE)` to evict an unknown writer.

**Rollback**, at any point after the swap: rename the two back
(`uiw` to `uiw_failed_…`, `uiw_prev_…` to `uiw`). Nothing was changed in
the old database, so it is exactly the state step 3 counted.

## Step 8 — record it, and keep the old database for a while

- Keep `uiw_prev_…` and `~/uiw-backups/<timestamp>/` until at least one
  real collection run has succeeded on the new database. Dropping the old
  database is a separate act, later, by a person, after looking at it.
- Say what happened wherever the triggering work records its execution
  (the DR's *Executed* section, as DR-0105 and DR-0110 did): the commit
  reloaded to, the step 1 output, the counts diff, and anything that
  surprised you. Update the "last reload" commit named under *When to run it*
  in this file. No hostnames, IPs, logins or rows go in it (`CLAUDE.md`,
  *This repository is public*).
- Run a dry collection (`collector/run.py --dry-run`) before the next
  real run.

## If something looks wrong

- **Step 1 exits 2.** Usually the role lacks `CREATEDB`, or the database name
  is wrong. Run it as `postgres`. Never read exit 2 as "clean".
- **The data dump's circular-foreign-key warnings.** Expected. They are why
  the reload needs a superuser and `--disable-triggers`.
- **Step 6 count diff in a seed table.** The live database held a lookup row
  the DDL's seed differs on, or fewer. Compare the two rows before swapping.
- **A difference only in enum values.** Closed vocabularies come from the
  registry (`schema/gen_enums.py`, DR-0078); a new value is a registry
  change that already went through a Decision Record. The reload carries
  data as text, so existing rows are unaffected.
- **You cannot tell whether a difference matters.** Stop and ask the
  founder, with the step 1 output. A reload that was unnecessary costs an
  evening; one that was wrong costs a record.
