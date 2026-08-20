# Phase II / Workstream 1 — Preservation & Provenance Concept Map
## Working Paper 0.2

**Project:** Ukraine's Second War of Independence
**Status:** CANDIDATE — AI-drafted, awaiting founder review and approval. Nothing in this paper is canonical.
**Version:** 0.2 (first draft of Workstream 1)
**Mandate:** WP 0.1, "Next deliverable" — compare OAIS, PREMIS, PROV, WARC and BagIt against the Phase I requirements for acquisition, immutable originals, fixity, custody, source lifecycle, transformation lineage, rights/access, failed acquisition, evidence packages, backup versus archive, succession and reproducibility.

### AI provenance (per Phase I record §80)

| Field | Value |
|---|---|
| Drafted by | AI assistant (Anthropic Claude Code agent session), at the founder's request |
| Date | 2026-08-10 |
| Inputs | Phase I Requirements Discovery Record; WP 0.1; web verification of current standard versions (sources listed at end) |
| Human review | **Pending** — founder is final editor (record §78); this document proposes, it does not decide |
| Disposition | Candidate working paper; all "candidate Decision Records" herein are proposals requiring explicit approval |

---

## 1. Scope and method

This paper maps five preservation/provenance standards against the Phase I
requirements. For each requirement area it identifies: which standard supplies the
concept, how faithfully, and what remains uncovered. It follows the Phase II rule —
concepts before tables. No schema, serialization format, or storage technology is
selected here.

Method: (1) restate each standard's conceptual core and current version;
(2) establish a composition model showing how the five relate without overlap or
contradiction; (3) map the twelve requirement areas named in WP 0.1;
(4) extract candidate conceptual-conflict-register entries (Phase II output 3);
(5) record gaps and additional candidate standards surfaced by the mapping;
(6) propose candidate Decision Records and unresolved research questions.

---

## 2. The five standards — conceptual cores

### 2.1 OAIS — ISO 14721:2025 / CCSDS 650.0-M-3

A **reference model for archival responsibility**, not a metadata format. Version 3
was published by CCSDS in December 2024 and by ISO in January 2025; it adds
**Preservation Objectives** (making "independently understandable" testable) and a
**Preservation Watch** function within Preservation Planning.

Core concepts relevant to Phase I:

- **Information packages:** SIP (submission), AIP (archival), DIP (dissemination).
  The distinction between what is submitted, what is preserved, and what is
  disseminated is exactly the Phase I separation of acquisition, preservation, and
  publication (§8, Principle 11).
- **Preservation Description Information (PDI):** provenance, context, reference,
  fixity, and access-rights information — a ready-made checklist for what must
  accompany every preserved object.
- **Representation Information & Designated Community:** preserved bits must remain
  *interpretable* by an identified future audience — the conceptual grounding for
  Phase I's "reconstructible even if the public website disappears" (§7) and
  Principle 16 (reproducibility).
- **Succession planning:** OAIS treats handover of archival responsibility as a
  first-class obligation — grounding for §7's institutional-deposit trajectory.

### 2.2 PREMIS 3.0 — preservation metadata data dictionary

The Library of Congress-maintained dictionary of **what an archive must record to
preserve digital objects**. Its data model has five entities:

- **Intellectual Entities** — the conceptual unit (a report, a video);
- **Objects** at three levels — *representation*, *file*, *bitstream*;
- **Events** — datable actions performed **on archived objects** (ingestion, message
  digest calculation, virus check, fixity check, migration, normalization), each with
  agents, outcomes, and outcome details;
- **Agents** — persons, organizations, or **software** performing events;
- **Rights** — rights statements with a basis (copyright, license, statute) governing
  what the archive may do (preserve, replicate, migrate, disseminate).

PREMIS events with recorded outcomes — including **failure outcomes** — and typed
inter-object derivation relationships are the closest existing vocabulary to Phase I
§7 and §28.

### 2.3 W3C PROV / PROV-O (2013)

A **generic provenance model**: **Entities** (things), **Activities** (processes
spanning time), **Agents** (bearing responsibility), connected by relations such as
`wasGeneratedBy`, `used`, `wasDerivedFrom`, `wasAttributedTo`, `actedOnBehalfOf`.
Two properties matter especially:

