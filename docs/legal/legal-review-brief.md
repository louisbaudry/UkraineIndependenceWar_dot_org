# Brief for the POL-0001 §10 external legal review

**Status:** DRAFT v0.4 — AI-drafted, awaiting founder review. **Not** a
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
at the founder's direction; revised to v0.2 the same day after the founder
ruled on §9.1–9.3, and to **v0.3** after the founder supplied the two facts
that ruling left open — **France** as the establishment jurisdiction and
**IONOS, Spain** as the archive host. v0.3 rewrites Q1–Q3, Q5, Q6, Q7 and Q9
against French law instead of a placeholder, and adds Q12 on the hosting
arrangement.

v0.4 closes the last two of §9's blanks — the engagement is split (§9.5) and
counsel answers for both states in §3.5 with the deltas named (§9.4) — adds
§3.5, and rewrites §8 accordingly. **No decision in this brief is now
outstanding.**

**What was verified for v0.3, and how.** The French statutory texts quoted in
Q1–Q3 and Q5 were read from the CNIL's own consolidated version of the Loi
n° 78-17 du 6 janvier 1978, fetched from `cnil.fr` on 2026-09-15 (HTTP 200).
`legifrance.gouv.fr` was tried on the same date for the authoritative text
and returned 403 behind an anti-bot challenge, so **every article quoted here
should be checked against Légifrance before the brief is sent**; the CNIL
version is reliable in practice but is not the official journal. No case law,
CNIL deliberation, doctrinal commentary or Code du patrimoine provision was
read. The drafter is not a lawyer. Where this brief observes that a
statutory limb appears not to fit the project, that is an observation about
the text put to counsel as a question — **not** a conclusion, and not advice. Every factual claim
in §3 was taken from the repository as it stood on that date and is
footnoted to its source there; no claim in §3 was verified against the
archive server's live database, which this session cannot reach. No external
counsel, bar association, or fee schedule was consulted, and no external host
was contacted. Candidate until the founder approves it.

---

## 1. Read this first: the brief is not yet sendable

Facts an external adviser needs on the first page did not exist anywhere in
the project's record when this brief was first drafted. They do now:
**France**, the **founder as a natural person** as controller, and **IONOS in
Spain** as the host, all recorded in
[`DR-0100`](../decision-records/DR-0100-jurisdiction-controller-and-hosting.md)
rather than decided here — which **confirms** the interim France ruling a
parallel session recorded on 2026-09-14 (`DR-0099`,
which amended POL-0001 to v1.1) and adds the controller and hosting facts to
it. *Interim* is that record's word and is kept: no legal entity exists, and
whether entity formation should itself be a preliminary question for this
review is open — counsel should be asked. The questions below are written
against French law accordingly.

**No decisions remain open.** All five of §9's blanks are closed: the brief
goes to **French data-protection counsel for Part A (Q1–Q6) only**, with Part
B (Q7–Q12) travelling as context rather than instructions for separate
IP/media counsel later (§9.5), and counsel answers **for both the project as
it is today and as it intends to be, naming the deltas** (§9.4, §3.5, §8).

**One caution**
carries into the engagement itself: every French statutory text quoted here
was read from the CNIL's consolidated version, not from Légifrance, which was
unreachable on the drafting date — see the provenance note above.

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

**Who and where.** The project is established in **France**; the controller
is the **founder/principal editor as a natural person** — there is no legal
entity, though incorporation is contemplated; the archive server is hosted
with **IONOS in Spain**. These are recorded in a decision record of the
project's own, not decided in this brief. The applicable framework is
therefore the GDPR as applied in France together with the **Loi n° 78-17 du
6 janvier 1978 (Loi Informatique et Libertés, "LIL")**, and the expected
supervisory authority is the **CNIL**.

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

