#!/usr/bin/env python3
"""Tests for schema/check_drift.py (issue #57; DR-0105 *Executed* §2, DR-0110).

Runs against real PostgreSQL. A "live" database is built from the DDL, then
broken one object at a time the way a stale live database actually differs
from `main`: a constraint absent (`source_identity_unique`, DR-0110), a column
absent (`acquisition_route`, DR-0105), a missing index, trigger and enum
value, a hand-added extra column. Each break must be reported, and the
untouched database must report nothing -- a drift check that always says
"clean" proves nothing, so the clean case and every break are both asserted.

Run:  PGHOST=... PGPORT=... PGUSER=... python3 schema/tests/test_check_drift.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "schema"))

import psycopg  # noqa: E402
from psycopg import sql  # noqa: E402

import check_drift  # noqa: E402

PASSES: list[str] = []
FAILURES: list[str] = []
LIVE = "uiw_drift_live_test"


def check(req: str, what: str, condition: bool) -> None:
    (PASSES if condition else FAILURES).append(
        f"{'PASS' if condition else 'FAIL'}  {req} — {what}"
    )


def build_live() -> psycopg.Connection:
    with psycopg.connect(dbname="postgres", autocommit=True) as admin:
        admin.execute(sql.SQL("DROP DATABASE IF EXISTS {} WITH (FORCE)").format(sql.Identifier(LIVE)))
        admin.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(LIVE)))
    conn = psycopg.connect(dbname=LIVE, autocommit=True)
    for f in sorted((ROOT / "schema").glob("0*.sql")):
        conn.execute(f.read_text())
    return conn


def drift() -> set[tuple[str, str, str]]:
    return set(check_drift.check(LIVE))


def main() -> int:
    live = build_live()

    check("issue #57", "a database built from the DDL reports no drift", drift() == set())

    # The two real cases from the issue.
    live.execute("ALTER TABLE source DROP CONSTRAINT source_identity_unique")
    check("DR-0110 / #62", "missing source_identity_unique is reported",
          ("missing-in-live", "constraint", "source.source_identity_unique") in drift())
    live.execute("ALTER TABLE source ADD CONSTRAINT source_identity_unique "
                 "UNIQUE NULLS NOT DISTINCT (name, locator)")
    check("issue #57", "restoring the constraint clears the report", drift() == set())

    live.execute("ALTER TABLE acquisition_attempt DROP COLUMN acquisition_route")
    d = drift()
    check("DR-0105", "a missing column is reported",
          ("missing-in-live", "column", "acquisition_attempt.acquisition_route") in d)
    # Dropping a column takes the CHECK constraints that mention it with it;
    # those are real consequences and must be reported, but nothing else may be.
    check("issue #57", "dropping a column reports only that column and the constraints that went with it",
          all(c == "missing-in-live" and (k == "column" or (k == "constraint" and key.startswith("acquisition_attempt.")))
              for c, k, key in d)
          and sum(1 for _, k, _ in d if k == "column") == 1)
    live.execute("ALTER TABLE acquisition_attempt ADD COLUMN acquisition_route text")
    # Re-adding with a different type than the DDL must not read as clean.
    check("issue #57", "a column re-added with a different definition is reported as differing",
          any(c == "differs" and k == "column" and key == "acquisition_attempt.acquisition_route"
              for c, k, key in drift()))
    live.execute("ALTER TABLE acquisition_attempt DROP COLUMN acquisition_route")
    live.close()
    # Rebuild rather than reconstruct the original type by hand: a fresh DDL
    # build is the reference the tool compares against.
    live = build_live()
    check("issue #57", "a rebuilt database is clean again", drift() == set())

    live.execute("ALTER TABLE source ADD COLUMN hand_edit text")
    check("issue #57", "a column present only in the live database is reported as extra",
          ("extra-in-live", "column", "source.hand_edit") in drift())
    live.execute("ALTER TABLE source DROP COLUMN hand_edit")

    idx = live.execute("SELECT indexname FROM pg_indexes WHERE schemaname='public' "
                       "AND indexname NOT IN (SELECT conname FROM pg_constraint) LIMIT 1").fetchone()
    if idx:
        live.execute(sql.SQL("DROP INDEX {}").format(sql.Identifier(idx[0])))
        check("issue #57", "a missing index is reported",
              any(c == "missing-in-live" and k == "index" and key.endswith("." + idx[0])
                  for c, k, key in drift()))
        live.close()
        live = build_live()
    else:
        check("issue #57", "the DDL has a standalone index to test against", False)

    trg = live.execute("SELECT cl.relname, t.tgname FROM pg_trigger t JOIN pg_class cl "
                       "ON cl.oid = t.tgrelid WHERE NOT t.tgisinternal LIMIT 1").fetchone()
    live.execute(sql.SQL("DROP TRIGGER {} ON {}").format(sql.Identifier(trg[1]), sql.Identifier(trg[0])))
    check("issue #57", "a missing trigger is reported",
          ("missing-in-live", "trigger", f"{trg[0]}.{trg[1]}") in drift())
    live.close()
    live = build_live()

    live.execute("DROP TABLE source_types CASCADE")
    d = drift()
    check("issue #57", "a missing table is reported",
          ("missing-in-live", "table", "source_types") in d)
    check("issue #57", "a missing table's columns are reported too",
          any(c == "missing-in-live" and k == "column" and key.startswith("source_types.")
              for c, k, key in d))
    live.close()
    live = build_live()

    enum = live.execute("SELECT t.typname, e.enumlabel FROM pg_type t JOIN pg_enum e "
                        "ON e.enumtypid = t.oid GROUP BY t.typname, e.enumlabel "
                        "ORDER BY t.typname LIMIT 1").fetchone()
    live.execute(sql.SQL("ALTER TYPE {} ADD VALUE 'zz_hand_added'").format(sql.Identifier(enum[0])))
    check("issue #57", "an enum value added only in the live database is reported as differing",
          ("differs", "enum", enum[0]) in drift())
    live.close()

    # The tool must leave nothing behind and must not write to the live database.
    with psycopg.connect(dbname="postgres", autocommit=True) as admin:
        left = admin.execute("SELECT count(*) FROM pg_database WHERE datname LIKE 'uiw_drift_ref_%'").fetchone()[0]
    check("issue #57", "no scratch reference database is left behind", left == 0)

    # An unreachable live database is "could not check", never "no drift".
    check("issue #57", "a nonexistent live database exits 2, not 0",
          check_drift.main(["--dbname", "uiw_no_such_database_xyz"]) == 2)
    check("issue #57", "a drifted database exits 1",
          check_drift.main(["--dbname", LIVE]) == 1)

    with psycopg.connect(dbname="postgres", autocommit=True) as admin:
        admin.execute(sql.SQL("DROP DATABASE IF EXISTS {} WITH (FORCE)").format(sql.Identifier(LIVE)))

    for line in PASSES + FAILURES:
        print(line)
    print(f"\n{len(PASSES)} passed, {len(FAILURES)} failed")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
