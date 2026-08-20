# Semantic Registry

The project's semantic registry, implemented per
[SPEC-0004](../docs/specifications/SPEC-0004-semantic-registry.md) and
governed by DR-0050, DR-0078, DR-0079, DR-0080, DR-0081.

**These YAML files are the source of truth.** SKOS/RDF, JSON, and
human-readable forms are derived projections (DR-0078); the compiled
projection enforces enumerations in the canonical store, so a value absent
from here cannot enter the data.

## Layout

```
registry.yaml          Registry-level metadata, version, namespace
vocabularies/          Controlled enumerations and their members
schemes/               Argument schemes with critical questions (DR-0034)
concepts/              Defined project concepts, incl. conflict-register scope notes
dist/                  DERIVED — generated projections, never edited
```

## Tools

```
python3 registry/validate.py           # source conformance; non-zero on error
python3 registry/compile.py            # regenerate dist/ projections
python3 registry/compile.py --check    # verify dist/ is current; non-zero if stale
```

Both exit non-zero on failure so they can gate a release baseline (DR-0048).
The projection mapping and its documented export losses are specified in
[SPEC-0005](../docs/specifications/SPEC-0005-registry-skos-mapping.md).

## Entry format

Every entry carries the fields required by DR-0079. Minimum:

```yaml
id: absence-states           # stable, never reused, never re-pointed
type: vocabulary             # concept | vocabulary | data-element
                             # relationship-type | argument-scheme | identifier-type
layer: epistemic             # per SPEC-0001's object families
status: effective            # draft | effective | deprecated | retired
effective: 2026-08-16
closed: true                 # vocabularies only: true = any change needs a DR
steward: founder
authorised_by: [DR-0029]     # the decisions that created or govern this entry
satisfies_requirements: [EVID-010]
definition: >
  ...
labels:
  en:
    prefLabel: absence state
members:                     # vocabularies only
  - id: unknown
    labels: {en: {prefLabel: unknown}}
    definition: >
      ...
```

Optional where they carry meaning: `scope_note`, `usage_note`, `not`
(disambiguation, typically from the conflict register), `altLabel`,
`broader` / `narrower` / `related`, `mappings`, `depends_on_specs`,
`replaced_by`, `version_history`.

### `closed` vocabularies

A vocabulary marked `closed: true` was fixed by a Decision Record and can
only be changed by one (DR-0080). All vocabularies seeded here are closed by
construction — each traces to the DR that set it.

### `mappings`

External alignments, each with a relation (`exactMatch`, `closeMatch`,
`relatedMatch`) and a note wherever the fit is imperfect:

```yaml
mappings:
  - target: "PHIA: realistic possibility"
    relation: closeMatch
    note: >
      PHIA's band is 40–<50%; no ICD 203 band shares its boundaries.
```

### `labels` and translation

English is the authoring language (DR-0081). Translated labels are entries
with provenance, never derivations:

```yaml
labels:
  en: {prefLabel: likely}
  uk:
    prefLabel: імовірно
    translator: <name>
    date: <date>
    review_status: reviewed | proposed
forbidden_translations:
  - lang: uk
    term: <term>
    reason: reads as near-certainty rather than 55–80%
```

Machine translation may propose; it never becomes authoritative without
human review (DR-0081, AI-001). **No translations are seeded** — they
require a translator and review, which this deposit does not have.

## Changing the registry

Per DR-0080:

| Change | Route |
|---|---|
| Typo; clarified wording not changing meaning; added translation; added scope note | Registry process; recorded |
| New member of an **open** vocabulary; new mapping; new alt label; new scheme | Registry process; recorded with rationale |
| Changing a definition's **meaning**; removing or deprecating a member; changing an enumeration data depends on; opening or closing a vocabulary | **Decision Record required**, with version, migration note, deprecation and replacement mapping |

Nothing is ever deleted: a dataset can outlive the vocabulary it used.

## Seed state

Seeded 2026-08-16 by transcription from enacted Decision Records. Argument
schemes are represented by exemplars only — DR-0034 assigns the seed
library's contents to methodology work tested against real investigations.
