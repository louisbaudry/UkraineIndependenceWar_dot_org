# Release baselines

Implements DR-0048: a release is a **named, frozen baseline** over versioned
configuration items — not a tagged commit.

```bash
python3 release/baseline.py --check --dbname uiw --dump path/to/dump
```

## Why a baseline rather than a version number

DR-0047 established that the project has no single version: code, schema,
registry, data, methodology and terminology each version differently, on
different regimes, for different reasons. A release is therefore the act of
**pinning one of each and attesting to the result** — which is what makes
§86's question answerable: *what exactly did we say about X, on date Z, and
on what evidence and methodology?*

## Creation fails closed

A baseline missing any configuration item is not created. A release whose
reproducibility depends on an unrecorded version is not reproducible
(Principle 16), so the honest response is refusal rather than a partial
record.

`--check` reports readiness without creating anything. It is the useful
thing to run long before a first release is possible, because it names what
the project still lacks.

### What it currently reports

```
  MISSING  code_commit            ← working tree not clean
  pinned   schema_version         sha256:650829529fd8ec0a
  pinned   registry_version       0.1.1
  MISSING  collector_version      ← no collector has run
  MISSING  pipeline_version
  pinned   methodology_version    1.0
  pinned   terminology_version    registry:0.1.1
  pinned   build_configuration    …
  MISSING  dataset_snapshot       ← no preservation dump supplied
```

`methodology_version` was the substantive gap, and this tool is how it
surfaced: §97 makes methodology a first-class versioned artifact and DR-0047
requires releases to pin it, but no METH document had been written.
[METH-0001](../docs/methodology/METH-0001-evidentiary-method.md) was drafted
in response and approved as v1.0 on 2026-08-26 (DR-0085); the item now pins.

While it was a candidate the check went on refusing it, which was the point:
**a draft carries no authority** (DR-0046), so pinning one would claim a
release rests on a document nobody has approved. The status logic that
enforces this is tested against fixtures for all four document statuses,
rather than against METH-0001's own header — an assertion about the live
document would have meant the opposite of itself the moment it was approved.

The remaining gaps need a real collection run, not a document:
`collector_version` and `pipeline_version` come from software agents that
have actually executed, and `dataset_snapshot` from a preservation dump of
the resulting archive.

One branch is currently unexercised: the note distinguishing "no METH
document exists at all" from "one exists but is not approved" is only
reachable while no effective METH document is present, which is no longer the
case. The status logic it depends on is covered; the wording of that one note
is not.

## What a baseline contains

| File | Contents |
|---|---|
| `baseline.json` | Pinned configuration, storage state, licensing, known limitations, the dataset snapshot's own manifest |
| `baseline.json.sha256` | Sidecar attesting to the manifest |
| `coverage.json` | Per-source coverage: discovered, acquired, skipped, failed, outages (§57, OPS-006) |
| `change-sets.json` | Merged, split, disproved, retracted and superseded mappings (§91, OPS-003) |
| `CHANGELOG.md` | What changed since the last baseline |

## Design notes

**A filtered dump is not an archive snapshot.** Only a preservation dump can
be pinned (SPEC-0006 §9A); a disclosure dump is deliberately incomplete, and
pinning one would make the release claim to be the archive when it is not.

**Known limitations are stated, not discovered.** The field exists because a
release that omits what it cannot do misleads whoever relies on it. The first
baseline's limitations would include that `HttpFetcher` has never completed a
live fetch and that OCFL conformance rests on the project's own validator.

**Change sets ship even when empty.** An empty `merged` list tells a consumer
that nothing merged; its absence would leave them guessing (OPS-003).

**Baselines are frozen.** Writing into a non-empty baseline directory is
refused. Corrections are new baselines, in keeping with the append-only
discipline everywhere else (DR-0055).

**An unclean working tree blocks the code commit.** A baseline pinned to a
commit that does not describe what was actually built is worse than no
baseline, because it looks reproducible.

## Tests

27, each naming the requirement it verifies — including that creation is
refused for each missing configuration item individually, that a disclosure
dump cannot be pinned as the snapshot, that coverage records failures rather
than only successes, that a controlled document pins only when Approved —
Effective (checked across all four statuses), and that tampering with a
released file is detected.
