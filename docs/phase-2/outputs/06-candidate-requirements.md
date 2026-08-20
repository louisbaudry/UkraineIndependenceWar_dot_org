# Phase II Output 6 — Candidate Requirements

Candidate requirement set extracted from the Phase I record and DR-0001…0052,
per DR-0051. Status of every entry: **candidate** — enactment as REQ-class
controlled documents (DR-0046) follows founder approval. Verification criteria
are sketches to be completed at enactment; traceability cites the primary
sources (record §, DRs). Categories per record §99.

## PRES — Preservation

| ID | Requirement | Sources |
|---|---|---|
| PRES-001 | Originals are preserved immutably, separate from all derivatives | §7; DR-0003 |
| PRES-002 | Every preserved object has a SHA-256 digest recorded at ingestion | §7; DR-0005 |
| PRES-003 | Periodic fixity checks are performed and recorded as events with outcomes | §7; DR-0005 |
| PRES-004 | Every preserved object is answerable against the five OAIS PDI components | DR-0001 |
| PRES-005 | High-value web sources are captured in WARC (or successor per WACZ evaluation) | §7; DR-0006 |
| PRES-006 | Packages that move between systems carry per-file checksum manifests | DR-0005/0007 |
| PRES-007 | Failed acquisitions are recordable as events; historically significant failures are preserved permanently | §28; DR-0002 |
| PRES-008 | Backup, archival preservation, and releases are governed and stored separately | §7; DR-0009 |
| PRES-009 | The archive is reconstructible without the public website | §7; Principle 18 |
| PRES-010 | Archival holdings are transferable to a successor archive with PDI intact | §7; DR-0001 |
| PRES-011 | Retention is multi-stage and source-specific; not everything is archived equally | §9 |
| PRES-012 | Graphic material can be preserved while restricted; visibility and preservation are separate decisions | §10 |

## EVID — Evidence & epistemics

| ID | Requirement | Sources |
|---|---|---|
| EVID-001 | Every assertion carries who asserts it, when, and on what basis | §30; DR-0024/0031 |
| EVID-002 | Documentary assertions, world assertions, and project conclusions are distinct objects | §32–33; DR-0024 |
| EVID-003 | Evidence relations are explicit and claim-relative; archived ≠ evidentially used | §29; DR-0024 |
| EVID-004 | Evidential annotations target preserved captures with version pinning and selector redundancy | §24; DR-0018 |
| EVID-005 | Quotations carry exact passage, source version, locus, omissions, and derivation; none minted from paraphrase | §59; DR-0019 |
| EVID-006 | Likelihood and analytic confidence are recorded separately; bare numeric scores are prohibited | §42; DR-0026 |
| EVID-007 | Contradictory assessments are preserved, never averaged | §40; DR-0026 |
| EVID-008 | Source grades never determine proposition truth | §37; DR-0027 |
| EVID-009 | Corroboration counts independent lines only; dependence relations are typed and recorded where consequential | §36; DR-0028 |
| EVID-010 | Missing values never default to negatives; absence states are typed; negatives carry provenance | §41; DR-0029 |
| EVID-011 | Quantitative assertions preserve original semantics; normalization never overwrites | §44; DR-0030 |
| EVID-012 | Consequential conclusions preserve visible inference chains with typed defeaters | §34; DR-0032/0033 |
| EVID-013 | Important investigations maintain competing-hypothesis sets with discriminating evidence | §35; DR-0035 |
| EVID-014 | No computation adjudicates a project conclusion | §79; DR-0036 |
| EVID-015 | Prior epistemic states are never rewritten by later events | §63; DR-0048 |

## SEC — Security & sensitive material

| ID | Requirement | Sources |
|---|---|---|
| SEC-001 | Confidential-source identity is architecturally separable from ordinary research data | §11 |
| SEC-002 | Third-party submissions are quarantined and security-checked before entering the archive | §11 |
| SEC-003 | Access control supports the §12 tier set without a universal is_public flag | §12 |
| SEC-004 | Restricted graphic material is inaccessible below its access tier at every layer | §10, §12 |

## LEGAL — Legal layer

| ID | Requirement | Sources |
|---|---|---|
| LEGAL-001 | No boolean sanctioned property exists anywhere in the system | §64; DR-0038 |
| LEGAL-002 | The system answers: which restrictions applied, under which authority/jurisdiction, to whom, during what period | §3; DR-0038 |
| LEGAL-003 | Designation records are distinct from canonical entities; mapping is an evidence-backed assertion, never fuzzy-matched | §72; DR-0039 |
| LEGAL-004 | Rule-derived applicability is computed, versioned, path-preserving, and never displayed as designation | §71/§73; DR-0041 |
| LEGAL-005 | Export-control state decomposes into classification, requirement, authorization, and violation-as-finding | §65–66; DR-0042 |
| LEGAL-006 | Legal findings carry jurisdiction, authority, standard of proof, and procedural posture; never merged with project conclusions | §62; DR-0024 |
| LEGAL-007 | The project never asserts legal chain of custody as a status | §6; DR-0008 |
| LEGAL-008 | Preservation rights and republication rights are recorded separately per §14's permission set | §14; DR-0002 |
| LEGAL-009 | A formal personal-data policy exists before broad automated collection begins | §13 |

