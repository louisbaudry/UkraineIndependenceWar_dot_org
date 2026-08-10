# Phase I — Requirements Discovery Record
## Ukraine's Second War of Independence Project

**Status:** Phase I complete  
**Purpose:** Preserve the foundational requirements-discovery decisions that precede architecture and implementation.  
**Next phase:** Phase II — Theoretical Synthesis & Standards Mapping

---

## 1. Project identity and mission

This project is not merely a website containing a database.

> **We are building a durable historical evidence and knowledge repository that happens to publish a website.**

The project is conceived as a long-term historical, documentary, OSINT, preservation, sanctions-evasion, export-control, and research infrastructure focused on Ukraine's struggle for sovereignty and the broader machinery sustaining Russia's war.

The working historical framing is:

> **Ukraine's Second War of Independence**

The project will explicitly distinguish this interpretive framing from established conventional terminology such as:

- Russo-Ukrainian War
- Russia's war against Ukraine
- Russian invasion of Ukraine
- full-scale Russian invasion of Ukraine

The project is independent and non-Ukrainian. It does not claim to speak on behalf of Ukraine or Ukrainian institutions.

The project is explicitly supportive of Ukrainian sovereignty and opposed to Russian imperial domination, while committing itself to rigorous evidentiary standards, transparent methodology, and careful distinctions among source claims, evidence, inference, legal findings, and project conclusions.

The time horizon is measured in years and potentially decades, not weeks.

---

## 2. Core historical scope

The historical narrative must not begin in February 2022.

The intended long chronology includes, as relevant:

- Ukrainian national development before 1917
- 1917–1921 Ukrainian struggle for independent statehood
- Soviet Ukraine
- 1990–1991 sovereignty and independence
- 1991 referendum and international recognition
- post-Soviet Ukraine–Russia relations
- Orange Revolution
- Euromaidan / Revolution of Dignity
- Russian intervention in Crimea and Donbas beginning in 2014
- war in Donbas, 2014–2021
- full-scale invasion from 2022
- occupation, atrocities, deportations, infrastructure attacks, military campaigns
- international support, sanctions, diplomacy, sanctions evasion, export controls
- accountability, prosecutions, reparations, reconstruction, and postwar consequences

The war's final historical endpoint should not be predetermined.

The architecture must allow the wartime corpus eventually to become bounded and versioned while related accountability, sanctions, reparations, and postwar datasets continue independently.

---

## 3. Sanctions-evasion and export-control scope

Sanctions evasion is a first-class domain from the start.

The project should eventually support a progressive evolution:

1. Documentary
2. Investigative
3. Monitoring
4. Professional research/intelligence platform

The architecture should support, as justified by evidence:

- sanctions programs and designations
- legal instruments and legal effects
- amendments, redesignations, suspensions, expiry, delisting, annulment
- rule-derived sanctions applicability
- ownership/control rules
- export controls
- licensing requirements
- authorizations, denials, exemptions, general licenses
- procurement networks
- dual-use goods
- controlled components
- customs/trade data
- transshipment and re-export
- vessels, ports, shipping, shadow fleet
- financial flows
- companies, intermediaries, beneficial owners
- corporate histories
- enforcement actions
- seizures
- indictments
- prosecutions
- court decisions

Sanctions are not a timeless boolean property.

The system must be able to answer questions such as:

> Which legal restrictions applied, under which authority and jurisdiction, to whom, during what period?

and:

> Was an entity directly designated, or merely potentially subject to restrictions through ownership/control rules?

---

## 4. Sustainability and access model

The project will use a multi-tier access model.

The public historical archive remains meaningfully open and free.

Specialized professional datasets and tools may be subscription-funded, including potentially:

- advanced structured datasets
- bulk exports
- enhanced network data
- monitoring
- API access
- historical snapshots
- advanced research tooling
- analytical reports
- intelligence products

The canonical evidence and provenance system remains common to all tiers.

Access rights must not create competing versions of historical truth.

The intended business model is progressive:

**data → tools → analytical/intelligence products**

Subscription revenue may finance the research and preservation work.

---

## 5. Collaboration model

Initial operating model:

- founder/principal editor
- extensive AI assistance
- automated collectors
- later expansion to a small trusted team

The architecture should support:

- defined roles
- attribution
- review history
- auditability
- risk-based editorial workflows

It should not prematurely become a public collaborative encyclopedia platform.

---

## 6. Preservation and evidence philosophy

The project is heavily concerned with data conservation.

The archive should be useful to:

- historians
- archivists
- journalists
- academic researchers
- OSINT investigators
- human-rights researchers
- prosecutors
- criminal investigators
- international criminal-law specialists
- courts and investigative bodies
- future researchers

The project must distinguish:

### Ordinary provenance
Where information came from, how it was acquired, transformed, analyzed, reviewed, and published.

### Legal chain of custody
A stricter evidentiary/legal concept that must never be falsely claimed merely because a file was downloaded, timestamped, hashed, and preserved.

The archive should maximize future evidentiary utility without overstating legal status.

---

## 7. Preservation principles

Foundational decisions:

