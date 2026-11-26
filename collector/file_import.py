#!/usr/bin/env python3
"""Import a register export a person downloaded by hand (DR-0118, issue #197).

    python3 collector/file_import.py --source ua-nsdc-sanctions-legal-entities \\
            --file ~/Downloads/legal_subjects.csv \\
            --downloaded-at 2026-11-26T14:05:00+01:00 --stated-count 9682 \\
            --dbname uiw --agent <pipeline_agent uuid> --archive-root /opt/uiw-archive

The operator's entry point to `Collector.import_file()`, for sources the
collector cannot fetch itself (the NSDC register's Cloudflare challenge
refuses every automated session). It refuses, before anything is written:

1. a candidate with no recorded export header (``export_checks.EXPORT_HEADERS``);
2. ``ua-nsdc-sanctions-individuals``, held until DR-0072's successor is
   recorded (DR-0118 Decision 4);
3. a candidate that is not registered and active (OPS-001, DR-0071(a));
4. an ``--agent`` that is not a registered person (DR-0093 §3: each import is
   a separate human act, and the person is its agent of record and the one
   recorded as having downloaded the file);
5. an ``--export-url`` that is not one of the candidate's ``run_locators``
   (defaults to the only one when there is exactly one);
6. a ``--downloaded-at`` without a time zone, or in the future;
7. a directory that is not an OCFL archive.

The file's own checks (empty, not UTF-8, wrong header, more records than
``--stated-count``) are made by the collector and recorded as a failed
attempt on the run, not refused here: a refused file is part of the coverage
record (PRES-007). ``--stated-count`` is the record count the register's page
showed when the file was downloaded.

``--dry-run`` makes checks 1-6, reads and hashes the file, prints what an
import would record, and writes nothing.

What it does not do: download anything, parse records into the store, or
register a source. A completed import creates zero documentary assertions
(DR-0066).
"""

from __future__ import annotations

import argparse
import signal
import sys
from datetime import datetime, timezone
from pathlib import Path

import psycopg

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "collector"))
sys.path.insert(0, str(ROOT / "storage"))
sys.path.insert(0, str(ROOT / "sources"))

from export_checks import (  # noqa: E402
    EXPORT_HEADERS, HELD_UNTIL_DR0072_SUCCESSOR, check_export, read_hashed,
)
from fetch import FixtureFetcher  # noqa: E402
from ocfl import OcflError  # noqa: E402
from pipeline import (  # noqa: E402
    Collector, PolicyViolation, SOFTWARE_AGENT_NAME, SOFTWARE_AGENT_VERSION,
    ensure_software_agent,
)
from run import (  # noqa: E402
    Refused, check_agent, find_candidate, git_commit, open_roots,
    resolve_registered_source,
)


def parse_downloaded_at(value: str, now: datetime | None = None) -> datetime:
    """Parse ``--downloaded-at``, refusing a naive or future time.

    Args:
        value: an ISO 8601 timestamp with an offset, e.g. ``2026-11-26T14:05+01:00``.
        now: the current time; a parameter so tests can fix it.

    Returns:
        The timezone-aware download time.

    Raises:
        Refused: the value is malformed, has no time zone, or is in the future.
    """
    try:
        when = datetime.fromisoformat(value)
    except ValueError as exc:
        raise Refused(f"--downloaded-at {value!r} is not an ISO 8601 timestamp") from exc
    if when.tzinfo is None:
        raise Refused("--downloaded-at needs a time zone, e.g. +01:00 or Z")
    if when > (now or datetime.now(timezone.utc)):
        raise Refused("--downloaded-at is in the future")
    return when


def choose_export_url(candidate: dict, given: str | None) -> str:
    """The export URL to record: one of the candidate's verified run locators.

    Raises:
        Refused: ``given`` is not a run locator, or none was given and the
            candidate has more than one.
    """
    locators = list(candidate.get("run_locators") or [])
    if given is None:
        if len(locators) != 1:
            raise Refused(f"{candidate['key']} has {len(locators)} run locators; "
                          "name the one the file came from with --export-url")
        return locators[0]
    if given not in locators:
        raise Refused(f"--export-url {given} is not one of {candidate['key']}'s "
                      "verified run_locators")
    return given


