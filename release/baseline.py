#!/usr/bin/env python3
"""Release baselines.

Implements DR-0048: a release is a **named, frozen baseline** over versioned
configuration items, not a tagged commit. DR-0047 fixed that the project has
no single version number — code, schema, registry, data, methodology and
terminology each version differently — so a release is the act of pinning one
of each and attesting to the result.

What a baseline must carry (DR-0048, OPS-002):

    dataset snapshot            a preservation dump (DR-0058, SPEC-0006)
    schema version              the canonical store's DDL state
    registry version            the semantic registry (DR-0078)
    collector version           what gathered the data
    pipeline version            what processed it
    methodology version         the METH document in force (§97)
    terminology version         localization resources (§60-61)
    code commit                 the git revision
    build configuration         how it was produced
    ---
    integrity manifest          checksums over everything (DR-0005)
    coverage statement          what was collected, and the gaps (§57)
    known limitations           stated, not discovered later
    licensing                   what a recipient may do
    changelog                   what changed since the last baseline
    change sets                 merged/split/retracted mappings (§91, OPS-003)

**Creation fails closed.** A baseline missing any configuration item is not
created, because a release whose reproducibility depends on an unrecorded
version is not reproducible (Principle 16). `--check` reports what is missing
without creating anything, which is the useful thing to run long before a
first release is possible.

Usage:
  python3 release/baseline.py --check
  python3 release/baseline.py --create <dir> --name 2026.1 --dump <dump-dir> …
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import psycopg

ROOT = Path(__file__).resolve().parent.parent

# Every configuration item a baseline must pin (DR-0047's dimensions).
# Adding a dimension here makes every future release refuse until it can be
# pinned — which is the intended cost of introducing one.
REQUIRED_ITEMS = (
    "code_commit",
    "schema_version",
    "registry_version",
    "collector_version",
    "pipeline_version",
    "methodology_version",
    "terminology_version",
    "build_configuration",
    "dataset_snapshot",
)


class BaselineIncomplete(Exception):
    """Raised when a release cannot be pinned, so it must not be created."""


@dataclass
class Configuration:
    """The pinnable state of the system at one moment."""

    items: dict[str, str | None] = field(default_factory=dict)
    notes: dict[str, str] = field(default_factory=dict)

    def missing(self) -> list[str]:
        return [k for k in REQUIRED_ITEMS if not self.items.get(k)]

    def complete(self) -> bool:
        return not self.missing()


def _git(*args: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
        )
        return out.stdout.strip() or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _sha256_tree(directory: Path) -> str:
    """A digest over a directory's contents, order-independent."""
    entries = sorted(
        (str(p.relative_to(directory)), _sha256_file(p))
        for p in directory.rglob("*") if p.is_file()
    )
    return hashlib.sha256(
        "\n".join(f"{name}  {digest}" for name, digest in entries).encode()
    ).hexdigest()


def _effective_document_version(path: Path) -> str | None:
    """Read a controlled document's version, but only if it is effective.

    A draft cannot be pinned: pinning one would claim a release rests on a
    document that carries no authority (DR-0046).
    """
    if not path.is_file():
        return None
    head = path.read_text()[:1200]
    if "Status:** Approved — Effective" not in head:
        return None
    for line in head.splitlines():
        if "**Version:**" in line:
            fragment = line.split("**Version:**")[1]
            return fragment.split("|")[0].strip()
    return None