Material is stored in OCFL objects on the project's archive server — hosted
with IONOS in Spain, so controller establishment and processing location are
both inside the EEA — with
retention tiers (`permanent`, `medium-term`, `metadata-only`, `discard`) and
seven declared access tiers (`public`, `subscriber`, `researcher-restricted`,
`investigator-restricted`, `internal`, `private-preservation`,
`confidential`). Access tiers are **declared per item**, never derived from a
ranking, and apply at every layer including derived projections and search
indexes. Witness identities, when the project ever holds any, are held in a
separable confidential store under pseudonymous identifier and are by default
never structured into the research graph.

### 3.5 The two states counsel is asked to answer for

Every question in Part A is asked twice, and §8 explains what the project
needs back. The two states, so there is no ambiguity about which is which:

**State 1 — as it is (2026-09-15).** Two registered sources; five files;
~211 MB; whole-file capture with no parsing on ingest; **nothing structured,
no assertions, nothing published, no public surface**; controller a natural
person; one processor (IONOS, Spain); no staff beyond the founder. Everything
in §3.1 and §3.2, and nothing beyond it.

**State 2 — as intended.** The end state of the acquisition plan in §3.3:
a census-derived set of registered sources collected on a recurring cadence;
retrospective recovery of those sources' past pages from third-party
archives; **Gate 2 structuring at volume, including the grounds of
designations and the identities of investigative subjects**; publication at
declared access tiers, including a genuinely public surface; plausibly an
incorporated entity and a small trusted team. The material stays what §3.2
describes — criminal-offence-adjacent, about living people, much of it
concerning people in Russia and in occupied territory.

The project is at State 1 and does not expect to reach State 2 for a long
time. It is asking about both because the review exists to unblock the
journey, and because a conclusion that holds at State 1 and fails at State 2
is the most useful thing counsel could tell it.

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

**P1 is under more pressure than the others**, and the project would rather
say so than have counsel discover it. Reading the LIL's Articles 46, 78 and
80 (quoted at Q2, Q1 and Q3) alongside what §3.2 says this archive holds,
the French route that appears to unlock criminal-offence data is the
*expression* limb rather than the *archiving/research* limb — which is the
opposite of the priority the founder ruled at POL-0001 §8.3. The project is
not asserting that; it is flagging it, because if it is right then §8 of this
brief requires counsel to name the divergence so the superseding decision
record can state what changed.

---

## 5. Part A — the six topics POL-0001 §10 requires

Each question states what the project believes, what it is unsure of, and
what form of answer would let it act. Counsel should feel free to answer a
question the project failed to ask.

### Q1 — Lawful basis and Art. 89 safeguards, in France
Is P1 sustainable for this project as described in §2–§3? Specifically: does
an independent, privately-run repository with no academic, memorial or
public-service affiliation carry out *"traitements à des fins archivistiques
dans l'intérêt public"* in France?

The project's difficulty is that **LIL Article 78 appears to frame that
route around public archive services**:

> "Lorsque les traitements de données à caractère personnel sont mis en œuvre
> par **les services publics d'archives** à des fins archivistiques dans
> l'intérêt public conformément à l'article L. 211-2 du code du patrimoine,
> les droits prévus aux articles 15, 16 et 18 à 21 du règlement […] ne
> s'appliquent pas […]. Les conditions et garanties appropriées prévues à
> l'article 89 du même règlement sont déterminées par le code du patrimoine
> et les autres dispositions législatives et réglementaires applicables aux
> **archives publiques**."

(a) Can a private archive rely on *fins archivistiques dans l'intérêt public*
in France at all, or is that in practice reserved to *services publics
d'archives*? If it cannot, is **recherche scientifique ou historique** the
available route, and what does the Conseil d'État decree contemplated by
Article 78's second paragraph require of a body relying on it?

(b) If the project qualifies under neither, what basis should it be operating
on, and what changes in §2's architecture or §3.4's posture?

(c) **LIL Article 79** disapplies GDPR Art. 14(1)–(4) for archiving,
research and statistical purposes where the data were not obtained from the
subject, and is not on its face limited to public archive services. Does the
project get it? This matters practically: the project cannot notify the
~25,000 listed persons in §3.1's two files, and would like to know whether
that is lawful or merely impossible.

