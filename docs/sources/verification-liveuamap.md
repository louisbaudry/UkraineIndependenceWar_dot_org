# Verification record — `liveuamap` (third war-fact candidate)

**Status:** Verification record for one candidate registration. Nothing here is
registered, nothing is collected into the project's archive, and nothing is
enacted by this document. Registering it is the founder's act, separately from
`isw-orca` and `deepstatemap` (issue #47).
**Verified:** 2026-10-05, from this session's container.
**Candidate:** `liveuamap` in
[`sources/candidates/war-facts.yaml`](../../sources/candidates/war-facts.yaml).
Follow-up to [`verification-war-facts-first-two.md`](verification-war-facts-first-two.md),
which could not reach it (403) on 2026-09-21.

## 1. What it is

Liveuamap is a commercial live-map news service run by Liveuamap LLC (USA). It
shows individually geolocated event reports (strikes, explosions, troop
movements), found by "AI web crawlers" in social media and passed to editors
before they are displayed, by its own account on its About page. It is **not**
a front-line geometry series and not an analytical narrative, so it is a
different kind of source from the first two war-fact candidates: nearer the
strike-tracking sources' subject than territorial control.

## 2. What was checked, in order

1. **Reachability.** `https://liveuamap.com/` and `https://ukraine.liveuamap.com/`
   return 200 through Cloudflare. The 403 of 2026-09-21 did not recur. Whether
   that was this session's network or a change on the site was not determined.
2. **Content.** The Ukraine regional page is server-rendered HTML with about 30
   recent event items and a world-wide banner (non-Ukraine items appear on
   it). One capture is the latest items only, not a history.
3. **Rights.** `robots.txt` names only a sitemap. The Terms of Use sit on the
   About page (`/about#terms`; `/terms` is a 404). They say a user "may use our
   data and maps, including map tiles and areas polygons partially, or in the
   whole in your work, with reference to liveuamap.com", and that text and
   images from third-party networks are "distributed under Terms of Service of
   original resources". No clause on automated access or on archiving was
   found. The page also sells a paid API ($150 a month, 200 requests a day,
   GeoJSON), which is the publisher's sanctioned structured route.
4. **Not done, deliberately.** No undocumented data endpoint was probed. The
   page's inline script uses obfuscated variable names, which reads as an
   effort to discourage scraping, and the project's method is to follow what a
   site documents, not to guess around it.
5. **Rehearsal** through the real collector, as for every earlier candidate. A
   throwaway PostgreSQL database was built from `schema/0*.sql`; the candidate
   was registered into it with `register.commit` using the merged class
   defaults; `collector/run.py` ran with the real `HttpFetcher`. Result: 1
   discovered, 1 acquired, 0 failed, **299 194 bytes**, **0 documentary
   assertions**. The database and archive were then destroyed.

## 3. A bug the rehearsal caught

The first draft used `source_type: media-aggregator`. `register.py`'s
description step accepted it and `registry/validate.py` reported 0 errors, but
the rehearsal's `commit` failed on the foreign key `source_source_type_fkey`:
that value is not in `registry/vocabularies/source-types.yaml`. Changed to
`news-media`. **So `register.py`'s dry description does not check
`source_type` against the registry; only a commit does.** Not fixed here: it
is a separate gap, worth its own card.

## 4. What this does and does not settle

**Settled:** the page exists, is reachable, matches the category, and a real
`Collector` run against it succeeds with zero documentary assertions.

**Not settled, and not this session's to settle:**
- **Whether the Terms of Use allow this.** The attribution grant is permissive
  in wording but sits beside a paid API and is silent on automated capture and
  on archiving. It is a legal question (POL-0001 section 10), and the
  `UNVERIFIED` rights position stays. The only safe reading is
  `may-preserve`, with no redistribution claim.
- **Coverage over time.** A capture holds the latest ~30 items. Without a
  daily (or more frequent) schedule, which `docs/infrastructure.md` records as
  not running, most items would never be captured.
- **Third-party content.** The items link to posts and images by other people,
  some of which may show named individuals or graphic material. Those are not
  fetched by this candidate, and the candidate does not structure anything
  (DR-0071(b)).
- **Which class it belongs to.** It sits in `war-facts-territorial-control`
  only for that class's conservative rights default; it is closer to an
  event-report source. Moving it is a registration-time question.
- **Grades.** C and 3 are the drafter's triage judgement for an aggregator
  whose items come from social media; the founder owns them (DR-0027).
- **The coverage start** in the candidate is a placeholder and was not checked.

## Sources

- [`sources/candidates/war-facts.yaml`](../../sources/candidates/war-facts.yaml) — the entry
- [`verification-war-facts-first-two.md`](verification-war-facts-first-two.md) — the two sibling candidates and the rehearsal method
- Retrieved 2026-10-05: `https://liveuamap.com/about` (About, Privacy, Terms), `https://liveuamap.com/promo/api` (pricing), `https://liveuamap.com/robots.txt`, `https://ukraine.liveuamap.com/`
