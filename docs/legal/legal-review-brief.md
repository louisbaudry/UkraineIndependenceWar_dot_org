# Legal review brief — POL-0001 §10 and WP 3.4 §7

**Status:** CANDIDATE — AI-drafted, awaiting founder review. Not legal
advice, and not itself a request for legal advice — this is the document
the founder hands to external counsel to make the review possible, not the
review itself.
**Version:** 0.1 | **Deposited:** 2026-09-14
**Origin:** WP 3.4 §7 (the brief was named as a deliverable, not written);
Track A item A6, put to the founder 2026-09-14 as one of three live options
and chosen.
**Fulfils:** POL-0001 §10 — "the review is asked the questions this plan
actually raises" (WP 3.4 §7's own framing).

> **AI provenance (record §80).** Drafted by an AI assistant (Anthropic
> Claude Code agent session) on 2026-09-14, from the questions WP 3.4 §7
> already raised, POL-0001, DR-0071, and the CDR-P3-3x candidates in WP 3.4.
> No new legal research was performed and no legal conclusion is drawn
> anywhere in this document — it organizes what the project already knows
> it needs answered, in the form a reviewer can act on, and flags what is
> not yet known well enough to send. The drafter is not a lawyer. Candidate
> until the founder approves it as ready to send.

## 1. What this document is for

POL-0001 §10 makes external legal review a **condition** of the policy's
operation at scale: until the review is recorded, §9's releases of the
DR-0071 interim constraints do not take effect, whatever POL-0001 itself
says (DR-0072). The review has not been commissioned. This brief exists so
that when it is commissioned, the reviewer is asked the project's actual
questions — not a generic "is this GDPR-compliant" — and so the founder can
see, before sending anything, what is ready to ask and what is not.

This is **not** the legal review. It answers no question in §3 below. It is
not sent to anyone by this record's deposit — commissioning the review, and
choosing who reviews it, remain the founder's acts, per DR-0071/POL-0001's
consistent pattern of leaving the review itself outside AI-drafted work.

## 2. What the reviewer needs to know about the project first

A reviewer with no prior context needs, at minimum:

- **What the project is** (record §1): a durable historical evidence and
  knowledge repository about Ukraine's Second War of Independence — an
  archive first, a public website only secondarily. Not a news
  organization, not a platform hosting user content, not primarily a
  research-publication venture, though it does all three at the margins.
- **What it collects**: official and institutional documents (sanctions
  designations, court and government records), open-source material about
  the war, and — the part §10 exists for — material that names or describes
  identifiable people who are not the project's staff: sanctioned persons,
  officials, combatants, victims, witnesses, minors, and civilians
  incidentally present in collected material.
- **The three-decision model it already applies** (POL-0001 §1): preserving
  material, structuring a person's data into queryable fields, and
  publishing are three independent decisions. The review's job is to test
  whether the *structuring* and *publishing* rules in POL-0001 §§4–5 hold up
  against real law, not to relitigate whether the project may preserve
  source material at all (Art. 89/Art. 17(3)(d) cover that, per §8.3).
- **The legal posture already chosen, subject to the review testing it**
  (POL-0001 §8.3): GDPR Art. 6(1)(f)/Art. 89 archiving-and-research as the
  **primary** basis, with Art. 9(2)(j) for special categories, Art. 85
  expression provisions invoked **secondarily**. The founder ruled this;
  the review does not choose between it and an alternative, it tests
  whether it survives contact with real law and real jurisdiction.
- **What is explicitly out of scope for this review**: publication editorial
  judgment (who gets named, when — that is DR-0063/§78 editorial process,
  not a legal question), the sanctions/export-control legal-finding layer
  (REQ-LEGAL, a different kind of "legal" — classification of designations,
  not data protection), and IP/copyright in collected documents themselves
  (a real question, listed at §3.2 below, but distinct from personal data).

## 3. The five questions, expanded for a reviewer

These are WP 3.4 §7's five questions, each expanded with the specific
project facts and documents a reviewer needs to answer it, not a restated
legal issue-spot.

