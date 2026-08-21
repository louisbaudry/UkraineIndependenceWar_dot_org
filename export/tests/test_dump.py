#!/usr/bin/env python3
"""Tests for the durable export.

Populates a real archive by running the real collector, dumps it, then runs
the reconstruction as a **separate process** so it cannot accidentally rely
on anything already imported here.

Run:  PGHOST=… PGPORT=… PGUSER=… python3 export/tests/test_dump.py
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "collector"))
sys.path.insert(0, str(ROOT / "storage"))
sys.path.insert(0, str(ROOT / "export"))

import psycopg  # noqa: E402

from dump import create_dump, list_tables, verify_dump  # noqa: E402
from fetch import FixtureFetcher  # noqa: E402
from ocfl import StorageRoot  # noqa: E402
from pipeline import Collector  # noqa: E402

PASSES: list[str] = []
FAILURES: list[str] = []
DB = "uiw_export_test"


def check(req: str, what: str, condition: bool) -> None:
    (PASSES if condition else FAILURES).append(
        f"{'PASS' if condition else 'FAIL'}  {req} — {what}"
    )


def build_database() -> None:
    subprocess.run(
        ["psql", "-q", "-c", f"DROP DATABASE IF EXISTS {DB}",
         "-c", f"CREATE DATABASE {DB}", "postgres"],
        check=True, capture_output=True,
    )
    for sql in sorted((ROOT / "schema").glob("0*.sql")):
        subprocess.run(
            ["psql", "-q", "-d", DB, "-v", "ON_ERROR_STOP=1", "-f", str(sql)],
            check=True, capture_output=True,
        )


def run() -> int:
    build_database()
    work = Path(tempfile.mkdtemp(prefix="uiw-export-"))

    fixture = work / "instrument.html"
    fixture.write_text("<html>Council Regulation — test fixture</html>")

    roots = {
        "permanent": StorageRoot(work / "ocfl-permanent", "permanent"),
        "medium-term": StorageRoot(work / "ocfl-medium", "medium-term"),
    }
    for root in roots.values():
        root.initialize()

    conn = psycopg.connect(dbname=DB, autocommit=True)
    try:
        # ---- populate a real archive by running the real collector -------

        agent_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO pipeline_agent (id, kind, name, software_version) "
            "VALUES (%s,'software','test-collector','0.1.0')", (agent_id,))
        source_id = str(uuid.uuid4())
        conn.execute(
            """INSERT INTO source (id, source_type, name, locator,
               collection_method, default_retention_tier, default_access_tier,
               rights_permission)
               VALUES (%s,'government','Test source','https://example.invalid',
                       'http','permanent','public','may-preserve')""",
            (source_id,))

        collector = Collector(
            conn,
            FixtureFetcher({"https://example.invalid/reg": fixture,
                            "https://example.invalid/gone": FileNotFoundError("404")}),
            work / "quarantine", roots, agent_id,
        )
        collector.run(source_id,
                      ["https://example.invalid/reg", "https://example.invalid/gone"],
                      configuration={"test": True})

        # An assertion, so the dump carries epistemic content too.
        prop_id = str(uuid.uuid4())
        holding_id = conn.execute("SELECT id FROM holding LIMIT 1").fetchone()[0]
        conn.execute("INSERT INTO proposition (id, statement) VALUES (%s,%s)",
                     (prop_id, "The regulation was published on the stated date."))
        conn.execute(
            """INSERT INTO documentary_assertion
               (id, valid_time, asserter_id, epistemic_category, proposition_id,
                holding_id, locator)
               VALUES (%s, ROW('2014-03-17'::timestamptz,NULL,NULL,NULL,NULL)::timespan,
                       %s,'claim',%s,%s,'{"selector":"TextQuote"}'::jsonb)""",
            (str(uuid.uuid4()), agent_id, prop_id, holding_id))

        # ---- dump --------------------------------------------------------

        dump_dir = work / "dump"
        manifest = create_dump(conn, dump_dir, ROOT / "registry/dist/registry.json")

        # ---- DR-0058: the dump is complete by construction ---------------

        dumped = set(manifest["tables"])
        in_database = set(list_tables(conn))
        check("DR-0058", "every table in the database is in the dump",
              dumped == in_database)

        check("DR-0058", "the dump carries data, not just structure",
              manifest["total_rows"] > 0)

        check("DR-0058", "both JSONL and CSV are produced for every table",
              all(set(t["files"]) == {"jsonl", "csv"} for t in manifest["tables"].values()))

        check("DR-0058", "the dump records the registry version it was made against",
              manifest["registry_version"] is not None)

        # ---- DR-0005 / DR-0048: fixity over the dump ---------------------

        check("DR-0005", "the dump verifies against its own manifest",
              verify_dump(dump_dir) == [])

        target = dump_dir / manifest["tables"]["holding"]["files"]["jsonl"]["path"]
        original = target.read_text()
        target.write_text(original.replace("original", "tampered", 1))
        check("DR-0005", "tampering with dumped data is detected",
              any("digest" in p for p in verify_dump(dump_dir)))
        target.write_text(original)
        check("DR-0005", "the dump verifies clean again once restored",
              verify_dump(dump_dir) == [])

        # ---- DATA-008: the schema descriptor links to the registry -------

        schema = json.loads((dump_dir / "schema.json").read_text())
        linked = [
            (t, c["name"], c["registry_entry"])
            for t, spec in schema["tables"].items()
            for c in spec["columns"] if "registry_entry" in c
        ]
        check("DATA-008", "vocabulary columns resolve to their registry entry",
              len(linked) > 0)
        check("DATA-008", "enum columns carry their permitted values inline",
              all("enum_values" in c
                  for spec in schema["tables"].values()
                  for c in spec["columns"] if "registry_entry" in c))

        composite = [
            c for spec in schema["tables"].values() for c in spec["columns"]
            if "composite_fields" in c
        ]
        check("EVID-010", "composite columns describe their internal fields",
              any(any(f["name"] == "absence" for f in c["composite_fields"])
                  for c in composite))

        # ---- the JSONL preserves what CSV would flatten -------------------

        assertions = [
            json.loads(line) for line in
            (dump_dir / "data/documentary_assertion.jsonl").open() if line.strip()
        ]
        check("EVID-010", "a time span keeps its structure in JSONL",
              isinstance(assertions[0]["valid_time"], dict)
              and "absence" in assertions[0]["valid_time"])

        # ---- PRES-009: reconstruction, in a separate process --------------

        result = subprocess.run(
            [sys.executable, str(ROOT / "export/tests/reconstruct.py"),
             str(dump_dir), str(roots["permanent"].path), str(roots["medium-term"].path)],
            capture_output=True, text=True,
            # A bare environment: nothing on the path that could smuggle in
            # project modules.
            env={"PATH": os.environ.get("PATH", ""), "HOME": os.environ.get("HOME", "")},
            cwd=work,
        )
        check("PRES-009", "the archive reconstructs without project code",
              result.returncode == 0)
        if result.returncode != 0:
            FAILURES.extend(f"       {line}" for line in
                            (result.stdout + result.stderr).splitlines()[-12:])
        else:
            for line in result.stdout.splitlines():
                if line.strip().startswith(("dump:", "schema:", "archive:",
                                            "reconstructed", "absence:")):
                    PASSES.append(f"      · {line.strip()}")

        # ---- the reconstruction notices a broken archive ------------------

        broken = work / "dump-broken"
        shutil.copytree(dump_dir, broken)
        holdings_file = broken / "data/holding.jsonl"
        rows = [json.loads(x) for x in holdings_file.open() if x.strip()]
        for row in rows:
            row["ocfl_object_id"] = "holding-that-does-not-exist"
        holdings_file.write_text("".join(json.dumps(r) + "\n" for r in rows))
        # Re-point the manifest so it is the archive that is broken, not the
        # fixity — otherwise the digest check would mask the real failure.
        manifest_path = broken / "manifest.json"
        m = json.loads(manifest_path.read_text())
        import hashlib
        m["tables"]["holding"]["files"]["jsonl"]["sha256"] = hashlib.sha256(
            holdings_file.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(m, indent=2, sort_keys=True) + "\n")
        (broken / "manifest.json.sha256").write_text(
            hashlib.sha256(manifest_path.read_bytes()).hexdigest() + "  manifest.json\n")

        result = subprocess.run(
            [sys.executable, str(ROOT / "export/tests/reconstruct.py"),
             str(broken), str(roots["permanent"].path)],
            capture_output=True, text=True, cwd=work,
        )
        check("PRES-009", "reconstruction fails when the bytes are missing",
              result.returncode == 1 and "not found" in result.stdout)

    finally:
        conn.close()
        shutil.rmtree(work, ignore_errors=True)

    for line in PASSES:
        print(line)
    for line in FAILURES:
        print(line)
    real = [p for p in PASSES if p.startswith("PASS")]
    print(f"\n{len(real)} passed, {len(FAILURES)} failed")
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
