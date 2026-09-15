# Runbook — WP 3.4 Track A item A7 (storage and bandwidth measurement)

**Status:** Operator runbook, not a Decision Record and not a controlled
document under DR-0046. It proposes no policy and enacts nothing; it is
instructions for running tooling that already exists and is already
authorised, on the archive server, and writing down what comes back.
**Author:** AI assistant (Anthropic Claude Code agent session), at the
founder's direction, 2026-09-15. Nothing in this runbook has been executed
— see `storage/README.md` for what was and was not verified when the
tooling it calls was built.

## What this is for

WP 3.4 §5.3: *"Storage volume, bandwidth, and backup dominate and are
unknown until A7 measures them. The plan sizes storage after the first
retrospective pull, not before."* A7's own row (WP 3.4 §4.1) names two
things to measure:

1. storage and bandwidth **on the A1 sources** — the two already collected
   (`eu-consolidated-list`, `ofac-sdn`, DR-0093, 2026-09-09);
2. storage and bandwidth **on one retrospective pull for a registered
   domain** — a recovery via `Collector.ingest_warc` (WP 3.4 §4,
   CDR-P3-35, candidate), which neither A1 run exercised: both were
   live fetches (`acquisition_route = 'live-fetch'`), not recoveries from
   an external archive.

`storage/measure.py` (built and tested 2026-09-15, `storage/README.md`)
does the measuring for both. This runbook is what to run, in what order,
and what to do with the numbers — it does not re-explain the tool itself.

## Before starting

- Run on the archive server, in the same `uiw` database and
  `~/uiw-archive` archive root every prior registration and run used
  (DR-0093, `DR-0096`,
  `DR-0098`), unless the install used
  different names — check `setup/install.sh` and prior session notes if so.
- `git pull` this branch (or `main`, once merged) so `storage/measure.py`
  and its tests are present.
- Confirm the suite still passes in this environment before trusting its
  output here — an environment difference is worth catching before it
  produces a wrong number, not after:

  ```bash
  export PGHOST=… PGPORT=… PGUSER=…
  python3 storage/tests/test_measure.py   # expect: 11 passed, 0 failed
  ```
- Have the person `pipeline_agent` id from DR-0093's step 1 (or another
  person's id, if a different founder-authorised operator is running this).
  Nothing here needs a new registration — both sources used are already
  registered and active.

## Step 1 — baseline: measure what is already there

No new collection. Reads `collector_run` and walks the existing archive
root. Safe to run at any time, as often as wanted.

```bash
python3 storage/measure.py --dbname uiw --archive-root ~/uiw-archive --json \
    > /tmp/a7-baseline-$(date +%F).json
python3 storage/measure.py --dbname uiw --archive-root ~/uiw-archive
```

Read the text output for:

- **per-source bytes preserved and throughput** for `eu-consolidated-list`
  and `ofac-sdn` — WP 3.4 §5.3's bandwidth figure for the A1 sources;
- **on-disk footprint** for each tier root and for `quarantine/` —
  WP 3.4 §5.3's storage figure;
- **duplication ratio** — expected close to **2×**, since
  `collector/README.md` records that quarantine copies are never removed
  after Gate 1 admits them (an open gap, not a bug in the tool). A ratio
  far from 2× is worth a second look before trusting the rest of the
  numbers — see *If something looks wrong*, below.

This step alone already answers most of what A7 asks for on the two A1
sources. Record the output (see *Recording the results*) even if step 2
is deferred.

## Step 2 — one retrospective pull for a registered domain

This is new acquisition, not measurement, so it needs the same care as any
other collector run: `--dry-run` first, a person as agent of record
(DR-0093 §3), and it is a separate act from steps 1 and 3, done at
whatever pace the operator wants — nothing here requires it to happen in
the same sitting as step 1.

`collector/run.py` only performs live fetches. There is no CLI for
`Collector.ingest_warc` (WARC recovery from an external archive,
WP 3.4 §4 / CDR-P3-35), so this step is a short script rather than one
command. Recommended target: one of the two A1 sources
(`eu-consolidated-list` or `ofac-sdn`) — already registered, already
verified, and using a source this project already holds a live capture of
means the retrospective pull is directly comparable to it, which is the
point of measuring both.

