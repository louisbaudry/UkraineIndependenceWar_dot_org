#!/usr/bin/env python3
"""Report schema drift between a live database and the DDL on this checkout.

Issue #57; the problem it names is DR-0105 *Executed* §2 (a live schema ~10
weeks behind ``main``) and DR-0110 *Executed* (``source_identity_unique``
missing from the live database). The project has no migration mechanism
(``docs/infrastructure.md`` §3.2): the schema is rebuilt from ``schema/0*.sql``,
which a database holding real data cannot be. This tool answers the question
that comes before any reload -- *is the live database behind the DDL, and by
what?* -- so a person decides to run ``docs/runbooks/schema-reload.md`` on
evidence, not on a hunch or on a failed collection run.

How it works: build a scratch database from the checkout's DDL, read the
catalogs of both databases, diff them, drop the scratch database. The live
database is only ever *read* (catalog queries, no table data, no writes).
The scratch database is created and dropped on the same server, so the
connecting role needs ``CREATEDB``; use ``--reference-dsn-db`` to point at a
different administrative database if ``postgres`` is not reachable.

What is compared (schema ``public`` only): tables and columns (type,
nullability, default), constraints, indexes, triggers, functions, views and
enum values. What is **not** compared: row data -- the DDL seeds lookup tables
(``source_types``, ``identifier_types`` ...), and a live database is expected
to hold more rows than a fresh one. Seed-row drift is real but is a data
question; it is outside this tool.

Exit status: 0 no drift, 1 drift found, 2 the check itself could not run.
Exit 0 means *structurally identical on the compared objects*, nothing wider.

Environment: PGHOST, PGPORT, PGUSER, PGPASSWORD as for ``psql``.
"""

from __future__ import annotations

import argparse
import sys
import uuid
from pathlib import Path

import psycopg
from psycopg import sql

SCHEMA_DIR = Path(__file__).resolve().parent

# One query per object kind. Each returns (key, definition) rows; the key
# names the object, the definition is what must match. Using the server's own
# pg_get_*def functions means a difference in how the DDL was typed (spacing,
# ordering of clauses) cannot show up as drift -- only a difference the
# server itself normalises differently can.
_QUERIES: dict[str, str] = {
    "column": """
        SELECT c.table_name || '.' || c.column_name,
               c.udt_name || ' null=' || c.is_nullable
                   || ' default=' || coalesce(c.column_default, '')
        FROM information_schema.columns c
        JOIN information_schema.tables t
          ON t.table_schema = c.table_schema AND t.table_name = c.table_name
        WHERE c.table_schema = 'public' AND t.table_type = 'BASE TABLE'
    """,
    "table": """
        SELECT table_name, table_type FROM information_schema.tables
        WHERE table_schema = 'public'
    """,
    "constraint": """
        SELECT cl.relname || '.' || co.conname, pg_get_constraintdef(co.oid)
        FROM pg_constraint co
        JOIN pg_class cl ON cl.oid = co.conrelid
        JOIN pg_namespace n ON n.oid = cl.relnamespace
        WHERE n.nspname = 'public'
    """,
    "index": """
        SELECT tablename || '.' || indexname, indexdef
        FROM pg_indexes WHERE schemaname = 'public'
    """,
    "trigger": """
        SELECT cl.relname || '.' || t.tgname, pg_get_triggerdef(t.oid)
        FROM pg_trigger t
        JOIN pg_class cl ON cl.oid = t.tgrelid
        JOIN pg_namespace n ON n.oid = cl.relnamespace
        WHERE n.nspname = 'public' AND NOT t.tgisinternal
    """,
    "function": """
        SELECT p.proname || '(' || pg_get_function_identity_arguments(p.oid) || ')',
               pg_get_functiondef(p.oid)
        FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace
        WHERE n.nspname = 'public'
    """,
    "view": """
        SELECT viewname, definition FROM pg_views WHERE schemaname = 'public'
    """,
    "enum": """
        SELECT t.typname,
               string_agg(e.enumlabel, ',' ORDER BY e.enumsortorder)
        FROM pg_type t
        JOIN pg_enum e ON e.enumtypid = t.oid
        JOIN pg_namespace n ON n.oid = t.typnamespace
        WHERE n.nspname = 'public'
        GROUP BY t.typname
    """,
}