(d) What **Art. 89(1) safeguards** must the project have that it does not,
given §2's gate structure and §3.4's tiering and access controls?

### Q2 — Art. 9, Art. 10, and LIL Article 46 — **the sharpest question here**
Given §3.2's account of what official sanctions designations contain, and
what this project is for, **LIL Article 46 is the provision the project most
needs resolved**:

> "Les traitements de données à caractère personnel relatives aux
> condamnations pénales, aux infractions ou aux mesures de sûreté connexes
> **ne peuvent être effectués que par** : les juridictions, les autorités
> publiques et les personnes morales gérant un service public […] ainsi que
> les personnes morales de droit privé collaborant au service public de la
> justice et appartenant à des catégories dont la liste est fixée par décret
> en Conseil d'État […] ; les auxiliaires de justice […] ; les personnes
> physiques ou morales, aux fins de leur permettre de préparer et, le cas
> échéant, d'exercer et de suivre une action en justice en tant que victime,
> mise en cause, ou pour le compte de ceux-ci […] ; les personnes morales
> mentionnées aux articles L. 321-1 et L. 331-1 du code de la propriété
> intellectuelle […] ; les réutilisateurs des informations publiques
> figurant dans les décisions [de justice] […] sous réserve que les
> traitements […] n'aient ni pour objet ni pour effet de permettre la
> réidentification des personnes concernées."

The project is a private archive documenting alleged atrocity crimes and
sanctions evasion. **It does not obviously fall within any of those limbs**,
and it would rather be told that plainly now than find out later.

(a) Does what the project does engage Article 46 at all — and does the answer
differ between **preserving** a published sanctions list whole (Gate 1) and
**structuring** a person's designation grounds into queryable fields
(Gate 2)? The project's entire architecture rests on that distinction being
real, and it would like to know whether French law recognises it or treats
both as one *traitement*.

(b) If Article 46 is engaged and no limb fits, is **Article 80** (Q3) the
only available route, and what would the project have to do, or be, to use
it?

(c) Does the position change for material that is not a designation — a
published indictment, an ICC filing, a court judgment — which POL-0001 §4
already treats as "the authoritative record itself"?

(d) **Art. 9**: where a designation recites a person's political role or
affiliation, is the project processing political-opinion data, and does
Art. 9(2)(j) with Art. 89 cover it in France given Q1's answer?

(e) Is P4's blanket prohibition on *automated* structuring sufficient, or
does the project also need a documented standard for the manual case beyond
"an explicit, recorded editorial decision citing necessity"?

### Q3 — Art. 85 in France: LIL Article 80
France's Art. 85 provision appears to be **LIL Article 80**, and it matters
here because it expressly disapplies Article 46:

> "À titre dérogatoire, les dispositions du 5° de l'article 4, celles des
> articles 6, **46**, 48, 49, 50, 53, 118, 119 et celles du chapitre V du
> règlement […] ne s'appliquent pas, lorsqu'une telle dérogation est
> nécessaire pour concilier le droit à la protection des données à caractère
> personnel et la liberté d'expression et d'information, aux traitements mis
> en œuvre aux fins : d'expression universitaire, artistique ou littéraire ;
> d'exercice à titre professionnel, de l'activité de journaliste, dans le
> respect des règles déontologiques de cette profession."

(a) **Which limb, if any, does this project fall under?** It is not a
university and holds no academic affiliation; it is not a press
organisation and its founder is not a professional journalist; it describes
itself as a historical evidence repository.

(b) Does *"expression universitaire"* require an institutional affiliation,
or does it describe a kind of work? If the latter, what would the project
have to show?

(c) If the journalism limb were the route, what do *"les règles
déontologiques de cette profession"* require of a body that has none of the
usual apparatus — no press card, no publication yet, no editorial staff
beyond the founder? Would adopting and publishing an editorial code help, or
is it beside the point?

(d) Can the project rely on Article 80 for part of its processing and on the
archiving/research provisions (Q1) for the rest, or must it pick one posture?

