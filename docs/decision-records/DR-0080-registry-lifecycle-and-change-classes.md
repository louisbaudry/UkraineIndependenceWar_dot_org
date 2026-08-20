# DR-0080 — Registry lifecycle and change classes

**Category:** architecture / methodology | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-27, SPEC-0004 §5–6 | **Supersedes:** — | **Superseded by:** —

## Context

DR-0025 and DR-0050 require structural vocabulary changes to go through
Decision Records while routine entries follow a registry process — without
specifying the boundary. Record §96 requires meaning-changing changes to
carry version, migration, deprecation, and replacement mapping.

## Alternatives considered

1. Four-status lifecycle plus an explicit three-class change rule (chosen).
2. Leave the boundary to judgment (rejected: the distinction is exactly
   where silent semantic drift enters).

## Decision

**Registration statuses:** `draft` (may not appear in data) → `effective`
(usable) → `deprecated` (readable in existing data, not permitted for new
data, carries `replacedBy` and a migration note) → `retired` (historical
interpretation only). **Nothing is ever deleted from the registry** — a
dataset can outlive the vocabulary it used, and §96 exists so its meaning
survives.

**Change classes:**

| Class | Examples | Route |
|---|---|---|
| **Editorial** | Typo; clarified wording not changing meaning; added translation; added scope note | Registry process, recorded |
| **Additive** | New member in an **open** vocabulary; new external mapping; new alt label; new argument scheme | Registry process, recorded with rationale |
| **Structural** | Changing a definition's meaning; removing or deprecating a member; changing an enumeration data depends on; changing relationship semantics; opening or closing a vocabulary | **Decision Record required**, plus version, migration note, deprecation, replacement mapping (§96) |

Vocabularies are marked **open** or **closed**. Vocabularies fixed by
Decision Record — epistemic categories, absence states, likelihood bands,
entity statuses, retention tiers, defeater types, and the rest of SPEC-0004
§9's DR-set seed — are **closed by construction**: set by a DR, changeable
only by a DR.

## Consequences

- DR-0025's rule becomes operative rather than a matter of judgment.
- Semantic drift requires a visible governance act.
- Ontology versioning (§96) has its trigger defined.
