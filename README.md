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
| Phase III — Conceptual Architecture | **Open** — see [docs/phase-3/](docs/phase-3/README.md). All nine planned studies delivered; SPEC-0001…0007, POL-0001, METH-0001 and ten REQ documents effective; all three pipeline gates built. **First collection performed 2026-09-09** — two sanctions lists, registered and run on the archive server ([DR-0093](docs/decision-records/DR-0093-first-source-registrations.md)). **Collection at scale is suspended pending external legal review** ([POL-0001 §10](docs/policies/POL-0001-personal-data.md), DR-0072); the founder ruled on 2026-09-08 that no scale-up precedes that review ([WP 3.4](docs/phase-3/working-papers/wp-3.4-foundational-corpus-acquisition.md), candidate) |

DR-0001…0095 are approved and in force. DR-0094 (third-party web captures —
Common Crawl, the Wayback Machine, and qualifying archives — as an
acquisition channel for registered sources) was approved 2026-09-11 after a
second round of founder rulings on points the draft had left open. DR-0095
governs how DRs are numbered going forward (drafted unnumbered, assigned at
merge) — and, per that rule, one further decision is approved but not yet
numbered: `DR-pending-collection-run-two-agents` (2026-09-12), resolving
DR-0093 §3's collector/pipeline-version tension. No permanent API contract
or technical stack beyond PostgreSQL, Python and OCFL has been frozen.

## Where things stand, plainly

**Governance and design are far ahead of collection.** The evidentiary method, the
data model, the registry, the three-gate pipeline, the storage layout and the
personal-data policy are all decided and documented. The code implements them and is
tested against a real database and real storage. But:

- **Two sources are registered and collected; five are still proposals.** Of the
  seven sanctions authorities in [`sources/candidates/`](sources/README.md), the
  founder accepted `eu-consolidated-list` and `ofac-sdn` on 2026-09-08 and ran the
  first collection on the archive server on 2026-09-09 — five files, ~211 MB, zero
  failures ([DR-0093](docs/decision-records/DR-0093-first-source-registrations.md)).
  The other five remain candidates awaiting a per-source decision; registering is
  the act that authorises collection (OPS-001).
- **A live fetch has now completed, once, deliberately.** `HttpFetcher` acquired
  the two sources above from a real server with an identified User-Agent. No WARC
  file from Common Crawl or the Wayback Machine has been parsed against a live
  archive yet — the WARC reader is exercised only against files the test suite
  writes itself. [`collector/README.md`](collector/README.md) says exactly what is
  and is not verified. The first run's rehearsal exposed two gaps that still
  stand (unchanged bytes stored again, quarantine copies never removed) and
  one that unrelated work fixed the next day (captures now join a capture
  series on every admission) before the two branches were even aware of each
  other — see [DR-0093](docs/decision-records/DR-0093-first-source-registrations.md)
  for the residual it left.
- **The external legal review required by POL-0001 §10 has not been commissioned.**
  Until it is recorded, collection is bound to explicitly registered sources with
  human-configured scope (DR-0071): no open-ended crawling, no bulk social harvesting,
  no automatic structuring of personal data. This is why only two of seven
  institutional, near-zero-personal-data sources were registered rather than all
  seven or a broader crawl.
- **Gate 2 and Gate 3 are human.** Bulk collection produces holdings and review queues,
  never canonical knowledge. That is the design (DR-0066, Principle 5), and it means the
  knowledge graph grows at the pace of editorial review. The first collection created
  zero documentary assertions, as designed.

## The acquisition strategy (candidate)

[WP 3.4](docs/phase-3/working-papers/wp-3.4-foundational-corpus-acquisition.md) proposes
how the foundational corpus is constituted: **not by crawling the general web**, before
or after the legal review, but by

1. a **source census** producing registry entries for the founder to accept or reject;
2. **retrospective recovery** of registered sources from existing web archives, which
   is the only route to the pre-2026 web; and
3. **registered live collection**, daily, through the pipeline.

Its Track A (permitted now under DR-0071) is under way: the WARC recovery path and the
live WARC wrapping are built and tested, and A1 has produced a real first collection
(above). Its Track B waits on the recorded review. Five candidate Decision Records
(CDR-P3-31…35) await the founder.

## Recent work

