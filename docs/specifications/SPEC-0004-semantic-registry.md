# SPEC-0004 — Semantic Registry Implementation

**Class:** SPEC (DR-0046 control) | **Version:** 0.1 | **Status:** Draft — proposed
**Approval:** pending founder review | **Effective:** upon approval
**Supersedes:** — | **Superseded by:** —
**Governed by:** DR-0050 (11179 pattern, SKOS), DR-0025 (vocabulary changes by DR), DR-0046 (document control), DR-0047 (versioning regimes), DR-0048 (baselines), DR-0054 (layered: canonical + projections), DR-0056 (projection mappings controlled); record §60–61, §96, §101–102; requirements DATA-008, I18N-002/003.
**Resolves:** Q-30.

### AI provenance (record §80)

Drafted 2026-08-16 by an AI assistant (Anthropic Claude Code agent session)
at the founder's direction. Candidate until approved.

---

## 1. Scope

How the semantic registry is stored, structured, changed, versioned, and
served. **Not in scope:** the content of individual entries (seeded per §9,
then grown by registry process), and the presentation of terminology to
readers (presentation layer, §61).

## 2. Source of truth and runtime form (answers Q-30)

**The registry's source of truth is plain files in Git**, and the runtime
registry is a **derived projection** built from them.

This is DR-0054's layering applied to the registry itself:

| Layer | Form | Purpose |
|---|---|---|
| **Source** | YAML files under version control | Authoring, review, diff, history, governance |
| **Projections** | SKOS/RDF (per DR-0050); JSON for runtime validation; human-readable pages | Interchange, enforcement, publication |

Why files rather than a registry service:

- Registry changes **are governance events** (DR-0025/DR-0050), and Git
  already carries governance documents (DR-0046) with review, diff, and
  permanent history.
- The registry is **small** — hundreds of entries, not millions.
- **Zero operational surface**, which WP 3.1 established as a preservation
  property for a single-founder project over decades.
- The source remains **readable without the project's software**, in the
  spirit of PRES-009.

Why YAML rather than authoring in Turtle directly: YAML diffs cleanly and
reads plainly in review, which is where registry changes are actually
scrutinized. SKOS is what the registry *means*, not what it must be typed
in — the SKOS/RDF form is generated, and its mapping is a controlled
artifact under DR-0056.

**Runtime enforcement:** the canonical store validates against the compiled
registry projection — enumerations are enforced from it, so an absence
state or likelihood band that is not in the registry cannot enter the data.
The compiled registry carries its version, and that version is a
configuration item in every release baseline (DR-0047/0048).

## 3. Entry types

| Type | Holds | Example |
|---|---|---|
| `concept` | A defined project concept (SKOS concept) | *holding*, *designation record*, *capture* |
| `vocabulary` | A controlled enumeration and its members | absence states, retention tiers, likelihood bands |
| `data-element` | An 11179-style element: definition, permissible values, stewardship | `valid_time`, `completeness_statement` |
| `relationship-type` | A typed relation and its semantics | dependence relations, territorial statuses |
| `argument-scheme` | A reasoning pattern with its critical questions (DR-0034) | witness testimony, geolocation, document authenticity |
| `identifier-type` | An external identifier system (§16, DR-0012) | Wikidata, OpenSanctions, LEI, IMO, MMSI |

## 4. Entry structure

Every entry carries:

- **Identity:** stable registry ID (never reused, never re-pointed), type,
  layer (per SPEC-0001's families).
- **Meaning:** definition; scope notes; usage notes; **what it is not**,
  where a conflict-register entry applies (Phase II output 3).
- **Labels:** `prefLabel` and `altLabel` per language, plus
  **forbidden/misleading translations** (§60) — recorded as explicit
  negative guidance, not omission.
- **Structure:** broader / narrower / related links; for vocabularies, the
  member list with each member's own definition; for schemes, the critical
  questions.
- **Mappings:** `exactMatch` / `closeMatch` / `relatedMatch` to external
  vocabularies (CIDOC CRM classes, PREMIS, PROV, FtM, BODS, Wikidata, PHIA
  bands, …), each with the mapping's own note where fit is imperfect.
- **Governance:** registration status (§5); effective date; stewardship;
  **links to the DRs, SPECs, and REQs that authorize or depend on it**;
  version history; `replacedBy` where deprecated.

The DR/SPEC/REQ links are what make DATA-008 auditable: every consequential
data element traces to the decision that created it.

## 5. Registration status lifecycle

| Status | Meaning |
|---|---|
| `draft` | Proposed; **may not appear in data** |
| `effective` | Usable in canonical data |
| `deprecated` | Readable in existing data; **not permitted for new data**; carries `replacedBy` and a migration note (§96) |
| `retired` | No longer applicable; retained for historical interpretation only |

Nothing is ever deleted from the registry: a dataset can outlive the
vocabulary it used, and §96 exists precisely so its meaning survives.

## 6. Change classes — where a DR is required

DR-0025 and DR-0050 draw the line between registry process and Decision
Record. This SPEC makes it operative:

| Class | Examples | Route |
|---|---|---|
| **Editorial** | Typo; clarified wording that does not change meaning; added translation; added scope note | Registry process; recorded in registry history |
| **Additive** | New member in an **open** vocabulary; new external mapping; new alt label; new argument scheme | Registry process; recorded, with rationale |
| **Structural** | Changing a definition's **meaning**; removing or deprecating a member; changing an enumeration that data depends on; changing relationship semantics; opening or closing a vocabulary | **Requires a Decision Record** (DR-0025), plus version, migration note, deprecation, and replacement mapping (§96) |

Vocabularies are marked **open** (may grow by registry process) or
**closed** (any change is structural). The vocabularies fixed by DR —
epistemic categories, absence states, likelihood bands, entity statuses,
retention tiers, defeater types — are **closed** by construction: they were
each set by a Decision Record and can only be changed by one.

## 7. Versioning and releases

- The registry carries an **explicit version** under DR-0047's
  ontology/vocabulary regime — not SemVer, but a version with a changelog,
  deprecations, and replacement mappings.
- **Every release baseline pins a registry version** (DR-0048); a dataset
  release is interpretable only against the registry version it names.
- Registry changes appear in release change sets alongside merged/split/
  retracted object mappings (§91).

## 8. Multilingual governance

- **English is the authoring language**; other languages are governed
  translations, not derivations.
- A translated label is **an entry with provenance**: translator, date,
  review status (§60). Machine translation may propose; it never becomes an
  authoritative label without human review (§60: translation memory does not
  establish terminological authority; AI-001).
- **Forbidden-translation notes are first-class** — e.g., renderings that
  turn "likely" into near-certainty, or "roughly even chance" into
  "possible" (DR-0065), and any rendering that collapses a conflict-register
  distinction (Phase II output 3).
- Which languages are carried, and in what order, is an operational
  decision; the subject matter makes Ukrainian and Russian the first
  priorities after English.

## 9. Seed contents

The registry is not speculative: enacted DRs have already assigned it
concrete vocabularies. The initial seed comprises at least —

**Epistemic:** epistemic categories (DR-0025) · likelihood bands with PHIA
mappings (DR-0065) · analytic confidence (DR-0026) · absence states
(DR-0029) · quantity semantic types (DR-0030) · source-grade axes (DR-0027)
· dependence relation types (DR-0028)

**Argument:** defeater types (DR-0033) · seed argument schemes with critical
questions (DR-0034)

**Identity:** entity statuses (DR-0062) · match states and review tiers
(DR-0063)

**Documentary & preservation:** completeness states (DR-0061) · PREMIS event
types (DR-0060) · retention tiers (DR-0068) · rights permissions (§14) ·
access tiers (§12) · source types (DR-0067)

**Legal:** interest types (DR-0040) · territorial statuses (DR-0044) ·
classification systems (DR-0042)

**Governance:** document statuses (DR-0046) · registration statuses (§5)

**Cross-cutting:** the 39 **conflict-register resolutions** (Phase II output
3) as scope notes on the terms they disambiguate.

## 10. Candidate Decision Records (proposals — require founder approval)

- **CDR-P3-25:** **Registry source of truth is YAML files in Git; runtime
  and interchange forms are derived projections** (SKOS/RDF, JSON), with the
  compiled registry enforcing enumerations in the canonical store and its
  version pinned in every release baseline. Resolves Q-30.
- **CDR-P3-26:** Adopt the **entry typology and entry structure** (§3–4),
  including mandatory links to authorizing DRs/SPECs/REQs (DATA-008) and
  explicit forbidden-translation notes.
- **CDR-P3-27:** Adopt the **registration status lifecycle** (§5) with
  nothing ever deleted, and the **change-class rule** (§6) fixing where a
  Decision Record is required; DR-set vocabularies are closed by
  construction.
- **CDR-P3-28:** Adopt **English as authoring language with governed
  translation** (§8): translated labels carry translator, date, and review
  status; machine translation proposes but never authorises.

## 11. Open questions raised

1. Registry compilation tooling and validation (implementation).
2. Whether registry pages are published publicly from the outset, or after
   the first release (product decision; §61).
3. Language priority beyond English/Ukrainian/Russian (operational).
4. Whether argument schemes' critical questions need their own sub-registry
   as the library grows (revisit at ~20 schemes).

## 12. Sources

DR-0025, DR-0046, DR-0047, DR-0048, DR-0050, DR-0054, DR-0056, and the
vocabulary-setting DRs listed in §9; record §60–61, §96, §101–102;
ISO/IEC 11179 registration pattern; W3C SKOS Reference.
