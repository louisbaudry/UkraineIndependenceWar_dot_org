# DR-0103 — Registration classes: adopt Option A

**Category:** architecture / operations | **Status:** Approved  
**Decided:** 2026-09-15 by founder/principal editor | **Origin:** WP 3.7, CDR-P3-32  
**Supersedes:** — | **Superseded by:** —

## Context

Track A item A5 requires a mechanism to scale source authorization from per-source decisions (thousands, impractical) to per-class decisions (tens of classes plus exceptions, tractable). WP 3.7 proposed three design approaches and recommended Option A: class definitions as a section in the candidate YAML file, with sources naming their class and inheriting policy defaults, overriding specific fields only where needed.

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

## Next step

The founder must decide: **what classes should the project define for the census candidates?** 

WP 3.7 §6 asks three sub-questions:
1. Which ~10–20 candidate classes should exist?
2. What is the grouping principle (jurisdiction, publisher type, combination)?
3. Should classes be shared across multiple candidate files or scoped per file?

Recommendation: Define classes by jurisdiction first (EU, US, UK, Switzerland, Ukraine), then topic second within each jurisdiction (institutional authority, export control, courts, OSINT, etc.). Scope classes per candidate file initially; harmonize later if duplicates emerge.

Once the founder names the classes, implementation can begin.

---

**AI provenance (record §80):** This record was drafted by an AI assistant (Anthropic Claude Code agent session) at the founder's direction, based on WP 3.7 and the founder's choice of Option A. The decision itself — adopting Option A — is the founder's.

