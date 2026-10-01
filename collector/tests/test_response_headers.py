#!/usr/bin/env python3
"""Tests for preserving the response headers a fetch already receives (issue #74).

The 2026-09-09 rehearsal showed `Last-Modified`, `ETag`, filenames and a
publisher's own metadata arriving at the fetcher and being discarded by the
acquisition record. Those headers exist only at fetch time. Placement
(`acquisition_attempt.response_headers`, jsonb) is the drafter's recommended
design, assumed pending the founder's ruling at review; if the founder rules
otherwise, this suite changes with it.

Real PostgreSQL, real OCFL storage, real pipeline; only the network is a
fixture, plus a loopback `http.server` that exercises `HttpFetcher`'s header
capture (never a live publisher: `HttpFetcher` is still unverified against one).

Each test names the requirement or Decision Record it verifies.

Run:  PGHOST=... PGPORT=... PGUSER=... python3 collector/tests/test_response_headers.py
"""

from __future__ import annotations

import base64
import hashlib
import os
import shutil
import sys
import tempfile
import threading
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "collector"))
sys.path.insert(0, str(ROOT / "storage"))
sys.path.insert(0, str(ROOT / "collector" / "tests"))

import psycopg  # noqa: E402

import test_pipeline as shared  # noqa: E402
from fetch import FetchResult, FixtureFetcher, HttpFetcher, record_headers  # noqa: E402
from ocfl import StorageRoot  # noqa: E402
from pipeline import Collector, ensure_software_agent  # noqa: E402

shared.DB = "uiw_headers_test"
check, rejects, PASSES, FAILURES = shared.check, shared.rejects, shared.PASSES, shared.FAILURES

NOW = lambda: datetime.now(timezone.utc)  # noqa: E731


def success(locator: str, body: bytes, headers: dict | None) -> FetchResult:
    return FetchResult(locator=locator, attempted_at=NOW(), outcome="success",
                       content=body, media_type="text/html",
                       response_headers=headers or {}, http_status=200, http_reason="OK")


# -- a loopback server, so HttpFetcher's header capture is exercised for real ------

class _Handler(BaseHTTPRequestHandler):
    def version_string(self):  # one Server header, ours, so the 404 check is unambiguous
        return "fixture/1.0"

    def do_GET(self):  # noqa: N802
        if self.path == "/doc":
            body = b"<html>fixture</html>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("ETag", '"abc123"')
            self.send_header("Last-Modified", "Tue, 15 Nov 1994 12:45:26 GMT")
            self.send_header("Content-Disposition", 'attachment; filename="list.xml"')
            self.send_header("Set-Cookie", "session=SECRET; Path=/")
            self.send_header("Link", "<https://example.invalid/a>; rel=alternate")
            self.send_header("Link", "<https://example.invalid/b>; rel=canonical")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/limited":
            self.send_response(429)
            self.send_header("Retry-After", "120")
            self.send_header("Content-Length", "0")
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header("Content-Length", "0")
            self.end_headers()

    def log_message(self, *args):  # silence
        pass


