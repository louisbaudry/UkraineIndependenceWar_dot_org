# DR-pending-second-source-registrations — Second source registrations: UK OFSI Consolidated List and BIS Denied Persons List

**Category:** operations / preservation | **Status:** Approved | **Decided:** 2026-09-12 by founder/principal editor
**Origin:** founder's direction of 2026-09-12 ("register both now, as verified"), following the verification record for both candidates | **Supersedes:** — | **Superseded by:** —

> **AI provenance (§80).** Drafted by Claude (model: `claude-sonnet-5`) on
> 2026-09-12 at the founder's direction, and **approved by the founder the
> same day**, matching DR-0093's pattern for the first two registrations.
> Approval is what authorises the registrations described below; the
> registrations themselves are executed on the archive server by the
> founder, per *How to execute*, and have not been executed by this record.
>
> **The `register.py` dependence gap this record found was fixed the same
> day**, at the founder's direction after this record's first draft named
> it as a known issue: `commit()` and `validate()` in `sources/register.py`
> were changed to resolve a dependence link's other end against the
> database, not only the current call's own batch. Verified before and
> after — the gap reproduced in a throwaway database seeded to match the
> archive server's state, then confirmed closed in the same scenario —
> and by test: `sources/tests/test_register.py` gained four checks, two of
> which were shown to fail when each half of the fix was reverted in turn.

## Context

DR-0093 registered two of the seven sanctions-authority candidates
(`eu-consolidated-list`, `ofac-sdn`) and ran the project's first
collection. The other five remained candidates. On 2026-09-12, two more
were verified against live locators with the same rigor — real fetches,
digest-stability checks across two fetches, and an end-to-end rehearsal
through the real collector into a throwaway database
([verification record](../sources/verification-bis-dpl-ofsi-consolidated.md)).
The founder then directed registering both.

`uk-ofsi-consolidated` is fully verified: both files it needs (CSV and
XML) were found on OFSI's own blob storage (not the gov.uk publication
page the candidate names as its `locator`), fetched twice with stable
digests, and acquired end to end.

