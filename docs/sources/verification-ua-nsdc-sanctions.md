# Verification record — NSDC sanctions decisions (Ukraine)

**Status:** Verification record for one candidate registration —
**UNBLOCKED 2026-09-22** by human-assisted (browser) access, which passed
the Cloudflare challenge every automated session had failed. The
2026-09-21 Wayback-history check's working hypothesis
(search-UI-only, no bulk export) is **overturned**: the register exposes a
dedicated bulk-download page with structured CSV/XLSX exports per entity
class. Nothing here is registered, nothing is collected, and nothing is
enacted by this document. Registering this candidate is the founder's act
(CLAUDE.md standing ruling).
**Verified:** 2026-09-20, ~19:00–19:10 UTC (automated, blocked); Wayback
follow-up 2026-09-21, ~19:10–19:25 UTC (automated, blocked); human-assisted
browser access 2026-09-22 (founder, screenshot evidence — see §2b).
**Candidate:** `ua-nsdc-sanctions` in
[`sources/candidates/sanctions-authorities.yaml`](../../sources/candidates/sanctions-authorities.yaml).

## 1. What was done, in order

1. Confirmed `www.rnbo.gov.ua` (the candidate's `locator`) is reachable
   from this session — 200, full page fetched. `sanctions-t.rnbo.gov.ua`,
   the subdomain A2's 2026-09-17 live Wayback query surfaced as "worth a
   look" (25 captures, 2021-04-22 to 2022-05-20), is **not** reachable:
   this session's egress proxy rejected the CONNECT to it outright
   (`connect_rejected — organization policy`), distinct from a site-side
   block. That subdomain's captures remain unexplored from this session;
   a future session with different proxy rules, or Wayback itself (which
   *is* reachable, per A2's 2026-09-17 record), may reach it.
2. Followed rnbo.gov.ua's own navigation (`/ua/Documents/` →
   `/ua/Ukazy/` for presidential decrees) rather than guessing a URL
   pattern, per the project's established method (seco-sanctions record
   §0). Found that recent decree pages there are routinely
   sanctions-adjacent (interdepartmental sanctions-policy appointments,
   e.g. Decree № 919/2026 of 2026-09-15, "Питання Міжвідомчої комісії з
   політики військово-технічного співробітництва та експортного
   контролю"), confirming rnbo.gov.ua **publishes about** the sanctions
   mechanism, but that these decree pages are not themselves the
   sanctions *list*.
3. Found the actual authoritative register: every page on rnbo.gov.ua
   carries a persistent navigation link, **"Державний реєстр санкцій"**
   (State Register of Sanctions), to a **separate host**:
   `https://drs.nsdc.gov.ua`. This matches the candidate's `scope_rules`
   far more precisely than the decree pages do — it is the NSDC's own
   register of the sanctions decisions and enacting decrees the candidate
   is meant to cover, not a secondary news mention of them.
4. `drs.nsdc.gov.ua` returned **HTTP 403** on every path tried (root,
   `/api`, `/api/sanctions`, `/sitemap.xml`, `/robots.txt`) — a Cloudflare
   managed challenge (`cf-mitigated: challenge`, `server: cloudflare`,
   title "Just a moment..."), the same class of block this session found
   on Légifrance (see
   [`docs/sources/verification-lil-articles.md`](verification-lil-articles.md)).
   The proxy completes the TLS handshake; Cloudflare still blocks before
   any page content.

## 2. What this settles, and what remains blocked

**Settled:** the specific instrument category this candidate should point
to is the NSDC's **State Register of Sanctions**, `drs.nsdc.gov.ua` — not
rnbo.gov.ua's own decree pages, which are a secondary publication surface
about the same decisions, not the register itself. This narrows the
candidate's locator meaningfully: `rnbo.gov.ua` (the current `locator`
field) is the *publisher*, correctly, but the *register* a `run_locator`
would need to point at is a different host entirely, exactly the same
correction seco-sanctions needed (whose real file also lived on a
different host — `sesam.search.admin.ch` — than its publisher's main site).

**Blocked:** everything past that — whether the register exposes a
bulk-downloadable list (CSV/XML/JSON) the way SECO's does, or only a
searchable web interface the way the EU's FSF application does (unusable
as a source address per the `eu-consolidated-list` candidate's own note),
or something else, cannot be determined without passing the Cloudflare
challenge. **No rehearsal was attempted** against `drs.nsdc.gov.ua` for
this reason — there is no confirmed fetchable locator to rehearse against,
unlike `eur-lex-sanctions` where a rehearsal made sense once two concrete
instrument URLs were confirmed reachable.

## 2a. The Wayback workaround, tried 2026-09-21

Per the "Next steps" below (as originally drafted), queried
`drs.nsdc.gov.ua` through Wayback's CDX index instead of fetching it live,
using `sources/census.py`'s already-tested `WaybackCdxClient` and direct
CDX queries. Wayback itself was reachable this session, intermittently
(the Internet Archive returned its own "Temporarily Offline" page and a
connection reset on two of five attempts — worth noting as its own
instability, separate from the Cloudflare block on the live site).

**Result:** `drs.nsdc.gov.ua` has **3 489 Wayback captures**, first seen
2024-02-02, **last seen 2026-08-24** — recent enough to be a live,
actively crawled site, not an archived-and-abandoned one. This confirms
the register exists and is real, but does not unblock verification:
- The captured URL pattern is overwhelmingly a client-side **search
  application** — `/actions/personal?searchQuery=<name>` — a person-search
  UI, not a bulk list.
- A large fraction of the captures are themselves **HTTP 403** with
  Cloudflare challenge-token query parameters (`__cf_chl_tk=...`),
  meaning Wayback's own crawler was blocked at capture time on many
  attempts — the same wall this session hit live, just recorded
  historically instead of encountered directly.
- A filtered CDX query across up to 5 000 captures for common
  bulk-export MIME types (`text/csv`, `application/json`,
  `application/xml`, `text/xml`, `application/vnd.ms-excel`,
  `application/octet-stream`) returned **zero matches**, across three
  attempts. No evidence surfaced of a downloadable list file anywhere in
  Wayback's history of this host.

**What this changes:** the working hypothesis for §3's "next steps" below
shifts from "unknown whether it's a bulk export or search-only" to
**probably search-only, with no bulk export ever observed** — consistent
with a search-UI architecture, though absence of a CSV/JSON capture in
Wayback's history is evidence, not proof, that no such endpoint exists.

## 2b. Human-assisted browser access, 2026-09-22

The founder reached `https://drs.nsdc.gov.ua` directly in a browser,
passing the Cloudflare challenge that blocked every prior automated
attempt (§1.4, §2a). The site has a **"Data integration"** section
(separate from the search UI at `/actions/personal`) with three tabs:
"Downloading sanctions actions," "Loading subjects" (shown), and "API
documentation." The "Loading subjects" tab provides a **"Download file"**
panel: "Full list of unique entities according to selected filters,"
with per-entity-class CSV and XLSX downloads, each showing a live record
count as of the page's stated last update (Decree No. 901/2026 of
2026-09-13):

