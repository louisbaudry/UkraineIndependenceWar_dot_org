# Working instructions for Claude

This file governs every AI-assisted session in this repository. Read it whole
before doing anything; it is short relative to what it prevents.
[`AGENTS.md`](AGENTS.md) exists only as a pointer to this file, for tools
that look for that filename specifically — there are no separate
instructions there, and none should be added; a second copy would drift.

## What this repository is

A durable historical evidence and knowledge repository about Ukraine's Second
War of Independence — an archive first, a website last (record §1, Principle
18). Its founding requirements are the immutable
[Phase I record](docs/discovery/phase-1-requirements-discovery-record.md);
every enacted decision since is a Decision Record (DR-0001…0102); the design
lives in SPEC, POL, REQ and METH documents under DR-0046 document control;
the code under `schema/`, `registry/`, `storage/`, `collector/`, `editorial/`,
`publication/`, `export/` and `release/` implements those documents and is
tested against a real PostgreSQL database and real OCFL storage.

Governance is still far ahead of collection, but collection is no longer
theoretical. **The first real collection ran on the archive server on 2026-09-09**
(`eu-consolidated-list`, `ofac-sdn` — five files, ~211 MB, zero failures, zero
documentary assertions, [DR-0093](docs/decision-records/DR-0093-first-source-registrations.md)),
**and as of 2026-09-21 six of the seven sanctions-authority candidates are
registered and collected**; only `ua-nsdc-sanctions` is not, and it is blocked
rather than undecided. The external legal review POL-0001 §10 requires has not
been commissioned, and collection **at scale** stays suspended until it is
(DR-0072, DR-0093 §3).
Do not write "nothing has been collected" or "no live fetch has ever
completed" anywhere — both were true until 2026-09-09 and are not true now.
Check the actual state (`sources/README.md`, `docs/decision-records/README.md`
register, a live `psql` query if you have database access) before repeating
any claim about what has or has not happened; this file is a starting point,
not a substitute for checking.

## Where state lives

Three places, three different things, and everything below depends on not
mixing them:

