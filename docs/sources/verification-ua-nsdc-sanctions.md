# Verification record — NSDC sanctions decisions (Ukraine)

**Status:** Verification record for one candidate registration —
**PARTIALLY BLOCKED**: the mechanism is identified, the actual sanctions
register is not reachable from this session. A 2026-09-21 Wayback-history
check (§2a) found no bulk-export capture in 3 489 historical crawls of the
register, strengthening but not confirming the working hypothesis that it
is a search-UI-only application. Nothing here is registered, nothing is
collected, and nothing is enacted by this document. Registering this
candidate is the founder's act (CLAUDE.md standing ruling).
**Verified:** 2026-09-20, ~19:00–19:10 UTC; Wayback follow-up 2026-09-21,
~19:10–19:25 UTC. Both from this session's container.
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

## 3. Next steps

This needs the same thing Légifrance needs: human-assisted (browser-based)
access, or a session whose network policy passes Cloudflare's managed
challenge. Until then:
- The candidate's `scope_rules` and `locator` in
  `sources/candidates/sanctions-authorities.yaml` are not changed by this
  record — `drs.nsdc.gov.ua` is proposed as the register to target, not
  written in as a decided `run_locator`, since it has not actually been
  reached.
- `sanctions-t.rnbo.gov.ua` (the A2-surfaced Wayback lead) stays
  unexplored — this session's proxy rejected the direct CONNECT to it
  outright (§1.1), and querying it *through* Wayback's CDX index (as §2a
  did for `drs.nsdc.gov.ua`) was not attempted for that specific
  subdomain; worth a future session's try.
- **Per §2a's finding**, `drs.nsdc.gov.ua` looks like a search-UI-only
  application with no bulk export ever captured by Wayback across 3 489
  historical captures — not proven (Wayback's own instability this
  session limited how thoroughly this could be checked), but the working
  hypothesis now, not an open unknown. If confirmed, this candidate may
  need to be registered against something more like rnbo.gov.ua's decree
  stream instead (each decree/decision individually, WARC-captured)
  rather than a single list locator — a materially different
  registration shape from every other sanctions
  candidate, and a founder question when it is reachable enough to answer.

## Sources

- [`sources/candidates/sanctions-authorities.yaml`](../../sources/candidates/sanctions-authorities.yaml) — `ua-nsdc-sanctions` entry
- [`sources/README.md`](../../sources/README.md) — A2's 2026-09-17 live-query record naming `sanctions-t.rnbo.gov.ua`
- [`docs/sources/verification-lil-articles.md`](verification-lil-articles.md) — the same Cloudflare-challenge block, independently confirmed on a different site
- [`docs/sources/verification-seco-sanctions.md`](verification-seco-sanctions.md) — precedent for "the real file lives on a different host than the publisher's main site"
