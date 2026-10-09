# Census A2 — OSINT and monitoring sources (from the Wikipedia sample)

> **Status: informal working note.** Not a registration, not an authorization to
> collect, not a Decision Record. The last of the editorial evidence sources of
> WP 3.4 §4.1 Track A item A2 (issue #53). **AI provenance (record §80):**
> drafted by an AI assistant (Anthropic Claude Code agent session) on
> 2026-10-09; nothing here has been reviewed by the founder.

## What this is

A cross-check of which open-source-intelligence (OSINT) trackers, conflict
monitors and think-tank data pages are **actually cited** by English Wikipedia
war articles, using the data already pulled for
[the Wikipedia citation-graph note](census-a2-wikipedia-citation-graph.md)
(72 articles, 19 023 links). It adds no new query and fetches no candidate host
(DR-0071(a), WP 3.4 §4.1).

## Method and its main limit

The names probed are **a probe list written from the assistant's own recall of
well-known trackers, monitors and institutions**, not a list taken from any
published OSINT directory. Each name was then looked up (exact host or subdomain
match) in the saved Wikipedia host counts. So:

- A hit is evidence: the number is real, from Wikipedia's API.
- A miss means only "not linked from these 72 articles". It does **not** mean the
  source is unimportant, and the probe list itself may have missed sources nobody
  on this project has thought of. A bibliography of published OSINT directories
  or the founder's own list would be a better seed; this is the cheap first pass.

## Result — probes that appeared (articles of 72 / links)

| Host | Articles | Links | What it is (as far as the host name and context show; not verified) |
|---|---|---|---|
| `understandingwar.org` | 23 | 153 | Think-tank daily assessments |
| `suspilne.media` | 9 | 60 | Ukrainian public broadcaster |
| `csis.org` | 8 | 11 | Think tank |
| `rusi.org` (+ `static.rusi.org`) | 7 (+4) | 12 (+4) | Think tank |
| `bellingcat.com` (+ `ukraine.`, `ru.` subdomains) | 7 (+2, +1) | 7 (+2, +2) | Investigative OSINT collective |
| `criticalthreats.org` | 6 | 9 | Think-tank project |
| `gur.gov.ua` (+ `war-sanctions.gur.gov.ua`) | 4 (+1) | 4 (+1) | Ukrainian military intelligence |
| `kse.ua` | 3 | 3 | Economics school |
| `gp.gov.ua` | 3 | 3 | Prosecutor General's Office |
| `liveuamap.com` | 2 | 2 | Live conflict map |
| `mod.gov.ua` (+ `sprotyv.mod.gov.ua`) | 2 (+1) | 3 (+1) | Ministry of Defence |
| `mil.gov.ua` | 2 | 2 | Armed forces |
| `deepstatemap.live` | 1 | 1 | Front-line map |
| `militaryland.net` | 1 | 1 | Military-situation site |
| `sipri.org` | 1 | 1 | Arms-transfer research |
| `ukraine.ohchr.org` | 2 | 3 | UN human-rights monitoring (same publisher as the registered `un-hrmmu-protection-of-civilians`) |
| `hrw.org`, `amnesty.org`, `ohchr.org`, `icc-cpi.int`, `osce.org`, `hudoc.echr.coe.int` | 5 to 21 | 6 to 110 | Human-rights and legal bodies, ranked in the main note |

## Result — probes with no hit in the sample

`oryxspioneer.com`, `deepstatemap.com`, `acleddata.com`, `warspotting.com`,
`informnapalm.org`, `conflictintelligence.com`, `cit.com.ua`, `gdeltproject.org`,
`globalsecurity.org`, `mediaforensics.org`, `firms.modaps.eosdis.nasa.gov`,
`sentinel-hub.com`, `yalehumanitarianresearch.org`, `hub.conflictobservatory.org`,
`ukrainianwitness.org`. Not linked from these articles; see the limit above.

## Reading it

- **Overlap with what is registered or ruled:** `kpszsu`/`generalstaffzsu` (strike
  tracking) and `ua-pgo-crime-statistics` have Wikipedia counterparts in
  `gp.gov.ua` and `mil.gov.ua` only thinly; `ukraine.ohchr.org` is the one clear
  overlap with a registered source.
- **Think-tank daily assessments are the most-cited OSINT-style host** by a wide
  margin (`understandingwar.org`, 23 articles), far above any map or tracker.
- **Civilian-harm relevance (DR-0109):** `bellingcat.com` and the human-rights
  bodies are the hosts most plausibly relevant to civilian-harm sources; none is
  registered, and this note does not propose registering any.
- **Rights and personal-data questions are open for every host here** and belong
  to Track B and the pending POL-0001 §10 review.

## Not done

- No OSINT directory, bibliography or the founder's own list was consulted; this
  is a probe against one index only.
- No host was checked for reachability, scope or rights.

## Sources

- The saved English Wikipedia `prop=extlinks` data behind the citation-graph note
  (queried 2026-10-09). WP 3.4 §4.1; DR-0071(a); issue #53.