def collect_configuration(
    conn: psycopg.Connection | None = None,
    dump_dir: Path | None = None,
) -> Configuration:
    """Gather what can be pinned right now, and note what cannot."""
    config = Configuration()

    # -- code -------------------------------------------------------------
    commit = _git("rev-parse", "HEAD")
    config.items["code_commit"] = commit
    dirty = _git("status", "--porcelain")
    if dirty:
        config.notes["code_commit"] = (
            "working tree is not clean; a baseline pinned to this commit would "
            "not describe what was actually built"
        )
        config.items["code_commit"] = None

    # -- schema -----------------------------------------------------------
    # No schema version file yet; the DDL's own digest stands in, so a
    # baseline still pins exactly which schema produced it.
    schema_files = sorted((ROOT / "schema").glob("0*.sql"))
    if schema_files:
        digest = hashlib.sha256(
            "".join(_sha256_file(f) for f in schema_files).encode()
        ).hexdigest()
        config.items["schema_version"] = f"sha256:{digest[:16]}"
        config.notes["schema_version"] = (
            "derived from the DDL digest; no explicit schema version scheme "
            "exists yet (DR-0047 assigns schemas a SemVer regime)"
        )

    # -- registry ---------------------------------------------------------
    compiled = ROOT / "registry" / "dist" / "registry.json"
    if compiled.is_file():
        config.items["registry_version"] = json.loads(
            compiled.read_text()
        )["registry"]["version"]

    # -- collector and pipeline -------------------------------------------
    # Software agents carry their version (AI-002); a release pins what
    # actually ran, not what is installed.
    if conn is not None:
        for key, name in (("collector_version", "collector"),
                          ("pipeline_version", "pipeline")):
            row = conn.execute(
                """
                SELECT DISTINCT software_version FROM pipeline_agent
                 WHERE kind = 'software' AND name ILIKE %s
                 ORDER BY software_version DESC LIMIT 1
                """,
                (f"%{name}%",),
            ).fetchone()
            if row:
                config.items[key] = row[0]
            else:
                config.notes[key] = f"no software agent named like {name!r} has run"

    # -- methodology and terminology --------------------------------------
    meth = next((ROOT / "docs" / "methodology").glob("METH-*.md"), None) \
        if (ROOT / "docs" / "methodology").is_dir() else None
    config.items["methodology_version"] = (
        _effective_document_version(meth) if meth else None
    )
    if not config.items["methodology_version"]:
        # "None written" and "one written, not yet approved" are different
        # states and the report says which, rather than leaving the reader to
        # infer that nothing exists (DR-0029's rule applied to this tool's
        # own output).
        config.notes["methodology_version"] = (
            f"{meth.name} exists but is not Approved — Effective; a draft "
            "carries no authority and pinning one would claim a release rests "
            "on it (DR-0046)"
            if meth else
            "no METH document exists at all"
        ) + ". §97 makes methodology a first-class versioned artifact and " \
            "DR-0047 requires releases to pin it; until one is effective, " \
            "no release can be created"

    # Terminology travels with the registry until localization resources
    # exist as their own versioned artifact (DR-0081: none are seeded).
    if config.items.get("registry_version"):
        config.items["terminology_version"] = (
            f"registry:{config.items['registry_version']}"
        )
        config.notes["terminology_version"] = (
            "no localization resources exist yet (DR-0081 seeds no "
            "translations), so terminology is pinned to the registry version "
            "that carries the English labels"
        )

    # -- build configuration ----------------------------------------------
    config.items["build_configuration"] = json.dumps(
        {"python": sys.version.split()[0], "platform": sys.platform},
        sort_keys=True,
    )

    # -- dataset snapshot --------------------------------------------------
    if dump_dir and (dump_dir / "manifest.json").is_file():
        manifest = json.loads((dump_dir / "manifest.json").read_text())
        if manifest.get("purpose") != "preservation":
            config.notes["dataset_snapshot"] = (
                f"dump purpose is {manifest.get('purpose')!r}; a baseline pins "
                "a preservation dump, since a filtered one is not the archive "
                "(SPEC-0006 §9A)"
            )
        else:
            config.items["dataset_snapshot"] = (
                f"sha256:{_sha256_tree(dump_dir)[:16]}"
            )
    else:
        config.notes["dataset_snapshot"] = "no preservation dump supplied"

    return config


def coverage_statement(conn: psycopg.Connection) -> dict:
    """What was collected and what was missed (§57, DR-0070, OPS-006)."""
    per_source = [
        {
            "source": name,
            "runs": runs,
            "discovered": discovered or 0,
            "acquired": acquired or 0,
            "skipped": skipped or 0,
            "failed": failed or 0,
            "first_run": first.isoformat() if first else None,
            "last_run": last.isoformat() if last else None,
            "outages": outages or 0,
        }
        for name, runs, discovered, acquired, skipped, failed, first, last, outages
        in conn.execute(
            """
            SELECT s.name, count(r.id),
                   sum(r.items_discovered), sum(r.items_acquired),
                   sum(r.items_skipped), sum(r.items_failed),
                   min(r.started_at), max(r.started_at),
                   count(r.outage_note)
              FROM source s LEFT JOIN collector_run r ON r.source_id = s.id
             GROUP BY s.name ORDER BY s.name
            """
        )
    ]
    return {
        "per_source": per_source,
        "note": (
            "Frequency in the archive is not frequency in the world (§57). "
            "Skipped and failed counts, and any outages, are part of what this "
            "release covers — absence here does not mean absence in the world."
        ),
    }


def change_sets(conn: psycopg.Connection) -> dict:
    """Merged, split and retracted object mappings (§91, OPS-003).

    Ships from the first data release. May be empty — must be present, so a
    consumer can follow identity changes mechanically rather than guessing.
    """
    disproved = [
        {"entity": str(row[0]), "status": row[1]}
        for row in conn.execute(
            "SELECT id, status::text FROM world_actor WHERE status = 'disproved'"
        )
    ]
    redacted = [
        {"assertion": str(row[0]), "family": "documentary_assertion",
         "ground": row[1], "authority": row[2]}
        for row in conn.execute(
            """SELECT id, redaction_ground, redaction_authority
                 FROM documentary_assertion WHERE redacted_at IS NOT NULL"""
        )
    ]
    superseded = [
        {"superseded": str(row[0]), "by": str(row[1])}
        for row in conn.execute(
            """SELECT supersedes_id, id FROM documentary_assertion
                WHERE supersedes_id IS NOT NULL"""
        )
    ]
    return {
        "merged": [],   # populated once merge events exist (DR-0064)
        "split": [],
        "disproved_entities": disproved,
        "retracted": redacted,
        "superseded": superseded,
    }


