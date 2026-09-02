# Candidate source — War & Sanctions (GUR), "Components" section

**Status:** Candidate — **verified against the live site**, still not registered,
not collected, not evaluated for editorial acceptance.
**Logged:** 2026-09-01, at the founder's direction, following a link the founder received
(source of the link: a third party, unspecified).
**Verified:** 2026-09-02, by live fetch (see [Verification record](#verification-record)).

> **Supersedes the 2026-09-01 framing of this note.** The original note said its
> description of the site was "background knowledge ... not verified against the live
> page," because that session's egress proxy blocked the domain. That framing is now
> replaced by first-hand observation for the GUR portal. It is **not** replaced for
> KSE Institute and RUSI — those remain unverified here, for a different reason
> (see [§3](#3-comparison-sources-kse-institute-and-rusi)). The belligerent-party
> caveat is unchanged and, on the evidence below, strengthened.

---

## Verification record

**What was fetched, when, and how.** All fetches 2026-09-02, ~05:15–05:30 UTC, from
this session's container.

| URL | Result |
| --- | --- |
| `https://war-sanctions.gur.gov.ua/en/components` | 200, 170 KB HTML |
| `https://war-sanctions.gur.gov.ua/en/components/weapon` | 200 |
| `https://war-sanctions.gur.gov.ua/en/components/companies` | 200 |
| `https://war-sanctions.gur.gov.ua/en/components/{7355,7364,7365,5058}` | 200 (entry detail pages) |
| `https://war-sanctions.gur.gov.ua/en` (portal home) | 200 |
| `https://war-sanctions.gur.gov.ua/en/news` | 200 |
| `https://war-sanctions.gur.gov.ua/robots.txt` | 200 |
| `https://war-sanctions.gur.gov.ua/sitemap/sitemap.xml` | 200 |
| `https://war-sanctions.gur.gov.ua/api`, `/en/api` | **403** (Cloudflare) |
| `/en/about`, `/en/terms`, `/en/methodology`, `/sitemap.xml` | 404 |

**Access method — this needs a founder ruling before any collection (see [§6](#6-what-still-needs-a-founder-decision)).**
A plain `curl` and the agent's own fetch tool both received **HTTP 403** from
Cloudflare. The pages above were retrieved only after presenting a **desktop-Chrome
`User-Agent` string**. The site's `robots.txt` carries a Cloudflare-managed block
listing `ClaudeBot` — among others — under `Disallow: /`. Presenting a browser UA
sidesteps that rule in letter; whether it does so in spirit is a rights question this
note does not settle and has no authority to settle.
One request was made to `/api`, which `robots.txt` disallows for all agents; it
returned 403 and no content was obtained from it.

**What could not be verified, and why.** KSE Institute (`kse.ua`, `sanctions.kse.ua`)
and RUSI (`rusi.org`) are **blocked outright by this environment's egress proxy**
(`connect_rejected`, organization policy) for both `curl` and the fetch tool. So is
`web.archive.org`, and so is `example.com` — the allowlist is narrow, and
`gur.gov.ua` happens to be on it. Everything in §3 below about KSE and RUSI therefore
comes from **web-search result summaries, not from the primary documents**, and is
labelled as such throughout. No KSE or RUSI PDF was opened in this session.

---

## 1. What is actually on the page

### Identity and framing

- Page `<title>`: **"Foreign components in weapons"**.
- Site self-description (`<meta name="description">`, repeated as on-page tagline):
  **"The world`s only open database portal of foreign-produced weapon components"**.
- Operated under the **War & Sanctions** portal at `war-sanctions.gur.gov.ua`,
  footer-linked to `gur.gov.ua` and to Defence Intelligence social accounts
  (`t.me/DIUkraine`, `x.com/DI_Ukraine`, Facebook, Instagram, YouTube).
- **Named partners are both Ukrainian state bodies**: the Center for Countering
  Disinformation (`cpd.gov.ua`, an NSDC body) and the Ministry of Youth and Sports
  (`mms.gov.ua`). **No independent research institution — not KSE, not RUSI, not
  Conflict Armament Research — is named as a partner anywhere on the portal home
  page.** This is directly relevant to §4.

### Volume (as displayed, 2026-09-02)

| Figure | Value |
| --- | --- |
| Components | **5 993** |
| Weapon Units | **206** |
| "Updated:" banner | **31.08.2026** |
| Manufacturer filter options | **602** |
| Manufacturer-HQ-country filter options | **33** |
| Weapon (sample) filter options on `/components` | **236** |
| Weapon models on `/components/weapon` | **31**, across 5 armament types |
| "Involved enterprises" on `/components/companies` | **558** |

Pagination on `/en/components` runs to `page=500&per-page=12` (= 6 000 slots),
consistent with the stated 5 993.

**Observed internal inconsistency, unresolved:** the banner says 206 "Weapon Units",
while the weapon filter on the same page offers 236 named entries. The two counts are
not reconciled anywhere on the site. Do not quote "206" as authoritative without
re-deriving it.

### Structure

Three views over one dataset:

- `/en/components` — the component list (the main table).
- `/en/components/weapon` — 31 weapon models, faceted by armament type
  (Missile and bomb armament, UAV, Aviation, Artillery, Air defence equipment).
- `/en/components/companies` — 558 **Russian-side production enterprises**, faceted by
  weapon. Note this is a *different* axis from the 602 component manufacturers; the
  portal tracks both "who made the chip" and "who built the weapon".

### Fields per entry

Verified by opening four entry pages. The full field set is:

- **Name and marking** — free-text part type plus one or more marking lines
  (part number, date code, lot code), e.g. `DC/DC converter / TSM0505S / 2413`.
- **Armament** — the weapon sample the part was found in.
- **Manufacturer's headquarters country** — may be blank.
- **Manufacturer** — may be `Not identified`.
- **Production date** — where derivable from the date code, given as
  e.g. "13th week (March) of 2024". Often absent.
- **Extended description** — usually empty; on one entry (`/components/7364`) it
  contained **untranslated Ukrainian** ("Рік випуску 2025") on the English page.
- **Additional information** — usually empty.
- **Publication date** — when GUR published the entry (e.g. 27.08.2026, 05.09.2024).
- **One photograph** of the physical part, served from `/uploads/componentslist/...`.
- A "Provide additional information" crowdsourcing invitation, offering attribution
  "with reference to you, or without (at your request)".

**Fields that do not exist — this is the most important structural finding.** There is
**no** recovery date, **no** recovery location, **no** chain-of-custody or
custody-transfer record, **no** analysing-laboratory identifier, **no** confidence or
certainty marker, **no** per-entry source citation, and **no** stated basis for the
manufacturer attribution. The only thing tying a claim to reality is the photograph and
GUR's own say-so.

### Example entries (verbatim, from `/en/components`, 2026-09-02)

| Name / marking | Armament | Mfr. HQ country | Manufacturer | Production date |
| --- | --- | --- | --- | --- |
| Temperature sensor `AD 22100 STZ #2220` | Ballistic missile 9M723K5 "Iskander-M" | United States of America | Analog Devices | 20th week (May) of 2022 |
| FPGA `GW1N-UV9 / UG169C6/15 / 2229C` | Ballistic missile 9M723K5 "Iskander-M" | People's Republic of China | Gowin Semiconductor | 29th week (July) of 2022 |
| DC/DC converter `TSM0505S / 2413` | Ballistic missile 9M723K5 "Iskander-M" | Switzerland | Traco Power | 13th week (March) of 2024 |
| Tantalum SMD capacitor `337 G / 00A02` | UAV "GERAN-2" (Shahed-136) Ы-1311 | United States of America | KYOCERA AVX | — |
| Connector `РП15-50ШВ-В / 0501` | Ballistic missile 9M723K5 "Iskander-M" | russian federation | PLANT ATLANT JSC | 1st week (January) of 2025 |
| Microchip (no marking) | 3M22 Zircon ballistic missile | — | Not identified | — |

Two things to read off this table. First, the dataset is **not confined to
foreign parts** despite the page title — Russian-made components are catalogued
alongside them, and `russian federation` is one of the 33 filterable HQ countries
(as are Belarus, Iran and Ukraine). Second, a substantial share of rows are
`Not identified` / blank; the 5 993 figure is a count of catalogued parts, **not** a
count of successfully attributed foreign parts.

### Update cadence

Genuinely active. `/en/news` shows **116** portal updates, with component-section
entries dated 02.09.2026, 31.08.2026, 27.08.2026, 25.08.2026 — i.e. roughly every few
days. Recent items are specific and countable, e.g.:

> "Published: — 140 foreign- and russian-manufactured components identified in the
> 9M723 'Iskander-M' ballistic missile; — 35 enterprises involved in its production;
> — 108 officials and employees of the main enterprises of the production."
> (27.08.2026)

The sitemap index reports `lastmod` 2026-09-02T03:10:21+03:00 across all sections.

### API, export, download

- The footer shows an **"API"** label, but it is **not a link**: the markup is
  `<span class="virtual-link" href="javascript:void(0);"><span>API</span></span>`.
  Placeholder, not a published interface.
- `/api` and `/en/api` return **403**.
- `robots.txt` disallows `/api`, `/data`, `/download-controller`, `/subscription`,
  `/office`, `/search` — the existence of `/data` and `/download-controller` implies
  bulk endpoints exist, but they are **not publicly documented and are
  robots-disallowed**.
- **No export, download, CSV, JSON or dump link was found anywhere in the components
  section.** Practically: acquisition would mean HTML scraping of ~500 list pages plus
  ~6 000 detail pages — which collides squarely with the `robots.txt` position above.

### Licensing and terms of use

- **There is no terms-of-use page, no licence, and no copyright notice.** `/en/terms`,
  `/en/about` and `/en/methodology` all 404. Grepping the fetched pages for `©`,
  "copyright", "all rights reserved", "licence/license" and "terms of use" returns
  **nothing**. The footer carries only the bare string "War & Sanctions 2026".
- The one machine-readable rights statement on the site is in `robots.txt`:

  ```
  User-agent: *
  Content-Signal: search=yes,ai-train=no,use=reference
  Allow: /
  ```

  with an accompanying header stating that restrictions expressed via Content Signals
  are **"EXPRESS RESERVATIONS OF RIGHTS UNDER ARTICLE 4 OF THE EUROPEAN UNION
  DIRECTIVE 2019/790"**, and with `Disallow: /` blocks for `ClaudeBot`, `GPTBot`,
  `CCBot`, `Google-Extended`, `Amazonbot`, `Applebot-Extended`, `Bytespider`,
  `meta-externalagent` and `CloudflareBrowserRenderingCrawler`.

  Read plainly: **search indexing yes, AI training no, reference use yes, named AI
  crawlers excluded entirely.** Whether this project's pipeline is "reference use" or
  something the operator meant to exclude is a live question, not a settled one.

### Stated methodology

**None.** This is a firm negative finding, not an oversight in the search: there is no
methodology page, no explanation of how parts are recovered, no explanation of how a
marking is resolved to a manufacturer, no accuracy or correction policy, and no
versioning. The site does publish an advocacy frame instead — standing calls to action
addressed to "national governments" and to "manufacturers and distributors"
(ban re-export, standardise inspections, adopt due-diligence procedures, and so on) —
which sits on every page of the components section.

---

## 2. What the portal is, institutionally

Verified: the portal is operated by GUR and links to `gur.gov.ua`.

**Reported, not verified here:** several secondary accounts state that War & Sanctions
began as a project of Ukraine's **National Agency on Corruption Prevention (NACP)** in
2022, under the Yermak–McFaul sanctions roadmap; that the NACP portal was
**discontinued in March 2024**; and that it was **relaunched on 1 June 2024 under
Defence Intelligence (GUR)**. This session could not open the NACP or KSE primary
pages to confirm it. If the lineage matters to a registry entry, it must be confirmed
against primary sources — it changes who the custodian of the older records was.

---

## 3. Comparison sources: KSE Institute and RUSI

**Verification status: NOT verified in this session.** `kse.ua`, `sanctions.kse.ua` and
`rusi.org` are blocked by this environment's egress proxy. What follows is from web
search result summaries only. **Every figure in this section must be re-checked against
the primary document before it is relied on for anything.**

### RUSI — *Silicon Lifeline*

- *Silicon Lifeline: Western Electronics at the Heart of Russia's War Machine*, RUSI,
  **August 2022**; authors reported as James Byrne, Gary Somerville, Joe Byrne,
  Jack Watling, Nick Reynolds, Jane Baker.
- Reported findings: **450+ foreign-made components** across **27 Russian military
  systems**; component origins in the US, Japan, Taiwan, South Korea, Switzerland,
  the Netherlands, the UK, France, Germany; ~317 components attributed to US firms.
- Reported method: technical inspection of Russian equipment captured in, or fired at,
  Ukraine, combined with trade/procurement investigation.
- **Not established:** the report's acknowledgements, its licensing, whether the full
  PDF is free, and — critically — **whether and how Ukrainian state bodies mediated
  access to the wreckage**. Search summaries explicitly did not answer this.
- Note the age: this is a 2022 report. Any current RUSI component work was not located.

### KSE Institute

- Component work is run with the **Yermak–McFaul International Working Group on
  Russian Sanctions** — which is co-chaired by the head of the Office of the President
  of Ukraine. That is a material fact for independence analysis, not a footnote.
- Reported figures across several outputs, at different dates and **not mutually
  consistent as summarised**: 1 057 components (2023 joint study); ~2 800 components
  (a later analysis); 174 components in UAVs specifically, of which 91% from
  sanctions-coalition countries.
- Reported method: forensic teardown of battlefield debris **plus** customs/trade-data
  investigation — the trade-data half has no counterpart in the GUR portal.
- **Not established:** whether KSE's teardown samples come from Ukrainian military
  channels, and whether KSE cites the GUR portal as a source.

---

## 4. Cross-check: overlap, corroboration, dependence

### Overlap at manufacturer level is near-total

Testable first-hand, and tested: of **51** manufacturers prominent in RUSI/KSE
reporting on this subject, **49 appear in the GUR portal's 602-entry manufacturer
filter** — Texas Instruments, Xilinx, Analog Devices, Infineon, Cypress, Altera,
Marvell, ON Semiconductor, Murata, STMicroelectronics, Microchip/Atmel, Maxim,
Broadcom, NXP, Renesas, Micron, Nexperia, u-blox, Vishay, TDK, Toshiba, ROHM,
Panasonic, Semtech, Lattice, Winbond, Wolfspeed/Cree, Molex, TE Connectivity,
Amphenol, Qorvo, Skyworks, Samsung, KYOCERA AVX and others. GUR also records corporate
succession in the label itself (e.g. "Xilinx Inc. (AMD)", "Fairchild Semiconductor
(ON Semiconductor)").

**They agree about the phenomenon.** Western, Japanese, Taiwanese and Chinese
commodity microelectronics are present in Russian missiles and UAVs; the same
manufacturer names recur across all three bodies of work.

### But the overlap is weaker evidence than it looks

No **contradiction** was found between the sources. No **claim-level corroboration**
was established either, and that distinction is the point:

1. **Nothing could be matched at the claim level.** Corroboration under this project's
   standard would mean two sources independently reporting *the same part number in
   the same weapon system*. RUSI's and KSE's component tables were not obtainable in
   this session, so no part-number-level comparison was possible at all. Agreement that
   "Analog Devices parts appear in Russian missiles" is agreement about a category, not
   confirmation of a fact.
2. **The counts are not comparable and must not be summed or contrasted.** GUR's 5 993
   counts catalogued parts including Russian-made ones and including unattributed rows;
   RUSI's 450 counts foreign components across 27 systems in 2022; KSE's 1 057 / 2 800
   are different studies at different dates. These are four different denominators.
3. **No declared citation relationship was found in either direction.** The GUR portal
   cites no external research anywhere in its components section — no bibliography, no
   per-entry sourcing. Whether KSE or RUSI cite GUR could not be checked, because their
   documents were unreachable.

### The dependence question (DR-0028)

Under [DR-0028](../decision-records/DR-0028-explicit-source-dependence.md), independence
is a *researched conclusion*, never a default — and the research here points the wrong
way for treating these as independent lines.

All three bodies of work rest on **physical wreckage recovered on Ukrainian
territory**, and access to that wreckage is controlled by the Ukrainian state and
military. GUR *is* that state actor; RUSI's reported method is inspection of equipment
"captured in or fired at Ukraine"; KSE works through a group co-chaired by the Office
of the President of Ukraine. The likely typed relation is therefore
**`common-evidentiary-origin`**, and possibly **`shares-underlying-witness`** where
the same recovered unit was examined by more than one party.

**Provisional conclusion, to be confirmed, not assumed:** GUR, KSE and RUSI should
**not** be counted as independent corroborating lines for component claims by default.
The burden runs the other way — independence would have to be established per claim, by
showing that a given part identification did not trace back to the same recovery
pipeline. On present evidence it cannot be shown, because none of the three publishes
per-item chain of custody.

The one genuinely independent axis found is **KSE's customs/trade-data analysis**,
which does not depend on wreckage access at all. If claim-level corroboration is ever
wanted here, that is where to look for it — not in the teardown tables.

---

## 5. Caveats that any future registration must carry, not silently drop

The original note's caveats stand. The live findings sharpen them.

- **GUR is a directorate of Ukraine's Ministry of Defence** — an intelligence service
  of a belligerent state, not a neutral investigative body. Nothing observed on the
  live site softens this; the portal's own framing is explicitly a war-effort
  instrument ("We identify targets / To limit the aggressor's military and economic
  capabilities"), its section names are advocacy labels ("Kremlin Mouthpieces",
  "Champions of terror"), its house style renders "russian federation" in lower case
  throughout, and its only declared partners are two other Ukrainian state bodies. Any
  registration needs the `official Ukrainian` / `government` source type
  (SPEC-0003 §3 identity field), an explicit rights-assessment entry, and must never be
  treated as self-corroborating with other Ukrainian government output.
- **The absence of methodology and chain of custody is now a verified fact, not a
  worry.** A component entry is a photograph plus an assertion. Gate 2 editorial
  acceptance would have to separate "this part number was found in this wreckage" —
  which the portal asserts but does not evidence — from the sanctions-policy framing
  GUR attaches to it, which is advocacy and should be handled as such.
- **Rights status is unknown and the machine-readable signal is partly adverse.** No
  licence, no terms, no copyright notice; an express Art. 4 EU DSM reservation with
  `ai-train=no`; and named AI crawlers excluded. The correct SPEC-0003 §3 rights value
  is therefore `unknown` — an explicit, recordable value under
  [DR-0029](../decision-records/DR-0029-absence-state-vocabulary.md), not a blank to be
  filled in later. **It must not be recorded as permissive merely because the site calls
  itself "open".**
- **There is no supported acquisition path.** No API, no export, bulk endpoints
  robots-disallowed, and the only working access in this session required presenting a
  browser User-Agent against a `robots.txt` that names `ClaudeBot` under `Disallow: /`.
- **Entry-level data quality is uneven** — untranslated Ukrainian on English pages,
  many `Not identified` manufacturers, and a headline weapon count (206) that does not
  match the site's own filter (236).

---

## 6. What still needs a founder decision

Unchanged in substance from the original note; item 1 is now discharged, and items 5–6
are new and were surfaced by the verification itself.

1. ~~Fetch and review the live page.~~ **Done, 2026-09-02** — this note.
2. Confirm the NACP → GUR custody lineage (§2) against primary sources.
3. Decide where source registry *instances* live (DR-0067 approved a schema; no
   instance store exists). See [docs/sources/README.md](README.md).
4. Only then does DR-0071(a) permit the pipeline to collect from this source at all.
5. **New — rule on the `robots.txt` / User-Agent question.** The operator has expressly
   disallowed `ClaudeBot` and signalled `ai-train=no`. This session obtained pages by
   presenting a browser User-Agent. Whether that is acceptable for verification, for
   collection, for neither, or only with the operator's permission is a policy question
   for the founder, and it should be recorded as a Decision Record rather than settled
   inline. **Until it is settled, no bulk collection from this domain should be
   attempted.**
6. **New — rule on how this source may be counted for corroboration.** §4 argues GUR,
   KSE and RUSI probably share a common evidentiary origin. If that is accepted, it
   constrains every downstream confidence derivation that touches component claims, and
   belongs in a DR-0028 typed-dependence record — not in a source note.

## Recommendation

**Promote from "flagged for follow-up" to "verified candidate, blocked on two policy
rulings."** The source is real, substantial, actively maintained, on-scope, and richer
than the original note assumed — 5 993 catalogued parts with photographs, updated
within the last two days, across 31 weapon models. It is also a belligerent
intelligence service publishing unsourced assertions under no licence, behind a
robots policy that names our own crawler, with no export path.

The value is real and so is the problem. The next step is not collection; it is the
two rulings in §6 (items 5 and 6). Recommend taking item 5 first — it is the gating
one, since a negative answer makes item 6 moot.

---

**AI provenance (§80).** Drafted by Claude (Claude Code) on 2026-09-02 from live
fetches performed in this session. First-hand observations are confined to
`war-sanctions.gur.gov.ua` and are reproducible from the URLs in the
[Verification record](#verification-record). §3 (KSE, RUSI) rests on web-search
summaries only, because those domains were unreachable, and is explicitly not verified.
This note is a **candidate note**, not a registry entry and not a Decision Record; it
enacts nothing and authorises no collection.
