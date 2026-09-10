# DR-0093 — First source registrations: EU Consolidated Financial Sanctions List and OFAC SDN

**Category:** operations / preservation | **Status:** Approved | **Decided:** 2026-09-08 by founder/principal editor
**Origin:** founder's direction of 2026-09-08 ("draft the registration for the EU list and OFAC"), following the seven-candidate proposal in [`sources/README.md`](../../sources/README.md) | **Supersedes:** — | **Superseded by:** —

> **AI provenance (§80).** Drafted by Claude (Claude Code) on 2026-09-08 at
> the founder's direction, and **approved by the founder the same day for
> both sources**, with the instruction to build the run script this record
> had listed as missing (Consequence 5, now discharged). Approval is what
> authorises the registrations and the first run described below; the
> registrations themselves are executed on the archive server by the
> founder, per *How to execute*, and have not been executed by this record.

## Context

The archive is empty. Every gate, the storage layout, the export and release
paths exist and are tested, but no source is registered and nothing has ever
been collected, so no release baseline can pin a collector, pipeline or
dataset version (`release/baseline.py --check`). Registering a source is the
act that authorises collecting from it (OPS-001, DR-0067, DR-0071(a)); the
gap between "drafted" and "registered" is deliberate, and this record is how
the gap gets crossed for the first time.

Seven sanctions-authority candidates were drafted on 2026-08-26 with every
locator unverified, because that environment could not reach the internet.
On 2026-09-08 the founder chose to begin with two of them. This session could
reach both publishers, so before drafting anything it fetched every file a
first run would collect, recorded digests and headers, and ran the real
collector against them into a throwaway database and storage root. The
record is
[docs/sources/verification-eu-consolidated-list-ofac-sdn.md](../sources/verification-eu-consolidated-list-ofac-sdn.md);
the short version is that both sources are live, both are served whole as
structured files, and the pipeline acquired all five files end to end with
byte-identical results. The rehearsals also found eight things the founder
should know, listed under *Consequences*.

The two candidates as they now stand in
[`sources/candidates/sanctions-authorities.yaml`](../../sources/candidates/sanctions-authorities.yaml):

| Key | What it is | Registry locator | First-run locators |
| --- | --- | --- | --- |
| `eu-consolidated-list` | European Commission (DG FISMA) consolidated list of persons, groups and entities subject to EU financial sanctions; all programmes; ~6 200 entities of which ~2 960 under UKR | the public XML file URL (the application root wants an EU Login session and answers 401) | the full-list XML and CSV |
| `ofac-sdn` | US Treasury OFAC SDN list and Consolidated Sanctions List; all programmes; 19 329 SDN entries of which 6 348 under RUSSIA-EO14024 | `https://sanctionslist.ofac.treas.gov/` | `SDN.XML`, `SDN_ADVANCED.XML`, `CONS_ADVANCED.XML` from the Sanctions List Service export API |

Both are `sanctions-authority`, `permanent` retention, `public` access,
`may-redistribute` with a rights basis marked **NOT LEGALLY REVIEWED**,
triage grade A1, daily cadence, whole-file capture, no parsing on ingest.

## Alternatives considered

1. **Register these two now and authorise a first run against the verified
   locators** (chosen). Smallest authorisation that produces real data;
   both publishers are institutional, the files are served whole, and
   DR-0071's interim constraints are honoured by capturing without
   structuring.
2. Register all seven at once. Rejected for now: five locators remain
   unfetched, two rights positions are unverified, and it commits the
   project immediately to reading capacity in de, fr, it and uk at Gate 2.
   Nothing here prevents doing it next.
3. Register these two plus `eur-lex-sanctions`, so the consolidated list's
   declared `derives-from` dependence is recorded at the same time.
   Rejected for now: EUR-Lex's landing locator answered with an empty 202
   (a challenge page), no instrument locator has been fetched, and WARC
   capture of legal acts is a different collection problem from downloading
   two files. The dependence is recorded when EUR-Lex is registered
   (Consequence 4).
4. Wait for the POL-0001 §10 legal review before collecting anything.
   Rejected: POL-0001 and DR-0071 already permit collection from registered
   sources with human-configured scope, provided personal data is not
   promoted into structure; that is exactly what whole-file capture does.
   The review gates scale-up (§9 releases), not this.
5. Verify only, and register nothing. Rejected: the verification is done and
   the value now lies in the first real capture series.

## Decision

On approval:

