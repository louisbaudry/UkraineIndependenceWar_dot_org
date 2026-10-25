#!/usr/bin/env python3
"""Tests for the read-only archive MCP server.

The rules worth testing are the ones whose failure would mislead or write:
a missing database answered as "nothing collected", a registration state
guessed rather than read, a Decision Record status inferred from the wrong
place, and any path by which the server could change the archive.

Run:  PGHOST=… PGPORT=… PGUSER=… python3 archive_mcp/tests/test_tools.py
(needs `pip install -r archive_mcp/requirements.txt` for the protocol checks)
"""

from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "sources"))

import psycopg  # noqa: E402

from archive_mcp import tools  # noqa: E402
from register import commit, load_candidates, merge_class_defaults  # noqa: E402

PASSES: list[str] = []
FAILURES: list[str] = []
DB = "uiw_archive_mcp_test"


def check(req: str, what: str, condition: bool) -> None:
    (PASSES if condition else FAILURES).append(
        f"{'PASS' if condition else 'FAIL'}  {req} — {what}")


def refuses(req: str, what: str, fn, fragment: str) -> None:
    try:
        fn()
    except tools.ToolError as e:
        check(req, what, fragment in str(e))
        return
    check(req, what, False)


def build_database() -> None:
    subprocess.run(["psql", "-q", "-c", f"DROP DATABASE IF EXISTS {DB}",
                    "-c", f"CREATE DATABASE {DB}", "postgres"],
                   check=True, capture_output=True)
    for sql in sorted((ROOT / "schema").glob("0*.sql")):
        subprocess.run(["psql", "-q", "-d", DB, "-v", "ON_ERROR_STOP=1",
                        "-f", str(sql)], check=True, capture_output=True)


def seed() -> dict[str, str]:
    """Register two real candidates, give one a failed and a good run and a
    holding, leave the rest unregistered. Returns key -> source id."""
    raw, dep, classes = load_candidates()
    merged = []
    for s in raw:
        m = merge_class_defaults(s, classes)
        m.pop("class", None)
        merged.append(m)
    pick = [m for m in merged if m["key"] in ("ofac-sdn", "eu-consolidated-list")]
    with psycopg.connect(dbname=DB, autocommit=True) as conn:
        person = str(uuid.uuid4())
        conn.execute("INSERT INTO pipeline_agent (id, kind, name) "
                     "VALUES (%s,'person','Test founder')", (person,))
        ids = commit(conn, pick, [], person)
        sid = ids["ofac-sdn"]
        for acquired, failed, size in ((3, 0, 1000), (1, 2, 500)):
            conn.execute(
                "INSERT INTO collector_run (id, source_id, collector_agent_id, "
                "configuration, started_at, items_discovered, items_acquired, "
                "items_failed, bytes_preserved) VALUES "
                "(%s,%s,%s,'{}', now(), %s, %s, %s, %s)",
                (str(uuid.uuid4()), sid, person, acquired + failed,
                 acquired, failed, size))
        conn.execute(
            "INSERT INTO holding (id, completeness, retention_tier, "
            "access_tier, rights_permission) VALUES "
            "(%s,'metadata-only','metadata-only','public','may-preserve')",
            (str(uuid.uuid4()),))
        conn.execute(
            "INSERT INTO acquisition_attempt (id, source_id, locator, "
            "attempted_at, outcome) VALUES (%s,%s,'x',now(),'success')",
            (str(uuid.uuid4()), sid))
    return ids


def set_db(on: bool) -> None:
    if on:
        os.environ["PGDATABASE"] = DB
    else:
        os.environ.pop("PGDATABASE", None)


