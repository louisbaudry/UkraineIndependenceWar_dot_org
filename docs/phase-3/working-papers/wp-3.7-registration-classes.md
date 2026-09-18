# WP 3.7 — Registration classes for bulk authorization

**Project:** Ukraine Independence War Archive | **Status:** CANDIDATE — AI-drafted, awaiting founder review  
**Version:** 0.1 | **Mandate:** WP 3.4 Track A item A5 ("Draft the registration-class mechanism")  
**Constraints inherited:** WP 3.4 §1, DR-0067 (registry schema), OPS-001 (registration as authorisation)

---

## 1. The problem: decision scale vs. founder time

WP 3.4 §6 names the bottleneck plainly. The acquisition strategy yields thousands of candidate sources from the census (A2). Each requires a founder decision to authorize collection (OPS-001); without registration classes, that is thousands of individual authorizations — roughly two minutes per source across policy fields and verification, or **months of founder time** for a foundational corpus.

The mitigation: group sources by policy class and have the founder decide once per class, with individual exceptions for sources that deviate. That turns thousands of registrations into **tens of class rulings plus exceptions** — a tractable decision load.

This proposal designs the class mechanism. It does not invent the classes themselves; those are policy decisions for the founder to make (e.g., "EU institutional sanctions authorities", "OSINT aggregators", "court and tribunal records") alongside deciding whether each proposed class should authorize collection at all.

---

## 2. What a class carries: the policy fields

DR-0067's registry schema requires these fields per source (current sanctions-authorities.yaml):

| Category | Field | Current status |
|---|---|---|
| **Identity** | key, source_type, name, locator, publisher, jurisdiction | *required per source; distinct across all sources* |
| **Context** | primary_languages, coverage_start | *required per source* |
| **Collection policy** | collection_method, collection_cadence, scope_rules, exclusions, rate_limits | *required per source* |
| **Preservation** | capture_format, default_retention_tier | *required per source* |
| **Access** | default_access_tier, expects_graphic_content | *required per source* |
| **Rights** | rights_permission, rights_basis | *required per source* |
| **Triage** | grade_source_reliability, grade_item_credibility | *optional per source* |
| **Dependence** | declared_dependence_links | *per source if applicable* |

A **class** would carry defaults for all fields in the Collection policy, Preservation, Access, Rights, and Triage categories — those that express *how to treat* a source rather than *what* it is. Identity and Context fields are inherently per-source and remain mandatory.

Example class: **"EU institutional sanctions authorities"**
```yaml
class: EU-institutional-sanctions
name_pattern: "EU — {source_name}"
collection_method: http
collection_cadence: daily
capture_format: warc
default_retention_tier: permanent
default_access_tier: public
rights_permission: may-redistribute
rights_basis: "Reuse under EU Decision 2011/833/EU, subject to acknowledgement. See legal review §10."
grade_source_reliability: A
expects_graphic_content: false
```

A source using this class would need only:
```yaml
key: eu-consolidated-list
class: EU-institutional-sanctions          # inherit from class
name: EU Consolidated Financial Sanctions List
locator: https://webgate.ec.europa.eu/fsd/...
jurisdiction: EU
coverage_start: 2009-06-27
scope_rules: >                             # exception: more specific than class default
  Financial designations under the Ukraine/Russia programmes,
  and instrument consolidated texts only.
# All other policy fields inherited from the class
```

---

## 3. Three design options

### Option A — Class as a separate YAML section (Recommended)

**Structure:** A `classes:` section in the YAML file defines all classes once, then sources name their class and add overrides.

