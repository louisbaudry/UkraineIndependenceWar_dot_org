#!/usr/bin/env python3
"""Tests for closing an interrupted run (issue #174, §57, PRES-007).

An operator's Ctrl-C or a SIGTERM is not an `Exception`, so `Collector.run()`
used to leave the run open: no `ended_at`, totals at zero, although attempts
had been recorded against it. A run that stops partway must say so in its own
record, the interruption must still reach the operator, and the next run must
be unaffected.

Real PostgreSQL, real OCFL storage, real pipeline; only the network is a fixture.

Run:  PGHOST=... PGPORT=... PGUSER=... python3 collector/tests/test_interrupted_run.py
"""

from __future__ import annotations

import shutil
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
from fetch import FetchResult, FixtureFetcher  # noqa: E402
from ocfl import StorageRoot  # noqa: E402
from pipeline import Collector, ensure_software_agent  # noqa: E402

shared.DB = "uiw_interrupted_run_test"
check, rejects, PASSES, FAILURES = shared.check, shared.rejects, shared.PASSES, shared.FAILURES

NOW = lambda: datetime.now(timezone.utc)  # noqa: E731


def ok(locator: str, body: bytes) -> FetchResult:
    return FetchResult(locator=locator, attempted_at=NOW(), outcome="success", content=body,
                       media_type="text/html", http_status=200, http_reason="OK")


class InterruptingFetcher(FixtureFetcher):
    """Serves fixtures, then raises `interrupt` when asked for `at`."""

    def __init__(self, fixtures, at, interrupt):
        super().__init__(fixtures)
        self.at, self.interrupt = at, interrupt

    def fetch(self, locator, validators=None):
        if locator == self.at:
            raise self.interrupt
        return super().fetch(locator, validators)


def run() -> int:
    shared.build_database()
    work = Path(tempfile.mkdtemp(prefix="uiw-interrupted-"))
    roots = {"permanent": StorageRoot(work / "p", "permanent"),
             "medium-term": StorageRoot(work / "m", "medium-term")}
    for r in roots.values():
        r.initialize()
    conn = psycopg.connect(dbname=shared.DB, autocommit=True)
    try:
        person = str(uuid.uuid4())
        conn.execute("INSERT INTO pipeline_agent (id, kind, name) VALUES (%s, 'person', 'op')", (person,))
        software = ensure_software_agent(conn, "test-collector", "0.1.0")
        src = shared.seed_source(conn, locator="https://example.invalid/i/")
        locs = [f"https://example.invalid/i/{n}" for n in ("a", "b", "c", "d")]
        fixtures = {l: ok(l, f"<html>{l}</html>".encode()) for l in locs}

        def newest_run():
            return conn.execute(
                "SELECT ended_at, items_discovered, items_acquired, items_skipped, "
                "items_failed, skip_reasons, outage_note, id FROM collector_run "
                "ORDER BY started_at DESC LIMIT 1").fetchone()

        # -- Ctrl-C partway through ---------------------------------------
        fetcher = InterruptingFetcher(fixtures, locs[2], KeyboardInterrupt())
        c = Collector(conn, fetcher, work / "q1", roots, person, software)
        try:
            c.run(src, locs, configuration={})
            raised = False
        except KeyboardInterrupt:
            raised = True
        ended, disc, acq, skipped, failed, reasons, note, run_id = newest_run()
        attempts = conn.execute(
            "SELECT count(*) FROM acquisition_attempt WHERE collector_run_id = %s",
            (run_id,)).fetchone()[0]
        check("PRES-007", "the interruption still reaches the operator", raised)
        check("DR-0070", "the run is closed: it has an end time", ended is not None)
        check("DR-0070", "its counts reflect the three locators reached, the two finished "
              "ones acquired and the one in flight skipped",
              (disc, acq, skipped, failed) == (3, 2, 1, 0))
        check("DR-0070", "discovered equals acquired + skipped + failed",
              disc == acq + skipped + failed)
        check("PRES-007", "the in-flight item is recorded as skipped for the reason 'interrupted'",
              reasons == {"interrupted": 1})
        check("PRES-007", "the outage note says it was interrupted, how far it got, and how "
              "many locators were not attempted",
              note and "Interrupted (KeyboardInterrupt)" in note
              and "2 of 4 locators had finished" in note and "1 were not attempted" in note)
        check("DR-0070", "the attempts recorded before the interruption are still there",
              attempts == 2)

        # -- SIGTERM arrives as SystemExit-like interruption ----------------
        fetcher = InterruptingFetcher(fixtures, locs[0], SystemExit(143))
        c = Collector(conn, fetcher, work / "q2", roots, person, software)
        try:
            c.run(src, locs, configuration={})
            raised = False
        except SystemExit:
            raised = True
        ended, disc, acq, skipped, failed, reasons, note, _ = newest_run()
        check("PRES-007", "a SystemExit (as from SIGTERM) also closes the run and still propagates",
              raised and ended is not None and note and "SystemExit" in note
              and (disc, acq, skipped, failed) == (1, 0, 1, 0))

        # -- a normal run afterwards is unaffected and has no outage note ----
        c = Collector(conn, FixtureFetcher(fixtures), work / "q3", roots, person, software)
        c.run(src, locs, configuration={})
        ended, disc, acq, skipped, failed, reasons, note, _ = newest_run()
        check("DR-0070", "a complete run after an interruption closes normally with no outage note",
              ended is not None and note is None and disc == 4 and failed == 0)

        # -- a closing failure must never mask the interruption --------------
        class BrokenClose(Collector):
            def _close_run(self, *a, **k):
                raise RuntimeError("database went away")

        fetcher = InterruptingFetcher(fixtures, locs[1], KeyboardInterrupt())
        c = BrokenClose(conn, fetcher, work / "q4", roots, person, software)
        try:
            c.run(src, locs, configuration={})
            raised = None
        except KeyboardInterrupt:
            raised = "interrupt"
        except RuntimeError:
            raised = "runtime"
        check("PRES-007", "if closing the run itself fails, the interruption still reaches the "
              "operator rather than the closing error", raised == "interrupt")
    finally:
        conn.close()
        shutil.rmtree(work, ignore_errors=True)

    for line in PASSES + FAILURES:
        print(line)
    print(f"\n{len(PASSES)} passed, {len(FAILURES)} failed")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(run())
