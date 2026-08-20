#!/usr/bin/env python3
"""Compile the semantic registry into its derived projections.

Implements DR-0078 (files in Git are the source of truth; runtime and
interchange forms are derived projections) and the mapping specified in
SPEC-0005.

Outputs, written to registry/dist/:

  registry.json   Runtime projection. Its `enumerations` map is the
                  enforcement surface: a value absent from it cannot enter
                  the canonical store (DR-0078).
  registry.ttl    SKOS/RDF interchange projection (DR-0050).

Both are deterministic — sorted, no timestamps — so a diff is meaningful and
`--check` can verify the committed artifacts are current.

Usage:
  python3 registry/compile.py            # write projections
  python3 registry/compile.py --check    # verify committed projections are current
"""

import json
import sys
from pathlib import Path

import yaml

# Turtle is emitted directly rather than via rdflib: the output shape is
# simple, and avoiding a dependency suits a project that treats operational
# simplicity as a preservation property (WP 3.1, requirement 8).

SKOS = "http://www.w3.org/2004/02/skos/core#"
DCTERMS = "http://purl.org/dc/terms/"

# Fields carried into the SKOS projection via the project namespace, because
# SKOS has no equivalent. Documented as export losses in SPEC-0005 §5.
PROJECT_PROPERTIES = [
    "status", "effective", "closed", "steward", "layer", "type",
]


def load_registry(registry_dir):
    doc = yaml.safe_load((registry_dir / "registry.yaml").read_text())
    entries = []
    for path in sorted(registry_dir.rglob("*.yaml")):
        if path.name == "registry.yaml":
            continue
        entry = yaml.safe_load(path.read_text())
        entry["_source"] = str(path.relative_to(registry_dir))
        entries.append(entry)
    entries.sort(key=lambda e: e.get("id", ""))
    return doc, entries


# ---------------------------------------------------------------- JSON


def member_ids(entry):
    """Permissible values of a vocabulary, including multi-axis ones."""
    if entry.get("axes"):
        return {
            axis["id"]: sorted(m["id"] for m in axis.get("members", []))
            for axis in entry["axes"]
        }
    return sorted(m["id"] for m in entry.get("members", []))


def build_json(doc, entries):
    registry_meta = doc.get("registry", {})

    enumerations = {}
    for entry in entries:
        if entry.get("type") != "vocabulary":
            continue
        if entry.get("status") != "effective":
            # Only effective entries may appear in data (DR-0080).
            continue
        enumerations[entry["id"]] = {
            "closed": entry.get("closed", False),
            "values": member_ids(entry),
        }

    compiled_entries = {}
    for entry in entries:
        clean = {k: v for k, v in entry.items() if not k.startswith("_")}
        clean["_source"] = entry["_source"]
        compiled_entries[entry["id"]] = clean

    return {
        "registry": {
            "id": registry_meta.get("id"),
            "title": registry_meta.get("title"),
            "version": registry_meta.get("version"),
            "status": registry_meta.get("status"),
            "effective": registry_meta.get("effective"),
            "authoring_language": registry_meta.get("authoring_language"),
        },
        "generated_by": "registry/compile.py",
        "specification": "SPEC-0005",
        "layers": [layer["id"] for layer in doc.get("layers", [])],
        "enumerations": enumerations,
        "entries": compiled_entries,
    }


# ---------------------------------------------------------------- Turtle


def esc(text):
    """Escape a string for a Turtle single-line literal."""
    out = str(text).replace("\\", "\\\\").replace('"', '\\"')
    return out.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")


def lit(text, lang=None):
    value = f'"{esc(str(text).strip())}"'
    return f"{value}@{lang}" if lang else value


class Turtle:
    def __init__(self, base, prefix):
        self.base = base
        self.prefix = prefix
        self.lines = []

    def uri(self, ident):
        return f"{self.prefix}:{ident}"

    def triples(self, subject, pairs):
        """Emit one subject with its predicate/object pairs."""
        body = []
        for predicate, objects in pairs:
            if objects in (None, [], ""):
                continue
            if not isinstance(objects, list):
                objects = [objects]
            body.append(f"    {predicate} " + ", ".join(objects))
        if not body:
            return
        self.lines.append(f"{subject}")
        self.lines.append(" ;\n".join(body) + " .")
        self.lines.append("")

    def render(self, header):
        prologue = [
            f"@prefix skos: <{SKOS}> .",
            f"@prefix dcterms: <{DCTERMS}> .",
            f"@prefix {self.prefix}: <{self.base}> .",
            "",
        ]
        return "\n".join(header + prologue + self.lines).rstrip() + "\n"


