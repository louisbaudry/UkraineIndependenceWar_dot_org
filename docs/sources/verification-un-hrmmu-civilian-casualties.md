# Verification record — UN Human Rights Monitoring Mission in Ukraine, civilian-casualty updates

**Status:** Verification record for one candidate registration. Nothing here
is registered, nothing is collected into the project's archive, and nothing
is enacted by this document. Registering the candidate is the founder's act,
per source, on the archive server (DR-0067, DR-0093 §3); no Decision Record
acts on this yet.
**Verified:** 2026-09-24, ~19:00–20:00 UTC, from this session's container.
**Candidate:** `un-hrmmu-protection-of-civilians` in
[`sources/candidates/civilian-harm.yaml`](../../sources/candidates/civilian-harm.yaml).
**Mandate:** [DR-0109](../decision-records/DR-0109-civilian-harm-and-memorial.md)
Decision 5, step 1 ("UN monitoring … counts, with almost no names"), issue
#69. The other half of step 1, Ukraine's Prosecutor General, is not covered
here.

---

## 1. What was done, in order

1. The UN's Ukraine-facing hosts were requested with `curl`, presenting a
   User-Agent naming this project's repository, to find where the
   civilian-casualty series is actually published.
2. The mission's "Protection of civilians" listing was paged through to the
   end to establish the series' extent and rhythm.
3. The most recent update (August 2026) was fetched: its landing page and
   every language edition it links. The English PDF was fetched twice.
   Digests, headers and PDF metadata were recorded; the English and
   Ukrainian texts were extracted (with `pypdf`, in a scratch virtualenv —
   not a project dependency) and read; the embedded photographs were
   extracted and looked at.
4. Terms of use and any machine-readable data were searched for.
5. **Rehearsal.** A throwaway PostgreSQL database was built from
   `schema/0*.sql`, the candidate registered into it with the real
   `register.py --commit --only`, and the real `collector/run.py` run
   against the run locators into a throwaway archive root. Both were then
   destroyed. As with every earlier rehearsal, this is **not a
   collection**: nothing was registered in any system the project keeps
   and no bytes were retained.

## 2. Where the series lives

The monitoring mission (HRMMU, part of the Office of the UN High
Commissioner for Human Rights, OHCHR) has its own site, and that is where
the series is.

| URL | Result |
| --- | --- |
| `https://ukraine.ohchr.org/` | 301 → `/en`, 200, `text/html`, 78 924 bytes. The mission's own Drupal site: "UN Human Rights Monitoring Mission in Ukraine" |
| `https://ukraine.ohchr.org/en/reports/protection-of-civilians` (**candidate locator**) | 200, `text/html`, 66 547 bytes. Nine listing pages (`?page=0` … `?page=8`) |
| `https://ukraine.ohchr.org/robots.txt` | 200. Drupal defaults only: disallows `/admin/`, `/search/`, `/user/…` and the like; `/en/…` pages and `/sites/default/files/` are not disallowed |
| `https://www.ohchr.org/en/countries/ukraine` | **403**, body titled "Just a moment…" with a `challenges.cloudflare.com` script — a Cloudflare challenge, not content |
| `https://www.ohchr.org/en/about-us/copyright` | **403**, same challenge |
| `https://www.ohchr.org/robots.txt` | 200 (the challenge does not cover it) |
| `https://ukraine.un.org/en` | 200, `text/html`, 204 825 bytes. The UN country team's site. Not where the series is published; not used further |
| `https://web.archive.org/cdx/search/cdx?url=ohchr.org/en/news/2022/*…` | `curl: (35) Recv failure: Connection reset by peer`, twice. Wayback's index was unreachable this session |

**Extent.** Listing pages 0–7 carry the monthly updates, titled "Protection
of Civilians in Armed Conflict — <Month Year>", from **October 2023**
(posted 14 November 2023) to **August 2026** (posted 16 September 2026).
The last page (`?page=8`) carries older one-off documents in the same
category: "Attack on Funeral Reception in Hroza, 5 October 2023", "500 days
update: Civilian casualties in Ukraine from 24 February 2022 to 30 June
2023" and "Killings of civilians: summary executions and attacks on
individual civilians in Kyiv, Chernihiv, and Sumy regions … 2022". The
2022-to-autumn-2023 monthly (earlier, weekly) casualty updates were published
on `www.ohchr.org`, which could not be reached (above). Recovering them is a
retrospective-acquisition question for WP 3.4, not part of this candidate.