def run() -> int:
    shared.build_database()
    work = Path(tempfile.mkdtemp(prefix="uiw-headers-"))

    # -- the normaliser, no database needed -------------------------------------------

    check("PRES-007", "no headers is None, a distinct state from a recorded block",
          record_headers(None) is None and record_headers({}) is None)
    check("DR-0093", "names are lower-cased so a JSON lookup cannot miss on case",
          record_headers({"ETag": '"x"', "Last-Modified": "d"}) == {"etag": '"x"', "last-modified": "d"})
    check("DR-0093", "the same header under two spellings is joined, none lost",
          record_headers({"Link": "<a>", "link": "<b>"}) == {"link": "<a>, <b>"})
    check("DR-0093", "cookies are not recorded (session state, not a statement about the document)",
          record_headers({"Set-Cookie": "s=1", "set-cookie2": "x", "ETag": "e"}) == {"etag": "e"})
    check("PRES-007", "a block of only cookies records as None, not as an empty map",
          record_headers({"Set-Cookie": "s=1"}) is None)
    check("PRES-007", "a NUL byte (which jsonb cannot hold) is repaired, not raised",
          record_headers({"X-Odd": "a\x00b"}) == {"x-odd": "a�b"})
    check("PRES-007", "a lone surrogate is repaired, not raised",
          "\ud800" not in (record_headers({"X-Odd": "a\ud800b"}) or {}).get("x-odd", "\ud800"))
    check("PRES-007", "a non-text value is stored as its text form, not a crash",
          record_headers({"X-N": 7}) == {"x-n": "7"})
    check("PRES-007", "an empty header name is skipped",
          record_headers({"": "v", "ok": "1"}) == {"ok": "1"})

    # -- the pipeline, against the real database ----------------------------------------

    roots = {"permanent": StorageRoot(work / "ocfl-permanent", "permanent"),
             "medium-term": StorageRoot(work / "ocfl-medium", "medium-term")}
    for r in roots.values():
        r.initialize()

    conn = psycopg.connect(dbname=shared.DB, autocommit=True)
    try:
        person = str(uuid.uuid4())
        conn.execute("INSERT INTO pipeline_agent (id, kind, name) VALUES (%s, 'person', 'op')",
                     (person,))
        software = ensure_software_agent(conn, "test-collector", "0.1.0")
        source_id = shared.seed_source(conn)
        warc_source_id = shared.seed_source(conn, capture_format="warc",
                                            locator="https://example.invalid/w")

        body = b"<html>published instrument</html>"
        fetcher = FixtureFetcher({
            "https://example.invalid/oj/ok": success("https://example.invalid/oj/ok", body, {
                "ETag": '"v1"', "Last-Modified": "Tue, 15 Nov 1994 12:45:26 GMT",
                "Content-Disposition": 'attachment; filename="regulation.xml"',
                "Set-Cookie": "sid=SECRET"}),
            "https://example.invalid/oj/plain": success("https://example.invalid/oj/plain", b"x", None),
            "https://example.invalid/oj/cookies": success("https://example.invalid/oj/cookies", b"y",
                                                          {"Set-Cookie": "sid=SECRET"}),
            "https://example.invalid/oj/odd": success("https://example.invalid/oj/odd", b"z",
                                                      {"X-Odd": "a\x00b"}),
            "https://example.invalid/oj/limited": FetchResult(
                locator="https://example.invalid/oj/limited", attempted_at=NOW(), outcome="refused",
                error_detail="HTTP 429: Too Many Requests",
                response_headers={"Retry-After": "120", "Date": "Mon, 01 Oct 2026 00:00:00 GMT"},
                http_status=429, http_reason="Too Many Requests"),
            "https://example.invalid/oj/timeout": TimeoutError("timed out"),
        })
        collector = Collector(conn, fetcher, work / "quarantine", roots, person, software)
        run_id = collector.run(source_id, [
            "https://example.invalid/oj/ok", "https://example.invalid/oj/plain",
            "https://example.invalid/oj/cookies", "https://example.invalid/oj/odd",
            "https://example.invalid/oj/limited", "https://example.invalid/oj/timeout",
        ], configuration={"test": True})

        def headers_of(tail: str):
            row = conn.execute(
                "SELECT response_headers, outcome FROM acquisition_attempt "
                "WHERE collector_run_id = %s AND locator LIKE %s", (run_id, f"%{tail}")
            ).fetchone()
            return row if row is not None else (None, "no attempt recorded")

        ok, _ = headers_of("/ok")
        check("DR-0093", "a successful attempt keeps the publisher's ETag",
              ok is not None and ok.get("etag") == '"v1"')
        check("DR-0093", "a successful attempt keeps Last-Modified",
              (ok or {}).get("last-modified") == "Tue, 15 Nov 1994 12:45:26 GMT")
        check("DR-0093", "a successful attempt keeps the publisher's own filename",
              "regulation.xml" in (ok or {}).get("content-disposition", ""))
        check("DR-0093", "the cookie the origin set is not recorded", "set-cookie" not in (ok or {}))
        check("DR-0093", "the stored map can be read back by a lower-case key, as #50 will",
              conn.execute(
                  "SELECT response_headers->>'etag' FROM acquisition_attempt "
                  "WHERE collector_run_id = %s AND locator LIKE '%%/ok'", (run_id,)
              ).fetchone()[0] == '"v1"')

        plain, plain_outcome = headers_of("/plain")
        check("PRES-007", "an attempt with no headers is recorded with none (SQL NULL)",
              plain is None and plain_outcome == "success")
        cookies, _ = headers_of("/cookies")
        check("PRES-007", "an attempt with only cookies is SQL NULL, not a JSON null",
              cookies is None and conn.execute(
                  "SELECT response_headers IS NULL FROM acquisition_attempt "
                  "WHERE collector_run_id = %s AND locator LIKE '%%/cookies'", (run_id,)
              ).fetchone()[0])
        odd, odd_outcome = headers_of("/odd")
        check("PRES-007", "a malformed header value does not crash or lose the acquisition",
              odd_outcome == "success" and (odd or {}).get("x-odd") == "a�b")
        limited, limited_outcome = headers_of("/limited")
        check("PRES-007", "a refusal's headers are recorded: they are coverage facts",
              limited_outcome == "refused" and (limited or {}).get("retry-after") == "120")
        timeout, timeout_outcome = headers_of("/timeout")
        check("PRES-007", "a failure before any response records no headers, and is still recorded",
              timeout is None and timeout_outcome == "failure")

        # §28: the headers are a statement of the origin; our own observations stay ours.
        row = conn.execute(
            "SELECT a.acquisition_route, encode(q.sha256, 'hex') FROM acquisition_attempt a "
            "JOIN quarantine_item q ON q.acquisition_attempt_id = a.id "
            "WHERE a.collector_run_id = %s AND a.locator LIKE '%%/ok'", (run_id,)).fetchone()
        check("§28", "the attempt says how the bytes were obtained, so the headers can be read with it",
              row[0] == "live-fetch")
        check("§28", "our own sha256 of the bytes is unaffected by, and separate from, the headers",
              row[1] == hashlib.sha256(body).hexdigest())

        # DR-0006: a WARC source is wrapped, and the headers are still recorded.
        wf = FixtureFetcher({"https://example.invalid/w/p": success(
            "https://example.invalid/w/p", b"warc body", {"ETag": '"w1"'})})
        wcoll = Collector(conn, wf, work / "wq", roots, person, software)
        wrun = wcoll.run(warc_source_id, ["https://example.invalid/w/p"], configuration={})
        check("DR-0006", "a WARC-capture source still records the origin's headers on the attempt",
              conn.execute("SELECT response_headers->>'etag' FROM acquisition_attempt "
                           "WHERE collector_run_id = %s", (wrun,)).fetchone()[0] == '"w1"')

        # The database refuses what the code would never write (policy in both places).
        def insert_headers(value_sql: str):
            conn.execute(
                "INSERT INTO acquisition_attempt (id, source_id, locator, attempted_at, outcome, "
                "response_headers) VALUES (%s, %s, 'https://example.invalid/x', now(), 'success', "
                f"{value_sql}::jsonb)", (str(uuid.uuid4()), source_id))

        rejects("PRES-007", "the database refuses a header block that is a list",
                lambda: insert_headers("'[1,2]'"))
        rejects("PRES-007", "the database refuses a header block that is a bare string",
                lambda: insert_headers("'\"etag\"'"))
        insert_headers("'{\"etag\": \"x\"}'")
        check("PRES-007", "the database accepts a name->value map", True)

        # §28: an archive's capture records the origin's headers in the HTTP block and its
        # own in the WARC headers. Only the first are the publisher's statements.
        wbody = b"<html>archived instrument</html>"
        http_block = (b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nETag: \"arch1\"\r\n"
                      b"Last-Modified: Fri, 14 Mar 2014 09:00:00 GMT\r\n"
                      + f"Content-Length: {len(wbody)}\r\n\r\n".encode() + wbody)
        digest = "sha1:" + base64.b32encode(hashlib.sha1(wbody).digest()).decode()
        warc_rec = (
            "WARC/1.1\r\nWARC-Type: response\r\n"
            f"WARC-Record-ID: <urn:uuid:{uuid.uuid4()}>\r\nWARC-Date: 2014-03-17T10:00:00Z\r\n"
            "Content-Type: application/http; msgtype=response\r\n"
            f"Content-Length: {len(http_block)}\r\n"
            "WARC-Target-URI: https://example.invalid/oj/archived\r\n"
            f"WARC-Payload-Digest: {digest}\r\n\r\n").encode() + http_block + b"\r\n\r\n"
        warc_path = work / "capture.warc"
        warc_path.write_bytes(warc_rec)
        arch_source = shared.seed_source(conn, locator="https://example.invalid/oj/")
        acoll = Collector(conn, None, work / "aq", roots, person, software)
        arun = acoll.ingest_warc(arch_source, warc_path, "test-archive", configuration={})
        arow = conn.execute(
            "SELECT response_headers, acquisition_route FROM acquisition_attempt "
            "WHERE collector_run_id = %s", (arun,)).fetchone()
        check("§28", "a WARC recovery records the origin's HTTP headers from the archived response",
              arow[0] is not None and arow[0].get("etag") == '"arch1"'
              and arow[0].get("last-modified") == "Fri, 14 Mar 2014 09:00:00 GMT")
        check("§28", "the archive's own WARC headers are not recorded as the origin's response headers",
              arow[0] is not None and not any(k.startswith("warc-") for k in arow[0]))
        check("§28", "the attempt says it came from an external archive, so the headers read as the archive's record",
              arow[1] == "external-archive")

        # -- HttpFetcher against a loopback server -------------------------------------
        os.environ["no_proxy"] = os.environ["NO_PROXY"] = "127.0.0.1,localhost"
        server = HTTPServer(("127.0.0.1", 0), _Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{server.server_port}"
        hf = HttpFetcher("uiw-test")
        r_ok = hf.fetch(f"{base}/doc")
        check("DR-0093", "HttpFetcher captures the response headers of a success",
              r_ok.outcome == "success" and r_ok.response_headers.get("ETag") == '"abc123"')
        check("DR-0093", "recording the live response keeps the validators and drops the cookie",
              (record_headers(r_ok.response_headers) or {}).get("last-modified")
              == "Tue, 15 Nov 1994 12:45:26 GMT"
              and "set-cookie" not in (record_headers(r_ok.response_headers) or {}))
        check("DR-0093", "a header the server repeats is joined at capture, not reduced to its first value",
              r_ok.response_headers.get("Link", "").count("rel=") == 2)
        r_lim = hf.fetch(f"{base}/limited")
        check("PRES-007", "HttpFetcher captures the headers of a refusal and its status",
              r_lim.outcome == "refused" and r_lim.response_headers.get("Retry-After") == "120"
              and r_lim.http_status == 429)
        r_404 = hf.fetch(f"{base}/missing")
        check("PRES-007", "HttpFetcher captures the headers of a 404",
              r_404.outcome == "not-found" and r_404.response_headers.get("Server") == "fixture/1.0")
        server.shutdown()
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
