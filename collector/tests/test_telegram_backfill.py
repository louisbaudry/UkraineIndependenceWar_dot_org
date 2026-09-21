#!/usr/bin/env python3
"""Tests for collector/telegram_backfill.py.

The rules worth testing: pagination parsing is correct (only this
channel's ids, not a forwarded post's), the loop stops at each of its
three legitimate stopping points and for no other reason, and — the
point of the whole `CachingFetcher` design — preserving a page never
costs a second network request for it.

Run:  PGHOST=… PGPORT=… PGUSER=… python3 collector/tests/test_telegram_backfill.py
"""

from __future__ import annotations

import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "collector"))
sys.path.insert(0, str(ROOT / "storage"))

import psycopg  # noqa: E402

from fetch import FetchResult  # noqa: E402
from ocfl import StorageRoot  # noqa: E402
from pipeline import Collector, ensure_software_agent  # noqa: E402
from telegram_backfill import (  # noqa: E402
    CachingFetcher, backfill, extract_post_ids,
)

PASSES: list[str] = []
FAILURES: list[str] = []
DB = "uiw_telegram_backfill_test"


def check(req: str, what: str, condition: bool) -> None:
    (PASSES if condition else FAILURES).append(
        f"{'PASS' if condition else 'FAIL'}  {req} — {what}")


def build_database() -> None:
    import subprocess
    subprocess.run(["psql", "-q", "-c", f"DROP DATABASE IF EXISTS {DB}",
                    "-c", f"CREATE DATABASE {DB}", "postgres"],
                   check=True, capture_output=True)
    for sql in sorted((ROOT / "schema").glob("0*.sql")):
        subprocess.run(["psql", "-q", "-d", DB, "-v", "ON_ERROR_STOP=1", "-f", str(sql)],
                       check=True, capture_output=True)


