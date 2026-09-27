# Verification record — Office of the Prosecutor General of Ukraine, war-crime counts

**Status:** Verification record for one candidate registration. Nothing here
is registered, nothing is collected into the project's archive, and nothing
is enacted by this document. Registering the candidate is the founder's act,
per source, on the archive server (DR-0067, DR-0093 §3); no Decision Record
acts on this yet.
**Verified:** 2026-09-25 (routes tried from this session) and 2026-09-27
(the office's own site, through the archive server, by the founder, step by
step with an AI assistant reading each output).
**Candidate:** `ua-pgo-crime-statistics` in
[`sources/candidates/civilian-harm.yaml`](../../sources/candidates/civilian-harm.yaml).
**Mandate:** [DR-0109](../decision-records/DR-0109-civilian-harm-and-memorial.md)
Decision 5, step 1 ("UN monitoring … and Ukraine's Prosecutor General —
counts, with almost no names"), issue #70. The UN half is
[`verification-un-hrmmu-civilian-casualties.md`](verification-un-hrmmu-civilian-casualties.md),
registered by DR-0110.

---

## 1. What was done, in order

1. From this session, with `curl` and a browser User-Agent, every public
   route to the office's figures was requested: its own site, its Telegram
   channel, its evidence-submission portal and the government's children's
   portal (§2).
2. The office's own site was blocked from here, so the founder checked it
   from the archive server and from a browser. Both reached it (§3).
3. On the archive server, short read-only Python scripts (standard library,
   **nothing written to disk**) listed the front page's statistics links,
   then the monthly report page's files, then opened the newest file in
   memory. The scripts and their full output were pasted back into the
   session and read there (§4, §5).
4. Ukraine's copyright law was read on `zakon.rada.gov.ua`, which this
   session can reach (§7).

**Not done:** no rehearsal through the real collector, because a throwaway
database and archive on the archive server were not set up for this, and
this session cannot reach the files. The file was not fetched with the
collector's own User-Agent (`UIW-collector/0.1 (+…)`), and was fetched only
once, so digest stability is unchecked. See §9.

## 2. Routes tried from this session (2026-09-25)

| Route | Result | What it carries |
|---|---|---|
| `gp.gov.ua`, `www.gp.gov.ua`, `gp.gov.ua/en` | **403**, 5 483 bytes: Cloudflare "Sorry, you have been blocked", `cf-ray …-IAD` | — |
| `new.gp.gov.ua/ua/posts/statistika` and the report page (2026-09-27) | **403**, same block, `…-IAD` | — |
| `web.archive.org` CDX for `gp.gov.ua` | connection reset | — |
| `t.me/s/pgo_gov_ua` (Telegram, public preview) | 200. 212 posts read, 20 Aug – 25 Sep 2026, ~26K subscribers | News posts only. No recurring count post. Per-incident casualty posts ("5 killed, 7 injured"), which are DR-0109 step 2 material. A daily "minute of silence" post naming a fallen prosecutor. Ordinary criminal cases, including child sexual abuse, with suspects' ages and places |
| `warcrimes.gov.ua` | 200 | The office's evidence-reporting form, legal texts and a personal-data consent form. No figures. Its schema.org block names a private company ("Media Service Agency LLC") as the site's legal name |
| `childrenofwar.gov.ua` (uk and en) | 200 | Daily totals: children killed and injured "according to the Office of the Prosecutor General", missing and found (National Police), deported and returned (Bring Kids Back UA), sexually abused (Prosecutor General). Run by the Ministry of Reintegration and the National Information Bureau for the Office of the President. The front page also embeds photographs of missing children, with file names built from their names |

None of these is a clean step 1 source. The channel is a news feed with
names. The children's portal is another publisher's page that bundles the
office's counts with the deportation and sexual-violence counts DR-0109
Decision 2 holds for their own decisions, and with missing children's names
and photographs. The portal is recorded here and not drafted.

## 3. The block is regional, not general

On the archive server (Spain):

```
status 200, 100693 bytes
HTTP/2 200
server: cloudflare
cf-ray: a40b95cced83fcbf-MAD
```

The founder's browser also loaded the site normally. The block applies to
where this session runs (the US `IAD` edge), not to the archive server, so
**collection from the server is possible and verification from a session is
not**. Two consequences follow:

- Every future re-verification of this source must go through the archive
  server or a browser, as this one did.
- The GitHub Actions reminder built for the UN source (`.github/workflows/hrmmu-monthly-reminder.yml`)
  runs on US-hosted runners and would very likely be blocked the same way.
  A monthly reminder for this source would have to run on the archive
  server or only remind, without reading the site.

## 4. Where the counts are published

The front page's menu has a statistics section. Its links, as the server
listed them (hosts as served; the site mixes `www.`, `new.` and bare
`gp.gov.ua`):

- «Статистика» → `new.gp.gov.ua/ua/posts/statistika`
- **«Про зареєстровані кримінальні правопорушення та результати їх
  досудового розслідування»** ("On registered criminal offences and the
  results of their pre-trial investigation") → the candidate's `locator`
- reports on offences at enterprises, organised crime, money laundering
  (2011–2019), persons who committed offences, domestic violence and
  cybercrime (not relevant)
- «Кримінальне переслідування за злочини сексуального насильства,
  повʼязаного з конфліктом» (prosecution of conflict-related sexual
  violence), **not opened**, because DR-0109 Decision 2 reserves the topic
  for its own decision
- «Пам'ятка для потерпілих від міжнародних злочинів» (a leaflet for victims
  of international crimes) and the office's 2026–2028 strategy for
  prosecuting international crimes (not statistics)

The report page (200, 83 082 bytes) links **20 files**, all titled «Єдиний
звіт про кримінальні правопорушення за …» ("Unified report on criminal
offences for …"):

- **2026:** January, January–February, … **January–August** (8 files);
- **2025:** January … January–December (12 files).

Each report is **cumulative from January of its year**. The January–December
report is the year's closing figure. Every file is served from a third host,
`old.gp.gov.ua`, through a download script:

```
https://old.gp.gov.ua/ua/file_downloader.html?_m=fslib&_t=fsfile&_c=download&file_id=<N>
```

`file_id` is new for every report: 292316 for January–August 2026, 279658
for January–December 2025. The page's HTML writes the separators as
`&amp;`, and requesting that form literally returns a 26 275-byte HTML page
instead of the file (seen on the first attempt). The address has to be
unescaped, as a browser does.

Earlier years were not looked for. They may be on other pages of the office's
sites, and would be a retrospective question.

## 5. The January–August 2026 report

| | |
|---|---|
| Status | 200 |
| Content-Type | `application/octet-stream` |
| Content-Disposition | `attachment; filename="Forma_1_serpen_2026.xlsx"` ("Form 1, August 2026") |
| Last-Modified | Fri, 04 Sep 2026 15:04:59 EEST |
| Size | 418 672 bytes |
| SHA-256 | `7c5a33a89a7ec2d5d573e54d1b7c6fb67697aeb73c1b08cbf10d329fb4057936` |
| Format | Office Open XML workbook (ZIP, 47 parts), ten sheets named `0` to `9` |

Publication rhythm, from one data point: the August report appeared on
4 September, so about the first week of the following month.

A search of the workbook's shared strings for war-crimes terms found:

- «Таблиця 1.20. Кримінальні правопорушення проти миру, безпеки людства та
  міжнародного правопорядку»: Table 1.20, offences against peace, the
  security of mankind and the international legal order (Chapter XX of the
  Criminal Code);
- «Воєнні злочини, ст. 438»: war crimes, Article 438;
- «якщо вони спричинили загибель людини (ч. 2 ст. 438)»: war crimes that
  caused a person's death, Article 438(2);
- the chapter split into «Злочини» (crimes) and «Кримінальні проступки»
  (criminal misdemeanours), and a wartime offence on disclosing the
  movement of weapons and troops.

The numbers themselves were not read. The workbook's cells were not opened
from here, and no figure is quoted in this record.

**What the count means.** Form 1 counts **registered criminal proceedings**
and their investigation results: how many offences were entered in the
Unified Register of Pre-trial Investigations under each article. It is not
a count of victims and not a count of proven crimes. One strike can be one
proceeding or many, and a proceeding is an allegation under investigation
(Phase I record §62–63). Any later structuring must say so.

## 6. Personal data

Form 1 is a table of aggregate counts by article, region and investigation
outcome. No names were seen in the shared strings that were printed. Those
were only the lines matching the war-crimes search, so this is **not a
row-by-row check**. That aggregate statistical forms carry no personal data
is the expected case, not a verified one. The first real collection should
include a look at the workbook before anything is structured.

## 7. Rights

Ukraine's Law No. 2811-IX "On Copyright and Related Rights" (edition of
31 July 2026, read on `zakon.rada.gov.ua` 2026-09-27), Art. 8(1): "Не
охороняються авторським правом: … 3) акти органів державної влади, …
офіційні документи політичного, законодавчого, адміністративного і
судового характеру …" ("not protected by copyright: … acts of state
authorities, … official documents of a political, legislative,
administrative and judicial nature …"). A prosecutor's official statistical
report plausibly falls under that. However, Art. 8(1)(6) names non-original
databases as subject to a *sui generis* right, and whether that applies to
a statistics workbook was not established. No reuse terms were found on
the office's site; they were not searched for on the blocked hosts.