def labels_for(node, turtle_pairs):
    """SKOS labels from an entry's or member's `labels` block."""
    labels = node.get("labels") or {}
    pref, alt = [], []
    for lang, label in sorted(labels.items()):
        if not isinstance(label, dict):
            continue
        if label.get("prefLabel"):
            pref.append(lit(label["prefLabel"], lang))
        for alternate in label.get("altLabel") or []:
            alt.append(lit(alternate, lang))
    turtle_pairs.append(("skos:prefLabel", pref))
    turtle_pairs.append(("skos:altLabel", alt))


def notes_for(node, pairs):
    """Definitions and the several kinds of note the registry carries."""
    if node.get("definition"):
        pairs.append(("skos:definition", lit(node["definition"], "en")))
    if node.get("scope_note"):
        pairs.append(("skos:scopeNote", lit(node["scope_note"], "en")))
    if node.get("usage_note"):
        pairs.append(("skos:note", lit(node["usage_note"], "en")))
    # `not:` carries a conflict-register disambiguation. SKOS has no
    # dedicated property; it becomes a marked scopeNote (SPEC-0005 §4).
    if node.get("not"):
        pairs.append(("skos:scopeNote", lit("Not: " + node["not"], "en")))


def mappings_for(node, pairs, prefix="uiw"):
    """External alignments.

    skos:exactMatch and friends are object properties: their objects must be
    resources. The registry's mapping targets are external vocabularies named
    in prose ("PHIA: likely / probably"), not URIs, so emitting them as SKOS
    match properties would produce invalid SKOS. They are emitted as
    project-namespace datatype properties instead, and are promoted to real
    skos:*Match triples once a target is identified by URI
    (SPEC-0005 §5, loss L4).
    """
    buckets = {"exactMatch": [], "closeMatch": [], "relatedMatch": []}
    for mapping in node.get("mappings") or []:
        relation = mapping.get("relation")
        target = mapping.get("target")
        if relation not in buckets or not target:
            continue
        if str(target).startswith(("http://", "https://", "urn:")):
            buckets[relation].append(f"<{target}>")
        else:
            pairs.append((f"{prefix}:{relation}Target", lit(target)))
    for relation, values in buckets.items():
        pairs.append((f"skos:{relation}", values))


def project_properties(node, prefix, pairs):
    for field in PROJECT_PROPERTIES:
        if field in node and node[field] is not None:
            value = node[field]
            if isinstance(value, bool):
                value = f'"{str(value).lower()}"^^<http://www.w3.org/2001/XMLSchema#boolean>'
            else:
                value = lit(value)
            pairs.append((f"{prefix}:{field}", value))
    for field in ("authorised_by", "satisfies_requirements", "depends_on_specs"):
        values = [lit(v) for v in node.get(field) or []]
        pairs.append((f"{prefix}:{field}", values))


