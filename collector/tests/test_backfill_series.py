#!/usr/bin/env python3
"""Tests for collector/backfill_series.py (issue #75, DR-0074).

The 2026-09-09 holdings were admitted before `Collector._admit()` wrote a
`capture_series_member` row for every admission. The backfill must produce
rows indistinguishable from the ones `_admit()` writes, refuse to guess when a
holding cannot be placed, and leave the next capture of those locators joining
the existing series instead of starting a new one.

Method: collect for real (real PostgreSQL, real OCFL, fixture network), keep the
series rows `_admit()` wrote, delete them to recreate the pre-fix state, run the
backfill, and compare against the saved originals.

Run:  PGHOST=... PGPORT=... PGUSER=... python3 collector/tests/test_backfill_series.py
"""

from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "collector"))
sys.path.insert(0, str(ROOT / "storage"))
sys.path.insert(0, str(ROOT / "collector" / "tests"))

import psycopg  # noqa: E402

import test_pipeline as shared  # noqa: E402
import backfill_series as bf  # noqa: E402
from fetch import FetchResult, FixtureFetcher  # noqa: E402
from ocfl import StorageRoot  # noqa: E402
from pipeline import Collector, ensure_software_agent  # noqa: E402

shared.DB = "uiw_series_backfill_test"
check, PASSES, FAILURES = shared.check, shared.PASSES, shared.FAILURES

NOW = lambda: datetime.now(timezone.utc)  # noqa: E731


def ok(locator: str, body: bytes) -> FetchResult:
    return FetchResult(locator=locator, attempted_at=NOW(), outcome="success", content=body,
                       media_type="text/html", response_headers={"Content-Type": "text/html"},
                       http_status=200, http_reason="OK")


