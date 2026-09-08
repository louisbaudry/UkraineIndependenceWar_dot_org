# Verification record — EU Consolidated Financial Sanctions List and OFAC SDN

**Status:** Verification record for two candidate registrations. Nothing here
is registered, nothing is collected into the project's archive, and nothing
is enacted. The Decision Record that would act on this is
[DR-0087](../decision-records/DR-0087-first-source-registrations.md)
(proposed).
**Verified:** 2026-09-08, ~09:20–09:40 UTC, from this session's container.
**Candidates:** `eu-consolidated-list` and `ofac-sdn` in
[`sources/candidates/sanctions-authorities.yaml`](../../sources/candidates/sanctions-authorities.yaml).

This record exists because, until today, **no locator in the candidate file
had ever been fetched** and **the collector's fetch layer had never completed
a live request** (collector/README.md). Both statements are now false for
these two sources, and the rest of this document says exactly how far that
goes and where it stops.

---

## 1. What was done, in order

1. Each candidate locator, and the file URLs behind it, was requested with
   `curl`, presenting an identified User-Agent naming this project's
   repository. Status, content type, size, redirect chain and final URL were
   recorded.
2. Every file that a first run would collect was downloaded, its SHA-256
   computed, its head inspected, and its record count taken by pattern
   match (not by parsing).
3. The two largest files were fetched a second time, minutes apart, to see
   whether the served bytes are stable.
4. **Rehearsal.** A throwaway PostgreSQL database was created from
   `schema/0*.sql`, the two candidates were registered into it with the real
   `register.commit()`, and the real `Collector` was run with the real
   `HttpFetcher` against the run locators, writing to a throwaway OCFL root.
   The pipeline's own records were read back. The database and storage were
   then destroyed. The script is not part of the repository; it was a
   verification instrument, not a tool.

The rehearsal is **not a collection** in the project's sense. No source is
registered in any system the project keeps, no bytes are retained, and the
founder has authorised nothing. It was done so that the founder's decision
could rest on a run that has been seen to work rather than on the assumption
that it would.

## 2. EU Consolidated Financial Sanctions List

### Reachability

