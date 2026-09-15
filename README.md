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

DR-0001…0101 are approved and in force. DR-0095 governs how DRs are numbered
(drafted unnumbered, assigned at merge). **DR-0096…0101 were approved between
2026-09-12 and 2026-09-15 and numbered together on 2026-09-15** — three of
them had reached `main` unnumbered and without register rows, which is the
step DR-0095 prescribes; the register is brought current rather than left to
drift. **DR-0099 and DR-0100 are two records of one decision**, both kept:
parallel sessions each found the establishment-jurisdiction gap and the
founder answered both, so DR-0099 names France as *interim* (and amends
POL-0001 to v1.1) and DR-0100 confirms it while adding the controller and
hosting facts. See the [register](docs/decision-records/README.md) for the
full account. No permanent API contract or technical stack beyond PostgreSQL,
Python and OCFL has been frozen.

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
  seven or a broader crawl. The **brief** for that review is now drafted —
  [`docs/legal/legal-review-brief.md`](docs/legal/legal-review-brief.md) v0.1,
  2026-09-15, WP 3.4 Track A item A6 — and is **not sendable as it stands**: its §9
  lists five things the founder must settle first, beginning with the project's
  establishment jurisdiction, which POL-0001 §10 presumes and the record nowhere states.
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
| 2026-09-12 | DR-0093 §3's collector_version/pipeline_version tension resolved (option 1 of 3): a run now carries two agents, the founder's existing agent-of-record ruling unchanged, plus a separate, self-registering, versioned software agent (`collector-pipeline`) recorded on the run's preservation events. `release/baseline.py --check` confirmed to pin both dimensions from a real `collector/run.py` invocation; three new checks (across `test_pipeline.py` and `test_run.py`) shown to fail under sabotage before being restored green | `collector/pipeline.py`, `collector/run.py`, `docs/decision-records/DR-0097-collection-run-two-agents.md` |
| 2026-09-12 | WP 3.4 Track A item A2's index tooling built: `census.py` queries Common Crawl's index and the Wayback CDX index for candidate domains, evidence-only (capture counts, first/last seen), no fetch of any candidate host and no database writes — DR-0071(a) does not apply because nothing is collected. 28 tests pass with no network; two rules shown to fail under sabotage (the §28 "a failure explains itself" guard; the by-host deduplication key) and restored. Neither real client has completed a live query — both `index.commoncrawl.org` and `web.archive.org` failed every attempt from this session, tested with both `curl` and Python's own `urllib` | `sources/census.py`, `sources/tests/test_census.py`, `sources/README.md` |
| 2026-09-12 | Two more sanctions-candidate locators verified, live, real rehearsal through the actual collector (throwaway database): `uk-ofsi-consolidated` fully (CSV + XML, OFSI's own blob storage, not the gov.uk publication page); `bis-entity-list` partially — its Denied Persons List CSV found and verified, its Entity List half deliberately left unverified rather than substituting Commerce's Consolidated Screening List, which would misattribute OFAC's own data to BIS. Zero documentary assertions; the two-agent split (DR-0097) held correctly against real, live sources for the first time. Neither is registered — that stays the founder's act, per source | `sources/candidates/sanctions-authorities.yaml`, `docs/sources/verification-bis-dpl-ofsi-consolidated.md`, `sources/README.md` |
| 2026-09-12 | Founder approved registering both: OFSI in full, BIS with its Denied Persons List locator only (DR-0096). Drafting it surfaced a real gap in `register.py`: dependence-recording only linked sources registered in the same `--only` call, so `uk-ofsi-consolidated`'s declared dependence on the already-registered `eu-consolidated-list` would be silently dropped by a plain `--commit`. Registration itself is not yet executed — that happens on the archive server, not in this session | `docs/decision-records/DR-0096-second-source-registrations.md` |
| 2026-09-12 | The `register.py` dependence gap fixed, at the founder's direction: `commit()` now resolves a dependence link's other end against the database by name when it is outside the current `--only` batch, and `validate()` gained a `known_keys` parameter so the existence check does not flag it as unknown. Verified before and after — the gap reproduced in a throwaway database seeded to match the archive server's state, then confirmed closed in the same scenario, plus a second scenario (a dependence on nothing registered anywhere) confirmed to print a note and insert nothing rather than crash. `sources/tests/test_register.py` gained 4 checks (27 → 31 total), two shown to fail when each half of the fix was reverted in turn | `sources/register.py`, `sources/tests/test_register.py`, `sources/README.md`, `docs/decision-records/DR-0096-second-source-registrations.md` |
| 2026-09-13 | `seco-sanctions` verified, fully, on a second attempt: the previous session's six blind URL guesses had all missed that the real file lives on a different host (`sesam.search.admin.ch`) than the main site, only found this time by fetching the actual homepage and following its real navigation to the "Gesamtliste" download. 42 300 406 bytes, digest stable across two fetches and identical across all four `lang=` variants, 17 312 `<target>` elements, acquired end to end by the real collector (1 discovered, 1 acquired, 0 failed, 0 documentary assertions). No registration decision made yet | `sources/candidates/sanctions-authorities.yaml`, `docs/sources/verification-seco-sanctions.md`, `sources/README.md` |
| 2026-09-14 | Founder approved registering `seco-sanctions` — a separate decision from the OFSI/BIS pair, not linked to it, executable in either order (`DR-0098`). Re-verified the 2026-09-12 `register.py` dependence fix on a single-source `--only` call rather than a pair (its first test on that shape): `--commit --only seco-sanctions` alone, in a throwaway database seeded to match the real archive server's actual state, correctly recorded the declared dependence on the already-registered `eu-consolidated-list` with no companion source and no manual SQL. Three of seven sanctions authorities now approved for registration, none yet executed on the archive server | `docs/decision-records/DR-0098-seco-sanctions-registration.md` |
| 2026-09-14 | Branch `claude/common-crawl-fk1bw8` merged (PR #26): DR-0095, DR-0094's approval, the two-agent collection-run split, the `register.py` dependence fix, census tooling, and the OFSI/BIS/SECO verification-and-approval work above all landed on `main` in one pull request | PR #26 |
| 2026-09-14 | WP 3.4 Track A item A6 drafted: a legal-review brief expanding §7's five questions with the specific project facts a reviewer needs, and what to hand them. Found, rather than resolved, a real blocking gap: **no controlled document names the project's establishment jurisdiction**, which POL-0001 §10 and WP 3.4 §7 both assume is already settled — commissioning the review needs that answered first. Proposes no new project rule; not sent to anyone by this deposit | `docs/legal/legal-review-brief.md`, `docs/policies/README.md` |
| 2026-09-14 | Founder answered directly: the project's interim establishment jurisdiction is **France**, the founder's own personal jurisdiction — no separate legal entity exists yet. POL-0001 amended to v1.1 (§10 names France; no other substantive change), `DR-0099` records the ruling, and the legal-review brief updated to reflect it — which surfaced a narrower open question in its place: whether the project should form a legal entity before or as part of commissioning the §10 review, since GDPR's establishment concept ordinarily presumes an organized controller | `docs/policies/POL-0001-personal-data.md`, `docs/decision-records/DR-0099-establishment-jurisdiction.md`, `docs/legal/legal-review-brief.md` |
| 2026-09-15 | WP 3.4 Track A item A4, the WACZ evaluation DR-0006 made a standing task, done from primary sources: the WACZ container specification (v1.1.1) is stable and reachable, but its signing specification (v0.1.0) is, by its own words, "a working draft for a proposal" — confirmed against live PyPI release metadata for `wacz`, `authsign`, and `wacz-signing` (all still pre-1.0). Recommends **deferring** WACZ adoption entirely, WARC via `collector/pipeline.py` unchanged, on two stated revisit triggers; the "jurisdictionally meaningful" half of DR-0006's question is flagged as unanswerable from a spec alone, connecting to but not added to the A6 brief | [`WP 3.6`](docs/phase-3/working-papers/wp-3.6-wacz-evaluation.md) |
| 2026-09-15 | WP 3.4 Track A item A7's measurement tooling built and tested: `storage/measure.py` reads `collector_run` for recorded bytes/throughput and walks the OCFL roots and quarantine directory for real on-disk footprint, reporting a measured duplication ratio for the undischarged-quarantine-copy gap `collector/README.md` documents. 11 tests against a real local database and filesystem tree, one rule shown to fail under sabotage and restored. An archive-server runbook and a fill-in results template were then written for executing both halves of A7 (baseline measurement of the two A1 sources; one retrospective WARC pull for a registered domain, WP 3.4 §4/CDR-P3-35) — neither executed, since the retrospective pull is new acquisition needing a person as agent of record (DR-0093 §3) on the archive server. `docs/sources/README.md` gained a section documenting and linking the directory's verification/measurement records, a genre that existed but had gone undescribed since DR-0093's rehearsal note | `storage/measure.py`, `storage/tests/test_measure.py`, [`docs/runbooks/A7-storage-bandwidth-measurement.md`](docs/runbooks/A7-storage-bandwidth-measurement.md), [`docs/sources/TEMPLATE-a7-measurement-results.md`](docs/sources/TEMPLATE-a7-measurement-results.md) |

Track A of WP 3.4 (work permitted now under DR-0071) stands as follows. **A1
is under way**: 2 of the 7 sanctions sources are registered and have completed
a first collection on the archive server (2026-09-09); 3 more are approved but
not yet executed; the other 2 await verification. **A2's index tooling is
built** (2026-09-12), no live query yet. **A3 is done.** **A4's WACZ
evaluation is done** (2026-09-15, [WP 3.6](docs/phase-3/working-papers/wp-3.6-wacz-evaluation.md))
— recommends deferring adoption, WARC unchanged. **A6's legal-review brief is
done** (v0.4, 2026-09-15), with all five founder decisions in its §9 closed;
commissioning it is a separate founder act. **A7's measurement tooling is
built and tested** (2026-09-15) with a runbook written and unexecuted. **A5**
(registration classes) is the only item not started. See the Track A table in
[CLAUDE.md](CLAUDE.md) for each item's exact state.

## Picking up development

The next open decision, raised but not yet ruled on, is whether the project
should **form a legal entity** before, or as part of, commissioning the
POL-0001 §10 review — see
["Open decisions"](#open-decisions-for-the-next-session) below and
[CLAUDE.md](CLAUDE.md) for the full session-start protocol.

## Repository layout

```
docs/
  discovery/          Phase I requirements-discovery record (immutable source
                      material) + acquisition provenance
  decision-records/   Unified Decision Record system (record §98); DR-0001…0101
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
  runbooks/           Operator runbooks for executing already-authorised
                      tooling on the archive server — not Decision Records,
                      not controlled documents, no policy proposed
  legal/              Legal-review brief for POL-0001 §10 (WP 3.4 A6) — not
                      legal advice, not itself a Decision Record

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
AGENTS.md             Pointer to CLAUDE.md, for tools that look for this
                      filename specifically; no separate instructions
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
wait for the answer before building against an assumption. Five items that
stood here through 2026-09-11/14 (a DR-numbering collision; how a run is
versioned under a human agent of record; registering `uk-ofsi-consolidated`/
`bis-entity-list`; registering `seco-sanctions`; the project's establishment
jurisdiction) are resolved and dropped from this list — see "Recent work"
below for what changed and which DR governs each. **None of the three
approved registrations has been executed on the archive server yet** — that
remains outstanding, but it is no longer an open *decision*, just
outstanding *execution*.

1. **Whether POL-0001 §8.3's legal posture survives French law.** Not a
   question for a session to settle — but the A6 brief's drafting put it on
   the table and the founder should know it is there. With the jurisdiction
   now recorded as **France** — interim, 2026-09-14
   ([`DR-0099`](docs/decision-records/DR-0099-establishment-jurisdiction.md)),
   confirmed and extended 2026-09-15
   ([`DR-0100`](docs/decision-records/DR-0100-jurisdiction-controller-and-hosting.md))
   — the LIL's **Article 46** limits processing of
   criminal-offence data to a closed list of actors that a private
   documentation archive does not obviously sit in, while **Article 80**
   disapplies Article 46 for university/artistic/literary expression and for
   professional journalism. POL-0001 §8.3 ruled archiving and research
   *primary* and expression *secondary*; French law may invert that. The
   brief puts it to counsel at Q2 and Q3 and answers nothing — the drafter is
   not a lawyer and the texts were read from the CNIL's consolidated version,
   not Légifrance. **Nothing changes in POL-0001 until the review is
   recorded**; this is here so the ruling is not assumed safe in the interval.
2. **Whether the project should form a legal entity before, or as part of,
   commissioning the POL-0001 §10 review.** Surfaced 2026-09-14 while
   naming France as the interim establishment jurisdiction
   (`DR-0099`): no separate legal entity
   exists, and GDPR's establishment concept ordinarily presumes an
   organized controller. Engaging a reviewer productively may depend on
   knowing whether they are advising an individual running a project or an
   entity yet to be formed. **Still open** after the 2026-09-15 record, which
   states the controller as the founder as a natural person without closing
   this — a founder decision. The brief carries it to counsel at Q6 and flags
   it at §9.1–9.3.
3. **Registering `eur-lex-sanctions` or `ua-nsdc-sanctions`.** Neither is
   verified; each needs identifying a specific legal instrument or
   decision set, which is legal or editorial judgment, not a URL to find
   — closer to founder-guided work than something a session should
   attempt alone.
4. **WP 3.4's Track A item A5** (registration classes) is the only Track A
   item not started. **A4, the WACZ evaluation, is done**
   ([WP 3.6](docs/phase-3/working-papers/wp-3.6-wacz-evaluation.md),
   2026-09-15, CDR-P3-42 candidate) — recommends **deferring** WACZ adoption
   (the container spec is stable at v1.1.1, but its signing layer is a
   pre-1.0 working draft at v0.1.0), WARC via `collector/pipeline.py`
   unchanged, on two stated revisit triggers. **A6, the legal-review brief,
   is done** — [`docs/legal/legal-review-brief.md`](docs/legal/legal-review-brief.md)
   v0.4, 2026-09-15, with **all five founder decisions in its §9 closed**:
   France, controller a natural person, IONOS/Spain (§9.1–9.3); Part A
   (Q1–Q6) to French data-protection counsel with Part B (Q7–Q12) held for
   IP/media counsel (§9.5); counsel answers for both the project as it is and
   as it intends to be, naming the deltas, which become POL-0001 §11 review
   triggers (§9.4, §3.5). **Not a decision but still outstanding:** every LIL
   article the brief quotes must be checked against Légifrance, which was 403
   behind an anti-bot challenge when it was drafted — CNIL's consolidated
   text is what was read. Commissioning is a separate founder act. Three
   candidate DRs arose, **renumbered CDR-P3-43…45** because a parallel
   session's WP 3.6 had independently taken CDR-P3-42 the same day;
   **CDR-P3-43 was discharged** into the jurisdiction record at item 1 above,
   **CDR-P3-44** into
   [`DR-0101`](docs/decision-records/DR-0101-recording-the-legal-review.md)
   — "recorded" in POL-0001 §10 now means one specific act, fixed
   deliberately before the advice exists — and **CDR-P3-45 is held** with a
   named trigger, the start of Gate 3 work, so the brief has no open
   proposals. The gap it holds open, found by reading the code:
   `rights_basis` is free text, the two registered sources carry
   `may-redistribute` on a basis whose own text says "NOT LEGALLY REVIEWED",
   and nothing in the schema or Gate 3 prevents a publication decision
   resting on it — not urgent, since nothing is published. **A2's index
   tooling is now built and tested**
   (`sources/census.py`, 2026-09-12) — Common Crawl's index and the
   Wayback CDX index only, discovery of candidate domains with no fetch of
   any candidate host; the other four A2 evidence sources WP 3.4 names
   (Wikipedia citation graphs, sanctions-authority link graphs, OSINT
   source lists, academic bibliographies) remain editorial research tasks,
   not built as tooling. Neither client has completed a live query — both
   indexes were unreachable from this session; see `sources/README.md`.
   **A7's measurement tooling is now built and tested**
   (`storage/measure.py`, 2026-09-15) — reads `collector_run` for recorded
   bytes/throughput and walks the OCFL roots and quarantine directory for
   real on-disk footprint, including a measured duplication ratio for the
   undischarged-quarantine-copy gap `collector/README.md` documents; not
   yet run against the archive server's real database, so WP 3.4 §5.3's
   real numbers are still outstanding, and it deliberately does not perform
   A7's "one retrospective pull" clause (new acquisition, for
   `collector/run.py` on the archive server) or extrapolate the two
   registered sources' size onto the five unregistered candidates. A
   runbook for executing both halves of A7 on the archive server —
   [`docs/runbooks/A7-storage-bandwidth-measurement.md`](docs/runbooks/A7-storage-bandwidth-measurement.md)
   — is written and unexecuted.

This README is an entry point, not the project's institutional memory (record §100).
The authoritative statement of requirements, principles, and phase mandates is the
[Phase I Requirements Discovery Record](docs/discovery/phase-1-requirements-discovery-record.md).
