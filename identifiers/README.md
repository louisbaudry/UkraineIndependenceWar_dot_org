# Public identifiers and resolution

Implements [SPEC-0007](../docs/specifications/SPEC-0007-public-identifiers-and-resolution.md)
under DR-0087 (ARK as the scheme), DR-0088 (minting as assignment events at
publication), DR-0089 (the register and its five dispositions), DR-0090
(identifiers name objects, `.vN` names states), DR-0091 (project URIs
derive from ARKs) and DR-0092 (a split's deciding agent is shown as a
public title, never the agent's own id).

**Nothing can be minted yet, and that is correct.** The project holds no
NAAN, so `from_registry()` returns `None` and a `Publisher` built from it
publishes without minting. Minting under a number the project does not hold
would put identifiers into the world that no resolver chain can honour. The
suite mints under the ARK Alliance's shared test NAAN `99999`, which is
reserved for exactly this.

## Files

| File | Contents |
|---|---|
| `ark.py` | Syntax only: the betanumeric alphabet, name generation, the NOID check character, normalisation, `.vN` qualifiers. Knows nothing about the database. |
| `register.py` | Minting as `identifier_assignment` assertions, and the disposition changes behind a merge, split, redaction or tier decision. |
| `resolver.py` | The HTTP contract for the five dispositions, `?info` as an ERC record in ANVL, and `.vN` state resolution. |
| `tests/rebuild.py` | Resolution reimplemented from the specification, importing nothing from the project. |
| `tests/test_identifiers.py` | The suite. |

The database half is [`schema/08-identifiers.sql`](../schema/08-identifiers.sql):
the assignment family, the register, the forward-only disposition trigger,
`resolve_identifier()`, and the split-byline tables (below).

## Running

```bash
PGHOST=… PGUSER=… python3 identifiers/tests/test_identifiers.py
```

## Design notes

**Resolution lives in the database, not here.** `resolve_identifier()` is a
SQL function, and `tests/rebuild.py` reimplements it from SPEC-0007 alone.
A successor with a dump and the specification can answer every identifier
the project ever published without this code (PRES-009). The suite proves
it, in a subprocess with a bare environment.

**The register is public; the mapping is not.** `public_identifier` says
that an identifier exists and what became of it — public facts, because
DATA-009 promises a citation resolves forever, including for an object
nobody may read. `public_identifier_subject` maps it to an internal UUID,
which is `internal` tier and appears in no resolver response (SPEC-0007
§4.3). The suite greps every body and every `?info` record for a UUID.

**Minting is idempotent by rule, not by luck.** Two identifiers for one
object would give a reader two ways to cite it, and DATA-009 would then owe
both forever. `mint()` returns the existing identifier rather than making a
second.

**A minted identifier never 404s.** Merged redirects, split disambiguates,
redacted is `410` with a tombstone, restricted is `403` saying the object
exists. Only a name that was never issued is unknown — and a name whose
check character fails is a `400`, so a reader can tell a mistyped citation
from a withdrawn one.

**A split's byline is a title, never the agent (DR-0092).** A disambiguation
record can carry `decided_by_title` — a role an agent chose to have shown,
computed at insert from `pipeline_agent.public_title` — but never the
agent's own id. That link lives only in `disambiguation_decision`, a
separate `internal`-tier table. The split matters because
`disambiguation_record` is `public` tier and ships in every disclosure
dump, while a *preservation* dump separately carries `pipeline_agent` with
names attached: putting the raw id in the same table as the public byline
would let anyone holding both dumps join them and identify an agent who
chose to stay unnamed. Both disambiguation tables are made immutable after
insert, so a title changed later never rewrites what a past decision said.

## Tests

77 checks. The ones that carry weight, and how they were shown to be real:

- **The check character catches every single-character substitution and
  every adjacent transposition** over 10,000 generated names. Replacing the
  positional weighting with a constant weight drops transposition detection
  to 966/9,706 and turns the suite red — the check is doing work, not
  restating an identity.
- **No minted identifier returns 404**, checked over the whole register
  rather than on examples.
- **The deletion guard is what prevents deletion.** The suite drops the
  trigger on a second connection, confirms the delete then succeeds, and
  rolls back — a negative control rather than an assertion of faith.
- **The specification-derived rebuild agrees with the implementation**,
  which is the only place the check-character rule as written and as coded
  are compared.
- **No internal UUID reaches a resolver body.** Reintroducing one turns the
  suite red.
- **A preservation dump and a disclosure dump can never be joined to
  identify an untitled decider.** The suite checks the disclosure dump
  directly for the absence of `disambiguation_decision` and of any
  `decided_by`-shaped field on `disambiguation_record`, then checks the
  preservation dump *does* carry the link — confirming the protection is a
  deliberate separation, not an accidental absence of the data anywhere.
  Misclassifying `disambiguation_decision`'s tier, or removing its `UPDATE`
  guard, each turn a check red.

Removing the forward-only disposition trigger fails six checks. That was
verified, not assumed.
