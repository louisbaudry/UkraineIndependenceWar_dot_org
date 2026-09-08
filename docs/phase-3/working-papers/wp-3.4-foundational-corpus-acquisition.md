# Phase III / Study 4 — Foundational Corpus Acquisition Strategy
## Working Paper 3.4

**Project:** Ukraine's Second War of Independence
**Status:** CANDIDATE — AI-drafted, awaiting founder review.
**Version:** 3.4
**Mandate:** The founder's stated intent (2026-09-08) to constitute the project's foundational data by "a sweeping crawling of the internet", over several months and several hundred dollars of model tokens — reconciled with the enacted collection policy, and sequenced under the founder's ruling of the same day (§1.3).
**Constraints inherited:** record §8, §9, §13, §25, §26, §28, §57; DR-0006 (WARC, WACZ evaluation), DR-0027 (grades triage-only), DR-0028 (declared dependence), DR-0066 (three gates), DR-0067 (source registry), DR-0068 (retention tiers), DR-0069 (quarantine), DR-0070 (coverage record), DR-0071 (interim constraints), DR-0072 / POL-0001 (personal data; §9 releases suspended pending §10 review), DR-0074 (capture series); LEGAL-009, OPS-001/006, PRES-007, AI-001/002.

### AI provenance (record §80)

Drafted 2026-09-08 by an AI assistant (Anthropic Claude Code agent session)
at the founder's direction. **Drafted without network access:** the drafting
environment's proxy denies general internet hosts, so no external service,
index, or tool named in this paper was reached or verified from here. Names
and capabilities of external archives and tools are drawn from prior
knowledge and must be confirmed before any of them is relied on (§9).
Model prices in §5 are list prices from a reference cached 2026-06-24 and
must be re-checked at execution. **Nothing in §7 is legal advice.**
Candidate until approved.

---

## 1. The intent, the options, and the ruling

### 1.1 What was asked

The founder asked for a sweeping acquisition of internet material to form
the project's foundational data, accepting a horizon of several months and a
token budget in the low hundreds of dollars.

### 1.2 What the enacted policy already says

Three commitments constrain the literal reading, and none of them is new:

1. **DR-0071(a)** binds collection to explicitly registered sources with
   human-configured scope: "No open-ended crawling, no bulk social-media
   harvesting." It binds until POL-0001 §10's external legal review is
   recorded (DR-0072, LEGAL-009 "partially satisfied").
2. **POL-0001 §9(a)** governs what lifts *after* that review: collection
   may extend to "systematic capture within registered source domains", but
   "open-ended crawling of the general web and untargeted social harvesting
   remain prohibited." An open-web crawl is therefore not merely deferred
   by the review; it is outside the policy the review tests.
3. **Record §9** rejects undifferentiated collection on its own terms: "Do
   not archive everything equally." Collection policy is source-specific;
   retention is tiered.

A fourth point is structural rather than legal. Under DR-0066 nothing
crosses Gate 2 without a human at the applicable tier. Bulk acquisition
therefore produces **holdings and review queues, never canonical
knowledge**. The collector suite asserts this: a completed run creates zero
assertions (collector/README.md). "Foundational data" in the sense of the
knowledge graph grows at the pace of editorial review, whatever the crawl
does.

### 1.3 The options put to the founder, and the ruling

Three framings were proposed on 2026-09-08:

| Option | Framing | Cost |
|---|---|---|
| A | Reframed plan within current policy: source census, retrospective recovery from existing web archives, registered live collection; legal review unlocks the sensitive half | The general web outside registered sources stays uncollected |
| B | Supersede DR-0071(a) and POL-0001 §9(a) to permit open-web crawling at `discard` / `metadata-only` tiers | Rests real legal exposure on a policy its own author marks as not legal advice; contradicts §9 |
| C | No scale-up before the POL-0001 §10 legal review is recorded | Evidence continues to disappear from the live web in the interval |

**The founder chose C.** This paper is therefore written as a plan whose
*execution beyond DR-0071's present limits is gated on the recorded legal
review*, and whose *preparatory work proceeds now* so that the interval is
not lost. The reframing of option A survives as the shape of what runs
after the gate: the ruling changed *when*, not *what*.

## 2. The reframing: harvest the crawls that already exist

The web relevant to this project has been captured continuously since
before 2014 by institutions whose purpose is exactly that, and largely in
WARC (ISO 28500), the format DR-0006 already chose:

- **Common Crawl** — monthly whole-web crawls since 2008, WARC on public
  object storage, with a per-crawl URL index queryable by domain.
- **The Internet Archive's Wayback Machine** — captures back to 1996, a CDX
  index API listing every capture of a URL prefix with timestamp and digest,
  and Memento-conformant access (WP 0.2 §4.5, DR-0018, DR-0023 already
  assume Memento semantics for capture series).