1. **`eu-consolidated-list` and `ofac-sdn` are registered** into the source
   registry with the field values in the candidate file as of this record's
   approval, by `sources/register.py --commit --only eu-consolidated-list
   ofac-sdn`. Each is accepted individually (§78); the founder may approve
   one and not the other, and this record should be annotated accordingly.
2. **A first collection run is authorised** against exactly the five
   `run_locators` listed in the candidate file — two for the EU list, three
   for OFAC — and no others. Adding a locator is a registry edit, not a run
   parameter.
3. **The first run is a manual act, performed once, on the archive server**,
   with a person as the collector-run's agent of record and the run's
   configuration recording the User-Agent string presented. Daily cadence is
   the registered policy but **is not automated by this record**;
   automating it waits on Consequences 1 and 2.
4. **Nothing from the run crosses Gate 2.** The captures are preserved
   holdings and nothing else. A completed run with zero documentary
   assertions is the expected result (DR-0066, Principle 5).
5. **The rehearsal of 2026-09-08 does not count as collection.** No system
   the project keeps holds anything from it; the first run under this record
   is the first collection, and the coverage record should say so.
6. The registrations carry the obligations `register.py --dry-run` prints:
   permanent retention with fixity checking on the DR-0005 cadence, and
   resolution of the rights positions under the POL-0001 §10 review.

### How to execute

On the archive server, after `setup/install.sh` has run and the test suites
pass there (`DB_NAME` and `ARCHIVE_ROOT` are whatever the install used;
the defaults are `uiw` and `~/uiw-archive`):

```bash
# 1. the founder as a pipeline agent (once); keep the id it prints
psql -qtA -d uiw -c "INSERT INTO pipeline_agent (id, kind, name) \
  VALUES (gen_random_uuid(), 'person', '<founder name>') RETURNING id"

# 2. register — this is the authorisation, and it collects nothing
python3 sources/register.py --check
python3 sources/register.py --dry-run --only eu-consolidated-list ofac-sdn
python3 sources/register.py --commit --dbname uiw \
        --only eu-consolidated-list ofac-sdn

# 3. the first run, one source at a time. --dry-run first: it checks the
#    registration, the agent, the locators and the archive root, and does
#    nothing else.
python3 collector/run.py --source ofac-sdn --dbname uiw \
        --agent <id from step 1> --archive-root ~/uiw-archive --dry-run
python3 collector/run.py --source ofac-sdn --dbname uiw \
        --agent <id from step 1> --archive-root ~/uiw-archive
python3 collector/run.py --source eu-consolidated-list --dbname uiw \
        --agent <id from step 1> --archive-root ~/uiw-archive

# 4. see where the project now stands
python3 release/baseline.py --check --dbname uiw
```

`collector/run.py` takes its locators from the candidate file's
`run_locators` and refuses anything else: an unregistered candidate, a
candidate with no verified run locators, an agent that is not a registered
person, a paused source, or an archive root that is not empty and not OCFL.
It records the invocation — candidate key, locators, verification date,
User-Agent, code commit — in the run's configuration (DR-0070). This exact
sequence was rehearsed on 2026-09-08 in a throwaway database and archive
root (verification record §7): five files, 211 MB, 50 seconds, every check
and every capture behaving as described.

The website for testing plays no part in this. Collection writes to the
archive server's database and OCFL roots only; the site is a projection
(Principle 18) and sees nothing until Gate 2 and Gate 3 decisions exist.

## Executed

Performed by the founder on the archive server on **2026-09-09**, from
branch `claude/next-steps-2ag83g` at commit `dda02fd`, as the person agent
`442c1d13-a3e3-4e87-a856-f278e5063b47`:

| Act | Record |
| --- | --- |
| Registration | `eu-consolidated-list` → source `633a0bd3-a040-4883-824f-165f38035961`; `ofac-sdn` → source `49706db8-66ac-4d4e-9924-73e9049d09cf` |
| First run, OFAC | run `121adaf0-cb35-4449-9517-ebfc27d56c89`: discovered 3, acquired 3, failed 0, **160 398 618 bytes** in 20.5 s |
| First run, EU | run `3ab09fb5-b169-4b2b-bfc2-71a28182e778`: discovered 2, acquired 2, failed 0, **50 932 812 bytes** in 15.9 s |
| Canonical knowledge created | 0 documentary assertions (DR-0066) |

**This is the project's first collection.** Two observations from it:

