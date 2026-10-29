#!/usr/bin/env python3
"""Record that a source's rights position has been legally reviewed (or withdraw it).

CDR-P3-45 (candidate) made `rights_review_state` a declared field and has
Gate 3 refuse any holding that is not `reviewed`. This is the one act that sets
it, as ruled on 2026-10-29 and recorded in DR-0117:

- **Per source, one attributed append-only record** (`rights_review`), written
  by `record_rights_review()` in the database. Only a person (§79); never
  software. The database refuses a review with no named written basis:
  counsel's advice, or a Decision Record that relies on it.
- **In the same act**, the source's existing holdings are marked reviewed and
  the record lists exactly which (`rights_review_holding`). Holdings admitted
  later inherit the source's state at admission, as before.
- **A withdrawal is its own record** and moves the same holdings back to
  `unreviewed`. Nothing is edited or deleted (§77).

    python3 publication/rights_review.py --dbname uiw --source-id <uuid> \\
        --action reviewed --agent <person uuid> \\
        --basis-kind counsel-advice --basis-reference "<the advice>"        # plan
    ... --commit                                                             # record it

How a source's holdings are found: a holding has no direct link to its source.
Its original representation's `original_name` is the locator it was captured
from, and the `acquisition_attempt` rows with outcome `success` for that locator
say which source acquired it. A holding is **covered** when exactly this source
did. A locator also acquired under another source is **ambiguous** and is left
out of a review (it stays unreviewed, the safe state) and reported; for a
withdrawal it is included, because over-withdrawing is the safe error. A holding
with no traceable acquisition is left alone and counted. The plan prints all
three, so a reviewer sees what the review does and does not reach.

Writes only `rights_review`, `rights_review_holding` and the review-state
columns, all through the database function. It creates no assertion (DR-0066).
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field

import psycopg

ACTIONS = ("reviewed", "withdrawn")
BASIS_KINDS = ("counsel-advice", "decision-record")


class ReviewRefused(Exception):
    """The review cannot be recorded as asked; nothing was written."""


@dataclass
class Plan:
    source_id: str
    source_name: str
    action: str
    source_state: str
    to_cover: list[str] = field(default_factory=list)   # holdings this review changes
    ambiguous: list[str] = field(default_factory=list)  # shared locator, see module doc
    untraceable: int = 0                                # holdings no source can be named for

    @property
    def nothing_to_do(self) -> bool:
        target = "reviewed" if self.action == "reviewed" else "unreviewed"
        return self.source_state == target and not self.to_cover


def plan(conn: psycopg.Connection, source_id: str, action: str) -> Plan:
    """Work out what recording `action` for `source_id` would change. Writes nothing."""
    if action not in ACTIONS:
        raise ReviewRefused(f"action must be one of {', '.join(ACTIONS)}")
    row = conn.execute(
        "SELECT name, rights_review_state FROM source WHERE id = %s", (source_id,)
    ).fetchone()
    if row is None:
        raise ReviewRefused(f"no source {source_id}")
    result = Plan(source_id, row[0], action, row[1])

    holdings = conn.execute(
        """
        SELECT h.id::text, h.rights_review_state,
               coalesce(array_agg(DISTINCT a.source_id::text)
                        FILTER (WHERE a.source_id IS NOT NULL), '{}')
          FROM holding h
          JOIN holding_representation hr ON hr.holding_id = h.id AND hr.role = 'original'
          JOIN preserved_object po ON po.id = hr.object_id
          LEFT JOIN acquisition_attempt a
                 ON a.locator = po.original_name AND a.outcome = 'success'
         GROUP BY h.id, h.rights_review_state
         ORDER BY h.id
        """).fetchall()
    # The state a holding must be in to be changed by this action.
    from_state = "unreviewed" if action == "reviewed" else "reviewed"
    for holding_id, state, sources in holdings:
        if not sources:
            result.untraceable += 1
        elif sources == [source_id]:
            if state == from_state:
                result.to_cover.append(holding_id)
        elif source_id in sources:
            result.ambiguous.append(holding_id)
            if action == "withdrawn" and state == "reviewed":
                result.to_cover.append(holding_id)
    return result


def record(conn: psycopg.Connection, review: Plan, recorded_by: str,
           basis_kind: str, basis_reference: str, note: str | None = None) -> str:
    """Record the planned review in one transaction. Returns the record's id.

    The database refuses it if `recorded_by` is not a person or the basis is
    empty; the checks here only give the reason earlier.
    """
    if basis_kind not in BASIS_KINDS:
        raise ReviewRefused(f"basis kind must be one of {', '.join(BASIS_KINDS)}")
    if not (basis_reference or "").strip():
        raise ReviewRefused("a review needs a named written basis "
                            "(counsel's advice, or a Decision Record relying on it)")
    if review.nothing_to_do:
        raise ReviewRefused(f"{review.source_name!r} is already {review.action} "
                            "and there is nothing left to cover")
    kind = conn.execute("SELECT kind FROM pipeline_agent WHERE id = %s",
                        (recorded_by,)).fetchone()
    if kind is None or kind[0] != "person":
        raise ReviewRefused("a rights review is a human act: the agent must be "
                            "a registered person (§79, POL-0001 §10)")
    with conn.transaction():
        return str(conn.execute(
            "SELECT record_rights_review(%s::uuid, %s, %s::uuid, %s, %s, %s, %s::uuid[])",
            (review.source_id, review.action, recorded_by, basis_kind,
             basis_reference.strip(), note, review.to_cover),
        ).fetchone()[0])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--dbname", required=True)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--action", required=True, choices=ACTIONS)
    parser.add_argument("--agent", required=True, help="the person's pipeline_agent id")
    parser.add_argument("--basis-kind", required=True, choices=BASIS_KINDS)
    parser.add_argument("--basis-reference", required=True,
                        help="what the review rests on, e.g. which advice or record")
    parser.add_argument("--note")
    parser.add_argument("--commit", action="store_true",
                        help="record it; without this nothing is written")
    args = parser.parse_args(argv)
    try:
        with psycopg.connect(dbname=args.dbname, autocommit=True) as conn:
            review = plan(conn, args.source_id, args.action)
            print(f"source     {review.source_name}  ({review.source_id})")
            print(f"state now  {review.source_state}")
            print(f"action     {review.action}")
            print(f"covers     {len(review.to_cover)} holding(s) changed by this record")
            print(f"ambiguous  {len(review.ambiguous)} holding(s) whose locator another "
                  "source also acquired"
                  + (" (left out)" if review.action == "reviewed" else " (included)"))
            print(f"untraceable {review.untraceable} holding(s) with no named source "
                  "(not reached)")
            if review.nothing_to_do:
                print("nothing to do", file=sys.stderr)
                return 2
            if not args.commit:
                print("plan only: nothing written (pass --commit to record it)")
                return 0
            review_id = record(conn, review, args.agent, args.basis_kind,
                               args.basis_reference, args.note)
            print(f"recorded rights review {review_id}")
            return 0
    except ReviewRefused as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    except psycopg.Error as exc:
        print(f"refused by the database: {exc.diag.message_primary or exc}",
              file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
