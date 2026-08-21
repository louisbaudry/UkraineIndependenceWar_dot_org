#!/usr/bin/env python3
"""Reconstruct the archive from a dump and an OCFL root, using neither.

This is the demonstration REQ-PRES-009 asks for:

    "from an OCFL storage root plus a canonical dump alone, and without
     project code, holdings with their metadata and provenance are
     reconstructed"

**This script deliberately imports nothing from the project.** No `ocfl`, no
`pipeline`, no `dump`, no database. Only the Python standard library, the
published format documentation (SPEC-0006 and the OCFL 1.1 specification),
and the files on disk.

It stands in for a future archivist with the bytes, the specifications, and
no working copy of this repository. If it stops working, the archive's core
promise has stopped being true — which is exactly what it exists to detect.

Usage:
  python3 export/tests/reconstruct.py <dump-dir> <ocfl-root> [<ocfl-root> …]
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.open() if line.strip()]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def find_ocfl_object(roots: list[Path], object_id: str) -> Path | None:
    """Locate an object by reading inventories, not by knowing the layout.

    The storage root declares a hashed-n-tuple layout in ocfl_layout.json,
    but an archivist need not reimplement it: every object root carries an
    inventory naming its own id, so a walk finds them.
    """
    for root in roots:
        for inventory_path in root.rglob("inventory.json"):
            if inventory_path.parent.name.startswith("v"):
                continue  # a per-version copy, not the object root
            try:
                if json.loads(inventory_path.read_text()).get("id") == object_id:
                    return inventory_path.parent
            except (json.JSONDecodeError, OSError):
                continue
    return None


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2

    dump_dir = Path(sys.argv[1])
    ocfl_roots = [Path(p) for p in sys.argv[2:]]
    problems: list[str] = []
    findings: list[str] = []

    # ---- 1. The dump describes itself -----------------------------------

    manifest = json.loads((dump_dir / "manifest.json").read_text())
    sidecar = (dump_dir / "manifest.json.sha256").read_text().split()[0]
    if sidecar != sha256_file(dump_dir / "manifest.json"):
        problems.append("manifest does not match its sidecar")
    findings.append(
        f"dump: format {manifest['format_version']}, "
        f"{len(manifest['tables'])} tables, {manifest['total_rows']} rows, "
        f"registry version {manifest['registry_version']}"
    )

    for table, meta in manifest["tables"].items():
        path = dump_dir / meta["files"]["jsonl"]["path"]
        if sha256_file(path) != meta["files"]["jsonl"]["sha256"]:
            problems.append(f"{table}: content does not match its recorded digest")

    # ---- 2. The schema explains the data --------------------------------

    schema = json.loads((dump_dir / "schema.json").read_text())
    vocabulary_columns = [
        (table, column["name"], column["registry_entry"])
        for table, spec in schema["tables"].items()
        for column in spec["columns"]
        if "registry_entry" in column
    ]
    findings.append(
        f"schema: {len(schema['tables'])} tables described; "
        f"{len(vocabulary_columns)} columns resolve to a registry vocabulary"
    )
    if not vocabulary_columns:
        problems.append("no column links to a registry vocabulary — meaning is lost")

    # ---- 3. Holdings, and what the archive says it possesses ------------

    holdings = load_jsonl(dump_dir / "data" / "holding.jsonl")
    objects = load_jsonl(dump_dir / "data" / "preserved_object.jsonl")
    events = load_jsonl(dump_dir / "data" / "preservation_event.jsonl")
    attempts = load_jsonl(dump_dir / "data" / "acquisition_attempt.jsonl")

    findings.append(
        f"archive: {len(holdings)} holding(s), {len(objects)} preserved object(s), "
        f"{len(events)} preservation event(s), {len(attempts)} acquisition attempt(s)"
    )

    if not holdings:
        problems.append("no holdings in the dump — nothing to reconstruct")

    # ---- 4. Follow a holding to its bytes and verify them ----------------

    reconstructed = 0
    for holding in holdings:
        object_id = holding.get("ocfl_object_id")
        if not object_id:
            continue  # external custodian: no bytes of our own (§26)

        object_root = find_ocfl_object(ocfl_roots, object_id)
        if object_root is None:
            problems.append(f"holding {holding['id']}: OCFL object {object_id} not found")
            continue

        inventory = json.loads((object_root / "inventory.json").read_text())

        # The state of the head version is the holding's logical contents.
        head_state = inventory["versions"][inventory["head"]]["state"]
        for digest, logical_paths in head_state.items():
            content_paths = inventory["manifest"].get(digest)
            if not content_paths:
                problems.append(f"{object_id}: digest in state but not in manifest")
                continue
            content_file = object_root / content_paths[0]
            if not content_file.is_file():
                problems.append(f"{object_id}: content missing at {content_paths[0]}")
                continue
            # Verify with the algorithm the inventory itself declares.
            algorithm = inventory["digestAlgorithm"]
            h = hashlib.new(algorithm)
            h.update(content_file.read_bytes())
            if h.hexdigest() != digest:
                problems.append(f"{object_id}: {logical_paths} fails {algorithm}")
                continue
            reconstructed += 1

        # Cross-check the dump's recorded digest against the stored bytes.
        for obj in objects:
            if obj.get("ocfl_object_id") != object_id:
                continue
            recorded = obj.get("sha256", "")
            if isinstance(recorded, str) and recorded.startswith("\\x"):
                recorded_hex = recorded[2:]
                if recorded_hex not in inventory.get("fixity", {}).get("sha256", {}):
                    problems.append(
                        f"{object_id}: the dump's sha256 is absent from the "
                        "OCFL fixity block — dump and storage disagree"
                    )

    findings.append(f"reconstructed and verified {reconstructed} content file(s)")

    # ---- 5. Absence is legible ------------------------------------------

    absence_columns = [
        (table, column["name"])
        for table, spec in schema["tables"].items()
        for column in spec["columns"]
        if column.get("registry_entry") == "absence-states"
        or "absence" in str(column.get("composite_fields", ""))
    ]
    findings.append(
        f"absence: {len(absence_columns)} column(s) can say why a value is missing"
    )
    if not absence_columns:
        problems.append(
            "no column carries an absence state — a reader could not tell "
            "'unknown' from 'no'"
        )

    # ---- report ---------------------------------------------------------

    print("Reconstruction from dump + OCFL, using neither's software")
    print("=" * 62)
    for line in findings:
        print(f"  {line}")
    if problems:
        print()
        for problem in problems:
            print(f"  PROBLEM  {problem}")
        print(f"\nFAILED — {len(problems)} problem(s)")
        return 1
    print("\nPASSED — the archive is reconstructible without project code (PRES-009)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