- preserve raw/original acquired material separately from processed derivatives
- originals are immutable
- hash originals at ingestion
- preserve transformation lineage
- preserve acquisition metadata
- preserve source versions where material changes occur
- preserve deletion/modification history for significant sources
- preserve failed acquisitions where historically significant
- preserve provenance gaps explicitly
- distinguish locally held material from externally referenced material
- distinguish complete originals from fragments, screenshots, transcripts, metadata-only records, etc.
- preserve web captures in richer formats such as WARC for selected high-value sources as the system matures
- introduce periodic fixity checking as the archive grows
- maintain independent backups
- evolve toward geographic/provider redundancy
- distinguish backup, archival preservation, and frozen research releases
- eventually support institutional preservation/deposit for major releases

The archive should be reconstructible even if the public website disappears.

---

## 8. Continuous OSINT collection

The project requires a backend collection system that runs automatically every day.

Potential sources include:

- government websites
- official Russian and Ukrainian sources
- military/security institutions
- international organizations
- news and investigative media
- think tanks
- NGOs
- RSS/Atom
- public social media
- Telegram channels
- public Telegram groups/chats where lawful and appropriate
- YouTube/video sources
- podcasts/transcripts
- archived webpages
- public datasets
- sanctions databases
- court and prosecutor publications

The source list must be configurable.

Collection is conceptually separated into:

1. discovery
2. acquisition
3. preservation
4. normalization
5. enrichment
6. classification
7. editorial review
8. publication

Collection never implies publication.

A conceptual pipeline:

`source registry`
→ `fetch`
→ `raw preservation`
→ `hash`
→ `metadata extraction`
→ `deduplication`
→ `normalization`
→ `language detection`
→ `entity/date/place extraction`
→ `relevance classification`
→ `review queue`
→ `editorial acceptance`
→ `knowledge base`

---

## 9. Retention model

Use multi-stage retention.

Broad raw collection may enter temporary storage and then be classified into:

- discard
- metadata-only
- medium-term retention
- permanent preservation

Collection policy is source-specific.

High-value or fragile sources may receive comprehensive preservation even before item-level relevance is known.

A source can later be escalated to a higher preservation tier and older material may be retrospectively recovered from archives or other datasets.

Do not archive everything equally.

---

## 10. Sensitive and graphic material

Initial policy:

- selectively preserve graphic evidence when historically/evidentially important
- keep it restricted by default
- design the architecture so systematic preservation could be added later without redesign

Public visibility and archival preservation are separate decisions.

---

## 11. Evidence intake from third parties

The project should support controlled evidence intake.

Submitted material is not treated as automatically authentic or correctly contextualized.

The system should support:

- quarantine
- original-file preservation
- malware/security checks
- provenance assessment
- privacy/legal review
- submitter claims kept separate from project conclusions
- confidential attribution
- protected source identity
- pseudonymous source IDs
- granular access controls

Confidential-source identity must be architecturally separable from ordinary research data from the beginning.

---

## 12. Data classification and access

Do not use one universal `is_public` flag.

Keep separate dimensions for:

- publication/access tier
- sensitivity
- rights/licensing
- evidentiary disclosure

Initial access implementation may be simple, but the architecture should support:

- public
- subscriber
- internal
- confidential
- researcher-restricted
- investigator-restricted
- private preservation

Preservation status and access status are separate.

---

## 13. Personal data

Raw material may contain personal information, but unnecessary personal data should not automatically become searchable structured data.

Before broad automated collection, establish a formal personal-data policy covering:

- ordinary civilians
- victims
- witnesses
- minors
- public officials
- combatants
- investigative subjects
- sanctioned persons/entities

Preservation and publication decisions must be distinct.

---

## 14. Rights and licensing

Preservation rights and republication rights are different.

The system should be capable of distinguishing:

- may preserve
- may display
- may redistribute
- may provide to subscribers
- unknown rights

The archive may preserve material it is not permitted to republish publicly.

---

## 15. Stable identity and citation

Stable identifiers are foundational.

The system should support:

- immutable internal IDs
- stable public project identifiers
- permanent resolvable URLs
- external identifier mappings

Do not freeze a custom identifier syntax without researching established patterns first.

Meaningful research objects should be independently citable where appropriate:

- people
- organizations
- events
- assertions
- source captures
- quotations
- investigations
- legal records
- dataset releases

Internal implementation objects do not automatically require public identifiers.

---

## 16. External identifiers

Typed external identifiers should be supported from the beginning.

Examples:

- Wikidata
- OpenSanctions
- official sanctions IDs
- company registration numbers
- tax IDs
- LEIs
- IMO
- MMSI
- aircraft registrations
- official registry IDs

Identifiers are provenance-bearing relationships, not merely timeless fields.

False entity merges are considered higher risk than missed matches.

---

## 17. Entity resolution

Identity resolution is first-class.

The system must support:

- multiple names
- aliases
- historical names
- multilingual names
- transliterations
- account handles
- external identifiers
- candidate matches
- rejected matches
- confirmed matches
- merge history
- split history
- identity lineage

A sanctions-list identity must never be linked to a canonical person/entity through fuzzy name matching alone.

Candidate or merely claimed entities remain distinct from canonical entities.

Fabricated entities, impersonations, and disproved identities should eventually be representable.

---

## 18. Persons, roles, offices, and acting capacity

Roles are temporal relationships, not mutable person attributes.

