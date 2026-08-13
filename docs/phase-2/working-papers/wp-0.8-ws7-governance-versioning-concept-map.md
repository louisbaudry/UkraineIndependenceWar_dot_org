# Phase II / Workstream 7 — Governance & Versioning Concept Map
## Working Paper 0.8

**Project:** Ukraine's Second War of Independence
**Status:** CANDIDATE — AI-drafted, awaiting founder review and approval. Nothing in this paper is canonical.
**Version:** 0.8 (first draft of Workstream 7 — the final workstream)
**Mandate:** WP 0.1 research sequence item 7 — records management, configuration management, dataset/ontology releases; record §60–§61, §87–§102.
**Constraints inherited:** DR-0001…0045 throughout; especially DR-0009 (backup/archive/release), DR-0003 (PROV), DR-0022 (CSL), DR-0025 (vocabulary governance by DR).

### AI provenance (per Phase I record §80)

| Field | Value |
|---|---|
| Drafted by | AI assistant (Anthropic Claude Code agent session), continuing the founder-directed workstream sequence |
| Date | 2026-08-11 |
| Inputs | Phase I record (§60–§61, §87–§102 centrally); WP 0.1–0.7; DR-0001…0045 |
| Human review | **Pending** — founder is final editor (record §78) |
| Disposition | Candidate working paper; all candidate Decision Records herein are proposals |

---

## 1. Scope and method

The last workstream governs the project's *own* institutional machinery: how
documents carry status and authority (§100), how everything versions (§87),
how releases become reproducible and citable (§88–89), how vocabularies and
terminology are governed (§60–61, §101–102), and how requirements trace
(§99). The disciplines: records management, configuration management,
metadata-registry practice, terminology science, and research-data publishing.

## 2. Discipline survey — instruments worth taking

### 2.1 Records management (ISO 15489 family)

Core concepts: a **record** is evidence of business activity, with
authenticity, reliability, integrity, and usability as its required qualities;
records have **lifecycle states**, retention schedules, and disposition. For
this project the relevant import is the *document-control* tradition built on
it: controlled documents carry status (draft → review → approved → effective →
superseded/withdrawn), approval authority, effective dates, and supersession
links. The existing DR system already practices this; the DR pattern
generalizes to all six §100 document classes.

### 2.2 Configuration management (ISO 10007 / IEEE 828 tradition)

Concepts: **configuration item** (anything independently versioned),
**baseline** (a named, frozen configuration of items), **change control**
(changes to baselined items are deliberate acts), **status accounting** (what
version is where), and **audit**. The record's §88 release-manifest question —
"Git commit? schema version? ontology version? dataset snapshot? …" — is
verbatim a **baseline** definition. The project's release = a baseline over
named configuration items.

### 2.3 Metadata registries (ISO/IEC 11179 pattern)

The semantic registry required by §101 is a solved shape: **data elements**
with definitions, permissible values, stewardship, registration status, and
effective dates — one documented meaning per consequential element, or an
explicit contextual explanation. The registry itself is versioned and each
entry links to its authorities (here: DRs, requirements, specifications).

### 2.4 SKOS and terminology standards

- **SKOS** (W3C): concepts with per-language preferred/alternate labels,
  definitions, scope notes, broader/narrower/related links, and mapping
  relations to external vocabularies — matching §102's controlled-vocabulary
  requirements and §60's concept-oriented multilingual terminology almost
  term-for-term. "Forbidden/misleading translations" (§60) map to documented
  scope/editorial notes.
- **TBX (ISO 30042)** — the translation industry's termbase exchange format —
  matters when professional translation workflows begin; a study disposition
  suffices now.

### 2.5 Research-data publishing

- **DataCite** (already in the composition, WP 0.1): DOIs + metadata for
  released datasets, with versioning conventions.
- **DCAT** (W3C Data Catalog Vocabulary): standard description of datasets and
  distributions — the natural machine-readable face of the release register.
- **Schema.org** (per WP 0.1: publication mapping only) for discovery.

### 2.6 Versioning practice

The §87 warning ("do not impose SemVer everywhere") is confirmed by practice:
**SemVer** earns its keep where consumers depend on compatibility contracts
(code, APIs, schemas); **calendar/sequence versioning** fits dataset snapshots;
**effective-date versioning** fits governance documents and methodologies;
**ontology versioning** needs deprecation + replacement mappings (§96) more
than version arithmetic. One regime per dimension, chosen by consumer need.

