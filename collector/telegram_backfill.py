#!/usr/bin/env python3
"""Backfill a registered Telegram channel's public-preview history.

    python3 collector/telegram_backfill.py --source kpszsu --dbname uiw \\
            --agent <pipeline_agent uuid> --archive-root /opt/uiw-archive \\
            --channel kpszsu --delay 3.0

CDR-pending-telegram-backfill (candidate — see docs/sources/
verification-strike-tracking-first-two.md §2). A registered source's
`run_locators` normally names a fixed set of stable URLs, fetched fresh each
run. A Telegram public-preview channel (`t.me/s/<channel>`) has no such
locator for its history: the page shows only the newest ~20-30 posts, and
the only way to reach an earlier one is `?before=<message_id>` pagination,
discovered one page at a time. This script walks that pagination backward,
preserving each page through the same `Collector.run()` path every other
source uses (DR-0006/DR-0067's capture-format honouring, storage-first
writes at §26, zero documentary assertions at DR-0066) — nothing here
reads or interprets the content, it only walks and preserves pages.

It makes exactly ONE network request per page: `CachingFetcher` wraps the
real fetcher, is called directly first (so this script can parse the page
for the next `before=` id), and `Collector.run()`'s own internal fetch for
the same locator is served from that cache rather than hitting the network
again. This matters because the whole reason this script exists is a
channel with tens of thousands of posts — doubling the request count would
double the exposure to Telegram's own rate limiting, which lands on
whatever host this runs from (see the verification record's warnings on
this specific point).

`--delay` between pages is the caller's responsibility (HttpFetcher's own
docstring: "politeness and rate limits are per-source policy... and belong
to the caller"), same as everywhere else in this codebase — a positive
default is set here because getting the archive server's IP rate-limited
or blocked by Telegram is a real, named risk, not a hypothetical one, and
it would affect every OTHER source's daily collection too.

What this does NOT do: guarantee completeness. It stops when a page
returns no post ids (nothing earlier is discoverable) or a fetch fails
outright; either way it prints exactly where it stopped so a resumed run
(`--start-before <id>`) picks up cleanly. It does not retry a failed page
automatically — a systematic failure (e.g. a block) should surface, not be
silently absorbed into more requests against a host that is already
refusing them.
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

import psycopg

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "collector"))
sys.path.insert(0, str(ROOT / "storage"))
sys.path.insert(0, str(ROOT / "sources"))

from fetch import Fetcher, FetchResult, HttpFetcher  # noqa: E402
from pipeline import Collector, ensure_software_agent  # noqa: E402
from run import (  # noqa: E402
    DEFAULT_USER_AGENT, Refused, check_agent, find_candidate, git_commit,
    open_roots, resolve_registered_source,
)

# t.me's public preview labels each message with data-post="<channel>/<id>".
_POST_ID_RE = re.compile(r'data-post="(?P<channel>[^/"]+)/(?P<id>\d+)"')


def extract_post_ids(html: bytes | str, channel: str) -> list[int]:
    """Every message id on this preview page, for the given channel.

    Ignores ids for other channels — the preview occasionally embeds a
    forwarded-from post's own `data-post`, which is not this channel's
    history and must not be mistaken for it.
    """
    text = html.decode("utf-8", errors="replace") if isinstance(html, bytes) else html
    return [int(m.group("id")) for m in _POST_ID_RE.finditer(text)
            if m.group("channel") == channel]


class CachingFetcher:
    """Wraps a real `Fetcher`, remembering the last result per locator.

    Not a general-purpose cache — one entry is all this script ever needs,
    since each locator is fetched exactly once (directly, to parse) and
    then reused exactly once (by `Collector.run()`, to preserve). A second
    `.fetch()` of a locator NOT already cached still hits the network; this
    only stops the specific double-fetch this script would otherwise cause.
    """

    def __init__(self, inner: Fetcher):
        self.inner = inner
        self._cache: dict[str, FetchResult] = {}

    def fetch(self, locator: str) -> FetchResult:
        if locator in self._cache:
            return self._cache.pop(locator)
        result = self.inner.fetch(locator)
        self._cache[locator] = result
        return result

    def prime(self, locator: str) -> FetchResult:
        """Fetch and cache now, returning the result for this script to parse."""
        result = self.inner.fetch(locator)
        self._cache[locator] = result
        return result


@dataclass
class BackfillStats:
    pages_attempted: int = 0
    pages_preserved: int = 0
    pages_failed: int = 0
    earliest_id_seen: int | None = None
    stopped_because: str = ""
    run_ids: list[str] = field(default_factory=list)


def backfill(
    collector: Collector,
    source_id: str,
    base_url: str,
    channel: str,
    *,
    start_before: int | None = None,
    stop_before_id: int | None = None,
    max_pages: int | None = None,
    delay: float = 3.0,
    fetcher: CachingFetcher,
    sleeper=time.sleep,
) -> BackfillStats:
    """Walk `base_url`'s pagination backward, preserving each page.

    `stop_before_id`, if given, is exclusive: paging stops once a page's
    earliest id is at or below it — the point where a prior backfill run
    already covered history, so this run's job is only what is newer than
    that. `start_before`, if given, is where paging begins (the page
    showing posts just before that id) rather than the channel's live head.
    """
    stats = BackfillStats()
    before = start_before

    while True:
        if max_pages is not None and stats.pages_attempted >= max_pages:
            stats.stopped_because = f"reached --max-pages {max_pages}"
            break

        locator = base_url if before is None else f"{base_url}?before={before}"
        stats.pages_attempted += 1
        result = fetcher.prime(locator)

        if result.outcome != "success":
            stats.pages_failed += 1
            stats.stopped_because = (
                f"page fetch failed ({result.outcome}: {result.error_detail}) "
                f"at locator {locator!r} -- resume later with "
                f"--start-before {before if before is not None else '<omit, channel head>'}"
            )
            break

        ids = extract_post_ids(result.content or b"", channel)
        if not ids:
            stats.stopped_because = f"no post ids found on {locator!r} -- bottom of history"
            break

        earliest = min(ids)
        if stats.earliest_id_seen is None or earliest < stats.earliest_id_seen:
            stats.earliest_id_seen = earliest

        run_id = collector.run(source_id, [locator], configuration={
            "invoked_by": "collector/telegram_backfill.py",
            "channel": channel,
            "page_before": before,
        })
        stats.run_ids.append(run_id)
        stats.pages_preserved += 1

        if stop_before_id is not None and earliest <= stop_before_id:
            stats.stopped_because = (
                f"reached --stop-before-id {stop_before_id} "
                f"(page's earliest id {earliest})"
            )
            break

        before = earliest
        sleeper(delay)

    return stats


# -- CLI ----------------------------------------------------------------

def main(argv: list[str] | None = None, fetcher: Fetcher | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", required=True, metavar="KEY",
                        help="candidate key, e.g. kpszsu")
    parser.add_argument("--channel", required=True,
                        help="the Telegram channel name as it appears in "
                             "t.me URLs and data-post attributes, e.g. kpszsu")
    parser.add_argument("--dbname", required=True)
    parser.add_argument("--agent", required=True, metavar="UUID")
    parser.add_argument("--archive-root", required=True, type=Path)
    parser.add_argument("--start-before", type=int, default=None,
                        help="message id to page backward from; omit to "
                             "start at the channel's current live head")
    parser.add_argument("--stop-before-id", type=int, default=None,
                        help="stop once a page's earliest id reaches this "
                             "(use the earliest id a prior backfill reached, "
                             "printed at that run's end, to resume cleanly "
                             "without re-walking already-covered history)")
    parser.add_argument("--max-pages", type=int, default=None,
                        help="stop after this many pages regardless -- a "
                             "safety bound for a first, cautious run")
    parser.add_argument("--delay", type=float, default=3.0,
                        help="seconds to wait between page fetches (politeness "
                             "and rate-limit risk are real here -- see module "
                             "docstring)")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--dry-run", action="store_true",
                        help="check registration and agent, discover the "
                             "channel's current head, fetch and preserve "
                             "nothing")
    args = parser.parse_args(argv)

    try:
        candidate = find_candidate(args.source)
        with psycopg.connect(dbname=args.dbname, autocommit=True) as conn:
            source_id, state = resolve_registered_source(conn, candidate)
            agent_kind, agent_name = check_agent(conn, args.agent, allow_software=False)
            if state != "active":
                raise Refused(f"{args.source} is registered but {state}; a "
                              f"{state} source does not collect (DR-0067)")

            # find_candidate() already refuses a candidate with no
            # run_locators; the first one is the live-head form to page
            # backward from (candidate authors are expected to list the
            # bare channel URL first, not a pre-paginated one).
            base_url = candidate["run_locators"][0].split("?")[0]

            print(f"source     {args.source}  ({source_id})")
            print(f"agent      {agent_name}  [{agent_kind}]  {args.agent}")
            print(f"channel    {args.channel}")
            print(f"base url   {base_url}")
            print(f"delay      {args.delay}s between pages")

            if args.dry_run:
                print("\ndry run: nothing fetched, nothing written")
                return 0

            roots, quarantine = open_roots(args.archive_root)
            software_agent_id = ensure_software_agent(conn)
            real_fetcher = fetcher or HttpFetcher(args.user_agent, timeout=args.timeout)
            caching_fetcher = CachingFetcher(real_fetcher)
            collector = Collector(conn, caching_fetcher, quarantine, roots,
                                  args.agent, software_agent_id)

            stats = backfill(
                collector, source_id, base_url, args.channel,
                start_before=args.start_before,
                stop_before_id=args.stop_before_id,
                max_pages=args.max_pages,
                delay=args.delay,
                fetcher=caching_fetcher,
            )

            print(f"\npages attempted {stats.pages_attempted}  "
                  f"preserved {stats.pages_preserved}  failed {stats.pages_failed}")
            print(f"earliest id seen: {stats.earliest_id_seen}")
            print(f"stopped because: {stats.stopped_because}")
            print(f"runs: {', '.join(stats.run_ids) or '(none)'}")
            if stats.earliest_id_seen is not None:
                print(f"\nto resume from here later: --stop-before-id "
                      f"{stats.earliest_id_seen}")
            return 1 if stats.pages_failed and not stats.pages_preserved else 0

    except Refused as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