The system should support:

- role
- organization
- office
- tenure dates
- acting/interim positions
- disputed appointments
- de facto roles
- source provenance

Acting capacity matters.

Association with an organization does not imply that all actions by a person are organizational actions.

Presence, participation, responsibility, and criminal liability are distinct.

---

## 19. Organizations and corporate identity

Distinguish:

- formal organization
- incorporated legal entity
- broader organizational/corporate group
- informal analytical network

Support temporal organizational hierarchy.

Distinguish:

- legal ownership
- direct ownership
- indirect ownership
- beneficial ownership
- voting rights
- managerial control
- contractual control
- de facto control
- nominee ownership
- ultimate beneficial ownership

“Successor to” does not necessarily mean “same legal entity as.”

---

## 20. Corporate history and addresses

Corporate relationships and attributes are temporal.

Support, where relevant:

- incorporation
- dissolution
- renaming
- jurisdiction change
- merger
- ownership transfer
- beneficial-control change
- director history
- address history

Addresses should be typed:

- registered office
- legal domicile
- headquarters
- factory
- warehouse
- branch
- logistics hub
- virtual office
- service-provider address

A registered address is not proof of physical operation.

---

## 21. Physical objects, products, and components

Individually identifiable physical objects may become first-class entities where useful.

Examples:

- vessels
- aircraft
- vehicles
- weapons
- facilities
- buildings
- components
- equipment

Distinguish product/model identity from individual physical item identity.

Support, where evidence justifies:

- serial numbers
- lot numbers
- manufacture
- custody
- shipment history
- seizure/recovery
- photographs
- component identification

---

## 22. Documents, works, files, and representations

The system should not collapse all documentary layers into “a file.”

Where needed, distinguish:

- intellectual work/document
- language/version/expression
- published manifestation
- individual preserved copy
- derivative artifact
- OCR
- transcript
- translation
- screenshot
- excerpt
- reproduction

Use established bibliographic/archival concepts where appropriate.

---

## 23. Authorship and publication

Distinguish:

- stated author
- actual/inferred author
- drafter
- signer
- publisher
- issuing authority

“Signed by X” does not necessarily mean “written by X.”

Original publisher and acquisition source are separate.

Transmission lineage may include reposts, mirrors, forwards, and archives.

---

## 24. Source lifecycle

Important sources may have a lifecycle:

- published
- edited
- deleted
- restored
- redirected
- unavailable
- censored
- blocked
- unsealed
- replaced

For significant sources, preserve source-version history.

The same URL may later serve different content.

---

## 25. Source context

Preserve inexpensive structural context when practical:

- reply chains
- forwards
- nearby posts
- linked material
- thread relationships

Important evidence may have richer contextual packages.

A perfectly preserved but decontextualized quotation can become misleading.

---

## 26. Source completeness and holdings

The system should record what the archive actually possesses:

- original
- archival copy
- derivative
- screenshot
- transcript
- fragment
- metadata-only record

Also distinguish external copies/custodians.

Do not imply possession of a full document when only a partial representation survives.

---

## 27. Source accessibility

Accessibility is distinct from evidentiary value.

Possible states include:

- public
- paywalled
- restricted
- deleted
- archived
- licensed
- internally preserved

Accessibility may change over time.

---

## 28. Discovery and acquisition provenance

Record where feasible:

- discovery origin
- whether discovered automatically/manual
- whether learned through another investigation
- acquisition source
- original publisher
- acquisition attempts
- failures
- retries
- later success
- permanent loss

A failed acquisition can itself become historically important.

---

## 29. Evidence vs source vs claim

The conceptual distinction is foundational.

A source object may exist in the archive without being selected as evidence for any particular proposition.

Explicit source→assertion evidence relationships should be modeled.

Being in the corpus does not mean being evidentially used.

---

## 30. Epistemic vocabulary

A small formal epistemic vocabulary should be established early and expanded only when real cases require it.

Provisional categories include:

- observation
- claim
- assessment
- hypothesis
- finding
- project conclusion

Propositions should preserve:

- who asserts them
- when
- on what basis
- their epistemic status
- supporting/contradicting evidence
- later revisions

---

## 31. Provisional epistemic architecture

Working hypothesis for Phase II study:

1. **World entities/events** — what the knowledge system is about
2. **Source assertions** — what sources say
3. **Evidence objects/observations** — what bears on assertions
4. **Project assertions/conclusions** — what the project concludes
5. **Epistemic assessments** — uncertainty/status/verification attached to assertions
6. **Arguments/inferences** — how evidence supports or attacks conclusions

This is provisional and must be tested against established theory before ontology design.

---

## 32. Documentary facts vs world assertions

“The source says X” and “X is true” are different propositions.

The system should be able to preserve:

- documentary assertions
- world assertions
- evidentiary bridges between them

This is especially important for:

- propaganda
- official statements
- sanctions rationales
- corporate registries
- customs declarations
- wartime claims

---

## 33. Historical record vs project synthesis

The archive should preserve both:

1. what actors/sources claimed
2. what the project currently concludes

Project conclusions are explicit editorial outputs, not raw historical facts.

Consequential conclusions should eventually preserve full editorial provenance.

---

## 34. Evidence and inference

Direct evidence and inferential support must be distinct.

