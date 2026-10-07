# Phase III / Study 11 — Reaching Telegram Without a Single Point of Failure: Egress Options
## Working Paper 3.11

**Project:** Ukraine's Second War of Independence
**Status:** CANDIDATE — AI-drafted, awaiting founder review.
**Version:** 3.11 (draft 0.1)
**Mandate:** A founder question of 2026-10-07: whether a bought service could remove the single-IP risk that `docs/infrastructure.md` §2.5 and §4 item 7 and `docs/runbooks/telegram-channel-backfill.md` record for Telegram collection, and what such a service would have to be and do to be compatible with this archive's rules. Evaluation and requirements only; nothing is bought, registered or built by this paper.
**Constraints inherited:** DR-0071(a) (registered sources only; no open-web crawling); DR-0072 and the 2026-09-08 standing ruling (no collection scale-up before the POL-0001 §10 review is recorded); DR-0066 (collection creates no canonical knowledge); DR-0067 (capture format honoured; politeness is per-source policy and belongs to the caller); DR-0093 §3 (a person is the agent of record for a run); DR-0094 and record §28 (acquisition source is not the original publisher); DR-0106 and DR-0107 (the two Telegram sources and their backfills); DR-0100 and POL-0001 (France, the founder as controller, IONOS in Spain as the one processor); CLAUDE.md "Code conventions" (Python standard library plus `psycopg` and `PyYAML`; a new runtime dependency is the founder's decision) and "This repository is public".

### AI provenance (record §80)

Drafted 2026-10-07 by an AI assistant (Anthropic Claude Code agent session) at the founder's direction. **What was checked:** the repository's own text — `collector/telegram_backfill.py`, `collector/fetch.py` (the `Fetcher` protocol and `HttpFetcher`), `docs/runbooks/telegram-channel-backfill.md`, `docs/infrastructure.md`, DR-0106's *Executed* section, DR-0107, `docs/sources/verification-strike-tracking-first-two.md`, `docs/legal/legal-review-brief.md` and DR-0100 on IONOS. **What was not checked:** no provider was looked at, priced, tested or named; no Telegram terms of service, rate-limit documentation or blocking behaviour was retrieved; no network request was made. Every statement below about how a proxy or a fetch service behaves (what it can see, whether it can alter bytes, how Telegram treats a given kind of address) is the drafter's **background technical knowledge, unverified in this session**, and is marked so where it carries weight. Nothing here is legal advice. Candidate until the founder rules; **design only — no code, registration, purchase or schema change follows from this paper** (§9).

---

## 1. What the repository already says, and one fact that changes the urgency

**The risk as recorded.** Every Telegram fetch is a plain HTTPS GET of `t.me/s/<channel>`, Telegram's public preview, from the archive server's single address, with no account (runbook, "Read this before running anything"). If Telegram rate-limits or blocks that address, all Telegram collection stops, and the runbook adds that the same address serves every other source (`docs/infrastructure.md` §2.5, §4 item 7).

**What has actually happened.** The recorded evidence is that the risk has not materialised:

- `kpszsu`'s full historical backfill ran 3,960 page attempts from 2026-09-22, 3,959 preserved, **0 failures**, and bottomed out at post id 1 (DR-0106 *Executed*). `generalstaffzsu` also reached post id 1. DR-0107 records **no rate-limit signals** across the bounded passes that preceded the full run. I did not re-read the per-pass counts for `generalstaffzsu`.
- The largest exposure in this subject — thousands of sequential requests — is therefore **already spent**, on both registered channels.
- What remains is ongoing collection, which the registered locators make a handful of requests per run. I did **not** measure that volume; `storage/measure.py` (A7) can.
- Collection is manual (`docs/infrastructure.md` §3.1), so a run happens when a person starts it and can stop when something looks wrong.

**What can still make the risk real.** Another multi-thousand-page backfill (DR-0109's civilian-harm work may register further Telegram channels; `sources/candidates/civilian-harm.yaml` mentions Telegram once, which I did not read in detail); a scheduled, unattended collection (OPS-001); or Telegram simply changing its behaviour toward the server's address. None is decided or observed today.

**Consequence for this paper.** The founder asked about the egress option, so it is designed in full below. But the honest reading of §1 is that **buying now would insure against a risk that the record shows did not occur during its worst case**, so §8 puts the buy-now-or-on-a-trigger question to the founder as its own candidate rather than assuming it.

## 2. Terms, in plain words

- **Egress.** The address the server's outgoing requests appear to come from, as seen by the site that receives them. Telegram sees the archive server's address today.
- **Provider.** The company that would sell an egress service. The paper says "provider" throughout; the word "vendor" means the same.
- **Tunnel (forward) proxy.** A service you point your own program at. The program asks it to open a connection to `t.me` and then talks to Telegram *through* it. For an HTTPS site the connection is encrypted from the program to Telegram, so the provider carries the bytes without reading them. *(Background knowledge, unverified against any provider.)*
- **Fetch-on-your-behalf API.** A service you send a URL to; its servers fetch the page and send you the result. The provider sees the full URL and the full content, and what it returns is what *it* says it fetched.

## 3. Five ways to reach Telegram, compared

| | What the provider sees | What the archive receives | New dependency | Fits the archive's rules? |
|---|---|---|---|---|
| **A. Tunnel proxy** (egress only) | The destination host (`t.me`) and the traffic volume; not the channel, the page or the content *(unverified, general HTTPS behaviour)* | The same bytes Telegram sent, unaltered, with end-to-end TLS verification kept on | None in code (`urllib.request.ProxyHandler` is standard library); a subscription | **Yes**, if §4's requirements hold |
| **B. Fetch-on-your-behalf API** | The full URL (so the channel) and the full content | What the provider says it fetched; the provider can change, trim or re-render it, and may return rendered rather than raw HTML | A provider-specific client or HTTP convention | **Not as it stands.** The preserved original would be the provider's copy, so record §28 and DR-0094 would apply, and a "raw bytes as served" claim could not be made |
| **C. Telegram data API** (a commercial or account-based interface returning parsed posts) | The channel and the query | Parsed records, not the page | An account, which the runbook says exists nowhere in this project, plus a client | **No.** It changes what the source is (a registered `t.me/s/` page) and what is preserved (not the page) |
| **D. A second address of our own** (a small separate server used only for Telegram) | Nothing new; Telegram sees the second address | Same bytes as today | A second machine to host and keep in the record | **Yes.** Separates the failure domains cheaply; still one address per failure domain |
| **E. Nothing now; act on a trigger** | n/a | Same as today | None | **Yes.** The current position |

Options B and C are listed for completeness and are not recommended in any case. B fails the archive's central property (the preserved bytes are what the origin served); C fails the registered-source and no-account rules.

## 4. Requirements any egress service must meet

If the founder rules that an egress service may be used (§8), these are the conditions. Each is one a test or the registration record can check.

1. **Tunnel, not fetch-on-your-behalf.** The archive's own client performs the TLS handshake with `t.me` and verifies its certificate. A provider that terminates TLS, re-renders pages or requires the archive to install its certificate is refused.
2. **Raw bytes unchanged.** The preserved page is what Telegram sent. This is DR-0067's capture-format rule and the archive's reason to exist; it is checked by comparing a page fetched through the service with one fetched directly (§5).
3. **Registered sources only.** The service changes the route of a request, never what may be requested. DR-0071(a) holds: an unregistered locator is out of policy whatever its egress.
4. **No circumvention of an access control.** The service must not be used to pass a CAPTCHA, a Cloudflare challenge or a login, or to disguise the requester's identity from a site that has refused it. The challenge on `ua-nsdc-sanctions` stays a human-assisted-browser matter (`docs/infrastructure.md` §2.4). The service is for avoiding a *rate* concentration on one address, not for defeating a *refusal*. A page the origin refuses is recorded as a refusal (§28), not retried through another route.
5. **Address provenance is checked before purchase.** Some providers sell addresses belonging to private households whose owners may not have meaningfully agreed. Whether a given provider's addresses are datacentre, or residential and consented, is a fact to verify, not assume, and a provider that cannot say is refused. *(General caution, unverified for any provider.)*
6. **No secret in the repository.** The provider's host, account and credentials are configured on the server from the environment and never committed (`CLAUDE.md` "This repository is public"). The repository may say that an egress is configured and by what *class* of service; it never says where or as whom.
7. **The route is recorded, so a later reader can tell.** Each run's `configuration` (already a free-form record, `telegram_backfill.py`) states that the request went through an egress service, by neutral label, so the acquisition record never implies a direct fetch (§28).
8. **Politeness stays the caller's.** `--delay`, `--max-pages` and the one-channel-at-a-time rule of the runbook still apply. A bought address pool is not a licence to raise the request rate.

## 5. How it would fit the code — and what would be built, only after a ruling

`collector/fetch.py` is deliberately the one part that touches the network, behind the `Fetcher` protocol. `telegram_backfill.py` already receives a fetcher, so nothing downstream (quarantine, gates, OCFL storage, coverage accounting) would change.

- **Option A needs one constructor change:** an optional proxy setting on `HttpFetcher`, read from the environment, built with `urllib.request.ProxyHandler`. **No new runtime dependency**, so the standard-library rule is not engaged by the code, only by the subscription.
- **Default stays direct.** With no setting, behaviour is byte-for-byte what it is today.
- **Tests** (to be written when, and only when, a candidate below is ruled): a local proxy double serving a fixture page, asserting that the bytes recorded through it equal the bytes served (requirement 2) and that the run's `configuration` names the egress (7); a refusal test for a proxy that presents a different certificate (1); and the usual **sabotage** step — remove the route label and watch the test fail — recorded in `collector/README.md`.
- **What could not be tested here:** any live provider, as no network request was made and none is chosen. `HttpFetcher` itself has never had a live proxy path exercised.

## 6. Legal and policy points, flagged and not answered

1. **DR-0072 is untouched.** An egress service changes how a request travels, not what is collected or how much is authorised. It lifts nothing in §9 of POL-0001 and must not be cited as if it did.
2. **Is a provider a processor?** For a tunnel (A), the provider carries encrypted traffic and, on the drafter's understanding, does not read the page; it does learn the archive server's address, when it connects and how much it moves. For a fetch service (B), it does handle the content. Whether a tunnel provider is a processor of personal data under GDPR Art. 28, and what the project's records must then show, is a **question for counsel**, adjacent to the Art. 28 check already outstanding for IONOS (`docs/legal/legal-review-brief.md` Q12(b); `docs/infrastructure.md` §4 item 2). This paper does not answer it; if a service is chosen, the question joins the brief's open items.
3. **The server's address is project data.** Nothing here may put the server's address, or a provider's host or account, in the repository, an issue or a PR.
4. **Telegram's own terms** were not retrieved. Whether routing public-preview requests through an intermediary address is compatible with them is unverified; the archive's existing position (public pages, no account, polite pace, registered channels only) does not change.

## 7. Cost, and what was not measured

No provider was priced, so **no cost figure exists** in this paper. What would be needed to estimate one: the ongoing request count per run (A7's `storage/measure.py` against the real database; not run), and, for any future backfill, the page count (the runbook's own 2,500–4,000 estimate for `kpszsu` proved loose, per DR-0106). Option D's cost is a small server plus the work of keeping it in `docs/infrastructure.md`.

## 8. Candidate Decision Records

Each is put to the founder separately. Drafted as `CDR-pending-<slug>` and **numbered at merge** (DR-0102): `origin/main`'s highest was CDR-P3-57, so these are CDR-P3-58…60, in the order listed.

### CDR-P3-58
**Recommended:** adopt §4's eight requirements as the conditions under which any egress service may carry registered-source requests, tunnel-type only, with raw bytes unchanged, no circumvention of a refusal, address provenance checked, no secret committed, and the route recorded in the run's configuration. The record authorises no purchase and no code. *Alternatives:* decide the requirements per provider at the time of purchase (B); forbid egress services altogether and rely on options D or E (C).

### CDR-P3-59
**Recommended:** **do not buy now; buy on a named trigger** — any recorded rate-limit or block signal from `t.me` in a run; a decision to run another backfill of more than a few hundred pages; or a decision to schedule Telegram collection unattended. Until a trigger, the current position (option E) stands, and `docs/infrastructure.md` §4 item 7 keeps the risk recorded. On a trigger, the first step is a proportionate one (option D, or A under CDR-P3-58), chosen by the founder with the evidence then in hand. Rationale: §1 — the worst case already ran with no signal. *Alternatives:* buy now as insurance (B), accepting a recurring cost for a risk not observed; never, and rely on the founder's judgement at the time (C).

### CDR-P3-60
**Recommended:** if an egress service is ever used, it is for **Telegram channel collection only**. Every other registered source is an official publisher fetched from its own host at a low rate, and nothing in the record shows a rate problem for them; the only blocked source (`ua-nsdc-sanctions`) is blocked by a challenge, which requirement 4 puts out of an egress service's reach. *Alternatives:* route all collection through it (B); decide per source (C).

## 9. Open questions raised

1. **Timing** (CDR-P3-59) is the question that decides whether the rest of this paper is acted on soon or held.
2. **Which provider, if any,** is untouched: no shortlist exists. If CDR-P3-59 fires, a shortlist is a separate piece of work that retrieves each candidate's terms, address provenance and TLS behaviour; none of it was done here.
3. **Counsel's view on a tunnel provider** (§6.2) — whether it is a processor, and what the records must show — joins the Art. 28 items already outstanding.
4. **Ongoing request volume** has never been measured; `storage/measure.py` against the real database would turn "a handful" into a number and sharpen §7.
5. **Further Telegram channels.** If DR-0109's civilian-harm sources register Telegram channels, each registration's backfill size is a trigger under CDR-P3-59; that is a question for those registrations, not for this paper.
6. **The 3,960-page record for `generalstaffzsu`** was not re-read; the "0 failures" statement in §1 is verified for `kpszsu` from DR-0106 and taken from DR-0107's text for the bounded passes of both.

## 10. Sources

All internal: `collector/telegram_backfill.py`; `collector/fetch.py`; `docs/runbooks/telegram-channel-backfill.md`; `docs/infrastructure.md` §2.4, §2.5, §3.1, §4; DR-0067; DR-0071; DR-0072; DR-0093; DR-0094; DR-0100; DR-0102; DR-0106 *Executed*; DR-0107; DR-0109; POL-0001 §9; `docs/legal/legal-review-brief.md` Q12; `docs/sources/verification-strike-tracking-first-two.md`; `CLAUDE.md` "Code conventions" and "This repository is public". **No external source was retrieved.**
