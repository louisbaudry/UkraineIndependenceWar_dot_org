#!/usr/bin/env python3
"""Tests for not storing unchanged bytes again (issue #50).

The 2026-09-09 rehearsal showed a source fetched on a schedule being preserved
again whether or not its bytes had changed. Two rules now, each recorded as an
`acquisition_attempt` with outcome 'unchanged' that points at the holding it
confirmed and creates no quarantine item, object or holding:

- 'not-modified': the origin answered a conditional request with HTTP 304;
- 'digest-match': the bytes were fetched and equal the latest capture's.

Design choices (the drafter's, assumed pending the founder's ruling at review;
see collector/README.md) are what these tests pin down: only `http` capture
format, only against the *latest* capture, only while retention/access/rights
are unchanged, and never against the validators of a rejected response.

Real PostgreSQL, real OCFL storage, real pipeline; the network is a fixture,
plus a loopback `http.server` for `HttpFetcher`'s conditional request.

Run:  PGHOST=... PGPORT=... PGUSER=... python3 collector/tests/test_unchanged_captures.py
"""

from __future__ import annotations

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
from fetch import FetchResult, FixtureFetcher, HttpFetcher, validators_from  # noqa: E402
from ocfl import StorageRoot  # noqa: E402
from pipeline import Collector, ensure_software_agent  # noqa: E402

shared.DB = "uiw_unchanged_test"
check, rejects, PASSES, FAILURES = shared.check, shared.rejects, shared.PASSES, shared.FAILURES

NOW = lambda: datetime.now(timezone.utc)  # noqa: E731
LOC = "https://example.invalid/oj/list"


def ok(locator: str, body: bytes, etag: str | None = None) -> FetchResult:
    headers = {"Content-Type": "text/html"}
    if etag:
        headers["ETag"] = etag
        headers["Last-Modified"] = "Tue, 15 Nov 1994 12:45:26 GMT"
    return FetchResult(locator=locator, attempted_at=NOW(), outcome="success", content=body,
                       media_type="text/html", response_headers=headers,
                       http_status=200, http_reason="OK")


def not_modified(locator: str, etag: str) -> FetchResult:
    return FetchResult(locator=locator, attempted_at=NOW(), outcome="not-modified",
                       response_headers={"ETag": etag}, http_status=304, http_reason="Not Modified")


