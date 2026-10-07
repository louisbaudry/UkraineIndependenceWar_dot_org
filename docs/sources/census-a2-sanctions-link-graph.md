# Census A2 — sanctions-authority link graph

> **Status: informal working note.** Not a registration, not an authorization to
> collect, not a Decision Record. One of the four editorial evidence sources of
> WP 3.4 §4.1 Track A item A2 (issue #53). **AI provenance (record §80):**
> drafted by an AI assistant (Anthropic Claude Code agent session) on
> 2026-10-07 from one session's live reads; nothing here has been reviewed by
> the founder.

## What this is

The web hosts that the already-registered sanctions authorities link out to
from their own pages, as candidate domains for the census. The evidence for
each host is only that a registered authority's page links to it. A link says
the authority points readers there; it does not say the host is authoritative,
stable, in scope or lawful to collect. Those are Track B judgements.

## Method, and one reading of the rules to confirm

WP 3.4 §4.1 A2 says "indices only … no live fetch of any unregistered host".
No index available here exposes page links without a multi-gigabyte Common
Crawl graph download, so the founder ruled (2026-10-07, option 1 of 3) that the
registered authorities' own public pages may be read **in memory**: eight
requests in total, hostnames of `<a href>` targets extracted, **no page bytes
stored, nothing written to the archive or its database**, and no unregistered
host contacted.

**This is a reading of DR-0071(a), not an explicit permission in it.** The
pages fetched are each registered source's `locator` page or its dated
EUR-Lex instruments; the other fetched pages are not among the configured
`run_locators` data files. The reading is recorded here so it can be
confirmed or withdrawn. Collection scale stays suspended (DR-0072).

Requests made (identifying `User-Agent`, one request each, no crawling
beyond these):

| Source | Page requested | Result |
|---|---|---|
| `eur-lex-sanctions` | `eur-lex.europa.eu/` | HTTP 200, 24 links |
| `eur-lex-sanctions` | CELEX 02014R0269-20260807 (dated consolidated text) | HTTP 200, 262 links |
| `eur-lex-sanctions` | CELEX 02014D0145-20260807 | HTTP 200, 1 214 links |
| `eu-consolidated-list` | `webgate.ec.europa.eu/fsd/fsf` | **failed**: redirect loop; nothing extracted |
| `ofac-sdn` | `sanctionslist.ofac.treas.gov/` | HTTP 200, **1 link** (page is script-driven) |
| `bis-entity-list` | `www.bis.gov/` | HTTP 200, 93 links |
| `uk-ofsi-consolidated` | the OFSI consolidated-list publication page | HTTP 200, 98 links |
| `seco-sanctions` | `www.seco.admin.ch/` | HTTP 200, 19 links |

For each page, links to the authority's own host were set aside, and links to
social platforms and a survey tool (`twitter.com`, `x.com`, `youtube.com`,
`linkedin.com`, `smartsurvey.co.uk`) were dropped. Hosts below are as they
appear in the pages, with a leading `www.` removed.

## Result — 35 external hosts

| # | Host | Linked from | Links |
|---|---|---|---|
| 1 | `federalregister.gov` | `bis-entity-list` | 14 |
| 2 | `european-union.europa.eu` | `eur-lex-sanctions` | 12 |
| 3 | `data.europa.eu` | `eur-lex-sanctions` | 5 |
| 4 | `op.europa.eu` | `eur-lex-sanctions` | 5 |
| 5 | `assets.publishing.service.gov.uk` | `uk-ofsi-consolidated` | 4 |
| 6 | `europa.eu` | `eur-lex-sanctions` | 3 |
| 7 | `consilium.europa.eu` | `eur-lex-sanctions` | 2 |
| 8 | `ecas.ec.europa.eu` | `eur-lex-sanctions` | 2 |
| 9 | `nationalarchives.gov.uk` | `uk-ofsi-consolidated` | 2 |
| 10 | `sanctionssearchapp.ofsi.hmtreasury.gov.uk` | `uk-ofsi-consolidated` | 2 |
| 11 | `snapr.bis.gov` | `bis-entity-list` | 2 |
| 12 | `admin.ch` | `seco-sanctions` | 1 |
| 13 | `commerce.gov` | `bis-entity-list` | 1 |
| 14 | `commission.europa.eu` | `eur-lex-sanctions` | 1 |
| 15 | `cor.europa.eu` | `eur-lex-sanctions` | 1 |
| 16 | `cordis.europa.eu` | `eur-lex-sanctions` | 1 |
| 17 | `curia.europa.eu` | `eur-lex-sanctions` | 1 |
| 18 | `eca.europa.eu` | `eur-lex-sanctions` | 1 |
| 19 | `ecb.europa.eu` | `eur-lex-sanctions` | 1 |
| 20 | `ecfr.gov` | `bis-entity-list` | 1 |
| 21 | `edpb.europa.eu` | `eur-lex-sanctions` | 1 |
| 22 | `eeas.europa.eu` | `eur-lex-sanctions` | 1 |
| 23 | `eesc.europa.eu` | `eur-lex-sanctions` | 1 |
| 24 | `eib.org` | `eur-lex-sanctions` | 1 |
| 25 | `epso.europa.eu` | `eur-lex-sanctions` | 1 |
| 26 | `europarl.europa.eu` | `eur-lex-sanctions` | 1 |
| 27 | `law-tracker.europa.eu` | `eur-lex-sanctions` | 1 |
| 28 | `n-lex.europa.eu` | `eur-lex-sanctions` | 1 |
| 29 | `ombudsman.europa.eu` | `eur-lex-sanctions` | 1 |
| 30 | `regulations.gov` | `bis-entity-list` | 1 |
| 31 | `secure.edps.europa.eu` | `eur-lex-sanctions` | 1 |
| 32 | `ted.europa.eu` | `eur-lex-sanctions` | 1 |
| 33 | `trade.gov` | `bis-entity-list` | 1 |
| 34 | `usa.gov` | `bis-entity-list` | 1 |
| 35 | `wbf.admin.ch` | `seco-sanctions` | 1 |

## How to read it

- **EUR-Lex rows are mostly site chrome.** The 23 hosts linked from EUR-Lex are
  almost all EU institutions' footer and navigation links
  (`european-union.europa.eu`, `consilium.europa.eu`, `curia.europa.eu`, …),
  not references a sanctions reader would follow. Treat them as low-signal.
- **The US and UK rows carry the real signal.** `federalregister.gov` (14 links
  from the BIS page), `ecfr.gov`, `regulations.gov`, `nationalarchives.gov.uk`,
  `sanctionssearchapp.ofsi.hmtreasury.gov.uk` and
  `assets.publishing.service.gov.uk` are where those authorities point for
  rule text and search tooling. Whether `assets.publishing.service.gov.uk`
  is a new host or part of the already-registered `gov.uk` publisher was not
  checked.
- **No `ofac-sdn` row means unmeasured, not "links nowhere".** OFAC's page
  returned one link, so its outbound references are unknown.

## What this does not tell us

- **Landing pages only.** Eight pages cannot represent the authorities'
  outbound links; deeper pages (guidance, FAQs, press releases) would add more.
  I did not go deeper because the ruling covered a handful of pages.
- **One authority failed and one was opaque.** `eu-consolidated-list`
  (redirect loop) and `ofac-sdn` (script-driven page) contribute nothing.
- **`ua-nsdc-sanctions` was not read at all.** It is unregistered, so its host
  is outside the ruling, and Wayback copies (the other option) were not used.
- Counts come from one fetch each on 2026-10-07. Pages change.
- Whether each host is the official host of the body it appears to belong to
  was **not verified**.

## Next steps (not done)

- Confirm or withdraw the DR-0071(a) reading above.
- This list feeds B1 (Track B), blocked until DR-0072's successor is recorded
  (issue #56). It is not a registration queue.
- Two A2 sources remain open on #53: Wikipedia citation graphs and OSINT
  source lists.
