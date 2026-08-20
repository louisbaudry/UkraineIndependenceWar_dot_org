#!/usr/bin/env python3
"""Validate the semantic registry against SPEC-0004 / DR-0079 / DR-0080.

Exit status is non-zero on any error, so this can gate a release baseline
(DR-0048). Warnings do not fail the run.

Usage: python3 registry/validate.py [registry_dir]
"""

import sys
from pathlib import Path

import yaml

ENTRY_TYPES = {
    "concept", "vocabulary", "data-element",
    "relationship-type", "argument-scheme", "identifier-type",
}
REGISTRATION_STATUSES = {"draft", "effective", "deprecated", "retired"}
MAPPING_RELATIONS = {"exactMatch", "closeMatch", "relatedMatch"}

# Required on every entry, per DR-0079.
REQUIRED = ["id", "type", "layer", "status", "steward", "authorised_by", "definition"]


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, where, msg):
        self.errors.append(f"{where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"{where}: {msg}")


def load_layers(registry_dir, report):
    path = registry_dir / "registry.yaml"
    if not path.exists():
        report.error("registry.yaml", "missing")
        return set()
    doc = yaml.safe_load(path.read_text()) or {}
    return {layer["id"] for layer in doc.get("layers", [])}


def check_entry(path, doc, layers, seen_ids, report):
    where = path.name

    for field in REQUIRED:
        if not doc.get(field):
            report.error(where, f"missing required field '{field}' (DR-0079)")

    entry_id = doc.get("id")
    if entry_id:
        if entry_id in seen_ids:
            report.error(where, f"duplicate entry id '{entry_id}' (also in {seen_ids[entry_id]})")
        else:
            seen_ids[entry_id] = where
        if entry_id != entry_id.lower() or " " in entry_id:
            report.error(where, f"id '{entry_id}' must be lowercase without spaces")

    if (t := doc.get("type")) and t not in ENTRY_TYPES:
        report.error(where, f"unknown entry type '{t}'")

    if (s := doc.get("status")) and s not in REGISTRATION_STATUSES:
        report.error(where, f"unknown registration status '{s}'")

    if (layer := doc.get("layer")) and layers and layer not in layers:
        report.error(where, f"unknown layer '{layer}' (not declared in registry.yaml)")

    if doc.get("status") == "deprecated" and not doc.get("replaced_by"):
        report.error(where, "deprecated entries must carry 'replaced_by' (DR-0080, §96)")

    if doc.get("status") == "effective" and not doc.get("effective"):
        report.error(where, "effective entries must carry an 'effective' date")

    for ref in doc.get("authorised_by", []) or []:
        if not str(ref).startswith("DR-"):
            report.warn(where, f"authorised_by '{ref}' is not a Decision Record reference")

    # English prefLabel is required: English is the authoring language (DR-0081).
    labels = doc.get("labels") or {}
    if not (labels.get("en") or {}).get("prefLabel"):
        report.error(where, "missing English prefLabel (DR-0081: English is the authoring language)")

    for lang, label in labels.items():
        if lang == "en" or not isinstance(label, dict):
            continue
        for field in ("translator", "date", "review_status"):
            if not label.get(field):
                report.error(
                    where,
                    f"translation '{lang}' missing '{field}' — translations carry "
                    f"provenance and review status (DR-0081)",
                )

    check_mappings(where, doc.get("mappings"), report)

    if doc.get("type") == "vocabulary":
        check_vocabulary(where, doc, report)
    if doc.get("type") == "argument-scheme":
        check_scheme(where, doc, report)


def check_mappings(where, mappings, report):
    for mapping in mappings or []:
        rel = mapping.get("relation")
        if rel not in MAPPING_RELATIONS:
            report.error(where, f"mapping relation '{rel}' not in {sorted(MAPPING_RELATIONS)}")
        if not mapping.get("target"):
            report.error(where, "mapping missing 'target'")
        if rel in {"closeMatch", "relatedMatch"} and not mapping.get("note"):
            report.warn(where, f"{rel} to '{mapping.get('target')}' has no note explaining the imperfect fit")


def check_vocabulary(where, doc, report):
    if "closed" not in doc:
        report.error(where, "vocabulary must declare 'closed' (true/false) — DR-0080")

    members = doc.get("members")
    axes = doc.get("axes")
    if not members and not axes:
        report.error(where, "vocabulary has no members")

    groups = [("members", members or [])]
    for axis in axes or []:
        groups.append((f"axis '{axis.get('id')}'", axis.get("members") or []))

    for group_name, group in groups:
        seen = set()
        for member in group:
            mid = member.get("id")
            if not mid:
                report.error(where, f"{group_name}: member missing 'id'")
                continue
            if mid in seen:
                report.error(where, f"{group_name}: duplicate member id '{mid}'")
            seen.add(mid)
            if not (member.get("labels", {}).get("en", {}) or {}).get("prefLabel"):
                report.error(where, f"{group_name}: member '{mid}' missing English prefLabel")
            # Every member needs defining content. A definition is the usual
            # form, but a numeric range defines a likelihood band (DR-0065:
            # "the numeric range is the anchor") and an issuing authority
            # defines an identifier type. Axis members are self-defining
            # grade labels.
            defining = ("definition", "range", "issuing_authority")
            if group_name == "members" and not any(member.get(f) for f in defining):
                report.warn(where, f"member '{mid}' has no defining content ({'/'.join(defining)})")


def check_scheme(where, doc, report):
    if not doc.get("premises"):
        report.error(where, "argument scheme missing 'premises'")
    if not doc.get("conclusion"):
        report.error(where, "argument scheme missing 'conclusion'")
    cqs = doc.get("critical_questions")
    if not cqs:
        report.error(where, "argument scheme missing 'critical_questions' (DR-0034)")
    valid = {"rebutting", "undercutting", "undermining"}
    for cq in cqs or []:
        if not cq.get("id") or not cq.get("text"):
            report.error(where, "critical question missing 'id' or 'text'")
        dt = cq.get("defeater_type_if_unanswered")
        if dt and dt not in valid:
            report.error(where, f"critical question '{cq.get('id')}': defeater type '{dt}' not in {sorted(valid)}")


def main():
    registry_dir = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent)
    report = Report()
    layers = load_layers(registry_dir, report)

    paths = sorted(
        p for p in registry_dir.rglob("*.yaml") if p.name != "registry.yaml"
    )
    if not paths:
        report.error("registry", "no entry files found")

    seen_ids = {}
    for path in paths:
        try:
            doc = yaml.safe_load(path.read_text())
        except yaml.YAMLError as exc:
            report.error(path.name, f"YAML parse error: {exc}")
            continue
        if not isinstance(doc, dict):
            report.error(path.name, "file does not contain a mapping")
            continue
        check_entry(path, doc, layers, seen_ids, report)

    print(f"Registry: {registry_dir}")
    print(f"Entries checked: {len(paths)}")

    for warning in report.warnings:
        print(f"  warning  {warning}")
    for error in report.errors:
        print(f"  ERROR    {error}")

    print(
        f"\n{len(report.errors)} error(s), {len(report.warnings)} warning(s)"
    )
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