```yaml
classes:
  EU-institutional-sanctions:
    collection_method: http
    collection_cadence: daily
    capture_format: warc
    default_retention_tier: permanent
    default_access_tier: public
    rights_permission: may-redistribute
    rights_basis: "EU Decision 2011/833/EU…"
    grade_source_reliability: A
    expects_graphic_content: false

  US-institutional-export-control:
    collection_method: http
    collection_cadence: daily
    capture_format: warc
    default_retention_tier: permanent
    default_access_tier: public
    rights_permission: may-provide-subscribers
    rights_basis: "US federal public domain / ITAR…"
    grade_source_reliability: A
    expects_graphic_content: false

sources:
  - key: eu-consolidated-list
    class: EU-institutional-sanctions
    name: EU Consolidated Financial Sanctions List
    locator: https://webgate.ec.europa.eu/...
    jurisdiction: EU
    coverage_start: 2009-06-27
    scope_rules: "Financial designations, Ukraine/Russia only…"
    # other fields inherited from class, or can override
```

**Pros:**
- Classes are explicit and reusable
- Overrides are visible and deliberate (deviation is obvious)
- Schema change is minimal; no database refactoring needed
- `register.py` logic is straightforward: merge class defaults, then apply per-source values

**Cons:**
- File grows as classes accumulate, but this is mitigated by grouping classes by file
- Founder must name classes deliberately (e.g., when does a new class start? when does an exception belong in the class vs. the source?)

---

### Option B — Inline class reference with field override list

**Structure:** Classes defined elsewhere; sources name class and explicitly list which fields override class defaults.

```yaml
classes:
  # (same as Option A)

sources:
  - key: eu-consolidated-list
    class: EU-institutional-sanctions
    name: EU Consolidated Financial Sanctions List
    locator: https://webgate.ec.europa.eu/...
    jurisdiction: EU
    coverage_start: 2009-06-27
    scope_rules_override: "Financial designations, Ukraine/Russia only…"
    # Everything else from EU-institutional-sanctions; no silent defaults
```

**Pros:**
- Makes exceptions ultra-explicit; less risk of accidental field inheritance
- Clearer audit trail (exactly which source fields override which class fields)

**Cons:**
- Every override requires an `_override` suffix or extra metadata, making the file verbose
- More code complexity in merge logic
- `register.py` must maintain two parallel field lists (class fields, overrides)

---

### Option C — Classes in the database schema

**Structure:** Classes registered as separate entities in the database; sources reference class IDs; overrides stored as delta rows.

```yaml
# YAML remains unchanged; classes are defined and registered separately
sources:
  - key: eu-consolidated-list
    class_id: 42  # the EU-institutional-sanctions class registered in the db
    class_override_jurisdiction: EU  # only if different from class default
    name: EU Consolidated Financial Sanctions List
    locator: https://webgate.ec.europa.eu/...
    # ... other source-specific fields
```

**Pros:**
- Full audit trail (class history, when it was changed, which sources reference it)
- Class updates can be versioned
- Registry consistency (one source of truth in the database)

**Cons:**
- Requires schema additions (sources.class_id, sources.class_override_* columns)
- Requires schema versioning / migration (complexity for this project)
- Makes candidate files harder to read (class_id is opaque until queried in database)
- Founder can't easily review a class before authorizing all sources that use it

---

## 4. Recommendation

**Option A is recommended** for these reasons:

1. **Founder clarity:** Classes are explicit in the file; the founder reviews what they are authorizing
2. **Policy transparency:** Policy decisions (class definitions) are visible alongside collection decisions (per-source selections)
3. **Implementation simplicity:** `register.py` already merges YAML with database; adding a class merge step is straightforward
4. **Schema stability:** No database migration; changes scoped to the candidate file format
5. **Scale match:** A sanctions-authorities YAML with 20 classes and 200 sources is still readable; if it grows beyond that, split into thematic files (EU, US, export control, courts, OSINT, etc.)

Option B's explicitness is valuable but verbose for this use case. Option C's audit trail is valuable but premature — classes are not expected to change frequently during the foundational corpus phase.

---

## 5. Implementation sketch

### Changes to `sources/register.py`

1. Extend `load_candidates()` to extract `classes:` sections separately from `sources:`
2. Add `merge_class_defaults(source, classes)` function:
   - For each policy field not present in source, look it up in source's named class
   - Return merged dict
3. Update `validate()` to check that:
   - All named classes exist in the classes dict
   - Inherited + overridden fields still satisfy REQUIRED and policy constraints
   - Class definitions themselves are valid (complete, no cycles)
