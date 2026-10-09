# Census A2 — Wikipedia citation graph (external links)

> **Status: informal working note.** Not a registration, not an authorization to
> collect, not a Decision Record. One of the four editorial evidence sources of
> WP 3.4 §4.1 Track A item A2 (issue #53). **AI provenance (record §80):**
> drafted by an AI assistant (Anthropic Claude Code agent session) on
> 2026-10-09 from one session's live Wikipedia API queries; nothing here has
> been reviewed by the founder.

## What this is

A ranked list of web hosts that English Wikipedia articles about the war **link
to as references**, as candidate domains for the census. The evidence for each
host is only how many of the sampled articles link to it. It says nothing about
whether a host is authoritative, durable, lawful to collect, or in scope — those
are Track B judgements. Wikipedia editors choosing a link is a popularity signal
of the English-language press, not a quality signal.

Nothing was fetched from any candidate host. The only service contacted was
English Wikipedia's public MediaWiki API (`en.wikipedia.org/w/api.php`), an
index of what editors cited (WP 3.4 §4.1: indices only, DR-0071(a)).

## Method (reproducible)

1. For each of eight search queries — `Russian invasion of Ukraine`,
   `Russo-Ukrainian War`, `war crimes Russian invasion Ukraine`,
   `sanctions Russia Ukraine invasion`, `civilian casualties Russian invasion
   Ukraine`, `attacks on Ukraine energy infrastructure`, `Ukrainian prisoners of
   war`, `Russian strikes Ukrainian cities` — take the top 15 main-namespace
   results (`list=search`). Deduplicated: **72 articles.**
2. Read each article's external links with `prop=extlinks` (`ellimit=max`,
   20 titles per request, `elcontinue` paging, 3 s between requests,
   identifying `User-Agent`, `maxlag=5`, back-off on HTTP 429): **19 023 links.**
