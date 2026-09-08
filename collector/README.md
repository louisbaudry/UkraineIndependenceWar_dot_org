# Collection pipeline

Implements SPEC-0003: discovery, acquisition, quarantine and Gate 1.

```bash
PGHOST=… PGPORT=… PGUSER=… python3 collector/tests/test_pipeline.py
```

## What is verified, and what is not

**Read this before treating collection as working.**

The pipeline below the network — quarantine, the security check, Gate 1,
retention-tier handling, OCFL writing, canonical-store rows, preservation
events and coverage accounting — is exercised end to end by 29 tests against
a real PostgreSQL database and real OCFL storage. Only the fetch is
substituted.

**`HttpFetcher` has completed live fetches once, in a rehearsal, and no
real source has been collected.** On 2026-09-08 it fetched the EU
Consolidated Financial Sanctions List (XML and CSV) and three OFAC exports
(up to 127 MB, through a 302 to a presigned S3 URL) into a throwaway
database and storage root, byte-identical to independent `curl` downloads,
with the whole pipeline below it behaving as it does on fixtures. The
record is
[docs/sources/verification-eu-consolidated-list-ofac-sdn.md](../docs/sources/verification-eu-consolidated-list-ofac-sdn.md).
Everything from that rehearsal was destroyed; the project's archive is still
empty, because no source is registered and the founder has not authorised a
run ([DR-0087](../docs/decision-records/DR-0087-first-source-registrations.md), proposed).

What the rehearsal did **not** exercise: behaviour under a slow or
rate-limiting origin, conditional requests (none are made — an unchanged
file is fetched and stored again), and the security check (the stand-in
scanner ran, and recorded that it ran). It also showed three gaps in the
pipeline itself: successive captures of one locator are not linked through
`capture_series_member` (DR-0074); the response headers a publisher
sends — `Last-Modified`, `ETag`, filenames, OFAC's publication metadata —
are received by the fetcher and then discarded by the acquisition record;
and quarantine copies are never removed after Gate 1 admits them, so the
archive directory holds every capture twice.

This is the reason the fetch layer is the only place that touches the
network. The seam is not for testing convenience; it is so the untested part
is one small, replaceable class rather than a property of the whole pipeline.

## Running a collection

```bash
python3 collector/run.py --source ofac-sdn --dbname uiw \
        --agent <pipeline_agent uuid> --archive-root ~/uiw-archive [--dry-run]
```

`run.py` is the operator's entry point to `Collector.run()`. It takes the
locators from the candidate entry's `run_locators` in `sources/candidates/`
and refuses to proceed if the candidate is not registered (DR-0071(a)), has
no verified run locators, is paused (DR-0067), if the agent is not a
registered person (DR-0087 §3; `--allow-software-agent` exists for the day
automation is decided), or if the archive root is a non-empty directory that
is not an OCFL root. `--dry-run` performs every check and nothing else. The
invocation — candidate key, locators, verification date, User-Agent, code
commit — is recorded in the run's configuration (DR-0070), and a run with
failed acquisitions exits 1 after recording them (PRES-007).

18 tests in `collector/tests/test_run.py`. The registration refusal and the
person-agent refusal were each removed in turn and the suite was seen to
fail. The full sequence was also rehearsed live against both approved
sources in a throwaway database on 2026-09-08 (verification record §7).

## The three gates

Only **Gate 1** is automated, and that is the design (DR-0066).

| Gate | What it decides | Here |
|---|---|---|
| **1 — Preservation** | Does this become an archival object, at what tier? | Automated: security check, retention tier, then admission |
| **2 — Editorial acceptance** | Does anything from it become canonical knowledge? | **Not automated.** Requires a human at the applicable risk tier (§78, DR-0063) |
| **3 — Publication** | Does it reach a public surface, at what access tier? | **Not automated.** |

A test asserts that a completed collection run creates **zero** documentary
assertions and **zero** evidence relations. Material that is permanently
preserved and never crosses Gate 2 is not an edge case — it is the normal
outcome of bulk collection (Principle 5).

## Policy enforcement

- **DR-0071(a)** — collection from unregistered sources is refused outright,
  by `run.py` before any fetch and by `Collector.run()` again underneath it.
  Until POL-0001 §10's legal review is recorded, only registered sources with
  human-configured scope may be collected. An unregistered locator is not
  merely unknown; it is out of policy, and the code says so.
- **DR-0067** — a paused or retired source does not collect.
- **DR-0068** — `discard` and `metadata-only` tiers record the acquisition
  and store no bytes.
- **SEC-002 / DR-0069** — material failing the security check is refused at
  Gate 1; the database also refuses admission without a clean check, so the
  rule holds even if the collector is wrong.

## Two systems, one order

A holding row and its OCFL object live in different systems and cannot share
a transaction. The order is deliberate:

1. Write the OCFL object (idempotent by content).
2. Write the database rows.

If step 2 fails, an unreferenced OCFL object remains — harmless, and found by
`find_orphaned_objects()`. The reverse order would leave a holding pointing
at bytes that do not exist, which is worse: the archive would claim to hold
something it does not (§26). A test simulates the failed transaction and
confirms the orphan is detectable.

## The security scanner is a stand-in

`_default_scan` recognises a test marker and otherwise returns `clean`. It is
**not** a malware scanner. It exists so that the gate cannot be bypassed by
the check being absent, and so an outcome is always recorded. A deployment
substitutes a real scanner through the `scanner` argument; the gate logic
does not change.

## Tests

29 tests, each naming the requirement or Decision Record it verifies.
Verified to fail honestly:

- bypassing the security check turns `SEC-002` red, along with the coverage
  counts that no longer add up;
- making collection create an assertion automatically turns
  `DR-0066 — collection creates no canonical knowledge by itself` red.
