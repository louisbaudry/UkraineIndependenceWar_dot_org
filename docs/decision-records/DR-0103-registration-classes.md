# DR-0103 — Registration classes: adopt Option A

**Category:** architecture / operations | **Status:** DECIDED — enacted 2026-09-18  
**Decided:** 2026-09-15 by founder/principal editor | **Implemented:** 2026-09-16 | **Enactment:** 2026-09-18 | **Origin:** WP 3.5, CDR-P3-32  
**Supersedes:** — | **Superseded by:** —

## Context

Track A item A5 requires a mechanism to scale source authorization from per-source decisions (thousands, impractical) to per-class decisions (tens of classes plus exceptions, tractable). WP 3.5 proposed three design approaches and recommended Option A: class definitions as a section in the candidate YAML file, with sources naming their class and inheriting policy defaults, overriding specific fields only where needed.

The founder has decided to adopt Option A.

## Alternatives considered

1. **Option A — Classes in YAML** (chosen): Class definitions grouped in a `classes:` section of the candidate file; sources name their class and add overrides; merged values stored in the registry at registration time. Simple to implement (register.py merge logic); no database schema changes; founder sees classes explicitly.

2. **Option B — Inline class reference with override syntax**: Sources list which fields override class defaults with `field_override` syntax. More verbose and explicit about deviations; higher implementation complexity.

3. **Option C — Classes in database schema**: Classes registered as entities with full audit history; sources reference class IDs with delta rows. Full versioning and consistency; premature for this use case (classes are not expected to change often).

## Decision

The project adopts **Option A**. Classes are defined in YAML, candidate files structure their `sources:` section with references to a `classes:` section in the same file, and policy defaults flow from class to source at registration time.

**Implementation commitments:**

1. **`sources/register.py` changes:**
   - Extend `load_candidates()` to extract and store class definitions separately
   - Add `merge_class_defaults(source, classes)` function to inherit class fields
   - Update `validate()` to check class references and merged fields against REQUIRED and policy constraints
   - Update `register()` to merge class defaults into each source before storing in the registry

2. **Schema: no changes.** Class definitions are not stored in the database; they exist only in candidate files. At registration, merged values are stored as-is in the registry table (no separate class_id column). This means:
   - Classes frozen at their definition time (no silent updates to registered sources if class definition changes)
   - Straightforward audit trail: every registered source carries the exact merged values that were authorized
   - If a class is refined later, re-registration under a new class name is the path forward

3. **Candidate file format change:**
   ```yaml
   classes:
     class-name-1:
       field: value
       ...
     class-name-2:
       field: value
       ...
   
   sources:
     - key: source-key
       class: class-name-1
       name: Source Name
       # identity and context fields (always per-source)
       # policy fields inherited from class, or overridden here
   ```

4. **Timing: before Track B Wave B2.** The class mechanism must be in place, tested, and the initial set of classes authorized before retrospective recovery begins (WP 3.4 Track B Wave B2). This prevents thousands of unclassified candidates from accumulating in the queue.

## Consequences

1. **Decision scale reduction.** Authorization moves from per-source (thousands of founder decisions) to per-class (tens of decisions) plus exceptions. Founder time burden drops from months to days for the foundational corpus.

2. **Policy transparency.** Classes are explicit in the candidate file, so the founder sees what policies they are authorizing and which sources use them.

3. **Implementation scope.** `sources/register.py` grows by ~100 lines (class loading, merge logic, validation). One new test suite (`sources/tests/test_register_classes.py`) covering merge, inheritance, override, and edge cases.

4. **Follow-up decision required.** The founder must name the initial set of classes (grouping principle: jurisdiction? publisher type? both?) before implementation begins. This is a separate, subsequent decision.

5. **Immutability of registered sources.** Once registered, a source carries frozen merged values. If a class definition is later refined, that affects only future registrations under the new or updated class name. Existing registrations do not silently update. This is correct behavior: registration is an authorization decision, not a declaration.

## Implementation status

**Completed 2026-09-16:**
- `sources/register.py` extended with class loading, merging, validation
- `sources/tests/test_register_classes.py` created with 18 passing tests
- Initial class set defined in `sources/candidates/sanctions-authorities.yaml` (6 jurisdiction-based classes: EU, US export control, UK, CH, UA)
- All 7 candidates validate successfully
- Merged to main (PR #29, 2026-09-16)

**Classes defined (jurisdiction-first grouping):**
1. EU-institutional-sanctions
2. US-institutional-sanctions
3. US-institutional-export-control
4. UK-institutional-sanctions
5. CH-institutional-sanctions
6. UA-state-investigations

**Policy fields inherited:** collection_method, collection_cadence, capture_format, default_retention_tier, default_access_tier, expects_graphic_content, rights_permission, rights_basis, grade_source_reliability, grade_item_credibility.

## Next step

1. **Execute pending A1 registrations** using the class mechanism:
   - `uk-ofsi-consolidated` (approved DR-0096, 2026-09-12)
   - `bis-entity-list` (approved DR-0096, 2026-09-12)
   - `seco-sanctions` (approved DR-0098, 2026-09-14)
   
   Execution is on the archive server per each source's How to execute; not a session-side task.

2. **Define additional classes as census discovers more candidates** — grouping by jurisdiction first, then topic/authority type within each jurisdiction.

3. **Refine class definitions** if patterns emerge; new/updated class names enable graceful evolution without affecting frozen past registrations.

---

**AI provenance (record §80):** This record was drafted by an AI assistant (Anthropic Claude Code agent session) at the founder's direction, based on WP 3.5 and the founder's choice of Option A. The decision itself — adopting Option A — is the founder's.

