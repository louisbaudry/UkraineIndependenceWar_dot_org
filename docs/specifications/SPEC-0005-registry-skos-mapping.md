# SPEC-0005 — Registry Projection Mapping (JSON and SKOS/RDF)

**Class:** SPEC (DR-0046 control) | **Version:** 0.1 | **Status:** Draft — proposed
**Approval:** pending founder review | **Effective:** upon approval
**Supersedes:** — | **Superseded by:** —
**Governed by:** DR-0056 (projection mappings are controlled artifacts), DR-0078 (files in Git are source of truth; runtime and interchange forms are derived), DR-0050 (SKOS), DR-0079 (entry structure), DR-0047 (versioning).
**Generator:** `registry/compile.py`

### AI provenance (record §80)

Drafted 2026-08-16 by an AI assistant (Anthropic Claude Code agent session)
at the founder's direction, alongside the compiler it specifies. Candidate
until approved.

---

## 1. Scope

The mapping from the registry's YAML source of truth to its two derived
projections, and **the losses each incurs** — the documentation DR-0056
requires of every standards surface.

| Projection | File | Purpose |
|---|---|---|
| **JSON** | `registry/dist/registry.json` | Runtime. Its `enumerations` map is the enforcement surface (DR-0078) |
| **SKOS/RDF** | `registry/dist/registry.ttl` | Interchange, in Turtle (DR-0050) |

Both are **deterministic** — sorted, no timestamps — so a diff is meaningful
and `compile.py --check` can verify the committed artifacts are current.

## 2. Derived, not authored

Both files carry a header marking them derived. **They are never edited.**
They are committed so that a registry change shows both its source diff and
its projection diff in one review; `--check` prevents drift.

## 3. JSON projection

```
registry     Registry metadata: id, title, version, status, effective,
             authoring_language
layers       Declared layer identifiers
enumerations The enforcement surface (§3.1)
entries      Every entry, verbatim, keyed by id, with its source path
```

### 3.1 The enforcement surface

`enumerations` contains **only vocabularies whose status is `effective`** —
`draft` entries may not appear in data, and `deprecated` ones may not be used
for new data (DR-0080). Each carries:

```json
"likelihood-bands": {
  "closed": true,
  "values": ["almost-certain", "almost-no-chance", "likely", ...]
}
```

A multi-axis vocabulary carries a map of axis id to that axis's values
rather than a flat list:

```json
"source-grades": {
  "closed": true,
  "values": {
    "source-reliability": ["A", "B", "C", "D", "E", "F"],
    "item-credibility": ["1", "2", "3", "4", "5", "6"]
  }
}
```

The canonical store validates registry-governed field values against this
map. `closed` tells a consumer whether the value set may grow by registry
process or only by Decision Record (DR-0080).

## 4. SKOS/RDF projection

| Registry construct | SKOS/RDF |
|---|---|
| The registry itself | `skos:ConceptScheme` |
| `vocabulary` entry | `skos:ConceptScheme` |
| vocabulary member | `skos:Concept`, `skos:inScheme` + `skos:topConceptOf` the vocabulary |
| `concept` / `identifier-type` / other entry | `skos:Concept` in the registry scheme |
| `labels.<lang>.prefLabel` | `skos:prefLabel` with language tag |
| `labels.<lang>.altLabel` | `skos:altLabel` with language tag |
| `definition` | `skos:definition` |
| `scope_note` | `skos:scopeNote` |
| `usage_note` | `skos:note` |
| `not` | `skos:scopeNote`, prefixed `"Not: "` |
| mapping with a URI target | `skos:exactMatch` / `closeMatch` / `relatedMatch` |
| mapping with a prose target | `uiw:exactMatchTarget` / `closeMatchTarget` / `relatedMatchTarget` (see §5, L4) |
| `status`, `effective`, `closed`, `steward`, `layer`, `type` | `uiw:` datatype properties |
| `authorised_by`, `satisfies_requirements`, `depends_on_specs` | `uiw:` datatype properties |
| member `range` | `uiw:range`, as `"min-max unit"` |
| member `issuing_authority` | `uiw:issuingAuthority` |
| argument scheme | `skos:Concept` + `uiw:premise`, `uiw:conclusion`, `uiw:criticalQuestion` |