3. Reduce each link to its host (lower-case, leading `www.` removed).
4. Drop hosts that are Wikimedia projects, archives, link resolvers, catalogues
   or social platforms rather than candidate sources: `web.archive.org`,
   `archive.org`, `archive.is`, `archive.ph`, `doi.org`, `dx.doi.org`,
   `worldcat.org`, `books.google.com`, `google.com`, `youtube.com`, `youtu.be`,
   `facebook.com`, `twitter.com`, `x.com`, `t.me`, `instagram.com`, `jstor.org`,
   and any `*wikipedia.org`, `*wikimedia.org`, `*wikidata.org`. **2 071 hosts
   remain.** (`search.worldcat.org` was *not* dropped by the exact-match list
   and appears at #4 below; it is a catalogue, not a source.)
5. Rank by **distinct citing articles**, then by raw link count.

## Result — top 40

| # | Host | Articles (of 72) | Links |
|---|---|---|---|
| 1 | `theguardian.com` | 62 | 535 |
| 2 | `reuters.com` | 58 | 1012 |
| 3 | `bbc.com` | 55 | 519 |
| 4 | `search.worldcat.org` | 54 | 256 |
| 5 | `aljazeera.com` | 48 | 242 |
| 6 | `nytimes.com` | 47 | 318 |
| 7 | `kyivindependent.com` | 46 | 500 |
| 8 | `edition.cnn.com` | 45 | 227 |
| 9 | `apnews.com` | 44 | 215 |
| 10 | `pravda.com.ua` | 43 | 286 |
| 11 | `themoscowtimes.com` | 42 | 228 |
| 12 | `rferl.org` | 41 | 142 |
| 13 | `washingtonpost.com` | 40 | 211 |
| 14 | `dw.com` | 39 | 113 |
| 15 | `cnn.com` | 37 | 145 |
| 16 | `politico.eu` | 37 | 109 |
| 17 | `kyivpost.com` | 36 | 128 |
| 18 | `meduza.io` | 34 | 108 |
| 19 | `businessinsider.com` | 34 | 92 |
| 20 | `bbc.co.uk` | 33 | 122 |
| 21 | `france24.com` | 33 | 97 |
| 22 | `wsj.com` | 33 | 92 |
| 23 | `npr.org` | 32 | 73 |
| 24 | `newsweek.com` | 31 | 56 |
| 25 | `telegraph.co.uk` | 30 | 93 |
| 26 | `ukrinform.net` | 29 | 96 |
| 27 | `independent.co.uk` | 29 | 83 |
| 28 | `ft.com` | 28 | 94 |
| 29 | `euronews.com` | 28 | 88 |
| 30 | `forbes.com` | 27 | 71 |
| 31 | `abcnews.go.com` | 27 | 57 |
| 32 | `english.nv.ua` | 25 | 96 |
| 33 | `lemonde.fr` | 25 | 41 |
| 34 | `news.un.org` | 24 | 93 |
| 35 | `cnbc.com` | 24 | 69 |
| 36 | `timesofisrael.com` | 24 | 64 |
| 37 | `news.yahoo.com` | 24 | 62 |
| 38 | `thehill.com` | 24 | 45 |
| 39 | `understandingwar.org` | 23 | 153 |
| 40 | `news.sky.com` | 23 | 54 |

### Institutional and primary-source hosts only

The list above is dominated by the press. Filtering to international bodies,
NGOs and governments (host pattern match, then ranked the same way) gives the
hosts closest to this archive's scope. Top 12:

| # | Host | Articles (of 72) | Links |
|---|---|---|---|
| 1 | `news.un.org` | 24 | 93 |
| 2 | `hrw.org` | 21 | 110 |
| 3 | `ohchr.org` | 20 | 83 |
| 4 | `amnesty.org` | 19 | 59 |
| 5 | `un.org` | 13 | 18 |
| 6 | `osce.org` | 10 | 24 |
| 7 | `consilium.europa.eu` | 9 | 31 |
| 8 | `icc-cpi.int` | 9 | 23 |
| 9 | `president.gov.ua` | 9 | 17 |
| 10 | `eeas.europa.eu` | 9 | 10 |
| 11 | `ukraine.un.org` | 8 | 12 |
| 12 | `reliefweb.int` | 8 | 11 |

## Reading it

- **Overlap with what is already registered or decided:** `ohchr.org` (the
  publisher behind `un-hrmmu-protection-of-civilians`, DR-0110) ranks #3 among
  institutional hosts; `home.treasury.gov` (OFAC) and `consilium.europa.eu`
  (EU sanctions) appear in the top 20 institutional hosts. `pravda.com.ua` and
  `kyivindependent.com` rank highly in the press list. `rnbo.gov.ua` was not
  looked up separately.
- **Overlap with the bibliography note** ([academic bibliographies](census-a2-academic-bibliographies.md)):
  the two lists agree on `eur-lex.europa.eu`-type official hosts and `unhcr.org`
  only weakly. Wikipedia leans on the English press; the papers lean on Ukrainian
  legal and statistical hosts (`zakon.rada.gov.ua`, `ukrstat.gov.ua`), which
  barely appear here. Neither list is a substitute for the other.
- **A press host is not an authorized source.** Registering any news outlet is a
  separate founder decision with its own rights question (POL-0001 §10 is
  pending); this note proposes nothing.

## Limits

- One session, one day: the Wikipedia article set is the top 15 search hits for
  eight queries, so it over-represents the highest-traffic English articles and
  says nothing about other language editions.
- Links to a host are counted per article, not per claim; a host linked 500 times
  from one article would still count as 1 article.
- Several hosts appear under two names (`bbc.com`/`bbc.co.uk`, `cnn.com`/
  `edition.cnn.com`). They were not merged.
- Wikipedia's API answered HTTP 429 repeatedly from this session's shared egress
  address; the pull succeeded only with a 3 s delay and back-off. A re-run may
  need the same, and may give slightly different results as articles change.
- Not verified: that any listed host is reachable, in scope or collectable.

## Sources

- English Wikipedia MediaWiki API, `list=search` and `prop=extlinks`, queried
  2026-10-09.
- WP 3.4 §4.1 (census, indices only); DR-0071(a); issue #53.