## 3. Composition (candidate)

### 3.1 Document control (§100)

All six document classes — REQ, POL, PROC, DR, SPEC, METH — share one control
pattern (generalizing the existing DR practice): stable ID, class, title,
status (draft / proposed / approved / effective / superseded / withdrawn),
approval authority and date (founder, per §78), effective date where distinct,
supersession links both ways, and change history. Git stores governance
documents (WP 0.1 permitted this role); **status is explicit document
metadata, never inferred from Git state** — a commit is not an approval.

### 3.2 Versioning regimes (§87)

| Dimension | Regime (candidate) |
|---|---|
| Code / APIs | SemVer; API deprecation policy per §93 when an API exists |
| Database schema | SemVer-style with migration scripts as first-class artifacts |
| Ontology / vocabulary / registry | Explicit versions; meaning-changing edits require deprecation + replacement mappings + migration notes (§96); governed by DR (DR-0025 pattern) |
| Dataset / content releases | Snapshot identifiers (date-based sequence), immutable, manifest-carrying (§89) |
| Collectors / pipelines / prompts | Versioned configurations; every run records its versions (§80, DR-0003) |
| Methodology (METH) | Version + effective date + changelog (§97); a significant methodology change is release provenance |
| Terminology / localization | Versioned resources per §60–61; releases pin the version they used |
| Governance documents | Document-control status + dates (§3.1); no SemVer |

### 3.3 Releases as baselines (§88–89)

A **release is a configuration-management baseline**: a named, frozen set of
(dataset snapshot, schema version, ontology/registry version, collector and
pipeline versions, methodology version, terminology version, code commit,
build configuration) plus an **integrity manifest** (checksums per DR-0005),
**coverage statement** (§57), known limitations, licensing, changelog, and
machine-readable change sets as they mature (§91) — including
merged/split/retracted object mappings from the first data release onward.
Release descriptions are expressed in **DCAT** terms; public dataset releases
receive **DataCite DOIs** when the release practice is mature (per WP 0.1's
disposition). Release manifests are preserved, fixity-checked objects with
PROV provenance (per DR-0009's consequence — this closes WP 0.5 §11 Q4's
mechanism: assessments and manifests append under baseline discipline, never
rewrite).

### 3.4 Semantic registry (§101–102)

One **ISO/IEC 11179-patterned registry**, SKOS-expressed where the content is
conceptual: data elements and concepts with definitions, per-language labels
(§60), synonyms, broader/narrower links, external mappings (Wikidata, FtM,
BODS, CRM classes…), validation rules, stewardship, status, effective dates,
deprecations with replacements. The registry hosts what earlier DRs assigned
to it: epistemic vocabulary (DR-0025), absence states (DR-0029), argument
schemes (DR-0034), interest types (DR-0040), territorial statuses (DR-0044),
and the conflict-register resolutions. Registry changes follow a lightweight
registry process; *structural* vocabulary changes require DRs (DR-0025's
rule).

### 3.5 Requirements traceability (§99)

Requirements get stable IDs with the §99 category prefixes (PRES, EVID, SEC,
LEGAL, DATA, ARCH, EDIT, AI, I18N, OPS), each with status, verification
criteria, and links along the §99 chain (objective → requirement → DR → spec →
implementation → verification → methodology → release). The **candidate
requirements themselves are Phase II output 6**, to be extracted from the
Phase I record and the 45+ enacted DRs as the consolidation step after this
workstream.

### 3.6 Public site history (§90)

Page/content revision history from the first public page; whole-site snapshots
at significant releases (a site snapshot is one more configuration item in the
baseline). Public browsability of history remains a later product decision, as
the record allows.

## 4. Candidate conflict-register entries (additions)

| Term | Colliding senses | Resolution direction (candidate) |
|---|---|---|
| **record** | Records-management sense (evidence of activity) vs database record vs the Phase I "Requirements Discovery Record" | Registry-qualified; "record" unqualified never used in specifications |
| **baseline** | CM baseline (frozen configuration) vs colloquial baseline | CM sense only in governance documents |
| **release** | Baseline + published artifact (§89) vs software release vs press release | Project sense defined in registry; press releases are "publications" |
| **effective** | Effective date (document control) vs legal effective time (§45, DR-0038) | Two registry entries; never one field |
| **status** | Document-control status vs epistemic status (DR-0026) vs legal status | Class-qualified always |
| **version** (final consolidation) | The senses accumulated across WP 0.2/0.4/this paper | One registry entry enumerating the regimes of §3.2, closing the term |

