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

import contextlib
import copy
import io
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "sources"))

import psycopg  # noqa: E402

from register import (  # noqa: E402
    commit, load_candidates, merge_class_defaults, validate,
)

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
    raw_sources, dependence, all_classes = load_candidates()

    # ---- the shipped candidates are internally sound --------------------

    check("DR-0067", "the shipped candidates validate as they stand",
          validate(raw_sources, dependence, all_classes) == [])

    # From here on, work against each candidate's merged (class defaults +
    # own overrides) view, with the class reference itself dropped — the
    # same fields commit() and describe() see (DR-0103). A class default is
    # part of what a candidate declares, not an exemption from checking it,
    # and the mutation tests below need a field's absence to actually mean
    # absence, not "falls back to the class".
    sources = []
    for s in raw_sources:
        merged = merge_class_defaults(s, all_classes)
        merged.pop("class", None)
        sources.append(merged)

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

    # Set the claim under test rather than relying on whichever candidate
    # happens to load first carrying it: files load alphabetically, and a
    # `may-preserve` source sorting first (civilian-harm.yaml, 2026-09-24)
    # silently turned this check into one that could not fail the rule.
    unflagged = copy.deepcopy(sources)
    unflagged[0]["rights_permission"] = "may-redistribute"
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

    # ---- a --only batch's dependence-existence check (DR-pending-second-
    #      source-registrations): the other end may be outside this batch
    #      without being unknown ------------------------------------------

    ofsi_only = [s for s in sources if s["key"] == "uk-ofsi-consolidated"]
    ofsi_dep = [d for d in dependence if d["from"] == "uk-ofsi-consolidated"]
    all_keys = {s["key"] for s in sources}
    check("DR-pending-second-source-registrations",
          "a dependence naming a source outside a --only batch validates "
          "when known_keys includes it",
          ofsi_dep and validate(ofsi_only, ofsi_dep, known_keys=all_keys) == [])
    check("DR-pending-second-source-registrations",
          "the same dependence is refused as unknown without known_keys, "
          "i.e. validate()'s old behaviour is unchanged by default",
          any("unknown source" in p
              for p in validate(ofsi_only, ofsi_dep)))

    # ---- verification claims must be readable, or not made -----------------

    verified = [s for s in sources if s.get("locator_verified")]
    check("PRES-007", "the two first-run candidates carry a verification date "
          "and run locators",
          {s["key"] for s in verified} >= {"eu-consolidated-list", "ofac-sdn"}
          and all(s.get("run_locators") for s in verified))
    check("PRES-007", "no candidate claims run locators without a "
          "verification date",
          all(s.get("locator_verified") for s in sources
              if s.get("run_locators")))

    undated = copy.deepcopy(sources)
    for s in undated:
        if s["key"] == "ofac-sdn":
            s.pop("locator_verified")
    rejects("PRES-007", "run locators without a verification date are refused",
            undated, [], "locator_verified is not set")

    badly_dated = copy.deepcopy(sources)
    for s in badly_dated:
        if s["key"] == "ofac-sdn":
            s["locator_verified"] = "recently"
    rejects("PRES-007", "a verification date that is not a date is refused",
            badly_dated, [], "must be an ISO date")

    insecure = copy.deepcopy(sources)
    for s in insecure:
        if s["key"] == "ofac-sdn":
            s["run_locators"] = ["http://sanctionslistservice.ofac.treas.gov/x"]
    rejects("SPEC-0003", "a run locator that is not absolute https is refused",
            insecure, [], "not an absolute https URL")

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

        # -- DR-pending-second-source-registrations: a dependence on a
        #    source registered by an *earlier*, separate commit() call is
        #    still recorded, not silently dropped ------------------------

        conn.execute("DELETE FROM source_dependence")
        conn.execute("DELETE FROM source")
        by_key = {s["key"]: s for s in sources}
        eu = [s for s in sources if s["key"] == "eu-consolidated-list"]
        ofsi = [s for s in sources if s["key"] == "uk-ofsi-consolidated"]
        commit(conn, eu, [], agent, all_sources_by_key=by_key)
        commit(conn, ofsi, ofsi_dep, agent, all_sources_by_key=by_key)
        check("DR-pending-second-source-registrations",
              "a dependence on a source registered by an earlier, separate "
              "call is recorded when the later call supplies "
              "all_sources_by_key",
              conn.execute(
                  "SELECT count(*) FROM source_dependence sd "
                  "JOIN source s ON s.id = sd.dependent_id "
                  "WHERE s.name = %s", (ofsi[0]["name"],)
              ).fetchone()[0] == len(ofsi_dep))

        # -- and the reverse: nothing is inserted, and nothing crashes, when
        #    the other end is not registered anywhere at all --------------

        conn.execute("DELETE FROM source_dependence")
        conn.execute("DELETE FROM source")
        seco = [s for s in sources if s["key"] == "seco-sanctions"]
        seco_dep = [d for d in dependence if d["from"] == "seco-sanctions"]
        ids_seco = commit(conn, seco, seco_dep, agent, all_sources_by_key=by_key)
        check("DR-pending-second-source-registrations",
              "a dependence whose other end is not registered anywhere is "
              "not recorded, and commit() does not crash",
              len(ids_seco) == 1 and conn.execute(
                  "SELECT count(*) FROM source_dependence").fetchone()[0] == 0)

        # -- DR-0103: the operator's real entry point, end to end. Every
        #    shipped candidate now references a class, and commit() reads
        #    each policy field directly off the dict it is given, so
        #    `register.py --commit` must hand it the merged view — the
        #    2026-09-19 regression was main() passing the unmerged one, which
        #    no test above can see because they all call commit() directly.
        conn.execute("DELETE FROM source_dependence")
        conn.execute("DELETE FROM source")
        proc = subprocess.run(
            [sys.executable, str(ROOT / "sources" / "register.py"),
             "--commit", "--dbname", DB, "--only", "ofac-sdn", "--agent", agent],
            capture_output=True, text=True)
        registered = conn.execute(
            "SELECT default_retention_tier, rights_permission FROM source "
            "WHERE name = %s", (by_key["ofac-sdn"]["name"],)).fetchone()
        check("DR-0103",
              "register.py --commit registers a class-referencing candidate "
              "with its class's policy fields merged in, not a crash",
              proc.returncode == 0 and registered is not None
              and registered[0] == by_key["ofac-sdn"]["default_retention_tier"]
              and registered[1] == by_key["ofac-sdn"]["rights_permission"])

        # -- #62: re-running --commit must not register the same source
        #    twice. Found on the archive server 2026-09-22 (DR-0106,
        #    *Executed* step 1): a repeated commit inserted a second row per
        #    candidate, and since collector/run.py resolves a source by
        #    (name, locator) and refuses an ambiguous match, the duplicate
        #    disabled the source that had just been registered. Cleared by
        #    hand at the time; nothing stopped it recurring.

        conn.execute("DELETE FROM source_dependence")
        conn.execute("DELETE FROM source")
        again = [s for s in sources if s["key"] == "ofac-sdn"]
        first = commit(conn, again, [], agent)
        # Caught rather than allowed to propagate: without the guard in
        # commit() the DDL refuses the duplicate insert, which is the point of
        # enforcing in both places — but an uncaught UniqueViolation would
        # abort the suite here and every check below it would go unreported.
        second, raised = None, None
        try:
            with contextlib.redirect_stdout(io.StringIO()) as spoken:
                second = commit(conn, again, [], agent)
        except psycopg.errors.UniqueViolation as exc:
            spoken, raised = io.StringIO(), exc
        check("#62", "commit() itself skips an already-registered source "
              "rather than relying on the store to refuse it",
              raised is None)
        rows = conn.execute(
            "SELECT count(*) FROM source WHERE name = %s",
            (again[0]["name"],)).fetchone()[0]
        check("#62", "a second --commit of the same source inserts no second "
              "row, and returns the id already registered",
              rows == 1 and second == first)
        check("#62", "and says so, rather than succeeding silently",
              "already registered" in spoken.getvalue())

        # -- the same rule in the database, so the store refuses what the
        #    code would if the code were wrong (a policy that matters is
        #    enforced in both places).
        try:
            conn.execute(
                "INSERT INTO source (id, source_type, name, locator, "
                "collection_method, default_retention_tier, "
                "default_access_tier, rights_permission) "
                "SELECT gen_random_uuid(), source_type, name, locator, "
                "collection_method, default_retention_tier, "
                "default_access_tier, rights_permission FROM source "
                "WHERE name = %s", (again[0]["name"],))
            refused = False
        except psycopg.errors.UniqueViolation:
            refused = True
        check("#62", "the DDL refuses a duplicate (name, locator) even when "
              "inserted directly, not only through commit()", refused)

        # -- a null locator is one locator, not a wildcard: NULLS NOT
        #    DISTINCT is what makes the constraint cover this case at all.
        # Vocabulary values are taken from a real candidate rather than
        # written in, so this cannot drift from the generated enums (DR-0078).
        no_locator = (
            "INSERT INTO source (id, source_type, name, collection_method, "
            "default_retention_tier, default_access_tier, rights_permission) "
            "VALUES (gen_random_uuid(),%s,'No Locator Source',%s,%s,%s,%s)")
        no_locator_args = (
            again[0]["source_type"], again[0]["collection_method"],
            again[0]["default_retention_tier"],
            again[0]["default_access_tier"], again[0]["rights_permission"])
        conn.execute(no_locator, no_locator_args)
        try:
            conn.execute(no_locator, no_locator_args)
            refused_null = False
        except psycopg.errors.UniqueViolation:
            refused_null = True
        check("#62", "two rows sharing a name and a NULL locator are refused "
              "too (UNIQUE NULLS NOT DISTINCT)", refused_null)

        # -- a re-run is a no-op, which means an edited candidate file must
        #    not look as though its new policy was applied. Re-registering a
        #    source whose policy changed is a founder act (DR-0093 §3).
        drifted = copy.deepcopy(again[0])
        drifted["capture_format"] = (
            "warc" if again[0].get("capture_format") != "warc" else "http")
        try:
            with contextlib.redirect_stdout(io.StringIO()) as spoken:
                commit(conn, [drifted], [], agent)
        except psycopg.errors.UniqueViolation:
            spoken = io.StringIO()   # guard gone; the store refused instead
        stored_format = conn.execute(
            "SELECT capture_format FROM source WHERE name = %s",
            (again[0]["name"],)).fetchone()[0]
        check("#62", "a changed policy field in the candidate file is reported "
              "and NOT silently applied by a re-run",
              "NOT updated: capture_format" in spoken.getvalue()
              and stored_format == again[0].get("capture_format", "http"))

        # -- and the operator's real entry point, twice, which is exactly what
        #    happened on 2026-09-22. The checks above call commit() directly,
        #    so none of them would catch main() losing this guard.
        conn.execute("DELETE FROM source_dependence")
        conn.execute("DELETE FROM source")
        cmd = [sys.executable, str(ROOT / "sources" / "register.py"),
               "--commit", "--dbname", DB, "--only", "ofac-sdn",
               "--agent", agent]
        one_run = subprocess.run(cmd, capture_output=True, text=True)
        two_run = subprocess.run(cmd, capture_output=True, text=True)
        check("#62", "register.py --commit run twice leaves one row, both "
              "runs succeeding",
              one_run.returncode == 0 and two_run.returncode == 0
              and conn.execute(
                  "SELECT count(*) FROM source WHERE name = %s",
                  (by_key["ofac-sdn"]["name"],)).fetchone()[0] == 1)
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
