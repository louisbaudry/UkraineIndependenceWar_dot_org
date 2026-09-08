#!/usr/bin/env python3
"""Tests for collector/run.py — the operator's entry point.

The script's job is to refuse. It sits between an operator and
`Collector.run()`, and the rules worth testing are the ones that would let a
run happen that nobody authorised: an unregistered candidate, an unverified
locator list, an agent that is not a person, a directory that is not an
archive. The one positive case checks that an authorised run fetches exactly
the listed locators and records what it did.

Run:  PGHOST=… PGPORT=… PGUSER=… python3 collector/tests/test_run.py
"""

from __future__ import annotations

import contextlib
import copy
import io
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "collector"))
sys.path.insert(0, str(ROOT / "sources"))

import psycopg  # noqa: E402

import run as runner  # noqa: E402
from fetch import FixtureFetcher  # noqa: E402
from register import commit, load_candidates  # noqa: E402

PASSES: list[str] = []
FAILURES: list[str] = []
DB = "uiw_run_test"


def check(req: str, what: str, condition: bool) -> None:
    (PASSES if condition else FAILURES).append(
        f"{'PASS' if condition else 'FAIL'}  {req} — {what}")


def build_database() -> None:
    subprocess.run(["psql", "-q", "-c", f"DROP DATABASE IF EXISTS {DB}",
                    "-c", f"CREATE DATABASE {DB}", "postgres"],
                   check=True, capture_output=True)
    for sql in sorted((ROOT / "schema").glob("0*.sql")):
        subprocess.run(["psql", "-q", "-d", DB, "-v", "ON_ERROR_STOP=1",
                        "-f", str(sql)], check=True, capture_output=True)


def invoke(argv: list[str], fetcher=None) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = runner.main(argv, fetcher=fetcher)
    return code, out.getvalue(), err.getvalue()