4. Update `register()` to store only per-source values in the database:
   - source.class_name (or null if source defines its own values)
   - source.policy_overrides (JSON or nullable text; omitted if empty)
   - The merged values are computed on read by repeating the merge

### Changes to the schema

The database schema (schema/03-registry.sql) stores per-source values, not class definitions. No schema change is required; class definitions live only in candidate files and in register.py's working memory. On registration, the merged values are stored as-is in the registry table.

**Consequence:** If a class definition changes after registration, already-registered sources keep their merged values (frozen at registration time). Updating a registered source requires a new registration record with new values, which is correct because registration is an authorization decision (not a declaration that gets silently updated).

---

## 6. What the founder must decide

This proposal designs *how* classes work. Before the implementation, the founder must decide:

**Decision:** Should the project adopt the class mechanism for source registration? If yes:

1. **Which classes should exist for the census candidates?** The brief should name ~10–20 candidate classes based on the source characteristics (jurisdiction, publisher type, topic area, format, rights posture). These become the "classes" section in the YAML once authorized.

2. **Class grouping principle:** Should classes cluster by:
   - Jurisdiction (EU, US, UK, Switzerland, Ukraine)? 
   - Publisher type (institutional authority, OSINT aggregator, court, media)?
   - Topic area (sanctions, export control, war crimes, damage assessment)?
   - Some combination?
   
   The recommendation is a two-level scheme: jurisdiction first (grouping related sources by country/bloc), topic second (so "EU institutional sanctions authorities" and "EU export-control authorities" are separate but sibling classes).

3. **Timing:** Implement before or after the first retrospective recovery (WP 3.4 Track B, Wave B2)? The recommendation is *before B2 starts* — classes should be in place before thousands of candidates flood the queue, not retrofitted afterward.

---

## 7. Open questions raised

1. **Should class definitions be versioned?** If the founder refines what "EU institutional sanctions authority" means, should old registrations carry the v1 definition or be re-recorded under v2? The recommendation: no versioning (classes are frozen at their definition time; refinement means a new class name), but this is cosmetic if class changes are rare.

2. **Can a source belong to multiple classes?** The recommendation: no, one source per class, for simplicity. If a source truly straddles two classes, it should define its own values (no class reference) and note why it is exceptional.

3. **Should classes be shared across multiple candidate files (e.g., sanctions-authorities.yaml, courts.yaml)?** The recommendation: not in this proposal. Each candidate file carries its own classes section. If class definitions duplicate, that is visible and can be harmonized when the next file arrives. Deduplication can happen later if needed.

4. **How does the class mechanism interact with Track B's per-class decisions?** WP 3.4 §4.2 (Wave B1) has the founder "accept, amend, or reject by class and exception". This proposal assumes that means classes are defined beforehand (here) and B1 authors a full DR-0067 registration for each class exception (not each individual source). This is tractable and reduces founder load from thousands of decisions to dozens.

---

## 8. Candidate Decision Records

This paper does not raise a new candidate DR. **CDR-P3-32** (WP 3.4 §8:
"`register.py` accepts a *class* template carrying every DR-0067 field
group, which the founder approves once; individual sources register under
it by inheritance, with per-source exceptions stated explicitly") already
names this mechanism, deposited 2026-09-08. This paper is the design that
discharges it: Option A above is the founder's chosen shape for CDR-P3-32,
and DR-0103 enacts it.

No decision is outstanding on the mechanism itself unless the founder
rejects Option A or proposes a different approach. Implementation is done
(`sources/register.py`, `sources/tests/test_register_classes.py`); what
remains is the founder naming the initial set of classes and authorizing
the class definitions per candidate file.

---

## 9. Sources

- WP 3.4 §6 (the bottleneck)
- DR-0067 (registry schema)
- OPS-001 (registration as authorisation)
- `sources/register.py` (current implementation)
- `sources/candidates/sanctions-authorities.yaml` (current candidate format)
- `sources/README.md` (registration workflow)

