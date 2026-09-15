#!/usr/bin/env python3
"""Tests for storage/measure.py (WP 3.4 §4.1, Track A item A7).

Runs against a real PostgreSQL database (dropped and rebuilt from schema/)
and a real filesystem tree standing in for an archive root, so the
on-disk-walk code is exercised against actual files, not a mock.

Run:  PGHOST=... PGPORT=... PGUSER=... python3 storage/tests/test_measure.py
"""

from __future__ import annotations

import os
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

from measure import (  # noqa: E402
    build_report, disk_footprint, measure_quarantine, measure_runs,
    summarize_by_source,
)

PASSES: list[str] = []
FAILURES: list[str] = []
DB = "uiw_measure_test"


def check(req: str, what: str, condition: bool) -> None:
    (PASSES if condition else FAILURES).append(
        f"{'PASS' if condition else 'FAIL'}  {req} — {what}"
    )


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


def seed_source(conn, name: str) -> str:
    source_id = str(uuid.uuid4())
    conn.execute(
        """
        INSERT INTO source (id, source_type, name, locator, collection_method,
            default_retention_tier, default_access_tier, rights_permission,
            lifecycle_state, expects_graphic_content, capture_format)
        VALUES (%s, 'government', %s, 'https://example.invalid', 'http',
                'permanent', 'public', 'may-preserve', 'active', false, 'http')
        """,
        (source_id, name),
    )
    return source_id


def seed_run(
    conn, source_id: str, agent_id: str, started_at: datetime,
    duration_seconds: float | None, bytes_preserved: int, items_acquired: int,
) -> str:
    run_id = str(uuid.uuid4())
    ended_at = (
        started_at + timedelta(seconds=duration_seconds)
        if duration_seconds is not None else None
    )
    conn.execute(
        """
        INSERT INTO collector_run
            (id, source_id, collector_agent_id, configuration, started_at,
             ended_at, items_acquired, bytes_preserved)
        VALUES (%s, %s, %s, '{}', %s, %s, %s, %s)
        """,
        (run_id, source_id, agent_id, started_at, ended_at, items_acquired,
         bytes_preserved),
    )
    return run_id


def run() -> int:
    build_database()
    conn = psycopg.connect(dbname=DB, autocommit=True)

    agent_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO pipeline_agent (id, kind, name) VALUES (%s, 'person', 'test operator')",
        (agent_id,),
    )

    eu = seed_source(conn, "EU consolidated list (test)")
    ofac = seed_source(conn, "OFAC SDN (test)")
    now = datetime(2026, 9, 9, tzinfo=timezone.utc)

    # DR-0070: a run with an outage note and no end is coverage, not a zero.
    seed_run(conn, eu, agent_id, now, None, 0, 0)
    seed_run(conn, eu, agent_id, now, 100.0, 50_000_000, 2)
    seed_run(conn, ofac, agent_id, now, 200.0, 161_331_430, 3)

    # -- collector_run measurement ------------------------------------------

    runs = measure_runs(conn)
    check("WP-3.4-A7", "unterminated run (no ended_at) is excluded from throughput",
          len(runs) == 2)
    check("WP-3.4-A7", "a timed run reports bytes/second",
          any(r.bytes_per_second == 500_000.0 for r in runs))

    scoped = measure_runs(conn, source_id=ofac)
    check("WP-3.4-A7", "--source-id scopes measurement to one source",
          len(scoped) == 1 and scoped[0].source_id == ofac)

    by_source = summarize_by_source(runs)
    check("WP-3.4-A7", "per-source summary folds every run for that source",
          len(by_source) == 2)
    eu_summary = next(s for s in by_source if s.source_id == eu)
    check("WP-3.4-A7", "per-source bytes_preserved sums across runs",
          eu_summary.bytes_preserved == 50_000_000)
    check("WP-3.4-A7", "per-source average throughput is bytes / summed duration",
          eu_summary.average_bytes_per_second == 500_000.0)

    # -- on-disk walk --------------------------------------------------------

    tmp = Path(tempfile.mkdtemp())
    try:
        archive_root = tmp / "archive"
        permanent = archive_root / "permanent"
        permanent.mkdir(parents=True)
        (permanent / "object-a").mkdir()
        (permanent / "object-a" / "inventory.json").write_bytes(b"x" * 1000)
        (permanent / "object-a" / "content.bin").write_bytes(b"y" * 9000)

        quarantine = archive_root / "quarantine"
        quarantine.mkdir()
        (quarantine / str(uuid.uuid4())).write_bytes(b"z" * 10_000)

        footprint = disk_footprint(permanent)
        check("WP-3.4-A7", "disk_footprint counts real bytes on disk, not a DB total",
              footprint.on_disk_bytes == 10_000 and footprint.file_count == 2)

        q_footprint = measure_quarantine(archive_root)
        check("WP-3.4-A7",
              "quarantine footprint is measured separately from OCFL roots "
              "(collector/README's undischarged-copy gap)",
              q_footprint.on_disk_bytes == 10_000)

        # A run whose preserved bytes exactly match one OCFL object plus one
        # quarantine copy of the same size should report ~2x duplication.
        dup_source = seed_source(conn, "duplication-ratio source")
        seed_run(conn, dup_source, agent_id, now, 1.0, 10_000, 1)
        report = build_report(conn, archive_root, source_id=dup_source)
        check("WP-3.4-A7",
              "duplication ratio reflects on-disk bytes divided by preserved bytes",
              report.duplication_ratio is not None
              and abs(report.duplication_ratio - 2.0) < 0.01)

        # Extrapolation is clearly a separate, labelled field, not folded
        # into the measured total.
        report_x = build_report(conn, archive_root, extrapolate_sources=7)
        check("WP-3.4-A7",
              "extrapolation is a distinct labelled projection, not the measurement",
              report_x.extrapolated_sources == 7
              and report_x.total_bytes_preserved
                  == sum(r.bytes_preserved for r in measure_runs(conn)))

        # -- empty archive root: no crash, zero footprint -------------------
        empty_root = tmp / "does-not-exist"
        empty_footprint = disk_footprint(empty_root)
        check("WP-3.4-A7", "a missing archive root measures as zero, not a crash",
              empty_footprint.on_disk_bytes == 0 and empty_footprint.file_count == 0)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    conn.close()

    for line in PASSES + FAILURES:
        print(line)
    print(f"\n{len(PASSES)} passed, {len(FAILURES)} failed")
    return 1 if FAILURES else 0


def main() -> int:
    try:
        return run()
    except Exception as exc:  # noqa: BLE001 — a crash is a suite failure
        print(f"FAIL  suite crashed: {exc!r}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
