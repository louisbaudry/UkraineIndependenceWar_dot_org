#!/usr/bin/env python3
"""Tests for source registration.

Registration is the act that authorises collection (OPS-001), so the rules
worth testing are the ones that would let an unauthorised or under-specified
source through: a missing policy field silently defaulted, an open-ended
scope, a rights claim nobody checked, or a dependence declaration with no
reasoning behind it.

Run:  PGHOST=… PGPORT=… PGUSER=… python3 sources/tests/test_register.py
"""

from __future__ import annotations

import copy
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "sources"))

import psycopg  # noqa: E402

from register import commit, load_candidates, validate  # noqa: E402

PASSES: list[str] = []
FAILURES: list[str] = []
DB = "uiw_sources_test"


def check(req: str, what: str, condition: bool) -> None:
    (PASSES if condition else FAILURES).append(
        f"{'PASS' if condition else 'FAIL'}  {req} — {what}")


def rejects(req: str, what: str, sources, dependence, fragment: str) -> None:
    """Validation must refuse, and say why in terms the founder can act on."""
    problems = validate(sources, dependence)
    if problems and any(fragment in p for p in problems):
        PASSES.append(f"PASS  {req} — {what}")
        return
    FAILURES.append(
        f"FAIL  {req} — {what}: got {problems or 'no problems'}")


def build_database() -> None:
    subprocess.run(["psql", "-q", "-c", f"DROP DATABASE IF EXISTS {DB}",
                    "-c", f"CREATE DATABASE {DB}", "postgres"],
                   check=True, capture_output=True)
    for sql in sorted((ROOT / "schema").glob("0*.sql")):
        subprocess.run(["psql", "-q", "-d", DB, "-v", "ON_ERROR_STOP=1",
                        "-f", str(sql)], check=True, capture_output=True)


def run() -> int:
    sources, dependence = load_candidates()

    # ---- the shipped candidates are internally sound --------------------

    check("DR-0067", "the shipped candidates validate as they stand",
          validate(sources, dependence) == [])
    check("DR-0067", "every candidate names a jurisdiction and a scope",
          all(s.get("jurisdiction") and s.get("scope_rules") for s in sources))
    check("§14", "no candidate claims redistribution without flagging the basis",
          all("NOT LEGALLY REVIEWED" in (s.get("rights_basis") or "").upper()
              or "UNVERIFIED" in (s.get("rights_basis") or "").upper()
              for s in sources
              if s["rights_permission"] == "may-redistribute"))

    # ---- what registration must refuse -----------------------------------

    for field in ("scope_rules", "default_access_tier", "rights_permission",
                  "jurisdiction"):
        broken = copy.deepcopy(sources)
        broken[0].pop(field, None)
        rejects("DR-0067", f"a candidate missing {field} is refused",
                broken, [], f"missing required field {field!r}")

    crawling = copy.deepcopy(sources)
    crawling[0]["scope_rules"] = "Crawl the entire site for anything relevant."
    rejects("DR-0071", "an open-ended scope is refused",
            crawling, [], "open-ended crawling")

    unflagged = copy.deepcopy(sources)
    unflagged[0]["rights_basis"] = "Public domain, obviously."
    rejects("§14", "a redistribution claim with an unflagged basis is refused",
            unflagged, [], "without flagging that the basis is unreviewed")

    graphic = copy.deepcopy(sources)
    graphic[0]["expects_graphic_content"] = True
    graphic[0]["default_access_tier"] = "public"
    rejects("PRES-012", "a graphic-content source cannot default to public",
            graphic, [], "expects graphic content but defaults to public")

    duplicated = copy.deepcopy(sources) + [copy.deepcopy(sources[0])]
    rejects("DR-0067", "duplicate source keys are refused",
            duplicated, [], "duplicate source key")

    rejects("DR-0028", "a dependence declaration with no reasoning is refused",
            sources,
            [{"from": sources[0]["key"], "to": sources[1]["key"],
              "relation": "cites"}],
            "no note")

    rejects("DR-0028", "dependence on an unregistered source is refused",
            sources,
            [{"from": sources[0]["key"], "to": "nonexistent",
              "relation": "cites", "note": "x"}],
            "unknown source")

    # ---- the declared dependence is not decorative ------------------------

    check("DR-0028", "the consolidated list is declared derived, not independent",
          any(d["from"] == "eu-consolidated-list"
              and d["to"] == "eur-lex-sanctions"
              and d["relation"] == "derives-from" for d in dependence))
    check("§36", "every declared dependence carries its reasoning",
          all(len(d.get("note", "")) > 40 for d in dependence))

    # ---- registration against a real schema -------------------------------

    build_database()
    conn = psycopg.connect(dbname=DB, autocommit=True)
    try:
        agent = str(uuid.uuid4())
        conn.execute("INSERT INTO pipeline_agent (id, kind, name) "
                     "VALUES (%s,'person','Test founder')", (agent,))

        ids = commit(conn, sources, dependence, agent)
        check("OPS-001", "registration inserts every accepted source",
              len(ids) == len(sources))
        check("DR-0067", "registered sources carry their collection policy",
              conn.execute(
                  "SELECT count(*) FROM source WHERE scope_rules IS NOT NULL "
                  "AND collection_method IS NOT NULL").fetchone()[0]
              == len(sources))
        check("DR-0028", "declared dependence is stored with an asserter",
              conn.execute(
                  "SELECT count(*) FROM source_dependence WHERE "
                  "asserter_id = %s AND note IS NOT NULL", (agent,)
              ).fetchone()[0] == len(dependence))
        check("DR-0027", "triage grades are stored and are not truth values",
              conn.execute(
                  "SELECT count(*) FROM source WHERE "
                  "grade_source_reliability IS NOT NULL").fetchone()[0] > 0)

        # Registration authorises collection; it does not perform it. A
        # registry full of sources and an empty archive is the correct state
        # immediately after this step.
        check("OPS-001", "registration collects nothing",
              conn.execute("SELECT count(*) FROM holding").fetchone()[0] == 0
              and conn.execute(
                  "SELECT count(*) FROM collector_run").fetchone()[0] == 0)

        # A source registered at `permanent` enters the fixity schedule; that
        # obligation starts at registration, not at first collection.
        check("DR-0005", "permanent sources are registered as permanent",
              conn.execute(
                  "SELECT count(*) FROM source WHERE "
                  "default_retention_tier = 'permanent'").fetchone()[0]
              == len([s for s in sources
                      if s["default_retention_tier"] == "permanent"]))

        # -- per-source registration, which is how a per-source decision is
        #    actually executed
        conn.execute("DELETE FROM source_dependence")
        conn.execute("DELETE FROM source")
        one = [s for s in sources if s["key"] == "ofac-sdn"]
        ids = commit(conn, one, [], agent)
        check("§78", "a single source can be registered on its own",
              len(ids) == 1
              and conn.execute("SELECT count(*) FROM source").fetchone()[0] == 1)
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
