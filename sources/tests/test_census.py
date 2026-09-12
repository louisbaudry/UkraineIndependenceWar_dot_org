#!/usr/bin/env python3
"""Tests for the census tool (WP 3.4 §4.1, Track A item A2).

No database, no network: `census()`'s aggregation and ranking logic is
exercised through `FixtureIndexClient`, and the real Common Crawl / Wayback
response parsers are exercised against hand-built payloads matching each
service's documented shape — the same "test the parsing, not the network"
split `collector/tests/test_warc_ingest.py` uses for WARC records.

Run:  python3 sources/tests/test_census.py
"""

from __future__ import annotations

import io
import sys
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "sources"))

from census import (  # noqa: E402
    CensusEntry,
    FixtureIndexClient,
    IndexQueryResult,
    IndexRecord,
    _parse_cc_index,
    _parse_cc_timestamp,
    _parse_wayback_rows,
    census,
    format_report,
    main,
)

PASSES: list[str] = []
FAILURES: list[str] = []


def check(req: str, what: str, condition: bool) -> None:
    (PASSES if condition else FAILURES).append(
        f"{'PASS' if condition else 'FAIL'}  {req} — {what}")


def ts(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=timezone.utc)


def run() -> int:
    # -- census(): aggregation, dedup, ranking -----------------------------

    cc = FixtureIndexClient("common-crawl", {
        "*.example.gov.ua": IndexQueryResult(
            index_name="common-crawl", domain_pattern="*.example.gov.ua",
            outcome="success", records=(
                IndexRecord(url="https://a.example.gov.ua/x", timestamp=ts("2024-01-01")),
                IndexRecord(url="https://a.example.gov.ua/y", timestamp=ts("2024-06-01")),
                IndexRecord(url="https://b.example.gov.ua/", timestamp=ts("2023-01-01")),
            ),
        ),
    })
    wayback = FixtureIndexClient("wayback", {
        "*.example.gov.ua": IndexQueryResult(
            index_name="wayback", domain_pattern="*.example.gov.ua",
            outcome="success", records=(
                IndexRecord(url="https://a.example.gov.ua/x", timestamp=ts("2020-01-01")),
                IndexRecord(url="https://c.example.gov.ua/", timestamp=ts("2022-01-01")),
            ),
        ),
    })

    entries, results = census("*.example.gov.ua", [cc, wayback])
    by_host = {e.host: e for e in entries}

    check("WP-3.4-A2", "every configured client is queried with the domain pattern",
          cc.queries == ["*.example.gov.ua"] and wayback.queries == ["*.example.gov.ua"])
    check("WP-3.4-A2", "records for the same host from different indexes are one entry",
          "a.example.gov.ua" in by_host and by_host["a.example.gov.ua"].total_captures == 3)
    check("WP-3.4-A2", "a host seen by both indexes records both names",
          by_host["a.example.gov.ua"].seen_by == ("common-crawl", "wayback"))
    check("WP-3.4-A2", "a host seen by only one index records only that one",
          by_host["b.example.gov.ua"].seen_by == ("common-crawl",)
          and by_host["c.example.gov.ua"].seen_by == ("wayback",))
    check("WP-3.4-A2", "first_seen/last_seen span every record for a host, across indexes",
          by_host["a.example.gov.ua"].first_seen == ts("2020-01-01")
          and by_host["a.example.gov.ua"].last_seen == ts("2024-06-01"))
    check("WP-3.4-A2", "entries are ranked by total captures, descending",
          [e.host for e in entries]
          == ["a.example.gov.ua", "b.example.gov.ua", "c.example.gov.ua"])
    check("DR-0027", "ranking is a triage signal only — no entry carries a truth claim",
          not any(hasattr(e, "verified") or hasattr(e, "confidence") for e in entries))

    # -- §28 / PRES-007: a failed query is recorded, not dropped -----------

    broken = FixtureIndexClient("broken-index", {})  # no fixture for any pattern
    entries2, results2 = census("*.unfixtured.test", [broken])
    check("§28", "a failed index query appears in results, explained",
          len(results2) == 1 and results2[0].outcome == "failure"
          and results2[0].error_detail)
    check("§28", "a failed query contributes no phantom entries",
          entries2 == [])

    mixed_entries, mixed_results = census("*.example.gov.ua", [cc, broken])
    check("§28", "one client failing does not suppress another client's results",
          any(e.host == "a.example.gov.ua" for e in mixed_entries)
          and any(r.outcome == "failure" for r in mixed_results))

    # -- format_report -------------------------------------------------------

    report = format_report("*.example.gov.ua", entries, results)
    check("WP-3.4-A2", "the report names the domain pattern queried",
          "*.example.gov.ua" in report)
    check("WP-3.4-A2", "the report is a ranked table, most-captured host first",
          report.index("a.example.gov.ua") < report.index("b.example.gov.ua")
          < report.index("c.example.gov.ua"))

    empty_report = format_report("*.nothing.test", [], [])
    check("WP-3.4-A2", "an empty census says so plainly rather than an empty table",
          "No hosts discovered" in empty_report)

    failed_report = format_report("*.unfixtured.test", entries2, results2)
    check("§28", "a failed query is visible in the rendered report, not silently absent",
          "broken-index" in failed_report and results2[0].error_detail in failed_report)

    # -- IndexQueryResult's own §28 discipline ------------------------------

    def build_unexplained_failure():
        IndexQueryResult(index_name="x", domain_pattern="y", outcome="failure")

    try:
        build_unexplained_failure()
        check("§28", "a failure with no explanation is refused at construction", False)
    except ValueError:
        check("§28", "a failure with no explanation is refused at construction", True)

    # -- real-format parsers, against hand-built payloads matching each
    #    service's documented shape (§ "What has not been verified") --------

    check("WP-3.4-A2", "_parse_cc_timestamp reads Common Crawl/Wayback's shared "
          "YYYYMMDDHHMMSS format as UTC",
          _parse_cc_timestamp("20240615120000")
          == datetime(2024, 6, 15, 12, 0, 0, tzinfo=timezone.utc))
    check("WP-3.4-A2", "_parse_cc_timestamp returns None rather than raising on "
          "a malformed or missing timestamp",
          _parse_cc_timestamp("not-a-timestamp") is None
          and _parse_cc_timestamp(None) is None)

    cc_body = (
        '{"urlkey": "ua,gov,example)/", "timestamp": "20240101000000", '
        '"url": "https://example.gov.ua/", "status": "200", '
        '"mime": "text/html", "digest": "ABCDEF"}\n'
        '{"urlkey": "ua,gov,example)/news", "timestamp": "20240615000000", '
        '"url": "https://example.gov.ua/news", "status": "200"}\n'
    )
    cc_records = _parse_cc_index(cc_body)
    check("WP-3.4-A2", "_parse_cc_index reads one record per JSON line",
          len(cc_records) == 2
          and cc_records[0].url == "https://example.gov.ua/"
          and cc_records[0].timestamp == ts("2024-01-01")
          and cc_records[1].status == "200")
    check("WP-3.4-A2", "_parse_cc_index skips a line it cannot parse, rather than crashing",
          len(_parse_cc_index('not json\n' + cc_body)) == 2)
    check("WP-3.4-A2", "_parse_cc_index skips a line with no url field",
          len(_parse_cc_index('{"timestamp": "20240101000000"}\n' + cc_body)) == 2)

    wayback_rows = [
        ["urlkey", "timestamp", "original", "mimetype", "statuscode", "digest", "length"],
        ["ua,gov,example)/", "20200101000000", "https://example.gov.ua/",
         "text/html", "200", "ABCDEF", "1234"],
        ["ua,gov,example)/news", "20210601000000", "https://example.gov.ua/news",
         "text/html", "200", "GHIJKL", "5678"],
    ]
    wb_records = _parse_wayback_rows(wayback_rows)
    check("WP-3.4-A2", "_parse_wayback_rows skips the header row and reads the rest",
          len(wb_records) == 2
          and wb_records[0].url == "https://example.gov.ua/"
          and wb_records[0].timestamp == ts("2020-01-01")
          and wb_records[0].status == "200")
    check("WP-3.4-A2", "_parse_wayback_rows returns nothing for an empty response",
          _parse_wayback_rows([]) == [])
    check("WP-3.4-A2", "_parse_wayback_rows returns nothing if the header lacks the "
          "fields this tool reads, rather than guessing column positions",
          _parse_wayback_rows([["digest", "length"], ["x", "1"]]) == [])
    check("WP-3.4-A2", "_parse_wayback_rows skips a short row rather than indexing "
          "past its end",
          len(_parse_wayback_rows(wayback_rows + [["short"]])) == 2)

    # -- CLI: argument validation needs no network at all -------------------

    err = io.StringIO()
    with redirect_stderr(err):
        code = main(["--domain", "x.test", "--index", "not-a-real-index"])
    check("WP-3.4-A2", "an unknown --index name is refused before any query is made",
          code == 2 and "unknown index" in err.getvalue())

    err = io.StringIO()
    with redirect_stderr(err):
        code = main(["--domain", "x.test", "--index", "common-crawl"])
    check("WP-3.4-A2", "querying common-crawl without --crawl-id is refused, "
          "not silently skipped",
          code == 2 and "--crawl-id" in err.getvalue())

    # -- CLI: the successful path, with injected fixture clients -----------

    out = io.StringIO()
    with redirect_stdout(out):
        code = main(["--domain", "*.example.gov.ua"], clients=[cc, wayback])
    check("WP-3.4-A2", "a run with at least one successful query exits 0",
          code == 0 and "a.example.gov.ua" in out.getvalue())

    out = io.StringIO()
    with redirect_stdout(out):
        code = main(["--domain", "*.unfixtured.test"], clients=[broken])
    check("§28", "a run where every query failed exits non-zero, not silently 0",
          code == 1)

    for line in PASSES:
        print(line)
    for line in FAILURES:
        print(line)
    print(f"\n{len(PASSES)} passed, {len(FAILURES)} failed")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(run())
