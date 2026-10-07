# DR-0114 — Register DeepStateMap's front-line snapshot

**Category:** operations / preservation | **Status:** Approved | **Decided:** 2026-10-06 by founder/principal editor
**Origin:** the founder's ruling of 2026-10-06 (option 1 of three: register `deepstatemap` now and hold `isw-orca` until ISW answers a written permission request), answering the question that closed the verification of issue #47 | **Supersedes:** — | **Superseded by:** —

> **AI provenance (§80).** Drafted 2026-10-06 by an AI assistant (Anthropic
> Claude Code agent session) at the founder's direction. The ruling is the
> founder's: it was put as a question with three options (register
> `deepstatemap` only and hold ISW; register both; register neither yet) and
> a recommendation for the first, and the founder chose it. The wording,
> reasons and consequences below are the drafter's. Approval authorises the
> registration and the first run described below. **Both are executed on the
> archive server by the founder, per *How to execute*, and have not been
> executed by this record.** This session had no access to the archive server
> or its database.

## Context

The founder chose territorial control as the first war-fact category
(`sources/candidates/war-facts.yaml`, 2026-09-21). The candidate
`deepstatemap` is DeepState's live front-line map (a Ukrainian volunteer
OSINT project), read through its unauthenticated JSON endpoint
`https://deepstatemap.live/api/history/last`. It was verified live on
2026-09-21 and again on 2026-10-06, and rehearsed through the real collector
in a throwaway database on 2026-09-21 (1 acquired, 0 failed, 627 479 bytes,
0 documentary assertions). The full record is
[`verification-war-facts-first-two.md`](../sources/verification-war-facts-first-two.md).

What registration takes on, in short:

- **Geometry, not people.** The body is front-line polygons as GeoJSON
  (525 features on 2026-10-06). No named individuals were seen, and nothing
  is structured (DR-0066).
- **Rights unverified.** No licence or terms text was found on the site on
  either date; `/terms`, `/privacy`, `/about`, `/license` and `/api` all
  return 404. The candidate claims `may-preserve` and nothing more (§14). The
  silence is not a grant.
- **A current snapshot only.** The endpoint returns the latest map. A time
  series exists only if someone fetches it repeatedly. The body's own
  `datetime` field read "04.10 22:56" on 2026-10-06, so the map is republished
  when DeepState updates it, not on every request: a run between updates
  captures identical bytes.

### Relation to POL-0001 §10 and DR-0072

This is not the collection scale-up DR-0072 and the 2026-09-08 ruling
suspend. It registers one source with one configured endpoint of about
0.6 MB. No crawl, no discovery, no link-following (DR-0071(a)).

## Alternatives considered

1. **Register `deepstatemap` only and hold `isw-orca`** (chosen).
   DeepStateMap needs no per-run URL maintenance and is the geometry other
   work depends on. Its terms are absent, not restrictive.
2. **Register both.** Not chosen: ISW's Fair Use and Attribution Policy
   (read 2026-10-06) requires prior written permission for "incorporation of
   ISW Materials into other datasets ... or systems", and automated daily
   copying of its reports is the case the policy appears to reach. Held
   instead (see Decision 8).
3. **Register neither yet; write licensing enquiries first.** Not chosen: the
   `may-preserve` position is the project's established floor for sources
   whose rights are unverified, and an enquiry to DeepState can be made
   alongside.

## Decision

On approval:

1. **`deepstatemap` is registered** in the source registry, with its class
   `war-facts-territorial-control` and the field values in the candidate file
   as of this record's approval, by
   `sources/register.py --commit --only deepstatemap`.
2. **A first collection run is authorised** against the single run locator
   `https://deepstatemap.live/api/history/last`: `--dry-run` first, then a
   real run.
3. **Later runs are authorised only as manual runs by a person**, each one
   request to that locator, at times the founder chooses. **No scheduled or
   automatic run is authorised.** `docs/infrastructure.md` records no
   collection schedule as running; creating one is a separate decision.