def build_turtle(doc, entries):
    namespaces = doc.get("namespaces", {})
    base = namespaces.get("base", "urn:uiw:registry:")
    prefix = namespaces.get("prefix", "uiw")
    meta = doc.get("registry", {})

    turtle = Turtle(base, prefix)

    header = [
        "# SKOS/RDF projection of the semantic registry.",
        "#",
        "# DERIVED ARTIFACT — do not edit. The source of truth is the YAML",
        "# under registry/ (DR-0078). Regenerate with registry/compile.py.",
        "# Mapping and its documented export losses: SPEC-0005.",
        f"# Registry version: {meta.get('version')}",
        "",
    ]

    # The registry itself.
    turtle.triples(
        turtle.uri(meta.get("id", "registry")),
        [
            ("a", "skos:ConceptScheme"),
            ("skos:prefLabel", lit(meta.get("title", ""), "en")),
            (f"{prefix}:version", lit(meta.get("version", ""))),
            (f"{prefix}:status", lit(meta.get("status", ""))),
            ("dcterms:issued", lit(meta.get("effective", ""))),
        ],
    )

    for entry in entries:
        entry_id = entry["id"]
        entry_type = entry.get("type")

        if entry_type == "vocabulary":
            schemes = []
            if entry.get("axes"):
                # A multi-axis vocabulary becomes one scheme per axis
                # (SPEC-0005 §5, loss L3).
                for axis in entry["axes"]:
                    schemes.append((f"{entry_id}-{axis['id']}", axis, entry))
            else:
                schemes.append((entry_id, entry, entry))

            for scheme_id, node, parent in schemes:
                pairs = [("a", "skos:ConceptScheme")]
                labels_for(node, pairs)
                notes_for(node, pairs)
                mappings_for(node, pairs)
                project_properties(parent, prefix, pairs)
                if scheme_id != entry_id:
                    pairs.append((f"{prefix}:axisOf", turtle.uri(entry_id)))
                turtle.triples(turtle.uri(scheme_id), pairs)

                for member in node.get("members") or []:
                    member_pairs = [
                        ("a", "skos:Concept"),
                        ("skos:inScheme", turtle.uri(scheme_id)),
                        ("skos:topConceptOf", turtle.uri(scheme_id)),
                    ]
                    labels_for(member, member_pairs)
                    notes_for(member, member_pairs)
                    mappings_for(member, member_pairs)
                    # Numeric ranges have no SKOS equivalent
                    # (SPEC-0005 §5, loss L2).
                    if member.get("range"):
                        rng = member["range"]
                        member_pairs.append((
                            f"{prefix}:range",
                            lit(f"{rng.get('min')}-{rng.get('max')} {rng.get('unit')}"),
                        ))
                    if member.get("issuing_authority"):
                        member_pairs.append((
                            f"{prefix}:issuingAuthority",
                            lit(member["issuing_authority"]),
                        ))
                    turtle.triples(
                        turtle.uri(f"{scheme_id}--{member['id']}"), member_pairs
                    )

        elif entry_type == "argument-scheme":
            # Argument schemes have no SKOS analogue; represented as a
            # concept with project properties (SPEC-0005 §5, loss L1).
            pairs = [
                ("a", "skos:Concept"),
                ("skos:inScheme", turtle.uri(meta.get("id", "registry"))),
            ]
            labels_for(entry, pairs)
            notes_for(entry, pairs)
            project_properties(entry, prefix, pairs)
            if entry.get("conclusion"):
                pairs.append((f"{prefix}:conclusion", lit(entry["conclusion"], "en")))
            pairs.append((
                f"{prefix}:premise",
                [lit(p.get("text", ""), "en") for p in entry.get("premises") or []],
            ))
            pairs.append((
                f"{prefix}:criticalQuestion",
                [lit(q.get("text", ""), "en") for q in entry.get("critical_questions") or []],
            ))
            turtle.triples(turtle.uri(entry_id), pairs)

        else:
            pairs = [
                ("a", "skos:Concept"),
                ("skos:inScheme", turtle.uri(meta.get("id", "registry"))),
            ]
            labels_for(entry, pairs)
            notes_for(entry, pairs)
            mappings_for(entry, pairs)
            project_properties(entry, prefix, pairs)
            turtle.triples(turtle.uri(entry_id), pairs)

    return turtle.render(header)


# ---------------------------------------------------------------- main


def main():
    check_only = "--check" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    registry_dir = Path(args[0]) if args else Path(__file__).parent
    dist = registry_dir / "dist"

    doc, entries = load_registry(registry_dir)
    outputs = {
        # default=str renders the dates PyYAML parses into date objects as
        # ISO-8601 strings.
        dist / "registry.json": json.dumps(
            build_json(doc, entries),
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
            default=str,
        )
        + "\n",
        dist / "registry.ttl": build_turtle(doc, entries),
    }

    if check_only:
        stale = []
        for path, content in outputs.items():
            if not path.exists() or path.read_text() != content:
                stale.append(path.name)
        if stale:
            print(f"STALE: {', '.join(sorted(stale))} — run registry/compile.py")
            return 1
        print(f"Projections current ({len(entries)} entries).")
        return 0

    dist.mkdir(exist_ok=True)
    for path, content in outputs.items():
        path.write_text(content)
        print(f"wrote {path.relative_to(registry_dir.parent)} ({len(content):,} bytes)")

    enum_count = len(build_json(doc, entries)["enumerations"])
    print(f"{len(entries)} entries; {enum_count} enforceable enumerations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