The candidate claims `may-preserve`, marked **UNVERIFIED**, like every
candidate whose rights position no lawyer has reviewed. That is below what
Art. 8(1)(3) may allow, on purpose.

## 8. Capture format and class

`capture_format: http`. The workbook is the document. The listing page is
server-rendered HTML whose links are in the body, as the scripts showed. It
is kept alongside the file because it is the only place that says which
month a `file_id` holds.

A new class, **`UA-state-civilian-harm`**, following jurisdiction first,
topic second (the 2026-09-17 ruling). It is kept apart from
`UA-state-investigations` (the NSDC register) because the topic,
rights basis and cadence differ. `source_type: court-prosecutor` is the
vocabulary's term for exactly this publisher. Grades B / "2", triage only
(DR-0027):

- **B** because a state party to the conflict is reporting on its
  adversary, the same reasoning as the NSDC candidates.
- **"2"** because the count is the office's own record of its own
  registrations, accurate as such. What it proves is the part to read with
  care.

## 9. What this settles, and what it does not

**Settled:**

- The office publishes monthly, cumulative, official war-crime counts
  (Art. 438 and 438(2)) in a spreadsheet, with no names expected.
- The archive server can reach them.
- The exact address of the newest report, with its size and fingerprint.

**Not settled, and worth doing before or at registration:**

1. **The collector's User-Agent.** Cloudflare passed a browser-like
   User-Agent from the server. Whether it passes `UIW-collector/0.1 (+…)`
   is untested. `collector/run.py` has a `--user-agent` option if it does
   not, but using it would be a deliberate choice to record.
2. **Digest stability and a collector rehearsal.** The file was fetched
   once. The registration's `--dry-run` and first run will show more.
3. **A row-by-row look at the workbook** for personal data (§6).
4. **Children's counts.** Issue #70 also names children killed and injured.
   The office publishes those on `childrenofwar.gov.ua`, bundled as §2
   describes, not as a clean file of its own that was found. Not drafted.
5. **Earlier reports** (2025 and before). January–December 2025 is the
   obvious first backfill and a separate decision.
6. **A monthly reminder** that can reach the site (§3).