| URL | Result |
| --- | --- |
| `https://webgate.ec.europa.eu/fsd/fsf` (the candidate's original locator) | **401 Unauthorized**, header `Proxy-support: Session-based-authentication`. This is the FSF application root and wants an EU Login session. **Not usable as the registry locator.** |
| `…/fsd/fsf/public/files/xmlFullSanctionsList_1_1/content?token=dG9rZW4tMjAxNw` | 200, `application/xml`, 25 766 640 bytes |
| `…/fsd/fsf/public/files/csvFullSanctionsList_1_1/content?token=dG9rZW4tMjAxNw` | 200, `text/plain`, 25 166 172 bytes |
| `https://webgate.ec.europa.eu/robots.txt` | 404 — no robots policy published at that host |
| `https://data.europa.eu/data/datasets/consolidated-list-of-persons-groups-and-entities-subject-to-eu-financial-sanctions` | 200, but a JavaScript application shell; the catalogue record's content was not readable without a browser and was not read |

**On the `token` value.** The public file URLs carry a fixed query token.
It is the same value that appears in the Commission's own published download
links for these files and it is not something this project was issued. Its
terms of use were **not** verified here: the data.europa.eu catalogue page
that would state the licence did not render for a non-browser client, and
no Commission page stating the token's conditions was fetched. The
candidate's `rights_basis` stays "NOT LEGALLY REVIEWED"; this is one of the
things the review should cover.

### The files

| | XML | CSV |
| --- | --- | --- |
| `Content-Disposition` filename | `20260805-FULL-1_1(xsd).xml` | `20260805-FULL-1_1.csv` |
| `Last-Modified` (server) | Wed, 05 Aug 2026 14:50:10 GMT | Wed, 05 Aug 2026 14:50:12 GMT |
| In-file generation stamp | `generationDate="2026-08-05T16:47:04.449+02:00"`, `globalFileId="184961"` | first column `fileGenerationDate` |
| SHA-256 | `0c83e632fea7709d9c75bdd1deb4fa50782a93d2c99459f01c7a7a2d873c79c9` | `049cb95cf55cd9a77dfb8d3fed21eb61a541e4c46f80d1f1b581f2e537e0f015` |
| Stable across two fetches | yes (identical digest ~10 min apart, and identical again through `HttpFetcher`) | not re-fetched separately; identical digest through `HttpFetcher` |
| Structure | root `<export xmlns="http://eu.europa.ec/fpi/fsd/export">`; one `<sanctionEntity>` per designation with `<regulation>`, `<subjectType>`, `<nameAlias>`, and further child elements; each regulation carries a `publicationUrl` into EUR-Lex | semicolon-separated, UTF-8 with BOM, 43 852 lines including header; one row per name alias, so rows outnumber entities |
| `<sanctionEntity>` count (pattern match) | 6 234 | — |
| Regulation elements tagged `programme="UKR"` (pattern match) | 2 960 — the largest programme; next are IRN 707, SYR 380, BLR 374 | — |

Two things worth the founder's attention:

- **The file is 34 days old at verification** (generated 2026-08-05,
  checked 2026-09-08). Whether that reflects no designations in August or a
  publication lag is not something this check can tell; the first captures
  will. It is recorded, not interpreted.
- **The file is the whole list, all programmes.** UKR is under half of it.
  Whole-file capture is what the candidate's `scope_rules` say and what
  DR-0071(b) requires (no parsing on ingest), so this is expected — but it
  means the archive preserves designation records, with dates and places of
  birth, for programmes the project has no interest in. See §5.

## 3. OFAC Specially Designated Nationals list

### Reachability

| URL | Result |
| --- | --- |
| `https://sanctionslist.ofac.treas.gov/` (candidate locator) | 302 → `/Home/index.html`, 200, `text/html`, the "OFAC - Sanctions List Site" single-page application |
| `https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/SDN.XML` | 302 → presigned S3 URL (`wc2h-sls-prod-public-published.s3.us-gov-west-1.amazonaws.com`, `X-Amz-Expires=3600`) → 200, `text/xml`, 28 978 335 bytes |
| `…/exports/SDN_ADVANCED.XML` | same pattern → 200, 126 590 461 bytes |
| `…/exports/CONS_ADVANCED.XML` | same pattern → 200, 4 534 269 bytes |
| `…/exports/SDN.CSV` | same pattern → 200, `text/csv`, 5 672 451 bytes, 19 329 lines |
| `…/exports/CONS_PRIM.CSV` | same pattern → 200, 262 810 bytes, 481 lines |
| `https://www.treasury.gov/ofac/downloads/sdn.xml` (legacy address) | 302 → 302 → the **same** S3 object as `SDN.XML` above |
| `https://ofac.treasury.gov/specially-designated-nationals-list-data-formats-data-schemas` | 302 → `https://sanctionslist.ofac.treas.gov/Home/SdnList` |
| `https://sanctionslist.ofac.treas.gov/robots.txt` | a JSON body `{"message":"Forbidden"}` rather than a robots file |
| `https://sanctionslistservice.ofac.treas.gov/robots.txt` | 404 |

**On the redirect.** Every export request is answered with a one-hour
presigned URL into an S3 bucket in the US GovCloud region. `HttpFetcher`
follows it (Python's `urllib` follows redirects by default) and this was
confirmed in the rehearsal. But the fetcher records only the URL it was
asked for. The S3 response carries provenance that is worth keeping and
currently is not: see §5.

### The files

| | SDN.XML | SDN_ADVANCED.XML | CONS_ADVANCED.XML |
| --- | --- | --- | --- |
| `Last-Modified` (S3) | Fri, 04 Sep 2026 14:01:44 GMT | 14:01:45 GMT | 14:01:46 GMT |
| `ETag` (S3) | `a20aede42d1f65a913618c5a09b63113` | not recorded | not recorded |
| `x-amz-meta-publication-id` | 969 | 969 | 969 |
| `x-amz-meta-preview-date` | 9/3/2026 2:44:52 PM | 9/3/2026 2:46:48 PM | 9/3/2026 2:46:50 PM |
| `x-amz-meta-delta-name` | `2026-09-04_delta.xml` | — | — |
| In-file date | `<Publish_Date>09/04/2026</Publish_Date>`, `<Record_Count>19329</Record_Count>` | `<DateOfIssue>` 2026-09-04, schema `Version="3"` (`ADVANCED_XML.xsd`) | `<DateOfIssue>` 2026-09-04, same schema |
| SHA-256 | `a6fe1073e4cc3a9ea9b827f63f5ab56b80933603a8af791b21d7cacbf99da598` | `0ec4e7e77fb184ecab51f6e2979a2107e72f967c83097e2ade6cc3e01039027b` | `c0cdbcc3c7cb9c6bc4af5e1cff6110220aaa7628cb8216882a4feac5e71ab971` |
| Stable across two fetches | yes (identical digest, and identical through `HttpFetcher`) | identical through `HttpFetcher` | identical through `HttpFetcher` |
| `<sdnEntry>` count (pattern match) | 19 329, matching `Record_Count` | — | — |
| Programmes (pattern match, top five) | RUSSIA-EO14024 6 348; SDGT 3 259; IFSR 1 574; SDNTK 1 365; NPWMD 1 195 | — | — |

CSV digests, for the record though the CSVs are not in the proposed first
run: `SDN.CSV`
`0ffb4504696e2f5adecbd23a3f27c27e8264447a8021752f1043c74422650f5f`;
`CONS_PRIM.CSV`
`fa681487dfd865c189177b478a171178ab8e7133402342acc51f638a7bc121de`.

The same point as for the EU list, only more so: **about a third of the SDN
list is the Russia programme.** The rest — terrorism, narcotics,
proliferation, Cuba and others — comes along in every whole-file capture,
individuals with dates and places of birth included.

## 4. Rehearsal of the first run

Environment: this container; PostgreSQL 16.13; repository at commit
`d18eb9e`; `HttpFetcher` with a 300-second timeout and the User-Agent
`UIW-collector/rehearsal (+https://github.com/louisbaudry/UkraineIndependenceWar_dot_org)`.

| Step | Result |
| --- | --- |
| Register the two candidates into the scratch database via `register.commit()` | 2 `source` rows; **0 `source_dependence` rows** — the declared `derives-from` link to `eur-lex-sanctions` is dropped because EUR-Lex is not in the set being registered (see §5) |
| Run `eu-consolidated-list` against its 2 run locators | discovered 2, acquired 2, skipped 0, failed 0; 50 932 812 bytes preserved; 38–40 s |
| Run `ofac-sdn` against its 3 run locators | discovered 3, acquired 3, skipped 0, failed 0; 160 103 065 bytes preserved; 12 s |
| Run the EU XML locator a second time | acquired 1; **a new holding and a new OCFL object with the same SHA-256** as the first capture |
| State afterwards | 6 holdings, 6 preserved objects, 6 OCFL objects in the `permanent` root, **0 documentary assertions**, 0 orphaned objects; preservation events `ingestion` 6, `message-digest-calculation` 6, `virus-check` 6 |
| Digests in the database vs. digests from `curl` | identical for all five files |
| Teardown | database dropped, storage root deleted |

What the rehearsal proves: the fetch layer completes live requests,
follows the OFAC redirect, handles files up to 127 MB, and hands
byte-identical content to the pipeline; quarantine, Gate 1, the retention
tier, OCFL writing, canonical-store rows and coverage accounting behave on
real material as they do on fixtures; and a completed run creates no
canonical knowledge (DR-0066).

What it does not prove: anything about behaviour under a slow or
rate-limiting origin, conditional requests (none are made), or the security
check — `_default_scan` is the documented stand-in, so the six `virus-check`
events record that the gate ran, not that anything was scanned.

## 5. Findings the founder should know before authorising

Ordered by how much they matter to the first run. None blocks it; two
(the first and the last) deserve a ruling before daily automation.

1. **Successive captures are not linked.** DR-0074 makes each capture a
   distinct holding, related by the capture-series relation. The schema has
   `capture_series_member`; `collector/pipeline.py` never writes to it. The
   rehearsal's repeat capture became an unrelated second holding. The first
   run does not need the relation, but the series the candidates'
   `scope_rules` promise does not exist until the collector records it.
2. **Unchanged bytes are stored again.** There is no conditional request
   and no "digest unchanged, record the attempt, store nothing" rule. At the
   candidates' daily cadence, an unchanged day costs about 211 MB of
   duplicate storage. The EU server sends `Last-Modified`; the OFAC S3
   object sends `ETag`. Either a conditional fetch or a digest comparison
   before admission would do. A ruling is needed on which, because "record
   the attempt but do not create a holding" is a coverage-accounting
   question (DR-0070), not just a storage one.
3. **Response provenance is discarded.** `FetchResult` carries the response
   headers, but `_record_attempt` stores only locator, time, outcome and
   error. For OFAC that loses the publication id, the delta name, the final
   S3 URL and the ETag; for the EU it loses the server's filename and
   `Last-Modified`. These are the publisher's own statements about what was
   served and belong on the acquisition record.
4. **`--only` silently drops the EUR-Lex dependence.** Registering the
   consolidated list without `eur-lex-sanctions` leaves its declared
   `derives-from` relation unrecorded. The relation can be added when EUR-Lex
   is registered; until then the registry says nothing about the
   consolidated list being a compilation rather than a primary instrument,
   even though the file itself links every entry to its EUR-Lex act.
5. **There is no command-line entry point for a run.** `Collector.run()` is
   a library call; the rehearsal drove it from a script. The founder's first
   run will need the same, or a small `collector/run.py` that takes a source
   key and reads `run_locators` from the candidate file. Not built here.
6. **The EU token's terms are unverified** (§2). The value is public and the
   files are served without login, but no page stating the conditions was
   readable from here.
7. **Whole-file capture is broad.** Both lists carry personal data for
   programmes outside the project's scope (§2, §3). Preserved unparsed under
   DR-0071(b), with structuring reserved to Gate 2 under POL-0001 §4, this
   is within policy as written — but it is a data-minimisation fact the
   POL-0001 §10 legal review should see, and the reason the candidate file
   now says so in the `ofac-sdn` entry.

## 6. The other five candidates

Only a reachability probe of each landing locator was made, for the record.
No file was fetched, so **these remain unverified** in every sense that
matters.

| Candidate | Landing locator | Result |
| --- | --- | --- |
| `eur-lex-sanctions` | `https://eur-lex.europa.eu/` | 202 with an empty body — a challenge page or queue, not content |
| `bis-entity-list` | `https://www.bis.doc.gov/` | 200 after redirect to `https://www.bis.gov/` — the candidate's host is now a redirect |
| `uk-ofsi-consolidated` | gov.uk publication page | 200 |
| `seco-sanctions` | `https://www.seco.admin.ch/` | 200 after redirect to `/de` |
| `ua-nsdc-sanctions` | `https://www.rnbo.gov.ua/` | 200 |

---

**AI provenance (§80).** Drafted by Claude (Claude Code) on 2026-09-08 from
fetches and a rehearsal performed in this session. Every figure above comes
from a response received here and is reproducible from the URLs given;
counts marked "pattern match" were taken by string search over the files,
not by parsing them. This is a verification record, not a Decision Record;
it enacts nothing and authorises no collection.