def create_baseline(
    output: Path,
    name: str,
    conn: psycopg.Connection,
    dump_dir: Path,
    licensing: str,
    changelog: str,
    known_limitations: list[str],
    ocfl_roots: dict[str, Path] | None = None,
    configuration: Configuration | None = None,
) -> dict:
    """Freeze a baseline. Refuses unless every configuration item is pinned.

    `configuration` may be supplied by a caller that has assembled it
    otherwise; the completeness check applies either way, so passing one is
    not a way around fail-closed.
    """
    config = configuration or collect_configuration(conn, dump_dir)
    if not config.complete():
        raise BaselineIncomplete(
            "cannot create a release baseline; unpinned configuration item(s): "
            + ", ".join(config.missing())
            + ". "
            + " ".join(
                f"[{k}] {v}" for k, v in config.notes.items() if k in config.missing()
            )
        )
    if not licensing:
        raise BaselineIncomplete("a baseline must state its licensing (DR-0048)")
    if not changelog:
        raise BaselineIncomplete("a baseline must carry a changelog (DR-0048)")

    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise BaselineIncomplete(f"{output} is not empty; baselines are frozen")

    coverage = coverage_statement(conn)
    changes = change_sets(conn)

    (output / "coverage.json").write_text(
        json.dumps(coverage, indent=2, sort_keys=True) + "\n")
    (output / "change-sets.json").write_text(
        json.dumps(changes, indent=2, sort_keys=True) + "\n")
    (output / "CHANGELOG.md").write_text(changelog if changelog.endswith("\n")
                                         else changelog + "\n")

    storage_state = {}
    for tier, path in (ocfl_roots or {}).items():
        if Path(path).is_dir():
            storage_state[tier] = {"path": str(path),
                                   "digest": f"sha256:{_sha256_tree(Path(path))[:16]}"}

    manifest = {
        "release": name,
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "decision_record": "DR-0048",
        "configuration": config.items,
        "configuration_notes": config.notes,
        "storage_state": storage_state,
        "licensing": licensing,
        "known_limitations": known_limitations,
        "integrity": {
            name: {"sha256": _sha256_file(output / name)}
            for name in ("coverage.json", "change-sets.json", "CHANGELOG.md")
        },
        "dataset_snapshot_manifest": json.loads(
            (dump_dir / "manifest.json").read_text()
        ),
    }
    manifest_path = output / "baseline.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    (output / "baseline.json.sha256").write_text(
        f"{_sha256_file(manifest_path)}  baseline.json\n")
    return manifest


def verify_baseline(output: Path) -> list[str]:
    problems: list[str] = []
    manifest_path = output / "baseline.json"
    if not manifest_path.is_file():
        return ["missing baseline.json"]
    sidecar = output / "baseline.json.sha256"
    if not sidecar.is_file():
        problems.append("missing baseline sidecar")
    elif sidecar.read_text().split()[0] != _sha256_file(manifest_path):
        problems.append("baseline manifest does not match its sidecar")

    manifest = json.loads(manifest_path.read_text())
    for missing in [k for k in REQUIRED_ITEMS if not manifest["configuration"].get(k)]:
        problems.append(f"configuration item not pinned: {missing}")
    for name, meta in manifest.get("integrity", {}).items():
        path = output / name
        if not path.is_file():
            problems.append(f"missing {name}")
        elif _sha256_file(path) != meta["sha256"]:
            problems.append(f"{name} does not match its recorded digest")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--dbname")
    parser.add_argument("--dump", type=Path)
    args = parser.parse_args()

    conn = None
    if args.dbname:
        conn = psycopg.connect(dbname=args.dbname, autocommit=True)

    config = collect_configuration(conn, args.dump)
    print("Release baseline readiness (DR-0048)")
    print("=" * 60)
    for item in REQUIRED_ITEMS:
        value = config.items.get(item)
        mark = "pinned " if value else "MISSING"
        shown = (value[:52] + "…") if value and len(value) > 53 else (value or "")
        print(f"  {mark}  {item:<22} {shown}")
        if item in config.notes:
            print(f"           └─ {config.notes[item]}")

    if config.complete():
        print("\nAll configuration items pinned; a baseline can be created.")
        return 0
    print(f"\nNot ready: {len(config.missing())} item(s) unpinned. "
          "No release can be created until each is resolved (Principle 16).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