Concept URIs are `{base}{entry-id}` for entries and
`{base}{scheme-id}--{member-id}` for members. The **namespace is declared in
`registry.yaml`, not in code**, and is marked provisional: record §15
forbids freezing a custom identifier syntax before researching established
patterns, and the identifier design is open (Q-12).

## 5. Documented export losses

Required by DR-0056. A consumer reading only the SKOS projection loses the
following; the JSON projection and the YAML source retain all of it.

- **L1 — Argument-scheme structure.** SKOS has no analogue for premises,
  conclusions, or critical questions. They are emitted as `uiw:` properties;
  a pure-SKOS consumer sees a concept with labelled notes and **loses the
  reasoning structure entirely**, including which defeater type an
  unanswered critical question implies. Consumers needing schemes should read
  the JSON or the source.

- **L2 — Numeric ranges.** `uiw:range "55-80 percent"` is a string. A
  pure-SKOS consumer sees the label "likely" without its calibration — which
  is precisely the meaning DR-0065 says the range, not the word, carries.
  **This is the most consequential loss in the SKOS surface.**

- **L3 — Multi-axis vocabularies.** `source-grades` becomes two schemes
  (`source-grades-source-reliability`, `source-grades-item-credibility`)
  linked by `uiw:axisOf`. A consumer ignoring `uiw:` sees two unrelated
  schemes rather than one two-axis grade.

- **L4 — Prose mapping targets.** `skos:exactMatch` and its siblings are
  object properties whose objects must be resources. The registry's targets
  are external vocabularies named in prose ("PHIA: likely / probably"), so
  emitting them as SKOS match properties would produce **invalid SKOS**.
  They are emitted as `uiw:*Target` datatype properties instead. A target
  given as a URI *is* emitted as a proper `skos:*Match`; the mappings are
  promoted as target vocabularies acquire identified URIs.

- **L5 — Governance metadata.** Registration status, `closed`, stewardship,
  authorising Decision Records, and satisfied requirements have no SKOS
  equivalent. They survive only in the `uiw:` namespace, so a pure-SKOS
  consumer **cannot tell an effective entry from a deprecated one**.

- **L6 — Forbidden translations.** Not emitted at all. Emitting them as
  notes would risk a consumer harvesting them as valid labels — the exact
  harm DR-0081 records them to prevent. They exist only in the source and
  the JSON.

- **L7 — Note-type collapse.** `usage_note` becomes `skos:note` and `not`
  becomes a prefixed `skos:scopeNote`, so the registry's distinct note kinds
  are not reliably recoverable from SKOS alone.

## 6. Verification

- `registry/validate.py` — source conformance (DR-0079/0080/0081); exits
  non-zero on error, so it can gate a release baseline (DR-0048).
- `registry/compile.py --check` — verifies committed projections are current;
  exits non-zero if stale.

Both are intended to run in a release-gating check alongside the tests
required by the REQ documents' verification criteria.

## 7. Open questions

1. Namespace URI, pending the identifier design (Q-12, record §15).
2. Whether to emit a JSON-LD context so the JSON projection is directly
   RDF-consumable, removing some of §5's losses for consumers who want both.
3. Whether target vocabularies (PHIA, CIDOC CRM classes, PREMIS, BODS)
   should be given URIs now to promote L4's `uiw:*Target` properties to
   proper `skos:*Match`.
4. Whether release baselines pin the compiled projections themselves or only
   the registry version they were built from (DR-0048 interaction).

## 8. Candidate Decision Record

- **CDR-P3-29:** Adopt SPEC-0005 as the controlled mapping document for the
  registry's JSON and SKOS/RDF projections, satisfying DR-0056 for these two
  surfaces, with the export losses of §5 as the documented and accepted loss
  set.
