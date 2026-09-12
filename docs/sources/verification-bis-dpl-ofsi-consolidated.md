# Verification record — BIS Denied Persons List and UK OFSI Consolidated List

**Status:** Verification record for two of the five remaining candidate
registrations. Nothing here is registered, nothing is collected into the
project's archive, and nothing is enacted by this document — registering
these, like `eu-consolidated-list` and `ofac-sdn` before them, is the
founder's act, per source (CLAUDE.md standing ruling).
**Verified:** 2026-09-12, ~16:30–16:45 UTC, from this session's container.
**Candidates:** `bis-entity-list` (partially — see §3) and
`uk-ofsi-consolidated` (fully) in
[`sources/candidates/sanctions-authorities.yaml`](../../sources/candidates/sanctions-authorities.yaml).
This record does not touch `eur-lex-sanctions`, `seco-sanctions`, or
`ua-nsdc-sanctions` — see §5 for what was found about each and why none of
the three was carried further today.

This session's egress proxy could not reach `index.commoncrawl.org` or
`web.archive.org` (see `sources/README.md`'s "Census tooling" section), but
reaches all five of these candidates' domains without difficulty — network
access is per-host, not a single allow/deny switch, consistent with what
CLAUDE.md's "Environment notes" already says.

---

## 1. What was done, in order

1. Each candidate's landing locator was fetched to confirm reachability.
2. For the two candidates carried further, the landing page (and, where the
   first page didn't have it, a linked sub-page) was searched for the actual
   downloadable file — a direct URL, not the candidate's landing page —
   the same distinction `eu-consolidated-list`'s own locator makes between
   the FSD application root (401 without a login) and the public file URLs.
3. Each file found was fetched twice, minutes apart, with its SHA-256
   computed both times, to check the served bytes are stable — not a moving
   target a real run could catch mid-update.
4. **Rehearsal.** A throwaway PostgreSQL database was built from
   `schema/0*.sql`. The two sources were inserted directly (not through
   `sources/register.py`, since the candidate file did not yet carry
   `run_locators` for them at the point this rehearsal ran — a difference
   from the EU/OFAC rehearsal's use of the real `register.commit()`, noted
   here rather than left implicit). The real `Collector`
   (`collector/pipeline.py`, with the two-agent split
   `DR-pending-collection-run-two-agents` added 2026-09-12) was run with the
   real `HttpFetcher` against the live URLs, into a throwaway OCFL root.
   Digests, byte counts, agent attribution and documentary-assertion counts
   were read back from the database. Database and storage were then
   destroyed; the script was a verification instrument, not a tool, and is
   not part of the repository.

## 2. UK OFSI Consolidated List of Financial Sanctions Targets

The candidate's `locator`
(`https://www.gov.uk/government/publications/financial-sanctions-consolidated-list-of-targets`)
is a gov.uk publication page, not a file. It links to a sub-page
(`.../consolidated-list-of-targets`), which links the actual files, hosted
on OFSI's own blob storage, not gov.uk:

| File | URL |
| --- | --- |
| CSV | `https://ofsistorage.blob.core.windows.net/publishlive/2022format/ConList.csv` |
| XML | `https://ofsistorage.blob.core.windows.net/publishlive/2022format/ConList.xml` |
| (also linked, not fetched) | `.../2022format/ConList.txt` |

Both files fetched twice, 2026-09-12, digests identical across both fetches:

| File | Size | SHA-256 | Content-Type | Last-Modified |
| --- | --- | --- | --- | --- |
| ConList.csv | 16 641 139 bytes | `9585695391b51f72ca9eae1b6671e1f81fb1fa6e21a1661dad346636f2320c7f` | `text/csv` | 2026-06-03 |
| ConList.xml | 54 098 673 bytes | `4d14d0d8a5584fffd123c378938692b1c6331388e0ae658e82084ef76f7159e6` | `text/xml` | 2026-06-03 |

Both acquired end to end by the real collector in the rehearsal: 2
discovered, 2 acquired, 0 failed, 70 739 812 bytes total (exactly the sum of
the two files above). Stored digests matched the independently-computed
ones exactly.

**Proposed `run_locators`:** both CSV and XML — the TXT variant is
redundant with the CSV for this project's purposes and was not fetched.

## 3. BIS Denied Persons List — the Entity List half of this candidate is still open

The candidate `bis-entity-list` is named for **two** BIS lists: the Entity
List and the Denied Persons List. Only the second has a clean, structured
file locator as of this session.

**Denied Persons List (DPL) — found and verified.** The candidate's
`locator` (`https://www.bis.doc.gov/`) now redirects to `https://www.bis.gov/`
(a domain migration since the candidate was drafted 2026-08-26). From
there, `/denied-persons-list` redirects to a guidance page linking the
actual file:

`https://media.bis.gov/sites/default/files/dpl_04142026.csv`

Fetched twice, digest identical: 110 427 bytes,
`365c78e50988c608b1496d4c57c34bb380f75930a71920aff658ac91551cf951`,
`Content-Type: text/csv`, `Last-Modified: 2026-04-14`. Acquired end to end
by the real collector in the rehearsal: 1 discovered, 1 acquired, 0 failed,
110 427 bytes — digest matched exactly.

**Entity List — not found as a structured file.** BIS's own site
(`/entity-list`) redirects to the regulation text itself (EAR §744.16,
Supplement No. 4 to Part 744), not a data file; the linked documents from
that page are PDFs unrelated to the list content (a SORN notice, a quality
guidance PDF). The Entity List's authoritative form is CFR text, which
`eCFR.gov`'s API can plausibly serve structured, but two attempts against
that API in this session did not succeed (one `406`, one redirect not
followed further) and were not pursued past that, since guessing further
at an unfamiliar API's parameters risks recording something that only
looks verified. **One alternative exists but was deliberately not used
here:** the Commerce Department's Consolidated Screening List
(`data.trade.gov/downloadable_consolidated_screening_list`) is a real,
working ~34 MB JSON file that includes BIS's Entity List — but it also
merges in OFAC's own lists and others' into one file. Registering that as
"the BIS source" would misattribute OFAC-sourced entries to BIS and
duplicate `ofac-sdn`'s own coverage without a declared-dependence relation
for it (DR-0028) — worse than leaving the Entity List unverified a while
longer.

**Proposed `run_locators` for now: DPL only.** The candidate's scope names
both lists; registering it with only the DPL locator would under-deliver
what `bis-entity-list` promises by name. This is a founder call, not a
technical one: register now with DPL alone (and expand `run_locators` later
once the Entity List's own locator is found), or hold the whole candidate
until both are ready.

## 4. Two agents, exercised in this rehearsal

The rehearsal used `Collector`'s two-agent constructor
(`DR-pending-collection-run-two-agents`, added earlier today): a person
agent of record on `collector_run`, and the self-registered
`collector-pipeline` software agent (version `0.1.0`) on every preservation
event. Read back after both runs: every `preservation_event.agent_id` was
the software agent, never the person — the same invariant
`collector/tests/test_pipeline.py` and `test_run.py` check with fixtures,
now also true against two real, live sources. Zero documentary assertions
were created by either run (DR-0066, Principle 5), same as every other
collection to date.

## 5. The other three candidates

Not carried past a landing-page reachability check today — each raises a
question that either needs more work or is a founder judgment call, not a
guess to make silently.

| Candidate | Landing locator | Result | Why not carried further |
| --- | --- | --- | --- |
| `eur-lex-sanctions` | `https://eur-lex.europa.eu/` | 200 (the 2026-09-08 verification record found 202/empty from a different session) | The candidate's scope is specific legal instruments (regulations, Council Decisions) under the Ukraine/Russia regime, not one downloadable file — identifying the right instrument set is legal research, not a URL to find |
| `seco-sanctions` | `https://www.seco.admin.ch/` | 200 after redirect to `/de` | Six URL guesses at SECO's sanctions-list file and site-search endpoints returned 404/500/no-links; the site's navigation is not readable from a plain fetch. Needs proper site exploration this session did not complete |
| `ua-nsdc-sanctions` | `https://www.rnbo.gov.ua/` | 200 | A page-based site (matching its `capture_format: warc`), not a single file. Its homepage and `/ua/Diialnist/` (Activity) section carry no link recognisably about sanctions in a shallow check. Finding the right decisions/decrees to capture is the same kind of editorial identification EUR-Lex needs, in Ukrainian |

## What has not been verified

Everything not stated as fetched above: the Entity List's own file, and
anything from EUR-Lex, SECO, or NSDC beyond their landing pages responding.
No claim is made about the rights position for any of the five — all
remain `NOT LEGALLY REVIEWED` (SECO and NSDC additionally `may-preserve`
only, per the candidate file's existing conservative default) pending
POL-0001 §10.

---

**AI provenance (§80).** Drafted by Claude (`claude-sonnet-5`) on
2026-09-12, from fetches and one rehearsal performed in this session. Every
figure above comes from a response received here and is reproducible from
the URLs given. This is a verification record, not a Decision Record; it
enacts nothing and authorises no collection.