def main(argv: list[str] | None = None) -> int:
    """Run the command; returns 0 imported, 1 file refused or failed, 2 refused."""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", required=True, metavar="KEY")
    parser.add_argument("--file", required=True, type=Path)
    parser.add_argument("--downloaded-at", required=True, metavar="ISO8601")
    parser.add_argument("--stated-count", required=True, type=int,
                        help="records the register stated when you downloaded the file")
    parser.add_argument("--export-url", help="which run locator the file came from")
    parser.add_argument("--dbname", required=True)
    parser.add_argument("--agent", required=True, metavar="UUID",
                        help="the person who downloaded the file (a pipeline_agent)")
    parser.add_argument("--archive-root", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    try:
        if args.source in HELD_UNTIL_DR0072_SUCCESSOR:
            raise Refused(f"{args.source} is held until DR-0072's successor is "
                          "recorded (DR-0118 Decision 4)")
        header = EXPORT_HEADERS.get(args.source)
        if header is None:
            raise Refused(f"no export header is recorded for {args.source}; this "
                          "command imports only the sources DR-0118 covers")
        if args.stated_count < 1:
            raise Refused("--stated-count must be the register's stated count, at least 1")
        downloaded_at = parse_downloaded_at(args.downloaded_at)
        candidate = find_candidate(args.source)
        export_url = choose_export_url(candidate, args.export_url)
        if not args.file.is_file():
            raise Refused(f"{args.file} is not a file")

        with psycopg.connect(dbname=args.dbname, autocommit=True) as conn:
            source_id, state = resolve_registered_source(conn, candidate)
            if state != "active":
                raise Refused(f"{args.source} is registered but {state}")
            _, agent_name = check_agent(conn, args.agent, allow_software=False)

            print(f"source        {args.source}  ({source_id})")
            print(f"downloaded by {agent_name}  {args.agent}")
            print(f"downloaded at {downloaded_at.isoformat()}")
            print(f"export url    {export_url}")
            if args.dry_run:
                data, sha = read_hashed(args.file)
                records, refusal = check_export(data, header, args.stated_count)
                print(f"file          {args.file.name}  {len(data)} bytes  sha256 {sha}")
                print(f"records       {records} of {args.stated_count} stated")
                print(f"checks        {'REFUSED: ' + refusal if refusal else 'pass'}")
                print("\ndry run: nothing written")
                return 1 if refusal else 0

            roots, quarantine = open_roots(args.archive_root)
            software_agent_id = ensure_software_agent(conn)
            print(f"software      {SOFTWARE_AGENT_NAME}  {SOFTWARE_AGENT_VERSION}")
            configuration = {
                "invoked_by": "collector/file_import.py",
                "candidate_key": args.source,
                "candidate_file": candidate.get("_file"),
                "code_commit": git_commit(),
                "software_agent_id": software_agent_id,
            }
            # The collector needs a fetcher by construction; an import fetches
            # nothing, so it gets one that holds no locators at all.
            collector = Collector(conn, FixtureFetcher({}), quarantine, roots,
                                  args.agent, software_agent_id)
            run_id = collector.import_file(
                source_id, args.file, export_url, agent_name, downloaded_at,
                header, args.stated_count, configuration)
            acquired, skipped, failed, failures = conn.execute(
                "SELECT items_acquired, items_skipped, items_failed, failure_details "
                "FROM collector_run WHERE id = %s", (run_id,)).fetchone()
            print(f"\nrun {run_id}")
            print(f"  acquired {acquired}  unchanged/skipped {skipped}  failed {failed}")
            for failure in failures or []:
                print(f"  failed: {failure.get('error')}")
            print("  documentary assertions created: 0 (by design, DR-0066)")
            return 1 if failed else 0

    except KeyboardInterrupt:
        print("\ninterrupted: the run was closed with a note", file=sys.stderr)
        return 130
    except (Refused, PolicyViolation, OcflError) as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2


def _terminate_as_interrupt(signum, frame):  # pragma: no cover - signal glue
    """Treat SIGTERM like Ctrl-C so `kill` also closes the run (issue #174)."""
    raise KeyboardInterrupt


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, _terminate_as_interrupt)
    sys.exit(main())
