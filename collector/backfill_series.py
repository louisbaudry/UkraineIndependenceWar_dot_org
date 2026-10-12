#!/usr/bin/env python3
"""Give holdings that predate the capture series a series row (issue #75).

DR-0074 relates successive captures of one locator through
`capture_series_member`. `Collector._admit()` has written a row for every
admission since 2026-09-10; the holdings admitted on 2026-09-09 predate that
and have none, so the next capture of either locator starts a new series that
does not include them (`collector/README.md`). This links each such holding
into the series `_admit()` would have put it in: the deterministic
`capture_series_id(source_id, locator)`, with the same `captured_at`
(`original_captured_at` for a recovered capture, else `attempted_at`).

    python3 collector/backfill_series.py --dbname uiw            # plan, writes nothing
    python3 collector/backfill_series.py --dbname uiw --commit   # write it

How a holding is traced back to a source: its original representation's
`original_name` is the locator it was admitted from, and the
`acquisition_attempt` rows with outcome `success` for that locator say which
source acquired it and when. If a locator has no such attempt, or successful
attempts under more than one source, the holding is **reported and nothing is
written at all**: guessing a series for a preserved holding would make the
archive's record wrong in a way nobody would see.

Only holdings with no series row are touched, so it is safe to run twice and
it does nothing once the gap is closed. It writes only to
`capture_series_member`; it creates no holding, object or assertion (DR-0066).
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

import psycopg

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "collector"))
sys.path.insert(0, str(ROOT / "storage"))

from pipeline import capture_series_id  # noqa: E402


@dataclass
class Link:
    holding_id: str
    source_id: str
    locator: str
    captured_at: object


def plan(conn: psycopg.Connection) -> tuple[list[Link], list[str]]:
    """Work out the rows to write and the holdings that cannot be placed."""
    holdings = conn.execute(
        """
        SELECT h.id, po.original_name, po.ingested_at
          FROM holding h
          JOIN holding_representation hr ON hr.holding_id = h.id AND hr.role = 'original'
          JOIN preserved_object po ON po.id = hr.object_id
         WHERE NOT EXISTS (SELECT 1 FROM capture_series_member m WHERE m.holding_id = h.id)
         ORDER BY po.ingested_at, h.id
        """
    ).fetchall()
    links: list[Link] = []
    problems: list[str] = []
    for holding_id, locator, ingested_at in holdings:
        attempts = conn.execute(
            """
            SELECT source_id, attempted_at, original_captured_at
              FROM acquisition_attempt
             WHERE locator = %s AND outcome = 'success'
            """,
            (locator,),
        ).fetchall()
        sources = {a[0] for a in attempts}
        if not attempts:
            problems.append(f"holding {holding_id}: no successful acquisition_attempt "
                            f"records locator {locator!r}")
            continue
        if len(sources) > 1:
            problems.append(f"holding {holding_id}: locator {locator!r} was acquired "
                            f"under {len(sources)} different sources; cannot tell which")
            continue
        # The attempt closest to when the holding was admitted: a locator
        # captured more than once has several, and the admission follows its
        # own attempt by moments.
        source_id, attempted_at, original = min(
            attempts, key=lambda a: abs((a[1] - ingested_at).total_seconds()))
        links.append(Link(str(holding_id), str(source_id), locator,
                          original or attempted_at))
    return links, problems


def apply(conn: psycopg.Connection, links: list[Link]) -> None:
    """Write the rows in one transaction, keyed exactly as `_admit()` keys them."""
    with conn.transaction():
        for link in links:
            conn.execute(
                "INSERT INTO capture_series_member (series_id, holding_id, locator, captured_at) "
                "VALUES (%s, %s, %s, %s)",
                (capture_series_id(link.source_id, link.locator), link.holding_id,
                 link.locator, link.captured_at),
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--dbname", required=True)
    parser.add_argument("--commit", action="store_true",
                        help="write the rows; without it nothing is written")
    args = parser.parse_args(argv)
    with psycopg.connect(dbname=args.dbname, autocommit=True) as conn:
        links, problems = plan(conn)
        print(f"{len(links)} holding(s) would be linked into a series, "
              f"{len(problems)} cannot be placed")
        for link in links:
            print(f"  holding {link.holding_id}  series "
                  f"{capture_series_id(link.source_id, link.locator)}  "
                  f"captured {link.captured_at}  {link.locator}")
        for problem in problems:
            print(f"  CANNOT PLACE: {problem}", file=sys.stderr)
        if problems:
            print("refused: nothing written while any holding cannot be placed",
                  file=sys.stderr)
            return 2
        if not args.commit:
            print("plan only: nothing written (pass --commit to write)")
            return 0
        apply(conn, links)
        print(f"wrote {len(links)} capture_series_member row(s)")
        return 0


if __name__ == "__main__":
    sys.exit(main())