(e) **This is where P1 gets tested.** POL-0001 §8.3 ruled archiving and
research primary, with expression secondary. If French law inverts that —
if Article 80 is what actually makes this project's core material lawful to
process — say so in terms, per §8 of this brief, so the project can record
the change rather than absorb it silently.

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
Every source registered so far is at `permanent` retention. The LIL permits
personal data to be kept beyond the ordinary period *"dans la mesure où elles
sont traitées exclusivement à des fins archivistiques dans l'intérêt public,
à des fins de recherche scientifique ou historique, ou à des fins
statistiques"*, and provides that the choice of what is kept for archiving in
the public interest is made *"dans les conditions prévues à l'article
L. 212-3 du code du patrimoine"* — a provision about public archives.

Given Q1's answer, is indefinite retention defensible for **this** archive,
and by what mechanism if not that one? Does it require a periodic review the
project is not doing? The project
currently re-decides only `medium-term` material at its review date and
checks `metadata-only` records for drift into de-facto identification. Should
`permanent` material about living private individuals carry a review cadence
too, and on what trigger?

### Q6 — DPIA obligation
Does the project's planned processing require a data protection impact
assessment — testing it against **the CNIL's published lists of processing
for which an AIPD is and is not required**, as well as GDPR Art. 35(3) — and
does any part of it require **prior consultation** with the CNIL? If a DPIA is required: is it required now, on the
current two-source footprint, or only at the point of scale-up — and would
counsel prepare it, review one the project drafts, or specify its scope for
the project to complete? The project would also like to know whether a data
protection officer must be designated, and whether an Art. 27 representative
is needed anywhere — noting that the controller is a natural person
established in France and that incorporation is contemplated, so advice that
holds only for an unincorporated founder has a short life.

---

## 6. Part B — questions the founding record does not reach

POL-0001 §10 is about personal data. Q7–Q11 come from the acquisition plan in
§3.3, which raises questions the project's founding record never
contemplated — the words *robots*, *terms of service* and *copyright* do not
appear in it. Q12 arises from the hosting arrangement. These are asked here
so each answer is obtained once rather than improvised per source.

**Scope note for Part A's counsel (§9.5).** Q7–Q12 are **not part of this
engagement.** They are set out here as context — they describe what the
project intends to do, which bears on Q1 and Q5 — and are going to separate
IP/media counsel later. Answer them only if something in them is obviously
wrong or obviously relevant to Part A; the project does not expect it and is
not asking to be charged for it.

### Q7 — Preservation-only copying, and the database right
The project's rights vocabulary separates **may preserve** from **may
display** from **may redistribute**, per source. Much of what it wants to
recover would be preserved and never displayed.