### 2a. Check reachability before relying on a plan

CLAUDE.md's environment notes record that `web.archive.org` was
**unreachable** from the session that wrote most of this repository, and
untested from the archive server itself. Check both candidate archives
before choosing:

```bash
curl -sI --max-time 20 -A "$(python3 -c "import sys; sys.path.insert(0,'collector'); from run import DEFAULT_USER_AGENT as u; print(u)")" \
    https://index.commoncrawl.org/collinfo.json
curl -sI --max-time 20 https://web.archive.org/web/2024/https://webgate.ec.europa.eu/
```

Use whichever responds. The rest of this section assumes **Common
Crawl**, since its index server returns the byte `offset`/`length` needed
to fetch one exact response record without downloading a whole crawl
segment (tens of gigabytes) — the Wayback Machine's public API does not
expose an equivalent WARC-record fetch, so recovering a byte-identical
WARC record from it needs more improvisation than this runbook covers. If
only Wayback is reachable, treat that as a finding to report (see *If
something looks wrong*) rather than a reason to guess at a workaround.

### 2b. Find a capture and fetch its exact WARC record

```bash
# Pick the crawl id from https://index.commoncrawl.org/collinfo.json
CRAWL=CC-MAIN-2025-XX   # substitute the latest listed there
LOCATOR="<the source's run_locator from sources/candidates/sanctions-authorities.yaml>"

curl -s "https://index.commoncrawl.org/${CRAWL}-index?url=$(python3 -c 'import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=""))' "$LOCATOR")&output=json" \
    | tail -1 > /tmp/cc-record.json
cat /tmp/cc-record.json   # inspect: filename, offset, length, status, timestamp

python3 - <<'PY'
import json
rec = json.load(open("/tmp/cc-record.json"))
print(rec["filename"], rec["offset"], rec["length"])
PY

# Byte-range fetch of exactly that record (not the whole segment file):
OFFSET=<from above>; LENGTH=<from above>; FILENAME=<from above>
curl -s -o /tmp/retrospective-pull.warc.gz \
    -r "${OFFSET}-$((OFFSET+LENGTH-1))" \
    "https://data.commoncrawl.org/${FILENAME}"
gunzip -k /tmp/retrospective-pull.warc.gz   # storage/warc.py reads uncompressed WARC
```

**Time and size this fetch explicitly** — it is the bandwidth half of this
step, and it is not recorded anywhere `storage/measure.py` reads, because
it happens before anything touches the database:

```bash
/usr/bin/time -v curl -o /tmp/retrospective-pull.warc.gz \
    -r "${OFFSET}-$((OFFSET+LENGTH-1))" \
    "https://data.commoncrawl.org/${FILENAME}" 2>&1 | tee /tmp/a7-pull-fetch-timing.txt
```

### 2c. Dry-run, then ingest

There is no `--dry-run` flag on `ingest_warc` itself (unlike
`collector/run.py`), so dry-run it by hand: confirm the source resolves,
inspect the WARC's records, and only then call `ingest_warc` for real.

```python
#!/usr/bin/env python3
# save as e.g. /tmp/a7-retrospective-pull.py and edit the four values below
import sys
from pathlib import Path

sys.path.insert(0, "collector")
sys.path.insert(0, "storage")
sys.path.insert(0, "sources")

import psycopg
from ocfl import StorageRoot
from pipeline import Collector, ensure_software_agent
from warc import iter_warc_records

SOURCE_ID = "<uuid from: select id from source where name = '...'>"
AGENT_ID = "<the person pipeline_agent id, same as collector/run.py --agent>"
ARCHIVE_ROOT = Path.home() / "uiw-archive"
WARC_PATH = Path("/tmp/retrospective-pull.warc.gz")  # or the ungzipped .warc

conn = psycopg.connect(dbname="uiw", autocommit=True)

# Inspect first -- this is the dry-run: no database write happens until
# collector.ingest_warc() is actually called below.
for record in iter_warc_records(WARC_PATH):
    if record.is_http_response:
        print(record.target_uri, record.record_type)

roots = {
    "permanent": StorageRoot(ARCHIVE_ROOT / "permanent", "permanent"),
    "medium-term": StorageRoot(ARCHIVE_ROOT / "medium-term", "medium-term"),
}
software_agent_id = ensure_software_agent(conn)
collector = Collector(
    conn, fetcher=None, quarantine_dir=ARCHIVE_ROOT / "quarantine",
    roots=roots, agent_id=AGENT_ID, software_agent_id=software_agent_id,
)

run_id = collector.ingest_warc(
    SOURCE_ID, WARC_PATH,
    acquisition_source="Common Crawl",   # or "Internet Archive Wayback Machine"
    configuration={
        "invoked_by": "docs/runbooks/A7-storage-bandwidth-measurement.md",
        "warc_source_crawl": "CC-MAIN-2025-XX",
    },
)
print("run", run_id)
```

