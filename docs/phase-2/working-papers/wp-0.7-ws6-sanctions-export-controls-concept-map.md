# Phase II / Workstream 6 — Sanctions & Export-Control Concept Map
## Working Paper 0.7

**Project:** Ukraine's Second War of Independence
**Status:** CANDIDATE — AI-drafted, awaiting founder review and approval. Nothing in this paper is canonical.
**Version:** 0.7 (first draft of Workstream 6)
**Mandate:** WP 0.1 research sequence item 6 — authoritative legal structures and datasets; the ownership/control and sovereignty assignments made by DR-0015.
**Constraints inherited:** DR-0012 (identity as events), DR-0014 (type vs item), DR-0015 (layer assignment), DR-0024 (epistemic layers), DR-0030 (quantity semantics); record §3, §62–§73.

### AI provenance (per Phase I record §80)

| Field | Value |
|---|---|
| Drafted by | AI assistant (Anthropic Claude Code agent session), continuing the founder-directed workstream sequence |
| Date | 2026-08-11 |
| Inputs | Phase I record (§3, §62–§73 centrally); WP 0.1–0.6; DR-0001…0037 |
| Human review | **Pending** — founder is final editor (record §78) |
| Disposition | Candidate working paper; all candidate Decision Records herein are proposals |

---

## 1. Scope and method

This workstream grounds the sanctions/export-control layer in **actual legal
structures** — UN, EU, US, UK primarily — and in the **established data models**
of the ecosystem, per the record's §64 command that sanctions are never a
boolean and DR-0015's assignment of ownership/control modeling here. The method:
map the legal reality first (what kinds of legal objects exist and how they
change), then the data models available to express it, then compose candidate
structures and DRs.

## 2. The legal reality — what must be representable

### 2.1 The instrument hierarchy

Every major regime shares a layered legal shape, with jurisdiction-specific
names:

| Layer | UN | EU | US | UK |
|---|---|---|---|---|
| Enabling authority | UN Charter Ch. VII | TEU Art. 29 / TFEU Art. 215 | IEEPA, other statutes | SAMLA 2018 |
| Regime/program | Security Council sanctions regime (e.g., the 1518/2014-lineage measures) | Council Decision + Regulation pair per regime (e.g., 269/2014, 833/2014) | Executive Orders + CFR program (e.g., E.O. 14024; Ukraine-/Russia-related programs) | Statutory instrument (e.g., Russia (Sanctions) (EU Exit) Regulations 2019) |
| Measure/effect | Asset freeze, travel ban, embargo articles | Article-level prohibitions (asset freeze, sectoral, trade, services) | Blocking, sectoral (directives), trade restrictions | Asset freeze, trade, transport, services |
| Designation act | Committee listing | Implementing Regulation amending an annex | OFAC SDN/non-SDN listing action | OFSI designation |
| Consolidated list entry | UN Consolidated List | EU Consolidated Financial Sanctions List | SDN + other lists | UK Sanctions List / OFSI Consolidated List |

The record's §64 lifecycle (amendment, suspension, expiry, delisting,
annulment, redesignation, legal challenge, judgment, replacement) is real in
every jurisdiction — EU annulments by the General Court followed by immediate
redesignation under a modified rationale are a recurring pattern and the
sharpest test case: the *person* did not change; the *legal state* cycled
through designation → annulment → redesignation, and each state has dates,
instruments, and grounds.

### 2.2 Effects are not designations

§73's distinction is legally exact:

- **Designation** — a named listing act by an authority against a subject.
- **Direct legal effect** — the prohibitions the instrument attaches to
  designation (asset freeze; prohibition to make funds available).
- **Rule-derived effect** — restrictions reaching *undesignated* parties
  through rules: the **OFAC 50 Percent Rule** (entities owned 50%+ in
  aggregate by blocked persons are blocked without being listed) and the
  **EU ownership/control criteria** (ownership >50% or control indicators).
- **Sectoral/activity effects** — restrictions attaching to categories
  (sectors, goods, services, vessels) rather than named subjects.

"Subject to restrictions" therefore decomposes into *why*, *under which
instrument*, *in which jurisdiction*, *during which period*, and — for
rule-derived cases — *via which ownership/control path computed under which
rule version* (§71).

### 2.3 Export controls

Parallel but distinct machinery: **classification** of items (US ECCN under
the EAR; EU dual-use annexes under Regulation 2021/821; national lists;
Wassenaar and other multilateral lists upstream), **licensing** (requirements,
general licenses/exceptions, denials, revocations), **end-user/end-use
controls** (entity lists, military end-user rules), and the war-specific
**Common High Priority List** of battlefield goods. §65's ladder — "license
required" ≠ "license absent" ≠ "violation established" — matches the legal
structure exactly: requirement flows from classification + destination +
end-use; authorization is a separate fact; violation is a legal finding (§62).

### 2.4 Enforcement

