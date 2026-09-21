# DR-0098 — Third source registration: SECO sanctions list (Switzerland)

**Category:** operations / preservation | **Status:** Approved | **Decided:** 2026-09-14 by founder/principal editor
**Origin:** founder's direction of 2026-09-14 ("register seco-sanctions"), following the 2026-09-13 verification record | **Supersedes:** — | **Superseded by:** —

> **AI provenance (§80).** Drafted by Claude (model: `claude-sonnet-5`) on
> 2026-09-14 at the founder's direction, and **approved by the founder the
> same day**, matching DR-0093 and DR-0096'
> pattern. Approval is what authorises the registration described below;
> the registration itself is executed on the archive server by the
> founder, per *How to execute*, and has not been executed by this record.

## Context

`seco-sanctions` was verified 2026-09-13 on a second attempt: the file
lives on `sesam.search.admin.ch`, a separate SECO application, not the
main site every earlier guess had targeted
([verification record](../sources/verification-seco-sanctions.md)). Same
rigor as every prior verification — fetched twice, digest stable, acquired
end to end by the real collector into a throwaway database, zero
documentary assertions. This is a **separate decision** from
`DR-0096` (`uk-ofsi-consolidated`/
`bis-entity-list`, approved but not yet executed): `seco-sanctions` had no
registration decision at all until the founder gave one today.

`seco-sanctions` declares one dependence,
`seco-sanctions --common-evidentiary-origin--> eu-consolidated-list`
(`sources/candidates/sanctions-authorities.yaml`), on a source already
registered under DR-0093. This is the exact case
`DR-0096` found `register.py --commit`
silently dropping and fixed the same day (2026-09-12): `commit()` now
resolves a dependence link's other end against the database when it is
not in the current `--only` batch. Re-verified for this record in a
throwaway database seeded to match the actual archive-server state
(`eu-consolidated-list` and `ofac-sdn` registered, nothing else): `register.py
--commit --only seco-sanctions` alone — no second source in the same
call, unlike the OFSI/BIS pair — correctly printed the dependence in
`describe()`'s output and inserted the expected row. This is the fix's
first confirmation on a single-source registration rather than a pair.

`seco-sanctions`' rights position remains `may-preserve`, basis marked
`UNVERIFIED` in the candidate file — a real locator says nothing about
redistribution rights, and this record does not change that. Registering
it also commits the project to German/French/Italian reading capacity at
Gate 2 (`primary_languages: [de, fr, it, en]`), per DR-0081's no-seeded-
translations rule — `register.py --dry-run`'s own output states this
plainly when run.

## Alternatives considered

1. **Register `seco-sanctions` now, as verified** (chosen). Same rigor as
   the four sources before it; no reason to withhold a fifth ready source
   while three items from a different, unrelated open-decisions thread
   (Track A A4/A5/A6/A7) remain unstarted.
2. Hold `seco-sanctions` until `eur-lex-sanctions` and `ua-nsdc-sanctions`
   are also verified, registering all three sanctions-authority stragglers
   together. Rejected: the founder's direction was to register this one
   now; §78's per-source acceptance does not require batching, and EUR-Lex/
   NSDC each need legal or editorial instrument-selection work with no
   estimate for when it lands.
3. Hold `seco-sanctions` until the OFSI/BIS pair
   (`DR-0096`) is actually executed on the
   archive server, so registrations happen in the order they were
   approved. Rejected: nothing links the two decisions technically —
   `seco-sanctions`' dependence resolves against `eu-consolidated-list`
   alone, already registered, regardless of whether OFSI/BIS have been
   executed yet — and sequencing registrations by approval order is a
   convenience, not a requirement DR-0067 or DR-0093 states.

## Decision

On approval:

1. **`seco-sanctions` is registered** into the source registry with the
   field values in the candidate file as of this record's approval, by
   `sources/register.py --commit --only seco-sanctions`. Accepted
   individually (§78), matching precedent.
2. **The declared dependence on `eu-consolidated-list` is recorded by
   this registration**, automatically, by the same `--commit` call — no
   manual SQL and no companion registration in the same call are needed,
   confirmed in *How to execute*.
3. **A first collection run is a separate act**, not authorised by this
   record alone. `--dry-run` first, then a manual run with a person as
   agent of record, per the established pattern, left to whoever executes
   this record at whatever pace is wanted.
4. **Nothing from any future run crosses Gate 2** (DR-0066, Principle 5),
   unchanged from every other registered source.
