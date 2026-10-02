#!/usr/bin/env python3
"""Tests for discharging quarantine copies after admission (issue #51).

DR-0069 makes quarantine a zone outside the archive. Before this change an
admitted capture's quarantine file stayed behind, so the archive directory
held every capture twice. The pipeline now removes the quarantine copy of an
*admitted and preserved* item, and records the removal as a `deletion`
preservation event on the quarantine item. Rules pinned here:

- the file goes only when the file on disk, the receipt record and the OCFL
  inventory agree on the sha256;
- a failed or refused discharge is a recorded failure and the file is kept;
  the admission and the run stand either way (§28, PRES-007);
- material that was not admitted and preserved is not touched: a rejected
  item stays in quarantine as evidence of what was refused.

Real PostgreSQL, real OCFL storage, real pipeline; the network is a fixture.

Run:  PGHOST=... PGPORT=... PGUSER=... python3 collector/tests/test_quarantine_discharge.py
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

shared.DB = "uiw_discharge_test"
check, rejects, PASSES, FAILURES = shared.check, shared.rejects, shared.PASSES, shared.FAILURES

NOW = lambda: datetime.now(timezone.utc)  # noqa: E731


def ok(locator: str, body: bytes) -> FetchResult:
    return FetchResult(locator=locator, attempted_at=NOW(), outcome="success", content=body,
                       media_type="text/html", http_status=200, http_reason="OK")


class _TamperAfterPreserve(Collector):
    """Alters the quarantine file after the archive has it: the file no longer
    matches what was admitted."""

    def _preserve(self, source, quarantine_id, *a, **k):
        digest = super()._preserve(source, quarantine_id, *a, **k)
        (self.quarantine_dir / quarantine_id).write_bytes(b"changed on disk")
        return digest


class _ArchiveDisagrees(Collector):
    """The OCFL inventory reports a different sha256 than the file received."""

    def _preserve(self, source, quarantine_id, *a, **k):
        super()._preserve(source, quarantine_id, *a, **k)
        return "0" * 64


class _LoseFileAfterPreserve(Collector):
    """The quarantine file vanishes before discharge: an OSError at read."""

    def _preserve(self, source, quarantine_id, *a, **k):
        digest = super()._preserve(source, quarantine_id, *a, **k)
        (self.quarantine_dir / quarantine_id).unlink()
        return digest


def run() -> int:
    shared.build_database()
    work = Path(tempfile.mkdtemp(prefix="uiw-discharge-"))
    roots = {"permanent": StorageRoot(work / "ocfl-permanent", "permanent"),
             "medium-term": StorageRoot(work / "ocfl-medium", "medium-term")}
    for r in roots.values():
        r.initialize()

    conn = psycopg.connect(dbname=shared.DB, autocommit=True)
    try:
        person = str(uuid.uuid4())
        conn.execute("INSERT INTO pipeline_agent (id, kind, name) VALUES (%s, 'person', 'op')", (person,))
        software = ensure_software_agent(conn, "test-collector", "0.1.0")
        source_id = shared.seed_source(conn, locator="https://example.invalid/d/")

        def collect(cls, body, name, scanner=None):
            qdir = work / f"q-{name}"
            fx = FixtureFetcher({f"https://example.invalid/d/{name}": ok(f"https://example.invalid/d/{name}", body)})
            c = cls(conn, fx, qdir, roots, person, software, scanner=scanner) if scanner else \
                cls(conn, fx, qdir, roots, person, software)
            c.run(source_id, [f"https://example.invalid/d/{name}"], configuration={})
            qid = conn.execute(
                "SELECT q.id FROM quarantine_item q JOIN acquisition_attempt a "
                "ON a.id = q.acquisition_attempt_id WHERE a.locator = %s",
                (f"https://example.invalid/d/{name}",)).fetchone()[0]
            return qdir / str(qid), str(qid)

        def deletions(qid):
            return conn.execute(
                "SELECT outcome, outcome_detail, agent_id FROM preservation_event "
                "WHERE event_type = 'deletion' AND quarantine_item_id = %s", (qid,)).fetchall()

        # -- the normal path ------------------------------------------------
        path, qid = collect(Collector, b"<html>admitted</html>", "ok")
        d = deletions(qid)
        check("DR-0069", "an admitted capture's quarantine file is removed", not path.exists())
        check("PRES-007", "the removal is one 'deletion' event on the quarantine item, success, naming the digest",
              len(d) == 1 and d[0][0] == "success" and "sha256" in d[0][1])
        check("DR-0097", "the deletion event names the software agent, not the person of record",
              d and str(d[0][2]) == str(software))
        held = conn.execute("SELECT count(*) FROM holding").fetchone()[0]
        check("DR-0066", "the admission stands: a holding and an OCFL object exist",
              held == 1 and len(roots["permanent"].object_ids()) == 1)
        check("DR-0061", "the archive still carries the quarantine item's row as history",
              conn.execute("SELECT gate1_decision FROM quarantine_item WHERE id = %s", (qid,)).fetchone()[0]
              == "admitted")

        # -- a file that no longer matches is kept --------------------------
        path, qid = collect(_TamperAfterPreserve, b"<html>tampered</html>", "tamper")
        d = deletions(qid)
        check("PRES-007", "a quarantine file whose digest disagrees is kept",
              path.exists() and path.read_bytes() == b"changed on disk")
        check("PRES-007", "the refusal is a recorded 'deletion' failure that says the digests disagree",
              len(d) == 1 and d[0][0] == "failure" and "disagree" in d[0][1])
        check("DR-0066", "a refused discharge does not undo the admission",
              conn.execute("SELECT count(*) FROM holding").fetchone()[0] == 2)

        # -- the archive's own digest disagrees -----------------------------
        path, qid = collect(_ArchiveDisagrees, b"<html>mismatch</html>", "arch")
        d = deletions(qid)
        check("DR-0075", "a quarantine file is kept when the OCFL digest disagrees with it",
              path.exists() and len(d) == 1 and d[0][0] == "failure" and "disagree" in d[0][1])

        # -- a file that cannot be read or removed is a recorded failure -----
        path, qid = collect(_LoseFileAfterPreserve, b"<html>vanished</html>", "lost")
        d = deletions(qid)
        check("PRES-007", "an OSError at discharge is a recorded failure, not an exception out of the run",
              len(d) == 1 and d[0][0] == "failure" and "not removed" in d[0][1])
        check("DR-0066", "the run still preserved the capture",
              conn.execute("SELECT count(*) FROM holding").fetchone()[0] == 4)

        # -- not admitted: not touched -------------------------------------
        path, qid = collect(Collector, b"<html>bad</html>", "mal", scanner=lambda b: "malicious")
        check("DR-0069", "a rejected item stays in quarantine", path.exists())
        check("DR-0069", "and no deletion is recorded for it", deletions(qid) == [])
        check("DR-0066", "and nothing was preserved for it",
              conn.execute("SELECT count(*) FROM holding").fetchone()[0] == 4)

        # -- the database accepts the event type and still demands a reason --
        rejects("PRES-007", "a failed 'deletion' event with no detail is refused by the DDL",
                lambda: conn.execute(
                    "INSERT INTO preservation_event (id, event_type, quarantine_item_id, agent_id, "
                    "occurred_at, outcome) VALUES (%s, 'deletion', %s, %s, now(), 'failure')",
                    (str(uuid.uuid4()), qid, str(software))))
    finally:
        conn.close()
        shutil.rmtree(work, ignore_errors=True)

    for line in PASSES + FAILURES:
        print(line)
    print(f"\n{len(PASSES)} passed, {len(FAILURES)} failed")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    try:
        sys.exit(run())
    except Exception as exc:  # noqa: BLE001
        import traceback

        traceback.print_exc()
        print(f"\nSUITE ERRORED — {type(exc).__name__}: {exc}")
        sys.exit(1)
