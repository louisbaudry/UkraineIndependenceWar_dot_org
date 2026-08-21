# Canonical store schema

Implements [SPEC-0001](../docs/specifications/SPEC-0001-conceptual-data-model.md)
under DR-0054 (relational, assertion-centric, append-only canonical store) and
DR-0057 (PostgreSQL as the default implementation candidate).

**Scope of this increment:** the core patterns, the two agent registries, the
pipeline layer, and two epistemic families demonstrating the assertion core.
SPEC-0001 names some fifty object families; the rest instantiate the same
patterns and follow as the layers are needed. Writing all fifty before any
data exists would be speculation, not design.

## Files

| File | Contents |
|---|---|
| `01-enums-generated.sql` | **Generated.** Registry-derived types — do not edit |
| `02-core.sql` | `timespan`, `quantity`, agent registries, the assertion core, append-only enforcement |
| `03-pipeline.sql` | Source registry, collector runs, acquisition attempts, quarantine, preserved objects, preservation events, holdings |
| `04-epistemic.sql` | Propositions, documentary assertions, evidence relations, the cross-family view |
| `gen_enums.py` | Generates `01-` from `registry/dist/registry.json` |
| `tests/` | Test suite and runner |

## Running

```bash
python3 registry/compile.py          # registry -> dist/
python3 schema/gen_enums.py          # dist/ -> 01-enums-generated.sql
./schema/tests/run.sh                # build a fresh database and test
```

`gen_enums.py --check` and `run.sh` exit non-zero on failure, so both can gate
a release baseline (DR-0048).

## How the registry reaches the database

Closed vocabularies (DR-0080) become **enum types**: changing one requires a
Decision Record, and a migration is the appropriate cost of that. Open
vocabularies become **seeded lookup tables**, so a registry-process addition
is a data change rather than a migration.

Either way a value absent from the registry cannot enter the store — which is
what DR-0078 promised.

## Design notes

**The assertion core is enforced by test, not inheritance.** SPEC-0001 §2.1
fixes a common core; §2.2 keeps families separate so payloads get real typing.
PostgreSQL table inheritance would share the columns but compromise foreign
keys, so each family repeats the core and `assertion_core_columns` states the
contract that the suite checks.

**Append-only is enforced in the database, not by convention.** A trigger
refuses `UPDATE` and `DELETE` on every assertion family. The single exception
is governed redaction (DR-0077), which requires a session flag and a complete
tombstone — ground, authority, and time — or it is refused too.

**Nulls never silently mean "no".** `timespan` and `quantity` each carry an
absence state and a check constraint requiring that a value either says
something or says why it says nothing (DR-0029, record §41).

**Triage grades are structurally quarantined.** `source.grade_*` exists for
prioritising attention, and DR-0027 bars it from reaching any assessment. The
column carries a comment saying so; no query computing a likelihood may read
it.

## Tests

The suite executes verification criteria from the REQ documents, naming the
requirement each one verifies — closing the record §99 chain at its last link:
requirement → verification criterion → executable test. 31 tests currently
pass, covering DATA-001/008, ARCH-001, EVID-003/006/010/011/015, EDIT-002,
LEGAL-001, PRES-007/012, SEC-002, and DR-0061/0065/0077.

The suite has been verified to fail when a protection is removed: deleting the
append-only trigger turns the EVID-015 test red rather than leaving it
silently green.
