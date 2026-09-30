#!/usr/bin/env python3
"""Detect a Decision Record numbered before merge (DR-0095, DR-0102, issue #86).

The rule those records enact: draft as ``DR-pending-<slug>.md`` and take the
real number once, at merge, from ``origin/main``'s register. The number is
therefore never legitimately present on a branch that is not on ``main``.

The test is the *presence of the filename on the base ref*, not any mention of
a number: citations of existing DRs are everywhere in this repository and must
never trip it. A ``DR-nnnn-*.md`` file in the working tree that ``origin/main``
does not carry is a number taken early.

Scope: DR filenames only. CDR-P3-nn numbers live inside working papers, not in
filenames, and are not checked here.

Exit status is non-zero when any such file is found.

Usage: python3 docs/decision-records/check_numbering.py [--base REF] [--no-fetch]
"""

import argparse
import subprocess
import sys
from pathlib import Path

DR_GLOB = "DR-[0-9][0-9][0-9][0-9]-*.md"


def git(*args, cwd=None, check=True):
    return subprocess.run(["git", *args], cwd=cwd, check=check,
                          capture_output=True, text=True)


def unmerged_numbered(repo, base="origin/main"):
    """Return repo-relative paths of numbered DR files absent from `base`."""
    root = Path(git("rev-parse", "--show-toplevel", cwd=repo).stdout.strip())
    found = []
    for f in sorted((root / "docs" / "decision-records").glob(DR_GLOB)):
        rel = f.relative_to(root).as_posix()
        if git("cat-file", "-e", f"{base}:{rel}", cwd=root, check=False).returncode != 0:
            found.append(rel)
    return found


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--base", default="origin/main")
    ap.add_argument("--no-fetch", action="store_true",
                    help="skip `git fetch origin` (offline; base ref may be stale)")
    args = ap.parse_args(argv)
    if not args.no_fetch:
        remote, _, branch = args.base.partition("/")
        r = git("fetch", remote, branch, "-q", check=False)
        if r.returncode != 0:
            print(f"ERROR: could not fetch {args.base}: {r.stderr.strip()}", file=sys.stderr)
            return 2
    bad = unmerged_numbered(".", args.base)
    for f in bad:
        print(f"UNMERGED NUMBERED DR: {f} -- rename to DR-pending-<slug>.md; "
              "the number is assigned at merge (DR-0095, DR-0102)")
    if not bad:
        print(f"0 unmerged numbered DR file(s) against {args.base}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
