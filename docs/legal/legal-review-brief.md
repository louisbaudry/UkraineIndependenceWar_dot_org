# Brief for the POL-0001 §10 external legal review

**Status:** DRAFT v0.2 — AI-drafted, awaiting founder review. **Not** a
controlled document under [DR-0046](../decision-records/DR-0046-unified-document-control.md):
it is not a DR, SPEC, POL, REQ, METH or PROC, it enacts nothing, and it
changes no policy. It is the instruction sheet for an engagement the
founder has not yet commissioned.
**Fulfils:** [WP 3.4](../phase-3/working-papers/wp-3.4-foundational-corpus-acquisition.md)
§4.1 Track A item **A6** ("Prepare the legal-review brief (§7), so the
review is asked the questions this plan actually raises"); the questions in
Part B are WP 3.4 §7 restated for an external reader.
**Standard it serves:** [POL-0001](../policies/POL-0001-personal-data.md) §10
and LEGAL-009. **This brief does not replace, narrow or reinterpret §10** —
§10 remains the statement of what the review must cover, and Part A below is
its six topics expanded, not amended.
**Not legal advice.** Nothing here is legal advice, and nothing here is a
legal conclusion. Where this brief says "the project's position", it means a
position the project has adopted internally and is asking counsel to test.

### AI provenance (record §80)

Drafted 2026-09-15 by an AI assistant (Anthropic Claude Code agent session)
at the founder's direction; revised to v0.2 the same day, after the founder
ruled on §9.1–9.3, to point those three at the decision record that now
holds them. The drafter is not a lawyer. Every factual claim
in §3 was taken from the repository as it stood on that date and is
footnoted to its source there; no claim in §3 was verified against the
archive server's live database, which this session cannot reach. No external
counsel, bar association, or fee schedule was consulted, and no external host
was contacted. Candidate until the founder approves it.

---

## 1. Read this first: the brief is not yet sendable

Facts an external adviser needs on the first page did not exist anywhere in
the project's record when this brief was drafted, and it leaves them blank
rather than guessing. **§9 lists them.** They are not drafting gaps; each is
a founder decision.

Since the first draft, the founder has ruled on how three of them are to be
recorded, and they have moved into
[`DR-pending-establishment-jurisdiction`](../decision-records/DR-pending-establishment-jurisdiction.md).
**Two remain empty and still block the engagement:** the project's
establishment jurisdiction — which decides which country's law five of the
eleven questions are answered in, and which counsel can be instructed at all
— and the archive server's provider and country.

Note also that this file lives in a public Git repository. The engagement's
particulars — the founder's identity and address, the counsel's name, fees,
and any material the project holds at a restricted access tier — belong in
the covering letter and the engagement terms, **not in this file**.

---

## 2. What the project is, in one page

*(Counsel will not have the repository. This section and §3 are meant to be
sufficient on their own.)*

The project is a **durable historical evidence and knowledge repository**
documenting Ukraine's Second War of Independence and the machinery sustaining
Russia's war against it — including sanctions and export-control evasion. It
is independent and non-Ukrainian. Its time horizon is measured in decades. It
describes itself, in its founding record, as an archive first and a website
last.

Three properties matter more than the subject matter for the questions below.

**It separates three decisions that most systems collapse into one.**
Material passes three gates, and a "yes" at one never implies a "yes" at the
next:

| Gate | Decision | Who |
|---|---|---|
| **Gate 1 — Preserve** | Do we keep these bytes, containing whatever they contain? | Automated admission check, on registered sources only |
| **Gate 2 — Structure** | Do we promote a person into queryable fields — name, identifiers, location, relationships? | A human editor, at a risk tier |
| **Gate 3 — Publish** | Does this appear on a public surface, at which access tier? | A human editor, separately |

The project's personal-data policy exists chiefly to govern **Gate 2**, on
the reasoning that preservation is usually permissible and often obligatory,
publication is already gated, and structuring is where a document quietly
becomes a surveillance index.

**Collection creates no knowledge.** No automated process may assert anything.
A completed collection run produces preserved files and review queues, and
zero assertions of fact. This is enforced in code and in the database, not
merely intended.

**Nothing about a person is inferred automatically.** Deriving a person's
location, affiliation, health, ethnicity, or beliefs from held material is an
editorial act subject to human review — never an automated enrichment. The
project does not build a personnel index of an army or a population index of
a territory.

The archive is append-only. Correction normally means adding a superseding
statement rather than editing history; **governed redaction is the single
exception to immutability**, and it leaves a tombstone recording the fact,
date, authority, and grounds of the removal.

---

## 3. What the project actually holds today

This is a small and unusually well-documented factual base, which is the
reason for commissioning the review now rather than later: **counsel is being
asked to advise on a scale-up that has not happened yet.**

### 3.1 Collection to date

| Fact | Value |
|---|---|
| Sources registered and collected | **2** — the EU Consolidated Financial Sanctions List (European Commission, DG FISMA) and the US Treasury OFAC SDN / Consolidated Sanctions lists |
| First and only live collection | **2026-09-09**, on the project's archive server: 5 files, ~211 MB, zero failures |
| Sources approved for registration but not yet executed | **3** — UK OFSI consolidated list; the US BIS Denied Persons List; the Swiss SECO sanctions list |
| Sources still unverified candidates | **2** — EUR-Lex sanctions instruments; Ukraine's NSDC sanctions decisions |
| Assertions of fact created from any of it | **zero** |
| Personal data promoted into structured, queryable fields | **none** |
| Material published on any public surface | **none**; no public surface carrying project content exists |
| Retention tier applied | `permanent`, with fixity re-checked on a 180-day cadence |

Every registration is an individual, recorded decision by the founder;
registering a source *is* the act that authorises collecting from it. There
is no general collection authority.

### 3.2 What that material contains, stated precisely

The five files are official sanctions lists: roughly 6,200 listed persons,
groups and entities on the EU list (about 2,960 of them under the Ukraine
programme) and 19,329 SDN entries on the OFAC list (6,348 under the Russia
programme). As published by the designating authorities, these entries
routinely carry:

- names and aliases; dates and places of birth; nationality;
- passport and national identity-document numbers; addresses;
- the designating authority's **stated grounds for designation**, which
  commonly recite alleged conduct and frequently recite a person's office,
  political role, or affiliation.

**Two adjacencies counsel should be aware of rather than have to discover.**
The stated grounds bring this material close to GDPR Art. 10 (criminal
convictions and offences) and, where a designation recites political role or
affiliation, close to Art. 9 (political opinions) — even though every word of
it was published by a public authority. The project's current position is
that this is authoritative record material which may be preserved and, at
Gate 2, structured as *designation records kept distinct from the project's
own conclusions about a person*; Q2 below asks counsel to test that.

The files are held whole, exactly as served, and are not parsed on ingest.

### 3.3 What the project intends to do next, and why it has stopped

The plan for constituting a foundational corpus (WP 3.4) is, in order:

1. a **census** of candidate sources built from public indexes and citation
   graphs — no fetch of any candidate host;
2. **retrospective recovery** of registered sources' past pages from existing
   web archives (Common Crawl, the Internet Archive's Wayback Machine);
3. **registered live collection** on a recurring cadence, including
   systematic capture within a registered source's own domain;
4. eventually, named channels and named accounts on social platforms, where
   those are themselves registered sources.

**Open-web crawling is excluded from this plan permanently**, before and after
this review, by the project's own policy — not as a matter of legal caution
but as a matter of archival method. The project is not asking counsel whether
it may crawl the web, because it has already decided it will not.

Steps 2–4 are **suspended**. The project's interim constraints bind collection
to registered sources with human-configured scope, and the policy's release of
those constraints is conditioned on this review being obtained and recorded.
Preparatory work that collects nothing continues; collection at scale does
not. **This review is the gate.**

### 3.4 Access and storage posture

Material is stored in OCFL objects on the project's own archive server, with
retention tiers (`permanent`, `medium-term`, `metadata-only`, `discard`) and
seven declared access tiers (`public`, `subscriber`, `researcher-restricted`,
`investigator-restricted`, `internal`, `private-preservation`,
`confidential`). Access tiers are **declared per item**, never derived from a
ranking, and apply at every layer including derived projections and search
indexes. Witness identities, when the project ever holds any, are held in a
separable confidential store under pseudonymous identifier and are by default
never structured into the research graph.

---

## 4. Positions the project has already taken

**These are for counsel to test, not to choose.** They were settled by the
founder on 2026-08-16 after individual review, and the project would rather
be told they are wrong than be handed a different framework without being
told why.

| # | Position | Where it comes from |
|---|---|---|
| P1 | The project's **primary lawful basis is archiving in the public interest and historical/scientific research** (GDPR Art. 89, with the Art. 9(2)(j) exception for special categories), invoking Art. 85 expression provisions secondarily — rather than treating itself primarily as journalism | POL-0001 §8.3 |
| P2 | **Victims are named publicly only where an authoritative or already-public source has named them**, or the family consents. The project never becomes the first publisher of a victim's name. Full identification may still be held internally, at its access tier | POL-0001 §8.1 |
| P3 | **An individual rank-and-file combatant is identified publicly only where reviewed evidence ties them to a specific documented act**, typed as an allegation unless a legal finding exists — never for presence or unit membership alone. Geneva III Art. 13 protection of prisoners of war against public curiosity is applied as an editorial constraint regardless of whether it binds the project legally | POL-0001 §8.2 |
| P4 | Special-category data, criminal-offence data about individuals, contact details and identity-document numbers of private individuals, precise location of living private individuals, and facial-recognition-derived identifications are **never structured automatically**, for any category of person, by any process | POL-0001 §4 |
| P5 | The GDPR does not apply to the deceased, but the project applies a **dignity standard regardless** | POL-0001 §5.9 |
| P6 | Content recovered from a third-party web archive carries the **original publisher's** rights position, not the archive's; the archive is recorded as the acquisition channel and is never itself registered as a source | DR-0094 §1 |

P6 is a premise the project adopted for archival-provenance reasons and has
never legally verified. Q7 asks counsel to test it.

---

## 5. Part A — the six topics POL-0001 §10 requires

Each question states what the project believes, what it is unsure of, and
what form of answer would let it act. Counsel should feel free to answer a
question the project failed to ask.

### Q1 — Lawful basis and Art. 89 safeguards
Is P1 sustainable for this project as described in §2–§3 — and specifically,
does an independent, privately-run repository with no academic or memorial
institutional affiliation qualify as carrying out "archiving in the public
interest" or "historical research" for Art. 89 purposes in the establishment
jurisdiction? If it does, **what safeguards does Art. 89(1) require us to
have in place that we do not have**, given §2's gate structure and §3.4's
storage posture? If it does not, what is the basis we should be operating
on instead, and what changes?

### Q2 — Art. 9 and Art. 10 handling
Given §3.2's account of what official sanctions designations contain:

(a) does holding and structuring designation records — as records of what an
authority decided, kept distinct from the project's own conclusions —
engage Art. 9 and Art. 10 at all, and if so on what basis may it continue?

(b) does the analysis change when the project structures the *grounds* of a
designation, as opposed to the identifying particulars?

(c) is P4's blanket prohibition on automated structuring of special-category
data sufficient, or does the project also need a documented rule for the
manual case beyond "an explicit, recorded editorial decision citing
necessity"?

### Q3 — Applicable Art. 85 provisions
Which member-state provisions reconciling data protection with freedom of
expression and information apply, and what do they actually give this project
— given P1's choice to treat journalism as secondary? Where the establishment
jurisdiction's Art. 85 regime distinguishes journalistic, academic, artistic
and literary purposes, **which limb, if any, does this project fall under**,
and does relying on it require anything of the project (registration,
self-designation, an editorial code) that it has not done?

### Q4 — Data-subject request procedure
The project's current procedure is at POL-0001 §6: requests logged, assessed
and answered with a recorded rationale whether granted or refused; the
derogation relied on named to the requester; rectification normally by
superseding assertion rather than editing history; erasure, where granted,
by governed redaction leaving a tombstone. **Is that procedure adequate and
lawful, and what does it omit?** In particular:

(a) is a tombstone recording the fact, date, authority and grounds of a
removal compatible with an erasure the project has actually granted, or does
the tombstone itself need to be erasable in some cases?

(b) what identity-verification standard should apply to a requester,
given the plausible case of a listed person's representative and the equally
plausible case of a hostile requester seeking to confirm what the project
holds?

(c) what response deadlines and escalation routes bind us, and is a published
contact point required before collection at scale begins?

### Q5 — Retention
Every source registered so far is at `permanent` retention. Is indefinite
retention of personal data defensible under the Art. 89 posture, and if so
does it require a periodic review the project is not doing? The project
currently re-decides only `medium-term` material at its review date and
checks `metadata-only` records for drift into de-facto identification. Should
`permanent` material about living private individuals carry a review cadence
too, and on what trigger?

### Q6 — DPIA obligation
Does the project's planned processing require a data protection impact
assessment, and does any part of it require **prior consultation** with the
supervisory authority? If a DPIA is required: is it required now, on the
current two-source footprint, or only at the point of scale-up — and would
counsel prepare it, review one the project drafts, or specify its scope for
the project to complete? The project would also like to know whether a data
protection officer must be designated, and whether an Art. 27 representative
is needed for any jurisdiction in which it is not established.

---

## 6. Part B — acquisition questions the record does not reach

POL-0001 §10 is about personal data. The acquisition plan in §3.3 raises
questions the project's founding record never contemplated — the words
*robots*, *terms of service* and *copyright* do not appear in it. These are
asked here so the answer is obtained once rather than improvised per source.
**They may need different counsel from Part A** (see §9.5).

### Q7 — Preservation-only copying, and the database right
The project's rights vocabulary separates **may preserve** from **may
display** from **may redistribute**, per source. Much of what it wants to
recover would be preserved and never displayed.

(a) Under the establishment jurisdiction's archiving and research exceptions,
may the project copy third-party web content wholesale into a **non-public**
archive, where no public display is made?

(b) The sanctions lists in §3.1 are copied **whole**, as datasets. Does the
**EU sui generis database right** restrict that, and does any exception cover
it? This is not hypothetical: the project's registry currently records the EU
list as redistributable under Commission Decision 2011/833/EU subject to
acknowledgement, and the OFAC list as a US federal government work not
subject to domestic copyright — **and both entries are explicitly marked "NOT
LEGALLY REVIEWED"** pending this engagement. Counsel is asked to confirm or
correct those two positions specifically, and to say whether "US federal
government work" carries the consequence the project has assumed for a
European holder.

(c) Is P6 — that a capture recovered from a third-party archive carries the
original publisher's rights position rather than the archive's — correct?

### Q8 — Terms of use of the external archives
Common Crawl and the Internet Archive's Wayback Machine are the two
acquisition channels the plan depends on for retrospective recovery. **Is
bulk retrieval from them, for archival preservation by a third party, within
their terms of use?** If their terms and the law diverge, which governs what
the project may do with material already retrieved?

### Q9 — `robots.txt` and rate limits, as policy
The project intends to adopt, as a recorded rule: identify collectors with a
stable User-Agent naming the project and a contact address; honour
`robots.txt` by default for live collection, with a per-source override that
must state its rationale in the registry; apply per-source rate limits as
registry policy rather than code; and record a publisher's opt-out request as
a governed event handled with the same care as a data-subject request.

**Is that default the right one, and does `robots.txt` carry any legal weight
in the establishment jurisdiction** — as contract, as a signal bearing on
authorised access, or not at all? Does an override that is documented and
rate-limited change the analysis? What should the project do when a publisher
demands removal of material the project believes it is entitled to preserve?

### Q10 — Platform terms for named-channel capture
Step 4 of §3.3 would capture **named** channels and **named** accounts on
platforms — Telegram in particular — as registered sources, expressly not
untargeted harvesting. Do the platforms' terms permit this; does breach of
those terms carry consequences beyond account termination in the
establishment jurisdiction; and does the answer differ for a public channel
versus an account that requires a logged-in session to read?

### Q11 — Discovery fetches
Assessing a candidate source means fetching a handful of its pages to see
what it is. The project proposes to treat such a fetch as a **`discard`-tier
acquisition**: the attempt, outcome, locator and digest are recorded, **no
bytes are retained**, and the record is not a holding and carries no
completeness claim.

Does a fetch whose content is never retained engage the personal-data
framework at all? If it does, what record of it suffices — and is the
proposed record too much, too little, or the wrong thing?

---

## 7. What the project is *not* asking

Stated so counsel does not spend fees on it, and so the answer is not
mistaken for something it is not:

- **Not** advice on any specific listed person, designation, or investigation.
- **Not** an opinion on legal chain of custody. The project's standing rule is
  that it **never claims chain of custody as a status**; it documents its own
  handling and says so. Counsel is asked not to supply a custody opinion, and
  the project will not cite one.
- **Not** litigation risk assessment, and not advice on any actual or
  threatened claim.
- **Not** a choice of legal posture. P1 was ruled by the founder; Q1 tests it.
- **Not** permission to crawl the open web. That is excluded by the project's
  own policy and is not on the table.
- **Not** advice on the project's corporate form or tax position, except so
  far as Q6 and §9.2 make the controller's identity relevant.

---

## 8. The form the answer has to take

POL-0001 §10 says the review's outcome **is recorded, and the policy is
revised to match it**. That has two consequences for how counsel's advice is
delivered.

1. **The project needs a written answer it can quote and cite, question by
   question.** An advice note structured against Q1–Q11 above — even where
   the answer to one is "this does not arise" — is worth considerably more
   to the project than a discursive memorandum, because the outcome is
   entered into a permanent decision record and the reasoning has to survive
   being read in ten years by someone who was not in the room.
2. **Where counsel's conclusion differs from a position in §4, the project
   needs the divergence named as such**, so the superseding decision record
   can state what changed and why. A silently different framework cannot be
   recorded.

The project also asks counsel to mark, for each answer, whether it is
(i) settled law, (ii) counsel's judgement on an unsettled point, or
(iii) a matter the project should keep under review as law or practice
develops. The project's document control distinguishes these, and collapsing
them would lose information the archive is built to keep.

Finally: the project will record **that** the review was obtained, from
counsel qualified in the named jurisdiction, and what it concluded. Whether
the advice itself is published, held at a restricted access tier, or held
under privilege is a decision the founder makes on counsel's recommendation —
see Q12 in §12.

---

## 9. What the founder must settle before this is sent

Five blanks. **The first three are now governed by a decision record of
their own** — see 9.1–9.3 below; two of them are still empty. The fourth and
fifth remain open.

### 9.1–9.3 Establishment jurisdiction, controller, hosting location
**These three facts are not decided in this brief.** They are decided in
[`DR-pending-establishment-jurisdiction`](../decision-records/DR-pending-establishment-jurisdiction.md),
and this brief is filled *from* that record rather than the other way round.

On 2026-09-15 the founder ruled how they should be recorded (option B of
three): the jurisdiction and the hosting location are recorded now, the
**controller is the founder/principal editor as a natural person** — no legal
entity exists — and later incorporation, or a change of jurisdiction or
hosting country, is a material change under POL-0001 §11 that triggers a
recorded review. Counsel should be told that incorporation is contemplated,
so the advice is not answering a question the project may stop asking.

**Still empty in that record, and blocking:** the establishment jurisdiction
itself, and the archive server's provider and country. POL-0001 §10 requires
review "in its establishment jurisdiction"; POL-0001 §2 says only that the
project is "European-based". Until the jurisdiction is supplied, **Q1, Q3,
Q5, Q7 and Q9 have no law to be answered in and no counsel can be
selected**. The hosting location is needed for establishment and transfer
analysis. Both go in the covering letter as well, and neither may be inferred
— not from this brief, not from the repository.

### 9.4 Whether the project holds itself out as publishing
Q3's Art. 85 analysis turns partly on this, and the honest current answer is
"not yet, and not for some time": nothing is published, and no public surface
carrying project content exists. The founder should decide whether counsel is
being asked about the project as it is or as it intends to be, and this brief
assumes **as it intends to be** — stated here so it can be corrected.

### 9.5 One engagement or two
Part A is data-protection work. Part B (Q7–Q10 especially) is copyright,
database-right and platform-terms work, which a data-protection practice may
decline or answer thinly. The founder should decide whether to brief one firm
across both, brief two, or send Part A now and hold Part B — noting that only
Part A is what POL-0001 §10 makes a condition of the §9 releases, and that
Part B governs acquisition steps the project cannot take until Part A is
answered anyway.

---

## 10. Materials to supply with the brief

Counsel should not be sent the repository. The proposed enclosure set:

1. POL-0001 (the personal data policy) in full — it is the thing being tested.
2. This brief.
3. The source registry entries for the two registered sources, showing the
   recorded rights positions and their "NOT LEGALLY REVIEWED" markers.
4. A one-page description of the three-gate pipeline and the access tiers
   (§2 and §3.4 of this brief serve, if a standalone page is not wanted).
5. On request: the decision records governing quarantine, retention tiers,
   governed redaction, and third-party captures.

Not enclosed: the Phase I requirements record (long, and mostly about
evidentiary method rather than anything counsel needs) and any material held
above `public` access tier.

---

## 11. Candidate Decision Records (proposals — require founder approval)

Numbering continues from CDR-P3-41, the highest used anywhere in `docs/`.

- **CDR-P3-42 — ~~The establishment jurisdiction and the controller's
  identity are recorded before the review is commissioned.~~ Discharged
  2026-09-15.** The founder ruled the same day this brief was drafted, and
  the proposal became
  [`DR-pending-establishment-jurisdiction`](../decision-records/DR-pending-establishment-jurisdiction.md),
  which is where these facts now live. That record is a **draft**: its shape
  is ruled, its jurisdiction and hosting-location fields are still blank, and
  it is not approvable until they are filled. Kept here, struck through,
  because the CDR number is spent and should not be reused.

- **CDR-P3-43 — What "the review's outcome is recorded" means.** The review
  is recorded by a decision record that supersedes DR-0072, states per
  question what counsel concluded and with what degree of settledness, names
  every divergence from the §4 positions, and carries POL-0001 to v2.0 in the
  same act. **POL-0001 §9's releases take effect on that record's approval
  and not before** — not on receipt of the advice, and not on the founder
  reading it. LEGAL-009 moves from "partially satisfied" to satisfied in the
  same commit, or the reason it does not is stated.

- **CDR-P3-44 — A rights position marked unreviewed cannot reach Gate 3.**
  The source registry's `rights_basis` is free text, and the two registered
  sources carry `may-redistribute` on a basis whose own text says "NOT
  LEGALLY REVIEWED". Nothing in the schema or the publication gate prevents a
  publication decision from resting on it. The proposal: rights review state
  becomes a declared field rather than a marker buried in prose, and Gate 3
  refuses a publication whose rights basis is unreviewed, in the database and
  in the code both. This is a real gap rather than a hypothetical one, but it
  is **not urgent** — nothing is published, and it can be fixed any time
  before the first Gate 3 decision.

---

## 12. Open questions raised

1. **Q12 — the status of counsel's advice itself.** Privileged, restricted,
   or publishable? The project's instinct is that the *conclusions* must be
   publishable, since they will be cited in a decision record that is public,
   while the advice document may not be. Counsel should be asked which.
2. Whether obtaining this review creates an ongoing relationship the project
   should budget for, given POL-0001 §11's annual review and its "material
   change to collection scope, jurisdiction, or applicable law" trigger.
3. Whether Ukrainian and Russian data-protection law bear on the project at
   all, given that most data subjects are in those two jurisdictions and the
   project is established in neither. Not asked in Part A because the answer
   may be that it is out of scope for establishment-jurisdiction counsel —
   but the project would rather be told that than assume it.
4. Whether any of Part B's answers should be re-asked per source at
   registration time, or answered once as a class rule. The registration-class
   mechanism (CDR-P3-32, candidate) is the natural home for the latter.

---

## 13. Sources

- [POL-0001](../policies/POL-0001-personal-data.md) — §1–§12, and §10 as the
  standard this brief serves; the §8 rulings are §4's P1–P3.
- [WP 3.4](../phase-3/working-papers/wp-3.4-foundational-corpus-acquisition.md)
  §4.1 (item A6), §4.2, §7 (Part B's five questions), §1.3 (the founder's
  ruling of 2026-09-08).
- Decision records: [DR-0008](../decision-records/DR-0008-custody-claims-discipline.md)
  (no chain-of-custody claim), [DR-0055](../decision-records/DR-0055-append-only-canonical-store.md)
  and [DR-0077](../decision-records/DR-0077-redaction-sole-immutability-exception.md)
  (append-only, governed redaction), [DR-0066](../decision-records/DR-0066-three-gate-pipeline.md)
  (three gates), [DR-0067](../decision-records/DR-0067-source-registry-schema.md)
  (registry, rights fields), [DR-0068](../decision-records/DR-0068-retention-tiers.md)
  (retention tiers), [DR-0071](../decision-records/DR-0071-interim-personal-data-constraints.md)
  and [DR-0072](../decision-records/DR-0072-personal-data-policy-adoption.md)
  (interim constraints; policy adoption),
  [DR-0086](../decision-records/DR-0086-tier-restrictiveness-declared.md)
  (declared access tiers), [DR-0093](../decision-records/DR-0093-first-source-registrations.md)
  (§3.1's and §3.2's collection facts),
  [DR-0094](../decision-records/DR-0094-third-party-web-captures.md) (§4's P6).
- Requirements: LEGAL-007 (§7's custody exclusion), LEGAL-008 (§3.4 and Q7's
  permission set), LEGAL-009 (the condition this review discharges).
- [`sources/README.md`](../../sources/README.md) and
  `sources/candidates/sanctions-authorities.yaml` — §3.1's registration
  state and Q7(b)'s two unreviewed rights positions, quoted verbatim.
- Record §9, §13, §14, §26, §28, §78–§80, §100 (Principles 5, 11, 18).
