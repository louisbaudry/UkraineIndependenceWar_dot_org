#!/usr/bin/env python3
"""Tests for periodic fixity checking (PRES-003).

Run:  PGHOST=… PGPORT=… PGUSER=… python3 storage/tests/test_fixity_schedule.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "storage"))

import psycopg  # noqa: E402

from fixity_schedule import CADENCE_DAYS, due_objects, run_checks  # noqa: E402
from ocfl import ContentFile, StorageRoot  # noqa: E402

PASSES: list[str] = []
FAILURES: list[str] = []
DB = "uiw_fixity_test"


def check(req: str, what: str, condition: bool) -> None:
    (PASSES if condition else FAILURES).append(
        f"{'PASS' if condition else 'FAIL'}  {req} — {what}")


def build_database() -> None:
    subprocess.run(["psql", "-q", "-c", f"DROP DATABASE IF EXISTS {DB}",
                    "-c", f"CREATE DATABASE {DB}", "postgres"],
                   check=True, capture_output=True)
    for sql in sorted((ROOT / "schema").glob("0*.sql")):
        subprocess.run(["psql", "-q", "-d", DB, "-v", "ON_ERROR_STOP=1", "-f", str(sql)],
                       check=True, capture_output=True)


def insert_object(conn, root: StorageRoot, tier: str, source: Path, name: str) -> str:
    ocfl_id = f"holding-{name}"
    root.create_object(ocfl_id, [ContentFile(source, "original.bin")],
                       message="test", user="test")
    inventory = root.read_inventory(ocfl_id)
    object_id = str(uuid.uuid4())
    conn.execute(
        """INSERT INTO preserved_object (id, object_level, sha512, sha256,
           ocfl_root, ocfl_object_id, ocfl_version, ingested_at)
           VALUES (%s,'representation', decode(%s,'hex'), decode(%s,'hex'),
                   %s,%s,'v1',%s)""",
        (object_id, next(iter(inventory["manifest"])),
         next(iter(inventory["fixity"]["sha256"])), tier, ocfl_id,
         datetime.now(timezone.utc)))
    return object_id


def run() -> int:
    build_database()
    work = Path(tempfile.mkdtemp(prefix="uiw-fixity-"))
    conn = psycopg.connect(dbname=DB, autocommit=True)
    try:
        source = work / "content.bin"
        source.write_bytes(b"preserved content")

        roots = {
            "permanent": StorageRoot(work / "permanent", "permanent"),
            "medium-term": StorageRoot(work / "medium", "medium-term"),
        }
        for root in roots.values():
            root.initialize()

        agent_id = str(uuid.uuid4())
        conn.execute("INSERT INTO pipeline_agent (id, kind, name, software_version) "
                     "VALUES (%s,'software','fixity-checker','0.1.0')", (agent_id,))

        good = insert_object(conn, roots["permanent"], "permanent", source, "good")
        bad = insert_object(conn, roots["permanent"], "permanent", source, "bad")
        medium = insert_object(conn, roots["medium-term"], "medium-term", source, "med")

        # -- PRES-003: cadence is defined in the system, not in a cron job --

        check("PRES-003", "a cadence is defined for every tier that holds bytes",
              set(CADENCE_DAYS) == {"permanent", "medium-term"}
              and all(d > 0 for d in CADENCE_DAYS.values()))
        check("PRES-003", "permanent material is checked more often than medium-term",
              CADENCE_DAYS["permanent"] < CADENCE_DAYS["medium-term"])

        # -- never-checked objects are due immediately ----------------------

        due = due_objects(conn)
        # psycopg returns UUID objects; compare as strings.
        check("PRES-003", "an object never verified is due immediately",
              {str(row[0]) for row in due} == {good, bad, medium})
        check("PRES-003", "never-verified objects are listed before stale ones",
              due[0][3] is None)

        # -- running checks records an event per object ---------------------

        summary = run_checks(conn, roots, agent_id)
        check("PRES-003", "every due object is checked", summary["checked"] == 3)
        check("PRES-003", "intact objects pass", summary["passed"] == 3)

        events = conn.execute(
            "SELECT count(*) FROM preservation_event "
            "WHERE event_type = 'fixity-check' AND outcome = 'success'").fetchone()[0]
        check("DR-0060", "each check is recorded as a preservation event",
              events == 3)

        # -- a checked object is no longer due ------------------------------

        check("PRES-003", "a freshly verified object is not due again",
              due_objects(conn) == [])

        # -- corruption is recorded as a failure, not repaired --------------

        target = (roots["permanent"].object_path("holding-bad")
                  / "v1" / "content" / "original.bin")
        target.write_bytes(b"corrupted")

        # Age the successful check past the cadence so the object comes due.
        conn.execute(
            """UPDATE preservation_event SET occurred_at = %s
                WHERE object_id = %s AND event_type = 'fixity-check'""",
            (datetime.now(timezone.utc) - timedelta(days=CADENCE_DAYS["permanent"] + 1),
             bad))

        due = due_objects(conn)
        check("PRES-003", "an object past its cadence comes due again",
              [str(row[0]) for row in due] == [bad])

        summary = run_checks(conn, roots, agent_id)
        check("PRES-003", "corruption is detected", summary["failed"] == 1)

        failure = conn.execute(
            """SELECT outcome, outcome_detail FROM preservation_event
                WHERE object_id = %s AND outcome = 'failure'""", (bad,)).fetchone()
        check("DR-0060", "the failure is recorded as an event with detail",
              failure is not None and "mismatch" in failure[1])

        check("PRES-003", "the corrupted content is left as found, not repaired",
              target.read_bytes() == b"corrupted")

        check("PRES-003", "a failed check does not count as verification",
              bad in {str(row[0]) for row in due_objects(conn)})

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
