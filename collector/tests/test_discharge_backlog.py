#!/usr/bin/env python3
"""Tests for collector/discharge_backlog.py (issue #152, DR-0069).

The 2026-09-09..2026-09-29 captures kept their quarantine copies because issue
#51's discharge did not exist yet. The one-off that removes them must verify
each against the real OCFL object first, remove nothing if anything fails to
verify, never touch rejected or unstored material, and record each removal as
the pipeline records one.

Method: collect for real (real PostgreSQL, real OCFL, fixture network) with the
discharge switched off, which is the pre-fix state, then run the tool.

Run:  PGHOST=... PGPORT=... PGUSER=... python3 collector/tests/test_discharge_backlog.py
"""

from __future__ import annotations

import contextlib
import io
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
import discharge_backlog as db  # noqa: E402
from fetch import FetchResult, FixtureFetcher  # noqa: E402
from ocfl import StorageRoot  # noqa: E402
from pipeline import Collector, ensure_software_agent  # noqa: E402

shared.DB = "uiw_discharge_backlog_test"
check, PASSES, FAILURES = shared.check, shared.PASSES, shared.FAILURES

NOW = lambda: datetime.now(timezone.utc)  # noqa: E731


class PreFix(Collector):
    """The collector as it was before issue #51: admits, never discharges."""

    def _discharge_quarantine(self, *a, **k):
        return None


def ok(locator: str, body: bytes) -> FetchResult:
    return FetchResult(locator=locator, attempted_at=NOW(), outcome="success", content=body,
                       media_type="text/html", http_status=200, http_reason="OK")


