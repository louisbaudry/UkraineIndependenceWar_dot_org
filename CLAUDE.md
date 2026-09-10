# Working instructions for Claude

This file governs every AI-assisted session in this repository. Read it whole
before doing anything; it is short relative to what it prevents.

## What this repository is

A durable historical evidence and knowledge repository about Ukraine's Second
War of Independence — an archive first, a website last (record §1, Principle
18). Its founding requirements are the immutable
[Phase I record](docs/discovery/phase-1-requirements-discovery-record.md);
every enacted decision since is a Decision Record (DR-0001…0086); the design
lives in SPEC, POL, REQ and METH documents under DR-0046 document control;
the code under `schema/`, `registry/`, `storage/`, `collector/`, `editorial/`,
`publication/`, `export/` and `release/` implements those documents and is
tested against a real PostgreSQL database and real OCFL storage.

Governance is far ahead of collection. **Nothing has been collected, no source
is registered, no live fetch has ever completed, and the external legal review
POL-0001 §10 requires has not been commissioned.** Do not write anything, in
code or prose, that implies otherwise.

## Starting a session

1. Read this file, then `README.md`, then the component README of whatever
   you are about to touch. `collector/README.md` says what the pipeline does
   and does not do today; `docs/phase-3/README.md` says where Phase III is.
2. Start PostgreSQL and run the suites you will touch **before** editing
   (see "Environment notes"), so you know green from green-because-broken.
3. Check `git log --oneline -15` and the branch you are on. Work happens on
   a fresh `claude/<topic>` branch from `main`; a merged branch is finished.
4. If the founder's request touches collection scope, personal data, legal
   posture or a document's status, re-read the "Standing rulings" below
   before proposing anything.

## Track A of WP 3.4 — what is done and what is not

The acquisition strategy's preparatory track (WP 3.4 §4.1), which DR-0071
permits now. Keep this list current when you finish or start an item.

| Item | State | Note |
|---|---|---|
| A1 — register the seven sanctions sources and make the first live collection | **waiting on the founder and on network access** | `sources/register.py --commit` is the founder's act; `HttpFetcher` has never completed a live fetch |
| A2 — census tooling against indices (Common Crawl index, Wayback CDX, citation graphs) | not started | must not live-fetch unregistered hosts |
| A3 — WARC bulk-ingest path | **done 2026-09-09** | `Collector.ingest_warc`; live `warc` sources wrapped as WARC records; CDR-P3-35 still a candidate |
| A4 — WACZ evaluation (DR-0006 standing task) | not started | from specifications only; say so |
| A5 — registration classes (CDR-P3-32) | not started | changes how authorisation is granted; founder ruling first is preferable |
| A6 — legal-review brief (WP 3.4 §7) | not started | a brief, not a policy; not legal advice |
| A7 — storage and bandwidth measurement | not started | needs A1 |

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
- **The seven sanctions authorities in `sources/candidates/` are candidates**,
  not registered. Registering is the founder's act, per source.

## Governance context

- The [Phase I record](docs/discovery/phase-1-requirements-discovery-record.md)
  is immutable source material. Changes happen by supersession, never in-place
  edits (§77).
- Every enacted decision is a [Decision Record](docs/decision-records/README.md).
  Drafts are proposed and marked as such; nothing is enacted unilaterally.
- Controlled documents (DR, SPEC, POL, REQ, METH, PROC) carry explicit status
  under [DR-0046](docs/decision-records/DR-0046-unified-document-control.md).
  **Status is document metadata, never inferred from Git state** — a commit is
  not an approval, and a merge is not an enactment.
- AI-drafted documents carry an **AI provenance** note per §80 and remain
  candidates until the founder approves them.

## Documents: where things go and how they are made

**Decision Records** live in `docs/decision-records/DR-nnnn-slug.md` with the
header block, Context, Alternatives considered, Decision, Consequences; the
register in that directory's README lists every DR. Next free number: check
the register, never assume. A DR is written only when the founder has decided;
before that it is a **candidate DR** inside a working paper.

**Working papers** (`docs/phase-3/working-papers/wp-3.N-slug.md`) are how
studies reach the founder. Follow WP 3.3 as the model: header block (Project,
Status `CANDIDATE — AI-drafted, awaiting founder review`, Version, Mandate,
Constraints inherited), an **AI provenance** block stating what was and was
not verified, numbered sections, a "Candidate Decision Records" section
numbered **CDR-P3-nn** continuing from the last one used anywhere in `docs/`
(grep for it), "Open questions raised", "Sources". On deposit:

1. compute `sha256sum` of the file and add an entry to
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

- **No general network access.** The proxy denies general internet hosts. No
  external source, archive or tool can be verified from here; say so in every
  document and README where it matters, as existing ones do.
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