Read the printed target URIs before trusting the run — confirm at least
one is the registered source's own locator (in scope; `ingest_warc` skips
and does not store anything out of scope, but seeing that happen on
purpose is better than assuming it). Then run it.

```bash
python3 /tmp/a7-retrospective-pull.py
```

### 2d. Confirm and re-measure

```bash
psql -d uiw -c "SELECT id, source_id, bytes_preserved, items_acquired, \
    configuration->>'acquisition_route' FROM collector_run \
    ORDER BY started_at DESC LIMIT 1"

python3 storage/measure.py --dbname uiw --archive-root ~/uiw-archive \
    --source-id "$SOURCE_ID"
```

Compare this run's `bytes_preserved` and on-disk footprint against the
same source's live-fetch run from step 1 — same locator, two acquisition
routes, is exactly the comparison WP 3.4 §5.3 wants.

## Recording the results

This produces data, not a decision, so it does not need a Decision
Record. Deposit it as a short prose note under `docs/sources/` (same
directory as `verification-eu-consolidated-list-ofac-sdn.md`), naming:

- date, operator, database/archive-root used;
- step 1's numbers (per-source bytes/throughput, on-disk footprint,
  duplication ratio) — quote `storage/measure.py`'s own output rather than
  re-deriving numbers by hand;
- step 2's numbers, and the WARC-fetch timing from `/tmp/a7-pull-fetch-timing.txt`;
- which archive (Common Crawl or Wayback) was actually reachable and used.

[`docs/sources/TEMPLATE-a7-measurement-results.md`](../sources/TEMPLATE-a7-measurement-results.md)
is a fill-in-the-blanks copy of exactly this shape — copy it to
`docs/sources/a7-measurement-results-YYYY-MM-DD.md` and fill it in as each
step's output comes back, rather than reconstructing numbers from memory
afterward.

Then update WP 3.4 §5.3 to cite the real numbers instead of "unknown until
A7 measures them" (a **working-paper edit**, not a new version unless the
founder wants one — see `docs/phase-3/README.md`'s PROVENANCE.md
convention if it is re-deposited), and update this repository's
`CLAUDE.md` Track A table and `README.md` "Open decisions" section the
same way A2's completion was recorded, marking A7 **done** rather than
**in progress**.

## If something looks wrong

- **Duplication ratio far from ~2×**: could mean quarantine was already
  partly cleaned up (a change worth knowing about) or that
  `--archive-root` pointed somewhere other than what `collector_run.py`
  actually wrote to. Check `psql -d uiw -c "SELECT ocfl_object_id FROM
  holding LIMIT 5"` against `find storage-root -name inventory.json` by
  hand before trusting the number.
- **Neither Common Crawl nor Wayback reachable from the archive server**:
  record that as a finding (it changes what "retrospective pull" can mean
  in practice — WP 3.4's third acquisition mode may need a different
  index or a manually deposited WARC) rather than skipping step 2 silently.
- **`ingest_warc` finds nothing in scope**: the WARC record's
  `target_uri` did not match the source's registered `locator` under
  `in_scope()` (collector/pipeline.py). Check the locator recorded in
  `sources/candidates/sanctions-authorities.yaml` against what the CDX
  record's `url` field actually says — sanctions-list publishers rotate
  URLs (see `docs/sources/verification-seco-sanctions.md`'s own
  wrong-host story) more often than instrument publishers do.
