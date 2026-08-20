# SPEC-0001 — Conceptual Data Model

**Class:** SPEC (DR-0046 control) | **Version:** 1.0 | **Status:** Approved — Effective
**Approval:** founder/principal editor, 2026-08-16 | **Effective:** 2026-08-16
**Supersedes:** — | **Superseded by:** —
**Change history:** 0.1 draft deposited 2026-08-16; approved as 1.0 the same day with no content changes beyond this status block and §5's enactment note
**Governed by:** DR-0001…0058; most directly DR-0024 (six layers), DR-0054/0055 (layered, append-only canonical), DR-0050 (registry)

### AI provenance (record §80)

Drafted 2026-08-16 by an AI assistant (Anthropic Claude Code agent session)
from the Phase II outputs and DR-0001…0058, at the founder's direction.
Candidate until approved.

---

## 1. Scope

The conceptual object model of the canonical store: object families, the
assertion pattern they share, and the resolution of the design questions that
gate them (Q-02 PREMIS subset, Q-07 agent registries, Q-09 the holding
bridge, plus the bitemporal and granularity questions raised by WP 3.1).
**Not in scope:** physical DDL, indexes, or engine tuning (implementation
specs); the projection mappings (own SPECs per DR-0056).

## 2. Core patterns

### 2.1 The assertion pattern (used by every layer)

Every assertion family shares a common core:

| Element | Content | Grounding |
|---|---|---|
| `id` | Immutable internal identifier | §15 |
| `subject` | What the assertion is about (typed reference) | |
| `content` | Family-specific payload (typed relation, quantity object, status…) | |
| `valid_time` | World-time validity: time-span with §45 approximations (from/to, each possibly bounded at-least/at-most, possibly open) | DR-0010 (E52 pattern) |
| `asserted_at` | Record time: when the assertion entered the store | bitemporality |
| `asserter` | Pipeline agent (person, software, the project) holding it | DR-0031 (belief pattern) |
| `basis` | Evidence relations and/or inference reference | DR-0024 layers 3/6 |
| `epistemic` | Category (DR-0025), likelihood band + confidence where assessed (DR-0026), absence state where applicable (DR-0029) | |
| `supersedes` | Optional link to the assertion(s) this one supersedes | DR-0055 |
| `redaction` | Tombstone fields, populated only under governed redaction | DR-0055 |

**Bitemporal pattern (resolves WP 3.1 §5 Q1):** explicit `valid_time` +
`asserted_at` columns on assertion families — the plain two-column bitemporal
pattern, not engine-specific temporal tables, keeping the model portable
(DR-0057's separability). "What did we hold at time T" filters on
`asserted_at` and supersession; "what was true of period P" filters on
`valid_time`.

**Granularity (resolves WP 3.1 §5 Q2):** **per-layer assertion families
sharing the §2.1 core** — not one polymorphic assertion table. Rationale:
family-specific payloads get real typing and constraints (DR-0030 quantity
objects, DR-0040 interest types); cross-family queries go through a thin
union view. A single table would push §41's null-discipline into JSON blobs.

### 2.2 The identity pattern

Entities (world layer) and designation-record subjects carry **no name or
identifier columns**. Names, identifiers, and external IDs are assertion
families (`appellation-assignment`, `identifier-assignment`) per DR-0012.
Identity resolution objects — candidate/confirmed/rejected matches,
merge/split lineage (Q-10) — are a further assertion family whose SPEC
follows the identity-workflow study (Phase III item 3).

## 3. Question resolutions proposed by this SPEC

### 3.1 Q-07 — Agent registries: **two registries, linked**

**Pipeline agents** (persons, organizations, software acting on the archive:
collectors, reviewers, models, the founder-as-editor) and **world actors**
(persons/groups as historical subjects) are **separate registries**. A real
person appearing in both gets an explicit, evidence-backed `same-person` link
— never a merge (DR-0004). Rationale: different lifecycles (software versions
vs biographies), different access sensitivities (§11 confidential sources vs
public history), different growth rates; and the link direction keeps
world-layer queries from ever silently traversing into pipeline data.

### 3.2 Q-02 — PREMIS subset: **objects, events, agents, rights core**

Adopted from PREMIS 3.0 for the initial model:

- **Objects:** representation and file levels (bitstream deferred until a
  real case needs sub-file addressing); fixity, size, format, originalName,
  storage location.
- **Events:** ingestion, message-digest calculation, fixity check, format
  identification, virus check, capture, migration/normalization — each with
  date, agents, linked objects, outcome (including failure) and detail.
- **Agents:** the pipeline-agent registry (§3.1) serves as PREMIS agents.
- **Rights:** rights-basis statements per DR-0002's scope (the §14 permission
  set), as an assertion family.