### 3.1 Preservation-only copying of third-party web content

**The question:** Does copying third-party web material into a **non-public
archive** (POL-0001 §14 "may preserve" without "may display") fall within
the establishment jurisdiction's archiving/research exceptions and text-
and-data-mining or research carve-outs, and does the **EU sui generis
database right** (Directive 96/9/EC Art. 7) attach where an entire list or
dataset (a sanctions list, a court docket) is copied whole — and if so,
what extraction/re-utilization defense applies to an archival copy that is
never redistributed in bulk?

**What bears on it:**
- POL-0001 §8.3's Art. 89/Art. 17(3)(d) posture (already chosen; the
  review tests it, per §2 above).
- DR-0093's actual practice: two sanctions lists (EU consolidated list,
  OFAC SDN) already copied in full and held in a non-public archive, zero
  documentary assertions drawn from them yet (Gate 2/3 untouched).
- The distinction the project draws between **acquisition source** and
  **original publisher** (record §28, CDR-P3-35): an archival copy always
  records where it came from and who made it, never claims to *be* the
  original.

### 3.2 Terms of use of the external archives used as acquisition sources

**The question:** Do Common Crawl's and the Internet Archive's own terms of
use, and any technical access agreement either service requires, permit
**bulk retrieval for archival purposes** by a third party such as this
project — as opposed to the ad hoc, individual-page access their public
interfaces are built for?

**What bears on it:**
- WP 3.4 Track A2/A3: the project's planned use is (i) querying each
  service's own index API for candidate-domain discovery, never fetching
  the candidate host itself (`sources/census.py`, CDR-P3-33 — a
  `discard`-tier act, no bytes retained), and (ii) bulk retrieval of
  **specific, already-identified** WARC records for registered sources
  (CDR-P3-35), not a general crawl of either archive.
- This question is closer to a **contract-terms** question than a
  copyright one — it should be checked against each service's current
  published terms, not assumed from general archival practice.

### 3.3 `robots.txt` and rate limits as policy, not just etiquette

**The question:** Beyond the technical convention CDR-P3-34 already commits
to (honour `robots.txt` by default for live collection, per-source override
with a stated rationale in the registry, per-source rate limits as registry
policy), does the establishment jurisdiction attach **legal** consequence
to a robots.txt override or a documented rate-limit decision — e.g., as
evidence of good or bad faith in a computer-misuse or contract claim, or
under any implemented Computer Fraud and Abuse Act-equivalent — and does
the archival-crawler convention (follow robots.txt; identify the collector)
versus the search-engine convention carry different legal weight?

**What bears on it:**
- CDR-P3-34's full text (WP 3.4 §8): stable identifying User-Agent and
  contact address, `robots.txt` honoured by default, per-source override
  with a **registered rationale** (not a code-level bypass), publisher
  opt-out treated with the same care as a data-subject request
  (POL-0001 §6).
- This is the one §7 question the project has **already fixed a default
  for** (CDR-P3-34); the review is asked to test that default, not propose
  one from nothing.

### 3.4 Platform terms for named-channel/named-account capture

**The question:** For **Telegram and other platforms** named in WP 3.4 B5
(systematic capture within a *registered* channel or account, never
untargeted harvesting), do the platform's own terms of service and any API
terms permit archival capture of a named, publicly-posted channel's
content, and does capturing a channel differ, in the platform's terms or in
law, from capturing an individual post a user links to?

**What bears on it:**
- POL-0001 §9(a)'s post-review scope: "systematic capture within registered
  source *domains*... open-ended crawling of the general web and
  untargeted social harvesting remain prohibited" — B5 is scoped to this
  already, before the review, as a matter of what the project intends to
  ask permission for.
- No platform-specific terms review has been performed by this project for
  any platform; this question is entirely unanswered as of this brief.

### 3.5 Discovery fetches and the personal-data framework

