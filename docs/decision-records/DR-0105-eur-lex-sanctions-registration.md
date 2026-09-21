# DR-0105 — Fourth source registration: EUR-Lex restrictive measures (Ukraine/Russia)

**Category:** operations / preservation | **Status:** Approved | **Decided:** 2026-09-21 by founder/principal editor
**Origin:** founder's direction of 2026-09-21 ("approve it now"), following the 2026-09-20 verification record and the same day's two scope rulings (both instruments in `run_locators`; manual per-run re-verification) | **Supersedes:** — | **Superseded by:** —

> **AI provenance (§80).** Drafted by Claude (model: `claude-sonnet-5`) on
> 2026-09-21 at the founder's direction, and **approved by the founder the
> same day**, matching DR-0096/DR-0098's pattern. Approval is what
> authorises the registration described below; the registration itself is
> executed on the archive server by the founder, per *How to execute*, and
> has not been executed by this record.

## Context

`eur-lex-sanctions` was verified 2026-09-20: the two foundational
instruments — Council Regulation (EU) No 269/2014 (CELEX `32014R0269`,
Annex I carries the designated-persons list) and Council Decision
2014/145/CFSP (CELEX `32014D0145`) — identified by following EUR-Lex's own
"Consolidated texts" links, fetched, and acquired end to end by the real
collector into a throwaway database (2 discovered, 2 acquired, 0 failed,
16 196 543 bytes, 0 documentary assertions)
([verification record](../sources/verification-eur-lex-sanctions.md)). Two
open questions that record flagged were both ruled by the founder the same
day, one at a time: `run_locators` keeps both instruments, not the
Regulation alone; and the dated-CELEX consolidated-text locator (which
advances roughly monthly as the Council amends the regime) is re-verified
manually before each collection run, the same agent-of-record model every
other source already uses (DR-0093 §3) — no new tooling built for this.

`eur-lex-sanctions` declares one dependence in
`sources/candidates/sanctions-authorities.yaml`:
`eu-consolidated-list --derives-from--> eur-lex-sanctions`. The "from" end
(`eu-consolidated-list`) is already registered (DR-0093); the "to" end
(`eur-lex-sanctions`) is what this record registers. This is the same
cross-batch dependence-resolution case DR-0096 found `register.py --commit`
silently dropping and DR-0098 confirmed the fix on: registering
`eur-lex-sanctions` alone, in a `--only eur-lex-sanctions` call, must still
resolve and record the dependence against the already-registered
`eu-consolidated-list`.