4. **NOT authorised:** the site's own history browsing, any other endpoint, the
   interactive map page, or any retrieval beyond the one locator. Adding any of
   them is an edit to `run_locators` that needs its own verification and
   record.
5. **Nothing from any run crosses Gate 2** (DR-0066, Principle 5). No polygon
   is structured into a territorial-status relation or a place until the
   `place` model (WP 3.10) is ruled and Gate 2 decides.
6. The registration carries the obligations `register.py --dry-run` prints:
   permanent retention with DR-0005 fixity checking, and the unverified
   `may-preserve` rights position, unchanged by this record. **Preserving is
   not publishing** (POL-0001 §1): nothing here authorises republishing the
   geometry, which waits on a rights check and Gate 3.
7. **This decision is independent of every other pending registration**
   (`isw-orca`, `liveuamap`, the Prosecutor General, `ua-nsdc-sanctions-*`).
   None is required, authorised or affected by it.
8. **`isw-orca` is held, not refused.** It stays a verified, unregistered
   candidate until ISW answers a written permission request (a draft is in
   [`isw-permission-request-draft.md`](../sources/isw-permission-request-draft.md);
   sending it is the founder's act). Registering it later is a new decision
   and a new record.

### How to execute

On the archive server, on current `main`. Reuse the person `pipeline_agent`
id from DR-0093's step 1.

```bash
# 1. register (idempotent per source since #62's fix)
python3 sources/register.py --check
python3 sources/register.py --dry-run --only deepstatemap
python3 sources/register.py --commit --dbname uiw \
        --agent <person agent id> --only deepstatemap

# 2. the first run
python3 collector/run.py --source deepstatemap \
        --dbname uiw --agent <agent id> --archive-root ~/uiw-archive --dry-run
python3 collector/run.py --source deepstatemap \
        --dbname uiw --agent <agent id> --archive-root ~/uiw-archive

# 3. see where the project now stands
python3 release/baseline.py --check --dbname uiw
PGDATABASE=uiw python3 storage/measure.py --archive-root ~/uiw-archive
```

Two corrections carried over from DR-0110's *Executed* section:
`storage/measure.py` takes no `--dbname` and reads `PGDATABASE`; and the
source table's state column is `lifecycle_state`, not `status`. The live
database still lacks `source_identity_unique` (issue #76); `register.py`
itself refuses a re-run, so registration is safe, but it is worth adding
first.

Expected from step 2, if the map is unchanged since 2026-10-06: 1
discovered, 1 acquired, 0 failed, about 0.63 MB, 0 documentary assertions.
The byte count will differ whenever DeepState has updated the map; that is
the source working, not a failure.

## Consequences

1. The archive gains its first territorial-control source: front-line
   geometry that incidents, strikes and DR-0044's territorial-status relations
   can later be set against, once structuring is designed.
2. **A series is manual.** Each run is one snapshot. If nobody runs it, the
   archive holds one dated map and nothing between. The board, not this
   record, tracks whether it is being done. A scheduled run is the natural
   next decision and needs its own record.
3. **Storage is small but permanent.** At about 0.63 MB a snapshot, a daily
   run is about 230 MB a year, and roughly twice that on disk until the
   undischarged-quarantine duplication (recorded as 2.01x in DR-0110's
   *Executed*) is closed. A run between map updates records an unchanged
   capture.
4. **Rights stay unverified, and no enquiry has been made.** The site states
   no terms. Writing to the DeepState team is open and not decided here.
   Citing the geometry with attribution is the plan; republishing it waits on
   that and on Gate 3.
5. **Single-origin caveat.** DeepStateMap is one volunteer project's account
   of control. It is a source, graded for triage only (DR-0027), and any
   territorial-status assertion drawn from it must be a source-attributed one
   (DR-0044), never the project's own conclusion.
