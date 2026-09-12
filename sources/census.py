#!/usr/bin/env python3
"""Census tooling: discover candidate domains from index services' own
records, without fetching a byte of the candidate domain itself.

Implements WP 3.4 (Foundational Corpus Acquisition Strategy) §4.1, Track A
item A2 — permitted now under DR-0071 because nothing here collects from an
unregistered host: it queries an index service's own API (Common Crawl's
crawl index, the Internet Archive's Wayback CDX index) about what that
service has already captured, and never contacts the candidate domain
itself. CDR-P3-33 (candidate) reserves an actual fetch of a candidate page
— "home, about, a sample" — for Track B's B1 wave, gated on the recorded
POL-0001 §10 review; this module makes no such fetch, and touches no
database (there is nothing here for DR-0071(a)'s registered-sources rule to
apply to, because nothing is collected or stored).

What this produces: a ranked, deduplicated list of hosts an index service
has captured under a domain pattern, each with the evidence for it (which
index, how many captures, first/last seen) — never the captured content.
WP 3.4 §4.1 describes the next step as a queue of *prose* candidate notes
under docs/sources/ (see docs/sources/candidate-war-sanctions-gur.md for the
shape one takes); this tool produces the ranked list that queue starts
from, not the notes themselves.

Only the two evidence sources WP 3.4 §4.1 calls "indices" are built here
(Common Crawl's crawl index, the Wayback Machine's CDX index). The other
four it names — Wikipedia citation graphs, sanctions-authority link graphs,
published OSINT source lists, academic bibliographies — are editorial
research tasks with no stable query API, not tooling, and are left for
separate work.

See sources/README.md on what has and has not been verified against a live
index in this environment (WP 3.4 §3: this tooling is meant to be built and
tested here, then run where a session has the network access this one does
not).

Run:  python3 sources/census.py --domain example.gov.ua --index wayback
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol
from urllib.parse import urlsplit

DEFAULT_USER_AGENT = (
    "UIW-census/0.1 "
    "(+https://github.com/louisbaudry/UkraineIndependenceWar_dot_org)"
)  # CDR-P3-34 (candidate): a stable User-Agent naming the project


@dataclass(frozen=True)
class IndexRecord:
    """One capture an index service reports for one URL.

    Deliberately thin: a census is evidence that something was captured, not
    the capture itself. No payload, no digest — retrieving either is a
    later, per-source, per-locator decision (DR-0094), not a census's job.
    """

    url: str
    timestamp: datetime | None
    status: str | None = None  # the index's own reported HTTP status, if any


@dataclass(frozen=True)
class IndexQueryResult:
    """The outcome of asking one index service about one domain pattern.

    A failure is as much a result as a success — the same discipline §28 and
    PRES-007 give a failed acquisition, applied to a non-archival query: an
    index service being unreachable is itself worth recording, not silently
    skipped.
    """

    index_name: str
    domain_pattern: str
    outcome: str  # 'success' | 'failure'
    records: tuple[IndexRecord, ...] = ()
    error_detail: str | None = None

    def __post_init__(self) -> None:
        if self.outcome != "success" and not self.error_detail:
            raise ValueError("a failed index query must explain itself (§28)")


class IndexClient(Protocol):
    """How the census queries one index service. The seam that keeps the
    network out of everything downstream — the same pattern as
    collector/fetch.py's `Fetcher`.
    """

    name: str

    def query(self, domain_pattern: str) -> IndexQueryResult: ...


@dataclass(frozen=True)
class CensusEntry:
    """One discovered host, ranked, with the evidence for it."""

    host: str
    total_captures: int
    first_seen: datetime | None
    last_seen: datetime | None
    seen_by: tuple[str, ...]  # index names that reported this host


def _host_of(url: str) -> str:
    return urlsplit(url).netloc.lower()


def census(
    domain_pattern: str, clients: list[IndexClient],
) -> tuple[list[CensusEntry], list[IndexQueryResult]]:
    """Queries every client for `domain_pattern` and returns a ranked,
    deduplicated list of hosts, alongside the raw per-client results — so a
    caller can see which queries failed and why (§28), not just what
    succeeded.

    Ranking is by total capture count across every index that reported a
    host, descending. This is the crudest honest signal a census has: a host
    with many captures across two independent indexes is not more *true* for
    it, only better attested — the DR-0027 triage-only distinction, applied
    here to domain discovery instead of source grading.
    """
    results = [client.query(domain_pattern) for client in clients]

    by_host: dict[str, dict] = {}
    for result in results:
        if result.outcome != "success":
            continue
        for record in result.records:
            host = _host_of(record.url)
            if not host:
                continue
            entry = by_host.setdefault(host, {
                "total_captures": 0, "first_seen": None, "last_seen": None,
                "seen_by": set(),
            })
            entry["total_captures"] += 1
            entry["seen_by"].add(result.index_name)
            if record.timestamp is not None:
                if entry["first_seen"] is None or record.timestamp < entry["first_seen"]:
                    entry["first_seen"] = record.timestamp
                if entry["last_seen"] is None or record.timestamp > entry["last_seen"]:
                    entry["last_seen"] = record.timestamp

    entries = [
        CensusEntry(
            host=host,
            total_captures=data["total_captures"],
            first_seen=data["first_seen"],
            last_seen=data["last_seen"],
            seen_by=tuple(sorted(data["seen_by"])),
        )
        for host, data in by_host.items()
    ]
    entries.sort(key=lambda e: (-e.total_captures, e.host))
    return entries, results


def format_report(
    domain_pattern: str, entries: list[CensusEntry], results: list[IndexQueryResult],
) -> str:
    """Renders the ranked list as markdown — WP 3.4 §4.1's 'ranked list of
    candidate domains with the evidence for each'."""
    lines = [f"# Census: `{domain_pattern}`", ""]
    failed = [r for r in results if r.outcome != "success"]
    if failed:
        lines.append("**Some index queries failed and are not reflected below:**")
        for r in failed:
            lines.append(f"- {r.index_name}: {r.error_detail}")
        lines.append("")
    if not entries:
        lines.append("No hosts discovered.")
        return "\n".join(lines)
    lines.append("| Host | Captures | First seen | Last seen | Seen by |")
    lines.append("|---|---|---|---|---|")
    for e in entries:
        first = e.first_seen.date().isoformat() if e.first_seen else "—"
        last = e.last_seen.date().isoformat() if e.last_seen else "—"
        lines.append(f"| {e.host} | {e.total_captures} | {first} | {last} | "
                     f"{', '.join(e.seen_by)} |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Test double
# ---------------------------------------------------------------------------


class FixtureIndexClient:
    """Serves recorded results. Used by the test suite; also usable to
    replay a saved real response without re-querying a live index.
    """

    def __init__(self, name: str, fixtures: dict[str, IndexQueryResult]):
        self.name = name
        self.fixtures = fixtures
        self.queries: list[str] = []

    def query(self, domain_pattern: str) -> IndexQueryResult:
        self.queries.append(domain_pattern)
        result = self.fixtures.get(domain_pattern)
        if result is None:
            return IndexQueryResult(
                index_name=self.name, domain_pattern=domain_pattern,
                outcome="failure",
                error_detail="no fixture registered for this pattern",
            )
        return result


# ---------------------------------------------------------------------------
# Real clients — UNVERIFIED IN THIS BUILD
# ---------------------------------------------------------------------------
#
# Both were reproducibly unreachable from this session: index.commoncrawl.org
# reset the connection on every attempt (collinfo.json and a direct index
# query alike; see the agent proxy's recentRelayFailures), and
# web.archive.org timed out outright — the same host DR-0094's drafting
# session and this project's earlier verification record both found blocked.
# Written to the documented API shape below, not exercised against a live
# response. See sources/README.md.


def _parse_cc_timestamp(raw: str | None) -> datetime | None:
    """Common Crawl and Wayback both use a bare YYYYMMDDHHMMSS timestamp."""
    if not raw:
        return None
    try:
        return datetime.strptime(raw, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _parse_cc_index(body: str) -> list[IndexRecord]:
    """Common Crawl's index server returns one JSON object per line."""
    records = []
    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        url = row.get("url")
        if not url:
            continue
        records.append(IndexRecord(
            url=url, timestamp=_parse_cc_timestamp(row.get("timestamp")),
            status=row.get("status"),
        ))
    return records


class CommonCrawlIndexClient:
    """Queries one Common Crawl monthly index (e.g. CC-MAIN-2024-46) via its
    CDX-style index server. UNVERIFIED IN THIS BUILD — see module docstring.

    A specific `crawl_id` is required rather than resolved automatically
    from `collinfo.json`, to keep one query deterministic and testable
    instead of two chained ones; the current id is listed at
    https://index.commoncrawl.org/collinfo.json.
    """

    def __init__(
        self, crawl_id: str, user_agent: str = DEFAULT_USER_AGENT,
        timeout: float = 30.0, base_url: str = "https://index.commoncrawl.org",
    ):
        self.crawl_id = crawl_id
        self.user_agent = user_agent
        self.timeout = timeout
        self.base_url = base_url.rstrip("/")
        self.name = "common-crawl"

    def query(self, domain_pattern: str) -> IndexQueryResult:
        import urllib.error
        import urllib.parse
        import urllib.request

        url = (f"{self.base_url}/{self.crawl_id}-index?"
               + urllib.parse.urlencode({
                   "url": domain_pattern, "output": "json", "matchType": "domain",
               }))
        request = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = response.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            return IndexQueryResult(
                index_name=self.name, domain_pattern=domain_pattern,
                outcome="failure", error_detail=f"HTTP {exc.code}: {exc.reason}")
        except Exception as exc:  # noqa: BLE001 — every failure is recordable
            return IndexQueryResult(
                index_name=self.name, domain_pattern=domain_pattern,
                outcome="failure", error_detail=f"{type(exc).__name__}: {exc}")
        return IndexQueryResult(
            index_name=self.name, domain_pattern=domain_pattern,
            outcome="success", records=tuple(_parse_cc_index(body)))


def _parse_wayback_rows(rows: list) -> list[IndexRecord]:
    """The Wayback CDX API returns a JSON array of arrays, header row first."""
    if not rows:
        return []
    header, *data = rows
    try:
        url_i = header.index("original")
        ts_i = header.index("timestamp")
    except ValueError:
        return []
    status_i = header.index("statuscode") if "statuscode" in header else None
    records = []
    for row in data:
        if len(row) <= max(url_i, ts_i):
            continue
        status = row[status_i] if status_i is not None and status_i < len(row) else None
        records.append(IndexRecord(
            url=row[url_i], timestamp=_parse_cc_timestamp(row[ts_i]), status=status))
    return records


class WaybackCdxClient:
    """Queries the Internet Archive's Wayback CDX Server API.
    UNVERIFIED IN THIS BUILD — see module docstring.
    """

    def __init__(
        self, user_agent: str = DEFAULT_USER_AGENT, timeout: float = 30.0,
        base_url: str = "https://web.archive.org/cdx/search/cdx",
    ):
        self.user_agent = user_agent
        self.timeout = timeout
        self.base_url = base_url
        self.name = "wayback"

    def query(self, domain_pattern: str) -> IndexQueryResult:
        import urllib.error
        import urllib.parse
        import urllib.request

        url = self.base_url + "?" + urllib.parse.urlencode({
            "url": domain_pattern, "matchType": "domain", "output": "json",
            "collapse": "urlkey",
        })
        request = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = response.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            return IndexQueryResult(
                index_name=self.name, domain_pattern=domain_pattern,
                outcome="failure", error_detail=f"HTTP {exc.code}: {exc.reason}")
        except Exception as exc:  # noqa: BLE001
            return IndexQueryResult(
                index_name=self.name, domain_pattern=domain_pattern,
                outcome="failure", error_detail=f"{type(exc).__name__}: {exc}")
        try:
            rows = json.loads(body)
        except json.JSONDecodeError as exc:
            return IndexQueryResult(
                index_name=self.name, domain_pattern=domain_pattern,
                outcome="failure", error_detail=f"unparseable response: {exc}")
        return IndexQueryResult(
            index_name=self.name, domain_pattern=domain_pattern,
            outcome="success", records=tuple(_parse_wayback_rows(rows)))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

KNOWN_INDEXES = ("common-crawl", "wayback")


def main(
    argv: list[str] | None = None, clients: list[IndexClient] | None = None,
) -> int:
    """`clients`, if given, replaces the real clients `--index`/`--crawl-id`
    would build — the same test-injection seam `collector/run.py`'s `main`
    gives its `fetcher` argument. Argument validation (unknown index name,
    missing `--crawl-id`) still runs either way, since it happens before any
    client is ever constructed or queried.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--domain", required=True, metavar="PATTERN",
                        help="domain pattern to query, e.g. example.gov.ua")
    parser.add_argument("--index", default="common-crawl,wayback",
                        help=f"comma-separated index names ({', '.join(KNOWN_INDEXES)}); "
                             "default both")
    parser.add_argument("--crawl-id", default=None, metavar="ID",
                        help="Common Crawl crawl id, e.g. CC-MAIN-2024-46 "
                             "(required if querying common-crawl; current id at "
                             "https://index.commoncrawl.org/collinfo.json)")
    parser.add_argument("--out", type=Path, default=None,
                        help="write the report here instead of stdout")
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args(argv)

    requested = [name.strip() for name in args.index.split(",") if name.strip()]
    unknown = [name for name in requested if name not in KNOWN_INDEXES]
    if unknown:
        print(f"refused: unknown index {unknown!r}; known: {', '.join(KNOWN_INDEXES)}",
              file=sys.stderr)
        return 2

    if clients is None:
        clients = []
        for name in requested:
            if name == "common-crawl":
                if not args.crawl_id:
                    print("refused: --crawl-id is required to query common-crawl "
                          "(e.g. --crawl-id CC-MAIN-2024-46; see "
                          "https://index.commoncrawl.org/collinfo.json for the current one)",
                          file=sys.stderr)
                    return 2
                clients.append(CommonCrawlIndexClient(args.crawl_id, timeout=args.timeout))
            elif name == "wayback":
                clients.append(WaybackCdxClient(timeout=args.timeout))

    entries, results = census(args.domain, clients)
    report = format_report(args.domain, entries, results)
    if args.out:
        args.out.write_text(report)
        print(f"wrote {args.out}")
    else:
        print(report)
    return 0 if any(r.outcome == "success" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