Cross-dataset joins produce derived assertions, not source-provided facts.

Important analytical conclusions should eventually preserve inference chains.

Formal argument/inference representation requires Phase II theoretical research before implementation.

---

## 35. Competing hypotheses

The research layer should support competing explanations.

For important investigations, preserve:

- hypothesis
- supporting evidence
- contradicting evidence
- alternative explanation
- discriminating evidence
- analyst assessment
- revisions

Avoid confirmation bias by design.

---

## 36. Source independence

Source dependence must be explicit where consequential.

Possible relationships:

- cites
- reposts
- syndicates
- derives from
- shares underlying document
- shares underlying witness
- common evidentiary origin

Five publications repeating one original report are not five independent confirmations.

---

## 37. Source reputation

Do not implement universal source-reliability scores.

Source reputation may influence:

- triage
- scrutiny
- review priority

It must not automatically determine proposition truth.

A propaganda outlet can publish an authentic document.
A reputable institution can make an error.

---

## 38. Authenticity, integrity, originality, and veracity

These are distinct.

The system should distinguish:

- authenticity of the object
- integrity of the preserved copy
- attribution/authorship
- originality
- representation lineage
- contextual integrity
- veracity of contained propositions

An authentic source may contain false claims.

An authentic image may be attached to a false context.

The earliest copy held by the project is not necessarily the original.

---

## 39. Contextual assertions

Date, location, depicted event, participants, and circumstances are evidence-backed contextual assertions.

Source-supplied context, inherited/reposted context, project-established context, and conflicting context should remain distinguishable.

---

## 40. Uncertainty and disagreement

Do not collapse all uncertainty into one field.

Distinguish:

- measurement uncertainty
- source uncertainty
- source disagreement
- analytical uncertainty
- unresolved contradiction

Do not average contradictions into false consensus.

---

## 41. Unknown vs no

A missing value must never silently mean “no.”

Potential absence states include:

- unknown
- not researched
- no evidence found
- unavailable
- withheld
- redacted
- lost/destroyed
- not applicable
- genuinely indeterminate

Explicit negative assertions require provenance.

---

## 42. Confidence, probability, and estimative language

Do not invent numeric confidence semantics prematurely.

Phase II should research established approaches from:

- intelligence analysis
- forecasting
- statistics
- scientific uncertainty
- evidence assessment

Probability and confidence are conceptually distinct.

The project should resist false precision.

---

## 43. Precision and accuracy

Representational precision and real-world accuracy are different.

Preserve:

- original expression
- significant figures/resolution
- uncertainty
- derivation method
- normalized value where useful

More decimal places do not mean more knowledge.

---

## 44. Quantitative assertions

Preserve original semantics:

- exact
- approximate
- at least
- at most
- range
- greater than
- fewer than

“At least 17” must never become “exactly 17.”

Normalized values are derived data and must not overwrite the original expression.

---

## 45. Temporal model

The architecture should support, where relevant:

- event time
- publication time
- creation time
- acquisition time
- discovery time
- verification time
- editorial acceptance time
- publication time
- legal effective time
- relationship validity periods
- approximate dates
- date ranges
- conflicting date assertions

Document date and described-event date are distinct.

Evidence may exist before it becomes publicly known.

---

## 46. Geographic model

Distinguish geographic identity from geometry.

Places can have:

- multilingual names
- historical names
- stable identity
- multiple/temporal geometries

Locations may have:

- exact coordinates
- approximate coordinates
- uncertainty radius
- area geometry
- route geometry
- source-derived vs analyst-derived location

Sovereignty, territorial claim, administration, occupation, and de facto control are separate relationships.

---

## 47. Events, processes, and campaigns

Distinguish:

- bounded events
- extended processes
- campaigns
- operations
- phases
- parent/child event structures

Typed event relationships may include:

- before
- after
- part_of
- response_to
- continuation_of
- same_underlying_event_as

Causation must never be inferred merely from chronology.

---

## 48. Observations

Observations are first-class research objects where useful.

Examples:

- satellite observation
- AIS position
- photograph
- eyewitness observation
- registry observation

Negative observation must be handled carefully.

“We did not observe X” is not automatically “X was absent.”

---

## 49. Machine observations

Machine-generated observations are a distinct evidence type.

Potential metadata:

- system/provider
- acquisition method
- timestamp precision
- measurement uncertainty
- processing
- spoofing/manipulation risk
- missing observations
- validation against independent evidence

Machine-generated does not mean objective or correct.

---

## 50. Derived measurements

Raw observations and derived analytical measurements remain separate.

A derived result should preserve:

- input
- method/tool
- parameters
- analyst/software
- timestamp
- uncertainty

Every derived object should be able to answer:

> What was I derived from?

---

## 51. Actions, attempts, plans, and outcomes

Distinguish:

- plan
- order/directive
- preparation
- attempt
- execution
- outcome
- failure
- blocking/intervention
- cancellation
- retry

An order is evidence of a directive, not necessarily execution.

Attempted sanctions evasion is not equivalent to successful sanctions evasion.

---

## 52. Capability, opportunity, intent, action, and responsibility

These are separate propositions.

Where relevant, distinguish:

- capability
- access/opportunity
- knowledge
- awareness
- belief
- intent
- purpose
- motive
- preparation
- attempt
- execution
- outcome
- attribution
- responsibility
- legal liability

Could have done it ≠ intended to do it ≠ attempted it ≠ did it ≠ legally responsible.

---

## 53. Misinformation/disinformation

Do not call every false statement “disinformation.”

Distinguish:

- falsehood
- misleading framing
- error
- negligence/recklessness
- knowing dissemination
- coordinated deception
- attributed influence operation

Deceptive intent requires its own evidence.

---

## 54. Propaganda corpus

The archive should preserve historically significant propaganda and falsehoods.

A false statement may be poor evidence for the proposition it asserts while being excellent primary evidence for what the speaker/publication claimed.

The architecture should eventually support:

- narrative origin
- amplifiers
- variants
- languages
- target audiences
- supporting media
- debunks/counter-evidence
- persistence/disappearance
- propagation indicators

---

## 55. Social-media metrics

Capture inexpensive engagement metadata at acquisition where available.

Do not initially build continuous social-media analytics.

Richer propagation/time-series analysis can be added selectively later.

---

## 56. Coordination analysis

Observable behavioral similarity is not itself proof of coordination.

The system may eventually support:

- synchronized posting
- identical text/media
- forwarding patterns
- shared URLs
- infrastructure overlap
- coordination hypotheses
- state/influence attribution as a distinct evidentiary layer

---

## 57. Corpus coverage and bias

Preserve:

- source scope
- source counts
- language scope
- jurisdiction scope
- collector start/end dates
- outages
- exclusions
- sampling rules
- known coverage gaps

Frequency in the archive is not automatically frequency in the world.

---

## 58. Translation and language

Original-language material is primary.

Translations are derived scholarly objects.

Preserve, where relevant:

- original language
- translation language
- translator/provider
- human vs machine
- review status
- translation version
- source version translated
- parallel translations
- translator notes
- passage-level language

Quotation, paraphrase, and summary must remain distinct.

---

## 59. Full textual provenance for quotations

For important quotations preserve where possible:

- exact original-language passage
- exact source version
- page/paragraph/timecode/offset
- translation
- transcription/OCR origin
- editorial context
- omissions

Do not manufacture quotations from paraphrases.

---

## 60. Project terminology governance

Canonical semantics and user-facing wording are separate.

The project should maintain concept-oriented multilingual terminology governance.

Each important concept may have:

- canonical identifier
- preferred term per language
- synonyms
- definition
- forbidden/misleading translations
- usage notes
- provenance
- version history

Translation memory does not establish terminological authority.

---

## 61. Canonical semantics vs presentation

Meaning belongs to the knowledge model.

Wording belongs to the presentation layer.

APIs/datasets expose stable semantic identifiers.

Websites/apps generate multilingual labels and contextual wording from versioned presentation/localization resources.

---

## 62. Legal findings vs historical findings

Judicial findings, sanctions designations, administrative findings, historical assessments, and project conclusions remain distinct.

Where relevant preserve:

- jurisdiction
- authority
- standard of proof
- procedural posture
- appeal status

“Not proven guilty” is not the same as “historically established not to have done it.”

---

## 63. Legal classifications over time

Legal characterization is temporal and authority-specific.

Possible lifecycle:

- allegation
- investigation
- charge
- indictment
- trial
- judgment
- appeal
- conviction
- acquittal
- administrative finding
- sanctions designation

Do not retrospectively rewrite earlier epistemic states.

---

## 64. Sanctions legal model

Sanctions should be modeled as legal instruments/regimes, not as a boolean field.

Support:

- authority
- jurisdiction
- program/regime
- legal instrument
- designation
- rationale
- effect
- effective dates
- amendment
- suspension
- expiry
- delisting
- annulment
- redesignation
- legal challenge
- judgment
- replacement measure

A sanctions authority's rationale remains an authority-attributed assertion unless independently established by the project.

---

## 65. Export controls and licensing

Export controls are first-class.

Distinguish:

- product identity
- regulatory classification
- legal restriction
- licensing requirement
- actual license/authorization
- exemption
- denial
- revocation
- uncertainty about authorization

“License required” ≠ “license absent” ≠ “violation established.”

---

## 66. Regulatory classification

A product's regulatory classification is contextual.

Possible systems:

- HS
- CN
- ECCN
- EU dual-use classifications
- national export-control regimes

Classification should preserve:

- system
- jurisdiction
- source/authority
- validity period
- official vs declared vs project analytical classification

---

## 67. Trade declarations vs actual trade

Customs declarations are documentary assertions.

Preserve declared:

- exporter
- importer/consignee
- commodity
- value
- origin
- destination
- classification

Keep separate from project conclusions about:

- actual goods
- actual destination
- actual end user
- misclassification
- false consignee
- undervaluation
- transshipment

---

## 68. Transactions, shipments, payments

These are separate first-class concepts.

A commercial transaction, a payment, and a physical shipment are different events.

Support progressively:

- orders
- invoices
- payments
- exporters/importers
- consignors/consignees
- goods
- quantities
- routes
- carriers
- vessels
- ports
- customs declarations
- financial institutions
- intermediaries

---

## 69. Logistics

Shipment movement legs and reusable analytical routes/corridors are distinct.

