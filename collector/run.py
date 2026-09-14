#!/usr/bin/env python3
"""Run one source's collection from the command line.

    python3 collector/run.py --source ofac-sdn --dbname uiw \\
            --agent <pipeline_agent uuid> --archive-root /opt/uiw-archive

This is the operator's entry point to `Collector.run()`. It does four things
before it fetches anything, and refuses at the first one that fails:

1. Finds the candidate entry for `--source` in `sources/candidates/` and
   takes its `run_locators` — the exact URLs a run is authorised for. A
   candidate with no verified run locators cannot be run; verifying them
   and listing them is a registry edit, not a run parameter.
2. Finds the *registered* source that entry corresponds to. An unregistered
   candidate is refused: registration is the authorisation (OPS-001,
   DR-0071(a)), and this script must not become a way around it.
3. Checks that `--agent` is a registered pipeline agent, and a person unless
   `--allow-software-agent` is given (DR-0093 §3: the first runs are manual
   acts with a person as the agent of record).
4. Opens the OCFL storage roots under `--archive-root`, initialising an
   empty directory and refusing a non-empty one that is not an OCFL root.

`--dry-run` does all four and stops, printing what a run would attempt.

For a real run, it also ensures a versioned **software** `pipeline_agent`
exists (self-registered by name and version, no human step) and passes it
to `Collector` separately from `--agent`: the software agent names every
preservation event this run produces, while `--agent` stays the run's
human agent of record (DR-0093 §3), unchanged
(DR-pending-collection-run-two-agents). This is not a fifth refusal check —
it never blocks a run — so `--dry-run` does not perform it.

What it does NOT do: parse anything it fetches, create canonical knowledge,
or decide whether a capture is worth keeping. A completed run with zero
documentary assertions is the expected result (DR-0066).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import psycopg

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "collector"))
sys.path.insert(0, str(ROOT / "storage"))
sys.path.insert(0, str(ROOT / "sources"))

from fetch import Fetcher, HttpFetcher  # noqa: E402
from ocfl import OcflError, StorageRoot  # noqa: E402
from pipeline import (  # noqa: E402
    Collector, PolicyViolation, SOFTWARE_AGENT_NAME, SOFTWARE_AGENT_VERSION,
    ensure_software_agent,
)
from register import load_candidates, validate  # noqa: E402

DEFAULT_USER_AGENT = (
    "UIW-collector/0.1 "
    "(+https://github.com/louisbaudry/UkraineIndependenceWar_dot_org)"
)


class Refused(Exception):
    """The run must not proceed, and the message says why."""


# -- the four checks --------------------------------------------------------

def find_candidate(key: str) -> dict:
    sources, dependence = load_candidates()
    problems = validate(sources, dependence)
    if problems:
        raise Refused("the candidate file does not validate:\n  "
                      + "\n  ".join(problems))
    matches = [s for s in sources if s.get("key") == key]
    if not matches:
        known = ", ".join(sorted(s["key"] for s in sources))
        raise Refused(f"no candidate with key {key!r}; known keys: {known}")
    candidate = matches[0]
    if not candidate.get("run_locators"):
        raise Refused(
            f"{key} has no run_locators. A run is authorised for exactly the "
            "locators listed and verified in the candidate file; verify them "
            "and list them there first (see sources/README.md)")
    return candidate


def resolve_registered_source(conn: psycopg.Connection, candidate: dict) -> tuple[str, str]:
    """The registry row this candidate was registered as. Refuses otherwise."""
    rows = conn.execute(
        "SELECT id, lifecycle_state FROM source WHERE name = %s AND locator = %s",
        (candidate["name"], candidate.get("locator")),
    ).fetchall()
    if not rows:
        raise Refused(
            f"{candidate['key']} is not registered. Registration is the act "
            "that authorises collection (OPS-001, DR-0071(a)); run "
            f"sources/register.py --commit --only {candidate['key']} first")
    if len(rows) > 1:
        raise Refused(
            f"{candidate['key']} matches {len(rows)} registered sources by name "
            "and locator; resolve the duplicate in the registry before running")
    source_id, state = rows[0]
    return str(source_id), state


def check_agent(conn: psycopg.Connection, agent_id: str,
                allow_software: bool) -> tuple[str, str]:
    try:
        row = conn.execute(
            "SELECT kind, name FROM pipeline_agent WHERE id = %s", (agent_id,)
        ).fetchone()
    except psycopg.errors.InvalidTextRepresentation as exc:
        raise Refused(f"--agent {agent_id!r} is not a uuid") from exc
    if row is None:
        raise Refused(
            f"no pipeline_agent with id {agent_id}. Insert one first: "
            "INSERT INTO pipeline_agent (id, kind, name) VALUES "
            "(gen_random_uuid(), 'person', '<name>') RETURNING id")
    kind, name = row
    if kind != "person" and not allow_software:
        raise Refused(
            f"agent {name!r} is a {kind} agent. DR-0093 §3 makes the first runs "
            "manual acts with a person as the agent of record; pass "
            "--allow-software-agent only once automation has been decided")
    return kind, name


def open_root(path: Path, tier: str) -> StorageRoot:
    root = StorageRoot(path, tier)
    if root.namaste.exists():
        return root
    if path.exists() and any(path.iterdir()):
        raise Refused(
            f"{path} is not empty and is not an OCFL storage root; refusing to "
            "write an archive into it")
    root.initialize()
    return root


def open_roots(archive_root: Path) -> tuple[dict[str, StorageRoot], Path]:
    roots = {
        "permanent": open_root(archive_root / "permanent", "permanent"),
        "medium-term": open_root(archive_root / "medium-term", "medium-term"),
    }
    return roots, archive_root / "quarantine"


def git_commit() -> str | None:
    try:
        out = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                             capture_output=True, text=True, check=True)
        return out.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


# -- the run ----------------------------------------------------------------

def main(argv: list[str] | None = None, fetcher: Fetcher | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", required=True, metavar="KEY",
                        help="candidate key, e.g. ofac-sdn")
    parser.add_argument("--dbname", required=True)
    parser.add_argument("--agent", required=True, metavar="UUID",
                        help="pipeline_agent performing the run")
    parser.add_argument("--archive-root", required=True, type=Path,
                        help="directory holding permanent/, medium-term/, quarantine/")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT)
    parser.add_argument("--timeout", type=float, default=300.0,
                        help="per-request timeout in seconds")
    parser.add_argument("--allow-software-agent", action="store_true")
    parser.add_argument("--dry-run", action="store_true",
                        help="check everything, fetch nothing, write nothing")
    args = parser.parse_args(argv)

    try:
        candidate = find_candidate(args.source)
        with psycopg.connect(dbname=args.dbname, autocommit=True) as conn:
            source_id, state = resolve_registered_source(conn, candidate)
            agent_kind, agent_name = check_agent(conn, args.agent,
                                                 args.allow_software_agent)
            if state != "active":
                raise Refused(f"{args.source} is registered but {state}; a "
                              f"{state} source does not collect (DR-0067)")

            locators = list(candidate["run_locators"])
            verified = candidate.get("locator_verified")
            print(f"source     {args.source}  ({source_id})")
            print(f"agent      {agent_name}  [{agent_kind}]  {args.agent}")
            print(f"locators   {len(locators)}, verified {verified}")
            for locator in locators:
                print(f"           {locator}")
            print(f"user-agent {args.user_agent}")
            print(f"archive    {args.archive_root}")

            if args.dry_run:
                print("\ndry run: nothing fetched, nothing written")
                return 0

            roots, quarantine = open_roots(args.archive_root)
            # DR-pending-collection-run-two-agents: --agent stays the run's
            # agent of record (DR-0093 §3); the preservation events this run
            # produces name a separate, versioned software agent instead --
            # self-registered, since a software agent's identity is its own
            # declared version, not a human decision (unlike --agent).
            software_agent_id = ensure_software_agent(conn)
            print(f"software   {SOFTWARE_AGENT_NAME}  {SOFTWARE_AGENT_VERSION}  "
                  f"{software_agent_id}")
            configuration = {
                "invoked_by": "collector/run.py",
                "candidate_key": args.source,
                "candidate_file": candidate.get("_file"),
                "locator_verified": verified.isoformat() if verified else None,
                "run_locators": locators,
                "user_agent": args.user_agent,
                "timeout_seconds": args.timeout,
                "code_commit": git_commit(),
                "software_agent_id": software_agent_id,
            }
            collector = Collector(
                conn, fetcher or HttpFetcher(args.user_agent, timeout=args.timeout),
                quarantine, roots, args.agent, software_agent_id,
            )
            run_id = collector.run(source_id, locators, configuration)

            row = conn.execute(
                "SELECT items_discovered, items_acquired, items_skipped, "
                "items_failed, bytes_preserved, failure_details, "
                "ended_at - started_at FROM collector_run WHERE id = %s",
                (run_id,),
            ).fetchone()
            discovered, acquired, skipped, failed, nbytes, failures, took = row
            print(f"\nrun {run_id}")
            print(f"  discovered {discovered}  acquired {acquired}  "
                  f"skipped {skipped}  failed {failed}")
            print(f"  bytes preserved {nbytes}  in {took}")
            for failure in failures or []:
                print(f"  failed: {failure.get('locator')}  "
                      f"{failure.get('error') or failure.get('detail') or failure}")
            print("  documentary assertions created: 0 (by design, DR-0066)")
            # A failed acquisition is a recorded outcome, not a crash (PRES-007),
            # but an operator should see it in the exit status.
            return 1 if failed else 0

    except (Refused, PolicyViolation, OcflError) as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