`eur-lex-sanctions`'s rights position is inherited from its
`EU-institutional-sanctions` class: `may-redistribute`, the same
institutional-publisher default `eu-consolidated-list` already carries —
no per-source override needed, unlike `bis-entity-list`, `seco-sanctions`
and `ua-nsdc-sanctions`, whose unverified rights positions needed the
conservative `may-preserve` override (`sources/README.md`, "Registration
classes"). Registering it also commits the project to French/German
reading capacity at Gate 2 (`primary_languages: [en, fr, de, uk]`, DR-0081)
— already committed by `seco-sanctions` (French, German) and
`eu-consolidated-list`/`uk-ofsi-consolidated` (English), so this adds
nothing new on that front; Ukrainian stays the one outstanding commitment,
pending `ua-nsdc-sanctions`.

## Alternatives considered

1. **Register `eur-lex-sanctions` now, as verified and scoped** (chosen).
   Same rigor as the four sources before it (`eu-consolidated-list`,
   `ofac-sdn`, `uk-ofsi-consolidated`/`bis-entity-list`, `seco-sanctions`);
   both of its open scope questions were resolved the same session by the
   founder, so nothing about the registration would be provisional.
2. **Hold until `ua-nsdc-sanctions` is also resolved**, registering the
   last two sanctions-authority candidates together. Rejected, matching
   DR-0098's reasoning for `seco-sanctions`: the founder's direction was to
   approve this one now, §78's per-source acceptance does not require
   batching, and `ua-nsdc-sanctions` is blocked on a Cloudflare challenge
   with no resolution estimate — waiting on it would hold a ready source
   hostage to an unrelated blocker.
3. **Hold until the dated-CELEX cadence question had a tooling answer**
   rather than a manual-process answer. Rejected: the founder ruled manual
   re-verification is sufficient, matching how every other source's
   locator freshness is actually handled (a person, before a run) — this
   was not a blocking engineering gap, just an unasked question.

## Decision

On approval:

1. **`eur-lex-sanctions` is registered** into the source registry with the
   field values in the candidate file as of this record's approval,
   by `sources/register.py --commit --only eur-lex-sanctions`. Accepted
   individually (§78), matching precedent.
2. **The declared dependence on `eu-consolidated-list` is recorded by this
   registration**, automatically, by the same `--commit` call — no manual
   SQL needed, confirmed in *How to execute*.
3. **`run_locators` carries both instruments** (CELEX `02014R0269-20260807`
   and `02014D0145-20260807` as of the 2026-09-20 verification) — the
   founder's 2026-09-21 ruling, over the Regulation alone.
4. **Whoever runs the collector against this source re-verifies the dated
   CELEX suffix first**, each time, before the run — the founder's
   2026-09-21 ruling on cadence. A stale dated CELEX in `run_locators` is
   expected to happen between registration and any given run; re-checking
   it is part of preparing that run, not a defect in this registration.
5. **A first collection run is a separate act**, not authorised by this
   record alone. `--dry-run` first (after re-verifying the CELEX suffix
   per Decision 4), then a manual run with a person as agent of record,
   per the established pattern, left to whoever executes this record at
   whatever pace is wanted.
6. **Nothing from any future run crosses Gate 2** (DR-0066, Principle 5),
   unchanged from every other registered source.
7. The registration carries the obligations `register.py --dry-run`
   prints: permanent retention with DR-0005 fixity checking; French/German
   reading capacity, already committed by prior registrations, unaffected;
   and the `may-redistribute` rights position inherited from the
   `EU-institutional-sanctions` class, unchanged by this record.
8. **This decision is independent of `ua-nsdc-sanctions`.** Registering
   this source neither requires nor authorises anything about the other,
   still-blocked candidate.

### How to execute

On the archive server, with the same database and archive root prior
registrations used (`uiw` and `~/uiw-archive` unless the install used
different names). Reuse the person `pipeline_agent` id DR-0093's step 1
already created, unless a different person is registering this time.
**Before running `--dry-run` or `--commit`, re-fetch
`https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32014R0269` and
`.../CELEX:32014D0145` to confirm the current dated consolidated CELEX is
still `20260807`** — if the Council has amended the regime since
2026-09-20, update `run_locators` in
`sources/candidates/sanctions-authorities.yaml` to the new dated CELEX
before proceeding (Decision 4).

```bash
# 0. re-verify the dated CELEX suffix is still current (Decision 4) --
#    see the instruction above this block.

# 1. register — this is the authorisation, and it collects nothing.
#    the declared eu-consolidated-list -> eur-lex-sanctions dependence is
#    recorded automatically by this call.
python3 sources/register.py --check
python3 sources/register.py --dry-run --only eur-lex-sanctions
python3 sources/register.py --commit --dbname uiw \
        --agent <the person agent id from DR-0093's step 1, or a new one> \
        --only eur-lex-sanctions

# 2. confirm the dependence was recorded:
psql -d uiw -c "SELECT s1.name, s2.name, sd.relation FROM source_dependence sd \
  JOIN source s1 ON s1.id=sd.dependent_id JOIN source s2 ON s2.id=sd.depends_on_id \
  WHERE s2.name = 'EUR-Lex — restrictive measures (Ukraine/Russia)'"

# 3. a first run, when wanted -- --dry-run first
python3 collector/run.py --source eur-lex-sanctions --dbname uiw \
        --agent <agent id> --archive-root ~/uiw-archive --dry-run
python3 collector/run.py --source eur-lex-sanctions --dbname uiw \
        --agent <agent id> --archive-root ~/uiw-archive

# 4. see where the project now stands
python3 release/baseline.py --check --dbname uiw
```

**The register.py `--commit` path this record depends on was itself found
broken and fixed on 2026-09-20**, the same session as this candidate's
verification: `main()` called `commit()` with unmerged candidate dicts,
which would have raised `KeyError: 'collection_method'` against any
class-based source, `eur-lex-sanctions` included — see `sources/README.md`,
"A real `--commit` bug found and fixed 2026-09-20."

## Executed

**2026-09-21, on the archive server, by the founder, an AI session guiding
each step interactively (commands proposed, founder ran them, output
pasted back for verification before the next step).**

1. **Registered** via `sources/register.py --commit --dbname uiw --agent
   442c1d13-a3e3-4e87-a856-f278e5063b47 --only eur-lex-sanctions`. Source
   id `fac9f632-6270-4055-b91e-a6b37ee1b63c`, `lifecycle_state = active`.
   The `eu-consolidated-list --derives-from--> eur-lex-sanctions`
   dependence recorded automatically by the same call, confirmed by query.
2. **A real, unrelated blocker found and cleared first: the archive
   server's database schema was ~10 weeks out of date.** Its checkout was
   on a stale branch (`claude/next-steps-2ag83g`, predating DR-0087) and,
   separately, the live `uiw` database's schema predated most of
   DR-0087…0103 — missing the entire identifier subsystem
   (`identifier_assignment`, `public_identifier`, `disambiguation_*`,
   `identifier_register_health`), most of `acquisition_attempt` (DR-0094),
   `citable_class`'s newer columns, and `pipeline_agent.public_title`
   (DR-0092). The first `--commit` run above failed
   (`ModuleNotFoundError: psycopg`, fixed by activating `.venv`); the first
   collection-run attempt failed with `UndefinedColumn:
   acquisition_route`, exposing the schema drift. **Resolved by a full
   backup-then-reload**, not a migration (this project has none): switched
   the checkout to `main` at `7e45c5a`; `pg_dump` (full, then data-only)
   to `~/uiw-backups/`, verified byte-identical across a duplicate run;
   row counts captured before touching anything (`source` 3,
   `source_dependence` 1, `collector_run` 3, `holding` 5, `pipeline_agent`
   2, `preservation_event` 15, `acquisition_attempt` 5); database dropped
   and rebuilt from current `schema/0*.sql`; data reloaded. Two real
   obstacles surfaced and were worked through, not around: the connecting
   role (`root`) lacked the privilege `pg_dump --disable-triggers`'
   technique needs (Postgres reserves disabling foreign-key-enforcement
   triggers to superuser) — resolved by reloading as the `postgres`
   superuser instead of weakening any constraint; and the data-only dump
   also carried DDL-seeded reference-table rows (`source_types`,
   `assertion_core_columns`, `classification_systems`,
   `identifier_types`) that collided with the same rows the fresh schema
   rebuild had already inserted — resolved by letting those specific,
   expected duplicate-key errors pass (`psql` without `ON_ERROR_STOP`) since
   the fresh schema's own seed data is correct and current, then
   confirming row counts for every real data table matched the pre-reload
   baseline exactly. **Nothing was lost**: `diff` of before/after row
   counts across all seven data tables showed no difference.
3. **Collection run**, real (not dry): `collector/run.py --source
   eur-lex-sanctions --dbname uiw --agent
   442c1d13-a3e3-4e87-a856-f278e5063b47 --archive-root ~/uiw-archive`.
   Run id `2eeef589-56aa-430d-af5f-855f5b6775d0`: **2 discovered, 2
   acquired, 0 failed, 16 199 485 bytes preserved, 0 documentary
   assertions** (DR-0066, as designed). The dated-CELEX suffix
   (`20260807`) was re-verified live immediately before this run, per
   Decision 4 — no amendment had landed since the 2026-09-20 verification.
4. **`release/baseline.py --check --dbname uiw`** run afterward to confirm
   nothing else regressed: every versioning dimension pinned except
   `dataset_snapshot` (expected — no preservation dump was requested this
   session, a separate act).
5. **Not addressed, flagged for a future session or the founder's
   attention:** the archive server has no schema-migration mechanism at
   all (this project's stated convention, "the schema is rebuilt from DDL,
   not migrated," assumes a throwaway test database, not a live one with
   real registered sources and preservation history) and no written
   runbook for the backup-verify-rebuild-reload sequence this execution
   improvised. Both the identical drift and the identical
   backup/reload work will recur at the next schema change unless one of
   these is written down. Worth a founder decision: whether to write that
   runbook now (companion to `docs/runbooks/A7-storage-bandwidth-measurement.md`),
   or accept the risk until the next registration/collection execution
   forces it again.

## Consequences

1. **Three of seven sanctions authorities are registered and collected**
   (`eu-consolidated-list`, `ofac-sdn`, and now `eur-lex-sanctions`);
   three more are approved for registration but not yet executed
   (`uk-ofsi-consolidated`, `bis-entity-list` partial, `seco-sanctions`);
   one remains a candidate, blocked on a Cloudflare challenge
   (`ua-nsdc-sanctions`).
2. **The archive server's schema is current as of this execution**
   (rebuilt from `main` at `7e45c5a`, 2026-09-21) — a real, incidental
   benefit: `uk-ofsi-consolidated`, `bis-entity-list` and `seco-sanctions`'s
   eventual execution will not hit the same schema-drift blocker this
   record's own execution did. This does not make execution of those
   three any more the founder's-act-per-source than before; it only means
   the archive server itself is no longer the obstacle it was.
3. **`eur-lex-sanctions`'s rights position needs no interim caution**,
   unlike three of the other six candidates: `may-redistribute` is
   inherited cleanly from the institutional-publisher class default,
   matching `eu-consolidated-list`, `ofac-sdn` and `uk-ofsi-consolidated`.
4. **The dated-CELEX re-verification obligation (Decision 4) is new** —
   no other registered source needs its `run_locators` checked before
   every run. Whoever executes this record, and whoever runs the
   collector against it afterward, needs to know that, which is why it is
   stated in *How to execute* as an explicit step rather than left
   implicit.
5. **The archive server has no schema-migration mechanism** — this
   execution's own Executed §5 flags it as unresolved, a founder decision
   for a future session, not settled here.