Support progressively:

- origin
- destination
- intermediate points
- mode
- carrier
- dates
- customs events
- ports
- border crossings
- transshipment
- route variants
- observed vs inferred legs

---

## 70. Financial flows

Payments are independent events.

Potential future structure:

- payer/payee
- account/wallet
- institution
- amount
- currency
- payment method
- intermediary
- fees
- partial payments
- refunds
- conversions
- cryptocurrency
- inferred links to transactions

Do not overbuild this until investigations require it.

---

## 71. Ownership calculations

Reported ownership percentages and project-calculated interests are separate.

Derived ownership should preserve:

- ownership path
- source percentages
- calculation method
- date
- legal/regulatory rule if relevant
- software/version
- uncertainty

Economic-interest calculations do not automatically establish legal control.

---

## 72. Sanctions identity resolution

Designation records exist independently from canonical entities.

Designation→entity mapping is an evidence-backed identity assertion.

Support:

- candidate matches
- rejected matches
- aliases
- DOBs
- addresses
- identifiers
- authority corrections
- delistings
- later merge/split history

---

## 73. Sanctions effects

Distinguish:

- designation
- legal effect
- rule-derived effect
- ownership/control-derived applicability

“Subject to sanctions restrictions” does not necessarily mean “named on a sanctions list.”

---

## 74. Research notebooks and dossiers

Start with private research notes.

Architect toward:

- structured research questions
- hypotheses
- negative findings
- unresolved issues
- analyst reasoning
- collections
- dossiers
- versioned dossiers
- evidence bundles
- exportable research packages

---

## 75. Research gaps

Explicit research questions should be supported.

Eventually include:

- question
- priority
- importance
- evidentiary requirement
- attempted research
- negative findings
- assigned researcher
- resolution status

The archive should know not only what it knows, but what remains unresolved.

---

## 76. Negative research findings

Preserve consequential negative research.

“We searched and found insufficient evidence” is not equivalent to “we proved non-occurrence.”

Substantial negative investigations should preserve scope and methodology.

---

## 77. Corrections and retractions

Do not silently overwrite substantive mistakes.

Support:

- correction
- retraction
- supersession
- merge
- split
- legal restriction
- privacy removal
- archival withdrawal

Substantive corrections should include:

- rationale
- supporting evidence
- editor/reviewer
- effect on published outputs

Being wrong and correcting the record should leave a trace.

---

## 78. Editorial approval

Initial model:

- founder remains final editor

Future model:

- risk-based review
- ordinary claims: lighter review
- higher-risk claims: stronger review
- highest-risk claims: independent reassessment where appropriate

The more consequential the claim, the stronger the evidence and review required.

---

## 79. Human accountability and AI

AI may:

- collect
- extract
- translate
- classify
- summarize
- propose assertions
- propose entity matches
- propose relationships

AI must not silently become canonical knowledge.

Low-risk factual enrichment may be automated under defined controls.

Consequential project conclusions require human accountability.

---

## 80. AI provenance

Consequential AI outputs should preserve:

- provider/model
- model/version where available
- instructions/prompt
- input references
- output
- pipeline version
- structured-output schema
- validation
- reviewer
- disposition
- downstream assertions influenced

Routine disposable model calls need not be preserved forever.

---

## 81. Verification and validation

Do not use one ambiguous `verified` flag.

Distinguish:

- extraction verification
- copy integrity verification
- source authenticity
- semantic validation
- analytical review
- proposition truth assessment

“We copied the source correctly” ≠ “we interpreted it correctly” ≠ “the underlying claim is true.”

---

## 82. Quality assurance

Use typed QA actions.

Examples:

- source verification
- translation review
- identity-resolution review
- legal review
- editorial review
- independent reassessment

Consequential publications may eventually have formal assurance cases.

---

## 83. Review independence

Second-person review is not always independent review.

Highest-risk conclusions may require reassessment where the reviewer examines the evidence independently before seeing the original conclusion.

Two signatures do not necessarily mean two independent judgments.

---

## 84. Conflicts of interest

Use a case-relative research-integrity model.

Conflicts can be:

- declared
- managed
- reviewed
- subject to recusal
- trigger stronger review

A conflict of interest does not itself prove research is wrong.

---

## 85. Funding provenance and editorial independence

Funding and editorial control are separate.

As external funding grows, disclose:

- funder
- funded project/dataset
- restrictions
- editorial rights, if any
- safeguards against interference

Independence should be demonstrable.

---

## 86. Publication provenance

Consequential published representations should be reproducible.

Where appropriate preserve:

- exact rendered text
- language
- publication date
- underlying dataset/assertions
- evidence bundle
- methodology version
- terminology version
- localization version
- template/software version
- subsequent correction/retraction history

The project should be able to answer:

> What exactly did we publicly say about X, in language Y, on date Z, and on what evidence/methodology?

---

## 87. Versioning dimensions

Do not treat “website version” as one number.

Version dimensions include at least:

- code
- database schema
- ontology/vocabulary
- dataset/content
- public release
- collector
- processing pipeline
- prompt/model
- methodology
- terminology/localization

The architecture study must determine an appropriate versioning strategy for each.

Do not impose SemVer everywhere without research.

---

## 88. Releases and reproducibility

