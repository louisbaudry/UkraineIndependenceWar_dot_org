# OCFL storage

At-rest storage for preserved bytes, implementing DR-0073 (OCFL 1.1 as the
archival layout, objects as AIP containers), DR-0074 (an object is a
holding), DR-0075 (SHA-512 content addressing, SHA-256 fixity block) and
DR-0076 (tier-separated roots, hashed n-tuple layout).

```bash
python3 storage/tests/test_ocfl.py    # 24 tests; exits non-zero on failure
```

## Library or direct implementation — WP 3.3 §8 Q1, resolved

WP 3.3 left this open, to be decided at build time. It recorded the argument
for a library plainly: *existing libraries are validated*, and a hand-rolled
implementation risks subtle non-conformance in an archival format. That
argument was taken seriously. The evidence at build time was:

| Candidate | Outcome |
|---|---|
| **ocfl-py** (by an OCFL editor; reference quality, includes a validator) | **Does not install.** Its `pairtree` dependency is Python 2-era and fails to build. |
| **ocflcore 0.1.0** | Installs, but has **no fixity-block support** — which DR-0075 requires — and its 0.x API does not match its own documentation. |

So the layer is implemented directly. This is not a preference for writing
our own; it is what the evidence left.

### What that costs, and how it is covered

The library argument was about *validation*, and losing it is a real cost.
It is partly covered by `validate_object()`, which checks written objects
against the OCFL 1.1 requirements this project depends on: namaste
declarations, inventory required fields, the digest algorithm and fixity
block DR-0075 mandates, sidecar agreement, a complete `v1..vN` sequence with
`head` last, every version-state digest present in the manifest, per-version
inventory copies, and content matching both recorded digests.

**It is deliberately not a complete OCFL validator.** It checks our
dependencies, not the whole specification.

**Open item:** independent third-party conformance validation. When
`ocfl-py` becomes installable — or another validated implementation appears
— objects written here should be validated against it, and any divergence
treated as a defect in this code rather than in the objects' design. Until
then the archive's conformance rests on this implementation plus its tests,
which is weaker than WP 3.3 hoped for and is recorded as such.

This matters because PRES-009 requires the archive to be readable without
this code: what must conform is the bytes on disk, not the writer.

## Shape on disk

```
<root>/
  0=ocfl_1.1                 namaste declaration
  ocfl_layout.json           declares the hashed n-tuple layout
  README.txt                 orientation for a reader without this code
  <hashed path>/             one object == one holding (DR-0074)
    0=ocfl_object_1.1
    inventory.json           + .sha512 sidecar
    v1/  content/…           the original as acquired
         inventory.json      + sidecar (copy as of this version)
    v2/  content/…           derivatives; the original is referenced, not copied
```

Two roots exist, `permanent` and `medium-term` (DR-0076), so that
disposition at a medium-term review date is an operation on that root and
can never touch the permanent archive. `metadata-only` and `discard` tiers
hold no bytes and have no root — constructing one is refused.

## Design notes

**v1 is the original; derivatives are later versions.** Adding a derivative
never rewrites v1, and forward-delta means identical content is referenced
by digest rather than duplicated. This is how OCFL *implements* PRES-001's
immutability rather than merely coexisting with it (DR-0074).

**Fixity failures are returned, not raised.** `fixity_check()` yields a list
of problems because a fixity failure is a recorded preservation event, never
a silent re-copy (DR-0060). The caller writes the event.

**Both algorithms are checked.** SHA-512 addresses content and SHA-256 sits
in the fixity block; the tests confirm tampering trips both. Two algorithms
disagreeing on the same bytes is itself a signal (DR-0075).

**Object paths are hashed.** Identifiers may echo source URLs, so they stay
out of directory names (DR-0076).

## Tests

24 tests, each naming the requirement or Decision Record it verifies. They
have been checked to fail honestly: removing the fixity block makes the suite
report `SUITE ERRORED` and exit 1, and breaking forward-delta turns the
DR-0073 test red — neither passes silently.
