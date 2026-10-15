#!/usr/bin/env python3
"""Discharge the quarantine copies that predate issue #51 (DR-0069).

`Collector._admit()` has removed the quarantine copy of every admitted and
preserved item since 2026-10-02 (`collector/README.md`, "Quarantine copies are
discharged"). The captures made before that kept theirs: on the archive server,
every item collected between 2026-09-09 and 2026-09-29 still has one, which is
the 2.01x duplication `storage/measure.py` reports. The README says removing
them is a one-off that needs verification against the real OCFL objects, by a
person. This is that operation.

    python3 collector/discharge_backlog.py --dbname uiw --archive-root ~/uiw-archive
    python3 collector/discharge_backlog.py --dbname uiw --archive-root ~/uiw-archive --commit

Without `--commit` it checks every candidate and writes nothing. A candidate is
a quarantine item admitted at Gate 1, with a quarantine file still on disk and
no successful `deletion` event. For each one it requires, before the file may
go:

- exactly one `ingestion` event naming the item ("admitted from quarantine …")
  and so one preserved object to compare against. An item admitted under a
  `discard`/`metadata-only` tier (its Gate 1 rationale says "retention tier")
  has none, was never stored, and is **left**, as the pipeline leaves it; an
  item admitted for preservation with no such event is a **problem**, not a
  skip;
- the OCFL object passes `StorageRoot.fixity_check` (its stored bytes still
  match both recorded digests: stricter than the live pipeline, which trusts an
  inventory it wrote moments earlier);
- the quarantine row, the preserved object, the OCFL inventory and a fresh hash
  of the file on disk all agree on the SHA-256, which is the same three-way rule
  `discharge_quarantine_copy` applies to a new capture.

A rejected item is never touched: it stays as the evidence of what was refused.
If **any** candidate fails a check the run exits 2, removes **nothing** and says
which; the operator looks before anything is deleted. With `--commit`, each
removal is a `deletion` preservation event naming the software agent
(DR-0097), exactly as for a new capture. Running it twice is safe: a discharged
item has its success event and is no longer a candidate.

It reads the archive and writes only `preservation_event` rows and the removal
of quarantine files. It creates no holding, object or assertion (DR-0066).
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

import hashlib  # noqa: E402

from ocfl import OcflError, StorageRoot  # noqa: E402
from pipeline import discharge_quarantine_copy, ensure_software_agent  # noqa: E402

TIERS = ("permanent", "medium-term")


@dataclass
class Candidate:
    quarantine_id: str
    received_sha256: str
    archived_sha256: str
    byte_size: int


@dataclass
class Plan:
    ready: list[Candidate]
    left_unstored: list[str]     # admitted but never stored: nothing duplicated
    problems: list[str]          # anything that stops the run
    no_file: int                 # admitted items whose file is already gone


def plan(conn: psycopg.Connection, roots: dict[str, StorageRoot],
         quarantine_dir: Path) -> Plan:
    """Check every admitted item with a quarantine file; nothing is written."""
    rows = conn.execute(
        """
        SELECT q.id, encode(q.sha256, 'hex'), q.byte_size, q.gate1_rationale
          FROM quarantine_item q
         WHERE q.gate1_decision = 'admitted'
           AND NOT EXISTS (
               SELECT 1 FROM preservation_event d
                WHERE d.quarantine_item_id = q.id
                  AND d.event_type = 'deletion' AND d.outcome = 'success')
         ORDER BY q.received_at, q.id
        """).fetchall()
    result = Plan([], [], [], 0)
    fixity_done: set[str] = set()
    for qid, received, size, rationale in rows:
        qid = str(qid)
        if not (quarantine_dir / qid).is_file():
            result.no_file += 1
            continue
        objects = conn.execute(
            """
            SELECT po.ocfl_root, po.ocfl_object_id, encode(po.sha256, 'hex')
              FROM preservation_event e
              JOIN preserved_object po ON po.id = e.object_id
             WHERE e.event_type = 'ingestion' AND e.outcome = 'success'
               AND e.outcome_detail = %s
            """, (f"admitted from quarantine {qid}",)).fetchall()
        if not objects:
            if (rationale or "").startswith("retention tier"):
                result.left_unstored.append(qid)     # DR-0068: seen, not stored
            else:
                # Admitted to be preserved yet nothing records it was: that is
                # a gap in the trail, not a reason to delete the only copy.
                result.problems.append(
                    f"{qid}: admitted for preservation but no ingestion event "
                    "names it; cannot tie it to an OCFL object")
            continue
        if len(objects) != 1:
            result.problems.append(
                f"{qid}: {len(objects)} preserved objects claim this item")
            continue
        tier, object_id, object_sha256 = objects[0]
        root = roots.get(tier)
        if root is None or not root.has_object(object_id):
            result.problems.append(
                f"{qid}: OCFL object {object_id} is not in the {tier} root")
            continue
        try:
            if object_id not in fixity_done:
                bad = root.fixity_check(object_id)
                if bad:
                    result.problems.append(
                        f"{qid}: OCFL object {object_id} fails fixity: {bad[0]}")
                    continue
                fixity_done.add(object_id)
            inventory = root.read_inventory(object_id)
            inventory_sha256 = next(iter(inventory["fixity"]["sha256"]))
        except (OcflError, OSError, KeyError, StopIteration, ValueError) as exc:
            result.problems.append(
                f"{qid}: cannot read OCFL object {object_id}: {exc}")
            continue
        on_disk = hashlib.sha256((quarantine_dir / qid).read_bytes()).hexdigest()
        if not (on_disk == received == object_sha256 == inventory_sha256):
            result.problems.append(
                f"{qid}: digests disagree (file {on_disk[:12]}, quarantine row "
                f"{received[:12]}, object row {object_sha256[:12]}, "
                f"inventory {inventory_sha256[:12]})")
            continue
        result.ready.append(Candidate(qid, received, inventory_sha256, size))
    return result


def open_roots(archive_root: Path) -> dict[str, StorageRoot]:
    """The existing roots only: this tool must never initialise one."""
    roots = {}
    for tier in TIERS:
        root = StorageRoot(archive_root / tier, tier)
        if not root.namaste.exists():
            raise SystemExit(f"{archive_root / tier} is not an OCFL storage root; "
                             "refusing to run against the wrong directory")
        roots[tier] = root
    return roots


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--dbname", required=True)
    parser.add_argument("--archive-root", required=True, type=Path)
    parser.add_argument("--commit", action="store_true",
                        help="remove the verified files; without it nothing is written")
    args = parser.parse_args(argv)
    archive_root = args.archive_root.expanduser()
    quarantine_dir = archive_root / "quarantine"
    roots = open_roots(archive_root)
    with psycopg.connect(dbname=args.dbname, autocommit=True) as conn:
        result = plan(conn, roots, quarantine_dir)
        total = sum(c.byte_size for c in result.ready)
        print(f"{len(result.ready)} quarantine copies verified against the archive "
              f"({total:,} bytes); {len(result.left_unstored)} left (admitted, never "
              f"stored); {result.no_file} already gone; {len(result.problems)} problem(s)")
        for problem in result.problems:
            print(f"  PROBLEM: {problem}", file=sys.stderr)
        if result.problems:
            print("refused: nothing removed while any candidate fails a check",
                  file=sys.stderr)
            return 2
        if not args.commit:
            print("plan only: nothing removed (pass --commit to remove)")
            return 0
        software = ensure_software_agent(conn)
        removed = failed = 0
        for c in result.ready:
            if discharge_quarantine_copy(conn, quarantine_dir, c.quarantine_id,
                                         c.received_sha256, c.archived_sha256, software):
                removed += 1
            else:
                failed += 1
        print(f"removed {removed} quarantine copies; {failed} refused at removal "
              "(each is a recorded 'deletion' failure)")
        return 0 if failed == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
