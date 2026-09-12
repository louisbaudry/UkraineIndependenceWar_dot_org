# Source registration

Candidate sources for the first real collection, drafted against the DR-0067
registry schema. **Two are registered** on the archive server as of
2026-09-09 under DR-0093 (`eu-consolidated-list`, `ofac-sdn`); the other five
remain proposals for the founder to accept, amend, or reject — per source,
not as a block. Registration lives in the server's database, not in this
file: the file is the candidate, the row is the registration.

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
founder chose. Two of them, `eu-consolidated-list` and `ofac-sdn`, are
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
| `ua-nsdc-sanctions` | NSDC decisions and enacting decrees | UA | weekly | B2 |

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

**Why `ua-nsdc-sanctions` is graded B2, not A1.** It is a party to the conflict
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

## What registering these commits you to

`--dry-run` prints this; it is repeated here because each item is a real
obligation rather than a formality.

- **Reading capacity in de, fr, it and uk at Gate 2.** No translations are
  seeded (DR-0081). Registering `ua-nsdc-sanctions` in particular commits the
  project to Ukrainian.
- **Permanent retention for all seven**, meaning indefinite fixity checking
  on a 180-day cadence (DR-0005).
- **Resolving the unverified rights positions** for `seco-sanctions` and
  `ua-nsdc-sanctions` (§14).
- **A first collection run against locators none of which have been fetched.**

## Which locators are verified

**Two are, five are not.** On 2026-09-08 the files behind
`eu-consolidated-list` and `ofac-sdn` were fetched, digested twice, and
acquired end to end by the real collector into a throwaway database; the
record is
[docs/sources/verification-eu-consolidated-list-ofac-sdn.md](../docs/sources/verification-eu-consolidated-list-ofac-sdn.md)
and the proposal to register them is
[DR-0093](../docs/decision-records/DR-0093-first-source-registrations.md).
Those two entries carry three optional fields the registry does not store:

| Field | Meaning |
|---|---|
| `locator_verified` | ISO date the run locators were last fetched successfully |
| `run_locators` | the exact URLs a first run passes to the collector — refused without a `locator_verified` date, and refused unless absolute `https://` |
| `verification_note` | where the record of that fetch lives |

`--dry-run` prints `(verified <date>)` or `(UNFETCHED)` per source, and
adjusts what it says the first run commits you to.

**The other five remain claims.** Their landing pages answered a
reachability probe (EUR-Lex with an empty 202 challenge page; BIS now
redirects to `bis.gov`), but no file has been fetched from any of them. Each
URL is drawn from documentation and prior knowledge, and some are probably
wrong: sanctions authorities move endpoints, and several of these publish
through interfaces that have changed more than once since 2014.

That is expected and handled. A 404 on first collection is a **recorded failed
acquisition** (PRES-007), not a system fault, and the coverage record will say
plainly what was sought and not obtained (DR-0070, §57). Correcting a locator
is a routine registry edit. Treat the first run against an unverified source
as locator verification; it is the cheapest way to find out which are right.

One correction already made on that basis: the EU consolidated list's locator
was the FSF application root, which answers 401 without an EU Login session.
It is now the public XML file URL.

## Verification

27 tests. The refusals are the substance:

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

**Not verified:** for the five unfetched candidates, that the source exists
at the address given or that the formats are as assumed; for all seven, that
the rights positions are correct — that is a legal question (POL-0001 §10),
not a network one.

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

**Not verified: `CommonCrawlIndexClient` and `WaybackCdxClient` have never
completed a live query.** This session's egress proxy resets the connection
to `index.commoncrawl.org` on every attempt (`collinfo.json` and a direct
index query alike — `curl` and Python's own `urllib` both fail identically,
`ECONNRESET`) and times out on `web.archive.org` outright, the same host
prior sessions and DR-0094's drafting session found blocked. Both clients
are written to each service's documented API shape, not exercised against a
live response. This matches WP 3.4 §3's own framing: "sessions are for
building and reviewing the pipeline, not for being the crawler" — real
execution is meant to happen where a session has the network access this
one does not, the same pattern `collector/fetch.py`'s `HttpFetcher` followed
before the 2026-09-08 verification session confirmed it against real
publishers.
