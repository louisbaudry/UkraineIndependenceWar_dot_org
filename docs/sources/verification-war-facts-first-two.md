# Verification record — first two war-fact candidates (territorial control)

**Status:** Verification record for two candidate registrations. Nothing
here is registered, nothing is collected into the project's archive, and
nothing is enacted by this document. This is the first work in a new
subject area — territorial control / military operations — following the
founder's 2026-09-20/21 redirection toward war-fact material, over
continuing to add sanctions-authority candidates. Registering either is
the founder's act (CLAUDE.md standing ruling for every candidate).
**Verified:** 2026-09-21, from this session's container.
**Candidates:** `isw-orca`, `deepstatemap` in
[`sources/candidates/war-facts.yaml`](../../sources/candidates/war-facts.yaml)
— a new file, the first outside `sanctions-authorities.yaml`.

## 1. Why these two, and why together

The founder chose territorial control / military operations as the first
war-fact category to source, over civilian harm or war-crimes documentation,
for its lower personal-data sensitivity — no named individuals, no
casualty records, nothing POL-0001's still-pending §10 review would flag.
Territorial control is also foundational: an incident, a casualty report,
or a war-crimes allegation each needs a place and a date to sit against,
which this category supplies.

Two sources were chosen as a deliberately complementary pair, not two
independent candidates: **DeepStateMap** gives the geometry (which polygon
is under whose control, as of when), **ISW** gives the narrative (why the
line moved, what operation caused it). Neither substitutes for the other.

## 2. What was done, in order

1. Reachability-tested three initial candidates: ISW's assessment index
   (200, redirects), DeepStateMap (200), LiveUAmap (403, not pursued
   further this session — a proxy or Cloudflare-style block, not
   distinguished which).
2. For ISW: followed the index page's own links to find the actual dated
   report format, confirmed the 2026-09-20 report resolves (following a
   301 from an older URL scheme to ISW's current one), and read the page
   for a license/rights statement directly rather than assuming — found
   "ALL RIGHTS RESERVED" in the footer text.
3. For DeepStateMap: the rendered page is a JS SPA with no visible API
   link in its raw HTML, so tried known public API URL patterns rather
   than guessing blind, matching the project's established method (seco-
   sanctions' navigation-following, not URL-guessing). `/api/history/last`
   worked immediately, unauthenticated, returning real GeoJSON. Fetched
   twice 40 seconds apart to check short-window stability (identical:
   same map id, same byte count) — deliberately not treated as a claim
   about long-window stability, since a live front-line dataset changing
   is the point of the source, not a defect. Searched the site for
   license/terms text; found none.
4. **Rehearsal**, matching every sanctions-candidate precedent. A
   throwaway PostgreSQL database was built from `schema/0*.sql`. Both
   sources inserted directly (not through `register.py`, matching the
   BIS/OFSI/SECO rehearsals' approach). The real `Collector`
   (`collector/pipeline.py`, two-agent split per DR-0097) was run with
   the real `HttpFetcher` against both locators, into a throwaway OCFL
   root. Both succeeded: 1 discovered, 1 acquired, 0 failed each — ISW
   445 121 bytes, DeepStateMap 627 479 bytes. Database and storage then
   destroyed.

## 3. The two candidates

| | ISW ORCA | DeepStateMap |
| --- | --- | --- |
| `source_type` | `think-tank` | `public-dataset` |
| Locator (index) | `understandingwar.org/analysis/russia-ukraine/russian-offensive-campaign-assessment/` | `deepstatemap.live/` |
| Run locator (as fetched) | `understandingwar.org/research/.../russian-offensive-campaign-assessment-september-20-2026/` | `deepstatemap.live/api/history/last` |
| Format | HTML page with embedded maps/graphics — captured as `warc` | Bare JSON body — captured as `http` |
| Cadence | Daily, one dated report | Continuous/live |
| Rights | UNVERIFIED, but "ALL RIGHTS RESERVED" stated directly on the site | UNVERIFIED — no license/terms found anywhere in this session's search |
| Locator staleness | The dated URL **will** go stale daily, same re-verification obligation `eur-lex-sanctions` carries (DR-0105) | The endpoint itself is stable; its *content* changes continuously, which is expected, not staleness |

## 4. What this does and does not settle

**Settled by this record:** both sources exist, are reachable from this
session, match the founder's chosen category, and a real `Collector` run
against them succeeds cleanly with zero documentary assertions.

**Not settled, and not this session's to settle:**
- **DeepStateMap's actual licensing/reuse terms** — not found by searching
  the site; may need direct outreach to the DeepState team, or a closer
  look at their Telegram/social presence, which this session did not
  attempt.
- **ISW's daily re-verification cadence in practice.** A single dated URL
  per run is the pattern, matching `eur-lex-sanctions`'s obligation — but
  unlike a monthly-amended legal instrument, ISW publishes *every day*,
  so whoever runs this source needs the current date's URL each time, not
  an occasional check.
- **DeepStateMap's history/past-snapshot access.** The site has its own
  interface for browsing dated past states, unverified and not part of
  `run_locators` yet — only the *current* snapshot is covered here.
- **LiveUAmap** was reachability-tested (403) and not pursued further —
  worth a retry from a session whose network reaches it, since it's a
  third source in the same category some OSINT researchers rely on
  alongside these two.
- **Whether either belongs to a new registration class at all**, or
  should join/split differently once more war-fact candidates arrive — one
  class with two members, drafted the same way the sanctions classes were
  (DR-0103), but not yet exercised at the scale that would test the
  grouping choice.
- Registration itself, per the standing ruling that this is the founder's
  act, per source.

## Sources

- [`sources/candidates/war-facts.yaml`](../../sources/candidates/war-facts.yaml) — both candidate entries
- [`docs/decision-records/DR-0105-eur-lex-sanctions-registration.md`](../decision-records/DR-0105-eur-lex-sanctions-registration.md) — precedent for a locator that legitimately goes stale and needs per-run re-verification
- [`docs/sources/verification-seco-sanctions.md`](verification-seco-sanctions.md) — precedent for "follow the site's real navigation / a known API pattern, don't guess a URL"
