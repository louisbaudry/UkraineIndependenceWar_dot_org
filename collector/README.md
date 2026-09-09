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

**`HttpFetcher` has never completed a live fetch.** The build environment's
network policy denies general internet hosts — EUR-Lex, for instance, is
refused at the proxy with a policy 403 — so no real source has been
collected. The class is written to the same standard as the rest and is
structurally simple, but *nothing has confirmed it works against a real
server*: not its redirect handling, not its encoding behaviour, not its
timeout semantics under a slow origin, not conditional requests, not how a
real site's rate limiting responds to it.

Before anyone claims the project collects: run it against a live source in
an environment with network access, and expect to find something.

This is the reason the fetch layer is the only place that touches the
network. The seam is not for testing convenience; it is so the untested part
is one small, replaceable class rather than a property of the whole pipeline.

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

- **DR-0071(a)** — collection from unregistered sources is refused outright.
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

## The registry's capture format is honoured (DR-0006, DR-0067)

A source registered with `capture_format: warc` — as the EUR-Lex and NSDC
candidates in `sources/candidates/` are — now receives WARC. `_collect_one`
wraps a successful live response in a single WARC 1.1 response record
(`warc.build_response_record`): status line, headers and body together,
WARC-Date as the capture time, payload and block digests declared. The
record is what enters quarantine and, at Gate 1, the OCFL object as
`original.warc` with format `application/warc`. A source registered `http`
still stores the body alone as `original.bin` — the lighter form, recorded
as such (§26).

The wrapping happens above the network seam, so every fetcher's response is
wrapped by one rule, and the live and recovered paths produce byte-comparable
holdings: a page captured live today and the same page recovered from an
archive's 2015 crawl are two records in one capture series, read by one
reader.

Honest limits of wrapping what an HTTP client library delivered, rather than
the wire: chunked transfer-encoding has already been undone, so the
`Transfer-Encoding` header is dropped to keep the recorded message
self-consistent; the request is not recorded; redirect responses on the way
are not recorded (the final URL is the record's target). A WARC-native
capture tool for the high-value tier remains DR-0006's plan and the WACZ
evaluation is still owed; this is the honest interim form. A fetcher that
cannot report an HTTP status cannot serve a `warc` source: the attempt is
recorded as failed rather than wrapped with an invented status line.

## Retrospective recovery from WARC (WP 3.4 §4, CDR-P3-35 — **candidate**)

`Collector.ingest_warc(source_id, warc_path, acquisition_source, configuration)`
recovers a registered source's historical captures from a WARC file obtained
from an external web archive. It implements a **candidate** proposal; if the
founder amends CDR-P3-35, this path changes with it.

```python
collector.ingest_warc(source_id, "CC-MAIN-…-segment.warc.gz",
                      acquisition_source="Common Crawl CC-MAIN-2015-06",
                      configuration={"operator": "…"})
```

What it does, and why:

- **Same gate, same quarantine.** Each HTTP response record becomes an
  acquisition attempt, a quarantine item, a security check and a Gate 1
  decision exactly as a live fetch does — `_admit()` is shared. Nothing about
  recovery is a shortcut past DR-0069 or DR-0066.
- **Scope is enforced, and out-of-scope is not written down.** A WARC from an
  archive holds whatever the archive crawled. Only records under the
  registered source's locator (same host or subdomain, path prefix if any)
  are the source's; the rest are counted as `scope:outside-registered-source`
  and **no row records their URL** — DR-0071(a) means an unregistered locator
  is out of policy, not merely unknown. A source with no locator cannot be
  ingested for at all.
- **Acquisition source ≠ original publisher (§28).** `acquisition_attempt`
  now carries `acquisition_route` (`live-fetch` / `external-archive` /
  `manual-deposit`), the archive's name, **its** capture time
  (`original_captured_at`, from WARC-Date) distinct from `attempted_at`
  (when we obtained the record), the WARC-Record-ID, and the archive's
  declared payload digest. The schema refuses an external-archive attempt
  without archive name and capture time. Live fetches record `live-fetch`
  and nothing else.
- **The archive's digest is checked (DR-0075).** A declared
  WARC-Payload-Digest that does not match the payload held makes the
  acquisition a recorded `failure`, never a holding. A match is recorded as
  a `fixity-check` event on the quarantine item. Both as-transmitted and
  de-chunked bodies are accepted, since tools differ.
- **The complete record is what is preserved (DR-0006).** WARC headers, HTTP
  status line and headers, body — as `original.warc` in the OCFL object,
  format `application/warc`. The body alone is a derivative for
  normalization to produce later (SPEC-0003 §6). WARC files are ordinary
  content inside OCFL objects (WP 3.3 §8 Q5).
- **Capture series (DR-0074).** Every admitted capture — live or recovered —
  joins the series for its (source, locator), ordered by the capture time.
  Two archived captures of one page years apart are two holdings in one
  series; a live capture today joins the same series.
- **Archived failures are failures (PRES-007).** An archived 404 is a
  `not-found` attempt whose detail says when the archive saw it. A file that
  is truncated or malformed part-way stops the run there, keeps what was
  admitted, and records the fault in the run's `failure_details`.
- **Revisit records** (the archive saw the page unchanged) are counted as
  `warc:revisit` and not admitted. Whether they should become evidence of
  "unchanged at date" is WP 3.4 §9's open question, deliberately unresolved
  in code.

`collector/warc.py` is a standard-library reader for WARC 1.0/1.1, plain and
per-record gzip. It exists so the project's runtime dependencies stay what
`setup/install.sh` installs, and so the format a future archivist must read is
one a page of code reads.

**What is verified, and what is not.** The suite writes its own WARC files,
so every byte is known. Where `warcio` is importable in the test environment
(it is not a project dependency), the reader is cross-checked in both
directions: our reader reads a warcio-written record to the same URI,
payload and verified digest, and warcio reads our fixture to the same URIs
and payloads. **No file produced by Common Crawl or the Wayback Machine has
been parsed** — the build environment cannot reach them — and **obtaining
WARC files from an archive is not implemented**; `ingest_warc` reads a local
path. Expect the first real file to teach the reader something.

## Tests

Two suites, each test naming the requirement or Decision Record it verifies.

**`test_pipeline.py` — 40 tests** on the live path. Verified to fail honestly:

- bypassing the security check turns `SEC-002` red, along with the coverage
  counts that no longer add up;
- making collection create an assertion automatically turns
  `DR-0066 — collection creates no canonical knowledge by itself` red;
- ignoring the registry's capture format turns seven `DR-0006` checks red —
  the `warc` source gets a bare body.

**`test_warc_ingest.py` — 57 tests** on the WARC reader and writer and on
retrospective recovery, including the warcio cross-check in both directions
(reported as a skip when warcio is absent). Verified to fail honestly, by
sabotaging the pipeline one rule at a time and watching:

- removing the scope check admits the out-of-scope record and turns seven
  checks red, `DR-0071 — an out-of-scope URL appears nowhere in the store`
  among them;
- recording our own time instead of the archive's capture time turns the §28
  and DR-0074 ordering checks red;
- skipping digest verification turns the DR-0075 checks red — the corrupt
  record reaches the archive;
- preserving only the payload instead of the complete record turns the
  CDR-P3-35 checks red;
- keeping the undone `Transfer-Encoding` header in a wrapped record turns
  the writer's envelope check red.