| Entity class | Records | Formats |
|---|---|---|
| Legal entities | 9,682 | CSV, XLSX |
| Individuals | 13,900 | CSV, XLSX |
| Vessels | 888 | CSV, XLSX |
| Aircraft | 0 | CSV, XLSX |

A left-hand filter panel (subject status, decree, sanction type, end
date, country/territory) scopes the export; the screenshot shows no
filters applied, i.e. the full unfiltered register per class. The page
also documents "Description of the file structure" per entity class
(collapsed sections, not yet expanded/read) and a separate **API
documentation** tab exists, unexplored.

**This overturns §2a's working hypothesis.** The register is not
search-UI-only: it has an authoritative bulk-export mechanism that
matches the shape every other registered sanctions source uses (a
downloadable structured list), making this candidate's registration
shape the *same* as `eu-consolidated-list`/`ofac-sdn`/`seco-sanctions`,
not the decree-stream alternative §3 (prior revision) considered.

**Not yet captured:** the exact download URLs (button `href`s), response
headers, content-type, and a byte-for-byte sample of at least one export
— none of this was read from the page itself, only observed visually.
`sources/register.py`'s schema needs a concrete `run_locator` (or one per
entity class, if this is registered as either one candidate covering all
four classes or split the way `bis-entity-list`'s Denied-Persons-List-only
scoping split a multi-list source). The "Description of the file
structure" sections need reading before scope_rules can be drafted
responsibly (DR-0071(b) — no automatic structuring of personal data means
the field layout of "Individuals" matters before this is registered).

## 3. Next steps

**No longer blocked on Cloudflare** — human-assisted access works. What
remains before this is registration-ready:
1. Confirm the exact download URLs (right-click → copy link, or read the
   Network tab when clicking a Download button) for each entity class's
   CSV and/or XLSX.
2. Read the "Description of the file structure" sections for at least
   "Individuals" and "Legal entities," since those two carry personal
   and organizational data respectively.
3. Decide the registration shape: one candidate spanning all four entity
   classes vs. one candidate per class (precedent: `bis-entity-list` was
   approved for its Denied Persons List half only, not the full BIS
   entity list) — a founder question once §3.1–3.2 are done, not decided
   here.
- `sanctions-t.rnbo.gov.ua` (the A2-surfaced Wayback lead) is no longer
  needed as a fallback path now that the register itself is reachable;
  left unexplored.
- The decree-stream registration shape (§3, prior revision) is now
  believed **unnecessary** — the bulk-export mechanism found in §2b
  supersedes that fallback — but is not formally withdrawn until §3.1–3.2
  confirm the export is genuinely complete (all sanctioned entities, not
  a partial or delayed-update subset).

## Sources

- [`sources/candidates/sanctions-authorities.yaml`](../../sources/candidates/sanctions-authorities.yaml) — `ua-nsdc-sanctions` entry
- [`sources/README.md`](../../sources/README.md) — A2's 2026-09-17 live-query record naming `sanctions-t.rnbo.gov.ua`
- [`docs/sources/verification-lil-articles.md`](verification-lil-articles.md) — the same Cloudflare-challenge block, independently confirmed on a different site
- [`docs/sources/verification-seco-sanctions.md`](verification-seco-sanctions.md) — precedent for "the real file lives on a different host than the publisher's main site"
