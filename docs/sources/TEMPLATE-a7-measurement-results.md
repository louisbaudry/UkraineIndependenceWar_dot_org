# Storage and bandwidth measurement results — WP 3.4 Track A item A7

> **This file is a template.** Copy it to
> `docs/sources/a7-measurement-results-YYYY-MM-DD.md`, fill in every `[ ]`
> blank from real command output (never by hand-calculation — quote
> `storage/measure.py`'s own numbers), delete this notice and the *How to
> use this template* section, and delete any bracketed sentence you did not
> need. Leave nothing bracketed in the deposited copy.

**Status:** Measurement record. Like
[`verification-eu-consolidated-list-ofac-sdn.md`](verification-eu-consolidated-list-ofac-sdn.md),
this states what was measured and how — it registers nothing, collects
nothing new beyond what the runbook's step 2 already did, and enacts no
policy. Not a Decision Record; nothing here needs founder approval to
exist, only to be trusted.
**Runbook followed:**
[`docs/runbooks/A7-storage-bandwidth-measurement.md`](../runbooks/A7-storage-bandwidth-measurement.md).
**Measured:** `[ YYYY-MM-DD, HH:MM–HH:MM UTC ]`, on the archive server.
**Operator:** `[ name / role, or "the founder" ]`.
**Environment:** database `[ uiw ]`, archive root `[ ~/uiw-archive ]`,
`storage/measure.py` at commit `[ git rev-parse HEAD, run on the archive
server ]`.

---

## 0. Pre-check

Confirm the tool's own suite passed in this environment before trusting
its output below (runbook, *Before starting*):

```
[ paste the last line of: python3 storage/tests/test_measure.py ]
```

`[ 11 passed, 0 failed ]` expected. If it did not read that, stop and say
so instead of continuing — see the runbook's *If something looks wrong*.

## 1. Baseline — the two A1 sources (runbook step 1)

```
[ paste the full text output of:
  python3 storage/measure.py --dbname uiw --archive-root ~/uiw-archive ]
```

| Source | Runs | Items acquired | Bytes preserved | Avg. throughput |
|---|---|---|---|---|
| `eu-consolidated-list` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |
| `ofac-sdn` | `[ ]` | `[ ]` | `[ ]` | `[ ]` |

| | On-disk bytes | Files |
|---|---|---|
| `permanent` root | `[ ]` | `[ ]` |
| `medium-term` root | `[ ]` | `[ ]` |
| `quarantine/` | `[ ]` | `[ ]` |

**Total bytes preserved (collector_run sum):** `[ ]`
**Duplication ratio (on-disk ÷ preserved):** `[ ]`×
`[ if far from ~2×, say what was checked per the runbook's "If something
looks wrong" and what was found ]`

The JSON form was also saved for the record:
`[ path to the saved --json output, e.g. /tmp/a7-baseline-YYYY-MM-DD.json,
or "attached to this note" if committed alongside it ]`

## 2. Retrospective pull (runbook step 2)

**Archive used:** `[ Common Crawl | Internet Archive Wayback Machine |
other, name it ]`, reached from `[ the archive server directly | a
workstation with the file transferred over, name how ]`.
`[ If Wayback was used instead of the runbook's default Common Crawl path,
say what made it necessary and how the WARC record was actually obtained
— the runbook does not script that path. ]`

**Source pulled:** `[ eu-consolidated-list | ofac-sdn ]`, locator
`[ the exact URL from sources/candidates/sanctions-authorities.yaml's
run_locators, as pulled ]`.
**Capture identified:** crawl/index `[ e.g. CC-MAIN-2025-XX ]`, captured at
`[ timestamp from the CDX/index record ]`.

### 2a. The fetch (bandwidth)

```
[ paste /tmp/a7-pull-fetch-timing.txt or equivalent timing output ]
```

| | |
|---|---|
| WARC record size | `[ ]` bytes |
| Wall-clock time | `[ ]` seconds |
| Throughput | `[ ]` bytes/second |

### 2b. The ingest (storage)

```
[ paste the ingest script's run id line and the psql confirmation query
  output from the runbook's step 2d ]
```

```
[ paste: python3 storage/measure.py --dbname uiw --archive-root
  ~/uiw-archive --source-id "$SOURCE_ID" — run AFTER the ingest, so it
  reflects both this source's live-fetch run (step 1) and this
  retrospective-pull run together ]
```

| | Live fetch (step 1, this source) | Retrospective pull (this step) |
|---|---|---|
| Bytes preserved | `[ ]` | `[ ]` |
| Items acquired | `[ ]` | `[ ]` |
| Acquisition route | `live-fetch` | `external-archive` |

`[ one or two sentences comparing the two — same locator, same bytes if
the source has not changed since the live fetch, or a note on why they
differ (revisit record, publisher update, etc.) ]`

## 3. What this changes in WP 3.4 §5.3

`[ Quote or paraphrase the real numbers this measurement gives §5.3 to
cite in place of "unknown until A7 measures them" — the total bytes for
two sources' worth of collection, the observed duplication overhead as a
storage-sizing multiplier, and the retrospective-pull bandwidth as a
second, independent throughput figure alongside the live-fetch one. Do
not extrapolate to the other five sanctions candidates here unless asked
— storage/measure.py's --extrapolate flag exists for that and labels it
as a projection, not a fifth measured number. ]`

## 4. What was not measured

`[ Say plainly what this pass did not cover — e.g. no run under load from
multiple concurrent sources, no measurement of database (as opposed to
OCFL/quarantine) disk usage, no backup-copy cost (record §7's OPS-005
independent-backup requirement, which WP 3.4 §5.3 also lists as unknown).
This section exists so nobody mistakes "A7 measured" for "A7 measured
everything §5.3 asked about." ]`

---

## How to use this template

1. Copy this file to `docs/sources/a7-measurement-results-YYYY-MM-DD.md`.
2. Run the runbook's steps, filling in each blank as you go rather than
   reconstructing output afterward from memory.
3. Delete this section and the "This file is a template" notice at the
   top before committing.
4. Update WP 3.4 §5.3
   (`docs/phase-3/working-papers/wp-3.4-foundational-corpus-acquisition.md`)
   to cite the real numbers, per the working-paper correction convention in
   `CLAUDE.md` (keep the original SHA-256 in `PROVENANCE.md`, add the new
   one with the reason).
5. Update `CLAUDE.md`'s Track A table (A7 row → **done**) and `README.md`'s
   "Open decisions" section, the same way A2's completion was recorded.
