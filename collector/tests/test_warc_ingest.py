#!/usr/bin/env python3
"""End-to-end tests for retrospective recovery from WARC (WP 3.4 §4, CDR-P3-35).

Runs the real pipeline against a real PostgreSQL database and real OCFL
storage, fed a WARC file written by this suite. Where the warcio library is
importable, the reader is also cross-checked against it in both directions.

Each test names the requirement or Decision Record it verifies. CDR-P3-35 is a
**candidate**; tests naming it verify the proposal as drafted.

Run:  PGHOST=... PGPORT=... PGUSER=... python3 collector/tests/test_warc_ingest.py
"""

from __future__ import annotations

import base64
import gzip
import hashlib
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
from ocfl import StorageRoot  # noqa: E402
from pipeline import Collector, capture_series_id  # noqa: E402
from warc import (  # noqa: E402
    WarcFormatError,
    build_response_record,
    in_scope,
    iter_warc_records,
    read_records,
    verify_payload_digest,
)

shared.DB = "uiw_warc_test"
check, rejects, PASSES, FAILURES = shared.check, shared.rejects, shared.PASSES, shared.FAILURES


# -- a minimal WARC writer, so the fixtures are exactly what the tests say ------

def sha1_b32(data: bytes) -> str:
    return "sha1:" + base64.b32encode(hashlib.sha1(data).digest()).decode()


def http_response(status: int = 200, body: bytes = b"", chunked: bool = False,
                  content_type: str = "text/html") -> bytes:
    reason = {200: "OK", 404: "Not Found", 500: "Internal Server Error"}.get(status, "X")
    headers = [f"HTTP/1.1 {status} {reason}", f"Content-Type: {content_type}"]
    if chunked:
        headers.append("Transfer-Encoding: chunked")
        wire = b""
        for i in range(0, len(body), 5):
            piece = body[i:i + 5]
            wire += f"{len(piece):x}\r\n".encode() + piece + b"\r\n"
        wire += b"0\r\n\r\n"
    else:
        headers.append(f"Content-Length: {len(body)}")
        wire = body
    return "\r\n".join(headers).encode() + b"\r\n\r\n" + wire


def warc_record(rtype: str, block: bytes, uri: str | None = None, date: str = "2014-03-17T10:00:00Z",
                digest: str | None = None, version: str = "WARC/1.1",
                content_type: str = "application/http; msgtype=response",
                angle_uri: bool = False) -> bytes:
    lines = [version, f"WARC-Type: {rtype}", f"WARC-Record-ID: <urn:uuid:{uuid.uuid4()}>",
             f"WARC-Date: {date}", f"Content-Type: {content_type}",
             f"Content-Length: {len(block)}"]
    if uri:
        lines.append(f"WARC-Target-URI: {'<' + uri + '>' if angle_uri else uri}")
    if digest:
        lines.append(f"WARC-Payload-Digest: {digest}")
    return "\r\n".join(lines).encode() + b"\r\n\r\n" + block + b"\r\n\r\n"


def response_record(uri: str, body: bytes, date: str, status: int = 200, **kw) -> bytes:
    declared = kw.pop("digest", sha1_b32(body))
    chunked = kw.pop("chunked", False)
    return warc_record("response", http_response(status, body, chunked=chunked),
                       uri=uri, date=date, digest=declared, **kw)


def write_warc(path: Path, records: list[bytes], compress: bool) -> None:
    if compress:
        path.write_bytes(b"".join(gzip.compress(r) for r in records))  # one member per record
    else:
        path.write_bytes(b"".join(records))


# -- the suite --------------------------------------------------------------------