## 5. Candidate Decision Records (proposals only — require founder approval)

- **CDR-W7-1:** **Unified document control** for all six §100 classes (REQ,
  POL, PROC, DR, SPEC, METH): stable IDs, explicit status lifecycle
  (draft/proposed/approved/effective/superseded/withdrawn), approval authority
  and dates, supersession links; Git stores governance documents but **status
  is explicit metadata, never inferred from Git**.
- **CDR-W7-2:** **One versioning regime per dimension** (§87), per the §3.2
  table: SemVer only where compatibility contracts exist (code, APIs,
  schemas); snapshot identifiers for data releases; effective-date versioning
  for governance and methodology; ontology/vocabulary changes carry
  deprecation + replacement mappings (§96). No universal SemVer.
- **CDR-W7-3:** **Releases are configuration-management baselines** (§88):
  a named, frozen set of versioned configuration items with integrity
  manifest, coverage statement, limitations, licensing, and changelog;
  release manifests are preserved, fixity-checked, PROV-carrying objects;
  merged/split/retracted mappings ship from the first data release (§91).
- **CDR-W7-4:** **DCAT for release description; DataCite DOIs for public
  dataset releases once release practice is mature** — DCAT immediately as
  the machine-readable release register format; DOI registration timing is an
  operational decision recorded when taken.
- **CDR-W7-5:** **The semantic registry follows the ISO/IEC 11179 pattern,
  expressed in SKOS where conceptual** (§101–102): definitions, per-language
  labels, mappings, stewardship, status, deprecation with replacement; it
  hosts the vocabularies earlier DRs assigned to it; structural changes by DR,
  routine entries by registry process. TBX studied when professional
  translation workflows begin (§60).
- **CDR-W7-6:** **Requirements management per §99:** stable category-prefixed
  IDs, status, verification criteria, and traceability links; the candidate
  requirement set (Phase II output 6) is extracted from the Phase I record and
  enacted DRs as the next consolidation step.
- **CDR-W7-7:** **Public site revision history from the first page; site
  snapshots at significant releases** (§90); public browsability deferred as a
  product decision.

## 6. Unresolved research questions (feed Phase II output 7)

1. Registry tooling: flat files in Git vs a small registry service — Phase III;
   the pattern (11179/SKOS) is tooling-independent.
2. DOI registration timing and DataCite membership route (direct vs via an
   institutional partner) — operational, deferred by CDR-W7-4.
3. Machine-readable change-set format (§91): custom JSON vs an activity-stream
   pattern — decide at first data release.
4. Whether METH documents need their own sub-versioning for investigation-
   specific methods vs one project methodology line (§97).
5. Site-snapshot mechanics (WARC of own site vs static build archive) —
   composes with DR-0006; decide at first public release.
6. TBX adoption trigger: first external professional translation engagement.

## 7. Phase II closure note

This is the final workstream paper. With its DRs decided, the remaining
Phase II obligations are the **consolidation outputs** (per the Phase I
record's Phase II mandate): (1) consolidated domain map; (2) final
standards/model matrix; (3) consolidated conceptual conflict register;
(4) candidate foundational vocabulary; (5) ✅ candidate DRs (delivered
incrementally, 45 enacted so far); (6) candidate requirements with stable
IDs; (7) consolidated unresolved-questions register; (8) the Phase II
methodology version describing how this mapping was performed. After founder
approval of those outputs, Phase II closes and **Phase III — Conceptual
Architecture** may begin.

## 8. Sources

- ISO 15489-1 (records management concepts); ISO 23081 (records metadata)
- ISO 10007 (configuration management guidance); IEEE 828 tradition
- ISO/IEC 11179 (metadata registries) — data-element registration pattern
- W3C SKOS Reference (2009); ISO 30042 TBX
- W3C DCAT 3; DataCite Metadata Schema; Semantic Versioning 2.0.0
- Keep-a-Changelog convention (human-readable changelogs)
- Record §60–61, §87–§102 (the requirements being mapped)