def cli(archive: Path, *extra: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = db.main(["--dbname", shared.DB, "--archive-root", str(archive), *extra])
    return code, out.getvalue(), err.getvalue()


def run() -> int:
    shared.build_database()
    work = Path(tempfile.mkdtemp(prefix="uiw-backlog-"))
    archive = work / "archive"
    roots = {"permanent": StorageRoot(archive / "permanent", "permanent"),
             "medium-term": StorageRoot(archive / "medium-term", "medium-term")}
    for r in roots.values():
        r.initialize()
    quarantine = archive / "quarantine"
    conn = psycopg.connect(dbname=shared.DB, autocommit=True)
    try:
        person = str(uuid.uuid4())
        conn.execute("INSERT INTO pipeline_agent (id, kind, name) VALUES (%s, 'person', 'op')", (person,))
        ensure_software_agent(conn, "test-collector", "0.1.0")
        src = shared.seed_source(conn, locator="https://example.invalid/p/")
        src_meta = shared.seed_source(conn, name="Meta", locator="https://example.invalid/m/",
                                      default_retention_tier="metadata-only")
        fetcher = FixtureFetcher({})

        def collect(cls, source, name, body, scanner=None):
            loc = f"https://example.invalid/p/{name}"
            fetcher.fixtures[loc] = ok(loc, body)
            kw = {"scanner": scanner} if scanner else {}
            cls(conn, fetcher, quarantine, roots, person,
                ensure_software_agent(conn, "test-collector", "0.1.0"), **kw
                ).run(source, [loc], configuration={})
            return str(conn.execute(
                "SELECT q.id FROM quarantine_item q JOIN acquisition_attempt a "
                "ON a.id = q.acquisition_attempt_id WHERE a.locator = %s", (loc,)).fetchone()[0])

        def deletions(qid):
            return conn.execute(
                "SELECT outcome, agent_id FROM preservation_event "
                "WHERE event_type = 'deletion' AND quarantine_item_id = %s", (qid,)).fetchall()

        def events():
            return conn.execute("SELECT count(*) FROM preservation_event").fetchone()[0]

        old1 = collect(PreFix, src, "old1", b"<html>one</html>")
        old2 = collect(PreFix, src, "old2", b"<html>two</html>")
        rejected = collect(PreFix, src, "bad", b"<html>bad</html>", scanner=lambda b: "malicious")
        unstored = collect(PreFix, src_meta, "meta", b"<html>meta</html>")
        new = collect(Collector, src, "new", b"<html>new, discharged at admission</html>")
        check("DR-0069", "setup: the pre-fix collector left both admitted copies in place",
              (quarantine / old1).exists() and (quarantine / old2).exists())

        # -- plan only ------------------------------------------------------
        before = events()
        code, out, err = cli(archive)
        check("DR-0069", "plan: two copies verified, the unstored one left, exit 0",
              code == 0 and out.startswith("2 quarantine copies verified")
              and "1 left (admitted, never stored)" in out and "0 problem(s)" in out)
        check("PRES-007", "plan only writes nothing: files stay, no events",
              (quarantine / old1).exists() and (quarantine / old2).exists() and events() == before)

        # -- a failed check stops everything --------------------------------
        original = (quarantine / old2).read_bytes()
        (quarantine / old2).write_bytes(b"altered after admission")
        code, out, err = cli(archive, "--commit")
        check("PRES-007", "a quarantine file that disagrees stops the run: exit 2, names the item",
              code == 2 and old2 in err and "digests disagree" in err)
        check("PRES-007", "and nothing is removed, not even the item that verified",
              (quarantine / old1).exists() and (quarantine / old2).exists() and events() == before)
        (quarantine / old2).write_bytes(original)

        # OCFL content corrupted: the archive copy itself is no longer trustworthy
        obj = conn.execute(
            "SELECT ocfl_object_id FROM preserved_object WHERE original_name LIKE %s",
            ("%old1",)).fetchone()[0]
        content = next((roots["permanent"].object_path(obj) / "v1" / "content").iterdir())
        good = content.read_bytes()
        content.write_bytes(b"bit rot")
        code, out, err = cli(archive, "--commit")
        check("DR-0005", "an OCFL object that fails its fixity check stops the run",
              code == 2 and "fails fixity" in err and (quarantine / old1).exists())
        content.write_bytes(good)

        # admitted for preservation, but nothing ties it to an object
        conn.execute("ALTER TABLE preservation_event DISABLE TRIGGER USER")
        saved = conn.execute(
            "DELETE FROM preservation_event WHERE event_type = 'ingestion' "
            "AND outcome_detail = %s RETURNING id, object_id, agent_id, occurred_at, outcome, outcome_detail",
            (f"admitted from quarantine {old2}",)).fetchall()
        code, out, err = cli(archive, "--commit")
        check("PRES-007", "an admitted item with no ingestion event is a problem, not a skip",
              code == 2 and old2 in err and "no ingestion event" in err)
        for row in saved:
            conn.execute(
                "INSERT INTO preservation_event (id, event_type, object_id, agent_id, occurred_at, "
                "outcome, outcome_detail) VALUES (%s, 'ingestion', %s, %s, %s, %s, %s)", row)
        conn.execute("ALTER TABLE preservation_event ENABLE TRIGGER USER")

        # -- the real run ---------------------------------------------------
        code, out, err = cli(archive, "--commit")
        check("DR-0069", "commit: both verified copies are removed, exit 0",
              code == 0 and "removed 2 quarantine copies" in out
              and not (quarantine / old1).exists() and not (quarantine / old2).exists())
        d = deletions(old1)
        kind = conn.execute("SELECT kind FROM pipeline_agent WHERE id = %s", (d[0][1],)).fetchone()[0]
        check("DR-0097", "each removal is one success 'deletion' event naming a software agent, not a person",
              len(d) == 1 and d[0][0] == "success" and kind == "software" and str(d[0][1]) != person)
        check("DR-0069", "a rejected item stays in quarantine as evidence",
              (quarantine / rejected).exists() and deletions(rejected) == [])
        check("DR-0068", "an item admitted but never stored is left alone",
              (quarantine / unstored).exists() and deletions(unstored) == [])
        check("DR-0066", "the archive is untouched: the same holdings and OCFL objects",
              conn.execute("SELECT count(*) FROM holding").fetchone()[0] == 3
              and len(roots["permanent"].object_ids()) == 3)

        # -- running it again is a no-op ------------------------------------
        before = events()
        code, out, err = cli(archive, "--commit")
        check("PRES-007", "a second run finds nothing to do and writes nothing",
              code == 0 and out.startswith("0 quarantine copies verified") and events() == before
              and len(deletions(old1)) == 1)

        # -- an item whose file is already gone is counted, not an error -----
        check("DR-0069", "an item already discharged by the pipeline is not a candidate",
              deletions(new) != [] and "0 problem(s)" in out)

        # -- the wrong directory is refused ---------------------------------
        stray = work / "not-an-archive"
        stray.mkdir()
        try:
            db.open_roots(stray)
            refused = False
        except SystemExit:
            refused = True
        check("DR-0073", "a directory that is not an OCFL storage root is refused, never initialised",
              refused and not (stray / "permanent").exists())
    finally:
        conn.close()
        shutil.rmtree(work, ignore_errors=True)

    for line in PASSES + FAILURES:
        print(line)
    print(f"\n{len(PASSES)} passed, {len(FAILURES)} failed")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(run())