def run() -> int:
    shared.build_database()
    work = Path(tempfile.mkdtemp(prefix="uiw-warc-"))
    roots = {
        "permanent": StorageRoot(work / "ocfl-permanent", "permanent"),
        "medium-term": StorageRoot(work / "ocfl-medium", "medium-term"),
    }
    for root in roots.values():
        root.initialize()

    # -- reader unit checks, no database needed -------------------------------------

    check("DR-0071", "a URL under the registered locator is in scope",
          in_scope("https://example.invalid/oj/", "http://www.example.invalid/oj/reg-269"))
    check("DR-0071", "a subdomain of the registered host is in scope",
          in_scope("https://example.invalid/", "https://data.example.invalid/x"))
    check("DR-0071", "another host is out of scope",
          not in_scope("https://example.invalid/oj/", "https://elsewhere.invalid/oj/reg-269"))
    check("DR-0071", "a path outside the registered prefix is out of scope",
          not in_scope("https://example.invalid/oj/", "https://example.invalid/other/"))
    check("DR-0071", "a host that merely ends with the registered host is out of scope",
          not in_scope("https://example.invalid/", "https://notexample.invalid/"))
    check("DR-0071", "a source with no locator has no scope",
          not in_scope(None, "https://example.invalid/"))

    fixtures = work / "fixtures"
    fixtures.mkdir()
    body_v1 = b"<html>Regulation 269/2014 as first published</html>"
    body_v2 = b"<html>Regulation 269/2014 as amended</html>"
    body_chunked = b"a body long enough to be chunked into several pieces"
    records = [
        warc_record("warcinfo", b"software: test-writer\r\n",
                    content_type="application/warc-fields"),
        warc_record("request", b"GET /oj/reg-269 HTTP/1.1\r\nHost: example.invalid\r\n\r\n",
                    uri="https://example.invalid/oj/reg-269",
                    content_type="application/http; msgtype=request"),
        response_record("https://example.invalid/oj/reg-269", body_v1, "2014-03-17T10:00:00Z"),
        response_record("https://example.invalid/oj/reg-269", body_v2, "2015-01-01T00:00:00Z"),
        response_record("https://elsewhere.invalid/page", b"not ours", "2015-01-01T00:00:00Z"),
        response_record("https://example.invalid/oj/missing", b"gone", "2016-06-01T00:00:00Z", status=404),
        warc_record("revisit", b"", uri="https://example.invalid/oj/reg-269", date="2016-01-01T00:00:00Z",
                    content_type='application/http; msgtype=response'),
        response_record("https://example.invalid/oj/corrupt", b"claimed bytes", "2016-01-01T00:00:00Z",
                        digest=sha1_b32(b"different bytes")),
        response_record("https://example.invalid/oj/evil", b"x __MALICIOUS_TEST_MARKER__ y",
                        "2016-01-01T00:00:00Z"),
        response_record("https://example.invalid/oj/chunked", body_chunked, "2017-01-01T00:00:00Z",
                        chunked=True),
        response_record("https://example.invalid/oj/old-style", b"warc 1.0 style", "2014-01-01T00:00:00Z",
                        version="WARC/1.0", angle_uri=True, digest=None),
    ]
    # Every response record above, plus the revisit, is an item the archive holds
    # about *some* URL; the request and warcinfo records are not.
    expected_discovered = 9

    plain = fixtures / "archive.warc"
    compressed = fixtures / "archive.warc.gz"
    write_warc(plain, records, compress=False)
    write_warc(compressed, records, compress=True)

    parsed_plain = list(iter_warc_records(plain))
    parsed_gz = list(iter_warc_records(compressed))
    check("DR-0006", "the reader yields every record of a plain WARC",
          len(parsed_plain) == len(records))
    check("DR-0006", "the reader yields every record of a per-record-gzipped WARC",
          len(parsed_gz) == len(records))
    check("DR-0006", "a record's raw bytes are exactly what lay in the file",
          all(r.raw == fixture for r, fixture in zip(parsed_plain, records)))
    check("DR-0006", "a WARC 1.0 angle-bracketed target URI is read bare",
          parsed_plain[-1].target_uri == "https://example.invalid/oj/old-style")
    check("DR-0006", "WARC-Date is read as an aware UTC timestamp",
          parsed_plain[2].date == datetime(2014, 3, 17, 10, 0, tzinfo=timezone.utc))
    check("DR-0006", "chunked transfer-encoding is undone for the payload",
          parsed_plain[9].payload() == body_chunked)
    check("DR-0075", "a declared payload digest that matches is verified",
          verify_payload_digest(parsed_plain[2])[0] == "verified")
    check("DR-0075", "a declared payload digest over the de-chunked body is verified",
          verify_payload_digest(parsed_plain[9])[0] == "verified")
    check("DR-0075", "a declared payload digest that does not match is a mismatch",
          verify_payload_digest(parsed_plain[7])[0] == "mismatch")
    check("DR-0075", "an undeclared digest is reported as such, not as verified",
          verify_payload_digest(parsed_plain[-1])[0] == "undeclared")

    # -- the project's own writer, read back by the project's own reader ------------

    built = build_response_record(
        "https://example.invalid/oj/built", 200, "OK",
        [("Content-Type", "text/html; charset=utf-8"), ("Transfer-Encoding", "chunked"),
         ("Content-Encoding", "identity")],
        b"<html>built</html>", datetime(2026, 9, 9, 12, 0, 5, tzinfo=timezone.utc),
    )
    back = list(read_records(io.BufferedReader(io.BytesIO(built))))
    check("DR-0006", "a record the project writes is one record the project reads",
          len(back) == 1 and back[0].raw == built)
    check("DR-0006", "the written record carries URI, type, and capture time",
          back[0].record_type == "response"
          and back[0].target_uri == "https://example.invalid/oj/built"
          and back[0].date == datetime(2026, 9, 9, 12, 0, 5, tzinfo=timezone.utc))
    check("DR-0006", "the written record's HTTP envelope survives, minus the undone hop-by-hop header",
          back[0].http()[0] == 200
          and back[0].http()[1].get("content-type") == "text/html; charset=utf-8"
          and back[0].http()[1].get("content-encoding") == "identity"
          and "transfer-encoding" not in back[0].http()[1])
    check("DR-0075", "the written record declares a payload digest that verifies",
          verify_payload_digest(back[0])[0] == "verified")
    check("DR-0075", "the written record declares a block digest over the whole block",
          back[0].headers.get("warc-block-digest") == sha1_b32(back[0].block))
    def naive_time():
        build_response_record("https://x.invalid/", 200, "OK", [], b"", datetime(2026, 1, 1))
    rejects("DR-0006", "a capture time without a timezone is refused",
            naive_time)

    truncated = fixtures / "truncated.warc"
    good = records[2] + records[3]
    truncated.write_bytes(good[:-40])  # cut into the second record's block
    def read_truncated():
        return list(iter_warc_records(truncated))
    rejects("PRES-007", "a truncated record raises rather than yielding a short record",
            read_truncated)

    conn = psycopg.connect(dbname=shared.DB, autocommit=True)
    try:
        agent_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO pipeline_agent (id, kind, name, software_version) "
            "VALUES (%s, 'software', 'test-warc-ingester', '0.1.0')", (agent_id,))
        source_id = shared.seed_source(conn, locator="https://example.invalid/oj/",
                                       collection_method="warc-import")
        # Not testing the agent-of-record/software-agent split here, so the
        # same software agent serves both roles.
        collector = Collector(conn, None, work / "quarantine", roots,
                              agent_id, agent_id)

        run_id = collector.ingest_warc(source_id, compressed, "test-archive",
                                       configuration={"test": True})

        # -- DR-0070 / OPS-006: coverage -------------------------------------------

        discovered, acquired, skipped, failed, preserved, skip_reasons, failures, config = (
            conn.execute(
                "SELECT items_discovered, items_acquired, items_skipped, items_failed, "
                "bytes_preserved, skip_reasons, failure_details, configuration "
                "FROM collector_run WHERE id = %s", (run_id,)).fetchone())
        check("DR-0070", "the run counts every response and revisit record as discovered",
              discovered == expected_discovered)
        check("DR-0070", "the run acquired the in-scope, intact, clean captures",
              acquired == 4)  # reg-269 x2, chunked, old-style
        check("DR-0070", "the run skipped the out-of-scope, revisit and malicious records",
              skipped == 3 and skip_reasons == {
                  "scope:outside-registered-source": 1, "warc:revisit": 1,
                  "security:malicious": 1})
        check("DR-0070", "the run failed on the archived 404 and the digest mismatch",
              failed == 2)
        check("DR-0070", "discovered = acquired + skipped + failed",
              discovered == acquired + skipped + failed)
        check("DR-0070", "the run configuration names the archive and the file's digest",
              config["acquisition_source"] == "test-archive"
              and config["warc_file_sha256"] == hashlib.sha256(compressed.read_bytes()).hexdigest())

        # -- §28 / PRES-007: acquisition source ≠ original publisher -------------------

        attempts = conn.execute(
            "SELECT locator, outcome, acquisition_route, acquisition_source, "
            "original_captured_at, attempted_at, external_record_id, external_payload_digest "
            "FROM acquisition_attempt WHERE collector_run_id = %s ORDER BY original_captured_at",
            (run_id,)).fetchall()
        check("PRES-007", "one attempt per in-scope response record, and none for out-of-scope",
              len(attempts) == 7 and not any("elsewhere" in a[0] for a in attempts))
        check("PRES-007", "every attempt names the archive as its acquisition source",
              all(a[2] == "external-archive" and a[3] == "test-archive" for a in attempts))
        check("PRES-007", "the archive's capture time is kept distinct from our own",
              all(a[4] < a[5] for a in attempts)
              and attempts[0][4] == datetime(2014, 1, 1, tzinfo=timezone.utc))
        check("PRES-007", "the archive's record id and declared digest are carried",
              all(a[6] and a[6].startswith("<urn:uuid:") for a in attempts)
              and sum(1 for a in attempts if a[7]) == 6)
        by_locator = {a[0]: a for a in attempts}
        check("PRES-007", "an archived 404 is recorded as not-found with its capture time",
              by_locator["https://example.invalid/oj/missing"][1] == "not-found"
              and "2016-06-01" in conn.execute(
                  "SELECT error_detail FROM acquisition_attempt WHERE locator = %s",
                  ("https://example.invalid/oj/missing",)).fetchone()[0])

        # -- DR-0075: the archive's digest is checked, and a mismatch is not preserved ----

        corrupt = by_locator["https://example.invalid/oj/corrupt"]
        check("DR-0075", "a payload-digest mismatch is a recorded failed acquisition",
              corrupt[1] == "failure" and "WARC-Payload-Digest" in conn.execute(
                  "SELECT error_detail FROM acquisition_attempt WHERE locator = %s",
                  (corrupt[0],)).fetchone()[0])
        check("DR-0075", "nothing with a mismatched digest reaches the archive",
              conn.execute(
                  "SELECT count(*) FROM capture_series_member WHERE locator = %s",
                  (corrupt[0],)).fetchone()[0] == 0)
        check("DR-0075", "a verified declared digest is recorded as a fixity-check event",
              conn.execute(
                  "SELECT count(*) FROM preservation_event WHERE event_type = 'fixity-check' "
                  "AND outcome = 'success'").fetchone()[0] == 4)  # reg-269 x2, chunked, and the malicious one:
        # declared digests that matched, on records that reached quarantine. old-style declared none;
        # corrupt never reached quarantine; missing was a 404.

        # -- DR-0071(a): out-of-scope material is not written down at all ---------------

        check("DR-0071", "an out-of-scope URL appears nowhere in the store",
              conn.execute(
                  "SELECT count(*) FROM acquisition_attempt WHERE locator LIKE '%%elsewhere%%'"
              ).fetchone()[0] == 0)

        # -- DR-0074: two captures of one locator are two holdings in one series ----------

        series = conn.execute(
            "SELECT h.id, m.captured_at FROM capture_series_member m "
            "JOIN holding h ON h.id = m.holding_id WHERE m.series_id = %s ORDER BY m.captured_at",
            (capture_series_id(source_id, "https://example.invalid/oj/reg-269"),)).fetchall()
        check("DR-0074", "successive captures of one locator are separate holdings",
              len(series) == 2 and series[0][0] != series[1][0])
        check("DR-0074", "the series is ordered by the archive's capture time, not ours",
              [m[1] for m in series] == [datetime(2014, 3, 17, 10, tzinfo=timezone.utc),
                                         datetime(2015, 1, 1, tzinfo=timezone.utc)])
        check("DR-0074", "each holding is its own OCFL object at v1",
              conn.execute(
                  "SELECT count(DISTINCT ocfl_object_id) FROM preserved_object "
                  "WHERE ocfl_version = 'v1'").fetchone()[0] == 4)

        # -- DR-0006 / CDR-P3-35: the complete WARC record is what is preserved ------------

        obj = conn.execute(
            "SELECT p.ocfl_object_id, p.format_identifier FROM preserved_object p "
            "JOIN holding_representation hr ON hr.object_id = p.id "
            "WHERE hr.holding_id = %s", (series[0][0],)).fetchone()
        stored = (roots["permanent"].object_path(obj[0]) / "v1" / "content" / "original.warc")
        check("CDR-P3-35", "the preserved bytes are the complete WARC record, headers and all",
              stored.read_bytes() == records[2])
        check("CDR-P3-35", "the preserved record is recorded as WARC, not as its payload type",
              obj[1] == "application/warc")
        try:
            reparsed = list(iter_warc_records(stored))
        except WarcFormatError:
            reparsed = []  # not a WARC record at all: the check below goes red
        check("CDR-P3-35", "the preserved record re-reads to the same URI and payload",
              len(reparsed) == 1 and reparsed[0].target_uri == "https://example.invalid/oj/reg-269"
              and reparsed[0].payload() == body_v1)
        check("DR-0073", "the OCFL object verifies", roots["permanent"].fixity_check(obj[0]) == [])

        # -- SEC-002 / DR-0069 -------------------------------------------------------------

        check("SEC-002", "a record failing the security check is refused at Gate 1",
              conn.execute(
                  "SELECT count(*) FROM quarantine_item WHERE security_check_outcome = 'malicious' "
                  "AND gate1_decision = 'rejected'").fetchone()[0] == 1)

        # -- DR-0066 -----------------------------------------------------------------------

        check("DR-0066", "retrospective recovery creates no canonical knowledge by itself",
              conn.execute("SELECT count(*) FROM documentary_assertion").fetchone()[0] == 0)

        # -- policy refusals ---------------------------------------------------------------

        rejects("DR-0071", "ingesting for an unregistered source is refused",
                lambda: collector.ingest_warc(str(uuid.uuid4()), compressed, "test-archive", {}))
        paused = shared.seed_source(conn, lifecycle_state="paused", name="Paused",
                                    locator="https://example.invalid/oj/")
        rejects("DR-0067", "a paused source does not ingest",
                lambda: collector.ingest_warc(paused, compressed, "test-archive", {}))
        no_locator = shared.seed_source(conn, name="No locator", locator=None)
        rejects("DR-0071", "a source without a locator has no scope and is refused",
                lambda: collector.ingest_warc(no_locator, compressed, "test-archive", {}))
        rejects("PRES-007", "an unnamed acquisition source is refused",
                lambda: collector.ingest_warc(source_id, compressed, "", {}))

        # -- DR-0068: metadata-only stores nothing -------------------------------------------

        meta = shared.seed_source(conn, default_retention_tier="metadata-only",
                                  name="Metadata-only", locator="https://example.invalid/oj/")
        before = roots["permanent"].object_ids()
        meta_run = collector.ingest_warc(meta, plain, "test-archive", {})
        check("DR-0068", "a metadata-only source records the recovery but stores no bytes",
              roots["permanent"].object_ids() == before and conn.execute(
                  "SELECT items_discovered FROM collector_run WHERE id = %s",
                  (meta_run,)).fetchone()[0] == expected_discovered)

        # -- §57 / PRES-007: a bad file is part of the coverage record, not a crash ----------

        trunc_run = collector.ingest_warc(source_id, truncated, "test-archive", {})
        t_acq, t_failed, t_details, t_ended = conn.execute(
            "SELECT items_acquired, items_failed, failure_details, ended_at IS NOT NULL "
            "FROM collector_run WHERE id = %s", (trunc_run,)).fetchone()
        check("PRES-007", "records before a truncation are preserved; the fault is recorded",
              t_acq == 1 and t_failed == 1 and t_ended
              and any("WarcFormatError" in d.get("error", "") for d in t_details))

        # -- cross-check against warcio, when available -------------------------------------

        try:
            from warcio.archiveiterator import ArchiveIterator
            from warcio.statusandheaders import StatusAndHeaders
            from warcio.warcwriter import WARCWriter
        except ImportError:
            PASSES.append("SKIP  DR-0006 — warcio not importable; cross-check not run")
        else:
            buf = io.BytesIO()
            writer = WARCWriter(buf, gzip=True)
            http_headers = StatusAndHeaders("200 OK", [("Content-Type", "text/html")],
                                            protocol="HTTP/1.1")
            rec = writer.create_warc_record("https://example.invalid/oj/from-warcio", "response",
                                            payload=io.BytesIO(b"hello from warcio"),
                                            http_headers=http_headers)
            writer.write_record(rec)
            theirs = fixtures / "warcio.warc.gz"
            theirs.write_bytes(buf.getvalue())
            ours = list(iter_warc_records(theirs))
            check("DR-0006", "our reader reads a warcio-written record: URI, payload, digest",
                  len(ours) == 1 and ours[0].target_uri == "https://example.invalid/oj/from-warcio"
                  and ours[0].payload() == b"hello from warcio"
                  and verify_payload_digest(ours[0])[0] == "verified")
            with open(compressed, "rb") as fh:
                seen = [(r.rec_type, r.rec_headers.get_header("WARC-Target-URI"),
                         r.content_stream().read() if r.rec_type == "response" else None)
                        for r in ArchiveIterator(fh)]
            check("DR-0006", "warcio reads every record our writer produced",
                  len(seen) == len(records))
            check("DR-0006", "warcio agrees on our fixture's URIs and payloads",
                  seen[2] == ("response", "https://example.invalid/oj/reg-269", body_v1)
                  and seen[9][2] == body_chunked)
            with io.BytesIO(built) as fh:
                mine = [(r.rec_type, r.rec_headers.get_header("WARC-Target-URI"),
                         r.http_headers.get_statuscode(), r.content_stream().read())
                        for r in ArchiveIterator(fh)]
            check("DR-0006", "warcio reads a record built by build_response_record",
                  mine == [("response", "https://example.invalid/oj/built", "200",
                            b"<html>built</html>")])

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
