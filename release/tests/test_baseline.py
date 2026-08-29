#!/usr/bin/env python3
"""Tests for release baselines (DR-0048, OPS-002/003/006).

Run:  PGHOST=… PGPORT=… PGUSER=… python3 release/tests/test_baseline.py
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
for sub in ("collector", "storage", "export", "release"):
    sys.path.insert(0, str(ROOT / sub))

import psycopg  # noqa: E402

from baseline import (  # noqa: E402
    REQUIRED_ITEMS,
    BaselineIncomplete,
    _effective_document_version,
    Configuration,
    change_sets,
    collect_configuration,
    coverage_statement,
    create_baseline,
    verify_baseline,
)
from dump import create_dump  # noqa: E402
from fetch import FixtureFetcher  # noqa: E402
from ocfl import StorageRoot  # noqa: E402
from pipeline import Collector  # noqa: E402

PASSES: list[str] = []
FAILURES: list[str] = []
DB = "uiw_release_test"


def check(req: str, what: str, condition: bool) -> None:
    (PASSES if condition else FAILURES).append(
        f"{'PASS' if condition else 'FAIL'}  {req} — {what}")


def rejects(req: str, what: str, fn) -> None:
    try:
        fn()
    except BaselineIncomplete:
        PASSES.append(f"PASS  {req} — {what}")
        return
    FAILURES.append(f"FAIL  {req} — {what}: accepted but must be refused")


def build_database() -> None:
    subprocess.run(["psql", "-q", "-c", f"DROP DATABASE IF EXISTS {DB}",
                    "-c", f"CREATE DATABASE {DB}", "postgres"],
                   check=True, capture_output=True)
    for sql in sorted((ROOT / "schema").glob("0*.sql")):
        subprocess.run(["psql", "-q", "-d", DB, "-v", "ON_ERROR_STOP=1", "-f", str(sql)],
                       check=True, capture_output=True)


def complete_configuration(dump_dir: Path) -> Configuration:
    """A fully pinned configuration, as a real release would have."""
    config = collect_configuration(None, dump_dir)
    config.items.update({
        "code_commit": "0" * 40,
        "collector_version": "0.1.0",
        "pipeline_version": "0.1.0",
        "methodology_version": "1.0",
    })
    return config


def run() -> int:
    build_database()
    work = Path(tempfile.mkdtemp(prefix="uiw-release-"))
    conn = psycopg.connect(dbname=DB, autocommit=True)
    try:
        # ---- populate an archive ------------------------------------------

        fixture = work / "instrument.html"
        fixture.write_text("<html>fixture</html>")
        roots = {"permanent": StorageRoot(work / "ocfl-permanent", "permanent"),
                 "medium-term": StorageRoot(work / "ocfl-medium", "medium-term")}
        for root in roots.values():
            root.initialize()

        agent_id = str(uuid.uuid4())
        conn.execute("INSERT INTO pipeline_agent (id, kind, name, software_version) "
                     "VALUES (%s,'software','test-collector','0.1.0')", (agent_id,))
        source_id = str(uuid.uuid4())
        conn.execute(
            """INSERT INTO source (id, source_type, name, collection_method,
               default_retention_tier, default_access_tier, rights_permission)
               VALUES (%s,'government','Test source','http','permanent','public',
                       'may-preserve')""", (source_id,))
        Collector(conn,
                  FixtureFetcher({"https://example.invalid/a": fixture,
                                  "https://example.invalid/b": TimeoutError("slow")}),
                  work / "quarantine", roots, agent_id).run(
            source_id, ["https://example.invalid/a", "https://example.invalid/b"],
            configuration={})

        preservation_dump = work / "dump"
        create_dump(conn, preservation_dump, ROOT / "registry/dist/registry.json",
                    purpose="preservation")

        # ---- OPS-002: creation fails closed -------------------------------

        check("DR-0047", "every versioning dimension is a required item",
              set(REQUIRED_ITEMS) >= {
                  "code_commit", "schema_version", "registry_version",
                  "collector_version", "pipeline_version",
                  "methodology_version", "terminology_version",
                  "build_configuration", "dataset_snapshot"})

        for item in ("methodology_version", "code_commit", "dataset_snapshot"):
            partial = complete_configuration(preservation_dump)
            partial.items[item] = None
            rejects("OPS-002", f"a baseline without {item} is refused",
                    lambda p=partial: create_baseline(
                        work / f"no-{item}", "test", conn, preservation_dump,
                        licensing="CC-BY-4.0", changelog="x",
                        known_limitations=[], configuration=p))

        rejects("OPS-002", "a baseline without licensing is refused",
                lambda: create_baseline(
                    work / "no-licence", "test", conn, preservation_dump,
                    licensing="", changelog="x", known_limitations=[],
                    configuration=complete_configuration(preservation_dump)))

        rejects("OPS-002", "a baseline without a changelog is refused",
                lambda: create_baseline(
                    work / "no-changelog", "test", conn, preservation_dump,
                    licensing="CC-BY-4.0", changelog="", known_limitations=[],
                    configuration=complete_configuration(preservation_dump)))

        # ---- a filtered dump is not an archive snapshot --------------------

        disclosure_dump = work / "dump-public"
        create_dump(conn, disclosure_dump, ROOT / "registry/dist/registry.json",
                    purpose="disclosure", access_tier="public")
        filtered_config = collect_configuration(None, disclosure_dump)
        check("SPEC-0006", "a disclosure dump cannot be pinned as the snapshot",
              filtered_config.items.get("dataset_snapshot") is None
              and "not the archive" in filtered_config.notes["dataset_snapshot"])

        # ---- a real baseline -----------------------------------------------

        release_dir = work / "release-2026.1"
        manifest = create_baseline(
            release_dir, "2026.1", conn, preservation_dump,
            licensing="CC-BY-4.0 for text; source material under its own terms",
            changelog="# 2026.1\n\nFirst baseline: pipeline through Gate 1.\n",
            known_limitations=[
                "HttpFetcher has never completed a live fetch (collector/README.md).",
                "OCFL conformance rests on the project's own validator (storage/README.md).",
            ],
            ocfl_roots={t: r.path for t, r in roots.items()},
            configuration=complete_configuration(preservation_dump),
        )

        check("DR-0048", "the baseline pins every configuration item",
              all(manifest["configuration"].get(i) for i in REQUIRED_ITEMS))
        check("DR-0048", "the baseline records its licensing",
              "CC-BY" in manifest["licensing"])
        check("DR-0048", "the baseline states known limitations rather than hiding them",
              len(manifest["known_limitations"]) == 2)
        check("DR-0048", "the baseline pins the storage state of every tier",
              set(manifest["storage_state"]) == {"permanent", "medium-term"})
        check("DR-0048", "the baseline embeds the dataset snapshot's manifest",
              manifest["dataset_snapshot_manifest"]["purpose"] == "preservation")

        # ---- OPS-006: coverage ships with the release ----------------------

        coverage = json.loads((release_dir / "coverage.json").read_text())
        source_row = coverage["per_source"][0]
        check("OPS-006", "coverage records what each source discovered",
              source_row["discovered"] == 2)
        check("OPS-006", "coverage records failures, not just successes",
              source_row["failed"] == 1 and source_row["acquired"] == 1)
        check("§57", "coverage warns that archive frequency is not world frequency",
              "not frequency in the world" in coverage["note"])

        # ---- OPS-003: change sets ship, even when empty --------------------

        changes = json.loads((release_dir / "change-sets.json").read_text())
        check("OPS-003", "change sets are present in the release",
              set(changes) >= {"merged", "split", "retracted", "superseded"})
        check("OPS-003", "an empty change set is present rather than omitted",
              changes["merged"] == [] and changes["split"] == [])

        # ---- integrity ------------------------------------------------------

        check("DR-0005", "the baseline verifies against its own manifest",
              verify_baseline(release_dir) == [])

        changelog = release_dir / "CHANGELOG.md"
        original = changelog.read_text()
        changelog.write_text(original + "tampered\n")
        check("DR-0005", "tampering with a released file is detected",
              any("digest" in p for p in verify_baseline(release_dir)))
        changelog.write_text(original)
        check("DR-0005", "the baseline verifies clean again once restored",
              verify_baseline(release_dir) == [])

        # ---- baselines are frozen -------------------------------------------

        rejects("DR-0048", "writing a second baseline into the same directory is refused",
                lambda: create_baseline(
                    release_dir, "2026.2", conn, preservation_dump,
                    licensing="CC-BY-4.0", changelog="x", known_limitations=[],
                    configuration=complete_configuration(preservation_dump)))

        # ---- the readiness check reports honestly ---------------------------

        live = collect_configuration(conn, preservation_dump)
        # .get(): when an item unexpectedly pins there is no note, and the
        # suite should report that as a failure rather than erroring.
        check("§97", "METH-0001 is effective, so methodology_version pins",
              live.items.get("methodology_version") == "1.0")
        check("DR-0047", "an unclean working tree blocks pinning the code commit",
              "code_commit" not in live.missing()
              or "not clean" in live.notes.get("code_commit", ""))

        # Draft rejection is tested against fixtures, not against the live
        # document. Asserting on METH-0001's own status would make the test
        # mean the opposite of itself the moment the founder approved it —
        # which is exactly what happened on 2026-08-26.
        header = ("# {id} — T\n\n**Class:** METH | **Version:** {v} | "
                  "**Status:** {status}\n")
        for status, version, pins in (
            ("Draft — Candidate for approval", "0.1", False),
            ("Proposed", "0.9", False),
            ("Approved — Effective", "1.0", True),
            ("Superseded", "1.0", False),
        ):
            fixture = work / f"meth-{version}-{status.split()[0]}.md"
            fixture.write_text(header.format(id="METH-0001", v=version,
                                             status=status))
            got = _effective_document_version(fixture)
            check("DR-0046",
                  f"a METH document marked {status.split(chr(32))[0]!r} "
                  f"{'pins' if pins else 'does not pin'}",
                  (got == version) is pins)

    finally:
        conn.close()
        shutil.rmtree(work, ignore_errors=True)

    for line in PASSES:
        print(line)
    for line in FAILURES:
        print(line)
    print(f"\n{len(PASSES)} passed, {len(FAILURES)} failed")
    return 1 if FAILURES else 0


def main() -> int:
    try:
        return run()
    except Exception as exc:  # noqa: BLE001
        import traceback
        traceback.print_exc()
        print(f"\nSUITE ERRORED — {type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
