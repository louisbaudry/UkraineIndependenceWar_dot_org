# Source registration

Candidate sources for the archive's collection, drafted against the DR-0067
registry schema, across two files: `sanctions-authorities.yaml` (the
original thematic area) and `war-facts.yaml` (territorial control /
military operations, started 2026-09-21 following the founder's
redirection toward war-fact subject matter — see that file's own header).
**Six of the seven sanctions candidates are registered and collected** on
the archive server (`eu-consolidated-list`, `ofac-sdn`, `eur-lex-sanctions`,
`uk-ofsi-consolidated`, `bis-entity-list`, `seco-sanctions`); the seventh,
`ua-nsdc-sanctions`, was Cloudflare-blocked from every automated session
through 2026-09-21. **Unblocked 2026-09-22/23** by human-assisted (founder)
browser access, and now drafted as **three separate candidates**
(`ua-nsdc-sanctions-legal-entities`, `ua-nsdc-sanctions-individuals`,
`ua-nsdc-sanctions-vessels` — Aircraft not registered, 0 records), all
fully verified (locator, export structure, row counts) but not yet
registered — see "Which locators are verified" below. **Both war-facts candidates
(`isw-orca`, `deepstatemap`) are verified but not yet registered** — the
founder's decision, per source. Registration lives in the server's
database, not in this file: the file is the candidate, the row is the
registration.

```bash
python3 sources/register.py --check                      # validate only
python3 sources/register.py --dry-run                    # what it would authorise
python3 sources/register.py --commit --dbname uiw \
        --agent <your-pipeline_agent-uuid> \
        --only ofac-sdn eu-consolidated-list             # register these two
```

Registering a source is **the act that authorises collecting from it**
(OPS-001). It is not a configuration change, and the gap between "drafted"
and "registered" exists so that authorising is deliberate.

Collecting from a registered source is a further, separate act:

```bash
python3 collector/run.py --source ofac-sdn --dbname uiw \
        --agent <your-pipeline_agent-uuid> --archive-root ~/uiw-archive
```

which takes the exact `run_locators` listed and verified in the candidate
file and refuses an unregistered candidate. **DR-0093 (approved 2026-09-08)
authorises this for `eu-consolidated-list` and `ofac-sdn`**; the other five
remain proposals.

## What is proposed

Seven sanctions and export-control authorities — the thematic area the
founder chose — drafted as **nine candidates**, since `ua-nsdc-sanctions`
was split into three (per entity class) on 2026-09-22 rather than
registered as one (see "Which locators are verified" below). Two of them,
`eu-consolidated-list` and `ofac-sdn`, are
approved for registration and a first run by
[DR-0093](../docs/decision-records/DR-0093-first-source-registrations.md);
the registration itself happens on the archive server. Institutional publishers, stable formats, near-zero
special-category personal data, so DR-0071's interim constraints barely bite
and POL-0001's structuring limits are straightforward to honour.

| Key | Authority | Jurisdiction | Cadence | Grade |
|---|---|---|---|---|
| `eur-lex-sanctions` | EUR-Lex restrictive measures | EU | daily | A1 |
| `eu-consolidated-list` | EU Consolidated Financial Sanctions List | EU | daily | A1 |
| `ofac-sdn` | OFAC SDN + Consolidated | US | daily | A1 |
| `bis-entity-list` | BIS Entity / Denied Persons | US | weekly | A1 |
| `uk-ofsi-consolidated` | OFSI Consolidated List | GB | daily | A1 |
| `seco-sanctions` | SECO sanctions list | CH | weekly | A1 |
| `ua-nsdc-sanctions-legal-entities` | NSDC State Register of Sanctions — legal entities | UA | weekly | B2 |
| `ua-nsdc-sanctions-individuals` | NSDC State Register of Sanctions — individuals | UA | weekly | B2 |
| `ua-nsdc-sanctions-vessels` | NSDC State Register of Sanctions — vessels | UA | weekly | B2 |

Grades are **triage only** — they set scrutiny depth and review priority and
are architecturally barred from touching any proposition's truth, likelihood
or confidence (DR-0027, EVID-008).

## The judgment calls, so you can disagree with the reasoning

**Why EUR-Lex and the consolidated list are both registered.** They are not
redundant. The instrument is the legal act; the consolidated list is an
administrative compilation of it. DR-0038 makes instruments carry lifecycles,
and a designation's history is reconstructible from instruments in a way it is
not from a snapshot list. Their dependence is declared (below), so they never
count as two lines.

**Why whole-file captures rather than parsing on ingest.** Each list is
captured whole, forming a capture series (DR-0074), and nothing is parsed into
structured fields at collection time. Designation records name individuals with
dates and places of birth; DR-0071(b) forbids automatic promotion of personal
data into queryable structure. Structuring is a Gate 2 decision under POL-0001
§4, taken per record, not a side effect of fetching.

**Why the `ua-nsdc-sanctions` candidates are graded B2, not A1.** They are a party to the conflict
publishing about its adversary. The grade means "read with the care a
belligerent source deserves" — it does not mean less likely to be true, and it
cannot reach any assessment. A1 for the EU and US lists is not a claim that
those bodies are right; it is a claim that they reliably publish what they
have decided.

**Why Switzerland is included.** Its non-EU status makes divergence between
Swiss and EU measures evidentially interesting in itself (§68–70, financial
flows). Where it mirrors the EU it is one line, not two — declared below.

**Why `may-preserve` for SECO and NSDC.** Their rights positions are
unverified. The conservative default is preserve-only, no redistribution,
until someone checks (§14). Claiming redistribution rights the project has not
confirmed is the kind of error that is cheap to avoid and expensive to make.

**What is deliberately excluded.** Interpretive guidance, FAQs, press releases
and enforcement notices. They have a different evidentiary character from legal
instruments and belong in their own registrations with their own scope rules —
not folded into these.

## Declared dependence (DR-0028)

Stated once here rather than rediscovered per item. **Five lists naming the
same person are not five independent confirmations** — in part they are one
designation propagating (§36).

| Dependent | Relation | Depends on |
|---|---|---|
| `eu-consolidated-list` | derives-from | `eur-lex-sanctions` |
| `uk-ofsi-consolidated` | common-evidentiary-origin | `eu-consolidated-list` |
| `seco-sanctions` | common-evidentiary-origin | `eu-consolidated-list` |

Declaring dependence is an analytic judgment, so `--commit` requires
`--agent`: the claim carries an asserter like any other assertion.

Not declared, deliberately: OFAC and the EU list. They designate
independently and often diverge, and asserting dependence where none is
established would understate corroboration as badly as assuming independence
overstates it.

## Registration classes (DR-0103)

Source authorization scales by class, not by source: the founder approves a
class once and individual sources register under it by inheritance
(`class:` in the candidate YAML), with per-source exceptions stated
explicitly as overrides. This file's `classes:` section carries six classes,
one commitment DR-0103's own "Next step" asked for — the founder's ruling
on the grouping principle is **jurisdiction first, topic second**, matching
[WP 3.7](../docs/phase-3/working-papers/wp-3.7-registration-classes.md) §7's
recommendation:

| Class | Jurisdiction | Topic | Members |
|---|---|---|---|
| `EU-institutional-sanctions` | EU | sanctions | `eur-lex-sanctions`, `eu-consolidated-list` |
| `US-institutional-sanctions` | US | sanctions | `ofac-sdn` |
| `US-institutional-export-control` | US | export control | `bis-entity-list` |
| `UK-institutional-sanctions` | GB | sanctions | `uk-ofsi-consolidated` |
| `CH-institutional-sanctions` | CH | sanctions | `seco-sanctions` |
| `UA-state-investigations` | UA | state investigations | `ua-nsdc-sanctions-legal-entities`, `ua-nsdc-sanctions-individuals`, `ua-nsdc-sanctions-vessels` |

Jurisdiction first because the policy fields that vary most — rights basis,
default access, retention — turn on *whose* publication this is, not what
kind of list it is; two sanctions lists from different jurisdictions carry
different copyright and reuse regimes, while two lists from the same
jurisdiction (here, US sanctions vs. US export control) mostly diverge only
in scope and redistribution terms. The one class split by topic within a
jurisdiction, `US-institutional-export-control` vs.
`US-institutional-sanctions`, exists because BIS's export-control lists
carry a narrower redistribution term than OFAC's sanctions lists, which a
single US class would have flattened.

**Every source in this file that belongs to a class references it**
(`eur-lex-sanctions` and `eu-consolidated-list` reference
`EU-institutional-sanctions`; `ofac-sdn` references
`US-institutional-sanctions`; `bis-entity-list` references
`US-institutional-export-control`; `uk-ofsi-consolidated` and
`seco-sanctions` reference their respective one-member classes;
`ua-nsdc-sanctions-legal-entities`, `ua-nsdc-sanctions-individuals` and
`ua-nsdc-sanctions-vessels` all reference the shared
`UA-state-investigations` class). Several of these sources needed explicit
per-source overrides on top of their class, because their actual verified
or approved values differ from the class default in policy-significant
ways:

- **`capture_format`.** The class default is `warc` (right for a source
  whose collection captures a browsing session, like `eur-lex-sanctions`),
  but `eu-consolidated-list`, `bis-entity-list`, `uk-ofsi-consolidated` and
  `seco-sanctions` were all verified as a bare-body HTTP fetch of a whole
  list file (DR-0006/DR-0067's capture-format guardrail: "a `warc` source
  gets a WARC record, an `http` source a bare body recorded as such").
  Inheriting the class default without an override would silently
  misrecord how each was actually verified — `ofac-sdn` already carried
  this override before classes existed; the other three did not reference
  a class at all until this pass wired them up with the same override.
- **`rights_permission`.** `bis-entity-list` was verified and (partially)
  approved under `may-redistribute`, not the `US-institutional-export-control`
  class's `may-provide-subscribers` default (written for a BIS
  subscriber-only term this source does not carry). `seco-sanctions` and
  all three `ua-nsdc-sanctions-*` candidates carry the conservative
  `may-preserve` — DR-0098 for `seco-sanctions`, candidate status set for
  the NSDC candidates — because their rights positions are unverified;
  their classes' `may-redistribute` default is for sources whose reuse
  basis **is** known (the EU/UK/US institutional publishers). Inheriting
  either class default without an override would state an authorization
  no DR ever gave.
- **`rights_basis`** (prose) and, for all three `ua-nsdc-sanctions-*`
  candidates, `grade_source_reliability`/`grade_item_credibility` — kept
  as the exact text or triage values each source was verified, approved
  or drafted against, rather than the class's more generic wording or
  (for the UA class) an unreconciled B2/"2" pairing these candidates have
  not themselves earned (DR-0027: triage only, never truth).

**Do not remove an override to "clean up" duplication with its class**
without first checking `python3 sources/register.py --dry-run` (or the
`merge_class_defaults` output) shows the same merged value before and
after — that is exactly the silent-misrecording failure mode this section
exists to prevent recurring.

Scope, for now: classes are defined per candidate file (WP 3.7 §7 sub-Q3),
not shared across files; if a future file's classes duplicate one here,
harmonizing is a later, visible decision, not an automatic one.

## What registering these commits you to

`--dry-run` prints this; it is repeated here because each item is a real
obligation rather than a formality.

- **Reading capacity in de, fr, it and uk at Gate 2.** No translations are
  seeded (DR-0081). Registering any of the three `ua-nsdc-sanctions-*`
  candidates in particular commits the project to Ukrainian.
- **Permanent retention for all nine candidates**, meaning indefinite
  fixity checking on a 180-day cadence (DR-0005).
- **Resolving the unverified rights positions** for `seco-sanctions` and
  all three `ua-nsdc-sanctions-*` candidates (§14).
- **A first collection run.** Six of nine now have a verified, fetched
  locator (one, `bis-entity-list`, only partially) — see "Which locators
  are verified" below for which is which; the `ua-nsdc-sanctions-*` three
  need human-assisted browser access at collection time, not a bare
  `register.py --commit`, since automated fetches of their locators are
  Cloudflare-blocked.

## Which locators are verified

**Six are (two partially), one is not.** On 2026-09-08 the files behind
`eu-consolidated-list` and `ofac-sdn` were fetched, digested twice, and
acquired end to end by the real collector into a throwaway database
([verification record](../docs/sources/verification-eu-consolidated-list-ofac-sdn.md),
proposal [DR-0093](../docs/decision-records/DR-0093-first-source-registrations.md)).
On 2026-09-12 `uk-ofsi-consolidated` was verified the same way, fully, and
`bis-entity-list` partially — only its Denied Persons List half has a
verified locator; the Entity List half does not, because BIS publishes it
as CFR text, not a standalone file, and the one working alternative found
(Commerce's Consolidated Screening List) merges in OFAC's own data and was
deliberately not substituted
([verification record](../docs/sources/verification-bis-dpl-ofsi-consolidated.md)).
On 2026-09-13 `seco-sanctions` was verified the same way, fully, on a
second attempt — the earlier session's six URL guesses had missed that the
real file lives on a separate host (`sesam.search.admin.ch`, not
`seco.admin.ch`), found only by following the site's own navigation
([verification record](../docs/sources/verification-seco-sanctions.md)).
On 2026-09-20 `eur-lex-sanctions` was verified partially — the two
foundational instruments (Council Regulation 269/2014, Council Decision
2014/145/CFSP) identified and fetched, rehearsed through the real collector
(2 discovered, 2 acquired, 0 failed), but with an open question this
session could not settle: the consolidated-text locator carries a dated
CELEX suffix that advances roughly monthly as the Council amends the
regime, so a registered `run_locator` will need periodic re-verification in
a way none of the other six candidates do
([verification record](../docs/sources/verification-eur-lex-sanctions.md)).
`ua-nsdc-sanctions` was unverified through 2026-09-21: the specific
register it should point to was identified (`drs.nsdc.gov.ua`, the NSDC's
own "State Register of Sanctions," found via rnbo.gov.ua's own
navigation), but that register returned HTTP 403 behind a Cloudflare
managed challenge from every automated session, the same block class
found on Légifrance, and a 2026-09-21 Wayback-history check (3 489
historical captures, last seen 2026-08-24, no bulk-export file among
them) pointed toward a search-UI-only-application hypothesis without
confirming it. **Unblocked 2026-09-22/23** by human-assisted (founder)
browser access, which reached `drs.nsdc.gov.ua`'s "Data integration"
section directly — the search-UI-only hypothesis was wrong: the register
exposes a structured bulk-export API,
`/registry-api/subjects/export/<class>/csv?lang=uk`, confirmed working
for all four entity classes (Legal entities, Individuals, Vessels,
Aircraft). Each of the three non-empty classes now has a confirmed
`run_locator`, confirmed field structure, and a row count matching the
register exactly (9,682 / 13,900 / 888); Aircraft's endpoint was confirmed
to genuinely return 0 records. Drafted as three separate candidates
rather than one (see "Registration classes" above), all validating under
`sources/register.py --check`, none yet registered
([verification record](../docs/sources/verification-ua-nsdc-sanctions.md)).
`eur-lex-sanctions` was **registered and collected 2026-09-21**
([`DR-0105`](../docs/decision-records/DR-0105-eur-lex-sanctions-registration.md)):
2 discovered, 2 acquired, 0 failed, 16 199 485 bytes preserved, 0
documentary assertions. The other three approved sources
(`uk-ofsi-consolidated`, `bis-entity-list`, `seco-sanctions`) remain
approved-but-unexecuted — registering any of them, like it was for the
first three, is the founder's act, per source.

These entries carry three optional fields the registry does not store:

| Field | Meaning |
|---|---|
| `locator_verified` | ISO date the run locators were last fetched successfully |
| `run_locators` | the exact URLs a first run passes to the collector — refused without a `locator_verified` date, and refused unless absolute `https://` |
| `verification_note` | where the record of that fetch lives |

`--dry-run` prints `(verified <date>)` or `(UNFETCHED)` per source, and
adjusts what it says the first run commits you to.

As of 2026-09-23, every candidate in this file carries a confirmed
`locator_verified` date and `run_locators` — none remains an unfetched
claim. `eur-lex-sanctions` is the one exception worth flagging even so:
its `run_locators` carry a dated CELEX suffix that advances roughly
monthly, so `locator_verified` records when it was last checked, not a
promise it stays current (see its candidate comment and verification
record).

That is expected and handled. A 404 on first collection is a **recorded failed
acquisition** (PRES-007), not a system fault, and the coverage record will say
plainly what was sought and not obtained (DR-0070, §57). Correcting a locator
is a routine registry edit. Treat the first run against an unverified source
as locator verification; it is the cheapest way to find out which are right.

Corrections already made on that basis: the EU consolidated list's
locator was the FSF application root, which answers 401 without an EU
Login session, and is now the public XML file URL; BIS's landing locator
now redirects to `bis.gov`, a domain migration since the candidate was
drafted; SECO's landing page never had a direct file link at all, and
the real download lives on a different host entirely
(`sesam.search.admin.ch`), found by navigating rather than guessing.

## Verification

32 tests. The refusals are the substance:

- a candidate missing any policy field is refused rather than defaulted —
  DR-0067's point is that collection policy is *stated*, and a silent default
  is a policy nobody chose;
- an open-ended scope is refused (DR-0071(a));
- a redistribution claim whose basis nobody flagged as unreviewed is refused
  (§14), because silence there reads as "checked and fine";
- a graphic-content source defaulting to public is refused (PRES-012);
- a dependence declaration with no reasoning is refused (DR-0028);
- **registration collects nothing** — a full registry and an empty archive is
  the correct state immediately afterwards;
- run locators with no verification date, a verification date that is not
  a date, or a run locator that is not absolute `https://` are refused — a
  verification that cannot be read is not a verification.

The scope, rights and verification-date checks were verified by sabotage:
removing any of them lets the corresponding bad candidate through and the
suite fails.

**Dependence on an already-registered source is recorded, not silently
dropped** (fixed 2026-09-12,
[DR-0096](../docs/decision-records/DR-0096-second-source-registrations.md)):
`commit()` resolves a declared link's other end against the database by
name when it is not in the current `--only` batch, and a link neither end
of which resolves prints which end could not be found rather than
vanishing. Verified by sabotage: reverting either half of the fix (the
database lookup in `commit()`, or `validate()`'s `known_keys` parameter)
turns one check red each.

**`register.py --commit` hands `commit()` the merged view** (fixed
2026-09-19): `commit()` reads each policy field straight off the dict it is
given, and since 2026-09-17 every shipped candidate references a class, so
its fields exist only after `merge_class_defaults()`. `main()` computed that
merged view for `describe()` but passed the *unmerged* `sources` to
`commit()` — a bare `KeyError` on the archive server the first time any of
the three approved registrations was actually executed, invisible to every
test above because they call `commit()` directly with fixture data. A new
end-to-end check runs `register.py --commit --only ofac-sdn` as a subprocess
against the test database and reads the registered row back. Verified by
sabotage: reverting `main()` to pass `sources` turns exactly that check
red. The same `load_candidates()` three-value return had also broken
`collector/run.py`'s `find_candidate()` (now merges before returning) and
the setup of this suite and `collector/tests/test_run.py`.

A separate session, branched before this fix merged to `main`, independently
rediscovered the identical bug on 2026-09-20 while verifying
`eur-lex-sanctions`, with its own redundant fix to `register.py` and
`test_register.py`. Merging the two branches kept this (2026-09-19) fix,
the more thorough of the two, and discarded the duplicate.

**A re-run of `register.py --commit` is a no-op per source, not a duplicate**
(fixed 2026-09-24, [#62](https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues/62)).
The third `register.py` bug found by *executing* a registration rather than by
testing one, and the worst of the three in effect: on 2026-09-22 a repeated
`--commit` inserted a second `source` row with a fresh uuid for each
strike-tracking candidate, and because `collector/run.py`'s
`resolve_registered_source()` identifies a source by `(name, locator)` and
refuses an ambiguous match rather than guessing which authorisation applies,
**the duplicate disabled the two sources that had just been registered**
(DR-0106, *Executed* step 1). It was cleared by hand — a read-only query
confirmed neither duplicate had any dependent `collector_run` row before
either was deleted — and nothing stopped it recurring.

Enforced in both places, as a rule that matters must be:

- **In code**, `commit()` calls `registered_id()` first and, on a hit, records
  the existing id, prints `already registered, not re-inserted`, and skips the
  insert. Returning the existing id rather than dropping the key keeps
  dependence links resolvable through `resolve()`.
- **In the DDL**, `source` gains `CONSTRAINT source_identity_unique UNIQUE
  NULLS NOT DISTINCT (name, locator)`, so the store refuses what the code
  would if the code were wrong. `NULLS NOT DISTINCT` because a null locator is
  one locator, not a wildcard — under the default, two null-locator rows
  sharing a name would both be admitted, which is the same ambiguity.
- **A silent no-op would be its own trap**, so a re-run whose candidate file
  has since been edited reports each differing authorising field
  (`collection_method`, `capture_format`, the two tiers, `rights_permission`)
  as `NOT updated` rather than appearing to apply it. Re-registering a source
  whose policy changed is a founder act per source (DR-0093 §3), never a
  `--commit` side effect.

Verified by sabotage, one rule at a time, each turning exactly the expected
checks red and nothing else:

| Sabotage | Result |
|---|---|
| `registered_id()` always returns `None` (the code guard) | 5 checks red |
| the DDL constraint removed entirely | 2 checks red |
| `UNIQUE NULLS NOT DISTINCT` → plain `UNIQUE` | 1 check red — the null-locator case only |
| the `_report_drift()` call removed | 1 check red |

`sources/tests/test_register.py` is now 39 checks, up from 32. Six are new,
and one of them runs `register.py --commit` **twice** as a subprocess — the
operator's real entry point, and the only shape of test that would have caught
this, since every other check calls `commit()` directly. Two checks needed
`try`/`except psycopg.errors.UniqueViolation` around their `commit()` calls:
without the code guard the DDL refuses the insert, and an uncaught violation
would abort the suite and leave every later check unreported.

**A limitation, stated rather than left to be discovered:** identity here is
`(name, locator)`, because that is the pair the collector resolves on. A
candidate whose `locator` changes is correctly seen as a different source; a
candidate whose **`name`** changes looks unregistered and would be inserted
afresh, leaving two rows for one real source under two names. Nothing in this
fix prevents that, and it is not a bug in it — making the registry's identity
something more stable than a display name would be a change to DR-0067's
schema and a founder decision, not a side effect of closing #62.

**Outstanding, and it matters:** this is a DDL change, and the project has no
schema-migration mechanism for a live database — only "drop and rebuild from
DDL," which the suites do and the archive server cannot
([#57](https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues/57)).
**The archive server's `source` table therefore still has no such
constraint**, so until someone adds it there the store-side half of this fix
protects the test databases only. Unlike most schema changes this one needs no
rebuild — a single `ALTER TABLE source ADD CONSTRAINT source_identity_unique
UNIQUE NULLS NOT DISTINCT (name, locator);` suffices, and it will succeed only
if no duplicate pair is present, which is itself worth knowing.

**Not verified:** for the three still-unfetched candidates
(`eur-lex-sanctions`, `seco-sanctions`, `ua-nsdc-sanctions`), that the
source exists at the address given or that the formats are as assumed;
for all seven, that the rights positions are correct — that is a legal
question (POL-0001 §10), not a network one.

## War-fact candidates (`war-facts.yaml`, started 2026-09-21)

The first candidates outside the sanctions/export-control thematic area,
following the founder's redirection toward war-fact subject matter:
territorial control / military operations, chosen first over civilian-harm
or war-crimes categories for its lower personal-data sensitivity. Two
complementary sources — `isw-orca` (the narrative: ISW's daily assessment
of why the front line moved) and `deepstatemap` (the geometry: a live
GeoJSON API of current control polygons) — both verified and rehearsed
through the real collector, neither registered.
[Verification record](../docs/sources/verification-war-facts-first-two.md)
has the full account, including what is not yet settled: DeepStateMap's
actual licensing (not found anywhere on the site), ISW's daily
re-verification burden (a new dated URL every day, more demanding than
`eur-lex-sanctions`'s monthly cadence), and a third candidate in the same
category (LiveUAmap) that this session's network could not reach (403).

## Strike-tracking candidates (`strike-tracking.yaml`, started 2026-09-21)

The founder's actual stated purpose for this project: "to come the closest
possible to record EVERY SINGLE MISSILE, DRONE, that fell on each side and
their effect" — not a category alongside territorial control, the point of
the archive. Two official Ukrainian government Telegram channels, one per
direction: `kpszsu` (Air Force Command — near-real-time incoming
drone/missile tracking over Ukraine) and `generalstaffzsu` (General Staff —
periodic summaries of Ukrainian strikes on Russia/occupied territory).
Both verified and rehearsed through the real collector, neither registered.
**The critical caveat**, stated in the candidate file's own header and in
full in the
[verification record](../docs/sources/verification-strike-tracking-first-two.md):
registering these sources gets ongoing coverage of *new* posts going
forward, not the channels' existing ~79 000-message history. A full
backfill is technically possible (Telegram's `?before=` pagination reaches
the whole history) but is real, separate engineering — a paginated crawl
of thousands of requests, closer in scope to A3's WARC bulk-ingest path
than to a normal registration — not something registering the source
does automatically. Also flagged: both sources are Ukraine's own official
voice on both directions of the war; a fuller record eventually needs
independently verified Russian-side sources too.

## Census tooling (`census.py`, WP 3.4 §4.1 Track A item A2)

A separate tool from registration, built for a separate purpose:
`census.py` discovers *candidate* domains for a `docs/sources/` prose note
to be written about, by querying Common Crawl's crawl index and the Wayback
Machine's CDX index for what they have already captured under a domain
pattern. It never fetches a page from a candidate domain — only from the
index service itself — so DR-0071(a)'s registered-sources rule does not
apply to it (nothing is collected), and it writes to no database.

```bash
python3 sources/census.py --domain example.gov.ua --index wayback
python3 sources/census.py --domain example.gov.ua --index common-crawl \
        --crawl-id CC-MAIN-2024-46   # current id: index.commoncrawl.org/collinfo.json
```

Output is a ranked, deduplicated markdown table of hosts, each with the
capture count, first/last-seen dates, and which index reported it — WP
3.4 §4.1's "ranked list of candidate domains with the evidence for each."
Ranking by capture count is triage only (DR-0027's distinction, applied to
domain discovery): more captures means better attested, never truer.

Only the two evidence sources WP 3.4 §4.1 groups as "indices" are built.
The other four it names for A2 — Wikipedia citation graphs of the war
articles, sanctions-authority link graphs, published OSINT source lists,
academic bibliographies — have no stable query API and are editorial
research tasks, left for separate work.

### What is verified, and what is not

28 tests in `sources/tests/test_census.py`, no database needed. The
aggregation/ranking logic (`census()`) is exercised through a fixture index
client; the real Common Crawl and Wayback response parsers are exercised
against hand-built payloads matching each service's documented shape — the
same "test the parsing, not the network" split `test_warc_ingest.py` uses
for WARC records. Verified by sabotage: removing the `IndexQueryResult`
"a failure must explain itself" guard (§28) turns one check red; breaking
the by-host deduplication key crashes the suite outright on a `KeyError`
rather than passing quietly. Both were restored and re-verified green.

**`CommonCrawlIndexClient` and `WaybackCdxClient` completed their first live
queries 2026-09-17.** Every prior session's egress proxy had reset the
connection to `index.commoncrawl.org` (`collinfo.json` and a direct index
query alike — `curl` and Python's own `urllib` failing identically,
`ECONNRESET`) and timed out on `web.archive.org` outright, the same host
DR-0094's drafting session also found blocked. This session's network
reached both. Run:

```bash
python3 sources/census.py --domain rnbo.gov.ua --index wayback
python3 sources/census.py --domain rnbo.gov.ua --index common-crawl \
        --crawl-id CC-MAIN-2024-46
```

against `rnbo.gov.ua` (the `ua-nsdc-sanctions` publisher). Wayback returned
25 hosts, ranked by capture count, first/last seen 2012–2026; the entry
`sanctions-t.rnbo.gov.ua` (73 captures, 2021-04-22 to 2022-05-20) is worth a
look for `ua-nsdc-sanctions`'s eventual instrument-identification work, but
that identification itself is legal/editorial judgment, not something this
run does — census only counts what an index has captured, it does not fetch
or interpret a candidate host (see "What registering these commits you to"
below: registering `ua-nsdc-sanctions` is a separate, still-open decision).
Common Crawl returned 2 hosts for the same domain. Both clients are exercised
against their documented API shape in the fixture-based suite and now,
separately, against a live response for the first time; this is not a
durable fix — **network access varies by session** (CLAUDE.md's own
caution) — so a future session finding these hosts unreachable again is not
a regression, just the same variability recurring.