- PROV entities are **immutable snapshots** — a change produces a *new* entity
  related by derivation. This matches Phase I's "originals are immutable; derivatives
  are separate objects" (§7) at the conceptual root.
- PROV is domain-neutral: the same three-class pattern describes OCR, translation,
  AI enrichment (§80), entity-resolution decisions (§17), editorial review (§78),
  dataset generation, and publication (§86). PREMIS cannot cover these; PROV can.
- **Bundles** — provenance *of provenance* — offer a conceptual basis for recording
  who asserted a provenance chain and when (relevant to §86–88 reproducibility).

### 2.4 WARC — ISO 28500 (WARC 1.1)

The container format for **web capture**: preserves full HTTP request/response
records, capture timestamps, block/payload digests, and **revisit records** for
recapture of unchanged content. WARC is *evidence-grade web preservation* — it
preserves what the server returned, not a rendering of it. Maps to §7 ("preserve web
captures in richer formats such as WARC for selected high-value sources").

### 2.5 BagIt — RFC 8493

A deliberately minimal **packaging convention** for storage and transfer: a payload
directory plus manifests with per-file checksums and optional metadata tags. Its
role is reliable movement and at-rest self-verification of packages — not
description, not preservation planning. **BagIt profiles** allow the project to
require specific tags per package type.

---

## 3. Composition model (working principle, refined from WP 0.1)

The five standards occupy different layers and compose without conflict:

| Layer | Standard | Governs |
|---|---|---|
| Responsibility & lifecycle | OAIS | What an archive *is obliged to do*: ingest, preserve, plan, disseminate, hand over |
| Preservation metadata | PREMIS | What is *recorded about* preserved objects and actions on them |
| General derivation & agency | PROV | How *anything* (including non-preservation research artifacts) was derived, by which activity, under whose responsibility |
| Capture format | WARC | How web content is acquired and stored as evidence-grade records |
| Package format | BagIt | How sets of files travel and self-verify |

Refined working principle:

> **OAIS defines the obligations; PREMIS records the preservation facts; PROV records
> the derivation graph of the whole research pipeline; WARC is one acquisition
> format among several; BagIt is one packaging convention among several.**

Boundary rule (candidate): every preservation action (PREMIS event) is *also
expressible* as a PROV activity, but not every PROV activity is a preservation
action. PREMIS is the specialized vocabulary inside the archive wall; PROV is the
lingua franca across the entire pipeline, including AI enrichment and editorial
work. The two must be mapped, not merged (a published PREMIS-3 OWL ontology exists
and aligns with PROV, so this mapping is established practice, not invention).

---

## 4. Requirement-by-requirement concept map

Phase I references are to sections of the Requirements Discovery Record.

### 4.1 Acquisition (§8, §28)

- **OAIS:** ingest function; SIP→AIP transformation; the Producer–Archive interface
  is further specified in PAIS (CCSDS 651.1-B-1), consistency with which was
  improved in OAIS v3.
- **PREMIS:** ingestion event, virus check, message-digest calculation; software
  collectors as PREMIS agents.
- **PROV:** the acquisition activity, its `used` source (URL, feed, channel), the
  collector agent, the generated entity.
- **Gap:** *discovery* provenance (§28: how a source was found, including "learned
  through another investigation") is not a preservation concept. PROV can express it
  ("discovery activity generated a lead entity"), but the vocabulary of discovery
  origins is project-specific and belongs in the semantic registry (§101).

### 4.2 Immutable originals (§7)

- **PREMIS:** originals as representations/files with `originalName`, fixity, and
  no modification events; derivatives as distinct objects with derivation
  relationships.
- **PROV:** immutability is native — entities are fixed; transformation creates new
  entities. This is the cleanest conceptual anchor for the rule.
- **Gap:** immutability is ultimately *policy plus storage discipline*; no metadata
  standard enforces it. A storage-layout standard such as **OCFL** (Oxford Common
  File Layout) — which stores immutable versioned objects with forward deltas —
  is a candidate for the enforcement layer and should be studied.

### 4.3 Fixity (§7)

- **PREMIS:** fixity semantic unit (algorithm + digest) on objects; *fixity check*
  events for §7's "periodic fixity checking," each with outcome and date.
- **OAIS:** Fixity Information is a mandatory PDI component.
- **BagIt:** payload manifests give every package portable, self-contained fixity.
- **WARC:** per-record block/payload digests.
- **Fit:** complete coverage; the four mechanisms operate at different granularities
  (object, package, capture record) and should all be used. Already practiced: both
  repository documents ingested so far carry SHA-256 at ingestion.

### 4.4 Custody (§6)

- **OAIS:** custody history is part of PDI Provenance Information; v3 retains
  explicit chain-of-custody language for the archival (not legal) sense.
- **PREMIS:** custody transfers as events with agents.
- **Critical distinction (§6):** none of these standards establishes **legal chain
  of custody**. They document custody; courts and legal frameworks assess it. The
  **Berkeley Protocol** (identified in WP 0.1 as methodologically central) is the
  bridge: it specifies *practices* during collection and handling that maximize
  future evidentiary utility. Candidate rule: the archive records custody in
  PREMIS/PROV vocabulary and **never emits the phrase "chain of custody" as a
  status claim** — only as documented custody history.

### 4.5 Source lifecycle (§24)

The states in §24 — published, edited, deleted, restored, redirected, censored,
unsealed, replaced — describe **the source's own history in the world**, not the
archive's copy.

- **WARC:** successive captures + revisit records document *observed* states over
  time; this is evidence *for* lifecycle assertions, not the lifecycle model itself.
- **Memento (RFC 7089):** the time-versioned-resource model ("this URI, as it
  existed at time T") is a strong conceptual candidate for expressing capture series
  and should be added to the standards matrix for study.
- **Gap (important):** source-lifecycle states are **world assertions** (§32) and
  belong to the historical/documentary layers (WP 0.1 layers C/D), supported by
  capture evidence from this layer. The preservation layer must not be asked to
  model them. This is a load-bearing boundary finding of Workstream 1.

### 4.6 Transformation lineage (§7, §22, §58)

- **PROV:** the primary model — OCR, transcription, translation, format migration,
  AI extraction each as an activity `using` the parent entity and generating the
  derivative, with software/model agents (§80).
- **PREMIS:** the preservation-relevant subset (migration, normalization) as events
  with derivation relationships between objects.
- **Fit:** strong, provided the boundary rule in §3 above is respected. Every
  derivative can answer "what was I derived from?" (§50) via `wasDerivedFrom`
  chains.

### 4.7 Rights and access (§12, §14)

- **PREMIS Rights:** rights basis (copyright, license, statute, policy) +
  permitted acts — maps almost one-to-one onto §14's "may preserve / may display /
  may redistribute / may provide to subscribers / unknown rights." "Unknown rights"
  is representable as absence of a rights statement **plus** an explicit
  unknown-status marker (§41: unknown ≠ no).
- **OAIS:** Access Rights Information in PDI.
- **Gap:** Phase I §12 requires **four separate dimensions** (access tier,
  sensitivity, rights, evidentiary disclosure). PREMIS covers the rights dimension
  only. Tiering and sensitivity are project policy vocabulary (semantic registry).
  **ODRL** (W3C policy expression) could formalize machine-readable access policies
  later — candidate disposition: **defer**.

### 4.8 Failed acquisition (§28)

- **PREMIS:** events carry `eventOutcome` including failure, with detail — an
  acquisition attempt that produced no object is a recordable event with an agent,
  date, and outcome. Retries and later success are further events.
- **PROV:** an activity that generated no entity.
- **Fit:** conceptually complete; what Phase I adds is the *editorial* judgment that
  some failures are historically significant and must be preserved permanently
  (§28). That selection rule is methodology, not metadata.

### 4.9 Evidence/research packages (§92)

- **BagIt:** the transport/storage envelope with fixity; BagIt profiles can define
  a project evidence-package profile.
- **OAIS:** the DIP concept — a package assembled for a consumer (court,
  researcher, journal) from AIPs.
- **Additional candidates surfaced by this mapping (per §92's instruction to use
  established packaging standards):**
  - **RO-Crate** — research-object packaging with a machine-readable metadata
    manifest; designed for exactly the "selected entities + files + provenance +
    manifest" bundle §92 describes; high-priority study.
  - **WACZ** — packaged, optionally cryptographically signed web-archive
    collections (Webrecorder ecosystem; used in OSINT evidentiary workflows aligned
    with the Berkeley Protocol); high relevance for web evidence packages.
  - **METS** — structural maps for complex packages; study as map-to.
- **Fit:** composition of BagIt (envelope) + PREMIS (preservation metadata) +
  PROV (derivation) + a manifest layer (RO-Crate candidate) covers §92 without
  inventing a proprietary package.

### 4.10 Backup vs archive vs frozen release (§7)

The three concepts Phase I insists on separating map to three different standards'
domains:

| Phase I concept | Standard grounding |
|---|---|
| **Backup** | Not an OAIS function at all — bit-level disaster recovery of storage; below the archival layer |
| **Archival preservation** | OAIS AIPs under active preservation planning, fixity monitoring, format watch |
| **Frozen research release** | Versioned DIP/dataset snapshot with its own identity, manifest, and citation (DataCite layer, per WP 0.1 §I) |

The mapping confirms the Phase I distinction is not idiosyncratic — it falls out of
OAIS naturally. Backup copies of AIP storage are infrastructure; a release is a
published information product; only the middle layer carries preservation
obligations.

### 4.11 Succession (§7)

- **OAIS:** succession planning is an explicit archival responsibility; the AIP
  concept requires packages to be transferable to a successor archive with their
  PDI intact.
- **ISO 16363** (trustworthy digital repository audit, revised alongside OAIS)
  provides the assessment framework a future institutional partner would apply —
  candidate **map-to** disposition: use its criteria as a self-assessment checklist
  long before formal certification is meaningful.
- **Fit:** §7's "eventually support institutional preservation/deposit" is
  precisely OAIS succession; designing AIPs + BagIt/OCFL storage from the start
  makes eventual deposit a transfer, not a migration.

### 4.12 Reproducibility (§86–88, Principle 16)

- **OAIS:** Representation Information and (new in v3) Preservation Objectives
  ground "a future researcher can interpret this" as a testable property.
- **PROV:** bundles + activity graphs answer "what did we know/use/conclude at
  time T"; the derivation graph of a release *is* its reproducibility record.
- **BagIt/manifests:** integrity of the released artifact set.
- **Gap:** §87–88's multi-dimensional versioning (code, schema, ontology, dataset,
  methodology, terminology…) is configuration-management territory — Workstream 7,
  not this one. This workstream contributes the rule that **every release manifest
  is itself a preserved, fixity-checked object with PROV provenance**.

---

## 5. Candidate entries — conceptual conflict register (Phase II output 3)

| Term | Colliding senses | Resolution direction (candidate) |
|---|---|---|
| **provenance** | Archival science (origin/custody of a fonds) vs PREMIS (preservation actions) vs PROV (generic derivation) vs record §6 (ordinary provenance vs legal chain of custody) | Qualify always: *acquisition provenance*, *preservation provenance*, *derivation provenance*, *custody history*. Never bare "chain of custody" as a claim |
| **event** | PREMIS event (action **on an archived object**) vs CIDOC CRM event (**historical occurrence in the world**) | Hard separation: pipeline events vs world events live in different layers and registries; a capture is never a world event |
| **agent** | PREMIS agent vs PROV agent vs historical actor (CRM) | Pipeline agents (people, orgs, software acting on the archive) form a registry distinct from historical actors; a person may appear in both, linked, never merged |
| **object** | PREMIS object (representation/file/bitstream) vs Phase I §21 physical objects (vessels, weapons) | "Digital object" vs "physical object" always qualified |
| **archive** | OAIS organization vs web archive vs "the archive" (project corpus) | Define in controlled vocabulary (§102) |
| **fixity / integrity / authenticity** | Fixity = bit-level sameness; integrity = §38 preserved-copy soundness; authenticity = §38 the object is what it purports to be | Three separate assessments; fixity success never implies authenticity (§38) |
| **version** | Source version (§24, world) vs object version (preservation) vs release version (§87) vs document version (governance) | Different version regimes per §87; never a single "version" field |

---

## 6. Gaps and additional candidate standards surfaced

Gaps in the five mandated standards (none fatal; all bounded):

1. **Discovery provenance** vocabulary — project-specific (semantic registry).
2. **Source lifecycle** — belongs to world/documentary layers; Memento candidate
   for the capture-series concept.
3. **Multi-dimensional access model** — PREMIS rights is one of §12's four
   dimensions; the rest are project policy vocabulary.
4. **Immutability enforcement** — policy + storage layout (OCFL candidate).
5. **Legal chain of custody** — no metadata standard confers it; Berkeley Protocol
   governs practice; claims discipline governs language.

Standards to add to the Phase II matrix for study (dispositions proposed):

| Standard | Proposed disposition | Role |
|---|---|---|
| OCFL | Study — likely adopt | Immutable, versioned archival storage layout |
| RO-Crate | Study — high priority | Evidence/research package manifests (§92) |
| WACZ | Study — high priority | Packaged, signable web-archive collections for OSINT evidence |
| Memento (RFC 7089) | Study | Time-versioned resource model for capture series |
| METS | Compare/map | Structural packaging maps |
| ISO 16363 | Map to (self-assessment) | Trustworthy-repository criteria; succession readiness |
| PAIS (CCSDS 651.1-B-1) | Reference | Producer–archive submission modeling |
| ODRL | Defer | Machine-readable access/rights policies |

---

## 7. Candidate Decision Records arising (proposals only — require founder approval)

- **CDR-W1-1:** Adopt OAIS (ISO 14721:2025) conceptually as the archival
  responsibility and lifecycle model; use PDI as the completeness checklist for
  preserved objects.
- **CDR-W1-2:** Adopt PREMIS 3.0 as the preservation-metadata vocabulary
  (conceptual adoption; serialization/implementation deferred to Phase III).
- **CDR-W1-3:** Adopt W3C PROV as the cross-pipeline derivation/agency model,
  covering AI enrichment and editorial activity; map PREMIS events into PROV via the
  published PREMIS-3 OWL alignment rather than inventing a bridge.
- **CDR-W1-4:** Hard layer boundary: pipeline/preservation events and agents are
  permanently separate from historical world events and actors. (Feeds the conflict
  register and the Phase III architecture.)
- **CDR-W1-5:** Fixity: SHA-256 digests at ingestion (already practiced), recorded
  per object; periodic fixity checks recorded as events with outcomes; package-level
  manifests (BagIt) for anything that moves.
- **CDR-W1-6:** WARC for high-value web capture; evaluate WACZ for signed,
  packaged captures before freezing the capture toolchain.
- **CDR-W1-7:** BagIt for storage/transfer envelopes; study RO-Crate before
  designing the §92 evidence-package manifest.
- **CDR-W1-8:** Claims discipline: the project documents custody history and never
  asserts "legal chain of custody" as a status; Berkeley Protocol guides collection
  and handling practice.
- **CDR-W1-9:** Backup, archival preservation, and frozen releases are governed,
  stored, and versioned separately (per §4.10 mapping).

## 8. Unresolved research questions (feed Phase II output 7)

1. PREMIS as conceptual vocabulary vs PREMIS-XML/OWL as implementation — how much
   of the dictionary does the project actually need? (Phase III boundary.)
2. One agent registry with roles, or separate pipeline-agent and
   historical-actor registries with explicit links? (Interacts with CIDOC CRM
   study, Workstream 2.)
3. Where exactly do source-lifecycle states live — documentary layer (D) or world
   layer (C)? (Workstreams 2–3.)
4. Is WACZ signing mature and jurisdictionally meaningful enough to rely on for
   evidentiary packaging?
5. Does OCFL's versioning model conflict with the "originals are immutable,
   derivatives are new objects" rule, or implement it?
6. How do PROV bundles relate to release manifests and methodology versions
   (§87–88, Workstream 7)?
7. What subset of ISO 16363 criteria is meaningful for a single-editor project,
   and when does self-assessment begin?

---

## 9. Sources

- OAIS v3: [ISO 14721:2025 catalogue entry](https://standards.iteh.ai/catalog/standards/sist/e69f8023-f60c-4b06-aa7a-1af3314b004e/sist-iso-14721-2025); [PTAB summary of the 2024/2025 OAIS and related-standard updates](http://www.iso16363.org/oais-iso-14721-iso-16363-and-others-updated/); [oais.info standards process](http://www.oais.info/standards-process/)
- PREMIS 3.0: [Data Dictionary, Library of Congress](https://www.loc.gov/standards/premis/v3/); [PREMIS 3 OWL ontology](https://www.loc.gov/standards/premis/ontology/owl-version3.html)
- W3C PROV-O: W3C Recommendation, 30 April 2013
- WARC: ISO 28500 (WARC 1.1)
- BagIt: RFC 8493