class CountingFetcher:
    """A fixture fetcher that counts how many times each locator is fetched.

    Pages are keyed by their exact locator string (including `?before=`),
    each mapped to a small HTML fixture naming which post ids it carries.
    """

    def __init__(self, pages: dict[str, list[int]], channel: str):
        self.pages = pages
        self.channel = channel
        self.call_counts: dict[str, int] = {}

    def fetch(self, locator: str) -> FetchResult:
        self.call_counts[locator] = self.call_counts.get(locator, 0) + 1
        ids = self.pages.get(locator)
        if ids is None:
            return FetchResult(locator=locator, attempted_at=_now(),
                               outcome="not-found", error_detail="no fixture")
        html = "".join(f'<div data-post="{self.channel}/{i}"></div>' for i in ids)
        return FetchResult(
            locator=locator, attempted_at=_now(), outcome="success",
            content=html.encode(), media_type="text/html",
            response_headers={"Content-Type": "text/html"},
            http_status=200, http_reason="OK")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def run() -> int:
    # ---- pure parsing, no network, no database ---------------------------

    html = (
        '<div data-post="kpszsu/100"></div>'
        '<div data-post="kpszsu/101"></div>'
        '<div data-post="otherchannel/999"></div>'  # forwarded post — not ours
        '<div data-post="kpszsu/102"></div>'
    )
    check("§57", "extract_post_ids returns only this channel's ids, in file order",
          extract_post_ids(html, "kpszsu") == [100, 101, 102])
    check("§57", "extract_post_ids on a page with none returns empty, not an error",
          extract_post_ids("<div>nothing here</div>", "kpszsu") == [])

    # ---- CachingFetcher: the whole point of this module -------------------

    calls: list[str] = []

    class SpyFetcher:
        def fetch(self, locator: str) -> FetchResult:
            calls.append(locator)
            return FetchResult(locator=locator, attempted_at=_now(),
                               outcome="success", content=b"<div></div>",
                               media_type="text/html", http_status=200, http_reason="OK")

    caching = CachingFetcher(SpyFetcher())
    caching.prime("https://t.me/s/kpszsu")
    caching.fetch("https://t.me/s/kpszsu")
    check("DR-0067", "priming then fetching the same locator hits the network once",
          calls == ["https://t.me/s/kpszsu"])
    check("DR-0067", "a locator fetched (not primed) without a prior prime still works",
          caching.fetch("https://t.me/s/other").outcome == "success"
          and calls == ["https://t.me/s/kpszsu", "https://t.me/s/other"])

    # ---- backfill loop: three stopping points, and no others -------------

    build_database()
    conn = psycopg.connect(dbname=DB, autocommit=True)
    try:
        agent_id = str(uuid.uuid4())
        conn.execute("INSERT INTO pipeline_agent (id, kind, name) "
                     "VALUES (%s,'person','Test operator')", (agent_id,))
        source_id = str(uuid.uuid4())
        conn.execute(
            """INSERT INTO source (id, source_type, name, collection_method,
               default_retention_tier, default_access_tier, rights_permission)
               VALUES (%s,'telegram-channel','Test channel','http','permanent',
                       'public','may-preserve')""", (source_id,))
        software_agent_id = ensure_software_agent(conn)

        def make_collector(fetcher):
            work = Path(tempfile.mkdtemp(prefix="uiw-backfill-test-"))
            roots = {"permanent": StorageRoot(work / "perm", "permanent"),
                     "medium-term": StorageRoot(work / "med", "medium-term")}
            for r in roots.values():
                r.initialize()
            return Collector(conn, fetcher, work / "q", roots, agent_id, software_agent_id)

        base = "https://t.me/s/testch"

        # Stop 1: bottom of history (a page with no ids).
        pages = {
            base: [300, 299, 298],
            f"{base}?before=298": [297, 296],
            f"{base}?before=296": [],  # nothing earlier — bottom
        }
        fetcher = CountingFetcher(pages, "testch")
        caching = CachingFetcher(fetcher)
        collector = make_collector(caching)
        stats = backfill(collector, source_id, base, "testch",
                         delay=0, fetcher=caching, sleeper=lambda s: None)
        check("§57", "backfill stops at the bottom of history, not before",
              "bottom of history" in stats.stopped_because
              and stats.pages_preserved == 2 and stats.earliest_id_seen == 296)
        check("DR-0067", "every preserved page's locator was fetched exactly once",
              all(c == 1 for loc, c in fetcher.call_counts.items()
                  if loc != f"{base}?before=296"))

        source_id = str(uuid.uuid4())
        conn.execute(
            """INSERT INTO source (id, source_type, name, collection_method,
               default_retention_tier, default_access_tier, rights_permission)
               VALUES (%s,'telegram-channel','Test channel 2','http','permanent',
                       'public','may-preserve')""", (source_id,))

        # Stop 2: stop_before_id reached.
        pages2 = {
            base: [300, 299, 298],
            f"{base}?before=298": [297, 296, 295],
        }
        fetcher2 = CountingFetcher(pages2, "testch")
        caching2 = CachingFetcher(fetcher2)
        collector2 = make_collector(caching2)
        stats2 = backfill(collector2, source_id, base, "testch",
                          stop_before_id=296, delay=0, fetcher=caching2,
                          sleeper=lambda s: None)
        check("§57", "backfill stops once stop_before_id is reached, preserving that page",
              "stop-before-id" in stats2.stopped_because
              and stats2.pages_preserved == 2 and stats2.earliest_id_seen == 295)

        source_id = str(uuid.uuid4())
        conn.execute(
            """INSERT INTO source (id, source_type, name, collection_method,
               default_retention_tier, default_access_tier, rights_permission)
               VALUES (%s,'telegram-channel','Test channel 3','http','permanent',
                       'public','may-preserve')""", (source_id,))

        # Stop 3: max_pages reached (a safety bound, not history-driven).
        pages3 = {
            base: [300, 299],
            f"{base}?before=299": [298, 297],
            f"{base}?before=297": [296, 295],
        }
        fetcher3 = CountingFetcher(pages3, "testch")
        caching3 = CachingFetcher(fetcher3)
        collector3 = make_collector(caching3)
        stats3 = backfill(collector3, source_id, base, "testch",
                          max_pages=1, delay=0, fetcher=caching3, sleeper=lambda s: None)
        check("§57", "backfill stops at max_pages even with more history available",
              "max-pages" in stats3.stopped_because and stats3.pages_preserved == 1
              and stats3.pages_attempted == 1)

        source_id = str(uuid.uuid4())
        conn.execute(
            """INSERT INTO source (id, source_type, name, collection_method,
               default_retention_tier, default_access_tier, rights_permission)
               VALUES (%s,'telegram-channel','Test channel 4','http','permanent',
                       'public','may-preserve')""", (source_id,))

        # A failed page stops the loop and says where to resume, rather than
        # retrying forever against a host that may be actively blocking it.
        pages4 = {base: [300, 299]}  # ?before=299 deliberately has no fixture -> not-found
        fetcher4 = CountingFetcher(pages4, "testch")
        caching4 = CachingFetcher(fetcher4)
        collector4 = make_collector(caching4)
        stats4 = backfill(collector4, source_id, base, "testch",
                          delay=0, fetcher=caching4, sleeper=lambda s: None)
        check("PRES-007", "a failed page fetch stops the loop and names where to resume",
              stats4.pages_failed == 1 and stats4.pages_preserved == 1
              and "resume later with --start-before 299" in stats4.stopped_because)

        # Zero documentary assertions, same as every other collector path.
        check("DR-0066", "backfill runs create no documentary assertions",
              not any(
                  conn.execute(f"SELECT 1 FROM {t} LIMIT 1").fetchone()
                  for t in ("documentary_assertion",)
              ))
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
        return 1


if __name__ == "__main__":
    sys.exit(main())