def cli(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = bf.main(argv)
    return code, out.getvalue(), err.getvalue()


def run() -> int:
    shared.build_database()
    work = Path(tempfile.mkdtemp(prefix="uiw-series-"))
    roots = {"permanent": StorageRoot(work / "p", "permanent"),
             "medium-term": StorageRoot(work / "m", "medium-term")}
    for r in roots.values():
        r.initialize()
    conn = psycopg.connect(dbname=shared.DB, autocommit=True)
    try:
        person = str(uuid.uuid4())
        conn.execute("INSERT INTO pipeline_agent (id, kind, name) VALUES (%s, 'person', 'op')", (person,))
        software = ensure_software_agent(conn, "test-collector", "0.1.0")
        src_a = shared.seed_source(conn, name="Source A", locator="https://example.invalid/a/")
        src_b = shared.seed_source(conn, name="Source B", locator="https://example.invalid/b/")
        la1, la2 = "https://example.invalid/a/one", "https://example.invalid/a/two"
        lb1 = "https://example.invalid/b/one"
        fetcher = FixtureFetcher({})
        collector = Collector(conn, fetcher, work / "quarantine", roots, person, software)

        def collect(src, loc, body):
            fetcher.fixtures[loc] = ok(loc, body)
            return collector.run(src, [loc], configuration={})

        collect(src_a, la1, b"<html>a one</html>")
        collect(src_a, la2, b"<html>a two</html>")
        collect(src_b, lb1, b"<html>b one</html>")

        def series_rows():
            return conn.execute(
                "SELECT series_id, holding_id, locator, captured_at FROM capture_series_member "
                "ORDER BY holding_id").fetchall()

        original = series_rows()
        check("DR-0074", "the pipeline wrote one series row per admission (the state to reproduce)",
              len(original) == 3)

        # -- nothing to do when no holding lacks a row -----------------------------------
        links, problems = bf.plan(conn)
        code, out, _ = cli(["--dbname", shared.DB, "--commit"])
        check("issue #75", "with no gap, the plan is empty and --commit writes nothing",
              links == [] and problems == [] and code == 0 and series_rows() == original)

        # -- recreate the pre-fix state, then plan and dry-run ---------------------------
        conn.execute("DELETE FROM capture_series_member")
        code, out, _ = cli(["--dbname", shared.DB])
        check("issue #75", "a plain run only plans: 3 holdings named, nothing written",
              code == 0 and "3 holding(s) would be linked" in out and "plan only" in out
              and series_rows() == [])

        code, out, _ = cli(["--dbname", shared.DB, "--commit"])
        check("issue #75", "--commit writes rows identical to the ones _admit() wrote "
              "(series id, holding, locator and captured_at)",
              code == 0 and series_rows() == original)

        code, out, _ = cli(["--dbname", shared.DB, "--commit"])
        check("issue #75", "running it again changes nothing", code == 0 and series_rows() == original
              and "0 holding(s)" in out)

        # -- the point of the card: the next capture joins the existing series -----------
        conn.execute("DELETE FROM capture_series_member WHERE locator = %s", (la1,))
        before = conn.execute("SELECT count(*) FROM holding").fetchone()[0]
        collect(src_a, la1, b"<html>a one</html>")
        gap = conn.execute("SELECT count(*) FROM holding").fetchone()[0]
        check("issue #75", "WITHOUT the backfill the same bytes are stored again (the gap this "
              "card closes)", gap == before + 1)
        # undo that duplicate so the next check starts from the repaired state
        conn.execute("DELETE FROM capture_series_member WHERE locator = %s", (la1,))
        code, _, _ = cli(["--dbname", shared.DB, "--commit"])
        before = conn.execute("SELECT count(*) FROM holding").fetchone()[0]
        collect(src_a, la1, b"<html>a one</html>")
        after = conn.execute("SELECT count(*) FROM holding").fetchone()[0]
        last = conn.execute(
            "SELECT outcome FROM acquisition_attempt WHERE locator = %s "
            "ORDER BY attempted_at DESC LIMIT 1", (la1,)).fetchone()[0]
        check("issue #75", "AFTER the backfill the same bytes are confirmed unchanged, not "
              "stored again", after == before and last == "unchanged")

        # -- a recovered capture is ordered by when the archive captured it ---------------
        conn.execute("DELETE FROM capture_series_member WHERE locator = %s", (la2,))
        conn.execute(
            "UPDATE acquisition_attempt SET acquisition_route = 'external-archive', "
            "acquisition_source = 'Test Archive', external_record_locator = 'x', "
            "original_captured_at = '2020-01-02T03:04:05Z' "
            "WHERE locator = %s AND outcome = 'success'", (la2,))
        links, problems = bf.plan(conn)
        check("DR-0074", "a recovered capture takes the archive's capture time, as _admit() does",
              len(links) == 1 and links[0].locator == la2
              and links[0].captured_at == datetime(2020, 1, 2, 3, 4, 5, tzinfo=timezone.utc))
        cli(["--dbname", shared.DB, "--commit"])

        # -- refusals: never guess ------------------------------------------------------
        conn.execute("DELETE FROM capture_series_member WHERE locator IN (%s, %s)", (la1, lb1))
        # Re-point the attempt rather than delete it: quarantine items reference it.
        conn.execute("UPDATE acquisition_attempt SET locator = %s WHERE locator = %s",
                     ("https://example.invalid/b/elsewhere", lb1))
        code, out, err = cli(["--dbname", shared.DB, "--commit"])
        rows_now = conn.execute("SELECT count(*) FROM capture_series_member").fetchone()[0]
        check("issue #75", "a holding with no successful attempt is reported, and NOTHING is written "
              "even for holdings that could be placed",
              code == 2 and "CANNOT PLACE" in err and "no successful acquisition_attempt" in err
              and rows_now == conn.execute("SELECT count(*) FROM capture_series_member").fetchone()[0]
              and conn.execute("SELECT count(*) FROM capture_series_member WHERE locator = %s",
                               (la1,)).fetchone()[0] == 0)

        conn.execute(
            "INSERT INTO acquisition_attempt (id, source_id, locator, attempted_at, outcome) "
            "VALUES (%s, %s, %s, now(), 'success')", (str(uuid.uuid4()), src_b, la1))
        links, problems = bf.plan(conn)
        check("issue #75", "a locator acquired under two different sources cannot be placed",
              any("different sources" in p and la1 in p for p in problems))
        code, _, err = cli(["--dbname", shared.DB, "--commit"])
        check("issue #75", "and the run refuses with exit 2", code == 2 and "refused" in err)

        check("DR-0066", "the backfill created no holding, object or assertion",
              conn.execute("SELECT count(*) FROM documentary_assertion").fetchone()[0] == 0)
    finally:
        conn.close()

    for line in PASSES:
        print(line)
    for line in FAILURES:
        print(line)
    print(f"\n{len(PASSES)} passed, {len(FAILURES)} failed")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(run())