**Rhythm.** Monthly, posted around the middle of the following month
(examples read off the listing: October 2023 → 14 Nov; November 2023 → 11
Dec; December 2023 → 15 Jan; August 2026 → 16 Sep). The June edition doubles
as a half-year summary ("June and the first six months of 2026"). The
English edition comes first; the Ukrainian followed a week later for August
(PDF `Last-Modified` 17 Sep for English, 23 Sep for Ukrainian).

## 3. The August 2026 update

| | Landing page | English PDF | Ukrainian PDF | Russian PDF |
| --- | --- | --- | --- | --- |
| URL | `/en/Protection-of-Civilians-in-Armed-Conflict-August-2026` | `/sites/default/files/2026-09/Ukraine%20-%20protection%20of%20civilians%20in%20armed%20conflict%20%28August%29_ENG.pdf` | `/sites/default/files/2026-09/Ukraine_protection_of_civilians_in_armed_conflict_August_UKR.pdf` | `/sites/default/files/2026-09/Ukraine_protection_of_civilians_in_armed_conflict_August_RUS.pdf` |
| Status | 200, `text/html` | 200, `application/pdf` | 200, `application/pdf` | **404**, an HTML error page (43 604 bytes) |
| Size | 55 537 bytes | 4 402 535 bytes | 4 193 477 bytes | — |
| `Last-Modified` / `ETag` | 23 Sep 2026 12:56:33 GMT / `"1790168193"` | 17 Sep 2026 06:59:06 GMT / `"432d67-65ba851e28443"` | 23 Sep 2026 12:34:26 GMT / `"3ffcc5-65c25b4302fa5"` | — |
| SHA-256 | `ae550e5028f175e82be2865c80a09c1500991684468a9860c6c857927f48068b` | `a8ff316b6d44753bf5be6ccffddb6a9fedba166426132d8c10fe2b17f0dc425b` | `dec34226801d19468c983e8d060994ce2bfd5428d25d3c61d60af57cfde6ab83` | — |
| Stable across two fetches | yes (identical digest) | yes (identical digest on a second fetch in the same session, and again through the collector) | identical through the collector | — |
| PDF metadata | — | 5 pages; InDesign; created 2026-09-17 08:56 +03:00 | 5 pages; InDesign; created 2026-09-23 09:36 +03:00 | — |

**The Russian edition is linked from the publisher's own landing page and
does not exist at that address.** It is recorded here and left out of the
run locators. It may appear later under another name.

**File names are not regular.** Compare `…(August)_ENG.pdf` with
`…_August_UKR.pdf`, and the June English file
`…June and the first six months of 2026_ENG.pdf` with its Ukrainian sibling
`…(June + 6 months)_UKR.pdf`. The next month's URLs cannot be predicted.
They have to be read off the new landing page before each run. This is the
same manual re-verification obligation `eur-lex-sanctions` (DR-0105) and
`isw-orca` carry.

### What it contains

Read from the extracted English text, and confirmed in outline in the
Ukrainian:

- **Monthly totals**: "At least 372 civilians were killed and 2,349 injured
  in Ukraine in August 2026", with a comparison to earlier months and years
  (January–August 2026: 2,222 killed, 13,058 injured).
- **By age and sex**: men, women, boys and girls, killed and injured,
  with children given separately.
- **By weapon or incident type**: long-range missiles and loitering
  munitions, short-range drones, aerial bombs, artillery and MLRS, mines
  and explosive remnants of war.
- **Place**: "across 13 regions of Ukraine and the city of Kyiv", with the
  worst-hit cities named and counted (Kyiv 31 killed/106 injured, Kherson
  25/334, Kryvyi Rih 16/147, Zaporizhzhia 11/131). The text layer does
  **not** show a full per-region table. If one exists it is in a graphic,
  not extractable text.
- **Occupied territory and Russia**: HRMMU's verified figure for occupied
  territory (4 killed, 35 injured), plus Russian authorities' own claims
  (85/498 occupied territory, 113/736 in Russia) explicitly **reported, not
  verified**.
- **Representative incidents**: six dated attacks, each with a place and
  counts by sex and age, e.g. "On 21 August, two drones struck an
  operational shopping centre in Kryvyi Rih … killing at least 13 civilians
  (9 women and 4 men) and injuring 126 (67 women, 38 men, 13 girls, and 8
  boys)". These map directly onto DR-0109 Decision 4's *incident* layer.