## DATA — Data & identity

| ID | Requirement | Sources |
|---|---|---|
| DATA-001 | Names and identifiers attach via assignment events with provenance | §16–17; DR-0012 |
| DATA-002 | Identity merges require evidence; merge/split history is preserved; false merges are treated as costlier than missed matches | §16–17; DR-0012 |
| DATA-003 | Roles and memberships are temporal events, never mutable attributes | §18; DR-0013 |
| DATA-004 | Product types and individual items are distinct, linkable objects | §21; DR-0014 |
| DATA-005 | Ownership/control are typed interest statements with provenance and validity periods | §19; DR-0040 |
| DATA-006 | Transactions, shipments, and payments are distinct event types | §68; DR-0043 |
| DATA-007 | Territorial statuses are typed temporal relations; competing characterizations coexist | §46; DR-0044 |
| DATA-008 | Every consequential data element has one registry-documented meaning | §101; DR-0050 |
| DATA-009 | Stable public identifiers resolve permanently for citable research objects | §15 |
| DATA-010 | External identifier mappings (Wikidata, OpenSanctions, registries, LEI, IMO…) are typed and provenance-bearing | §16; DR-0012/0045 |

## ARCH — Architecture

| ID | Requirement | Sources |
|---|---|---|
| ARCH-001 | Pipeline and world layers are permanently separate; cross-appearing parties are linked, never merged | DR-0004 |
| ARCH-002 | The six-layer epistemic architecture governs all knowledge modeling | DR-0024 |
| ARCH-003 | Documentary identity follows Work/Expression/Manifestation/Item | §22; DR-0011 |
| ARCH-004 | The canonical-representation decision (§95) is made in Phase III against requirements, not technology preference | §95 |
| ARCH-005 | A first-class API remains possible; no API contract freezes before the ontology stabilizes | §93 |
| ARCH-006 | Access tiers never create competing versions of historical truth; the canonical evidence system is common to all tiers | §4 |

## EDIT — Editorial

| ID | Requirement | Sources |
|---|---|---|
| EDIT-001 | The founder is final editorial authority; review becomes risk-tiered as the team grows | §78 |
| EDIT-002 | Substantive corrections leave a visible trace; nothing is silently overwritten | §77 |
| EDIT-003 | Consequential published conclusions are drafted against the Toulmin scaffold with calibrated qualifiers | DR-0037/0026 |
| EDIT-004 | Publication wording distinguishes designated from rule-derived, finding from assessment, quotation from paraphrase | DR-0041/0024/0019 |
| EDIT-005 | Published representations of consequential conclusions are reproducible from their release baseline | §86; DR-0048 |

## AI — AI involvement

| ID | Requirement | Sources |
|---|---|---|
| AI-001 | AI outputs never become canonical without human accountability | §79; DR-0036 |
| AI-002 | Consequential AI outputs preserve model, instructions, inputs, output, pipeline version, and reviewer disposition | §80 |
| AI-003 | AI-proposed assertions are beliefs held by a software agent until adopted under human review | DR-0031 |

## I18N — Language & terminology

| ID | Requirement | Sources |
|---|---|---|
| I18N-001 | Original-language material is primary; translations are derived expressions with provenance | §58; DR-0011 |
| I18N-002 | Important concepts have per-language preferred terms, definitions, and forbidden-translation notes in the registry | §60; DR-0050 |
| I18N-003 | Canonical semantics and user-facing wording are separate; presentation resources are versioned | §61; DR-0047 |

## OPS — Operations

| ID | Requirement | Sources |
|---|---|---|
| OPS-001 | Collection runs automatically on a configurable source registry; collection never implies publication | §8 |
| OPS-002 | Every release is a baseline with integrity manifest, coverage statement, and changelog | §88–89; DR-0048 |
| OPS-003 | Merged/split/retracted object mappings ship with every data release from the first | §91; DR-0048 |
| OPS-004 | Public pages carry revision history from first publication; site snapshots join release baselines | §90; DR-0052 |
| OPS-005 | Independent backups exist and evolve toward geographic/provider redundancy | §7 |
| OPS-006 | Collector coverage, outages, and known gaps are recorded per §57 | §57 |
