#!/usr/bin/env python3
"""Tests for recording a rights review (CDR-P3-45, candidate; issue #155).

Ruled 2026-10-29: a review is made per source by a person, on a named written
basis; one attributed append-only record; in the same act the source's existing
holdings are marked reviewed and listed in the record; later holdings inherit;
a withdrawal is its own record. Nothing may change the state any other way.

Real PostgreSQL, real OCFL, real pipeline; only the network is a fixture.

Run:  PGHOST=... PGPORT=... PGUSER=... python3 publication/tests/test_rights_review.py
"""

from __future__ import annotations

import contextlib
import io
import shutil
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "collector"))
sys.path.insert(0, str(ROOT / "storage"))
sys.path.insert(0, str(ROOT / "publication"))
sys.path.insert(0, str(ROOT / "collector" / "tests"))

import psycopg  # noqa: E402

import test_pipeline as shared  # noqa: E402
import rights_review as rr  # noqa: E402
from fetch import FetchResult, FixtureFetcher  # noqa: E402
from gate3 import Publisher, PublicationError  # noqa: E402
from ocfl import StorageRoot  # noqa: E402
from pipeline import Collector, ensure_software_agent  # noqa: E402

shared.DB = "uiw_rights_review_test"
check, rejects, PASSES, FAILURES = shared.check, shared.rejects, shared.PASSES, shared.FAILURES

NOW = lambda: datetime.now(timezone.utc)  # noqa: E731


def ok(locator: str, body: bytes) -> FetchResult:
    return FetchResult(locator=locator, attempted_at=NOW(), outcome="success", content=body,
                       media_type="text/html", http_status=200, http_reason="OK")


