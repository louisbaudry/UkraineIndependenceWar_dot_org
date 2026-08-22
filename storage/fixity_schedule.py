#!/usr/bin/env python3
"""Periodic fixity checking.

Implements PRES-003 — "periodic fixity checks are performed and recorded as
events with outcomes" — which DR-0005 required and left without a cadence.

The cadence is defined here rather than in a scheduler's configuration, so
that it is part of the specified system rather than an operational accident:

    permanent tier      every 180 days
    medium-term tier    every 365 days

Rationale. A fixity check costs a full read of the archive, so cadence trades
detection latency against I/O. Twice-yearly for permanently preserved
material bounds the worst case at six months between corruption and its
discovery, while independent backups (OPS-005) cover the interval. Material
held medium-term is by definition awaiting a retention decision and carries
less weight, so annually suffices.

**A failure is recorded, never repaired.** DR-0060 makes the outcome an
event; a silent re-copy from backup would erase the evidence that something
went wrong, which is exactly what a preservation record exists to retain.

Usage:
  python3 storage/fixity_schedule.py --due            # what is overdue
  python3 storage/fixity_schedule.py --run [--limit N]
"""

from __future__ import annotations

import argparse
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

import psycopg

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ocfl import StorageRoot  # noqa: E402

CADENCE_DAYS = {"permanent": 180, "medium-term": 365}


def due_objects(conn: psycopg.Connection, now: datetime | None = None) -> list[tuple]:
    """Objects whose last successful fixity check is older than their cadence.

    An object never checked is due immediately: 'never verified' and 'verified
    long ago' are different states, and the first is the more urgent.
    """
    now = now or datetime.now(timezone.utc)
    rows = []
    for tier, days in CADENCE_DAYS.items():
        cutoff = now - timedelta(days=days)
        rows.extend(conn.execute(
            """
            SELECT o.id, o.ocfl_root, o.ocfl_object_id, last.checked_at
              FROM preserved_object o
              LEFT JOIN LATERAL (
                    SELECT max(e.occurred_at) AS checked_at
                      FROM preservation_event e
                     WHERE e.object_id = o.id
                       AND e.event_type = 'fixity-check'
                       AND e.outcome = 'success'
                   ) last ON true
             WHERE o.ocfl_root = %s
               AND (last.checked_at IS NULL OR last.checked_at < %s)
             ORDER BY last.checked_at NULLS FIRST, o.ingested_at
            """,
            (tier, cutoff),
        ).fetchall())
    return rows


def run_checks(
    conn: psycopg.Connection,
    roots: dict[str, StorageRoot],
    agent_id: str,
    limit: int | None = None,
) -> dict:
    """Check due objects and record an event for each — pass or fail."""
    due = due_objects(conn)
    if limit is not None:
        due = due[:limit]

    summary = {"checked": 0, "passed": 0, "failed": 0, "problems": []}

    for object_id, tier, ocfl_object_id, _last in due:
        root = roots.get(tier)
        if root is None:
            summary["problems"].append(
                f"{ocfl_object_id}: no storage root configured for tier {tier!r}"
            )
            continue

        problems = root.fixity_check(ocfl_object_id)
        outcome = "success" if not problems else "failure"
        detail = (
            f"verified against sha512 content addresses and the sha256 fixity block"
            if not problems
            else "; ".join(problems[:5])
        )

        conn.execute(
            """
            INSERT INTO preservation_event
                (id, event_type, object_id, agent_id, occurred_at, outcome,
                 outcome_detail)
            VALUES (%s, 'fixity-check', %s, %s, %s, %s, %s)
            """,
            (str(uuid.uuid4()), object_id, agent_id,
             datetime.now(timezone.utc), outcome, detail),
        )

        summary["checked"] += 1
        if problems:
            summary["failed"] += 1
            summary["problems"].append(f"{ocfl_object_id}: {detail}")
        else:
            summary["passed"] += 1

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dbname")
    parser.add_argument("--permanent-root", type=Path)
    parser.add_argument("--medium-term-root", type=Path)
    parser.add_argument("--due", action="store_true", help="list what is overdue")
    parser.add_argument("--run", action="store_true", help="check and record")
    parser.add_argument("--agent-id", help="pipeline agent performing the check")
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    conn = psycopg.connect(dbname=args.dbname) if args.dbname else psycopg.connect()
    conn.autocommit = True

    if args.due or not args.run:
        due = due_objects(conn)
        for _oid, tier, ocfl_id, last in due:
            when = last.isoformat(timespec="seconds") if last else "never"
            print(f"  {tier:<12} {ocfl_id}  last verified: {when}")
        print(f"{len(due)} object(s) due for fixity check")
        return 0

    roots = {}
    if args.permanent_root:
        roots["permanent"] = StorageRoot(args.permanent_root, "permanent")
    if args.medium_term_root:
        roots["medium-term"] = StorageRoot(args.medium_term_root, "medium-term")
    if not args.agent_id:
        parser.error("--run requires --agent-id")

    summary = run_checks(conn, roots, args.agent_id, args.limit)
    print(f"checked {summary['checked']}: "
          f"{summary['passed']} passed, {summary['failed']} failed")
    for problem in summary["problems"]:
        print(f"  {problem}")
    # A failure is a recorded event and an operational alarm, not a crash.
    return 1 if summary["failed"] or summary["problems"] else 0


if __name__ == "__main__":
    sys.exit(main())
