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

DR-0001…0107 are approved and in force. DR-0095 governs how DRs are numbered
(drafted unnumbered, assigned at merge). **DR-0096…0101 were approved between
2026-09-12 and 2026-09-15 and numbered together on 2026-09-15** — three of
them had reached `main` unnumbered and without register rows, which is the
step DR-0095 prescribes; the register is brought current rather than left to
drift. **DR-0099 and DR-0100 are two records of one decision**, both kept:
parallel sessions each found the establishment-jurisdiction gap and the
founder answered both, so DR-0099 names France as *interim* (and amends
POL-0001 to v1.1; the policy is now at **v1.2**, whose §10 names DR-0100 and
restates its facts) and DR-0100 confirms it while adding the controller and
hosting facts. See the [register](docs/decision-records/README.md) for the
full account. No permanent API contract or technical stack beyond PostgreSQL,
Python and OCFL has been frozen.

## Where things stand, plainly

**Governance and design are far ahead of collection.** The evidentiary method, the
data model, the registry, the three-gate pipeline, the storage layout and the
personal-data policy are all decided and documented. The code implements them and is
tested against a real database and real storage. But:

- **Six of the seven sanctions sources are registered and collected; one
  remains blocked.** Of the seven sanctions authorities in
  [`sources/candidates/`](sources/README.md), the founder accepted
  `eu-consolidated-list` and `ofac-sdn` on 2026-09-08 and ran the first
  collection on the archive server on 2026-09-09 — five files, ~211 MB, zero
  failures ([DR-0093](docs/decision-records/DR-0093-first-source-registrations.md)).
  `eur-lex-sanctions` ([DR-0105](docs/decision-records/DR-0105-eur-lex-sanctions-registration.md)),
  `uk-ofsi-consolidated`, `bis-entity-list` (Denied Persons List half only)
  and `seco-sanctions` ([DR-0096](docs/decision-records/README.md),
  [DR-0098](docs/decision-records/README.md)) followed on **2026-09-21**,
  each a separate decision executed by a person on the archive server.
  `ua-nsdc-sanctions` remains a candidate, blocked on a Cloudflare challenge
  ([#46](https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues/46)); registering is the act that authorises collection
  (OPS-001).
- **A live fetch has now completed, twice, deliberately.** `HttpFetcher` acquired
  the sources above from real servers with an identified User-Agent. No WARC
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
| 2026-09-19 | Two regressions from DR-0103's class mechanism fixed before they reached the archive server: `load_candidates()`'s new three-value return had broken `collector/run.py`'s `find_candidate()` and the setup of four test suites, and — more seriously — `register.py --commit` passed the *unmerged* candidate list to `commit()`, so registering any of the seven (now all class-referencing) candidates would have crashed on the first real execution of DR-0096/DR-0098. `find_candidate()` and `main()` now merge first; a new end-to-end `--commit` check (32 in `test_register.py`) shown to fail under sabotage; two suites (`release`, `export`) also fixed for the DR-0097 `software_agent_id` argument. All 14 suites green. Separately, the legal-review brief's Part A confirmed sent to counsel, response pending; a third Légifrance verification attempt logged, still 403 | `sources/register.py`, `collector/run.py`, `sources/README.md`, `docs/sources/verification-lil-articles.md` |
| 2026-09-12 | Founder approved registering both: OFSI in full, BIS with its Denied Persons List locator only (DR-0096). Drafting it surfaced a real gap in `register.py`: dependence-recording only linked sources registered in the same `--only` call, so `uk-ofsi-consolidated`'s declared dependence on the already-registered `eu-consolidated-list` would be silently dropped by a plain `--commit`. Registration itself is not yet executed — that happens on the archive server, not in this session | `docs/decision-records/DR-0096-second-source-registrations.md` |
| 2026-09-12 | The `register.py` dependence gap fixed, at the founder's direction: `commit()` now resolves a dependence link's other end against the database by name when it is outside the current `--only` batch, and `validate()` gained a `known_keys` parameter so the existence check does not flag it as unknown. Verified before and after — the gap reproduced in a throwaway database seeded to match the archive server's state, then confirmed closed in the same scenario, plus a second scenario (a dependence on nothing registered anywhere) confirmed to print a note and insert nothing rather than crash. `sources/tests/test_register.py` gained 4 checks (27 → 31 total), two shown to fail when each half of the fix was reverted in turn | `sources/register.py`, `sources/tests/test_register.py`, `sources/README.md`, `docs/decision-records/DR-0096-second-source-registrations.md` |
| 2026-09-13 | `seco-sanctions` verified, fully, on a second attempt: the previous session's six blind URL guesses had all missed that the real file lives on a different host (`sesam.search.admin.ch`) than the main site, only found this time by fetching the actual homepage and following its real navigation to the "Gesamtliste" download. 42 300 406 bytes, digest stable across two fetches and identical across all four `lang=` variants, 17 312 `<target>` elements, acquired end to end by the real collector (1 discovered, 1 acquired, 0 failed, 0 documentary assertions). No registration decision made yet | `sources/candidates/sanctions-authorities.yaml`, `docs/sources/verification-seco-sanctions.md`, `sources/README.md` |
| 2026-09-14 | Founder approved registering `seco-sanctions` — a separate decision from the OFSI/BIS pair, not linked to it, executable in either order (`DR-0098`). Re-verified the 2026-09-12 `register.py` dependence fix on a single-source `--only` call rather than a pair (its first test on that shape): `--commit --only seco-sanctions` alone, in a throwaway database seeded to match the real archive server's actual state, correctly recorded the declared dependence on the already-registered `eu-consolidated-list` with no companion source and no manual SQL. Three of seven sanctions authorities now approved for registration, none yet executed on the archive server | `docs/decision-records/DR-0098-seco-sanctions-registration.md` |
| 2026-09-14 | Branch `claude/common-crawl-fk1bw8` merged (PR #26): DR-0095, DR-0094's approval, the two-agent collection-run split, the `register.py` dependence fix, census tooling, and the OFSI/BIS/SECO verification-and-approval work above all landed on `main` in one pull request | PR #26 |
| 2026-09-14 | WP 3.4 Track A item A6 drafted: a legal-review brief expanding §7's five questions with the specific project facts a reviewer needs, and what to hand them. Found, rather than resolved, a real blocking gap: **no controlled document names the project's establishment jurisdiction**, which POL-0001 §10 and WP 3.4 §7 both assume is already settled — commissioning the review needs that answered first. Proposes no new project rule; not sent to anyone by this deposit | `docs/legal/legal-review-brief.md`, `docs/policies/README.md` |
| 2026-09-14 | Founder answered directly: the project's interim establishment jurisdiction is **France**, the founder's own personal jurisdiction — no separate legal entity exists yet. POL-0001 amended to v1.1 (§10 names France; no other substantive change), `DR-0099` records the ruling, and the legal-review brief updated to reflect it — which surfaced a narrower open question in its place: whether the project should form a legal entity before or as part of commissioning the §10 review, since GDPR's establishment concept ordinarily presumes an organized controller | `docs/policies/POL-0001-personal-data.md`, `docs/decision-records/DR-0099-establishment-jurisdiction.md`, `docs/legal/legal-review-brief.md` |
| 2026-09-15 | WP 3.4 Track A item A4, the WACZ evaluation DR-0006 made a standing task, done from primary sources: the WACZ container specification (v1.1.1) is stable and reachable, but its signing specification (v0.1.0) is, by its own words, "a working draft for a proposal" — confirmed against live PyPI release metadata for `wacz`, `authsign`, and `wacz-signing` (all still pre-1.0). Recommends **deferring** WACZ adoption entirely, WARC via `collector/pipeline.py` unchanged, on two stated revisit triggers; the "jurisdictionally meaningful" half of DR-0006's question is flagged as unanswerable from a spec alone, connecting to but not added to the A6 brief | [`WP 3.6`](docs/phase-3/working-papers/wp-3.6-wacz-evaluation.md) |
| 2026-09-15 | WP 3.4 Track A item A7's measurement tooling built and tested: `storage/measure.py` reads `collector_run` for recorded bytes/throughput and walks the OCFL roots and quarantine directory for real on-disk footprint, reporting a measured duplication ratio for the undischarged-quarantine-copy gap `collector/README.md` documents. 11 tests against a real local database and filesystem tree, one rule shown to fail under sabotage and restored. An archive-server runbook and a fill-in results template were then written for executing both halves of A7 (baseline measurement of the two A1 sources; one retrospective WARC pull for a registered domain, WP 3.4 §4/CDR-P3-35) — neither executed, since the retrospective pull is new acquisition needing a person as agent of record (DR-0093 §3) on the archive server. `docs/sources/README.md` gained a section documenting and linking the directory's verification/measurement records, a genre that existed but had gone undescribed since DR-0093's rehearsal note | `storage/measure.py`, `storage/tests/test_measure.py`, [`docs/runbooks/A7-storage-bandwidth-measurement.md`](docs/runbooks/A7-storage-bandwidth-measurement.md), [`docs/sources/TEMPLATE-a7-measurement-results.md`](docs/sources/TEMPLATE-a7-measurement-results.md) |
| 2026-09-15 | WP 3.4 Track A item **A6 done** (legal-review brief v0.4, French law, all five of its §9 founder decisions closed) and **two parallel A6 drafts reconciled** — the other line of work had already done A6 and A4 on an unmerged branch, so both are kept with DR-0100 superseding DR-0099 and the A6 brief's candidates renumbered around WP 3.6's CDR-P3-42. **DR-0096…0101 numbered** and the register brought current — three had reached `main` unnumbered and with no register rows. **DR-0102** supersedes DR-0095: CDR numbers are now assigned at merge like DR numbers, a session checks **unmerged** branches before starting (not just `origin/main`), and in-place revision of a record that has not reached `main` is permitted only under four named conditions. **POL-0001 is at v1.2** — §10 names DR-0100 and restates the jurisdiction, controller and hosting facts in the policy itself | `docs/legal/`, `docs/decision-records/`, `CLAUDE.md`, `docs/policies/POL-0001-personal-data.md` |
| 2026-09-16 | WP 3.4 Track A item **A5 (registration classes) enacted as `DR-0103`**, at the founder's direction. Enacting it surfaced a real numbering collision the merged A5 PR (#29) had left in place: its design paper was deposited as `wp-3.5-registration-classes.md`, silently colliding with the already-taken WP 3.5 (identifier design), with no `docs/phase-3/README.md` row or `PROVENANCE.md` entry. Renumbered to **WP 3.7**, pointed its candidate-DR section at the correct pre-existing **CDR-P3-32** (from WP 3.4 §8, not a new CDR), and added the missing register/provenance entries | `docs/decision-records/DR-0103-registration-classes.md`, [`WP 3.7`](docs/phase-3/working-papers/wp-3.7-registration-classes.md), `docs/phase-3/working-papers/PROVENANCE.md` |
| 2026-09-17 | Founder named the initial registration classes' grouping principle: **jurisdiction first, topic second**, matching WP 3.7 §7's recommendation. All seven `sanctions-authorities.yaml` sources wired to a class; four needed explicit per-source overrides where the class default would otherwise have silently changed an already-verified or DR-approved value (`capture_format`, `rights_permission`). Caught and fixed a live regression: `eu-consolidated-list` had already silently inherited `capture_format: warc` from its class against its DR-0093-verified `http`, the same fix `ofac-sdn` already carried | `sources/candidates/sanctions-authorities.yaml`, `sources/README.md` |
| 2026-09-17 | WP 3.4 Track A item A2's index clients **completed a live query for the first time**: this session's network reached both `index.commoncrawl.org` and `web.archive.org`, where every prior session's had failed (`ECONNRESET`/timeout). Ran both against `rnbo.gov.ua` (the `ua-nsdc-sanctions` publisher domain) — Wayback returned 25 hosts including a `sanctions-t.rnbo.gov.ua` subdomain worth a look; Common Crawl returned 2. Network access varies by session (CLAUDE.md); this does not mean the gap is permanently closed, only that it is not fixed shut either | `sources/census.py` |
| 2026-09-19 | Full status check across every component suite (per CLAUDE.md's "run the suites you will touch before editing", extended here since no Track A item was actionable without either a founder ruling or archive-server access): found `release/tests/test_baseline.py` had been erroring out (0/27, `TypeError`) since DR-0097 added a required `software_agent_id` argument to `Collector.__init__` and this test's own call site was never updated. Fixed; also renamed the stale `DR-pending-collection-run-two-agents` citation, still present in `collector/pipeline.py`, `collector/run.py`, and their tests, to `DR-0097`. All six component suites (199 checks) and `registry/validate.py` (31 entries) confirmed green. A fourth Légifrance re-attempt (same Article 46 direct-link URL as the three prior attempts) got the same `403`/Cloudflare-challenge response; logged as the fourth data point in the standing verification-attempt log | `release/tests/test_baseline.py`, `collector/pipeline.py`, `collector/run.py`, `collector/tests/`, `docs/sources/verification-lil-articles.md` |
| 2026-09-20 | Founder ruled, one question at a time: pursue both remaining unverified sanctions candidates (`eur-lex-sanctions`, `ua-nsdc-sanctions`) in parallel rather than sequentially or singly — research only, no registration by this or any session; and **start forming an association loi 1901 now**, in parallel with French counsel's still-pending Part A response, resolving README's open-decisions item 2. Candidate DR drafted recording the ruling and what remains outside any session's reach (statutes, filing, SIRET, first general assembly) — the controller stays the founder as a natural person (`DR-0100`) until the association legally exists and a separate POL-0001 §11 review records the handover | `docs/decision-records/DR-0104-legal-entity-formation.md` |
| 2026-09-20 | Both remaining sanctions candidates researched in parallel, per the founder's ruling above. **`eur-lex-sanctions`** verified partially: the two foundational instruments identified (Council Regulation 269/2014, Council Decision 2014/145/CFSP), fetched, and rehearsed through the real collector (2/2 acquired, 0 failed) — with a genuine open question flagged, not resolved: its consolidated-text locator carries a dated CELEX suffix that advances roughly monthly, unlike every other sanctions candidate's stable list-file locator. **`ua-nsdc-sanctions`** stays unverified: the actual register (`drs.nsdc.gov.ua`, the NSDC's own "State Register of Sanctions," found via rnbo.gov.ua's own navigation) is now identified but returns HTTP 403 behind a Cloudflare managed challenge, the same block class as Légifrance. **Separately, this branch independently rediscovered the same `register.py --commit` bug the 2026-09-19 row above already fixed on `main`** — unaware of it, since this branch was cut before that fix merged. `sources/tests/test_register.py` carried the identical redundant fix. On merging the two branches, the 2026-09-19 fix was kept (more thorough — also covers `collector/run.py` and `collector/tests/test_run.py`, plus a real end-to-end `--commit` subprocess check) and this branch's duplicate discarded; `eur-lex-sanctions`'s own verification and approval work is unaffected | `sources/candidates/sanctions-authorities.yaml`, `docs/sources/verification-eur-lex-sanctions.md`, `docs/sources/verification-ua-nsdc-sanctions.md`, `sources/README.md` |
| 2026-09-21 | Founder closed `eur-lex-sanctions`'s two remaining open questions, one at a time: `run_locators` keeps both instruments (Regulation 269/2014 and Decision 2014/145/CFSP), not the Regulation alone; and its dated-CELEX consolidated-text locator is re-verified manually before each collection run — the same agent-of-record model every other source uses (DR-0093 §3), no new tooling built. Founder then **approved `eur-lex-sanctions` for registration**, a fourth candidate joining `uk-ofsi-consolidated`/`bis-entity-list`/`seco-sanctions` as approved-but-unexecuted. Its cross-batch dependence on the already-registered `eu-consolidated-list` re-verified in a throwaway database seeded to match the archive server's real state, matching the `--only`-batch pattern `DR-0096`/`DR-0098` established | `docs/decision-records/DR-0105-eur-lex-sanctions-registration.md`, `docs/sources/verification-eur-lex-sanctions.md`, `sources/candidates/sanctions-authorities.yaml` |
| 2026-09-21 | **`eur-lex-sanctions` registration and first collection executed on the archive server**, interactively, by the founder: 2 discovered, 2 acquired, 0 failed, 16 199 485 bytes preserved, 0 documentary assertions (run `2eeef589-56aa-430d-af5f-855f5b6775d0`). Execution surfaced a real, unrelated blocker — the archive server's checkout was on a stale pre-DR-0087 branch, and its live database schema was ~10 weeks behind `main` (missing the whole identifier subsystem and more); this project has no schema-migration mechanism for a live database. Resolved by a full backup-then-reload: switched to `main`, `pg_dump` full and data-only to a timestamped backup, schema rebuilt from current DDL as the `postgres` superuser (the connecting `root` role lacked the privilege `pg_dump --disable-triggers`'s technique needs), data reloaded past expected DDL-seeded reference-table duplicate-key conflicts — row counts verified identical across every real data table before and after. Also numbered `DR-0104`/`DR-0105`, which had reached `main` still named `DR-pending-*` from an earlier merge that skipped the renaming step — every cross-reference updated | `docs/decision-records/DR-0105-eur-lex-sanctions-registration.md`, `docs/decision-records/DR-0104-legal-entity-formation.md`, `docs/decision-records/README.md` |
| 2026-09-21 | **The remaining three approved sanctions registrations executed on the archive server**, interactively, by the founder: `uk-ofsi-consolidated` (run `efcdcb38-44a8-4f07-972a-8a99c220b82b`, 70 739 812 bytes), `bis-entity-list` (run `cc2f55e3-84e0-4bca-a169-7c2072c46edb`, 110 427 bytes), `seco-sanctions` (run `d21d849d-fe96-409c-ae85-cb14b42f739e`, 42 300 406 bytes), all 0 failed, all dependence links on `eu-consolidated-list` recorded correctly. Six of seven sanctions authorities now registered and collected. DR-0096/DR-0098 *Executed* sections updated | `docs/decision-records/DR-0096-second-source-registrations.md`, `docs/decision-records/DR-0098-seco-sanctions-registration.md` |
| 2026-09-21 | **Founder redirected the project's central purpose**, mid-session, after pausing work to reflect: not territorial control, but strike-level completeness — "to come the closest possible to record EVERY SINGLE MISSILE, DRONE, that fell on each side and their effect." First step: two candidates drafted for territorial control (`isw-orca`, `deepstatemap`, `sources/candidates/war-facts.yaml`) before the redirection sharpened further; then two strike-tracking candidates for the actual goal (`kpszsu`, `generalstaffzsu`, `sources/candidates/strike-tracking.yaml`) — official Ukrainian channels covering both directions (incoming Russian strikes, outgoing Ukrainian strikes). All four verified and rehearsed through the real collector; none registered yet | `sources/candidates/war-facts.yaml`, `sources/candidates/strike-tracking.yaml`, `docs/sources/verification-war-facts-first-two.md`, `docs/sources/verification-strike-tracking-first-two.md` |
| 2026-09-21 | **Built and tested a Telegram channel historical-backfill mechanism**, `collector/telegram_backfill.py` (CDR-P3-46, candidate) — walks `t.me/s/<channel>?before=<id>` pagination backward, preserving each page through the ordinary `Collector.run()` path, one network request per page (a `CachingFetcher` avoids the double-fetch a naive discover-then-preserve approach would cause). 10 tests, sabotage-verified (removing the cache turns exactly the caching checks red; removing the bottom-of-history check crashes rather than looping forever). Rehearsed live against the real `kpszsu` channel: 2 pages, 0 failed, genuine pagination confirmed. No full backfill run. `docs/runbooks/telegram-channel-backfill.md` written with explicit rate-limit/block-risk warnings — a full `kpszsu` backfill is an estimated 2 500-4 000 requests, and a block would cost the archive server's Telegram access generally, not just this job. Civilian casualties noted as a future subject area at the founder's request, deliberately deferred, not started — see README's open decisions | `collector/telegram_backfill.py`, `collector/tests/test_telegram_backfill.py`, `docs/runbooks/telegram-channel-backfill.md`, `collector/README.md` |
| 2026-09-22 | **`kpszsu` and `generalstaffzsu` registered and their first collection and a bounded backfill pass executed on the archive server**, interactively, by the founder, per `DR-0106-strike-tracking-registration.md`. Registration hit a real bug — `register.py --commit` re-run left two identical `source` rows per candidate, which `collector/run.py`'s existing duplicate check correctly refused to run against; diagnosed via read-only query confirming zero dependent `collector_run` rows on either duplicate before either was deleted, no code change needed. First ordinary collection run each: `kpszsu` 112 709 bytes, `generalstaffzsu` 135 349 bytes, 0 failed. Bounded backfill pass each (`--max-pages 20 --delay 3`): 20/20 pages preserved, 0 failed, no rate-limit signals — `kpszsu` reached back to post id 79190, `generalstaffzsu` to 41903. Separately, PostgreSQL had been reinstalled as version 15 (not 16, `CLAUDE.md`'s documented version) with `pg_hba.conf` reverted to `peer` auth for the `postgres` role specifically (a more specific rule than the general `trust` line, so it won and blocked connections) — fixed by editing that one line. A full backfill remains undecided; see README's open decisions | `docs/decision-records/DR-0106-strike-tracking-registration.md` |
| 2026-09-23 | **A second, larger bounded backfill pass executed for both channels** (`--max-pages 100 --delay 3`, resumed from 2026-09-22's stop points), founder-directed as a scale check before any full-backfill decision. `kpszsu`: 100/100 pages preserved, 0 failed, reached post id 77184. `generalstaffzsu`: 100/100 pages preserved, 0 failed, reached post id 39618. Still zero rate-limit signals, now across 240 total backfill requests. A full backfill remains undecided | `docs/decision-records/DR-0106-strike-tracking-registration.md` |

Track A of WP 3.4 (work permitted now under DR-0071): **A3, A4, A5 and A6 are
done; A1 is six sources of seven; A2 and A7 have their tooling built and their
remaining halves open.** This paragraph used to restate each item's status and
drifted from the table it claimed to summarise — what each item *produced*
is the Track A table in [CLAUDE.md](CLAUDE.md), and what is still open is on
the board: [`epic:track-a`](https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues?q=is%3Aopen+label%3A%22epic%3Atrack-a%22).

Track B (WP 3.4 §4.2) does not start until DR-0072's successor records the
POL-0001 §10 review.

## Picking up development

Start from the board — [what needs a ruling](https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues?q=is%3Aopen+label%3A%22kind%3Adecision%22)
— and read [CLAUDE.md](CLAUDE.md) for the full session-start protocol,
including how a question is put to the founder (named options, a
recommendation, one at a time).

## Repository layout

```
docs/
  discovery/          Phase I requirements-discovery record (immutable source
                      material) + acquisition provenance
  decision-records/   Unified Decision Record system (record §98); DR-0001…0107
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
  infrastructure.md   What the project runs on (archive server, GitHub, Pages,
                      sessions), where each part is documented, and the
                      known gaps — informal, not a controlled document

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
GLOSSARY.md           Plain-language definitions of archival, preservation,
                      and sanctions-domain terms used across this repo;
                      informal, not a DR-0046 controlled document
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

For what the archive server actually is, what else the project runs on, and what
is not yet in place, see [docs/infrastructure.md](docs/infrastructure.md).

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

0. [GLOSSARY.md](GLOSSARY.md) — plain-language definitions of the archival,
   preservation, and sanctions-domain terms used throughout this repository
   (DR, CDR, OAIS, PREMIS, fixity, WARC, Gate 1/2/3, and more). Keep it open
   while reading everything below.
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
6. [docs/infrastructure.md](docs/infrastructure.md), for what all of this runs on
   and what is not yet in place (backups, scheduled fixity checks, a schema-change
   runbook).

## What needs deciding next

**The board is the list:** https://github.com/users/louisbaudry/projects/7
(its issues live in this repository: https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues)

This section used to carry a hand-maintained numbered list, and it drifted. On
2026-09-22 it still described three sanctions registrations as awaiting
execution, when all three had run on the archive server the day before and
`sources/README.md` said so. Status now has one home; this file keeps the
record instead. See [CLAUDE.md](CLAUDE.md)'s **"Where state lives"**.

Every open item is one issue, labelled on three axes:

| Axis | Values | What it tells you |
|---|---|---|
| `kind:` | `decision`, `execute`, `build`, `blocked-external` | what the item needs — a founder ruling, a person at the archive server or in the real world, a session, or somebody else |
| `epic:` | `legal`, `collection`, `track-a`, `infrastructure`, `governance`, `publication`, `war-facts` | which part of the project it belongs to |
| `size:` | `S`, `M`, `L` | rough cost |

Two views to start from:

- **[Needs a ruling](https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues?q=is%3Aopen+label%3A%22kind%3Adecision%22)** —
  what is waiting on the founder, and nothing else.
- **[On the server](https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues?q=is%3Aopen+label%3A%22kind%3Aexecute%22)** —
  real-world acts no session can perform: executing a registration, checking
  Légifrance from a browser, filing the association's statutes.

A session picking one up proposes named options with a recommendation and
waits for the answer (see [CLAUDE.md](CLAUDE.md)); it does not build against
an assumption. Each is a real fork, not busywork.

This README is an entry point, not the project's institutional memory (record §100).
The authoritative statement of requirements, principles, and phase mandates is the
[Phase I Requirements Discovery Record](docs/discovery/phase-1-requirements-discovery-record.md).