- **Cumulative since 24 February 2022**: 17,257 killed and 53,693 injured
  (70,950 total), by year, by month, and by age and sex.
- **A thematic paragraph** (August: attacks on retail, food and logistics
  companies, with company names).

### Stated methodology

In the PDF's own words, figures count individual records where "the
'reasonable grounds to believe' standard of proof was met, namely where,
based on a body of verified information, an ordinarily prudent observer
would have reasonable grounds to believe that the harm took place as
described. HRMMU refers to information that meets this criterion as
'verified.'" Sources named: interviews with victims, relatives and
witnesses; open-source photo and video; forensic, criminal-investigation
and court records; NGO reports; law-enforcement and military statements;
medical and local-authority data.

Three consequences for the archive:

1. **It is an undercount by design, and says so**: "The actual extent of
   civilian harm … is likely considerably higher", with Mariupol,
   Lysychansk, Popasna and Sievierodonetsk named as particularly
   undercounted. A footnote names a specific excluded incident (a drone
   attack on a bus near occupied Katerynivka, 26 August) pending
   verification.
2. **Earlier figures are revised in later editions**: "an increase in total
   figures in this update is not only due to casualties that occurred in the
   reporting period, but also to the corroboration by HRMMU of cases that
   occurred before the reporting period". Each monthly edition is therefore
   its own dated claim about the whole war to date. The archive keeps every
   edition and never overwrites one with the next (DR-0030; DR-0109
   Decision 4's "each stays that source's claim").
3. **Not-yet-verified is not a finding about status**: "the
   non-designation of an individual as a civilian reflects a lack of
   information, rather than a confirmation the individual's status as a
   combatant."

## 4. Personal data

As expected, the updates are **counts, with no victims' names**:

| What | Where | Bearing |
| --- | --- | --- |
| Victims | counts by sex and age only, including in the incident paragraphs | no names, no identifying detail found in the text |
| A witness quote | one, attributed to "an employee of one of the shops" | anonymous |
| UN media contacts | two staff names, work phone numbers and `@un.org` addresses on the last page, and the same media contact repeated in the site footer | professional contact details the UN itself publishes; preserved as part of the source, never structured |
| Company names | retail/logistics firms attacked | legal persons, not personal data |
| Photographs | three in the English PDF, captioned "Aftermath of a missile and drone attack on Kyiv city, 20 August 2026" | see below |

The photographs were looked at, not only counted. One shows a damaged
apartment block with a UN monitor seen from behind. One shows people sitting
under trees with firefighters behind them and **a figure lying under a
blanket, face not visible**. One shows people gathered at an aid point. Some
bystanders are identifiable. Nothing in them is gory. The drafter's judgment is that
they are not "graphic" in PRES-012/POL-0001 §5.9's sense, so the candidate
keeps `expects_graphic_content: false` and a `public` default. The people in
them fall under POL-0001 §5.8 (ordinary civilians incidentally present:
preserve as part of the source, never structure, never publish as
individuals), and the covered figure under §5.9's dignity standard for any
derivative. Photographs in later editions could be harder, and whoever
re-reads each month's landing page should look. This is flagged as a judgment
the founder can reverse.

## 5. Rights

| Checked | Result |
| --- | --- |
| The mission's site | footer "© UN Human Rights Monitoring Mission in Ukraine". No terms-of-use or copyright page linked from it |
| OHCHR's copyright page on `www.ohchr.org` | unreachable (Cloudflare 403) |
| UN website terms, `https://www.un.org/en/about-us/terms-of-use` | 200. Grants "permission to Users to visit the Site and to download and copy the information, documents and materials … for the User's personal, non-commercial use, without any right to resell or redistribute them or to compile or create derivative works therefrom", subject to more specific restrictions, and reserves the UN's privileges and immunities. **Whether these terms govern `ukraine.ohchr.org` was not established.** |

So the candidate claims **`may-preserve` and nothing more**, with a
rights basis that says `UNVERIFIED — NOT LEGALLY REVIEWED`. DR-0109
Decision 7 stage 2 already plans to *cite* figures with attribution. Whether
reproducing text or photographs is allowed goes to Part B of the legal brief
(IP/media counsel), as DR-0109 says.

## 6. Machine-readable data

The mission publishes **no data file** for this series: no CSV/XLSX link on
the listing, the landing page or the PDF. The only related dataset found is
on the Humanitarian Data Exchange (`data.humdata.org`, API search, 200):
"Ukraine: Civilian Casualties", maintained by **OCHA Ukraine**, sourced from
OHCHR, CC BY, covering **2016–September 2021 only**, last modified
2021-10-18. It is pre-invasion, from a different publisher and stale, so it
is out of scope and excluded by name.

## 7. Capture format and class

- **`capture_format: http`.** The PDF is the document. The landing page is a
  plain server-rendered HTML page whose content (the publication date
  "16 September 2026" and the summary) is in the body itself, so a bare
  body loses nothing, and the rehearsal stored it byte-identical to `curl`.
  A WARC record would add a browsing-session envelope that this source does
  not need (DR-0006, DR-0067).
- **Class `UN-international-civilian-harm`**: jurisdiction first, topic
  second, per the founder's 2026-09-17 ruling on WP 3.7 §7. The UN gets its
  own jurisdiction because its terms and immunities are its own, not any
  member state's; that is the policy-field difference the ruling groups by.
  Monthly cadence, permanent retention, public access, `may-preserve`, no
  graphic content expected, grades A / "2". A later UN civilian-harm source
  (a thematic report series, the Secretary-General's reports) would join
  it. A UN source in another area would not.
- **Grades (triage only, DR-0027).** Reliability **A**: the mission applies
  and publishes a stated verification standard, and this series is the
  reference count other publishers cite. Item credibility **"2" (probably
  true)** rather than "1": each figure is HRMMU's own verified claim, not one
  confirmed by independent sources, and the publisher itself revises it.

## 8. Rehearsal

Environment: this container; PostgreSQL 16.13; repository at `main`
`34388d0` plus the uncommitted candidate file; `collector/run.py` with its
default User-Agent `UIW-collector/0.1 (+https://github.com/louisbaudry/UkraineIndependenceWar_dot_org)`.

| Step | Result |
| --- | --- |
| `register.py --check` | 14 candidates validate |
| `register.py --commit --only un-hrmmu-protection-of-civilians` (scratch database) | 1 source registered |
| `run.py … --dry-run` | all four checks passed; nothing fetched, nothing written |
| `run.py …` | discovered 3, acquired 3, skipped 0, failed 0; **8 651 549 bytes** preserved in 11.5 s |
| Digests in the database vs. `curl` | identical for all three (landing page, English PDF, Ukrainian PDF) |
| State afterwards | 3 preserved objects in the `permanent` root; acquisition attempts: 3 `success`; preservation events `ingestion` 3, `message-digest-calculation` 3, `virus-check` 3; **0 documentary assertions** (DR-0066) |
| Disk | 17 MB for 8.65 MB of captures, because the quarantine copies remain after admission (the known gap from DR-0093 finding 8) |
| Teardown | database dropped, archive directory deleted |

As before, the `virus-check` events record that the gate ran, not that
anything was scanned (`_default_scan` is the documented stand-in).

## 9. What this settles, and what it does not

**Settled:** the series exists where the candidate says; it is reachable
without a challenge; it carries the counts DR-0109 step 1 wants, by sex,
age, weapon and place, with incident-level examples; it names no victims;
its methodology is stated and conservative; and a real collector run against
it succeeds cleanly.

**Not settled:**

1. **Rights**: which terms govern `ukraine.ohchr.org`. Only `may-preserve`
   is claimed.
2. **The 2022–autumn-2023 updates on `www.ohchr.org`**, behind a Cloudflare
   challenge, with Wayback unreachable this session. The candidate covers
   the mission's own site only.
3. **Per-run locators**: someone has to read each month's landing page and
   list its files before each run. The file names are irregular, and a
   linked edition can be missing (Russian, August).
4. **The periodic and thematic reports**, excluded here because they have
   broader scope and more personal detail. Each would be its own candidate.
5. **Structuring**: nothing here decides how HRMMU's counts become
   incidents and harms. That is DR-0109 Consequence 5's working paper and a
   Gate 2 decision.

---

**AI provenance (§80).** Drafted by an AI assistant (Anthropic Claude Code
agent session) on 2026-09-24 from fetches, text extraction and a rehearsal
performed in this session. Every figure above comes from a response received
here and can be reproduced from the URLs given. Quoted passages were taken
from the PDF's extracted text layer, not retyped. This is a verification
record, not a Decision Record. It enacts nothing and authorises no
collection. Nothing here is legal advice.