(a) Under French copyright law's archiving, research and related exceptions,
may the project copy third-party web content wholesale into a **non-public**
archive, where no public display is made? (The project is aware that France
operates a statutory web-legal-deposit regime through designated
institutions; it is **not** claiming to be one, and asks only whether that
regime's existence bears on what a private archive may do.)

(b) The sanctions lists in §3.1 are copied **whole**, as datasets. Does the
**sui generis database right, as implemented in French law**, restrict that,
and does any exception cover it? This is not hypothetical: the project's registry currently records the EU
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
in France** — as contract, as a signal bearing on
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

### Q12 — The hosting arrangement
The controller is established in France; the archive server is hosted with
IONOS in Spain. Both are inside the EEA, so the project does not believe a
Chapter V transfer question arises on these facts, and says so here rather
than asking counsel to rule out a non-issue at cost. What it does ask:

(a) Is that right — does hosting in another member state raise anything the
project has not thought of, including whether renting servers in Spain
creates an establishment there or affects which authority is competent?

(b) The project will separately confirm that an **Art. 28 processor
contract** is in place with the correct IONOS contracting entity, and what it
says about sub-processors and support access from outside the EEA. Is there
anything beyond a standard DPA that this particular archive should insist on
— given §3.2's content and the confidential store described in §3.4?

(c) Does any of this change if the project later incorporates, or moves the
server?

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
revised to match it**. That has three consequences for how counsel's advice
is delivered.

1. **The project needs a written answer it can quote and cite, question by
   question.** An advice note structured against **Q1–Q6** — even where the
   answer to one is "this does not arise" — is worth considerably more to the
   project than a discursive memorandum, because the outcome is entered into
   a permanent decision record and the reasoning has to survive being read in
   ten years by someone who was not in the room. (Q7–Q12 are out of scope for
   this engagement; see §6's scope note and §9.5.)
2. **Each answer is asked to cover both states in §3.5, and to name the
   deltas.** For each of Q1–Q6: what is the position for **State 1** (the
   project as it is today), what is it for **State 2** (as intended), **which
   conclusions differ**, and — where they differ — **on what trigger**, and
   what would have to be true for the State 2 answer to hold. Where the
   answer is the same for both, saying so plainly is a useful answer and the
   project would rather have it than have the question left open.

   This is not a request for two opinions. It is a request that the single
   opinion be explicit about which of its conclusions are contingent on
   facts that will change, because those triggers become the project's
   POL-0001 §11 review triggers, and it would otherwise be guessing at them.

3. **Where counsel's conclusion differs from a position in §4, the project
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
see §12, item 1.

---

## 9. What the founder must settle before this is sent

Five blanks. **All five are now closed.** Each is recorded below with the
ruling and its date; none was decided by inference. What remains before the
brief is sent is not a decision — see §1's caution on Légifrance, and the
covering letter §1 describes.

### 9.1–9.3 Establishment jurisdiction, controller, hosting — **closed**
**These three facts are not decided in this brief.** They are decided in
[`DR-0100`](../decision-records/DR-0100-jurisdiction-controller-and-hosting.md)
(approved 2026-09-15), and this brief is filled *from* that record rather
than the other way round:

- **Establishment jurisdiction: France.** The framework is the GDPR as
  applied in France plus the LIL; the expected supervisory authority is the
  CNIL.
- **Controller: the founder/principal editor as a natural person.** No legal
  entity exists. **Counsel must be told that incorporation is contemplated**,
  so the advice is not answering a question the project may stop asking.
- **Hosting: IONOS, Spain.** Both ends inside the EEA — see Q12.

All three go in the covering letter as well as here.

### 9.4 As it is, or as it intends to be — **closed 2026-09-15: both, staged**
Ruled by the founder: counsel answers **for both states, and names the
deltas** — which conclusions differ between them, on what trigger, and what
would have to be true for the later answer to hold. The two states are
defined at §3.5 and the requirement is carried into §8.

The reasoning recorded with the ruling: counsel must understand the current
state anyway in order to advise on the intended one, so the marginal cost is
the mapping rather than the analysis; the deltas are exactly what POL-0001
§11's "material change" trigger needs and the project would otherwise be
guessing at them; and answers that fall along the preserve/structure/publish
seams match how decisions actually reach the founder. Q2's Article 46
question in particular is fragile as a single snapshot — whether the project
publishes, and how it holds itself out, may be load-bearing for whether it
can lawfully structure its core material at all.

### 9.5 One engagement or two — **closed 2026-09-15: two**
Ruled by the founder: **Part A goes to French data-protection counsel now.
Part B is held**, to go to IP/media counsel later. The reasoning recorded
with the ruling: POL-0001 §10 requires its six topics answered as one body of
advice by one adviser, and splitting Part A would fragment the single record
CDR-P3-44 needs; Part B is different expertise, and it governs acquisition
steps the project cannot take until Part A is answered anyway.

**What that means for what is sent.** The whole brief goes to Part A's
counsel, Part B included, with Part B marked as **context rather than
instructions** — it tells them what the project actually plans to do, which
bears on Q1 and Q5, and a data-protection view on any of it is welcome
without being expected or charged for. Part B is not withdrawn from the
document; it is withdrawn from the retainer. §6's preamble says so in terms.
If the founder prefers Part B excised from the sent copy instead, that is a
one-line change here.

---

## 10. Materials to supply with the brief

Counsel should not be sent the repository. The proposed enclosure set:

1. POL-0001 (the personal data policy) in full — it is the thing being tested.
2. This brief.
3. The source registry entries for the two registered sources, showing the
   recorded rights positions and their "NOT LEGALLY REVIEWED" markers.
4. A one-page description of the three-gate pipeline and the access tiers
   (§2 and §3.4 of this brief serve, if a standalone page is not wanted).
5. The **IONOS processor contract / DPA**, for Q12 — or a note saying which
   contracting entity it is with if the document itself is not to hand.
6. On request: the decision records governing quarantine, retention tiers,
   governed redaction, and third-party captures.

Not enclosed: the Phase I requirements record (long, and mostly about
evidentiary method rather than anything counsel needs) and any material held
above `public` access tier.

---

## 11. Candidate Decision Records

Numbering runs CDR-P3-43…45. It originally ran 42…44; a parallel session's
WP 3.6 (WACZ evaluation) had independently taken **CDR-P3-42** on the same
day, and this line of work renumbered because WP 3.6's claim is the older.
DR-0095 prevents this for DR numbers and does not reach CDR numbers.
**Two of the three are discharged**, both on 2026-09-15, into decision
records of their own; they are kept here struck through because a spent CDR
number is not reused. **Only CDR-P3-45 is still a proposal**, and it is held
with a named trigger rather than open-ended.

- **CDR-P3-43 — ~~The establishment jurisdiction and the controller's
  identity are recorded before the review is commissioned.~~ Discharged
  2026-09-15.** The founder ruled the same day this brief was drafted, and
  the proposal became
  [`DR-0100`](../decision-records/DR-0100-jurisdiction-controller-and-hosting.md),
  which is where these facts now live. That record is a **draft**: its shape
  is ruled, its jurisdiction and hosting-location fields are still blank, and
  it is not approvable until they are filled. Kept here, struck through,
  because the CDR number is spent and should not be reused.

- **CDR-P3-44 — ~~What "the review's outcome is recorded" means.~~
  Discharged 2026-09-15.** Ruled the same day it was raised, and enacted as
  [`DR-0101`](../decision-records/DR-0101-recording-the-legal-review.md),
  which is where it now lives. In short: the review is recorded by a Decision
  Record superseding DR-0072 that carries POL-0001 to v2.0 in the same act;
  **§9's releases take effect on that record's approval and not before**;
  **§10 is discharged by Part A alone**, with Part B's answers recorded
  separately and moving neither DR-0072 nor LEGAL-009 while still gating
  Q8/Q9/Q10's acquisition steps; the §3.5 deltas are recorded as named
  POL-0001 §11 triggers rather than prose; and a failed or partial review is
  itself recorded, as a record that supersedes nothing. Kept here, struck
  through, because the CDR number is spent and should not be reused.

- **CDR-P3-45 — A rights position marked unreviewed cannot reach Gate 3.**
  **Held, deliberately** (founder ruling 2026-09-15): still a candidate, with
  a named trigger — **the start of Gate 3 work**. It is not urgent and does
  not become so before then: nothing is published and Gate 3 has never run.
  Its fix touches the schema, `publication/gate3.py` and a test suite that
  must be shown to fail, which is work worth scheduling rather than bolting
  on. The gap itself, so it is not rediscovered from scratch:
  the source registry's `rights_basis` is free text, and the two registered
  sources carry `may-redistribute` on a basis whose own text says "NOT
  LEGALLY REVIEWED". Nothing in the schema or the publication gate prevents a
  publication decision from resting on it. The proposal: rights review state
  becomes a declared field rather than a marker buried in prose, and Gate 3
  refuses a publication whose rights basis is unreviewed, in the database and
  in the code both. It is a real gap rather than a hypothetical one — found
  by reading the code, not imagined — which is why it is held with a trigger
  rather than dropped.

---

## 12. Open questions raised

1. **The status of counsel's advice itself.** Privileged, restricted,
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
