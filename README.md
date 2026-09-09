# Ukraine's Second War of Independence — Project Repository

A durable historical evidence and knowledge repository that happens to publish a website.

This project is a long-term historical, documentary, OSINT, preservation,
sanctions-evasion, export-control, and research infrastructure focused on Ukraine's
struggle for sovereignty and the broader machinery sustaining Russia's war. The working
historical framing — *Ukraine's Second War of Independence* — is an explicit interpretive
choice, distinguished from conventional terminology such as "Russo-Ukrainian War" or
"Russian invasion of Ukraine."

The project is independent and non-Ukrainian. It is explicitly supportive of Ukrainian
sovereignty and opposed to Russian imperial domination, while committing itself to
rigorous evidentiary standards, transparent methodology, and careful distinctions among
source claims, evidence, inference, legal findings, and project conclusions.

The time horizon is measured in years and potentially decades.

## Project status

| Phase | Status |
|---|---|
| Phase I — Requirements Discovery | **Complete** — see the [discovery record](docs/discovery/phase-1-requirements-discovery-record.md) |
| Phase II — Theoretical Synthesis & Standards Mapping | **Closed 2026-08-16** ([DR-0053](docs/decision-records/DR-0053-phase-2-closure.md)) — 7 workstreams, 53 Decision Records, all eight consolidation outputs approved ([docs/phase-2/outputs/](docs/phase-2/outputs/README.md)) |
| Phase III — Conceptual Architecture | **Open** — see [docs/phase-3/](docs/phase-3/README.md). All nine planned studies delivered; SPEC-0001…0006, POL-0001, METH-0001 and ten REQ documents effective; all three pipeline gates built. **Collection at scale is suspended pending external legal review** ([POL-0001 §10](docs/policies/POL-0001-personal-data.md), DR-0072). The founder ruled on 2026-09-08 that no collection scale-up precedes that review ([WP 3.4](docs/phase-3/working-papers/wp-3.4-foundational-corpus-acquisition.md), candidate) |

DR-0001…0086 are approved and in force. No permanent API contract or technical stack
beyond PostgreSQL, Python and OCFL has been frozen.

## Where things stand, plainly

**Governance and design are far ahead of collection.** The evidentiary method, the
data model, the registry, the three-gate pipeline, the storage layout and the
personal-data policy are all decided and documented. The code implements them and is
tested against a real database and real storage. But:

- **Nothing has been collected.** No source is registered. The seven sanctions
  authorities in [`sources/candidates/`](sources/README.md) are proposals awaiting the
  founder's per-source decision; registering is the act that authorises collection.
- **No live fetch has ever completed.** The build environments used so far cannot reach
  general internet hosts, so `HttpFetcher` has never been exercised against a real
  server, and no WARC file from Common Crawl or the Wayback Machine has ever been
  parsed. [`collector/README.md`](collector/README.md) says exactly what is and is not
  verified.
- **The external legal review required by POL-0001 §10 has not been commissioned.**
  Until it is recorded, collection is bound to explicitly registered sources with
  human-configured scope (DR-0071): no open-ended crawling, no bulk social harvesting,
  no automatic structuring of personal data.
- **Gate 2 and Gate 3 are human.** Bulk collection produces holdings and review queues,
  never canonical knowledge. That is the design (DR-0066, Principle 5), and it means the
  knowledge graph grows at the pace of editorial review.

## The acquisition strategy (candidate)

[WP 3.4](docs/phase-3/working-papers/wp-3.4-foundational-corpus-acquisition.md) proposes
how the foundational corpus is constituted: **not by crawling the general web**, before
or after the legal review, but by

1. a **source census** producing registry entries for the founder to accept or reject;
2. **retrospective recovery** of registered sources from existing web archives, which
   is the only route to the pre-2026 web; and
3. **registered live collection**, daily, through the pipeline.

Its Track A (permitted now under DR-0071) is under way: the WARC recovery path and the
live WARC wrapping are built and tested. Its Track B waits on the recorded review. Five
candidate Decision Records (CDR-P3-31…35) await the founder.

## Repository layout