# Report order: a missing table explains its missing columns, so it leads.
KINDS = ("table", "column", "constraint", "index", "trigger", "function", "view", "enum")


def snapshot(conn: psycopg.Connection) -> dict[str, dict[str, str]]:
    """Read the structural catalog of ``public`` into ``{kind: {key: definition}}``.

    Read-only: catalog queries only, no table data is touched.
    """
    snap: dict[str, dict[str, str]] = {}
    for kind in KINDS:
        snap[kind] = {k: (v or "") for k, v in conn.execute(_QUERIES[kind]).fetchall()}
    return snap


def diff(live: dict[str, dict[str, str]], ref: dict[str, dict[str, str]]) -> list[tuple[str, str, str]]:
    """Compare a live snapshot with the reference built from DDL.

    Returns ``(change, kind, key)`` rows, ``change`` being ``missing-in-live``
    (the DDL has it, the live database does not -- the case that breaks a
    run), ``extra-in-live`` (the live database has something the DDL does
    not -- a hand edit, or a column the DDL has since dropped) or ``differs``.
    """
    out: list[tuple[str, str, str]] = []
    for kind in KINDS:
        l, r = live[kind], ref[kind]
        for key in sorted(r.keys() - l.keys()):
            out.append(("missing-in-live", kind, key))
        for key in sorted(l.keys() - r.keys()):
            out.append(("extra-in-live", kind, key))
        for key in sorted(l.keys() & r.keys()):
            if l[key] != r[key]:
                out.append(("differs", kind, key))
    return out


def build_reference(admin_dbname: str, scratch: str) -> psycopg.Connection:
    """Create ``scratch`` from ``schema/0*.sql`` and return a connection to it.

    The files are applied in filename order, as ``schema/tests/run.sh`` and
    the archive server's install do, so the reference is exactly what a
    fresh rebuild would produce.
    """
    with psycopg.connect(dbname=admin_dbname, autocommit=True) as admin:
        admin.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(scratch)))
    ref = psycopg.connect(dbname=scratch, autocommit=True)
    for f in sorted(SCHEMA_DIR.glob("0*.sql")):
        ref.execute(f.read_text())
    return ref


def drop_reference(admin_dbname: str, scratch: str) -> None:
    with psycopg.connect(dbname=admin_dbname, autocommit=True) as admin:
        admin.execute(sql.SQL("DROP DATABASE IF EXISTS {} WITH (FORCE)").format(sql.Identifier(scratch)))


def check(live_dbname: str, admin_dbname: str = "postgres") -> list[tuple[str, str, str]]:
    """Build a throwaway reference, diff ``live_dbname`` against it, clean up."""
    scratch = f"uiw_drift_ref_{uuid.uuid4().hex[:8]}"
    ref = None
    try:
        ref = build_reference(admin_dbname, scratch)
        ref_snap = snapshot(ref)
        with psycopg.connect(dbname=live_dbname, autocommit=True) as live:
            live.execute("SET default_transaction_read_only = on")
            live_snap = snapshot(live)
    finally:
        if ref is not None:
            ref.close()
        drop_reference(admin_dbname, scratch)
    return diff(live_snap, ref_snap)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dbname", required=True, help="the live database to check (read-only)")
    ap.add_argument("--admin-dbname", default="postgres",
                    help="database to connect to for CREATE/DROP of the scratch reference")
    args = ap.parse_args(argv)
    try:
        rows = check(args.dbname, args.admin_dbname)
    except Exception as exc:  # the check could not run; that is not "no drift"
        print(f"check could not run: {exc}", file=sys.stderr)
        return 2
    if not rows:
        print(f"{args.dbname}: no structural drift from schema/0*.sql")
        return 0
    print(f"{args.dbname}: {len(rows)} difference(s) from schema/0*.sql")
    for change, kind, key in rows:
        print(f"  {change:16} {kind:10} {key}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