Enforcement actions (§3) — OFAC settlements and penalties, BIS denial orders,
EU member-state prosecutions, UK OFSI penalties, indictments, seizures,
forfeitures — are legal events by authorities against subjects, each with
documents, findings, and outcomes. They are evidence *both* about the subject's
conduct *and* about enforcement practice; the epistemic layering (DR-0024)
handles the difference between an allegation in an indictment and a finding in
a judgment (§63).

## 3. The data-model ecosystem

| Model / source | What it is | Fit |
|---|---|---|
| **OpenSanctions / FollowTheMoney (FtM)** | Open schema + aggregated dataset: entities (Person, Company, Vessel…), `Sanction` as an interval object linking entity/authority/program with start/end, rich per-source provenance, consolidated deduplication | The de-facto interchange standard of the investigative ecosystem; strong external-identifier spine (§16); **not** built to carry full instrument lifecycle or rule-derived effects |
| **BODS (Beneficial Ownership Data Standard, Open Ownership)** | **Statement-based** ownership data: ownership-or-control statements with interest types (shareholding, voting, appointment rights…), percentages, dates, sources, and statement provenance | Structurally aligned with the project's assertion model — BODS chose statements-with-provenance for exactly the record's reasons; the natural pattern for §19–20 |
| **GLEIF / LEI + relationship records** | Global legal-entity identifiers with direct/ultimate accounting-consolidation parent relationships | Authoritative identifier + a *specific, narrow* control notion (accounting consolidation) — valuable, not to be conflated with §19's broader control senses |
| **National corporate registries / ISO 20275 (entity legal forms)** | Primary-source incorporation data; standardized legal-form codes | Primary evidence for corporate events (§20); registry assertions remain documentary (§32) |
| **Classification systems: HS/CN, ECCN, national lists** | Goods nomenclatures and control lists | §66: classification is system+jurisdiction+time contextual; codes attach to product types (DR-0014) |
| **Trade data: customs records, UN Comtrade; transport: IMO/MMSI, AIS** | Declared trade flows; vessel identity and movement | §67–69: declarations documentary; AIS is a machine observation with spoofing risk (§49) |

Key negative finding, mirroring WP 0.3's: **no single model covers the legal
layer.** FtM covers interchange and identity; BODS covers ownership
statements; none carries instrument lifecycle, rule-derived applicability, or
license state. The legal-temporal core must be composed by the project — on
established patterns, with mappings out.

## 4. Composition (candidate)

- **Legal instruments and regimes** are first-class documentary-legal objects
  (works/expressions in the LRMoo sense where texts matter, DR-0011) with
  authority, jurisdiction, legal basis, effective periods, amendment lineage.
- **Designations** are records: acts by an authority under an instrument
  against a *designation subject* (name, identifiers, stated rationale as an
  authority-attributed assertion, §64). Designation→canonical-entity mapping is
  an evidence-backed identity assertion (DR-0012; §72) — the sanctions-list
  entry and the person are never the same object.
- **Effects** are typed legal relations derived from instrument + designation
  (or instrument + category), with validity periods; **rule-derived
  applicability** (50% rule, EU control criteria) is a *computed assertion*
  carrying ownership path, source percentages (DR-0030), rule + rule version,
  jurisdiction, computation date, and software version (§71) — stored as
  derived data (DR-0003), never as a designation.
- **Ownership/control** follows the **BODS statement pattern**: typed
  interest statements (legal ownership, beneficial ownership, voting rights,
  board control, contractual control, nominee arrangements — §19) with
  percentages as quantity objects, validity periods, and full provenance;
  GLEIF relationships and registry filings enter as documentary sources for
  such statements.
- **Export-control state** decomposes per §65: classification assertions
  (system, jurisdiction, authority, period; official vs declared vs
  project-analytical, §66) on product types (DR-0014); licensing requirements
  as rule-derived assertions; licenses/denials/exceptions as legal acts;
  violations only as legal findings (§62).
- **Trade events** keep the §68 triad: transaction (commercial), shipment
  (physical, with §69 legs), payment (financial) — distinct events, linkable,
  never merged; customs declarations are documentary assertions about them
  (§67).