- The OFAC files were **295 553 bytes larger** than at verification the day
  before: OFAC published a new list between 2026-09-08 and 2026-09-09, so
  the archive's first OFAC capture is not the one the verification record
  digests. That is the capture series doing its job from its first day.
  The EU files were byte-identical to verification, so the EU list was still
  the 2026-08-05 publication, now 35 days old.
- `release/baseline.py --check` afterwards reported four unpinned items.
  `dataset_snapshot` is expected (no dump has been made). `code_commit` was
  refused because the installer's `.venv` directory was untracked, which is
  fixed by ignoring it. `collector_version` and `pipeline_version` are a
  real tension between this record's §3 (a person as the run's agent of
  record) and the baseline's expectation that a versioned software agent
  ran (AI-002); resolved by a separate ruling, not here.

Two installer defects were found and fixed on the way: it cloned only
`main`, and as root it never switched to the postgres user, so the
database role was never created. Both are on the branch.

## Consequences

Findings from the verification, in the order they matter. None blocks the
first run. Items 1 and 2 need a ruling before the daily cadence is
automated; each would be its own record.

1. **Successive captures are not linked as a series.** DR-0074 relates
   captures of the same locator through `capture_series_member`; the
   collector never writes it. The repeat capture in the rehearsal became an
   unrelated second holding. The series the candidates' `scope_rules`
   promise does not exist until the collector records it.
2. **Unchanged bytes are stored again.** No conditional request is made and
   no digest comparison precedes admission, so an unchanged day at daily
   cadence stores about 211 MB of duplicates. The EU server sends
   `Last-Modified`, the OFAC object sends `ETag`. Whether an unchanged fetch
   is "a recorded attempt and no holding" or "a holding that happens to
   share bytes" is a DR-0070 coverage question, not only a storage one.
3. **Response provenance is discarded.** The fetcher receives the response
   headers and the acquisition record keeps none of them. For OFAC that
   loses the publication id (969 on 2026-09-03), the delta file name, the
   final S3 URL and the ETag; for the EU it loses the server's filename
   (`20260805-FULL-1_1(xsd).xml`) and `Last-Modified`. These are the
   publisher's statements about what was served and belong on the
   `acquisition_attempt` row.
4. **The EUR-Lex dependence goes unrecorded** until `eur-lex-sanctions` is
   registered, because `--only` drops any declared relation whose other end
   is not in the set. The consolidated list's own file links every entry to
   its EUR-Lex act, so the relation is recoverable, but the registry will
   not say the list is a compilation until then. Registering EUR-Lex is the
   natural next registration.
5. ~~No command-line entry point exists for a run.~~ **Discharged with this
   record's approval:** `collector/run.py`, with 18 tests, two of which
   were seen to fail when the registration check and the person-agent check
   were removed in turn.
6. **The EU public token's terms are unverified.** The value is public and
   the files are served without login; no page stating the conditions was
   readable from a non-browser client. Folded into the §10 review.
7. **Whole-file capture is broad.** UKR is under half of the EU list and the
   Russia programme about a third of the SDN list; the rest, individuals
   with dates and places of birth included, is preserved in every capture.
   Within policy as written (DR-0071(b), POL-0001 §4), and a
   data-minimisation fact the §10 review should see. The candidate file now
   says so on the `ofac-sdn` entry.
8. **Quarantine copies are never removed.** Found in the CLI rehearsal: the
   archive directory held 403 MB after 211 MB of captures, because
   `_quarantine()` writes the bytes to `quarantine/` and nothing deletes
   them after Gate 1 admits the object into OCFL. DR-0069 wants quarantine
   outside the archive; it does not want it to be a second archive. A
   quarantine item admitted at Gate 1 should be removed, and one refused
   should be kept for the record. Not blocking; the disk cost is the same
   order as Consequence 2 and should be fixed alongside it.

Also recorded:

- `sources/register.py` now accepts three optional, non-stored fields —
  `locator_verified`, `run_locators`, `verification_note` — so the dry-run
  can say which locators were fetched and which are still claims, and
  refuses run locators that carry no verification date. Five tests cover
  this; the suite was seen to fail when the refusal was removed.
- The candidate file's `eu-consolidated-list` locator changed from the
  application root (401) to the public XML file URL. This is a locator
  correction on an unregistered candidate, not a registry change.
- The collector's fetch layer has now completed live fetches (five files,
  up to 127 MB, one through a redirect chain) in a rehearsal. What remains
  unexercised is stated in `collector/README.md`: slow or rate-limiting
  origins, conditional requests, and any real security scanner.