- Smaller subject-specific archives (conflict-documentation NGOs, OSINT
  collectives, national web archives of Ukraine and of EU member states)
  whose holdings should be enumerated in the census rather than assumed.

Three consequences follow:

1. **A live crawl can only capture today's web.** No effort in 2026 recovers
   a 2015 ministry page or a 2022 Telegram post from the live host.
   Retrospective recovery from external archives is the *only* route to the
   pre-2026 corpus, and it is the route record §9 already names: "a source's
   escalation may trigger retrospective recovery from external archives."
2. **The scarce input is judgment, not bandwidth.** The token budget buys
   two things well: assessing thousands of candidate sources into DR-0067
   registrations for the founder to accept or reject, and triaging hundreds
   of thousands of holdings into ordered Gate 2 queues (SPEC-0003 §7). It
   does not buy, and the plan does not need, model reading of the general web.
3. **The binding dollar cost is storage and backup**, not tokens. WARC for
   a few thousand domains over twelve years is plausibly hundreds of
   gigabytes to several terabytes; OPS-005 requires an independent backup of
   all of it. Figures are unverified (§5.3) and must be measured on the
   first registered domains before the storage plan is sized.

Acquisition-source provenance matters here (record §28, PRES-007): a holding
recovered from Common Crawl has the external archive as its *acquisition
source* and the original publisher as its *original publisher*. Both are
recorded; the project never implies it captured the page itself.

## 3. Where the work runs

**Not in agent sessions.** Interactive sessions cannot reach general hosts
from the build environment, and their per-page cost is far above a script
calling the API. The pipeline runs unattended on the project server that
`setup/install.sh` builds, driven by the source registry (OPS-001), calling
the model API programmatically from the enrichment stage (SPEC-0003 §6), and
recording every consequential call per AI-002. Sessions are for building and
reviewing the pipeline, not for being the crawler.

## 4. The plan: two tracks

### 4.1 Track A — permitted now under DR-0071

Everything below either collects from registered sources with configured
scope, or touches no network at all.

