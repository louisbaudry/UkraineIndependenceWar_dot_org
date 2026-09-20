# Verification record — NSDC sanctions decisions (Ukraine)

**Status:** Verification record for one candidate registration —
**PARTIALLY BLOCKED**: the mechanism is identified, the actual sanctions
register is not reachable from this session. Nothing here is registered,
nothing is collected, and nothing is enacted by this document. Registering
this candidate is the founder's act (CLAUDE.md standing ruling).
**Verified:** 2026-09-20, ~19:00–19:10 UTC, from this session's container.
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
  unexplored; querying it *through* Wayback rather than fetching it live
  may be a workaround worth a future session's attempt, since Wayback
  itself was reachable in the 2026-09-17 session and A2's `census.py`
  already has a working `WaybackCdxClient`.
- If `drs.nsdc.gov.ua` turns out to only expose a search UI with no bulk
  export, this candidate may need to be registered against something more
  like rnbo.gov.ua's decree stream instead (each decree/decision
  individually, WARC-captured) rather than a single list locator — a
  materially different registration shape from every other sanctions
  candidate, and a founder question when it is reachable enough to answer.

## Sources

- [`sources/candidates/sanctions-authorities.yaml`](../../sources/candidates/sanctions-authorities.yaml) — `ua-nsdc-sanctions` entry
- [`sources/README.md`](../../sources/README.md) — A2's 2026-09-17 live-query record naming `sanctions-t.rnbo.gov.ua`
- [`docs/sources/verification-lil-articles.md`](verification-lil-articles.md) — the same Cloudflare-challenge block, independently confirmed on a different site
- [`docs/sources/verification-seco-sanctions.md`](verification-seco-sanctions.md) — precedent for "the real file lives on a different host than the publisher's main site"