- **Deferred:** environments (hardware/software context), bitstream level,
  preservation-level semantics — revisit triggers recorded in the registry.

### 3.3 Q-09 — The holding bridge: **holding as first-class join object**

A **holding** is the object that says "the archive possesses this": it links
**exactly one LRMoo Item** (documentary identity: which manifestation's
exemplar this is) to **one or more PREMIS representations** (preservation
identity: original representation plus derivative representations), and
carries the §26 completeness statement (original / archival copy /
derivative / screenshot / transcript / fragment / metadata-only) as typed
content. External custodians' copies (§26) are holdings with a
`custodian` other than the project and no representation link. Annotation
targets (DR-0018) resolve through holdings to pinned representations.

## 4. Object family inventory (by layer)

### Pipeline / preservation
`source` · `capture` · `preserved-object` (representation/file) ·
`preservation-event` · `pipeline-agent` · `package` · `collector-run`
(coverage per §57/OPS-006)

### World
`world-actor` (person / group) · `physical-object` (individual) ·
`product-type` · `place` · `world-event` · `period-phenomenon` ·
assertion families: `appellation-assignment` · `identifier-assignment` ·
`role-tenure` · `participation` · `territorial-status` (DR-0044) ·
`object-lifecycle-event` (production, move, custody, seizure)

### Documentary
`work` · `expression` · `manifestation` · `item` · `holding` (§3.3) ·
`annotation` (incl. `quotation`) · assertion families:
`documentary-relation` (reply, forward, thread, cites, mirrors — §25,
DR-0023/0028) · `source-lifecycle-event` (§24) · `accessibility-status`
(§27) · `authorship-role` (§23)

### Epistemic
`proposition` · `documentary-assertion` · `project-assertion` ·
`evidence-relation` · `assessment` (versioned, DR-0026) ·
`hypothesis-set` / `hypothesis` (DR-0035) · `dependence-relation` (DR-0028)
· `source-grade` (triage-only, DR-0027)

### Argument
`argument-structure` · `scheme-application` (inference / conflict /
preference, DR-0032) · `defeater` (typed, DR-0033) ·
`critical-question-response` (DR-0034)

### Legal
`sanctions-regime` · `legal-instrument` (versioned text object) ·
`designation-record` · `legal-effect` · `applicability-conclusion`
(DR-0041) · `interest-statement` (DR-0040) · `classification-assertion` ·
`authorization` (DR-0042) · `transaction` · `shipment` (+legs) · `payment`
(DR-0043) · `enforcement-action` (documentary-first per Q-26) ·
`legal-finding` (§62)

### Governance
`governance-document` (REQ/POL/PROC/DR/SPEC/METH metadata) · `requirement` ·
`registry-entry` · `configuration-item` · `release-baseline` ·
`site-revision` (DR-0052)

Every family's elements get registry entries (DR-0050) at implementation;
enumerations (absence states, interest types, defeater types, completeness
states…) are registry-governed vocabularies, never free text.

## 5. Decision Records arising (enacted)

The three question resolutions proposed by this SPEC were individually
approved by the founder on 2026-08-16 and enacted:

- **DR-0059** — two agent registries, linked (§3.1; resolves Q-07)
- **DR-0060** — initial PREMIS subset (§3.2; resolves Q-02)
- **DR-0061** — the holding object (§3.3; resolves Q-09)

(The bitemporal-pattern and granularity choices in §2.1 are specification
content under this SPEC's own approval, not separate DRs — they bind only
while this SPEC is effective and can be revised by SPEC supersession.)

## 6. Open questions raised

1. Identity-resolution family detail — Phase III item 3 (Q-10).
2. Union-view design for cross-family queries — implementation SPEC.
3. Registry-entry ↔ SPEC element cross-linking mechanics — with Q-30.
4. Whether `legal-instrument` text versions reuse the expression machinery
   (LRMoo) wholesale — likely yes; confirm in the legal-layer SPEC.

## 7. Sources

DR-0001…0058; Phase II outputs 1, 4, 6, 7; PREMIS 3.0 Data Dictionary
(subset selection); LRMoo 1.0 (Item semantics); bitemporal modeling practice
(SQL:2011 discussion in WP 3.1 sources).
