#!/usr/bin/env python3
"""End-to-end tests for the collection pipeline.

Runs the real pipeline against a real PostgreSQL database and real OCFL
storage. Only the network is substituted (`FixtureFetcher`), because the
build environment's policy denies general internet hosts.

Each test names the requirement or Decision Record it verifies.

Run:  PGHOST=... PGPORT=... PGUSER=... python3 collector/tests/test_pipeline.py
"""

from __future__ import annotations

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

import psycopg  # noqa: E402

from fetch import FetchResult, FixtureFetcher  # noqa: E402
from ocfl import StorageRoot  # noqa: E402
from pipeline import Collector, PolicyViolation, find_orphaned_objects  # noqa: E402

PASSES: list[str] = []
FAILURES: list[str] = []
DB = "uiw_collector_test"


def check(req: str, what: str, condition: bool) -> None:
    (PASSES if condition else FAILURES).append(
        f"{'PASS' if condition else 'FAIL'}  {req} — {what}"
    )


def rejects(req: str, what: str, fn) -> None:
    try:
        fn()
    except Exception:
        PASSES.append(f"PASS  {req} — {what}")
        return
    FAILURES.append(f"FAIL  {req} — {what}: accepted but must be rejected")


def build_database() -> None:
    env = os.environ.copy()
    subprocess.run(
        ["psql", "-q", "-c", f"DROP DATABASE IF EXISTS {DB}",
         "-c", f"CREATE DATABASE {DB}", "postgres"],
        check=True, env=env, capture_output=True,
    )
    for sql in sorted((ROOT / "schema").glob("0*.sql")):
        subprocess.run(
            ["psql", "-q", "-d", DB, "-v", "ON_ERROR_STOP=1", "-f", str(sql)],
            check=True, env=env, capture_output=True,
        )


def seed_source(conn, **overrides) -> str:
    source_id = str(uuid.uuid4())
    values = {
        "source_type": "government",
        "name": "Test legal-instrument source",
        "locator": "https://example.invalid/oj",
        "collection_method": "http",
        "default_retention_tier": "permanent",
        "default_access_tier": "public",
        "rights_permission": "may-preserve",
        "lifecycle_state": "active",
        "expects_graphic_content": False,
    }
    values.update(overrides)
    conn.execute(
        """
        INSERT INTO source (id, source_type, name, locator, collection_method,
            default_retention_tier, default_access_tier, rights_permission,
            lifecycle_state, expects_graphic_content)
        VALUES (%(id)s, %(source_type)s, %(name)s, %(locator)s,
                %(collection_method)s, %(default_retention_tier)s,
                %(default_access_tier)s, %(rights_permission)s,
                %(lifecycle_state)s, %(expects_graphic_content)s)
        """,
        {"id": source_id, **values},
    )
    return source_id