**The question:** Do **discovery fetches** — CDR-P3-33's `discard`-tier
acts, made only to assess whether a candidate source is worth registering,
with no bytes retained and no holding created — fall within the
personal-data framework (GDPR processing) **at all**, given nothing is
stored past the assessment, and if they do, what record of the fetch
(locator, outcome, digest of nothing retained) suffices to demonstrate
compliance without itself becoming a new category of retained personal
data?

**What bears on it:**
- CDR-P3-33's exact terms (WP 3.4 §8, quoted at §3.5 above) — a discovery
  fetch is explicitly designed to create no holding and carry no §26
  completeness claim.
- This is the narrowest of the five questions technically, and possibly the
  easiest for a reviewer to answer quickly, since the project's own design
  already minimizes what exists to be regulated.

## 4. What blocks commissioning the review today

1. **The establishment jurisdiction is not yet named anywhere in this
   project's documents.** POL-0001 §10 and this brief both say "the
   establishment jurisdiction" as if it were settled; a search of every
   controlled document as of this brief's drafting finds no country, no
   legal-entity name, and no stated place of establishment. **This is the
   single blocking gap** — a reviewer cannot be engaged, and the questions
   above cannot be answered, without knowing which jurisdiction's law and
   which country's counsel apply. This is a founder decision (a real-world
   organizational fact, not a research question this session can resolve),
   and it should be the first thing settled, ahead of sending this brief
   anywhere.
2. **No named reviewer or firm has been identified.** A brief this precise
   travels well to specialist data-protection or media-law counsel; a
   generalist may need more framing than §2 above provides.
3. **Platform terms of service (§3.4) have not been read by anyone on this
   project for any named platform.** A reviewer will likely ask for this as
   an input rather than research it themselves; someone should read
   Telegram's (and any other named platform's) current terms before the
   review, so the reviewer is testing a stated position, matching how §3.3
   was prepared for CDR-P3-34.

## 5. Documents to hand the reviewer

- [`POL-0001` — Personal Data Policy](../policies/POL-0001-personal-data.md)
  (the policy under test, all twelve sections)
- [`DR-0072`](../decision-records/DR-0072-personal-data-policy-adoption.md)
  — its adoption, including the §10 operative limit
- [`DR-0071`](../decision-records/DR-0071-interim-personal-data-constraints.md)
  — the interim constraints §9 releases
- [`DR-0067`](../decision-records/DR-0067-source-registry-schema.md) —
  the source registry, for how rights/jurisdiction/scope are recorded
  per source
- [`WP 3.4`](../phase-3/working-papers/wp-3.4-foundational-corpus-acquisition.md)
  §§4, 7–8 — the acquisition plan and the CDR-P3-3x candidates (31, 33, 34,
  35) this brief draws on
- This brief itself, as the organizing document

## 6. Open questions raised

1. **What is the project's establishment jurisdiction?** Blocks
   commissioning the review entirely (§4.1). Needs a founder answer before
   any further legal-review work is useful.
2. **Who reviews it** — a named firm or individual, and in what
   jurisdiction once §4.1 is answered.
3. **Should platform terms of service (§3.4) be read and summarized by a
   future session before the review is sent**, the way CDR-P3-34 was
   already prepared for §3.3? Recommended, but not this brief's job to do
   without being asked, since it means fetching and reading each named
   platform's current terms — a bounded, concrete task for whenever the
   founder wants it done.

## 7. Candidate Decision Records arising

None. This brief proposes no new project rule and changes no existing one
— it organizes questions POL-0001 §10 and WP 3.4 §7 already posed. Nothing
here is enacted by this document's deposit.

## 8. Sources

- Record §1, §13, §78–§80
- POL-0001 (all sections, especially §8.3, §9, §10)
- DR-0071, DR-0072, DR-0067
- WP 3.4 §§4, 7, 8 (CDR-P3-31, 33, 34, 35)
- REQ-SEC (SEC-001, for the confidential-identity boundary POL-0001 §5.6
  and §9(c) depend on, referenced but not itself a §10 question)
