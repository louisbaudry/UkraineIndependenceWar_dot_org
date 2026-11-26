#!/usr/bin/env python3
"""Tests for the file-import path (DR-0118, issue #197).

`collector/export_checks.py` (the checks on a downloaded file),
`Collector.import_file()` (admission through the existing path) and
`collector/file_import.py` (the operator's command and its refusals), end to
end against fixture files in a throwaway database. Every fixture row is
synthetic; no real register content is used.

Run:  PGHOST=… PGPORT=… PGUSER=… python3 collector/tests/test_file_import.py
"""

from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "collector"))
sys.path.insert(0, str(ROOT / "storage"))
sys.path.insert(0, str(ROOT / "sources"))

import psycopg  # noqa: E402

import file_import  # noqa: E402
from export_checks import EXPORT_HEADERS, check_export, read_hashed  # noqa: E402
from fetch import FixtureFetcher  # noqa: E402
from pipeline import Collector, PolicyViolation, ensure_software_agent  # noqa: E402
from register import commit, load_candidates, merge_class_defaults  # noqa: E402
from run import open_roots  # noqa: E402
from warc import build_resource_record, read_records, verify_payload_digest  # noqa: E402

PASSES: list[str] = []
FAILURES: list[str] = []
DB = "uiw_file_import_test"
LEGAL = "ua-nsdc-sanctions-legal-entities"
VESSELS = "ua-nsdc-sanctions-vessels"
INDIVIDUALS = "ua-nsdc-sanctions-individuals"


def check(req: str, what: str, condition: bool) -> None:
    (PASSES if condition else FAILURES).append(
        f"{'PASS' if condition else 'FAIL'}  {req} — {what}")


def build_database() -> None:
    subprocess.run(["psql", "-q", "-c", f"DROP DATABASE IF EXISTS {DB}",
                    "-c", f"CREATE DATABASE {DB}", "postgres"],
                   check=True, capture_output=True)
    for sql in sorted((ROOT / "schema").glob("0*.sql")):
        subprocess.run(["psql", "-q", "-d", DB, "-v", "ON_ERROR_STOP=1",
                        "-f", str(sql)], check=True, capture_output=True)


def csv_bytes(key: str, records: int, header: tuple[str, ...] | None = None,
              bom: bool = False) -> bytes:
    """A synthetic export: the class's header and `records` invented rows."""
    header = header or EXPORT_HEADERS[key]
    lines = [",".join(header)]
    for i in range(records):
        lines.append(",".join(f"TEST-{name}-{i}" for name in header))
    text = "\r\n".join(lines) + "\r\n"
    return (b"\xef\xbb\xbf" if bom else b"") + text.encode("utf-8")