class _Handler(BaseHTTPRequestHandler):
    seen: list[dict] = []
    always_304 = False

    def version_string(self):
        return "fixture/1.0"

    def do_GET(self):  # noqa: N802
        _Handler.seen.append({"if-none-match": self.headers.get("If-None-Match"),
                              "if-modified-since": self.headers.get("If-Modified-Since")})
        if _Handler.always_304 or self.headers.get("If-None-Match") == '"v1"':
            self.send_response(304)
            self.send_header("ETag", '"v1"')
            self.end_headers()
            return
        body = b"<html>served</html>"
        self.send_response(200)
        self.send_header("ETag", '"v1"')
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def run() -> int:
    shared.build_database()
    work = Path(tempfile.mkdtemp(prefix="uiw-unchanged-"))

    check("DR-0093", "validators are read from recorded (lower-case) header names",
          validators_from({"etag": '"x"', "last-modified": "d", "server": "s"})
          == {"etag": '"x"', "last-modified": "d"})
    check("DR-0093", "a header block with no validators yields None",
          validators_from({"server": "s"}) is None and validators_from(None) is None)

    roots = {"permanent": StorageRoot(work / "ocfl-permanent", "permanent"),
             "medium-term": StorageRoot(work / "ocfl-medium", "medium-term")}
    for r in roots.values():
        r.initialize()

    conn = psycopg.connect(dbname=shared.DB, autocommit=True)
    try:
        person = str(uuid.uuid4())
        conn.execute("INSERT INTO pipeline_agent (id, kind, name) VALUES (%s, 'person', 'op')", (person,))
        software = ensure_software_agent(conn, "test-collector", "0.1.0")
        source_id = shared.seed_source(conn, locator="https://example.invalid/oj/")
        fetcher = FixtureFetcher({})
        collector = Collector(conn, fetcher, work / "quarantine", roots, person, software)

        def go(result_or_none, loc=LOC, src=source_id, coll=None):
            fx = (coll or collector).fetcher
            if result_or_none is not None:
                fx.fixtures[loc] = result_or_none
            try:
                return (coll or collector).run(src, [loc], configuration={})
            except Exception as exc:  # noqa: BLE001 -- a crashed run must show as failed checks
                print(f"  (run raised {type(exc).__name__}: {str(exc)[:80]})")
                return None

        def counts():
            q = lambda sql: conn.execute(sql).fetchone()[0]  # noqa: E731
            return {"holdings": q("SELECT count(*) FROM holding"),
                    "objects": q("SELECT count(*) FROM preserved_object"),
                    "quarantine": q("SELECT count(*) FROM quarantine_item"),
                    "ocfl": len(roots["permanent"].object_ids())}

        def attempt(run_id):
            if run_id is None:
                return (None, None, None, None)
            row = conn.execute(
                "SELECT outcome, unchanged_basis, unchanged_of_holding_id, response_headers "
                "FROM acquisition_attempt WHERE collector_run_id = %s", (run_id,)).fetchone()
            return row if row is not None else ("no attempt recorded", None, None, None)

        def totals(run_id):
            if run_id is None:
                return (None, None, None, None)
            return conn.execute(
                "SELECT items_acquired, items_skipped, bytes_preserved, skip_reasons "
                "FROM collector_run WHERE id = %s", (run_id,)).fetchone()

        v1 = b"<html>published list, version one</html>"

        # -- a first capture: nothing to compare against ---------------------------------
        r1 = go(ok(LOC, v1, '"v1"'))
        first_holding = conn.execute("SELECT id FROM holding").fetchone()[0]
        check("§26", "a first capture is stored as before",
              counts() == {"holdings": 1, "objects": 1, "quarantine": 1, "ocfl": 1}
              and attempt(r1)[0] == "success")
        check("DR-0093", "no conditional request is made when nothing is held",
              fetcher.validators_seen[-1] == (LOC, None))
        base = counts()
        qfiles = len(list((work / "quarantine").iterdir()))

        # -- same bytes again, origin does not do 304: digest-match ----------------------
        r2 = go(ok(LOC, v1, '"v1"'))
        a2 = attempt(r2)
        check("DR-0093", "the second run asks against the validators it holds",
              fetcher.validators_seen[-1][1] == {"etag": '"v1"',
                                                 "last-modified": "Tue, 15 Nov 1994 12:45:26 GMT"})
        check("§26", "identical bytes create no holding, object, quarantine item or OCFL object",
              counts() == base)
        check("DR-0069", "identical bytes are not written to quarantine at all",
              len(list((work / "quarantine").iterdir())) == qfiles)
        check("PRES-007", "the attempt is recorded as unchanged, by digest match, naming the holding",
              a2[0] == "unchanged" and a2[1] == "digest-match" and a2[2] == first_holding)
        check("DR-0093", "the unchanged attempt keeps the origin's headers",
              a2[3] is not None and a2[3].get("etag") == '"v1"')
        t2 = totals(r2)
        check("DR-0070", "coverage says skipped-as-unchanged, acquired 0, nothing preserved",
              t2[0] == 0 and t2[1] == 1 and t2[2] == 0 and t2[3] == {"unchanged": 1})

        # -- same bytes, origin answers 304: not-modified ---------------------------------
        r3 = go(not_modified(LOC, '"v1"'))
        a3 = attempt(r3)
        check("PRES-007", "a 304 is recorded as unchanged, by not-modified, naming the holding",
              a3[0] == "unchanged" and a3[1] == "not-modified" and a3[2] == first_holding)
        check("§26", "a 304 creates nothing", counts() == base)

        # -- a 304 with nothing held, or never asked for, is a failure, not a confirmation --
        loc2 = "https://example.invalid/oj/other"
        r4 = go(not_modified(loc2, '"z"'), loc=loc2)
        check("PRES-007", "a 304 where nothing is held is recorded as a failure, never as unchanged",
              attempt(r4)[0] == "failure" and counts() == base)

        # -- changed bytes: a new holding, in the same series -----------------------------
        v2 = b"<html>published list, version TWO</html>"
        r5 = go(ok(LOC, v2, '"v2"'))
        check("§26", "changed bytes are stored as a new holding",
              counts()["holdings"] == 2 and attempt(r5)[0] == "success")
        series = conn.execute("SELECT count(*) FROM capture_series_member").fetchone()[0]
        check("DR-0074", "both captures are in the one capture series", series == 2)

        # -- a revert to the old bytes is a change: compared with the LATEST only ----------
        r6 = go(ok(LOC, v1, '"v1"'))
        check("DR-0074", "bytes that return to an older version are captured again, not 'unchanged'",
              attempt(r6)[0] == "success" and counts()["holdings"] == 3)

        # -- a policy change is a reason to capture again ---------------------------------
        conn.execute("UPDATE source SET default_access_tier = 'internal' WHERE id = %s", (source_id,))
        before = counts()["holdings"]
        r7 = go(ok(LOC, v1, '"v1"'))
        check("DR-0086", "identical bytes under a changed access tier are captured again",
              attempt(r7)[0] == "success" and counts()["holdings"] == before + 1)
        check("DR-0086", "no conditional request is made against a holding made under another policy",
              fetcher.validators_seen[-1][1] is None)
        conn.execute("UPDATE source SET default_access_tier = 'public' WHERE id = %s", (source_id,))

        # -- validators come only from responses that were admitted or confirmed -----------
        loc3 = "https://example.invalid/oj/guarded"
        go(ok(loc3, b"good bytes", '"A"'), loc=loc3)
        bad = ok(loc3, b"x __MALICIOUS_TEST_MARKER__ y", '"B"')
        rb = go(bad, loc=loc3)
        check("SEC-002", "the rejected response is recorded and nothing new is admitted",
              attempt(rb)[0] == "success"
              and conn.execute("SELECT gate1_decision FROM quarantine_item q JOIN acquisition_attempt a "
                               "ON a.id = q.acquisition_attempt_id WHERE a.collector_run_id = %s",
                               (rb,)).fetchone()[0] == "rejected")
        go(ok(loc3, b"good bytes", '"A"'), loc=loc3)
        check("SEC-002", "validators are those of the admitted capture, not the rejected response",
              fetcher.validators_seen[-1][1] is not None
              and fetcher.validators_seen[-1][1]["etag"] == '"A"')

        # -- a warc source is not deduplicated (its stored bytes carry capture time) -------
        warc_source = shared.seed_source(conn, capture_format="warc", locator="https://example.invalid/w/")
        locw = "https://example.invalid/w/p"
        wres = lambda: FetchResult(locator=locw, attempted_at=NOW(), outcome="success",  # noqa: E731
                                   content=b"same warc body", media_type="text/html",
                                   response_headers={"ETag": '"w"'}, http_status=200, http_reason="OK")
        go(wres(), loc=locw, src=warc_source)
        go(wres(), loc=locw, src=warc_source)
        check("DR-0006", "a warc-format source stores each capture; identical bytes are not 'unchanged'",
              conn.execute("SELECT count(*) FROM acquisition_attempt a JOIN source s ON s.id = a.source_id "
                           "WHERE s.id = %s AND a.outcome = 'success'", (warc_source,)).fetchone()[0] == 2
              and fetcher.validators_seen[-1][1] is None)

        # -- the database holds the shape the code builds ---------------------------------
        def raw_attempt(outcome, holding, basis):
            conn.execute(
                "INSERT INTO acquisition_attempt (id, source_id, locator, attempted_at, outcome, "
                "unchanged_of_holding_id, unchanged_basis) VALUES (%s, %s, 'https://example.invalid/x', "
                "now(), %s, %s, %s)", (str(uuid.uuid4()), source_id, outcome, holding, basis))

        rejects("§28", "the database refuses an 'unchanged' attempt that names no holding",
                lambda: raw_attempt("unchanged", None, "digest-match"))
        rejects("§28", "the database refuses an 'unchanged' attempt that names no basis",
                lambda: raw_attempt("unchanged", first_holding, None))
        rejects("§28", "the database refuses a non-unchanged attempt that names a holding",
                lambda: raw_attempt("success", first_holding, "digest-match"))
        rejects("§28", "the database refuses an unchanged attempt pointing at no real holding",
                lambda: raw_attempt("unchanged", str(uuid.uuid4()), "digest-match"))
        rejects("§28", "the database refuses an unknown basis",
                lambda: raw_attempt("unchanged", first_holding, "vibes"))
        raw_attempt("unchanged", first_holding, "not-modified")
        check("§28", "the database accepts a well-formed unchanged attempt", True)

        # -- HttpFetcher makes the conditional request, against a loopback server ---------
        os.environ["no_proxy"] = os.environ["NO_PROXY"] = "127.0.0.1,localhost"
        server = HTTPServer(("127.0.0.1", 0), _Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        base_url = f"http://127.0.0.1:{server.server_port}/doc"
        hf = HttpFetcher("uiw-test")
        _Handler.seen.clear()
        plain = hf.fetch(base_url)
        check("DR-0093", "without validators HttpFetcher sends no conditional header",
              plain.outcome == "success" and _Handler.seen[-1] == {"if-none-match": None,
                                                                  "if-modified-since": None})
        cond = hf.fetch(base_url, validators={"etag": '"v1"',
                                              "last-modified": "Tue, 15 Nov 1994 12:45:26 GMT"})
        check("DR-0093", "with validators HttpFetcher sends If-None-Match and If-Modified-Since",
              _Handler.seen[-1] == {"if-none-match": '"v1"',
                                    "if-modified-since": "Tue, 15 Nov 1994 12:45:26 GMT"})
        check("PRES-007", "a 304 to a conditional request is 'not-modified', carrying no content and its headers",
              cond.outcome == "not-modified" and cond.content is None
              and cond.response_headers.get("ETag") == '"v1"' and cond.http_status == 304)
        stale = hf.fetch(base_url, validators={"etag": '"old"'})
        check("DR-0093", "a validator that no longer matches gets the full 200",
              stale.outcome == "success" and stale.content == b"<html>served</html>")
        _Handler.always_304 = True
        unasked = hf.fetch(base_url)
        check("PRES-007", "a 304 to a request that was not conditional is a refusal, not 'not-modified'",
              unasked.outcome == "refused")
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
