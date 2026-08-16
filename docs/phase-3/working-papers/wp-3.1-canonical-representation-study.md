# Phase III / Study 1 — Canonical Representation
## Working Paper 3.1

**Project:** Ukraine's Second War of Independence
**Status:** CANDIDATE — AI-drafted, awaiting founder review and approval.
**Version:** 3.1 (first Phase III working paper)
**Mandate:** Q-01 / record §95 — compare relational-first, RDF/OWL-first, layered, and other canonical-representation models **against actual requirements**, and recommend.
**Constraints inherited:** every enacted DR; most bindingly DR-0003/0031 (everything reified with provenance), DR-0024 (six layers), DR-0026/0029/0030 (typed uncertainty/absence/quantity), DR-0047/0048 (versioning, baselines), PRES-009 (archive reconstructible), AI-001/EDIT-001 (human accountability); the record's warning that nothing is chosen "because it sounds more sophisticated."

### AI provenance (per record §80)

| Field | Value |
|---|---|
| Drafted by | AI assistant (Anthropic Claude Code agent session), at the founder's direction to continue into Phase III |
| Date | 2026-08-16 |
| Inputs | Phase II outputs 1–8; DR-0001…0053; candidate requirements (output 6) |
| Human review | **Pending** — founder is final editor |
| Disposition | Candidate; its candidate DRs are proposals |

---

## 1. What the requirements actually demand of the canonical store

Extracted from the enacted DRs and the 63 candidate requirements, the load-
bearing properties are:

1. **Assertion-centric reification everywhere.** Names, identifiers, roles,
   ownership, sanctions states, territorial statuses, epistemic assessments —
   all are *statements with provenance, time, and status*, not attribute
   values (DR-0012/0013/0024/0031/0040/0044). The store's native shape is
   "statement about a statement," at scale.
2. **Bitemporality.** What was asserted about period P, and what did *we*
   believe at time T (§45, §63, EVID-015). Legal effective time, event time,
   and record time never collapse (C-38).
3. **Append-only revision.** Prior epistemic states and published baselines
   are never rewritten (DR-0048, EDIT-002); correction is supersession.
4. **Typed, constraint-checked vocabularies.** Absence states, likelihood
   bands, quantity semantics, interest types — enumerations with validation
   (DR-0026/0029/0030, DATA-008), where silent nulls are a defect (§41).
5. **Path queries in bounded shapes.** Ownership chains for rule-derived
   applicability (DR-0041), dependence chains (DR-0028), derivation chains
   (DR-0003) — recursive but bounded traversals with full path capture.
6. **Standards-shaped exports.** RDF ontologies (CRM, CRMinf, PROV, SKOS,
   Web Annotation), FtM JSON, BODS JSON, DCAT — all mandatory *interchange*
   surfaces (DR-0017/0032/0040/0045/0049/0050).
7. **Durable reconstructibility.** The canonical store must export to formats
   a future archivist can read without the original software (PRES-009,
   DR-0001 designated-community reasoning).
8. **Operational reality.** One founder, AI assistance, decades-long horizon
   (record §1, §5): the canonical store must be boring, widely understood,
   self-hostable, and cheap to keep alive — operational simplicity is a
   *preservation* property here, not a convenience.

## 2. The alternatives, against those demands

### 2.1 RDF/OWL-first (triple store canonical)

**For:** the adopted ontologies are RDF-native; interchange is identity, not
projection; W3C longevity.
**Against, on requirements:** requirement 1 is RDF's weak point — statement-
level provenance forces reification machinery (named graphs, RDF-star) that
every query then carries; requirement 2 (bitemporality) has no standard
treatment; requirement 4's closed-world validation runs against OWL's
open-world semantics (SHACL exists but adds a second modeling layer);
requirement 8 fails hardest — triple stores are a thin operational talent
pool for a single-founder, decades-horizon project. OWL reasoning, the
technology's distinctive payoff, is something the project has explicitly
constrained (DR-0036: no computation adjudicates).

### 2.2 Property-graph-first (graph DB canonical)

**For:** requirement 5's traversals are native.
**Against:** no standards alignment (requirement 6 all becomes custom
projection anyway); vendor-specific data models and query languages against a
decades horizon; statement-level temporality and validation are no better
than relational; WP 0.1's no-go instinct ("do not choose a graph database")
was pointing at real risk. Traversal performance alone does not earn
canonical status — the ownership and dependence graphs are bounded (thousands
to low millions of edges), not web-scale.

### 2.3 Document/event-store canonical (append-only log + views)

**For:** requirement 3 is native; flexible statement shapes.
**Against:** requirement 4 (typed validation) and cross-statement integrity
land entirely on application code; queryability of requirement 5 requires
building the very projection layer that then *becomes* the de facto canonical
store. The append-only *discipline* is the valuable part — it does not
require an event-store *product*.