def run() -> int:
    shared.build_database()
    work = Path(tempfile.mkdtemp(prefix="uiw-rights-"))
    roots = {"permanent": StorageRoot(work / "p", "permanent"),
             "medium-term": StorageRoot(work / "m", "medium-term")}
    for r in roots.values():
        r.initialize()
    conn = psycopg.connect(dbname=shared.DB, autocommit=True)
    try:
        person = str(uuid.uuid4())
        conn.execute("INSERT INTO pipeline_agent (id, kind, name) VALUES (%s, 'person', 'reviewer')", (person,))
        software = ensure_software_agent(conn, "test-collector", "0.1.0")
        src_a = shared.seed_source(conn, name="Source A", locator="https://example.invalid/a/")
        src_b = shared.seed_source(conn, name="Source B", locator="https://example.invalid/b/")
        base = "https://example.invalid"
        fx = {}
        fetcher = FixtureFetcher(fx)

        def collect(src, loc, body):
            fx[loc] = ok(loc, body)
            Collector(conn, fetcher, work / "q", roots, person, software
                      ).run(src, [loc], configuration={})
            return conn.execute(
                "SELECT h.id::text FROM holding h JOIN holding_representation hr "
                "ON hr.holding_id = h.id JOIN preserved_object po ON po.id = hr.object_id "
                "WHERE po.original_name = %s ORDER BY h.created_at DESC LIMIT 1",
                (loc,)).fetchone()[0]

        a1 = collect(src_a, f"{base}/a/1", b"<html>a1</html>")
        b1 = collect(src_b, f"{base}/b/1", b"<html>b1</html>")
        shared_a = collect(src_a, f"{base}/shared", b"<html>shared</html>")
        shared_b = collect(src_b, f"{base}/shared", b"<html>shared</html>")

        def state(table, id_):
            return conn.execute(f"SELECT rights_review_state FROM {table} WHERE id = %s",
                                (id_,)).fetchone()[0]

        # -- nothing is reviewed until a person records it -------------------
        check("CDR-P3-45", "everything collected starts unreviewed",
              state("source", src_a) == "unreviewed" and state("holding", a1) == "unreviewed")

        # -- the plan: which holdings a review would reach --------------------
        plan_a = rr.plan(conn, src_a, "reviewed")
        check("CDR-P3-45", "the plan covers the source's own holdings and no other source's",
              plan_a.to_cover == [a1] and b1 not in plan_a.to_cover)
        check("CDR-P3-45", "a holding whose locator another source also acquired is reported "
              "as ambiguous and left out of a review",
              sorted(plan_a.ambiguous) == sorted([shared_a, shared_b])
              and shared_a not in plan_a.to_cover)
        before = conn.execute("SELECT count(*) FROM rights_review").fetchone()[0]
        check("CDR-P3-45", "planning writes nothing",
              before == 0 and state("holding", a1) == "unreviewed")

        # -- the database refuses what is not a proper review -----------------
        def refused(sql, params):
            try:
                conn.execute(sql, params)
                return False
            except psycopg.errors.Error:
                return True

        call = ("SELECT record_rights_review(%s::uuid, %s, %s::uuid, %s, %s, NULL, %s::uuid[])")
        check("CDR-P3-45", "a software agent cannot record a rights review",
              refused(call, (src_a, "reviewed", software, "counsel-advice", "advice 1", [a1]))
              and state("source", src_a) == "unreviewed")
        check("CDR-P3-45", "a review with no basis is refused",
              refused(call, (src_a, "reviewed", person, "counsel-advice", "   ", [a1])))
        check("CDR-P3-45", "a review on an unknown kind of basis is refused",
              refused(call, (src_a, "reviewed", person, "my own opinion", "x", [a1])))
        check("CDR-P3-45", "an unknown action is refused",
              refused(call, (src_a, "approved", person, "counsel-advice", "advice 1", [a1])))
        check("CDR-P3-45", "after the refusals, no record and no state change exists",
              conn.execute("SELECT count(*) FROM rights_review").fetchone()[0] == 0
              and state("source", src_a) == "unreviewed")
        check("CDR-P3-45", "the state cannot be changed by a plain UPDATE of a source",
              refused("UPDATE source SET rights_review_state = 'reviewed' WHERE id = %s", (src_a,)))
        check("CDR-P3-45", "nor of a holding",
              refused("UPDATE holding SET rights_review_state = 'reviewed' WHERE id = %s", (a1,)))
        check("CDR-P3-45", "a source cannot be inserted already reviewed",
              refused("INSERT INTO source (id, source_type, name, collection_method, "
                      "default_retention_tier, default_access_tier, rights_permission, "
                      "rights_review_state, lifecycle_state, capture_format) VALUES "
                      "(%s,'government','Sneaky','http','permanent','public','may-preserve',"
                      "'reviewed','active','http')", (str(uuid.uuid4()),)))

        # -- gate 3 refuses before a review -----------------------------------
        pub = Publisher(conn)
        kw = dict(person_id=person, holding_id=a1, access_tier="public",
                  rights_basis="Project text", rationale="fixture")
        try:
            pub.decide(**kw)
            blocked = False
        except PublicationError:
            blocked = True
        check("CDR-P3-45", "Gate 3 refuses an unreviewed holding", blocked)

        # -- recording the review ---------------------------------------------
        review_a = rr.record(conn, plan_a, person, "counsel-advice", "Advice of 2026-10-29 (fixture)")
        check("CDR-P3-45", "one record names the source, the person, the basis and the action",
              conn.execute(
                  "SELECT source_id::text, recorded_by::text, action, basis_kind, basis_reference "
                  "FROM rights_review WHERE id = %s", (review_a,)).fetchone()
              == (src_a, person, "reviewed", "counsel-advice", "Advice of 2026-10-29 (fixture)"))
        check("CDR-P3-45", "the source and its covered holding are now reviewed",
              state("source", src_a) == "reviewed" and state("holding", a1) == "reviewed")
        check("CDR-P3-45", "the record lists exactly the holdings it covered",
              [r[0] for r in conn.execute(
                  "SELECT holding_id::text FROM rights_review_holding WHERE review_id = %s",
                  (review_a,))] == [a1])
        check("CDR-P3-45", "another source, and the ambiguous holdings, stay unreviewed",
              state("source", src_b) == "unreviewed" and state("holding", b1) == "unreviewed"
              and state("holding", shared_a) == "unreviewed"
              and state("holding", shared_b) == "unreviewed")
        try:
            pub.decide(**kw)
            published = True
        except PublicationError:
            published = False
        check("CDR-P3-45", "Gate 3 now accepts the reviewed holding", published)

        # -- append-only ------------------------------------------------------
        check("§77", "a rights review cannot be edited",
              refused("UPDATE rights_review SET basis_reference = 'other' WHERE id = %s", (review_a,)))
        check("§77", "a rights review cannot be deleted",
              refused("DELETE FROM rights_review WHERE id = %s", (review_a,)))
        check("§77", "its holding list cannot be edited or deleted",
              refused("DELETE FROM rights_review_holding WHERE review_id = %s", (review_a,)))

        # -- later holdings inherit; another source's do not -------------------
        a2 = collect(src_a, f"{base}/a/2", b"<html>a2</html>")
        b2 = collect(src_b, f"{base}/b/2", b"<html>b2</html>")
        check("CDR-P3-45", "a holding admitted later from a reviewed source is reviewed",
              state("holding", a2) == "reviewed")
        check("CDR-P3-45", "and one from an unreviewed source is not",
              state("holding", b2) == "unreviewed")

        # -- nothing left to do ------------------------------------------------
        again = rr.plan(conn, src_a, "reviewed")
        try:
            rr.record(conn, again, person, "counsel-advice", "Advice again")
            repeated = False
        except rr.ReviewRefused:
            repeated = True
        check("CDR-P3-45", "recording the same review again, with nothing new to cover, is refused",
              repeated and conn.execute("SELECT count(*) FROM rights_review").fetchone()[0] == 1)

        # -- the Python layer gives reasons before the database does -----------
        plan_b = rr.plan(conn, src_b, "reviewed")
        for label, args in (("no basis", (person, "counsel-advice", "  ")),
                            ("a software agent", (software, "counsel-advice", "x"))):
            try:
                rr.record(conn, plan_b, *args)
                got = False
            except rr.ReviewRefused:
                got = True
            check("CDR-P3-45", f"record() refuses {label} before touching the database", got)

        # -- withdrawal: its own record, moving the same holdings back ----------
        plan_w = rr.plan(conn, src_a, "withdrawn")
        check("CDR-P3-45", "a withdrawal covers the source's reviewed holdings",
              sorted(plan_w.to_cover) == sorted([a1, a2]))
        review_w = rr.record(conn, plan_w, person, "decision-record", "DR-fixture withdrawing it")
        check("CDR-P3-45", "the withdrawal moves the source and its holdings back to unreviewed",
              state("source", src_a) == "unreviewed" and state("holding", a1) == "unreviewed"
              and state("holding", a2) == "unreviewed")
        check("§77", "the original review is still there: a withdrawal adds a record, never edits one",
              conn.execute("SELECT count(*) FROM rights_review WHERE source_id = %s", (src_a,)
                           ).fetchone()[0] == 2
              and conn.execute("SELECT action FROM rights_review WHERE id = %s", (review_a,)
                               ).fetchone()[0] == "reviewed" and review_w != review_a)
        try:
            pub.decide(**dict(kw, holding_id=a2))
            gate_open = True
        except PublicationError:
            gate_open = False
        check("CDR-P3-45", "after a withdrawal Gate 3 refuses the holding again", not gate_open)

        # -- the command line ---------------------------------------------------
        def cli(*extra):
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = rr.main(["--dbname", shared.DB, "--source-id", src_b, "--action", "reviewed",
                                "--agent", person, "--basis-kind", "decision-record",
                                "--basis-reference", "DR-fixture", *extra])
            return code, out.getvalue(), err.getvalue()

        code, out, _ = cli()
        check("CDR-P3-45", "the command plans by default and writes nothing",
              code == 0 and "plan only" in out and state("source", src_b) == "unreviewed")
        code, out, _ = cli("--commit")
        check("CDR-P3-45", "--commit records it",
              code == 0 and "recorded rights review" in out and state("source", src_b) == "reviewed"
              and state("holding", b1) == "reviewed" and state("holding", b2) == "reviewed")
        code, _, err = cli("--commit")
        check("CDR-P3-45", "running it again says there is nothing to do and exits 2",
              code == 2 and "nothing to do" in err)
    finally:
        conn.close()
        shutil.rmtree(work, ignore_errors=True)

    for line in PASSES + FAILURES:
        print(line)
    print(f"\n{len(PASSES)} passed, {len(FAILURES)} failed")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(run())
