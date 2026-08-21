#!/usr/bin/env python3
"""Tests for the OCFL storage layer.

Each test names the requirement or Decision Record it verifies, continuing
the pattern of the schema suite: requirement -> verification criterion ->
executable test (record §99).

Run: python3 storage/tests/test_ocfl.py
"""

import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ocfl import (  # noqa: E402
    CONTENT_ALGORITHM,
    FIXITY_ALGORITHM,
    ContentFile,
    OcflError,
    StorageRoot,
    hashed_n_tuple,
    validate_object,
)

PASSES: list[str] = []
FAILURES: list[str] = []


def check(req: str, what: str, condition: bool) -> None:
    if condition:
        PASSES.append(f"PASS  {req} — {what}")
    else:
        FAILURES.append(f"FAIL  {req} — {what}")


def rejects(req: str, what: str, fn) -> None:
    try:
        fn()
    except Exception:
        PASSES.append(f"PASS  {req} — {what}")
        return
    FAILURES.append(f"FAIL  {req} — {what}: was accepted but must be rejected")


def write(directory: Path, name: str, text: str) -> Path:
    path = directory / name
    path.write_text(text)
    return path


def main() -> int:
    try:
        return run()
    except Exception as exc:  # noqa: BLE001 — a crash is a suite failure
        # A gating suite must say plainly that it broke, not leave a bare
        # traceback for a caller to interpret.
        import traceback

        traceback.print_exc()
        print(f"\nSUITE ERRORED — {type(exc).__name__}: {exc}")
        print(f"{len(PASSES)} passed before the error")
        return 1