For important releases, the system should be able to answer:

- Git commit?
- software version?
- schema version?
- ontology version?
- dataset snapshot?
- collector/pipeline versions?
- methodology version?
- terminology/localization version?
- build/deployment timestamp?
- configuration?
- integrity manifest?

Important releases should be reproducible as far as practical.

---

## 89. Dataset releases

Meaningful dataset releases should be frozen/versioned snapshots.

They should progressively include:

- schema/ontology versions
- documentation
- checksums
- release manifest
- coverage information
- known limitations
- licensing
- provenance
- changelog
- machine-readable change sets
- DOI/persistent identifier where mature and appropriate

---

## 90. Public site history

Maintain page/content revision history from the beginning.

Create whole-site snapshots at significant releases.

Whether all historical revisions are publicly browsable can remain a later product decision.

---

## 91. Changelogs

Use:

- human-readable changelogs early
- structured change categories/statistics
- later research-grade change sets

Support mappings for:

- changed objects
- merged objects
- split objects
- retracted objects
- deprecated ontology terms

---

## 92. Evidence/research packages

The architecture should eventually support exportable provenance/evidence packages.

Potential contents:

- selected entities
- events
- assertions
- source versions
- original files
- hashes
- acquisition metadata
- transformations
- citations
- access/redaction metadata
- machine-readable manifest

Use established archival/forensic packaging standards where appropriate rather than inventing a proprietary package.

---

## 93. API strategy

Architect so a first-class API is possible.

Do not freeze an API contract before the ontology/evidence model stabilizes.

Possible evolution:

- small read-only API
- public API
- tiered API
- subscription API
- versioned API with deprecation policy

---

## 94. Standards-first principle

Do not reinvent established concepts unnecessarily.

Phase II should investigate relevant standards/models from:

- library and information science
- archival science
- museum collections
- digital preservation
- digital humanities
- scholarly publishing
- knowledge graphs
- provenance
- bibliographic description
- citation systems
- records management
- configuration management
- legal evidence
- intelligence analysis
- argumentation
- research data management
- terminology

Candidate standards/models to investigate include, without presupposing adoption:

- Schema.org
- Dublin Core
- PROV-O
- CIDOC CRM
- Wikidata modeling practices
- TEI
- CSL
- PREMIS
- BagIt
- OAIS concepts
- IIIF
- WARC
- relevant records/configuration-management standards

---

## 95. Canonical representation research question

Do not yet decide whether canonical knowledge representation is:

- relational-first
- RDF/OWL-first
- layered
- another model

Require an architecture study comparing the alternatives against actual requirements.

No permanent ontology/storage decision should be made merely because one technology sounds more sophisticated.

---

## 96. Ontology versioning

If semantic/ontology modeling is adopted, ontology/vocabulary versions must be explicit.

Meaning-changing ontology changes require:

- version
- migration
- deprecated term
- replacement mapping
- documentation
- relationship to dataset releases

A dataset can survive while its meaning is lost; ontology versioning prevents that.

---

## 97. Methodology as research infrastructure

The methodology is a first-class versioned artifact from the beginning.

It should have:

- version
- effective date
- changelog
- links to relevant dataset/release versions

A significant methodological change becomes release provenance.

---

## 98. Decision Records

Use a unified Decision Record system.

Potential categories:

- architecture
- methodology
- epistemology
- preservation
- security
- legal
- editorial

Each DR should capture:

- context
- alternatives
- decision
- rationale
- consequences
- status
- supersession

The Phase I questionnaire is raw requirements-discovery material.

Claude should extract candidate DRs, consolidate duplicates, and submit the proposed DR set for human approval rather than mechanically creating one DR per question.

---

## 99. Requirements traceability

Important requirements should have stable identifiers.

Traceability chain:

**objective → requirement → Decision Record → specification/design → implementation → verification/test → methodology → release**

Potential requirement categories:

- PRES
- EVID
- SEC
- LEGAL
- DATA
- ARCH
- EDIT
- AI
- I18N
- OPS

Each important requirement should ultimately have:

- ID
- status
- effective/version date
- verification criteria
- links to relevant DRs/specifications/tests/releases

---

## 100. Governance/documentation architecture

Distinguish document classes:

- `REQ` — requirement
- `POL` — policy
- `PROC` — procedure
- `DR` — decision record
- `SPEC` — specification
- `METH` — methodology

The README is an entry point, not the repository's institutional memory.

Governance/document-control standards should be researched before freezing document lifecycle semantics.

---

## 101. Semantic registry / data dictionary

Maintain a versioned semantic registry.

It should progressively include:

- field/data-element definitions
- controlled vocabularies
- enumerations
- units
- identifier types
- relationship semantics
- validation rules
- ownership/provenance
- effective dates
- deprecated terms
- replacement mappings
- links to ontology
- links to requirements
- links to specifications
- links to methodology

Every consequential data element should have one documented meaning, or an explicit explanation of contextual meaning.

---

## 102. Controlled vocabulary

Establish a small controlled vocabulary early.

Support:

- canonical terms
- definitions
- synonyms
- broader/narrower relationships
- external mappings
- multilingual preferred labels

Expand only as actual data requires.

---

## 103. Research workstreams required before implementation

