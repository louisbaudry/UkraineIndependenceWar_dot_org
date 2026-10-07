# Census A2 — academic bibliographies (Crossref reference lists)

> **Status: informal working note.** Not a registration, not an authorization to
> collect, not a Decision Record. One of the four editorial evidence sources of
> WP 3.4 §4.1 Track A item A2 (issue #53). **AI provenance (record §80):**
> drafted by an AI assistant (Anthropic Claude Code agent session) on
> 2026-10-07 from one session's live Crossref queries; nothing here has been
> reviewed by the founder.

## What this is

A ranked list of web hosts that peer-reviewed papers about Ukraine **cite in
their reference lists**, as candidate domains for the census. The evidence for
each host is only how many papers cite it. It says nothing about whether a
host is authoritative, durable, lawful to collect, or in scope — those are
Track B judgements.

Nothing was fetched from any candidate host. The only service contacted was
Crossref's public API (`api.crossref.org`), an index of what publishers
deposited (WP 3.4 §4.1: indices only, DR-0071(a)).

## Method (reproducible)

1. For each of six title queries — `Ukraine war`, `Russian invasion Ukraine`,
   `war crimes Ukraine`, `sanctions Russia Ukraine`, `Ukraine civilian casualties`,
   `Ukraine disinformation` — page the Crossref works endpoint (`query.title=<q>`,
   `filter=from-pub-date:2022-02-24,type:journal-article,has-references:true`,
   `select=DOI,title,reference`, `rows=100`, cursor paging, 4 pages, 1 s
   between requests, identifying `User-Agent`).
2. Keep only papers whose title contains `ukrain` (case-insensitive), deduplicated
   by DOI: **354 papers, 9 194 deposited references.**
3. Extract every `http(s)://` URL from each reference record; reduce to the
   host (lower-case, leading `www.` removed).
4. Drop hosts that identify a publisher, repository, shortener, archive or
   social platform rather than a candidate source: `doi.org`, `dx.doi.org`,
   `id.crossref.org`, `rb.gy`, `bit.ly`, `tinyurl.com`, `t.co`, `goo.gl`, `ow.ly`,
   `archive.org`, `web.archive.org`, `archive.is`, `archive.ph`, `ssrn.com`,
   `papers.ssrn.com`, `jstor.org`, `springer.com`, `link.springer.com`,
   `sciencedirect.com`, `tandfonline.com`, `onlinelibrary.wiley.com`,
   `cambridge.org`, `academic.oup.com`, `journals.sagepub.com`, `researchgate.net`,
   `scholar.google.com`, `books.google.com`, `google.com`, `zenodo.org`, `osf.io`,
   `arxiv.org`, `pubmed.ncbi.nlm.nih.gov`, `ncbi.nlm.nih.gov`, `youtube.com`,
   `facebook.com`, `twitter.com`, `x.com`. **879 hosts remain.**
5. Rank by **distinct citing papers** (one paper citing a host twenty times
   counts once), then by raw citing references.

## Result — top 40

| # | Host | Citing papers (of 354) | Citing references |
|---|---|---|---|
| 1 | `zakon.rada.gov.ua` | 37 | 144 |
| 2 | `ukrstat.gov.ua` | 25 | 38 |
| 3 | `ec.europa.eu` | 18 | 26 |
| 4 | `data2.unhcr.org` | 14 | 17 |
| 5 | `theguardian.com` | 11 | 14 |
| 6 | `who.int` | 10 | 14 |
| 7 | `eur-lex.europa.eu` | 9 | 15 |
| 8 | `bbc.com` | 9 | 13 |
| 9 | `unhcr.org` | 8 | 14 |
| 10 | `nytimes.com` | 8 | 9 |
| 11 | `oecd.org` | 8 | 8 |
| 12 | `apps.who.int` | 7 | 9 |
| 13 | `bank.gov.ua` | 7 | 9 |
| 14 | `euro.who.int` | 7 | 9 |
| 15 | `un.org` | 6 | 7 |
| 16 | `kmu.gov.ua` | 5 | 9 |
| 17 | `rferl.org` | 5 | 7 |
| 18 | `data.worldbank.org` | 5 | 6 |
| 19 | `drive.google.com` | 5 | 6 |
| 20 | `economy.nayka.com.ua` | 5 | 6 |
| 21 | `imf.org` | 5 | 6 |
| 22 | `nbuv.gov.ua` | 5 | 6 |
| 23 | `razumkov.org.ua` | 5 | 6 |
| 24 | `reuters.com` | 5 | 6 |
| 25 | `dw.com` | 5 | 5 |
| 26 | `epravda.com.ua` | 5 | 5 |
| 27 | `unicef.org` | 5 | 5 |
| 28 | `transparency.org` | 4 | 9 |
| 29 | `worldbank.org` | 4 | 9 |
| 30 | `nato.int` | 4 | 6 |
| 31 | `w1.c1.rada.gov.ua` | 4 | 6 |
| 32 | `washingtonpost.com` | 4 | 6 |
| 33 | `academia.edu` | 4 | 4 |
| 34 | `bloomberg.com` | 4 | 4 |
| 35 | `cfr.org` | 4 | 4 |
| 36 | `eeas.europa.eu` | 4 | 4 |
| 37 | `fao.org` | 4 | 4 |
| 38 | `me.gov.ua` | 4 | 4 |
| 39 | `ohchr.org` | 4 | 4 |
| 40 | `politico.eu` | 4 | 4 |

The tail is long: 879 hosts in all, most cited by a single paper.

## What this does not tell us

- **Selection bias.** Crossref title search for "Ukraine" returns whatever
  disciplines wrote about Ukraine in titles; judging only from the hosts, weighted to
  economics, public health and law; war-documentation and OSINT sources are
  probably under-represented. This is why the OSINT-list source, not this
  one, is expected to surface those.
- **Only deposited references count.** Publishers choose whether to deposit
  reference lists and whether URLs appear in them; coverage is uneven and
  was not measured.
- **Host, not page.** A host is a candidate domain, not a document. Link rot
  among cited URLs was not checked, because that would require fetching
  them.
- **A first attempt was discarded.** An earlier run used
  `query.bibliographic` (fuzzy matching, not a relevance filter) and returned
  papers unrelated to the war, so its hosts (heritage bodies, COVID pages)
  were noise. The title-restricted run above replaced it. A sample taken on
  one day is not a stable ranking; Crossref's relevance order and contents
  change.
- Hostnames in the table are as they appear in reference strings. Whether each
  is the official host of the organisation it appears to belong to was **not
  verified**.

## Next steps (not done)

- Do not read this list as a registration queue. It feeds B1 (Track B), which
  stays blocked until DR-0072's successor is recorded (issue #56).
- Three A2 evidence sources remain open on #53: Wikipedia citation graphs,
  sanctions-authority link graphs, OSINT source lists. In this session
  Wikipedia and OpenAlex answered HTTP 429 from the shared egress address,
  while Crossref and Wikidata answered 200; reachability varies by session.