| Step | What | Verifies / produces |
|---|---|---|
| A1 | Register the seven sanctions authorities drafted in `sources/candidates/` (per source, as `sources/README.md` requires) and run the first live collection | The first live fetch ever made by `HttpFetcher` (collector/README.md); locator verification; the first DR-0070 coverage statement |
| A2 | Build the **census tooling** against *indices only*: enumerate candidate domains from the Common Crawl domain index, Wayback CDX prefixes for domains already known, citation graphs of the war articles in uk/ru/en Wikipedia dumps, sanctions-authority link graphs, published OSINT source lists, academic bibliographies. No live fetch of any unregistered host | A ranked list of candidate domains with the evidence for each; a queue of *prose* candidate notes for `docs/sources/` (that directory's stated purpose) |
| A3 | Build and test the **WARC bulk-ingest path** (CDR-P3-35) with fixture WARCs, so a WARC record becomes a quarantine item, then a holding, with acquisition-source and original-publisher recorded separately | Suite green with fixtures; verified to fail when provenance is dropped |
| A4 | Perform the **WACZ evaluation** DR-0006 made a standing task, from specifications and fixtures | A short evaluation note; a candidate DR on WACZ adoption or deferral |
| A5 | Draft the **registration-class** mechanism (CDR-P3-32) so that, when the gate lifts, the founder rules on classes with per-source exceptions rather than on thousands of entries one by one | `register.py` accepts a class template; tests refuse a class without a stated policy |
| A6 | Prepare the **legal-review brief** (§7), so the review is asked the questions this plan actually raises | A brief, not a policy; POL-0001 §10 remains the standard |
| A7 | Measure storage and bandwidth on the A1 sources and on one retrospective pull for a registered domain | Real numbers to size §5.3 |

### 4.2 Track B — gated on the recorded POL-0001 §10 review

Nothing in this track starts until DR-0072's successor records the review's
outcome and POL-0001 is revised to match it (§10). The waves are sequential
in risk, not strictly in time.

| Wave | Scope | Personal-data posture |
|---|---|---|
| B1 — Census assessment | For each candidate domain from A2, fetch a handful of pages (home, about, a sample) and draft a full DR-0067 registration: type, jurisdiction, languages, coverage start, rights guess with basis flagged unreviewed (§14), triage grade (DR-0027), declared dependence hypotheses (DR-0028). Founder accepts, amends, or rejects by class and exception | Discovery fetches are non-archival (CDR-P3-33); nothing is structured |
| B2 — Retrospective recovery, institutional | For registered official and institutional publishers: pull historical captures from Common Crawl and Wayback into quarantine and through Gate 1 as capture series (DR-0074); record every gap and every failed acquisition (DR-0070, PRES-007) | Minimal special-category data; DR-0071(b) holds regardless |
| B3 — Live daily collection | The registered set through the existing pipeline; browser-based WARC/WACZ capture for the high-value tier per DR-0006 and the A4 result | As registered |
| B4 — Media, NGOs, investigators | Registration and recovery as B1–B3, at the review tiers the material demands | POL-0001 §5 categories bite here; structuring is a Gate 2 act |
| B5 — Registered channels and accounts | Systematic capture *within registered source domains* only, as POL-0001 §9(a) permits: named channels and accounts, never untargeted harvesting; structural context captured at acquisition (DR-0023, §25) | Highest exposure; the review's terms govern |
| Throughout — Triage | Language detection, deduplication, document typing, relevance classification, dependence detection, producing *proposals* that order Gate 2 queues (SPEC-0003 §6–7). Non-model filters first; the model only on what survives | Never structures personal data (DR-0071(b), POL-0001 §4); every consequential call recorded per AI-002 |

### 4.3 What the plan does not do

- It does not crawl the general web, before or after the review.
- It does not accept, reject, or publish anything automatically. Gate 2 and
  Gate 3 stay human (DR-0066).
- It does not build a personnel index of any army or a population index of
  any territory (POL-0001 §5.4, §5.8).
- It does not treat queue depth as failure. Material that is permanently
  preserved and never reviewed is the expected majority outcome of bulk
  collection (Principle 5; collector/README.md), and queue depth and age are
  coverage metrics that ship with releases (SPEC-0003 §7, DR-0048).

## 5. Budget model

### 5.1 Token costs

Assumptions: Batch API at half list price; no credit taken for prompt
caching of the shared instructions, which would lower input cost further;
per-unit token counts are estimates to be replaced by measured `usage` on
the first hundred units. List prices as cached 2026-06-24, per million
tokens: Opus 5 $5 in / $25 out; Sonnet 5 $2 / $10; Haiku 4.5 $1 / $5.

| Task | Model | Tokens per unit (in / out) | Cost per unit | Units per $300 |
|---|---|---|---|---|
| Census assessment, one domain, ~5 pages | Opus 5 | 15,000 / 1,500 | ≈ $0.056 | ≈ 5,300 |
| Census assessment, one domain | Sonnet 5 | 15,000 / 1,500 | ≈ $0.023 | ≈ 13,000 |
| Triage, one holding | Haiku 4.5 | 4,000 / 300 | ≈ $0.0028 | ≈ 110,000 |
| Triage, one holding | Sonnet 5 | 4,000 / 300 | ≈ $0.0055 | ≈ 55,000 |

Reading: several hundred dollars funds a census of every plausible source
at the strongest model, plus triage of a first corpus in the low hundreds of
thousands of holdings at the smallest. It does not fund model reading of
millions of pages, and §2 explains why it need not.

Model choice is a per-task decision to be made by measurement on a sample
(census drafts are consequential and few; triage signals are disposable and
many), not by this table.

### 5.2 Which calls are preserved

AI-002 requires consequential outputs to carry provider, model, version,
instructions, inputs, output, pipeline version, schema, validation, reviewer,
and disposition. Census registration drafts are consequential: the founder
rules on them. Triage signals are routine and disposable under record §80's
explicit carve-out, provided the exemption is stated as a documented rule
(REQ-AI, AI-002 *Inspection*). CDR-P3-31 states it.

### 5.3 Non-token costs (unverified)

Storage volume, bandwidth, and backup dominate and are unknown until A7
measures them. The plan sizes storage after the first retrospective pull,
not before. Record §7's demand for independent backups (OPS-005) means every
stored terabyte is at least two.

## 6. The human bottleneck, stated plainly

Every registration is a founder decision (registering "is the act that
authorises collecting", `sources/README.md`). Every canonical assertion is a
Gate 2 decision at a risk tier (§78, DR-0063). A census that yields thousands
of candidates and a corpus of hundreds of thousands of holdings therefore
produces a **decision backlog measured in months of the founder's time**,
which is the actual horizon of "foundational data" here. Two mitigations are
in the plan and neither removes the bottleneck:

- registration by class with exceptions (CDR-P3-32) turns thousands of
  registrations into tens of class rulings plus the exceptions;
- triage ordering (SPEC-0003 §7) ensures the founder's hours go to the
  highest-value queue first.

The trusted-team expansion record §5 anticipates is the only real relief,
and it is outside this paper's scope.

## 7. Brief for the legal review (not legal advice)

POL-0001 §10 lists what the review must cover for personal data. This plan
raises further questions the record never mentions (the words *robots*,
*terms of service*, *copyright* do not appear in it), and the review should
be asked them so the answer can be recorded once:

1. **Preservation-only copying** of third-party web content into a
   non-public archive (§14 "may preserve" without "may display"), under the
   establishment jurisdiction's archiving and research exceptions, and the
   EU sui generis database right where lists and datasets are copied whole.
2. **Terms of use** of the external archives themselves (Common Crawl,
   Internet Archive) as acquisition sources, and whether bulk retrieval for
   archival purposes is within them.
3. **`robots.txt` and rate limits** as a matter of policy: whether the
   project follows the archival-crawler convention or the search-engine
   convention, and how a publisher's opt-out is recorded and honoured
   (CDR-P3-34 fixes the project's default; the review tests it).
4. **Platform terms** for B5: named-channel and named-account capture on
   Telegram and other platforms, distinguished from bulk harvesting.
5. Whether **discovery fetches** (B1) that are never preserved fall within
   the personal-data framework at all, and what record of them suffices.

## 8. Candidate Decision Records (proposals — require founder approval)

- **CDR-P3-31: Acquisition strategy.** The foundational corpus is
  constituted by (i) a source census producing DR-0067 registrations for
  founder decision, (ii) retrospective recovery of registered sources from
  existing web archives, and (iii) registered live collection — **never by
  open-web crawling**, before or after the POL-0001 §10 review. Track A
  (§4.1) may proceed now under DR-0071; Track B (§4.2) starts only when
  DR-0072's successor records the review. Triage signals are disposable model
  calls exempt from AI-002 preservation by this rule; census registration
  drafts are consequential and preserved in full.
- **CDR-P3-32: Registration classes.** `register.py` accepts a *class*
  template carrying every DR-0067 field group, which the founder approves
  once; individual sources register under it by inheritance, with per-source
  exceptions stated explicitly. A class without a complete policy is refused,
  as a single candidate is today. Registration remains the act that
  authorises collection (OPS-001); the class only changes its granularity.
- **CDR-P3-33: Discovery fetches.** A fetch made to assess a candidate
  source is a `discard`-tier acquisition under DR-0068: the attempt, outcome,
  locator, and digest are recorded; no bytes are retained; the record is not
  a holding and carries no §26 completeness claim. Discovery fetches of
  unregistered hosts are part of Track B.
- **CDR-P3-34: Collection etiquette.** Collectors identify themselves with a
  stable User-Agent naming the project and a contact address; honour
  `robots.txt` for live collection by default, with a per-source override
  that must state its rationale in the registry (rights and access defaults
  are already per-source, DR-0067); apply per-source rate limits as registry
  policy, not code; and record a publisher's opt-out request as a governed
  event with the same care as a data-subject request (POL-0001 §6).
- **CDR-P3-35: WARC bulk ingest.** A WARC record from an external archive
  enters quarantine like any fetch, with **acquisition source** (the archive)
  and **original publisher** recorded as distinct fields (§28). Successive
  captures of one URL form a capture series of separate holdings (DR-0074).
  The WARC record's own digest is carried into DR-0005 fixity. WARC files are
  ordinary content inside OCFL objects (resolving WP 3.3 §8 Q5 in the
  direction it anticipated).

## 9. Open questions raised

1. Whether every external archive named in §2 exists as described, offers
   what is claimed, and permits bulk retrieval — none was reached from the
   drafting environment.
2. Deduplication across acquisition sources: the same original bytes from
   Common Crawl and Wayback are one holding or two (SPEC-0003 §11 Q4).
3. The retention tier for retrospective captures of a registered source
   before item-level relevance is known: `permanent` by source default
   (§9 permits it), or `medium-term` with review.
4. Scheduler and queue technology (SPEC-0003 §11 Q1) — needed for B3, not
   before.
5. Whether the census assessment prompt and schema are themselves
   configuration items under DR-0048 (they influence what gets registered).
6. Trusted-team expansion (§6): out of scope here, but the plan's horizon
   depends on it.

## 10. Sources

- Record §5, §7–§9, §13, §14, §25, §26, §28, §37, §57, §78–§80, §104
  (Principles 5, 11, 14).
- DR-0006, DR-0018, DR-0023, DR-0027, DR-0028, DR-0048, DR-0055, DR-0063,
  DR-0066…0072, DR-0074; SPEC-0003; POL-0001; REQ-AI, REQ-LEGAL, REQ-OPS;
  `collector/README.md`; `sources/README.md`; `docs/sources/README.md`;
  WP 0.2 §4.5; WP 3.3 §8.
- External archives and formats: Common Crawl; Internet Archive Wayback
  Machine CDX API; Memento (RFC 7089); WARC (ISO 28500); WACZ (Webrecorder).
  **Not verified from the drafting environment** (see AI provenance).
- Model list prices: Anthropic price list as cached 2026-06-24; re-verify
  at execution.