- **Sovereignty/occupation** (the DR-0015 joint item): territorial-control
  statuses — sovereignty claim, international recognition, administration,
  occupation, de facto control — are modeled as **typed, evidence-backed
  temporal relations grounded in period phenomena** (the CRM E4 pattern),
  authority-attributed where they are legal characterizations (a UN GA
  resolution's non-recognition is an authority assertion, §62).

## 5. Candidate conflict-register entries (additions)

| Term | Colliding senses | Resolution direction (candidate) |
|---|---|---|
| **sanctioned** | Colloquial catch-all vs designation vs subject-to-effects vs rule-derived applicability | The word never appears as a bare status; always decomposed (§73) |
| **designation** | Listing act vs the list entry vs the designated person | Act / record / entity are three objects (DR-0012) |
| **control** | Corporate control (§19) vs territorial control (§46) vs export control | Always qualified; three registry entries |
| **license** | Export license (§65) vs content/rights license (§14, DR-0002 rights) | "Export license" vs "rights license" spelled out |
| **program** | Sanctions program/regime vs software program | Regime preferred for the legal sense |
| **list** | Legal consolidated list vs any enumeration | "Sanctions list" reserved for authority-published lists |
| **owner** | Legal / beneficial / registered / nominee / colloquial | Never bare; BODS interest types govern |

## 6. Candidate Decision Records (proposals only — require founder approval)

- **CDR-W6-1:** **Sanctions are modeled as legal instruments, regimes,
  designations, and effects with full lifecycle** (authority, jurisdiction,
  legal basis, effective periods, amendment, suspension, expiry, delisting,
  annulment, redesignation, challenge, judgment, replacement — §64). No boolean
  `sanctioned` property exists anywhere in the system.
- **CDR-W6-2:** **Designation records are documentary objects distinct from
  canonical entities**; designation→entity mapping is an evidence-backed
  identity assertion under DR-0012, with candidate/confirmed/rejected states
  and authority-correction history (§72). Authority rationales remain
  authority-attributed assertions unless independently established (§64).
- **CDR-W6-3:** **Ownership and control follow the BODS statement pattern:**
  typed interest statements with quantity-object percentages (DR-0030),
  validity periods, and provenance; GLEIF, registries, and filings enter as
  documentary sources. Legal ownership, beneficial ownership, voting rights,
  and the control variants of §19 are distinct interest types, never merged.
- **CDR-W6-4:** **Rule-derived applicability is computed, versioned, and
  never stored as designation:** 50-percent-rule and EU-control conclusions are
  derived assertions carrying ownership path, source statements, rule and rule
  version, jurisdiction, date, and software version (§71, §73), with the
  epistemic status of their inputs propagating (DR-0024).
- **CDR-W6-5:** **Export-control state is decomposed** per §65–66:
  classification assertions are contextual (system, jurisdiction, authority,
  validity period; official/declared/analytical distinguished) and attach to
  product types (DR-0014); licensing requirements, authorizations, denials,
  exceptions, and revocations are separate legal facts; violations exist only
  as legal findings (§62).
- **CDR-W6-6:** **The transaction / shipment / payment triad** (§68) is
  adopted: three distinct event types with their own participants and
  evidence, linkable into trade networks; customs and trade declarations are
  documentary assertions (§67) bridged to project conclusions only through
  evidence relations.
- **CDR-W6-7:** **Territorial-status vocabulary** (fulfilling DR-0015's joint
  item): sovereignty claim, recognition, administration, occupation, and de
  facto control are typed, evidence-backed temporal relations grounded in
  period phenomena; legal characterizations of territory are
  authority-attributed assertions (§62). 
- **CDR-W6-8:** **FollowTheMoney/OpenSanctions is adopted as interchange
  mapping and external-identifier spine** (map-to disposition): the project
  maintains mappings to FtM entity/sanction shapes and consumes OpenSanctions
  identifiers as typed external identifiers (§16, DR-0012); FtM is not the
  canonical internal model.

## 7. Unresolved research questions (feed Phase II output 7)

1. Jurisdiction sequencing: which regimes are modeled first (EU + US + UK +
   UN assumed; Switzerland, others when?) — a collection-policy decision
   (§9), not ontology.
2. Instrument-text acquisition: OJ EU, Federal Register, legislation.gov.uk
   as collectors (§8) — pipeline design, Phase III.
3. Enforcement-action modeling depth (settlements, indictments, seizures):
   which subset is first-class vs documentary-only at start?
4. Cryptocurrency flows (§70): defer confirmed? (Record says do not overbuild
   until investigations require.)
5. FtM mapping mechanics: which project layers export losslessly, which
   degrade (lifecycle → interval flattening), and is the loss acceptable
   per package type?
6. AIS/vessel-tracking spoofing treatment (§49): scheme + critical questions
   for movement evidence (DR-0034's library).
7. Licensing-data availability: license grants/denials are rarely public —
   absence-state discipline (DR-0029) will carry much of this domain.

## 8. Sources

- UN Security Council Consolidated List and committee practice
- EU: TEU Art. 29 / TFEU Art. 215 architecture; Regulations 269/2014 and
  833/2014 lineages; EU Consolidated Financial Sanctions List; General Court
  annulment case-law on listings
- US: IEEPA/E.O. framework (incl. E.O. 14024); OFAC SDN and 50 Percent Rule
  guidance; EAR/ECCN structure; BIS Entity List; Common High Priority List
- UK: SAMLA 2018; Russia (Sanctions) (EU Exit) Regulations 2019; OFSI
  consolidated list and enforcement guidance
- EU Regulation 2021/821 (dual-use); Wassenaar Arrangement lists
- OpenSanctions / FollowTheMoney schema documentation
- Beneficial Ownership Data Standard (Open Ownership)
- GLEIF LEI and relationship (Level 2) data documentation
- ISO 20275 entity legal forms; HS/CN nomenclatures