def run() -> int:
    work = Path(tempfile.mkdtemp(prefix="uiw-ocfl-"))
    try:
        source_dir = work / "src"
        source_dir.mkdir()
        original = write(source_dir, "original.html", "<html>instrument text</html>")
        ocr = write(source_dir, "extracted.txt", "instrument text")

        # -- DR-0076: tier-separated roots ---------------------------------

        permanent = StorageRoot(work / "permanent", "permanent")
        medium = StorageRoot(work / "medium-term", "medium-term")
        permanent.initialize()
        medium.initialize()

        check("DR-0076", "storage roots exist per retention tier",
              permanent.namaste.is_file() and medium.namaste.is_file())

        check("DR-0073", "root declares OCFL 1.1 in its namaste file",
              permanent.namaste.read_text().strip() == "ocfl_1.1")

        check("DR-0076", "root declares its storage layout",
              json.loads((permanent.path / "ocfl_layout.json").read_text())["extension"]
              == "0004-hashed-n-tuple-storage-layout")

        rejects("DR-0076", "a tier without a storage root is refused",
                lambda: StorageRoot(work / "nope", "metadata-only"))

        check("DR-0076", "object paths are hashed, not derived from the id",
              "holding" not in hashed_n_tuple("holding-eu-reg-269-2014"))

        # -- DR-0074: the object is a holding; v1 is the original ----------

        holding_id = "holding-eu-reg-269-2014"
        permanent.create_object(
            holding_id,
            [ContentFile(original, "original.html")],
            message="Gate 1 admission: original as acquired",
            user="collector",
        )

        inventory = permanent.read_inventory(holding_id)
        check("DR-0074", "a new holding starts at v1 holding the original",
              inventory["head"] == "v1"
              and list(inventory["versions"]["v1"]["state"].values())[0]
              == ["original.html"])

        # -- DR-0075: dual digests ----------------------------------------

        check("DR-0075", f"content is addressed by {CONTENT_ALGORITHM}",
              inventory["digestAlgorithm"] == CONTENT_ALGORITHM)

        check("DR-0075", f"a {FIXITY_ALGORITHM} fixity block is present",
              bool(inventory["fixity"][FIXITY_ALGORITHM]))

        check("DR-0005", "the fixity block covers the stored content",
              len(inventory["fixity"][FIXITY_ALGORITHM])
              == len(inventory["manifest"]))

        # -- DR-0074: derivatives are later versions -----------------------

        permanent.add_version(
            holding_id,
            [ContentFile(ocr, "derivatives/extracted.txt")],
            message="OCR derivative",
            user="pipeline",
        )
        inventory = permanent.read_inventory(holding_id)

        check("DR-0074", "a derivative becomes a later version",
              inventory["head"] == "v2")

        v1_paths = [p for ps in inventory["versions"]["v1"]["state"].values() for p in ps]
        v2_paths = [p for ps in inventory["versions"]["v2"]["state"].values() for p in ps]
        check("DR-0074", "v2 carries the original forward alongside the derivative",
              set(v1_paths) <= set(v2_paths) and "derivatives/extracted.txt" in v2_paths)

        # PRES-001: the original's bytes are untouched by the later version.
        original_content = (
            permanent.object_path(holding_id) / "v1" / "content" / "original.html"
        )
        check("PRES-001", "the original in v1 is untouched by later versions",
              original_content.read_text() == "<html>instrument text</html>")

        # -- Forward delta: unchanged content is referenced, not copied -----

        permanent.add_version(
            holding_id,
            [ContentFile(original, "original.html")],
            message="Re-adding identical content",
            user="pipeline",
        )
        inventory = permanent.read_inventory(holding_id)
        copies = [
            p for paths in inventory["manifest"].values() for p in paths
            if p.endswith("original.html")
        ]
        check("DR-0073", "forward-delta references unchanged content rather than copying",
              len(copies) == 1 and copies[0].startswith("v1/"))

        # -- Conformance of what we wrote ----------------------------------

        problems = validate_object(permanent, holding_id)
        check("DR-0073", "the written object passes validation",
              problems == [])
        if problems:
            FAILURES.extend(f"       {p}" for p in problems)

        check("PRES-002", "fixity verifies clean on an intact object",
              permanent.fixity_check(holding_id) == [])

        # -- PRES-003: fixity failure is detected, not silently repaired ----

        second = StorageRoot(work / "corrupt", "permanent")
        second.initialize()
        second.create_object(
            "holding-corrupt",
            [ContentFile(original, "original.html")],
            message="test",
            user="collector",
        )
        target = (
            second.object_path("holding-corrupt") / "v1" / "content" / "original.html"
        )
        target.write_text("tampered")
        problems = second.fixity_check("holding-corrupt")
        check("PRES-003", "content tampering is detected by fixity check",
              any("mismatch" in p for p in problems))
        check("PRES-003", "both digest algorithms flag the tampering",
              any(CONTENT_ALGORITHM in p for p in problems)
              and any(FIXITY_ALGORITHM in p for p in problems))

        # -- The permanent archive is a separate root ----------------------

        check("DR-0076", "an object in one tier's root is absent from the other",
              permanent.has_object(holding_id) and not medium.has_object(holding_id))

        # -- Guards --------------------------------------------------------

        rejects("DR-0074", "creating an object that already exists is refused",
                lambda: permanent.create_object(
                    holding_id, [ContentFile(original, "x.html")], "dup", "test"))

        rejects("DR-0074", "adding a version to a nonexistent object is refused",
                lambda: permanent.add_version(
                    "holding-absent", [ContentFile(original, "x.html")], "m", "u"))

        rejects("DR-0073", "initializing a non-empty root is refused",
                lambda: StorageRoot(work / "permanent", "permanent").initialize())

        # -- PRES-009: readable without this code ---------------------------

        root_readme = (permanent.path / "README.txt").read_text()
        check("PRES-009", "the root explains itself to a reader without this code",
              "ocfl.io" in root_readme and "holding" in root_readme)

        # -- Detecting a broken inventory ----------------------------------

        broken = StorageRoot(work / "broken", "permanent")
        broken.initialize()
        broken.create_object(
            "holding-broken", [ContentFile(original, "o.html")], "m", "u")
        inventory_path = broken.object_path("holding-broken") / "inventory.json"
        data = json.loads(inventory_path.read_text())
        del data["fixity"]
        inventory_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        problems = validate_object(broken, "holding-broken")
        check("DR-0075", "validation catches a missing fixity block",
              any("fixity" in p for p in problems))
        check("DR-0073", "validation catches a sidecar that no longer matches",
              any("sidecar" in p for p in problems))

    finally:
        shutil.rmtree(work, ignore_errors=True)

    for line in PASSES:
        print(line)
    for line in FAILURES:
        print(line)
    print(f"\n{len(PASSES)} passed, {len(FAILURES)} failed")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
