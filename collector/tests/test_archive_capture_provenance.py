#!/usr/bin/env python3
"""Tests for recording a retrieved third-party capture (issue #52, DR-0094).

DR-0094 §3 and §5 require two things of an acquisition from an external web
archive that `acquisition_attempt` did not yet carry:

- **where in the archive the record lives** (`external_record_locator`), so a
  reader can go back to the archive's own copy; WARC-Record-ID names a record
  but does not say where it is;
- **that the archive cut the payload short** (`truncation_reason`,
  `captured_payload_bytes`): Common Crawl stops near 1 MB. Such a capture is
  admitted rather than refused, and is a `fragment`, never read as the whole
  page. A digest the archive declared for the *whole* payload cannot match the
  part held, so a mismatch on a truncated record is not a corrupt capture; on
  an untruncated one it still is.

Real PostgreSQL, real OCFL storage, real pipeline; the archive is a WARC file
the test writes. Nothing here has been run against Common Crawl or the Wayback
Machine (DR-0094, *What has not been verified*).

Run:  PGHOST=... PGPORT=... PGUSER=... python3 collector/tests/test_archive_capture_provenance.py
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
from ocfl import StorageRoot  # noqa: E402
from pipeline import Collector  # noqa: E402
from warc import build_response_record, digest_header  # noqa: E402

shared.DB = "uiw_archive_provenance_test"
check, rejects, PASSES, FAILURES = shared.check, shared.rejects, shared.PASSES, shared.FAILURES

BASE = "https://example.invalid/oj/"
WHEN = datetime(2024, 3, 1, 12, 0, 0, tzinfo=timezone.utc)
FULL = b"<html>" + b"0123456789" * 60 + b"</html>"
CUT = FULL[:200]


def record(uri, body, *, truncated=None, declared_for=None, headers=()):
    """A WARC response record. `declared_for`: the bytes the archive's
    WARC-Payload-Digest was computed over, when not `body` itself (a
    truncated record declares the whole payload)."""
    raw = build_response_record(uri, 200, "OK", [("Content-Type", "text/html"), *headers],
                                body, WHEN)
    if declared_for is not None:
        raw = raw.replace(digest_header(body).encode(), digest_header(declared_for).encode(), 1)
    if truncated is not None:
        raw = raw.replace(b"Content-Length:", f"WARC-Truncated: {truncated}\r\n".encode()
                          + b"Content-Length:", 1)
    return raw


def run() -> int:
    shared.build_database()
    work = Path(tempfile.mkdtemp(prefix="uiw-archprov-"))
    roots = {"permanent": StorageRoot(work / "ocfl-permanent", "permanent"),
             "medium-term": StorageRoot(work / "ocfl-medium", "medium-term")}
    for r in roots.values():
        r.initialize()

    conn = psycopg.connect(dbname=shared.DB, autocommit=True)
    try:
        agent = str(uuid.uuid4())
        conn.execute("INSERT INTO pipeline_agent (id, kind, name, software_version) "
                     "VALUES (%s, 'software', 'test-ingester', '0.1.0')", (agent,))
        source_id = shared.seed_source(conn, locator=BASE, collection_method="warc-import")
        collector = Collector(conn, None, work / "quarantine", roots, agent, agent)

        def ingest(name, records, **kw):
            path = work / name
            path.write_bytes(b"".join(records))
            run_id = collector.ingest_warc(source_id, path, "test-archive", {}, **kw)
            return conn.execute(
                "SELECT a.locator, a.outcome, a.external_record_locator, a.truncation_reason, "
                "a.captured_payload_bytes, h.completeness "
                "FROM acquisition_attempt a "
                "LEFT JOIN quarantine_item q ON q.acquisition_attempt_id = a.id "
                "LEFT JOIN holding h ON h.ocfl_object_id IS NOT NULL AND EXISTS ("
                "  SELECT 1 FROM capture_series_member m WHERE m.holding_id = h.id "
                "  AND m.locator = a.locator AND m.captured_at = a.original_captured_at) "
                "WHERE a.collector_run_id = %s ORDER BY a.locator", (run_id,)).fetchall(), run_id

        # -- DR-0094 §3: where the record lives ---------------------------------
        rows, _ = ingest("plain.warc", [record(BASE + "a", FULL)],
                         archive_locator="crawl-data/CC-MAIN-2024-10/segments/x/warc/y.warc.gz")
        check("DR-0094", "the attempt records where in the archive the record lives",
              rows[0][2] == "crawl-data/CC-MAIN-2024-10/segments/x/warc/y.warc.gz")
        check("DR-0094", "an untruncated capture records no truncation",
              rows[0][3] is None and rows[0][4] is None)
        check("DR-0061", "an untruncated capture is held as an original",
              rows[0][5] == "original")

        rows, _ = ingest("noloc.warc", [record(BASE + "b", FULL)])
        check("DR-0094", "with no archive locator given, the local file's name is recorded, never nothing",
              rows[0][2] == "noloc.warc")

        # -- DR-0094 §5: truncated records are admitted, flagged ------------------
        rows, run_id = ingest("cut.warc", [record(BASE + "c", CUT, truncated="length",
                                                  declared_for=FULL)])
        discovered, acquired, failed = conn.execute(
            "SELECT items_discovered, items_acquired, items_failed FROM collector_run "
            "WHERE id = %s", (run_id,)).fetchone()
        check("DR-0094", "a truncated capture is admitted, not refused",
              acquired == 1 and failed == 0 and rows[0][1] == "success")
        check("DR-0094", "its truncation reason is recorded as the archive stated it",
              rows[0][3] == "length")
        check("DR-0094", "the bytes actually held are recorded",
              rows[0][4] == len(CUT))
        check("DR-0061", "its holding is a fragment, never an original (§26)",
              rows[0][5] == "fragment")
        note = conn.execute(
            "SELECT outcome_detail FROM preservation_event e JOIN quarantine_item q "
            "ON q.id = e.quarantine_item_id JOIN acquisition_attempt a "
            "ON a.id = q.acquisition_attempt_id WHERE a.collector_run_id = %s "
            "AND e.event_type = 'fixity-check'", (run_id,)).fetchone()
        check("DR-0075", "the digest that cannot match is noted as expected, not silently dropped",
              note is not None and "truncated" in note[0])

        rows, _ = ingest("odd.warc", [record(BASE + "d", CUT, truncated="disconnect",
                                             declared_for=FULL),
                                      record(BASE + "e", CUT, truncated="something-new",
                                             declared_for=FULL)])
        check("DR-0094", "disconnect is recorded as the archive stated it",
              rows[0][3] == "disconnect")
        check("DR-0094", "a reason outside the known set is 'unspecified', still flagged",
              rows[1][3] == "unspecified" and rows[1][5] == "fragment")

        # -- the exemption is narrow ----------------------------------------------
        rows, run_id = ingest("bad.warc", [record(BASE + "f", CUT, declared_for=FULL)])
        check("DR-0075", "a digest mismatch on a record NOT marked truncated still fails",
              rows[0][1] == "failure")

        # -- the database refuses what the code would, if the code were wrong ------
        def insert(**cols):
            base = {"id": str(uuid.uuid4()), "source_id": source_id, "locator": BASE + "z",
                    "attempted_at": datetime.now(timezone.utc), "outcome": "success",
                    "acquisition_route": "external-archive", "acquisition_source": "t",
                    "original_captured_at": WHEN, "external_record_locator": "f.warc"}
            base.update(cols)
            names = ", ".join(base)
            conn.execute(f"INSERT INTO acquisition_attempt ({names}) VALUES ({', '.join(['%s'] * len(base))})",
                         list(base.values()))
        rejects("DR-0094", "an external-archive attempt with no archive locator is refused",
                lambda: insert(external_record_locator=None))
        rejects("DR-0094", "a truncation reason without the bytes held is refused",
                lambda: insert(truncation_reason="length"))
        rejects("DR-0094", "bytes held without a truncation reason is refused",
                lambda: insert(captured_payload_bytes=10))
        rejects("DR-0094", "a truncation reason outside the known set is refused",
                lambda: insert(truncation_reason="whim", captured_payload_bytes=10))
        rejects("DR-0094", "only an archive capture may be marked truncated",
                lambda: insert(acquisition_route="live-fetch", truncation_reason="length",
                               captured_payload_bytes=10))
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