| Date | What | Where |
|---|---|---|
| 2026-08-26 | Gate 3 built; DR-0086 enacted (tier restrictiveness declared, not derived); seven sanctions authorities drafted as candidate registrations | `publication/`, `sources/` |
| 2026-09-08 | WP 3.4, the foundational corpus acquisition strategy, deposited as candidate with CDR-P3-31…35; founder rules that no collection scale-up precedes the POL-0001 §10 legal review. Separately, two of the seven sanctions candidates verified against their live publishers and DR-0093 drafted and approved for both | [`docs/phase-3/`](docs/phase-3/README.md), [`docs/sources/`](docs/sources/verification-eu-consolidated-list-ofac-sdn.md) |
| 2026-09-09 | WARC recovery path built: a registered source's captures can be recovered from an external archive's WARC file through quarantine and Gate 1, with the archive recorded as acquisition source distinct from the publisher (§28); live fetches of `warc`-format sources are wrapped as WARC records. Separately, `collector/run.py` built and the two DR-0093 sources registered and collected on the archive server — **the project's first collection** | [`collector/`](collector/README.md), `schema/03-pipeline.sql` |
| 2026-09-09/10 | Public identifiers designed and implemented: WP 3.5 resolves Q-12; DR-0087…0092 enacted (ARK scheme, minting at publication, a five-disposition register, `.vN` state qualifiers, ARK-derived URIs, a split's decider shown as a title never an id). SPEC-0007 drafted as a candidate and implemented against it, 77 checks | [`identifiers/`](identifiers/README.md), `schema/08-identifiers.sql` |
| 2026-09-10 | Two independently-developed branches reconciled: DR-0093 renumbered around DR-0087…0092 (both branches had drafted a "DR-0087" for different topics), and two `setup/install.sh` defects found on the founder's first real install (as-root Postgres role creation; branch-only clone) fixed | this file, `docs/decision-records/README.md`, `setup/install.sh` |
| 2026-09-10 | A third branch reconciled: DR-0094 drafted (as "DR-0087", the same collision as above) on how Common Crawl and the Wayback Machine's third-party web captures fit an already-registered source as an acquisition channel, not a source of their own — renumbered to the next free slot on merge. Proposed, pending founder review | `docs/decision-records/DR-0094-third-party-web-captures.md` |
| 2026-09-11 | DR-0095 enacted: after the DR-0087 collision recurred a second time, Decision Records are now drafted unnumbered (`DR-pending-<slug>.md`) with the real number assigned exactly once, at merge — closing the gap DR-0093 and DR-0094 each hit ad hoc | `docs/decision-records/DR-0095-dr-numbering-placeholder-until-merge.md`, `CLAUDE.md`, `docs/decision-records/README.md` |
| 2026-09-11 | DR-0094 approved after a second round of founder rulings on what the draft had left open: loss-triggered third-party recovery may run automatically once scoped to the failed locator; a future archive qualifies by stated criteria rather than needing its own DR; retrieval proceeds independently of the DR-0006 WACZ evaluation. Text amended to carry all four rulings (including how to record them) in the same step that approved it | `docs/decision-records/DR-0094-third-party-web-captures.md` |
| 2026-09-12 | DR-0093 §3's collector_version/pipeline_version tension resolved (option 1 of 3): a run now carries two agents, the founder's existing agent-of-record ruling unchanged, plus a separate, self-registering, versioned software agent (`collector-pipeline`) recorded on the run's preservation events. `release/baseline.py --check` confirmed to pin both dimensions from a real `collector/run.py` invocation; three new checks (across `test_pipeline.py` and `test_run.py`) shown to fail under sabotage before being restored green | `collector/pipeline.py`, `collector/run.py`, `docs/decision-records/DR-pending-collection-run-two-agents.md` |
| 2026-09-12 | WP 3.4 Track A item A2's index tooling built: `census.py` queries Common Crawl's index and the Wayback CDX index for candidate domains, evidence-only (capture counts, first/last seen), no fetch of any candidate host and no database writes — DR-0071(a) does not apply because nothing is collected. 28 tests pass with no network; two rules shown to fail under sabotage (the §28 "a failure explains itself" guard; the by-host deduplication key) and restored. Neither real client has completed a live query — both `index.commoncrawl.org` and `web.archive.org` failed every attempt from this session, tested with both `curl` and Python's own `urllib` | `sources/census.py`, `sources/tests/test_census.py`, `sources/README.md` |

Track A of WP 3.4 (work permitted now under DR-0071) stands as follows. **A1 is
under way**: 2 of the 7 sanctions sources are registered and have completed a
first collection on the archive server (2026-09-09); the other 5 await the
founder's per-source decision. A2 (census tooling against indices), A4 (WACZ
evaluation), A5 (registration classes), A6 (legal-review brief) and A7 (storage
measurement) are not started. A3 is done.