def run() -> int:
    build_database()
    work = Path(tempfile.mkdtemp(prefix="uiw-collector-"))
    fixtures_dir = work / "fixtures"
    fixtures_dir.mkdir()

    instrument = fixtures_dir / "regulation.html"
    instrument.write_text(
        "<html><body>Council Regulation (EU) No 269/2014 — test fixture</body></html>"
    )
    malicious = fixtures_dir / "bad.bin"
    malicious.write_bytes(b"harmless prefix __MALICIOUS_TEST_MARKER__ suffix")

    roots = {
        "permanent": StorageRoot(work / "ocfl-permanent", "permanent"),
        "medium-term": StorageRoot(work / "ocfl-medium", "medium-term"),
    }
    for root in roots.values():
        root.initialize()

    conn = psycopg.connect(dbname=DB, autocommit=True)
    try:
        agent_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO pipeline_agent (id, kind, name, software_version) "
            "VALUES (%s, 'software', 'test-collector', '0.1.0')",
            (agent_id,),
        )
        source_id = seed_source(conn)

        fetcher = FixtureFetcher({
            "https://example.invalid/reg-269": instrument,
            "https://example.invalid/malicious": malicious,
            "https://example.invalid/gone": FetchResult(
                locator="https://example.invalid/gone",
                attempted_at=__import__("datetime").datetime.now(
                    __import__("datetime").timezone.utc),
                outcome="not-found", error_detail="HTTP 404: Not Found",
            ),
            "https://example.invalid/boom": TimeoutError("connection timed out"),
        })

        collector = Collector(
            conn, fetcher, work / "quarantine", roots, agent_id
        )

        run_id = collector.run(
            source_id,
            [
                "https://example.invalid/reg-269",
                "https://example.invalid/malicious",
                "https://example.invalid/gone",
                "https://example.invalid/boom",
                "https://example.invalid/unregistered-locator",
            ],
            configuration={"test": True},
        )

        # -- DR-0070 / OPS-006: coverage is recorded whatever happened -------

        totals = conn.execute(
            "SELECT items_discovered, items_acquired, items_skipped, "
            "items_failed, bytes_preserved, ended_at IS NOT NULL "
            "FROM collector_run WHERE id = %s", (run_id,)
        ).fetchone()
        discovered, acquired, skipped, failed, preserved, ended = totals

        check("DR-0070", "the run records what it discovered", discovered == 5)
        check("DR-0070", "the run records what it acquired", acquired == 1)
        check("DR-0070", "the run records what it skipped", skipped == 1)
        check("DR-0070", "the run records what it failed on", failed == 3)
        check("DR-0070", "the run records bytes preserved", preserved > 0)
        check("DR-0070", "the run is closed with an end time", ended)

        # -- §28 / PRES-007: every attempt is recorded, not just successes ---

        attempts = conn.execute(
            "SELECT outcome, count(*) FROM acquisition_attempt "
            "WHERE collector_run_id = %s GROUP BY outcome", (run_id,)
        ).fetchall()
        by_outcome = dict(attempts)

        check("PRES-007", "every acquisition attempt is recorded",
              sum(by_outcome.values()) == 5)
        check("PRES-007", "failures are recorded with their outcome",
              by_outcome.get("not-found", 0) >= 1 and by_outcome.get("failure", 0) >= 1)

        explained = conn.execute(
            "SELECT count(*) FROM acquisition_attempt "
            "WHERE collector_run_id = %s AND outcome <> 'success' "
            "AND error_detail IS NULL", (run_id,)
        ).fetchone()[0]
        check("PRES-007", "no failed attempt is left unexplained", explained == 0)

        # -- DR-0069 / SEC-002: quarantine and the security gate ------------

        rejected = conn.execute(
            "SELECT security_check_outcome, gate1_decision FROM quarantine_item "
            "WHERE security_check_outcome = 'malicious'"
        ).fetchone()
        check("SEC-002", "material failing the security check is refused at Gate 1",
              rejected == ("malicious", "rejected"))

        check("DR-0069", "every quarantined item was security-checked",
              conn.execute(
                  "SELECT count(*) FROM quarantine_item "
                  "WHERE security_check_outcome IS NULL").fetchone()[0] == 0)

        check("DR-0069", "the security check is recorded as a preservation event",
              conn.execute(
                  "SELECT count(*) FROM preservation_event "
                  "WHERE event_type = 'virus-check'").fetchone()[0] >= 2)

        # -- DR-0066: Gate 1 admission produces a holding --------------------

        holding = conn.execute(
            "SELECT id, completeness, retention_tier, access_tier, "
            "rights_permission, ocfl_object_id FROM holding"
        ).fetchone()
        check("DR-0066", "Gate 1 admission creates exactly one holding",
              holding is not None)
        check("DR-0061", "the holding records what the archive possesses",
              holding[1] == "original")
        check("DR-0067", "the holding inherits the source's access and rights defaults",
              holding[3] == "public" and holding[4] == "may-preserve")

        # -- DR-0073/0075: the bytes are in OCFL with both digests -----------

        obj = conn.execute(
            "SELECT ocfl_root, ocfl_object_id, ocfl_version, "
            "length(sha512), length(sha256) FROM preserved_object"
        ).fetchone()
        check("DR-0076", "content lands in the tier's storage root",
              obj[0] == "permanent")
        check("DR-0074", "the admitted original is v1 of its object", obj[2] == "v1")
        check("DR-0075", "both digests are recorded", obj[3] == 64 and obj[4] == 32)

        check("DR-0073", "the OCFL object exists and verifies",
              roots["permanent"].fixity_check(obj[1]) == [])

        stored = (roots["permanent"].object_path(obj[1])
                  / "v1" / "content" / "original.bin").read_bytes()
        check("PRES-001", "the preserved bytes are what was fetched",
              stored == instrument.read_bytes())

        # -- DR-0066: preservation events record the ingestion --------------

        check("DR-0060", "ingestion is recorded as a preservation event",
              conn.execute(
                  "SELECT count(*) FROM preservation_event "
                  "WHERE event_type = 'ingestion' AND outcome = 'success'"
              ).fetchone()[0] == 1)

        # -- Principle 11 / DR-0066: nothing crosses Gate 2 automatically ----

        check("DR-0066", "collection creates no canonical knowledge by itself",
              conn.execute("SELECT count(*) FROM documentary_assertion").fetchone()[0] == 0)
        check("EVID-003", "an acquired holding bears no evidence relation yet",
              conn.execute("SELECT count(*) FROM evidence_relation").fetchone()[0] == 0)

        # -- DR-0071(a): registered sources only ----------------------------

        rejects("DR-0071", "collecting from an unregistered source is refused",
                lambda: collector.run(str(uuid.uuid4()), ["https://example.invalid/x"],
                                      configuration={}))

        # -- DR-0067: a paused source does not collect ----------------------

        paused_id = seed_source(conn, lifecycle_state="paused", name="Paused source")
        rejects("DR-0067", "a paused source does not collect",
                lambda: collector.run(paused_id, ["https://example.invalid/reg-269"],
                                      configuration={}))

        # -- DR-0068: metadata-only tiers record but do not store ------------

        meta_id = seed_source(conn, default_retention_tier="metadata-only",
                              name="Metadata-only source")
        before = roots["permanent"].object_ids()
        meta_run = collector.run(meta_id, ["https://example.invalid/reg-269"],
                                 configuration={})
        after = roots["permanent"].object_ids()
        check("DR-0068", "a metadata-only source stores no bytes",
              before == after)
        check("DR-0068", "a metadata-only acquisition is still recorded",
              conn.execute(
                  "SELECT items_discovered FROM collector_run WHERE id = %s",
                  (meta_run,)).fetchone()[0] == 1)

        # -- Two-system integrity: orphan detection --------------------------

        check("SPEC-0003", "no orphaned OCFL objects after a clean run",
              find_orphaned_objects(conn, roots) == [])

        roots["medium-term"].create_object(
            "holding-orphan", [__import__("ocfl").ContentFile(instrument, "x.html")],
            message="simulating a failed database transaction", user="test")
        check("SPEC-0003", "an object written before a failed transaction is detectable",
              find_orphaned_objects(conn, roots) == ["holding-orphan"])

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
        print(f"{len(PASSES)} passed before the error")
        return 1


if __name__ == "__main__":
    sys.exit(main())