Phase II should explicitly research:

### Epistemology / philosophy of science
- facts vs assertions
- observation
- evidence
- inference
- uncertainty
- confidence
- causation
- competing hypotheses

### Knowledge representation
- entities
- events
- temporal relationships
- provenance
- semantic modeling
- canonical representation

### Archival science / digital preservation
- provenance
- custody
- fixity
- PREMIS
- OAIS
- WARC
- BagIt
- preservation packages
- long-term identifiers

### Library/information science
- bibliographic identity
- work/expression/manifestation/item distinctions
- controlled vocabularies
- metadata
- citation

### Legal evidence
- direct/circumstantial evidence
- authentication
- chain of custody
- standards of proof
- legal findings
- admissibility concepts

### Intelligence analysis
- source evaluation
- confidence
- probability
- alternative hypotheses
- structured analytic techniques
- attribution
- source independence

### Argumentation theory
- premises
- conclusions
- defeaters
- counterarguments
- competing explanations
- formal/computational argumentation

### Sanctions/export-control law and data
- designations
- legal effects
- ownership/control rules
- licensing
- temporal legal applicability
- trade classification
- customs/transaction modeling

### Records/configuration management
- document status
- approval
- effective date
- supersession
- retention
- traceability
- versioning

### Terminology and multilingual publishing
- concept-oriented terminology
- authoritative terminology
- translation provenance
- TM vs terminology
- language/version management

---

## 104. Phase I synthesis principles

The 200+ individual decisions repeatedly reduce to a smaller set of governing principles.

### Principle 1 — Preserve distinctions
Do not collapse concepts merely because databases prefer simple fields.

### Principle 2 — Provenance is first-class
Every consequential datum should be traceable to origin and transformation.

### Principle 3 — Source ≠ truth
What a source says is not automatically what happened.

### Principle 4 — Authenticity ≠ veracity
A genuine object can contain false information.

### Principle 5 — Collection ≠ evidence
Being in the archive does not mean being evidentially selected.

### Principle 6 — Evidence is claim-relative
A source's evidentiary value depends on the proposition it bears on.

### Principle 7 — Inference must remain visible
Derived conclusions must not masquerade as source-provided facts.

### Principle 8 — Unknown ≠ no
Absence of data must never become a factual negative by default.

### Principle 9 — Uncertainty must remain uncertainty
Do not transform uncertainty into false precision.

### Principle 10 — Legal status ≠ historical truth
Legal findings, authority claims, and historical conclusions remain distinct.

### Principle 11 — Preservation ≠ publication
The project may preserve material it cannot or should not publicly expose.

### Principle 12 — Identity is evidentiary
Names, identifiers, accounts, aliases, and entity matches require provenance.

### Principle 13 — Time matters
Relationships, statuses, legal regimes, names, control, ownership, and assertions change over time.

### Principle 14 — AI proposes; humans remain accountable
AI may scale research, but consequential project conclusions require human accountability.

### Principle 15 — Version meaning, not just files
Code, schema, ontology, data, methodology, terminology, collectors, and releases all have distinct version histories.

### Principle 16 — Reproducibility matters
A future researcher should be able to reconstruct what the project knew, used, concluded, and published at a particular time.

### Principle 17 — Use established standards before inventing new ones
Theoretical and standards research precedes permanent architecture.

### Principle 18 — The public website is a projection
The durable evidence/knowledge repository is primary; the website is one publication interface.

---

## 105. Phase I closure

Phase I — Requirements Discovery is now complete.

The questionnaire and decision trail are to be preserved as source material.

This document is a structured synthesis of that discovery record, not a substitute for the original reasoning trail.

No permanent data model, ontology, API contract, or technical stack should be frozen from this document alone.

---

# Phase II — Theoretical Synthesis & Standards Mapping

## Objective

Determine which established concepts, models, vocabularies, and standards already solve the problems identified in Phase I.

## Required outputs

Phase II should produce at least:

1. **Domain map**
   - epistemology
   - evidence
   - provenance
   - archives/preservation
   - knowledge representation
   - temporal modeling
   - sanctions/export controls
   - legal findings
   - argumentation
   - multilingual terminology
   - records/configuration management
   - research reproducibility

2. **Standards/model matrix**
   For each candidate standard/model:
   - problem solved
   - discipline of origin
   - strengths
   - limitations
   - fit to project
   - adoption level:
     - adopt
     - adapt
     - map to
     - reject
     - defer

3. **Conceptual conflict register**
   Where disciplines use the same word differently, document the conflict.

4. **Candidate foundational vocabulary**
   Derived from established theory, not ad hoc schema design.

5. **Candidate Decision Records**
   Consolidated from Phase I and submitted for approval.

6. **Candidate Requirements**
   Stable IDs, categories, traceability, verification criteria.

7. **Unresolved research questions**
   Questions that must remain open before Phase III.

8. **Phase II methodology version**
   The research method used to perform the standards mapping.

---

## Constraint

During Phase II:

> **Do not start by asking what database tables to create.**

Start with:

> **What concepts already exist, what distinctions have mature disciplines already made, and which standards can faithfully express the requirements discovered in Phase I?**

Only after that should the project proceed to:

**Phase III — Conceptual Architecture**

---

## End of Phase I Record