def invoke(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = file_import.main(argv)
    return code, out.getvalue(), err.getvalue()


def unit_checks() -> None:
    header = EXPORT_HEADERS[LEGAL]
    good = csv_bytes(LEGAL, 3)
    check("DR-0118", "a well-formed export passes", check_export(good, header, 3) == (3, None))
    check("DR-0118", "a UTF-8 byte-order mark is not read as part of the header",
          check_export(csv_bytes(LEGAL, 2, bom=True), header, 2) == (2, None))
    check("DR-0118", "an empty file is refused",
          check_export(b"", header, 3)[1] == "the file is empty")
    check("DR-0118", "a header with no records is refused",
          "no records" in (check_export(csv_bytes(LEGAL, 0), header, 3)[1] or ""))
    check("DR-0118", "a header other than the class's is refused",
          "header is not the one recorded" in (
              check_export(csv_bytes(VESSELS, 2), header, 3)[1] or ""))
    reordered = (header[1], header[0], *header[2:])
    check("DR-0118", "the right fields in the wrong order are refused",
          "different order" in (
              check_export(csv_bytes(LEGAL, 2, header=reordered), header, 3)[1] or ""))
    check("DR-0118", "more records than the register stated are refused",
          check_export(good, header, 2) == (3, "the file holds 3 records, more than "
                                                "the 2 the register stated"))
    check("DR-0118", "a file that is not UTF-8 is refused",
          "not UTF-8" in (check_export(b"\xff\xfe" + good, header, 3)[1] or ""))
    quoted = (",".join(header) + "\r\n"
              + ",".join(['"line one\nline two"'] + ["x"] * (len(header) - 1))
              + "\r\n").encode()
    check("DR-0118", "a quoted field spanning lines is one record, not two",
          check_export(quoted, header, 1) == (1, None))
    check("DR-0118", "a refusal quotes no row content",
          "TEST-" not in (check_export(good, header, 1)[1] or ""))

    with tempfile.NamedTemporaryFile() as handle:
        handle.write(good)
        handle.flush()
        data, sha = read_hashed(handle.name)
    check("DR-0118", "the file is hashed as it is read: same bytes, same SHA-256",
          data == good and sha == hashlib.sha256(good).hexdigest())

    when = datetime(2026, 11, 26, 13, 5, tzinfo=timezone.utc)
    record_bytes = build_resource_record("https://example.invalid/x.csv", "text/csv",
                                         good, when)
    records = list(read_records(io.BufferedReader(io.BytesIO(record_bytes))))
    check("DR-0006", "a file import's WARC record is a resource record, "
          "claiming no HTTP response",
          len(records) == 1 and records[0].record_type == "resource"
          and not records[0].is_http_response)
    check("DR-0118", "the resource record holds the file unchanged, dated at download",
          records and records[0].payload() == good and records[0].date == when)
    check("DR-0075", "the resource record's declared payload digest verifies",
          records and verify_payload_digest(records[0])[0] == "verified")


def run() -> int:
    unit_checks()
    build_database()
    work = Path(tempfile.mkdtemp(prefix="uiw-import-"))
    archive = work / "archive"

    raw, _, classes = load_candidates()
    sources = {s["key"]: merge_class_defaults(s, classes) for s in raw}
    legal = sources[LEGAL]
    export_url = legal["run_locators"][0]
    downloaded = (datetime.now(timezone.utc) - timedelta(hours=1)).replace(microsecond=0)

    good = work / "legal.csv"
    good.write_bytes(csv_bytes(LEGAL, 4))
    bad_header = work / "vessels-as-legal.csv"
    bad_header.write_bytes(csv_bytes(VESSELS, 4))

    conn = psycopg.connect(dbname=DB, autocommit=True)
    try:
        person = str(uuid.uuid4())
        software = str(uuid.uuid4())
        conn.execute("INSERT INTO pipeline_agent (id, kind, name) "
                     "VALUES (%s, 'person', 'Test founder')", (person,))
        conn.execute("INSERT INTO pipeline_agent (id, kind, name, software_version) "
                     "VALUES (%s, 'software', 'cron', '0.1')", (software,))

        def args(source=LEGAL, path=good, when=downloaded.isoformat(), count="4",
                 agent=person, *extra):
            return ["--source", source, "--file", str(path), "--downloaded-at", when,
                    "--stated-count", count, "--dbname", DB, "--agent", agent,
                    "--archive-root", str(archive), *extra]

        def runs() -> int:
            return conn.execute("SELECT count(*) FROM collector_run").fetchone()[0]

        # -- refusals before anything is written ------------------------------

        code, _, err = invoke(args(source=INDIVIDUALS))
        check("DR-0118 Decision 4", "the individuals class is refused until "
              "DR-0072's successor", code == 2 and "DR-0118 Decision 4" in err)
        code, _, err = invoke(args(source="ofac-sdn"))
        check("DR-0118", "a source with no recorded export header is refused",
              code == 2 and "no export header" in err)
        code, _, err = invoke(args())
        check("DR-0071", "an unregistered candidate is refused",
              code == 2 and "not registered" in err)

        commit(conn, [copy.deepcopy(legal)], [], person)

        code, _, err = invoke(args(agent=software))
        check("DR-0093 §3", "a software agent cannot be the person who downloaded",
              code == 2 and "person as the agent of record" in err)
        code, _, err = invoke(args(when="2026-11-26T10:00:00"))
        check("DR-0118", "a download time without a time zone is refused",
              code == 2 and "time zone" in err)
        future = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
        code, _, err = invoke(args(when=future))
        check("DR-0118", "a download time in the future is refused",
              code == 2 and "future" in err)
        code, _, err = invoke(args() + ["--export-url", "https://drs.nsdc.gov.ua/other"])
        check("DR-0071", "an export URL that is not a verified run locator is refused",
              code == 2 and "not one of" in err)
        check("DR-0118", "no refusal wrote a run", runs() == 0)

        code, out, _ = invoke(args() + ["--dry-run"])
        check("DR-0118", "a dry run checks the file and writes nothing",
              code == 0 and "checks        pass" in out and runs() == 0
              and not archive.exists())

        # -- an authorised import ------------------------------------------

        code, out, err = invoke(args())
        check("DR-0118", "an authorised import completes", code == 0)
        attempt = conn.execute(
            "SELECT acquisition_route, acquisition_source, original_captured_at, "
            "locator, outcome, collector_run_id FROM acquisition_attempt").fetchone()
        check("DR-0118", "the attempt is a file-import naming the person and the "
              "download time, at the export URL",
              attempt is not None and attempt[:5] == (
                  "file-import", "Test founder", downloaded, export_url, "success"))
        run_row = conn.execute(
            "SELECT collector_agent_id, configuration FROM collector_run").fetchone()
        check("DR-0093 §3", "the person is the run's agent of record",
              str(run_row[0]) == person)
        check("DR-0118", "the run records the file's name, size and SHA-256",
              run_row[1].get("file_sha256") == hashlib.sha256(good.read_bytes()).hexdigest()
              and run_row[1].get("file_bytes") == good.stat().st_size
              and run_row[1].get("records") == 4)
        check("DR-0074", "the import joins the capture series",
              conn.execute("SELECT count(*) FROM capture_series_member").fetchone()[0] == 1)
        holding = conn.execute(
            "SELECT h.id FROM holding h").fetchall()
        check("DR-0118", "one holding is created", len(holding) == 1)
        stored = list((archive / "permanent").rglob("original.warc"))
        records = list(read_records(io.BufferedReader(io.BytesIO(stored[0].read_bytes())))) if stored else []
        check("DR-0006", "a warc-format source's import is stored as a WARC "
              "resource record holding the file",
              len(records) == 1 and records[0].record_type == "resource"
              and records[0].payload() == good.read_bytes()
              and records[0].target_uri == export_url)
        check("issue #51", "the quarantine copy is discharged after admission",
              not any((archive / "quarantine").iterdir()))
        software_agent_id = run_row[1].get("software_agent_id")
        check("DR-0097", "preservation events name the software agent, not the person",
              conn.execute("SELECT count(*) FROM preservation_event").fetchone()[0] > 0
              and conn.execute("SELECT count(*) FROM preservation_event "
                               "WHERE agent_id::text <> %s",
                               (software_agent_id,)).fetchone()[0] == 0)
        check("DR-0066", "an import creates no canonical knowledge",
              conn.execute("SELECT count(*) FROM documentary_assertion").fetchone()[0] == 0)

        # -- a file that fails its checks is a recorded failure ---------------

        code, _, _ = invoke(args(path=bad_header))
        failed = conn.execute(
            "SELECT outcome, error_detail, acquisition_route FROM acquisition_attempt "
            "ORDER BY attempted_at DESC LIMIT 1").fetchone()
        check("PRES-007", "a file with the wrong header is a recorded failure, not a holding",
              code == 1 and failed[0] == "failure" and failed[2] == "file-import"
              and "header is not the one recorded" in failed[1]
              and conn.execute("SELECT count(*) FROM holding").fetchone()[0] == 1)
        code, _, _ = invoke(args(count="3"))
        failed = conn.execute(
            "SELECT outcome, error_detail FROM acquisition_attempt "
            "ORDER BY attempted_at DESC LIMIT 1").fetchone()
        check("PRES-007", "a file over the stated count is a recorded failure",
              code == 1 and failed[0] == "failure" and "more than the 3" in failed[1]
              and conn.execute("SELECT count(*) FROM holding").fetchone()[0] == 1)

        # -- the collector itself refuses an export URL outside the locator ---

        roots, quarantine = open_roots(archive)
        collector = Collector(conn, FixtureFetcher({}), quarantine, roots, person,
                              ensure_software_agent(conn))
        source_id = str(conn.execute("SELECT id FROM source WHERE name = %s",
                                     (legal["name"],)).fetchone()[0])
        before = runs()
        try:
            collector.import_file(source_id, good, "https://example.invalid/x.csv",
                                  "Test founder", downloaded, EXPORT_HEADERS[LEGAL], 4, {})
            refused = False
        except PolicyViolation:
            refused = True
        check("DR-0071", "an export URL outside the registered locator is refused "
              "and nothing is recorded", refused and runs() == before)

        # -- an http-format source: bare file, unchanged on re-import --------

        vessels = copy.deepcopy(sources[VESSELS])
        vessels["capture_format"] = "http"
        commit(conn, [vessels], [], person)
        vessel_file = work / "vessels.csv"
        vessel_file.write_bytes(csv_bytes(VESSELS, 2))
        holdings_before = conn.execute("SELECT count(*) FROM holding").fetchone()[0]
        code1, _, _ = invoke(args(source=VESSELS, path=vessel_file, count="2"))
        code2, _, _ = invoke(args(source=VESSELS, path=vessel_file, count="2"))
        last = conn.execute(
            "SELECT outcome, acquisition_route, unchanged_basis FROM acquisition_attempt "
            "ORDER BY attempted_at DESC LIMIT 1").fetchone()
        stored_bare = [p for p in (archive / "permanent").rglob("original.bin")
                       if p.read_bytes() == vessel_file.read_bytes()]
        check("DR-0006", "an http-format source's import is stored as the bare file",
              code1 == 0 and len(stored_bare) == 1)
        check("issue #50", "re-importing the same file is recorded unchanged, as a "
              "file import, and not stored again",
              code2 == 0 and last == ("unchanged", "file-import", "digest-match")
              and conn.execute("SELECT count(*) FROM holding").fetchone()[0]
              == holdings_before + 1)

    finally:
        conn.close()

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