- **The [project board](https://github.com/users/louisbaudry/projects/7) and [its issues](https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues)**
  — status, ordering, what is in flight, what is blocked and on whom. The
  only thing that changes constantly. One card per open item, labelled on
  three axes: `epic:`, `size:`, and `kind:` — `decision` needs a founder
  ruling, `execute` needs a person at the archive server or in the real
  world, `build` a session can take, `blocked-external` waits on counsel, a registrar or a blocked host.
- **Decision Records, working papers and the SPEC/POL/REQ/METH documents** —
  the decision itself, and the reasoning. Changed by supersession, never in
  place (§77, DR-0046).
- **This file, `README.md` and the component READMEs** — the record of what
  shipped and what it cost to learn. An entry is rewritten once, when its
  work lands.

**One card, one branch, one PR**, whose body says `Closes #NN`. On merge that
closes the issue and moves its card, so the board stays true with nobody
updating it by hand.

**Writing an item's *status* into markdown is the thing not to do.** Move the
card instead. Until 2026-09-22 this file and `README.md` both said three
sanctions sources were "approved but not yet executed" — all six had been
registered and collected on 2026-09-21 (`003b75c`), and `sources/README.md`
said so plainly. Three files, one fact, two of them wrong, and the wrong ones
were the two a session is told to read first. That is the failure this split
exists to prevent, which is why status now has exactly one home.

## Starting a session

1. Read this file, then **the [board](https://github.com/users/louisbaudry/projects/7)** — it is the living
   list of what needs a founder ruling (`kind:decision`), what needs a person
   at the archive server or in the real world (`kind:execute`), what a session
   can pick up (`kind:build`) and what is waiting on somebody else
   (`kind:blocked-external`). Then `README.md`, and the component README of
   whatever you are about to touch. `collector/README.md` says what the
   pipeline does and does not do today; `docs/phase-3/README.md` says where
   Phase III is. [`GLOSSARY.md`](GLOSSARY.md) defines the archival/preservation/sanctions
   vocabulary this file and the DRs assume — the founder has no prior
   background in the domain and is learning it alongside the build, so keep
   it current: when a session introduces or leans on a term a newcomer
   wouldn't know, add it there in the same session, in plain language.
2. Start PostgreSQL and run the suites you will touch **before** editing
   (see "Environment notes"), so you know green from green-because-broken.
3. Check `git log --oneline -15` and the branch you are on. Work happens on
   a fresh `claude/<topic>` branch from `main`; a merged branch is finished.
   **Fetch `origin/main` and diff against it before assuming your branch's
   view of decision-record numbers, `README.md`'s status claims, or the
   collector/registry code is current** — two sessions working in parallel
   on 2026-09-08…10 each drafted an unrelated "DR-0087", discovered only at
   merge time (see DR-0093's numbering note in the DR register). Grep
   `docs/decision-records/README.md` on `origin/main`, not just your branch,
   for the next free DR number.

   **Then look at the branches that are *not* merged.** `origin/main` only
   shows you finished work, so this check is the one that catches another
   session working the same item right now — which `origin/main` cannot, by
   construction:

   ```bash
   git fetch origin -q
   comm -13 <(git branch -r --merged origin/main | sed 's/^ *//' | sort)             <(git branch -r | sed 's/^ *//' | sort)      # unmerged branches
   git diff --stat origin/main...<branch>                # what each is doing
   ```

   Do this **before starting**, not before merging. On 2026-09-14/15 two
   sessions each drafted the WP 3.4 Track A6 legal-review brief at the same
   path, each obtained the same founder ruling, and each took CDR-P3-42 —
   discovered only because the founder asked whether anything was in flight
   (DR-0099/DR-0100, and the DR register's provenance note). If an unmerged
   branch already holds the file you are about to create, the working paper
   you are about to deposit, or the Track A item you are about to start,
   **say so and ask before duplicating it**.
4. If the founder's request touches collection scope, personal data, legal
   posture or a document's status, re-read the "Standing rulings" below
   before proposing anything.

## Track A of WP 3.4 — what it produced

The acquisition strategy's preparatory track (WP 3.4 §4.1), which DR-0071
permits now.

**This table is the record, not the status.** The "Outcome" column states what
an item finished and when — a terminal fact that does not change — and points
at the issue for whatever is still open. Do not write progress here; move the
card. Filter the board on `epic:track-a` for the live view.

| Item | Outcome | Note |
|---|---|---|
| A1 — register the seven sanctions sources and make the first live collection | **six of seven registered and collected**, 2026-09-08 … 2026-09-21; the seventh is [#46](https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues/46) | `eu-consolidated-list` and `ofac-sdn` first (DR-0093, 2026-09-08/09); then `eur-lex-sanctions` (DR-0105), `uk-ofsi-consolidated`, `bis-entity-list` (Denied Persons List half only) and `seco-sanctions` (DR-0096, DR-0098), all on 2026-09-21, each a separate decision executed on the archive server by a person. `eur-lex-sanctions` fetched both foundational instruments cleanly (2 discovered, 2 acquired, 0 failed, 16 199 485 bytes, 0 documentary assertions, run `2eeef589-56aa-430d-af5f-855f5b6775d0`) and carries a **manual per-run re-verification obligation** for its dated-CELEX locator. **Executing it surfaced a real, unrelated operational gap**: the archive server's checkout was on a stale pre-DR-0087 branch and its live database schema was ~10 weeks out of date, because this project has no schema-migration mechanism for a live database — only "drop and rebuild from DDL," which the suites do and a production database holding real data cannot. Resolved by a full backup-then-reload (`pg_dump` full + data-only to a timestamped backup, schema rebuilt from current DDL as the `postgres` superuser, data reloaded past expected DDL-seed-table duplicate-key conflicts), row counts verified identical before and after across every data table; DR-0105's *Executed* section has the sequence. `seco-sanctions`'s real file turned out to live on `sesam.search.admin.ch`, a different host than the main site — found only on a second attempt (2026-09-13). Two `register.py` bugs were caught along the way: dependence on an already-registered source silently dropped under `--only` (fixed 2026-09-12; `sources/tests/test_register.py` 27 → 31 tests), and `--commit` passing **unmerged** candidates to `commit()` after DR-0103 (fixed 2026-09-19 — see A5). Since 2026-09-12 `collector/run.py` records a versioned software agent on preservation events (DR-0097). `ua-nsdc-sanctions` is **blocked, not merely unverified**: its register (`drs.nsdc.gov.ua`) is identified but Cloudflare-challenged from every session that has tried it, live or via a 2026-09-21 Wayback-history check (3 489 captures, no bulk-export file found — suggestive of a search-UI-only application, not confirmed) |
| A2 — census tooling against indices (Common Crawl index, Wayback CDX, citation graphs) | **index tooling done 2026-09-12**, first live query 2026-09-17; the four research sources are [#53](https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues/53) | `sources/census.py` queries Common Crawl's index and Wayback's CDX index for candidate domains, no fetch of any candidate host, no database writes. 28 tests. **Live query succeeded for the first time 2026-09-17**, against `rnbo.gov.ua` (the `ua-nsdc-sanctions` publisher domain) — both `index.commoncrawl.org` and `web.archive.org` were reachable this session, where every prior session's `curl`/`urllib` attempt had failed (`ECONNRESET`/timeout); Wayback returned 25 hosts (including a `sanctions-t.rnbo.gov.ua` subdomain, unexplored), Common Crawl 2. Network access varies by session — this is not a durable fix, just a session where the gap did not hold. The other four A2 evidence sources (Wikipedia citation graphs, sanctions link graphs, OSINT lists, bibliographies) are not built — editorial research tasks, not tooling. DR-0094 (approved 2026-09-11) still governs how a *retrieved* third-party capture gets recorded — that's the separate acquisition_attempt/FetchResult extension, not started |
| A3 — WARC bulk-ingest path | **done 2026-09-09** | `Collector.ingest_warc`; live `warc` sources wrapped as WARC records; CDR-P3-35 still a candidate |
| A4 — WACZ evaluation (DR-0006 standing task) | **done 2026-09-15** | [WP 3.6](docs/phase-3/working-papers/wp-3.6-wacz-evaluation.md) (CDR-P3-42 candidate): the container spec is stable (v1.1.1) but its signing layer is a pre-1.0 working draft (v0.1.0), confirmed by live retrieval of both spec texts and PyPI release metadata for `wacz`/`authsign`/`wacz-signing`. Recommends **deferring** adoption of both, WARC via `collector/pipeline.py` unchanged, on two stated triggers; the "jurisdictionally meaningful" half of DR-0006's question is flagged as unanswerable from a spec alone, not resolved |
| A5 — registration classes ([DR-0103](docs/decision-records/DR-0103-registration-classes.md)) | **done 2026-09-16; enacted 2026-09-16** | Option A implemented: classes defined in YAML, sources reference and inherit policy defaults, merged at registration time. `sources/register.py` extended with `load_candidates()` class extraction, `merge_class_defaults()` inheritance, and validation support; `describe()` shows class membership. `sources/tests/test_register_classes.py` has 18 tests covering inheritance, overrides, validation, and error handling — all passing. All 7 candidates validate successfully. Authorization scale reduced from thousands per-source to tens per-class plus exceptions; decision load reduced from months to days for foundational corpus (DR-0103 §8). The merged PR deposited its design paper as `wp-3.5-registration-classes.md`, colliding with the already-taken WP 3.5 (identifier design) — enacting DR-0103 renumbered it to [WP 3.7](docs/phase-3/working-papers/wp-3.7-registration-classes.md) and added the deposit's missing `docs/phase-3/README.md` row and `PROVENANCE.md` entry (see `docs/decision-records/README.md`'s provenance note on DR-0103). CDR-P3-32 discharged by DR-0103. **Initial classes named 2026-09-17**: the founder ruled the grouping principle — jurisdiction first, topic second, matching WP 3.7 §7's recommendation — and all seven `sanctions-authorities.yaml` sources now reference a class; four needed explicit overrides (`capture_format`, `rights_permission`) where the class default would otherwise have silently changed an already-verified or DR-approved value (`sources/README.md`'s "Registration classes" section has the full account, including a regression this pass fixed: `eu-consolidated-list` had silently inherited `capture_format: warc` from its class against its DR-0093-verified `http`). **2026-09-19 — a second, more serious regression found and fixed**: `load_candidates()`'s three-value return (DR-0103) broke every other caller still unpacking two — `sources/tests/test_register.py`, `collector/tests/test_run.py`, and `collector/run.py`'s `find_candidate()` — leaving `main`'s full test suite (`sources/tests/test_register.py`, `collector/tests/test_run.py`, `release/tests/test_baseline.py`, `export/tests/test_dump.py`) unable to even run (`ValueError`/`TypeError` on import or setup). Worse, `sources/register.py`'s own `main()` `--commit` path passed the **unmerged** `sources` to `commit()`, which reads required fields (`default_retention_tier`, `rights_permission`, etc.) directly off each dict — since all seven real candidates now reference a class, `register.py --commit` would have crashed on the archive server the first time anyone actually executed one of the three approved-but-unexecuted registrations. Fixed: `find_candidate()` now merges before returning; `main()`'s `--commit` path uses the same merged view `describe()` already computed; the four affected test files were updated to work against merged sources (with `class` popped, so mutation tests that remove a field can't have it silently restored from the class). All 14 test suites pass again (`sources/tests/test_register.py` 32/32 — including a new end-to-end `--commit` check shown to fail under sabotage — `collector/tests/test_run.py` 21/21, `collector/tests/test_pipeline.py` 44/44, `release/tests/test_baseline.py` 27/27, `export/tests/test_dump.py` 31/31, `sources/tests/test_register_classes.py` 8/8, plus the rest unaffected). `release/tests/test_baseline.py` and `export/tests/test_dump.py` also carried an unrelated, separately-introduced bug (constructing `Collector` without the `software_agent_id` positional argument DR-0097 added) — fixed the same way. **A separate session independently rediscovered the same `--commit` bug on 2026-09-20**, unaware of the fix above (its own branch was cut before 2026-09-19's merge to `main`) — see A1's note; merging the two branches kept the more thorough 2026-09-19 fix and discarded the redundant duplicate. The class mechanism was then used for all four remaining A1 registrations on 2026-09-21, on the archive server, by a person, per source |
| A6 — legal-review brief (WP 3.4 §7) | **done 2026-09-15** (brief v0.4); the engagements and the Légifrance check are [#40](https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues/40)–[#43](https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues/43) | [`docs/legal/legal-review-brief.md`](docs/legal/legal-review-brief.md) — a brief, not a policy, not a DR-0046 controlled document, not legal advice. Part A = POL-0001 §10's six topics as Q1–Q6 (it does **not** narrow or reinterpret §10); Part B = WP 3.4 §7's five questions as Q7–Q11 plus Q12 on hosting. **Jurisdiction France; controller the founder as a natural person; host IONOS, Spain** (`DR-0100`, approved — CDR-P3-43 discharged). **CDR-P3-44 also discharged 2026-09-15**, into `DR-0101`; **CDR-P3-45 held** with a named trigger (the start of Gate 3 work), so the brief has no open proposals. Rulings of 2026-09-15: **two engagements** — Part A to French data-protection counsel now, Part B held for IP/media counsel, travelling with the sent brief as context not instructions (§9.5); and **counsel answers for both states in §3.5** — the project as it is and as it intends to be — **naming the deltas**, which CDR-P3-44 requires recorded as named POL-0001 §11 review triggers (§9.4, §8). Governance consequence of the split: **§10 is satisfied by Part A alone**, so Part A's advice supersedes DR-0072 and lifts §9's suspension, while Q8/Q9/Q10's acquisition steps stay unauthorised until Part B is answered **whatever Part A concludes** — a released §9 is not a licence to run all of Track B. **As of 2026-09-19, Part A has been sent to counsel and no response has been received yet** — DR-0072's suspension remains in effect; nothing changes until a DR superseding DR-0072 records counsel's advice (that recording act, not receipt of advice, is what lifts §9). **Outstanding, not a decision:** the brief quotes **LIL Arts. 46, 78, 79, 80** from the CNIL's consolidated text (fetched 2026-09-15) because Légifrance returned a 403 anti-bot challenge; **four independent sessions (2026-09-15, 2026-09-18 ×2, 2026-09-19) have since retried Légifrance and all four got the same 403** — see [`docs/sources/verification-lil-articles.md`](docs/sources/verification-lil-articles.md) for the full attempt log. Verification against Légifrance itself is still outstanding and needs human-assisted (browser) access; it should be completed before counsel returns advice, per that document. The drafting surfaced that Art. 46 limits criminal-offence processing to a closed list this project does not obviously sit in, while Art. 80 disapplies Art. 46 for university/literary expression and professional journalism — putting POL-0001 §8.3's "archiving primary, expression secondary" ruling genuinely in question. Flagged to counsel as a question, never answered here |
| A7 — storage and bandwidth measurement | **tooling done 2026-09-15**; execution is [#54](https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues/54) and [#55](https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues/55) | `storage/measure.py` reads `collector_run` for recorded bytes/throughput and walks the OCFL roots and quarantine directory for actual on-disk footprint, including the duplication ratio from `collector/README.md`'s undischarged-quarantine-copy gap. 11 tests, against fixture data only — not yet run against the archive server's real database, so WP 3.4 §5.3's real numbers are still outstanding. [`docs/runbooks/A7-storage-bandwidth-measurement.md`](docs/runbooks/A7-storage-bandwidth-measurement.md) gives the archive-server steps for both halves of A7 (baseline measurement of the two A1 sources, and one retrospective WARC pull via `Collector.ingest_warc` for a registered domain, WP 3.4 §4/CDR-P3-35) — a session did not execute it, since the retrospective pull is new acquisition needing a person as agent of record (DR-0093 §3) on the archive server, not something decided unilaterally from here |

Track B (WP 3.4 §4.2) does not start until DR-0072's successor records the
POL-0001 §10 review.

## How to ask the founder a question

**This is the standing instruction for every question, without exception.**

When anything needs a decision from the founder/principal editor:

1. **One question at a time.** Never batch questions into a single message.
   Ask, wait for the answer, then ask the next.
2. **Propose multiple concrete choices.** Not "what would you like to do?" —
   named options, each with what it means and what it costs.
3. **State a recommendation.** Say which option is best and why. A menu with
   no recommendation pushes the analysis back onto the founder, which is the
   opposite of the point.
4. **Give enough context to answer without scrolling back.** The question
   should be answerable on its own terms.

This applies to Decision Records, specification choices, policy rulings,
methodology questions, branch and merge decisions, and ordinary implementation
forks alike. It is not reserved for large decisions.

### Why

Record §78–79: the founder is final editorial authority, and AI proposes
while humans decide. A proposal with no options is not a proposal, and a set
of options with no recommendation is not analysis. Asking one at a time keeps
each decision separable and separately recorded — which is what the Decision
Record system requires.

### What does not need a question

Routine judgment calls within work already directed: naming, file layout,
test structure, wording of code comments, which of two equivalent
implementations to use. Make the call, mention it, and move on. Reserve
questions for choices that would change what gets built or what the project
commits to.

### Standing rulings to remember

- **2026-09-08 — no collection scale-up before the POL-0001 §10 legal review
  is recorded** (option C of three put to the founder; see WP 3.4 §1.3).
  Preparatory work that collects nothing, or collects only from registered
  sources with configured scope, may proceed (WP 3.4 Track A).
- **Open-web crawling is excluded**, before and after the review: DR-0071(a)
  now, POL-0001 §9(a) afterwards. The acquisition strategy is census,
  retrospective recovery from existing archives, registered live collection
  (WP 3.4, candidate). Do not propose a crawler.
- **Six of the seven sanctions authorities in `sources/candidates/` are
  registered and collected**: `eu-consolidated-list`, `ofac-sdn` (DR-0093,
  2026-09-08/09); `eur-lex-sanctions` (DR-0105), `uk-ofsi-consolidated`,
  `bis-entity-list` (Denied Persons List half only) and `seco-sanctions`
  (DR-0096, DR-0098) — all four of those on **2026-09-21**. **Each was a
  separate decision, not linked to the others.** Execution is on the archive
  server, per each record's *How to execute* — this is not a session-side
  task, and running `register.py --commit` in an interactive session's own
  throwaway database is not the same thing as executing it.
  **Executing DR-0105 surfaced a real operational gap**: the archive
  server's database schema had drifted ~10 weeks behind `main`
  (this project has no schema-migration mechanism for a live database).
  Resolved by a full backup-then-reload, verified lossless — see DR-0105's
  *Executed* section. The archive server's schema is current as of
  2026-09-21, so that blocker is not standing, but **writing an actual
  runbook for schema drift is an open founder decision** —
  [#57](https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues/57).
  **One remains a candidate**, blocked rather than merely unverified:
  `ua-nsdc-sanctions` — its register (`drs.nsdc.gov.ua`) is identified but
  Cloudflare-challenged from every session that has tried it —
  [#46](https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues/46).
  Registering it, or re-verifying/re-registering any of the six decided
  sources, is still the founder's act, per source — do not run
  `register.py --commit` against the real archive database without that
  being asked for, and do not treat approval of one registration as
  authorization for any other source.
- **2026-09-20 — the project has started forming a legal entity: an
  association loi 1901.** Resolves the "whether the project should form a
  legal entity" question this file's own standing ruling below had left
  open since 2026-09-14/15. Chosen over another French form or a
  non-French entity (which would have reopened the interim-jurisdiction
  ruling below), started **in parallel with**, not conditional on, French
  data-protection counsel's still-pending Part A response
  (`DR-0104`). **This is a decision to proceed,
  not a completed formation** — statutes, filing with a préfecture, a
  SIRET, and a first general assembly are real-world acts no session can
  perform. **The controller stays the founder as a natural person**
  (`DR-0100` Decision 2) until the association legally exists and takes
  over; that handover is itself a POL-0001 §11 material-change review,
  recorded separately when it happens, not assumed by this ruling.
- **2026-09-14/15 — the project's establishment jurisdiction is FRANCE, and
  the ruling is explicitly INTERIM.** Named 2026-09-14 as the founder's own
  personal jurisdiction in the absence of any incorporated or registered
  legal entity (`DR-0099`, which amended
  POL-0001 to v1.1 so §10 names it; **POL-0001 is now at v1.2**, whose §10
  names DR-0100 and restates the jurisdiction, controller and hosting facts
  in the policy itself); **confirmed and extended 2026-09-15**
  by `DR-0100`, which keeps the
  interim framing and adds that **the controller is the founder/principal
  editor as a natural person** and **the archive server is hosted with IONOS
  in SPAIN**. *Interim* means it identifies applicable law and counsel, not
  that a formal entity exists. **Whether the project should form a legal
  entity before or as part of commissioning the §10 review is a separate,
  still-open question — do not treat naming France as having answered it.**
  The applicable framework is the GDPR as applied in France plus the **Loi
  n° 78-17 du 6 janvier 1978 (LIL)**; the expected supervisory authority is
  the **CNIL**. Both ends are in the EEA, so no Chapter V transfer question
  arises from the hosting; an **Art. 28 processor contract with IONOS** is an
  outstanding administrative check, not a legal question. Later
  incorporation, or a change of jurisdiction or hosting country, is a
  **material change under POL-0001 §11** and triggers a recorded review,
  including a reassessment of the §10 legal review if obtained by then.
  **Caution for future sessions:** reading the LIL's Arts. 46/78/80 against
  what this archive holds puts POL-0001 §8.3's "archiving primary, expression
  secondary" ruling in genuine question. Do **not** resolve that here — it is
  the central thing the §10 review is being commissioned to answer, and no
  session should restate §8.3 as settled without flagging it.
- **2026-09-15 — "recorded", in POL-0001 §10, means one specific act**
  (`DR-0101`, approved). The review is recorded
  **only** by a Decision Record superseding DR-0072 that carries POL-0001 to
  v2.0 in the same act; **§9's releases take effect on that record's approval
  and not before** — not on receipt of counsel's advice, not on the founder
  reading it, not on a commit or a merge. **§10 is discharged by Part A of
  the brief alone**; Part B's answers supersede nothing and move neither
  DR-0072 nor LEGAL-009, while still gating Q8/Q9/Q10's acquisition steps
  whatever Part A concludes. A **failed or partial** review is recorded too,
  as a record that supersedes nothing — an unanswered review must not look
  like one nobody commissioned. A session that receives the advice follows
  that record; it does not re-decide what recording means.
- **A person, not software, is the agent of record for a collection run**
  (DR-0093 §3) — deliberately, at the founder's direction, for the first
  runs. Unchanged. As of 2026-09-12
  (`DR-0097`), a *second*,
  separate, self-registering software agent named `collector-pipeline` is
  recorded on the run's preservation events instead, which resolved
  `release/baseline.py --check`'s inability to pin `collector_version`/
  `pipeline_version` without touching `collector_run.collector_agent_id` or
  the Gate 1 decision. Do not resolve the *agent-of-record* question
  unilaterally by quietly switching it back to software — that would
  reverse a founder ruling, and is a different question from which agent a
  preservation event names.

## Governance context

- The [Phase I record](docs/discovery/phase-1-requirements-discovery-record.md)
  is immutable source material. Changes happen by supersession, never in-place
  edits (§77).
- Every enacted decision is a [Decision Record](docs/decision-records/README.md).
  Drafts are proposed and marked as such; nothing is enacted unilaterally.
- **An approved Decision Record changes by supersession, not by editing it**
  (§77, DR-0046). The one exception is narrow and enacted
  (DR-0102 Decision 7): a record may be
  revised in place only when **all four** hold — approved and revised in the
  **same session**, **never merged to `main`**, **the founder ruled the
  change**, and a **Revision note quotes the replaced text in full** with its
  date and reason. "Not merged yet" is a bound on the blast radius, **not the
  reason**: never infer from Git state alone that a record is open to
  revision, which is the same inference DR-0046 forbids for status. When in
  doubt, supersede.
- Controlled documents (DR, SPEC, POL, REQ, METH, PROC) carry explicit status
  under [DR-0046](docs/decision-records/DR-0046-unified-document-control.md).
  **Status is document metadata, never inferred from Git state** — a commit is
  not an approval, and a merge is not an enactment.
- AI-drafted documents carry an **AI provenance** note per §80 and remain
  candidates until the founder approves them.

## Documents: where things go and how they are made

**Decision Records** live in `docs/decision-records/DR-nnnn-slug.md` with the
header block, Context, Alternatives considered, Decision, Consequences; the
register in that directory's README lists every DR. **Never write a number
while drafting** (DR-0095, extended by DR-0102) —
two branches checking the register and drafting concurrently can both be
right and still collide, as DR-0093 and DR-0094 each did. Draft and review it as `docs/decision-records/DR-pending-slug.md`,
titled `DR-pending-slug` throughout (header and any self-reference); the
real number is assigned exactly once, at merge time, by grepping
`origin/main`'s register for the highest `DR-nnnn`, taking the next integer,
renaming the file, fixing its title/self-references, and adding its register
row in the same commit that completes the merge. A DR is written only when
the founder has decided; before that it is a **candidate DR** inside a
working paper.

**Working papers** (`docs/phase-3/working-papers/wp-3.N-slug.md`) are how
studies reach the founder. Follow WP 3.3 as the model: header block (Project,
Status `CANDIDATE — AI-drafted, awaiting founder review`, Version, Mandate,
Constraints inherited), an **AI provenance** block stating what was and was
not verified, numbered sections, a "Candidate Decision Records" section, "Open questions
raised", "Sources".

**Candidate DRs are drafted unnumbered, like Decision Records**
(DR-0102, superseding DR-0095): write
**`CDR-pending-<slug>`** throughout the paper and in anything on the same
branch that cites it. **The real `CDR-P3-nn` is assigned at merge**, by
grepping `docs/` on `origin/main` for the highest one and taking the next
integers in the order the paper lists them. CDR numbers are a **single global
sequence**, not scoped per paper — two papers drafted the same week collide by
construction, as WP 3.4/WP 3.5 did and WP 3.6 and the A6 brief did again.

On deposit:

1. compute `sha256sum` of the file **after its CDR numbers are assigned**, so
   the hash covers the text as merged, and add an entry to
   `docs/phase-3/working-papers/PROVENANCE.md` (Title, Version, SHA-256 at
   deposit, Deposited, Origin, Inputs, Status);
2. add a row to the table in `docs/phase-3/README.md`;
3. if the paper is later corrected, keep the original hash and add the new
   one with the reason (see WP 3.1's entry) — never silently.

**SPEC / POL / REQ / METH** are controlled documents: version, status,
approval and effective dates, supersession links, change history, and a
provenance table in their directory README. A draft is v0.1; approval makes
it v1.0 with the status block and an enactment note as the only changes.

**Informal source notes** go in `docs/sources/` as prose; **candidate
registrations** go in `sources/candidates/*.yaml` against the DR-0067 schema
with the reasoning for each judgment in `sources/README.md`. Neither
registers anything.

**Code that implements a candidate DR says so** in its module docstring and
README ("CDR-P3-35, candidate — if the founder amends it, this changes with
it"), so nobody mistakes built for decided.

## Code conventions

- **Python 3.11, standard library plus `psycopg` and `PyYAML`** — exactly
  what `setup/install.sh` installs. Adding a runtime dependency is a decision
  for the founder, not a convenience. (The WARC reader/writer is stdlib for
  this reason; `warcio` is used only as a test-time cross-check when present.)
- **The schema is rebuilt from DDL, not migrated.** Edit `schema/0N-*.sql`
  directly; suites drop and recreate their databases. Enumerations are
  **generated from the registry** (`schema/01-enums-generated.sql` via
  `schema/gen_enums.py`; DR-0078) — never hand-edit them; change the
  vocabulary YAML and regenerate.
- **Tests are plain scripts**, one per component under `*/tests/`, printing
  `PASS`/`FAIL` lines that each **name the requirement or DR verified**
  (`check("DR-0074", "…", condition)`, `rejects(...)` for refusals). No test
  framework. Suites touching the store take `PGHOST`/`PGPORT`/`PGUSER`.
- **A suite must be shown to fail.** After writing tests, sabotage the rule
  under test one rule at a time, watch the suite go red, restore, and record
  the sabotages in the component README. Back up the file with `cp` first and
  restore with `cp`. **Never restore with `git checkout <file>` while the file
  carries uncommitted work** — it reverts everything, not just the sabotage.
- **Policy is enforced in code and in the database.** When a rule matters
  (registered sources only, admission needs a clean security check, tiers are
  declared not derived), the constraint lives in the DDL *and* the code checks
  it, and a test proves the DDL refuses what the code would if the code were
  wrong.
- **Failures are recorded, not raised away.** Fetch results, acquisition
  attempts, preservation events and collector runs carry failures as
  first-class outcomes with an explanation (§28, PRES-007). A bad input is
  part of the coverage record, not a crash.
- **Two-system writes go storage-first**: write the OCFL object, then the
  database rows; an orphaned object is detectable, a holding pointing at
  absent bytes is a false claim (§26).
- Module and function docstrings cite the record § and DRs they implement.
  Comments explain *why* a rule exists, not what the line does.

## Policy guardrails the code must keep

Whatever you build, these hold, and a test should prove each one that your
change could break:

- **Registered, active sources only** (DR-0071(a), DR-0067). An unregistered
  locator is out of policy, not merely unknown. Out-of-scope material is
  counted and **not written down**.
- **Collection creates no canonical knowledge** (DR-0066, Principle 5): zero
  documentary assertions, zero evidence relations from any collector run.
  Gate 2 and Gate 3 are human decisions at a risk tier and are not automated.
- **No automatic structuring of personal data** (DR-0071(b), POL-0001 §4),
  and never of the special-category list, for any person category.
- **Source grades are triage only** (DR-0027). No query computing an
  assessment may read a grade.
- **Acquisition source ≠ original publisher** (§28). Bytes recovered from an
  external archive record the archive and its capture time, distinct from
  ours.
- **The registry's capture format is honoured** (DR-0006, DR-0067): a `warc`
  source gets a WARC record, an `http` source a bare body recorded as such.
- **Preserve / structure / publish are three independent decisions**
  (POL-0001 §1); access tiers are declared, never derived from an ordering
  (DR-0086); redaction is the sole immutability exception (DR-0077).
- **Never claim legal chain of custody** (DR-0008, LEGAL-007).

## Environment notes for agent sessions

- **Network access varies by session — check, do not assume from this file.**
  Some sessions' proxies deny general internet hosts entirely; the session
  that authored most of this file had no such access. The session that
  performed the 2026-09-08 verification and 2026-09-09 first collection
  could reach the specific publishers it needed (`eur-lex.europa.eu`,
  `webgate.ec.europa.eu`, `treas.gov` domains) but not others it tried
  (`web.archive.org`, `kse.ua`, `rusi.org`). Test the actual locator with
  `curl` before writing "cannot be verified from here" — and if you do write
  it, name what you actually tried, per
  [docs/sources/verification-eu-consolidated-list-ofac-sdn.md](docs/sources/verification-eu-consolidated-list-ofac-sdn.md)'s
  style.
- **PostgreSQL 16 is installed but the cluster is down** at session start:

  ```bash
  pg_ctlcluster 16 main start
  # allow local socket connections without a password, then:
  export PGUSER=postgres PGHOST=/var/run/postgresql
  pip install "psycopg[binary]"        # python3-psycopg is absent in the image
  ```

  If `psql` refuses peer authentication, change `peer` to `trust` for local
  connections in `/etc/postgresql/16/main/pg_hba.conf` and reload.
- `warcio` can be pip-installed for the WARC cross-check tests; it is not a
  project dependency and its absence is reported as a skip.
- Use the session scratchpad for backups and throwaway files, never the repo.
- `registry/validate.py` runs without arguments and must report
  `0 error(s)` after any vocabulary change; regenerate the enum DDL after it.

## Git and pull requests

- Work on a `claude/<topic>` branch from the latest `main`. The founder opens
  pull requests from the Claude Code UI and merges them; **do not open a PR
  unless asked**, and do not merge unless asked.
- Once a branch's PR is merged, follow-up work goes on a **new** branch from
  `main`; never stack commits on merged history.
- Merge commits, never rebase or force-push a branch the founder has seen.
- Commit messages say what changed and why, cite the DRs and record sections
  involved, and state what was verified and what was not. The message is part
  of the project's memory.
- Nothing in a commit, document or code comment names the AI model; the
  provenance block's "AI assistant (Anthropic Claude Code agent session)" is
  the established form.

## Reporting work

State what was verified and what was not. A test suite that has never been
seen to fail proves nothing — when a suite is added, check that it fails when
the thing it tests is broken, and say so. Where something could not be
verified in this environment (no network access to a live source, no external
legal review), say that plainly rather than implying it away.

Lead with the outcome. Give test counts in a table, not in prose. Name the
files a reader must open and describe the rest in words. End with the one
question the founder must answer next, with options and a recommendation.
