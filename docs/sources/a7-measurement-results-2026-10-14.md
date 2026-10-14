# Storage and bandwidth measurement results — WP 3.4 Track A item A7, step 1 (baseline)

**Status:** Measurement record. Like
[`verification-eu-consolidated-list-ofac-sdn.md`](verification-eu-consolidated-list-ofac-sdn.md),
this states what was measured and how — it registers nothing, collects
nothing, and enacts no policy. Not a Decision Record. Counts and sizes only;
no row, hostname or address is quoted (public repository).
**Runbook followed:**
[`docs/runbooks/A7-storage-bandwidth-measurement.md`](../runbooks/A7-storage-bandwidth-measurement.md),
step 1 only, as part of the sitting in
[`archive-server-sitting.md`](../runbooks/archive-server-sitting.md) step 3.
**Step 2 (the retrospective pull, issue #55) was not done.**
**Measured:** 2026-10-14, on the archive server.
**Operator:** the founder, with an AI assistant dictating the commands; the
output below was pasted back from the founder's terminal.
**Environment:** database `uiw` (PostgreSQL 15), archive root `~/uiw-archive`,
`storage/measure.py` run read-only. The `storage/measure.py` commit on the
server and the result of its own test suite on the server were **not
recorded**; the suite passed (11/11) where it was written.

The full text report and the `--json` form stay on the archive server as the
operator's copy (`~/uiw-backups/a7-baseline-2026-10-14.*`); the figures below
are the ones the founder pasted back.

## 1. Per source (`collector_run`, recorded at collection time)

The runbook was written for two sources. Ten are registered and collected, so
the baseline covers all ten.

| Source | Runs | Items | Bytes preserved | Avg. throughput (B/s) |
|---|---|---|---|---|
| Air Force Command (Telegram) | 3,960 | 3,960 | 476,185,141 | 24,174,555 |
| General Staff (Telegram) | 1,973 | 1,973 | 202,003,396 | 19,382,962 |
| OFAC SDN list | 1 | 3 | 160,398,618 | 7,826,591 |
| UK OFSI consolidated list | 1 | 2 | 70,739,812 | 5,747,235 |
| EU consolidated list | 1 | 2 | 50,932,812 | 3,199,693 |
| SECO sanctions list | 1 | 1 | 42,300,406 | 1,932,164 |
| EUR-Lex restrictive measures | 3 | 4 | 32,398,966 | 2,382,673 |
| Prosecutor General criminal-offence report | 1 | 21 | 9,524,697 | 304,890 |
| UN HRMMU civilians-in-conflict update | 1 | 3 | 8,651,549 | 5,222,943 |
| BIS Entity List and Denied Persons List | 1 | 1 | 110,427 | 350,654 |
| **Total** | **5,943** | **5,970** | **1,053,245,824** | |

Two readings the table cannot show by itself:

- The two Telegram channels are 64% of the bytes and 99% of the items. Both
  have one run per item (backfilled by 2026-09-24), so "runs" there counts
  messages, not scheduled passes. The tool does not say what a Telegram
  throughput figure is the rate of; read it as the tool's output, not as a
  network speed.
- The sanctions and statistical files are few, large and fetched once; their
  throughput (0.3–7.8 MB/s) is the figure that applies to a scheduled
  re-collection, not the Telegram one.

## 2. On-disk footprint

| | On-disk bytes | Files |
|---|---|---|
| `permanent` root | 1,066,895,304 | 35,823 |
| `medium-term` root | 466 | 3 |
| `quarantine/` | 1,053,245,824 | 5,970 |

**Duplication ratio (on-disk ÷ preserved), as printed by the tool:** 2.01×.

The permanent root holds 13,649,480 bytes more than `collector_run` records
(1.3%): OCFL's own inventories and version directories (derived here by
subtraction; the tool does not report it separately).

### Why the ratio is 2.01× and what it does not yet show

Quarantine holds exactly the bytes `collector_run` records, in exactly as many
files as there are items (5,970): **every item ever collected still has its
quarantine copy.** That is the known gap documented in `collector/README.md`.
The discharge-after-admission fix (issue #51) landed on 2026-10-02; every run
in this table predates it (the latest registered source, the Prosecutor
General's, dates from 2026-09-29). So this measurement is the pre-fix baseline and shows nothing
about whether the discharge works on the real server. **That is still to be
seen at the first real collection run after 2026-10-02**, when the quarantine
file count should stop growing with the item count.

Removing the existing 5,970 copies is a separate, one-off act that
`collector/README.md` says needs verification against the real OCFL objects
first, by a person. At 1.05 GB with about 108 GB free it is not urgent.

## 3. What this gives WP 3.4 §5.3

- **Storage:** 1.05 GB preserved for ten sources over five weeks; 1.07 GB in
  the permanent root (OCFL overhead 1.3%). At today's rate the Telegram
  channels dominate, one full collection of the six sanctions lists is
  about 0.36 GB (sum of the six rows above), and the civilian-harm sources are small.
- **Sizing multiplier:** until the discharge is seen to work, size disk at
  2× preserved bytes; after it, about 1.01×.
- **Bandwidth:** single-file government downloads ran at 0.3–7.8 MB/s from
  the server (a live-fetch figure only; the second, independent figure from a
  retrospective pull is step 2, not measured).
- Not extrapolated to the other candidate sources; `measure.py --extrapolate`
  exists for that and labels a projection as one.

## 4. What was not measured

- **Step 2, the retrospective pull** (#55): no WARC recovered from an external
  archive, so no second throughput figure and no live-fetch/retrospective
  comparison.
- **Database disk usage** (as opposed to OCFL and quarantine).
- **Backup cost**, the OPS-005 independent-backup requirement §5.3 also lists
  as unknown. The reload of 2026-10-13 produced 13 MB and 26 MB dumps; that is
  the database only, not the archive tree.
- **Concurrent sources under load**; every run here was sequential.
- **Whether the quarantine discharge works in production** (§2 above).