### 2.4 Relational-first (canonical), semantics by projection

**For:** requirement 1 — assertion tables with provenance columns are the
oldest trick in the relational book, queryable without ceremony; requirement
2 — bitemporal patterns are mature relational practice; requirement 3 —
append-only is a schema discipline plus permissions; requirement 4 —
constraints, enums, and foreign keys are native, and "unknown ≠ null ≠ no" is
enforceable; requirement 5 — recursive CTEs handle bounded traversals with
path capture (and a graph projection remains available if scale ever demands
it); requirement 7 — SQL, CSV/JSONL dumps are the most archivally durable
data surfaces in existence; requirement 8 — PostgreSQL is the reference
boring technology: open source, three decades old, universal talent pool.
**Against:** requirement 6 is *not* native — every standards surface (RDF,
FtM, BODS, DCAT) must be built as a projection, and the mappings must be
maintained as first-class, versioned artifacts or interchange quietly rots.
Schema evolution is real work (mitigated by DR-0047's migration discipline).

### 2.5 Layered: relational canonical + derived projections

Option 2.4 with the projection obligation made structural rather than
incidental: the canonical store is relational and assertion-centric; RDF
(CRM/CRMinf/PROV/SKOS/Web Annotation), FtM, BODS, DCAT, search indexes, and
any graph-analysis views are **derived, rebuildable projections** carrying
their generator's version (DR-0003, DR-0047). This is also the shape the
project's own principles predict: Principle 18 ("the website is a
projection") generalizes — *every* interchange and analysis surface is a
projection of one canonical evidence store.

## 3. Recommendation

**Adopt the layered model (2.5): a relational, assertion-centric,
append-only canonical store, with all semantic, interchange, analysis, and
publication surfaces as derived, versioned, rebuildable projections.**
PostgreSQL is the default implementation candidate; the DBMS choice itself is
an implementation decision that the specification (Phase III item 2) records
separately, so the *representation* commitment survives any engine change.

What this recommendation deliberately does **not** do: it does not put OWL
semantics in the canonical path (DR-0036 alignment), does not preclude a
graph database later as a *projection* (requirement 5 fallback), and does not
weaken the RDF commitments — the adopted ontologies govern the projections'
shapes, and projection-mapping specs become controlled SPEC documents.

## 4. Candidate Decision Records (proposals — require founder approval)

- **CDR-P3-1:** Canonical representation is **layered**: a relational,
  assertion-centric canonical store; every semantic (RDF), interchange (FtM,
  BODS, DCAT), search, graph-analysis, and publication surface is a derived,
  rebuildable projection whose generator is versioned (DR-0047) and
  provenance-recorded (DR-0003). This answers record §95 / Q-01.
- **CDR-P3-2:** The canonical store is **append-only for assertions**:
  corrections and revisions are superseding statements (§63, §77, DR-0048);
  deletion exists only as governed redaction (§77's legal/privacy cases) with
  a preserved tombstone.
- **CDR-P3-3:** **Projection mappings are controlled artifacts**: each
  standards surface (CRM/CRMinf/PROV/SKOS/Web Annotation RDF; FtM; BODS;
  DCAT) has a versioned SPEC-class mapping document (DR-0046), and known
  export losses are documented per surface (extends DR-0045's obligation).
- **CDR-P3-4:** **PostgreSQL is the default implementation candidate** for
  the canonical store; the binding engine choice is recorded in the
  conceptual-data-model SPEC with a revisit trigger, keeping representation
  (this DR set) independent of engine.
- **CDR-P3-5:** **Durable export is a standing obligation**: the canonical
  store ships a documented, complete dump format (JSONL + CSV + schema
  descriptor) exercised at every release baseline (DR-0048, PRES-009) — the
  archive outlives the database product.

## 5. Open questions raised (feed the Phase III register)

1. Bitemporal implementation pattern (valid-time/record-time columns vs
   temporal tables) — conceptual-data-model SPEC.
2. Assertion-table granularity: one polymorphic assertion relation vs
   per-layer families — SPEC, informed by Q-02 (PREMIS subset) and Q-07.
3. When, if ever, a graph projection materializes (trigger: traversal
   performance on real ownership networks).
4. Redaction mechanics under CDR-P3-2 (tombstone content, §77 legal cases).

## 6. Sources

- Phase II outputs 1–8 and DR-0001…0053 (requirement base)
- Record §95 (the question), §63/§77 (revision semantics), Principle 18
- PostgreSQL documentation (temporal patterns, recursive CTEs); SQL:2011
  temporal features; RDF-star/named-graph reification trade-offs (W3C);
  SHACL vs OWL validation semantics (W3C)