def run() -> int:
    # ---- no database: unknown, never "no" and never "empty" --------------

    set_db(False)
    st = tools.archive_status()
    check("CLAUDE.md", "without a database, archive_status says unknown, not zero",
          st["database"] is None and "unknown" in st["note"]
          and "collector_runs" not in st)
    listed = tools.list_sources()
    check("CLAUDE.md", "without a database no source claims to be registered or not",
          len(listed) > 0 and all(s["registered"] is None for s in listed))
    refuses("CLAUDE.md", "filtering on registration without a database is refused",
            lambda: tools.list_sources(registered=True), "needs a database")
    check("CLAUDE.md", "get_source without a database reports registration unknown",
          tools.get_source("ofac-sdn")["registration"]["registered"] is None)

    # ---- candidates: the same merged view register.py validates ----------

    raw, _dep, classes = load_candidates()
    check("DR-0103", "list_sources covers every candidate register.py loads",
          {s["key"] for s in listed} == {s["key"] for s in raw})
    full = tools.get_source("ofac-sdn")
    expected = merge_class_defaults(
        next(s for s in raw if s["key"] == "ofac-sdn"), classes)
    check("DR-0103", "get_source returns class defaults merged, as registered",
          full.get("collection_cadence") == expected["collection_cadence"]
          and full.get("collection_cadence") is not None
          and full["class"] == expected["class"])
    refuses("DR-0067", "an unknown source key is refused",
            lambda: tools.get_source("no-such-source"), "unknown source key")

    # ---- Decision Records: status from the register ----------------------

    d = tools.get_decision("72")
    check("DR-0046", "get_decision accepts 72, 0072 and DR-0072 alike",
          d["id"] == "DR-0072" == tools.get_decision("DR-0072")["id"]
          == tools.get_decision("0072")["id"])
    check("DR-0046", "status comes from the register row",
          d["status"] == "Approved")
    check("DR-0046", "supersession is read from the header block",
          d["header"].get("superseded_by") is not None
          and "text" not in d)
    check("DR-0046", "include_text returns the record itself",
          "Personal Data Policy" in tools.get_decision(
              "DR-0072", include_text=True)["text"])
    refuses("DR-0046", "a number the register lacks is refused",
            lambda: tools.get_decision("9999"), "not in the register")
    refuses("DR-0046", "a non-number is refused",
            lambda: tools.get_decision("../../etc/passwd"), "not a Decision")
    everything = tools.list_decisions()
    sup = tools.list_decisions(status="superseded")
    check("DR-0046", "list_decisions filters on the register's status",
          0 < len(sup) < len(everything)
          and all("superseded" in r["status"].lower() for r in sup))
    check("DR-0046", "list_decisions query matches the title",
          any(r["id"] == "DR-0072"
              for r in tools.list_decisions(query="personal data policy")))

    # ---- with a database: read from it, and cannot write to it -----------

    build_database()
    ids = seed()
    set_db(True)

    st = tools.archive_status()
    check("DR-0070", "archive_status counts the runs the database holds",
          st["collector_runs"]["runs"] == 2
          and st["collector_runs"]["items_failed"] == 2
          and st["collector_runs"]["bytes_preserved"] == 1500)
    check("DR-0061", "archive_status counts holdings by tier and rights state",
          st["holdings_by_retention_tier"] == {"metadata-only": 1}
          and st["holdings_by_rights_review_state"] == {"unreviewed": 1})
    check("PRES-007", "archive_status counts attempts by outcome",
          st["acquisition_attempts_by_outcome"] == {"success": 1})
    flat = json.dumps(st)
    check("DR-0071", "no holding id or source id appears in archive_status",
          not any(i in flat for i in ids.values()))

    by_key = {s["key"]: s for s in tools.list_sources()}
    check("OPS-001", "a registered candidate is reported registered with its runs",
          by_key["ofac-sdn"]["registered"] is True
          and by_key["ofac-sdn"]["runs"] == 2)
    check("OPS-001", "an unregistered candidate is reported not registered",
          by_key["kpszsu"]["registered"] is False)
    reg = tools.list_sources(registered=True)
    check("OPS-001", "registered=true filters on the database's answer",
          {s["key"] for s in reg} == {"ofac-sdn", "eu-consolidated-list"})
    check("PRES-007", "get_source returns recent runs with failures counted",
          [r["items_failed"] for r in tools.get_source("ofac-sdn")["recent_runs"]]
          in ([0, 2], [2, 0]))
    check("OPS-001", "an unregistered source has no recent_runs key",
          "recent_runs" not in tools.get_source("kpszsu"))

    conn = tools.connect()
    try:
        wrote = True
        try:
            conn.execute("DELETE FROM collector_run")
        except psycopg.errors.ReadOnlySqlTransaction:
            wrote = False
        check("DR-0093", "the connection refuses a write at the database",
              not wrote)
        try:
            conn.execute("INSERT INTO source (id, source_type, name, "
                         "collection_method, default_retention_tier, "
                         "default_access_tier, rights_permission) VALUES "
                         "(gen_random_uuid(),(SELECT id FROM source_types "
                         "LIMIT 1),'x','http',"
                         "'permanent','public','may-preserve')")
            wrote = True
        except psycopg.errors.ReadOnlySqlTransaction:
            wrote = False
        check("OPS-001", "registering a source through it is refused too",
              not wrote)
    finally:
        conn.close()
    with psycopg.connect(dbname=DB) as c:
        check("DR-0093", "nothing was removed or added by the attempts above",
              c.execute("SELECT count(*) FROM collector_run").fetchone()[0] == 2
              and c.execute("SELECT count(*) FROM source").fetchone()[0] == 2)

    # ---- the protocol, end to end ----------------------------------------

    try:
        from mcp import Client, StdioServerParameters
    except ImportError:
        print("SKIP  protocol checks — the `mcp` SDK is not installed")
    else:
        set_db(False)

        async def over_stdio() -> None:
            params = StdioServerParameters(
                command=sys.executable,
                args=[str(ROOT / "archive_mcp" / "server.py")],
                env={k: v for k, v in os.environ.items() if k != "PGDATABASE"})
            async with Client(params) as client:
                listed_tools = await client.list_tools()
                names = {t.name for t in listed_tools.tools}
                check("MCP", "the server lists exactly the five read tools",
                      names == {"list_sources", "get_source", "list_decisions",
                                "get_decision", "archive_status"})
                check("MCP", "every tool is annotated read-only",
                      all(t.annotations and t.annotations.read_only_hint
                          for t in listed_tools.tools))
                res = await client.call_tool("get_decision", {"number": "72"})
                check("MCP", "a tool call round-trips over stdio",
                      "DR-0072" in res.content[0].text)
                bad = await client.call_tool("get_decision", {"number": "9999"})
                check("MCP", "a refusal comes back as a tool error, not a crash",
                      bad.is_error and "not in the register" in bad.content[0].text)

        asyncio.run(over_stdio())

    subprocess.run(["psql", "-q", "-c", f"DROP DATABASE IF EXISTS {DB}",
                    "postgres"], check=True, capture_output=True)

    for line in PASSES + FAILURES:
        print(line)
    print(f"\n{len(PASSES)} passed, {len(FAILURES)} failed")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(run())