def run() -> int:
    build_database()
    work = Path(tempfile.mkdtemp(prefix="uiw-run-"))
    archive = work / "archive"

    sources, _ = load_candidates()
    ofac = next(s for s in sources if s["key"] == "ofac-sdn")
    eu = next(s for s in sources if s["key"] == "eu-consolidated-list")

    fixtures = work / "fixtures"
    fixtures.mkdir()
    fixture_files = {}
    for i, locator in enumerate(ofac["run_locators"]):
        path = fixtures / f"ofac-{i}.xml"
        path.write_text(f"<sdnList><!-- fixture {i} --></sdnList>")
        fixture_files[locator] = path
    fetcher = FixtureFetcher(fixture_files)

    conn = psycopg.connect(dbname=DB, autocommit=True)
    try:
        person = str(uuid.uuid4())
        software = str(uuid.uuid4())
        conn.execute("INSERT INTO pipeline_agent (id, kind, name) "
                     "VALUES (%s, 'person', 'Test founder')", (person,))
        conn.execute("INSERT INTO pipeline_agent (id, kind, name, software_version) "
                     "VALUES (%s, 'software', 'cron', '0.1')", (software,))

        base = ["--dbname", DB, "--agent", person,
                "--archive-root", str(archive)]

        # -- refusals first: nothing is registered yet -----------------------

        code, _, err = invoke(["--source", "ofac-sdn", *base, "--dry-run"], fetcher)
        check("DR-0071", "an unregistered candidate is refused, even for a dry run",
              code == 2 and "not registered" in err)

        code, _, err = invoke(["--source", "no-such-source", *base], fetcher)
        check("OPS-001", "an unknown candidate key is refused",
              code == 2 and "no candidate with key" in err)

        # register OFAC only
        commit(conn, [copy.deepcopy(ofac)], [], person)

        code, _, err = invoke(["--source", "ofac-sdn", "--dbname", DB,
                               "--agent", software, "--archive-root", str(archive),
                               "--dry-run"], fetcher)
        check("DR-0087 §3", "a software agent is refused without "
              "--allow-software-agent",
              code == 2 and "person as the agent of record" in err)

        code, _, err = invoke(["--source", "ofac-sdn", "--dbname", DB,
                               "--agent", str(uuid.uuid4()),
                               "--archive-root", str(archive), "--dry-run"], fetcher)
        check("DR-0059", "an agent that is not registered is refused",
              code == 2 and "no pipeline_agent" in err)

        code, _, err = invoke(["--source", "ofac-sdn", "--dbname", DB,
                               "--agent", "not-a-uuid",
                               "--archive-root", str(archive), "--dry-run"], fetcher)
        check("DR-0059", "an agent id that is not a uuid is refused cleanly",
              code == 2 and "not a uuid" in err)

        # -- dry run: everything checked, nothing done -----------------------

        code, out, _ = invoke(["--source", "ofac-sdn", *base, "--dry-run"], fetcher)
        runs = conn.execute("SELECT count(*) FROM collector_run").fetchone()[0]
        check("OPS-001", "a dry run passes every check and writes nothing",
              code == 0 and runs == 0 and not fetcher.calls
              and all(loc in out for loc in ofac["run_locators"])
              and not archive.exists())

        # -- the archive root must be an archive or empty --------------------

        cluttered = work / "cluttered"
        cluttered.mkdir()
        (cluttered / "permanent").mkdir()
        (cluttered / "permanent" / "notes.txt").write_text("not an archive")
        code, _, err = invoke(["--source", "ofac-sdn", "--dbname", DB,
                               "--agent", person, "--archive-root", str(cluttered)],
                              fetcher)
        check("DR-0073", "a non-empty directory that is not an OCFL root is refused",
              code == 2 and "not an OCFL storage root" in err and not fetcher.calls)

        # -- an authorised run ----------------------------------------------

        code, out, err = invoke(["--source", "ofac-sdn", *base,
                                 "--user-agent", "UIW-test/0"], fetcher)
        check("OPS-001", "an authorised run completes", code == 0, )
        check("DR-0087 §2", "the run fetches exactly the listed run locators, "
              "in order, and nothing else",
              fetcher.calls == list(ofac["run_locators"]))

        row = conn.execute(
            "SELECT configuration, items_acquired, items_failed, collector_agent_id "
            "FROM collector_run").fetchone()
        check("DR-0070", "the run is recorded with its coverage",
              row is not None and row[1] == len(ofac["run_locators"]) and row[2] == 0)
        check("DR-0070", "the run's configuration records how it was invoked: "
              "candidate key, locators, user agent, verification date",
              row is not None
              and row[0].get("candidate_key") == "ofac-sdn"
              and row[0].get("run_locators") == list(ofac["run_locators"])
              and row[0].get("user_agent") == "UIW-test/0"
              and row[0].get("locator_verified") == ofac["locator_verified"].isoformat())
        check("DR-0087 §3", "the agent of record is the person given",
              row is not None and str(row[3]) == person)
        check("DR-0073", "an empty archive root was initialised as OCFL",
              (archive / "permanent" / "0=ocfl_1.1").exists()
              and (archive / "medium-term" / "0=ocfl_1.1").exists())
        check("DR-0066", "the run created no canonical knowledge",
              conn.execute("SELECT count(*) FROM documentary_assertion").fetchone()[0] == 0
              and conn.execute("SELECT count(*) FROM holding").fetchone()[0]
              == len(ofac["run_locators"]))

        # -- a second run into the same, now initialised, root ---------------

        code, _, _ = invoke(["--source", "ofac-sdn", *base], fetcher)
        check("DR-0073", "an existing OCFL root is reused, not re-initialised",
              code == 0
              and conn.execute("SELECT count(*) FROM collector_run").fetchone()[0] == 2)

        # -- a failed fetch is recorded and surfaced, not hidden --------------

        partial = FixtureFetcher({ofac["run_locators"][0]: fixture_files[ofac["run_locators"][0]]})
        code, out, _ = invoke(["--source", "ofac-sdn", *base], partial)
        last = conn.execute(
            "SELECT items_acquired, items_failed FROM collector_run "
            "ORDER BY started_at DESC LIMIT 1").fetchone()
        check("PRES-007", "a run with failed acquisitions records them and exits "
              "non-zero without crashing",
              code == 1 and last == (1, len(ofac["run_locators"]) - 1)
              and "failed:" in out)

        # -- a paused source does not collect -------------------------------

        conn.execute("UPDATE source SET lifecycle_state = 'paused', "
                     "lifecycle_reason = 'test'")
        code, _, err = invoke(["--source", "ofac-sdn", *base], fetcher)
        check("DR-0067", "a paused source is refused before any fetch",
              code == 2 and "paused" in err)
        conn.execute("UPDATE source SET lifecycle_state = 'active'")

        # -- a candidate whose run locators are not verified cannot run -------

        commit(conn, [copy.deepcopy(eu)], [], person)
        import register
        import yaml
        unverified_dir = work / "candidates"
        unverified_dir.mkdir()
        stripped = {k: v for k, v in eu.items()
                    if k not in ("run_locators", "locator_verified",
                                 "verification_note", "_file")}
        (unverified_dir / "eu.yaml").write_text(yaml.safe_dump({"sources": [stripped]}))
        original_dir = register.CANDIDATES
        register.CANDIDATES = unverified_dir
        try:
            code, _, err = invoke(["--source", "eu-consolidated-list", *base,
                                   "--dry-run"], fetcher)
        finally:
            register.CANDIDATES = original_dir
        check("PRES-007", "a registered source whose candidate lists no verified "
              "run locators cannot be run",
              code == 2 and "no run_locators" in err and not fetcher.calls[len(ofac["run_locators"]) * 2:])

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
