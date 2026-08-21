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

## Tests

29 tests, each naming the requirement or Decision Record it verifies.
Verified to fail honestly:

- bypassing the security check turns `SEC-002` red, along with the coverage
  counts that no longer add up;
- making collection create an assertion automatically turns
  `DR-0066 — collection creates no canonical knowledge by itself` red.
