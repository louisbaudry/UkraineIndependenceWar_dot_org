# DR-pending-eur-lex-sanctions-registration — Fourth source registration: EUR-Lex restrictive measures (Ukraine/Russia)

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

Not yet. This record is approved; registration on the archive server has
not been performed as of this record's drafting. Whoever executes it
should replace this section with the actual run id, byte count and any
findings, matching DR-0093's *Executed* section.

## Consequences

1. **Four of seven sanctions authorities are now approved for
   registration** (`uk-ofsi-consolidated`, `bis-entity-list` partial,
   `seco-sanctions`, `eur-lex-sanctions`), alongside the two already
   registered — six of seven decided, one remaining
   (`ua-nsdc-sanctions`) still a candidate, blocked on a Cloudflare
   challenge. None of the four approved-but-unexecuted registrations has
   actually run on the archive server as of this record.
2. **`eur-lex-sanctions`'s rights position needs no interim caution**,
   unlike three of the other six candidates: `may-redistribute` is
   inherited cleanly from the institutional-publisher class default,
   matching `eu-consolidated-list`, `ofac-sdn` and `uk-ofsi-consolidated`.
3. **The dated-CELEX re-verification obligation (Decision 4) is new** —
   no other registered source needs its `run_locators` checked before
   every run. Whoever executes this record, and whoever runs the
   collector against it afterward, needs to know that, which is why it is
   stated in *How to execute* as an explicit step rather than left
   implicit.