```
docs/
  discovery/          Phase I requirements-discovery record (immutable source
                      material) + acquisition provenance
  decision-records/   Unified Decision Record system (record §98); DR-0001…0086
                      approved and in force; register in its README
  phase-2/            Phase II (closed) — working papers WP 0.1–0.8 + provenance,
                      approved consolidation outputs
  phase-3/            Phase III working area
    working-papers/   WP 3.1–3.4 + PROVENANCE.md (SHA-256 at deposit)
  specifications/     SPEC-class controlled documents (DR-0046)
  policies/           POL-class controlled documents (DR-0046)
  requirements/       REQ-class controlled documents (DR-0046/0051)
  methodology/        METH-class controlled documents (DR-0046, record §97)
  sources/            Informal prose notes on possible sources, written before
                      any registration is drafted (distinct from sources/ below)

registry/             Semantic registry: vocabularies, argument schemes, compiler;
                      the source of truth for every enumeration (DR-0078)
sources/              DR-0067 source registry — candidate registrations and the
                      register.py tool; registering authorises collection
schema/               Canonical store DDL (PostgreSQL); enums generated from the
                      registry; schema test suite
storage/              OCFL archival storage roots and fixity scheduling
collector/            Gate 1 — acquisition (live fetch and WARC recovery),
                      quarantine, preservation; the stdlib WARC reader/writer
editorial/            Gate 2 — editorial acceptance
publication/          Gate 3 — publication decision and page history
export/               Durable export and access-tier policy
release/              Release baselines
setup/                install.sh — one-command install on Debian/Ubuntu
CLAUDE.md             Working instructions for AI-assisted sessions
```

## Running the test suites

Every component ships a plain Python or SQL test script that prints one `PASS` or
`FAIL` line per check, each naming the requirement or Decision Record it verifies.
Suites that touch the canonical store need a reachable PostgreSQL (14+); they drop and
recreate their own database.

```bash
export PGHOST=… PGPORT=… PGUSER=…            # or a local socket with trust auth
bash schema/tests/run.sh                       # canonical store DDL and constraints
python3 collector/tests/test_pipeline.py       # live path: fetch → quarantine → Gate 1
python3 collector/tests/test_warc_ingest.py    # WARC reader/writer and archive recovery
python3 sources/tests/test_register.py         # source registration refusals
python3 storage/tests/test_ocfl.py             # OCFL objects, fixity
python3 storage/tests/test_fixity_schedule.py
python3 editorial/tests/test_gate2.py
python3 publication/tests/test_gate3.py
python3 export/tests/test_dump.py
python3 release/tests/test_baseline.py
python3 registry/validate.py                   # registry consistency
```

A suite that has never been seen to fail proves nothing. Each component's README
records the sabotages under which its suite was shown to go red.

## Installing on a server

[`setup/install.sh`](setup/install.sh) installs PostgreSQL and Python, creates the
database and the OCFL storage roots, loads the schema and runs the suites on a fresh
Debian or Ubuntu system. It collects nothing and registers nothing; both are separate,
deliberate acts that follow it (OPS-001).

## Governance

- The founder/principal editor is the final editorial authority (record §78).
- AI assistance may propose; consequential conclusions and canonical documents require
  human approval (record §79). Every AI-drafted document carries a provenance note
  (record §80) and remains a candidate until approved.
- Controlled documents (DR, SPEC, POL, REQ, METH, PROC) carry explicit status under
  [DR-0046](docs/decision-records/DR-0046-unified-document-control.md). **Status is
  document metadata, never inferred from Git**: a commit is not an approval, a merge is
  not an enactment.
- The Phase I record is preserved verbatim and treated as immutable; changes happen by
  supersession, not in-place edits (see [docs/discovery/PROVENANCE.md](docs/discovery/PROVENANCE.md)).
- Working conventions for sessions with an AI assistant are in [CLAUDE.md](CLAUDE.md).

## Reading order for a newcomer

1. The [Phase I record](docs/discovery/phase-1-requirements-discovery-record.md),
   especially §1–§14 and §104 (the principles). Everything else answers to it.
2. [METH-0001](docs/methodology/METH-0001-evidentiary-method.md), the evidentiary method.
3. [SPEC-0001](docs/specifications/SPEC-0001-conceptual-data-model.md) and
   [SPEC-0003](docs/specifications/SPEC-0003-collection-pipeline.md).
4. [POL-0001](docs/policies/POL-0001-personal-data.md), the personal-data policy, and
   why collection waits on its §10 review.
5. [WP 3.4](docs/phase-3/working-papers/wp-3.4-foundational-corpus-acquisition.md), the
   acquisition strategy, and [collector/README.md](collector/README.md) for what the
   code actually does today.

This README is an entry point, not the project's institutional memory (record §100).
The authoritative statement of requirements, principles, and phase mandates is the
[Phase I Requirements Discovery Record](docs/discovery/phase-1-requirements-discovery-record.md).