5. The registration carries the obligations `register.py --dry-run`
   prints: permanent retention with DR-0005 fixity checking; German/
   French/Italian reading capacity committed at Gate 2 (DR-0081); and
   resolution of the rights position under the POL-0001 §10 review
   (already `may-preserve`/`UNVERIFIED`, unchanged by this record).
6. **This decision is independent of
   `DR-0096`.** Executing either does not
   require, wait on, or depend on the other; they may be run in either
   order or on different days.

### How to execute

On the archive server, with the same database and archive root prior
registrations used (`uiw` and `~/uiw-archive` unless the install used
different names). Reuse the person `pipeline_agent` id DR-0093's step 1
already created, unless a different person is registering this time.

```bash
# 1. register — this is the authorisation, and it collects nothing.
#    the declared seco-sanctions -> eu-consolidated-list dependence is
#    recorded automatically by this call.
python3 sources/register.py --check
python3 sources/register.py --dry-run --only seco-sanctions
python3 sources/register.py --commit --dbname uiw \
        --agent <the person agent id from DR-0093's step 1, or a new one> \
        --only seco-sanctions

# 2. confirm the dependence was recorded:
psql -d uiw -c "SELECT s1.name, s2.name, sd.relation FROM source_dependence sd \
  JOIN source s1 ON s1.id=sd.dependent_id JOIN source s2 ON s2.id=sd.depends_on_id \
  WHERE s1.name = 'SECO sanctions list (Switzerland)'"

# 3. a first run, when wanted — --dry-run first
python3 collector/run.py --source seco-sanctions --dbname uiw \
        --agent <agent id> --archive-root ~/uiw-archive --dry-run
python3 collector/run.py --source seco-sanctions --dbname uiw \
        --agent <agent id> --archive-root ~/uiw-archive

# 4. see where the project now stands
python3 release/baseline.py --check --dbname uiw
```

**Step 1 and its dependence resolution were re-verified for this record**,
in a throwaway database seeded to match the archive server's actual
current state (`eu-consolidated-list` and `ofac-sdn` registered, nothing
else — `uk-ofsi-consolidated`/`bis-entity-list` not assumed, since their
own execution status is independent per Decision 6): the exact `--commit
--only seco-sanctions` call above registered the source and inserted the
expected `source_dependence` row
(`SECO sanctions list (Switzerland)` → `EU Consolidated Financial
Sanctions List`, `common-evidentiary-origin`) with no companion source in
the same call and no manual SQL — the first confirmation of the
2026-09-12 `register.py` fix on a single-source registration rather than
a pair.

## Executed

**2026-09-21, on the archive server, by the founder**, in the same
`--commit` call as `DR-0096`'s two sources
(`--only uk-ofsi-consolidated bis-entity-list seco-sanctions`) — matches
Decision 6's independence: registered together as a matter of session
convenience, not because either decision required the other.

1. **Registered.** Source id `04ea786f-0021-4033-b578-6921a7151386`. The
   declared `seco-sanctions --common-evidentiary-origin-->
   eu-consolidated-list` dependence recorded automatically by the same
   call, confirmed by query.
2. **Collection run**, real, `--dry-run` first: run
   `d21d849d-fe96-409c-ae85-cb14b42f739e` — 1 discovered, 1 acquired, 0
   failed, 42 300 406 bytes preserved, exactly matching the 2026-09-13
   verification's digested file size.
3. **`release/baseline.py --check --dbname uiw`** confirmed afterward:
   every versioning dimension pinned except `dataset_snapshot` (expected —
   no preservation dump requested this session).

## Consequences

1. **Three of seven sanctions authorities are now approved for
   registration** (`uk-ofsi-consolidated`, `bis-entity-list` partial,
   `seco-sanctions`), alongside the two already registered — five of
   seven decided, two remaining (`eur-lex-sanctions`, `ua-nsdc-sanctions`)
   still candidates. None of the three approved-but-unexecuted
   registrations has actually run on the archive server as of this
   record.
2. **German/French/Italian join English as committed Gate 2 reading
   languages** (DR-0081), the first non-English commitment since project
   start — `ua-nsdc-sanctions` (Ukrainian) remains the only outstanding
   language commitment not yet made.
3. **`seco-sanctions`' rights position stays the long pole for
   redistribution.** `may-preserve` means holdings from it can be
   preserved but not shared onward until POL-0001 §10's review resolves
   the basis — unchanged by this record, stated here so a later reader
   does not mistake registration for a rights determination.