## Picking up development

The next open decision, raised but not yet ruled on, is how a collection run's
software should be versioned for release baselines when a **person** is the
run's agent of record (DR-0093 §3) rather than a software agent — see
["Open decisions"](#open-decisions-for-the-next-session) below and
[CLAUDE.md](CLAUDE.md) for the full session-start protocol.

## Repository layout

```
docs/
  discovery/          Phase I requirements-discovery record (immutable source
                      material) + acquisition provenance
  decision-records/   Unified Decision Record system (record §98); DR-0001…0095
                      approved and in force; register in its README
  phase-2/            Phase II (closed) — working papers WP 0.1–0.8 + provenance,
                      approved consolidation outputs
  phase-3/            Phase III working area
    working-papers/   WP 3.1–3.5 + PROVENANCE.md (SHA-256 at deposit)
  specifications/     SPEC-class controlled documents (DR-0046)
  policies/           POL-class controlled documents (DR-0046)
  requirements/       REQ-class controlled documents (DR-0046/0051)
  methodology/        METH-class controlled documents (DR-0046, record §97)
  sources/            Informal prose notes on possible sources, written before
                      any registration is drafted (distinct from sources/ below)

registry/             Semantic registry: vocabularies, argument schemes, compiler;
                      the source of truth for every enumeration (DR-0078)
sources/              DR-0067 source registry — candidate registrations and the
                      register.py tool; registering authorises collection.
                      census.py discovers new candidates from Common Crawl /
                      Wayback indexes (WP 3.4 A2); collects nothing itself
schema/               Canonical store DDL (PostgreSQL); enums generated from the
                      registry; schema test suite
storage/              OCFL archival storage roots and fixity scheduling
collector/            Gate 1 — acquisition (live fetch and WARC recovery),
                      quarantine, preservation; the stdlib WARC reader/writer
editorial/            Gate 2 — editorial acceptance
publication/          Gate 3 — publication decision and page history
identifiers/          Public identifiers (ARK), the register and the resolver
export/               Durable export and access-tier policy
release/              Release baselines
setup/                install.sh — one-command install on Debian/Ubuntu
site/                 Public-facing progress briefing (not governance content,
                      not the eventual archive website — see site/README.md);
                      published via GitHub Pages from this folder only
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

## Open decisions for the next session

Not yet ruled on by the founder. Each is a real fork, not busywork — pick one,
propose named options with a recommendation (see [CLAUDE.md](CLAUDE.md)), and
wait for the answer before building against an assumption. Two items that
stood here through 2026-09-11/12 (a DR-numbering collision; how a run is
versioned under a human agent of record) are resolved and dropped from this
list — see "Recent work" below for what changed and which DR governs it.

1. **Registering the remaining five sanctions candidates**, or a different
   next source. `sources/candidates/sanctions-authorities.yaml` has five more
   ready; none has been fetched or verified the way the first two were.
2. **WP 3.4's Track A items A4, A5, A6, A7** (WACZ evaluation, registration
   classes, the legal-review brief, storage measurement) are not started;
   A6 in particular blocks nothing today but is the long pole before
   POL-0001 §10 can be commissioned. **A2's index tooling is now built and
   tested** (`sources/census.py`, 2026-09-12) — Common Crawl's index and the
   Wayback CDX index only, discovery of candidate domains with no fetch of
   any candidate host; the other four A2 evidence sources WP 3.4 names
   (Wikipedia citation graphs, sanctions-authority link graphs, OSINT
   source lists, academic bibliographies) remain editorial research tasks,
   not built as tooling. Neither client has completed a live query — both
   indexes were unreachable from this session; see `sources/README.md`.

This README is an entry point, not the project's institutional memory (record §100).
The authoritative statement of requirements, principles, and phase mandates is the
[Phase I Requirements Discovery Record](docs/discovery/phase-1-requirements-discovery-record.md).