`bis-entity-list` is **partially** verified. The candidate is named for
two BIS lists — the Entity List and the Denied Persons List — and only the
second has a clean, structured file locator as of this record: BIS
publishes the Entity List as federal regulation text (EAR Supplement No. 4
to Part 744), not a standalone file. A working alternative exists
(Commerce's Consolidated Screening List) but was deliberately not
substituted, because it merges in OFAC's own data and would misattribute
that to BIS while duplicating `ofac-sdn`'s own coverage with no declared
dependence for it (DR-0028).

**A gap found while preparing this record, and fixed the same day, not by
DR-0093:** `register.py --commit`'s dependence-recording originally
inserted a `source_dependence` row only when *both* ends of a declared
relation were being registered in the same `--only` call — it never
checked the database for an end already registered by an earlier call.
`uk-ofsi-consolidated`'s declared `common-evidentiary-origin` relation to
`eu-consolidated-list` (already registered under DR-0093) would therefore
have been silently dropped, the same way DR-0093 §Consequences 4 found the
EUR-Lex relation dropped for the opposite reason (the other end not yet
registered at all). Founder direction after this record's first draft:
fix `register.py` now rather than leave it for later. See Consequences.

## Alternatives considered

1. **Register both now: `uk-ofsi-consolidated` in full,
   `bis-entity-list` with its Denied Persons List locator only** (chosen).
   Both passed the same verification rigor DR-0093 required; a partial BIS
   registration is real, useful coverage rather than nothing, and the
   registry gains a fourth and fifth registered source without waiting on
   the Entity List's own locator.
2. Register `uk-ofsi-consolidated` only, and hold `bis-entity-list` until
   its Entity List locator is found, so the registered candidate matches
   its full name. Rejected: the founder's direction was to register both.
3. Hold both until every remaining candidate reaches the same state.
   Rejected: nothing about `eur-lex-sanctions`, `seco-sanctions`, or
   `ua-nsdc-sanctions` needing more work is a reason to withhold two
   sources that are ready, per §78's per-source acceptance.

## Decision

On approval:

1. **`uk-ofsi-consolidated` and `bis-entity-list` are registered** into the
   source registry with the field values in the candidate file as of this
   record's approval, by `sources/register.py --commit --only
   uk-ofsi-consolidated bis-entity-list`. Each is accepted individually
   (§78), matching DR-0093's precedent.
2. **`bis-entity-list` is registered with `run_locators` naming only its
   Denied Persons List file.** The registry entry's `name` still reads
   "BIS Entity List and Denied Persons List" — the candidate is not
   renamed — but only the Denied Persons List is collectible until the
   Entity List gets its own verified locator and `run_locators` is
   extended. `register.py --dry-run` and any coverage reporting should
   make this visible, not imply full coverage of the name.
3. **The declared dependence `uk-ofsi-consolidated →
   common-evidentiary-origin→ eu-consolidated-list` is recorded by this
   registration**, now that `register.py` is fixed (Consequences 1): its
   `commit()` resolves a dependence link's other end against the database
   by name when it is not in the current `--only` batch, rather than only
   against sources registered in the same call.
4. **A first collection run against either source is a separate act**,
   not authorised by this record alone. DR-0093's pattern — `--dry-run`
   first, then a manual run with a person as agent of record — applies
   equally here and is left to whoever executes this record, at whatever
   pace is wanted; nothing about collecting from these two is time-
   sensitive in the way the first-ever run was.
5. **Nothing from any future run crosses Gate 2** (DR-0066, Principle 5),
   unchanged from every other registered source.
6. The registrations carry the obligations `register.py --dry-run`
   prints: permanent retention with DR-0005 fixity checking, and
   resolution of the rights positions under the POL-0001 §10 review
   (both already `NOT LEGALLY REVIEWED`, unchanged by this record).

### How to execute

On the archive server, with the same database and archive root DR-0093
used (`uiw` and `~/uiw-archive` unless the install used different names).
Reuse the person `pipeline_agent` id DR-0093's step 1 already created,
rather than minting a second one for the same founder, unless a different
person is registering this time.

```bash
# 1. register — this is the authorisation, and it collects nothing.
#    the declared uk-ofsi-consolidated -> eu-consolidated-list dependence
#    is now recorded automatically by this call (Consequences 1 fix) --
#    no separate step or manual SQL is needed.
python3 sources/register.py --check
python3 sources/register.py --dry-run --only uk-ofsi-consolidated bis-entity-list
python3 sources/register.py --commit --dbname uiw \
        --agent <the person agent id from DR-0093's step 1, or a new one> \
        --only uk-ofsi-consolidated bis-entity-list

# 2. confirm the dependence was recorded (expected now, unlike before the fix):
psql -d uiw -c "SELECT s1.name, s2.name, sd.relation FROM source_dependence sd \
  JOIN source s1 ON s1.id=sd.dependent_id JOIN source s2 ON s2.id=sd.depends_on_id"

# 3. a first run, when wanted — one source at a time, --dry-run first
python3 collector/run.py --source uk-ofsi-consolidated --dbname uiw \
        --agent <agent id> --archive-root ~/uiw-archive --dry-run
python3 collector/run.py --source uk-ofsi-consolidated --dbname uiw \
        --agent <agent id> --archive-root ~/uiw-archive
python3 collector/run.py --source bis-entity-list --dbname uiw \
        --agent <agent id> --archive-root ~/uiw-archive --dry-run
python3 collector/run.py --source bis-entity-list --dbname uiw \
        --agent <agent id> --archive-root ~/uiw-archive

# 4. see where the project now stands
python3 release/baseline.py --check --dbname uiw
```

This exact sequence — registration and a live collector run against both
locators — was rehearsed 2026-09-12 in a throwaway database and storage
root (see the verification record), with the two-agent split
(`DR-pending-collection-run-two-agents`) also exercised: every
preservation event named the software agent, never the person, checked
directly against the rehearsal database.

**Step 1 and the dependence fix were both re-verified after the fix
landed**, in a separate throwaway database seeded to match the archive
server's actual state (`eu-consolidated-list`/`ofac-sdn` registered
first, exactly as DR-0093 left them). Before the fix: `register.py
--commit --only uk-ofsi-consolidated bis-entity-list` registered both
sources correctly but left zero rows in `source_dependence` — the gap was
real, not a guess. After the fix, in a fresh copy of the same database:
the identical `--commit` call registered both sources *and* printed the
dependence in `describe()`'s output *and* inserted exactly the expected
row (`UK OFSI Consolidated List of Financial Sanctions Targets` →
`EU Consolidated Financial Sanctions List`, `common-evidentiary-origin`)
with no separate step. A second scenario — registering a source whose
declared dependence points at something not registered anywhere yet
(`eu-consolidated-list` alone, which depends on the unregistered
`eur-lex-sanctions`) — was also tried: `register.py` prints "dependence
not recorded yet" for each such link and inserts nothing, rather than
crashing or asserting a link to a source that does not exist.

## Executed

Not yet. This record is approved; registration on the archive server has
not been performed as of this record's drafting. Whoever executes it
should replace this section with the actual run ids, byte counts and any
findings, matching DR-0093's *Executed* section.

## Consequences

1. **Fixed the same day, before execution.** `register.py`'s `commit()`
   now resolves a dependence link's `from`/`to` against the current
   `--only` batch first, then against an existing `source` row by name —
   and `main()` no longer drops a dependence link merely because one end
   is outside `--only`; it drops one only when *neither* end is in the
   batch and *no* database row resolves it, printing which end could not
   be resolved rather than silently discarding the link. `validate()`
   gained an optional `known_keys` parameter so a `--only` call's
   dependence-existence check can be told about candidates outside the
   filtered batch without a database. Four new tests in
   `sources/tests/test_register.py` (31 total, up from 27), two of which
   were shown to fail when each half of the fix was reverted in turn.
   This closes the gap for every future registration that depends on
   something already in the registry, not only this one.
2. **`bis-entity-list`'s registered name overstates its coverage** until
   the Entity List gets its own locator (Decision 2). Anyone reading the
   registry by name alone, without checking `run_locators`, would assume
   both BIS lists are covered. `register.py --dry-run`'s existing
   `(verified <date>)` / `(UNFETCHED)` marker per source does not
   distinguish a fully-verified candidate from a partially-verified one
   like this; that distinction is carried only in the candidate file's own
   `verification_note` and this record, not in any tool's output.
3. **Two more of seven are registered; three remain candidates**
   (`eur-lex-sanctions`, `seco-sanctions`, `ua-nsdc-sanctions`), each
   needing more than a locator search: EUR-Lex and NSDC need a specific
   instrument or decision set identified (legal/editorial judgment), SECO
   needs site navigation this session's plain fetches did not achieve.
4. **A first collection run against either source is still to happen.**
   This record authorises it; it does not perform it. `release/baseline.py
   --check`'s `collector_version`/`pipeline_version` pinning (resolved
   2026-09-12 by `DR-pending-collection-run-two-agents`) will be exercised
   against these two sources for the first time on the archive server
   whenever that run happens.
