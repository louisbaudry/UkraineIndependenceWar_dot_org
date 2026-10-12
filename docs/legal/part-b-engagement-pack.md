# Part B engagement pack — for IP / media counsel

**Status:** DRAFT v0.1 — AI-drafted, awaiting founder review. Not a
controlled document under [DR-0046](../decision-records/DR-0046-unified-document-control.md);
it enacts nothing, changes no policy, and is **not legal advice**. It is the
sendable form of Part B (Q7–Q12) of the [legal-review brief](legal-review-brief.md),
for the engagement the founder ruled on 2026-10-12 to commission **in
parallel with** Part A rather than after it (issue #42).
**Founder's acts, not a session's:** choosing the counsel, sending this,
agreeing the terms and fees. Nothing here has been sent.
**Standard it serves:** it answers [WP 3.4](../phase-3/working-papers/wp-3.4-foundational-corpus-acquisition.md)
§7 and gates the acquisition steps behind Q8, Q9 and Q10. Under
[DR-0101](../decision-records/DR-0101-recording-the-legal-review.md), Part B's
answers supersede nothing and move neither DR-0072 nor LEGAL-009; they still
decide whether those acquisition steps are authorised, **whatever Part A
concludes**.

### AI provenance (record §80)

Drafted 2026-10-12 by an AI assistant (Anthropic Claude Code agent session) at
the founder's direction. It restates Part B of brief v0.4 and **refreshes the
facts**: that brief was written on 2026-09-15, when two sources had been
collected. The register-derived facts in §3 below were read from the
repository on 2026-10-12 (`sources/candidates/*.yaml` with registration-class
defaults merged, the decision records named, `collector/` code). **Not
verified:** anything against the archive server's live database, which the
drafting session cannot reach; whether the two registrations approved since
(DR-0114, DR-0115) were executed; any external terms of use, statute or case
law. The drafter is not a lawyer. Where this pack says a position "appears" to
fit or not fit, that is a question put to counsel, never a conclusion.

**Handling.** This file is in a public repository. It carries no counsel
name, no fee, no postal address and no founder identity; those go in the
covering letter and the engagement terms. It quotes no row of collected
material and no personal data.

---

## 0. Covering letter — template for the founder

*(Edit, complete and send outside the repository. Square brackets are
placeholders the founder fills.)*

> [Counsel's name and firm]
>
> I am the founder and sole operator of an independent historical archive
> documenting Russia's war against Ukraine, established in France and hosted
> on a server in Spain. I am the data controller as a natural person; I intend
> to form an association loi 1901, which has been started but does not yet
> legally exist.
>
> I am asking for advice on six questions of **intellectual-property,
> contract and platform-terms law** that must be answered before the project
> collects at scale. They are set out in the enclosed pack, with the facts
> counsel needs. A separate engagement with French data-protection counsel
> covers the personal-data questions; their questions are not yours, and I am
> not asking you to answer them.
>
> I need a written note structured against the six questions (§5 and §7 of the
> pack), delivered by [date]. Please send your terms, your estimate and your
> conflict check before starting. [Anything else: privilege, confidentiality,
> payment.]
>
> [Name, contact details]

---

## 1. What the project is, in one page

*(Counsel will not have the repository. §1 and §3 are meant to be sufficient
on their own.)*

The project is a **durable historical evidence and knowledge repository**
documenting Ukraine's Second War of Independence and the machinery sustaining
Russia's war against it, including sanctions evasion. It is independent and
non-Ukrainian, with a horizon measured in decades. It describes itself as an
archive first and a website last.

**Who and where.** Established in **France**; the controller is the
founder/principal editor **as a natural person** (no legal entity yet;
incorporation is under way); the archive server is hosted by **IONOS in
Spain**. Recorded in the project's
[DR-0100](../decision-records/DR-0100-jurisdiction-controller-and-hosting.md).

**Three independent decisions.** Material passes three gates, and a "yes" at
one never implies a "yes" at the next: **Gate 1 preserve** (keep the bytes;
automated check; registered sources only), **Gate 2 structure** (a human
promotes a person or fact into queryable fields), **Gate 3 publish** (a human
decides what appears on a public surface, at which access tier). For your
questions the important one is that **preserving is not publishing**: the
project's rights vocabulary separates *may preserve*, *may display*, *may
redistribute* and so on, per source.

**Collection creates no knowledge.** No automated process asserts anything; a
collection run produces preserved files and zero assertions of fact.

**Nothing is published.** No public surface carrying collected material
exists. Material is held in an append-only archive (OCFL objects) with
declared access tiers; removal is possible only through a governed redaction
that leaves a tombstone.

**No open-web crawling, ever.** Excluded by the project's own policy as a
matter of archival method. A run fetches **exactly the locators listed for a
registered source** and nothing else; the collector follows no links. The
project is not asking whether it may crawl.

---

## 2. Positions the project has taken that bear on Part B

For counsel to test, not to choose.

| # | Position | Where it comes from |
|---|---|---|
| P6 | Content recovered from a third-party web archive carries the **original publisher's** rights position, not the archive's; the archive is recorded as the acquisition channel and is never itself registered as a source | [DR-0094](../decision-records/DR-0094-third-party-web-captures.md) §1 |
| P7 | A source's rights position is **recorded per source**, in the registry, as one of *unknown / may-preserve / may-display / may-provide-to-subscribers / may-redistribute*; a conservative default (*may-preserve*) applies until the position is checked | [DR-0067](../decision-records/DR-0067-source-registry-schema.md) |
| P8 | Registering a source is the act that authorises collecting from it; there is no general collection authority | OPS-001; [DR-0071](../decision-records/DR-0071-interim-personal-data-constraints.md)(a) |

P6 is a premise adopted for archival-provenance reasons and never legally
verified.

---

## 3. The facts, as of 2026-10-12

Brief v0.4 (2026-09-15) described **two** collected sources and said platform
capture was a later step. Both statements are out of date, and Q10 changes
accordingly.

### 3.1 Collection to date

| Fact | Value (from the repository; not checked against the live database) |
|---|---|
| Sources registered and collected | **10**: six sanctions and export-control publishers, two Ukrainian official Telegram channels, a UN human-rights monitoring publication, and a Ukrainian Prosecutor General statistics series |
| First collection | 2026-09-09; the sanctions lists were registered and collected between 2026-09-08 and 2026-09-21 |
| Approved for registration, execution not recorded | **2** more: a front-line map snapshot service and a regional Ukrainian administration's Telegram channel (DR-0114, DR-0115) |
| Held, not refused | **1**: a US think-tank's daily map product, pending the publisher's **written permission**, which its policy requires (see §3.4) |
| Assertions of fact created from any of it | **zero** |
| Personal data promoted into structured, queryable fields | **none** |
| Material published on any public surface | **none** |

### 3.2 The rights positions recorded for those ten sources (Q7)

Every registration records a rights position and the basis for it. Verbatim
or close to it, with sources identified by publisher and not by registry key:

| Source (publisher) | Recorded permission | Recorded basis |
|---|---|---|
| EU Consolidated Financial Sanctions List (European Commission) | may-redistribute | Commission Decision 2011/833/EU, subject to acknowledgement. **"NOT LEGALLY REVIEWED"** |
| EU restrictive-measures instruments (EUR-Lex, Publications Office) | may-redistribute | Same basis. **"NOT LEGALLY REVIEWED"** |
| OFAC SDN and Consolidated lists (US Treasury) | may-redistribute | "US federal government work, not subject to domestic copyright". **"NOT LEGALLY REVIEWED"** |
| BIS Denied Persons List (US Commerce) | may-redistribute | "US federal government work". **"NOT LEGALLY REVIEWED"** |
| OFSI Consolidated List (UK) | may-redistribute | Open Government Licence v3.0, subject to attribution. **"NOT LEGALLY REVIEWED"** |
| SECO sanctions list (Switzerland) | may-preserve | Rights position **unverified**; conservative default applied |
| Ukraine Air Force Telegram channel | may-preserve | **Unverified**: official government channel, but no explicit reuse licence found |
| Ukraine General Staff Telegram channel | may-preserve | **Unverified**: same |
| UN Human Rights Monitoring Mission in Ukraine (monthly update) | may-preserve | **"UNVERIFIED — NOT LEGALLY REVIEWED"**. The site carries only a copyright line; the UN's general terms permit personal, non-commercial download and copying "without any right to resell or redistribute them or to compile or create derivative works therefrom"; whether those or OHCHR's own terms govern is open |
| Ukraine Prosecutor General (monthly crime statistics) | may-preserve | **"UNVERIFIED — NOT LEGALLY REVIEWED"**. Ukrainian copyright law Art. 8(1)(3) excludes "official documents of a political, legislative, administrative and judicial nature"; Art. 8(1)(6) names non-original databases as subject to a sui generis right |

None of the five **may-redistribute** positions has been reviewed by a lawyer.
Nothing is redistributed, because nothing is published.

### 3.3 Platform capture is no longer prospective (Q10)

Two official Ukrainian government Telegram channels are registered sources
and have been **fully backfilled** (to post id 1) since 2026-09-22/24. Facts:

- Method: a plain HTTPS GET of Telegram's public web preview (`t.me/s/<channel>`);
  **no account, no login, no API**; the page needs no authentication.
- Volume: for the larger channel about 3,960 page requests in five passes, 0
  failures and no rate-limit signal recorded; a default of 3 seconds between
  pages.
- Source address: **one** address, the archive server's.
- Capture format: WARC, preserved, not parsed, not published.
- One further channel (a regional administration's) is approved, not yet run.

So the question is no longer whether the project may begin this, but whether
it may **continue and extend** it, and what follows from what it has already
done.

### 3.4 One concrete test case for Q7 and Q9

The US think-tank's daily map product is held because its Fair Use and
Attribution Policy (revised 2026-01-08) requires **prior written permission**
for "incorporation of ISW Materials into other datasets ... or systems" and
bars redistribution "in bulk, via API, or through automated means". It does
not mention archiving. A permission request is drafted and **has not been
sent**. This is a real instance of the Q7(a) question (preservation-only
copying) and the Q9 question (an explicit publisher restriction).

### 3.5 What the collector actually does about politeness (Q9)

The collector sends a fixed User-Agent naming the project and its public
repository URL. It fetches only registered locators. **It does not read or
evaluate `robots.txt`**; the project has not yet adopted the rule Q9 describes,
and wants advice before it does. Rate limits are an operator-set delay
(Telegram: 3 seconds), not registry policy yet.

### 3.6 The two states counsel is asked to answer for

**State 1 — as it is (2026-10-12):** the ten sources above; nothing structured,
nothing published; no public surface; one operator.

**State 2 — as intended:** a census-derived set of registered sources collected
on a recurring cadence; retrospective recovery of those sources' past pages
from Common Crawl and the Internet Archive; more named platform channels;
structuring at volume by human editors; publication at declared tiers
including a public one; plausibly an incorporated entity and a small team.

---

## 4. Part B — the six questions

*(Restated from brief v0.4 §6, with §3's facts folded in. Q-numbers are kept
so answers cite the same questions as the brief.)*

### Q7 — Preservation-only copying, and the database right

(a) Under French copyright law's archiving, research and related exceptions,
may the project copy third-party web content wholesale into a **non-public**
archive, with no public display? The project knows France operates a statutory
web-legal-deposit regime through designated institutions; it does **not**
claim to be one, and asks only whether that regime's existence bears on what a
private archive may do.

(b) The sanctions lists are copied **whole**, as datasets. Does the **sui
generis database right as implemented in French law** restrict that, and does
any exception cover it? §3.2 shows the five *may-redistribute* positions, none
reviewed. Counsel is asked to confirm or correct each, and to say whether "US
federal government work" carries, for a European holder, the consequence the
project has assumed.

(c) Is P6 correct?

(d) *(new)* For the five *may-preserve* sources in §3.2, is **preserve-only**
the right conservative default, and what, if anything, must be checked before
any display or redistribution? Does the Ukrainian copyright exclusion for
official documents, or the UN's terms, change the analysis for a holder in
France?

### Q8 — Terms of use of the external archives

Common Crawl and the Internet Archive's Wayback Machine are the two channels
the plan depends on for retrospective recovery. **Is bulk retrieval from them,
for archival preservation by a third party, within their terms of use?** If
their terms and the law diverge, which governs what the project may do with
material already retrieved?

### Q9 — `robots.txt` and rate limits, as policy

The project intends to adopt, as a recorded rule: a stable User-Agent naming
the project and a contact address; honour `robots.txt` by default for live
collection, with a per-source override that must state its rationale in the
registry; per-source rate limits as registry policy; and a publisher's opt-out
request recorded as a governed event.

**Is that the right default, and does `robots.txt` carry legal weight in
France** (as contract, as a signal bearing on authorised access, or not at
all)? Does a documented, rate-limited override change the analysis? What should
the project do when a publisher demands removal of material it believes it is
entitled to preserve? §3.4 is a live instance of a publisher restriction that
does not mention archiving.

### Q10 — Platform terms for named-channel capture

Given §3.3: do Telegram's terms permit capturing **named public channels**
through the public web preview, from one address, at the volume described? Does
breach of those terms carry consequences beyond account termination in the
establishment jurisdiction? Does the answer differ for (i) a public channel
read through the preview, as now, and (ii) an account that needs a logged-in
session? What follows, if anything, for the pages already captured, and for
the project's decision to extend this to more channels?

### Q11 — Discovery fetches

Assessing a candidate source means fetching a handful of its pages. The project
proposes to treat such a fetch as a **`discard`-tier acquisition**: the
attempt, outcome, locator and digest are recorded, **no bytes retained**, no
holding, no completeness claim. Does a fetch whose content is never retained
engage the personal-data framework at all? If it does, is the proposed record
too much, too little, or the wrong thing? *(Partly a data-protection question;
French data-protection counsel has it in Part A's context. Answer only the
parts that are yours.)*

### Q12 — The hosting arrangement

Controller established in France; server hosted by IONOS in Spain, both inside
the EEA. The project does not believe a Chapter V transfer question arises and
says so rather than asking counsel to rule out a non-issue. It asks:
(a) is that right, including whether renting servers in Spain creates an
establishment there or affects which authority is competent; (b) is there
anything beyond a standard Art. 28 processor contract this archive should insist
on, given what it holds; (c) does any of this change if the project
incorporates or moves the server? *(Largely a data-protection question; answer
only what is yours.)*

---

## 5. What the project is *not* asking

- **Not** advice on any specific listed person, designation or investigation.
- **Not** an opinion on legal chain of custody. The project never claims it as a
  status and will not cite a custody opinion.
- **Not** litigation-risk assessment or advice on any actual or threatened claim.
- **Not** permission to crawl the open web. Excluded by the project's own
  policy.
- **Not** the personal-data questions (lawful basis, Art. 9/10, data-subject
  requests, retention, DPIA). Those are with French data-protection counsel;
  where Part B touches them (Q11, Q12) this pack says so.
- **Not** advice on corporate form or tax.

---

## 6. The form the answer has to take

The outcome is entered into a permanent decision record and must survive being
read in ten years by someone who was not in the room.

1. **A written note structured against Q7–Q12**, even where the answer to one
   is "this does not arise".
2. **Each answer covers both states in §3.6 and names the deltas**: which
   conclusions differ between State 1 and State 2, on what trigger, and what
   would have to be true for the State 2 answer to hold. Where they are the
   same, saying so is a useful answer.
3. **Where counsel's view differs from a position in §2, name the divergence**
   as such, so the superseding decision record can state what changed.
4. **Mark each answer** as (i) settled law, (ii) counsel's judgement on an
   unsettled point, or (iii) a matter to keep under review.
5. **Say which conclusions can be applied as a class rule and which must be
   re-asked per source at registration time.** The project registers sources one
   at a time and has a class mechanism; it would rather answer once than ten
   times.
6. **Say whether the advice document is privileged**, and which of its
   conclusions the project may cite in a public decision record (the project's
   instinct: the conclusions must be citable; the document may not be).

---

## 7. Enclosures

1. POL-0001 (the project's personal-data policy) in full, for context only.
2. This pack.
3. The registry entries for the ten registered sources, showing the rights
   positions in §3.2 and their "NOT LEGALLY REVIEWED" / "UNVERIFIED" markers
   (the YAML under `sources/candidates/`, with no collected material).
4. A copy of the held publisher's policy and the draft permission request
   (§3.4).
5. On request: the decision records on quarantine, retention tiers, governed
   redaction and third-party captures (DR-0094).

Not enclosed: the Phase I requirements record, any collected material, and
anything held above `public` access tier.

---

## 8. For the founder — remove before sending

- **The pack is a snapshot.** §3 is as of 2026-10-12. If it is sent much later,
  re-check §3.1 (the count, and whether DR-0114/DR-0115 have been executed) and
  §3.3 against the records first.
- **Part A's counsel already has Q7–Q12 as context** (brief §9.5). Tell Part B's
  counsel that, and that Part A's answers may arrive later and may overlap Q11
  and Q12.
- **When advice arrives,** DR-0101 applies: a Decision Record records it;
  receipt, reading or commit is not recording. Part B's answers move neither
  DR-0072 nor LEGAL-009, and they decide Q8/Q9/Q10's acquisition steps.
- **Q10 is a finding for you, not just a question for counsel.** Platform
  capture began on 2026-09-21, not at some later step as the brief assumed.
  Whether to continue extending it (a third channel is approved but not run)
  while Q10 is unanswered is a choice the pack puts to counsel and does not
  make for you.
- **The engagement's cost and the controller.** If the association comes into
  being first, the client of this engagement changes; that is a POL-0001 §11
  material-change review, and counsel should be told.
