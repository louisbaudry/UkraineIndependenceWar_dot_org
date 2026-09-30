#!/usr/bin/env python3
"""Tests for docs/decision-records/check_numbering.py (issue #86).

Real git repositories in a temp dir (an origin plus a clone), no mocks.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_numbering as cn  # noqa: E402

fails = 0


def check(req, name, cond):
    global fails
    print(f"{'PASS' if cond else 'FAIL'} [{req}] {name}")
    fails += 0 if cond else 1


def sh(*a, cwd):
    subprocess.run(a, cwd=cwd, check=True, capture_output=True)


with tempfile.TemporaryDirectory() as t:
    origin, work = Path(t, "origin"), Path(t, "work")
    sh("git", "init", "-q", "-b", "main", str(origin), cwd=t)
    dr = origin / "docs" / "decision-records"
    dr.mkdir(parents=True)
    (dr / "DR-0001-first.md").write_text("# DR-0001\n")
    for k, v in (("user.email", "t@example.org"), ("user.name", "t")):
        sh("git", "config", k, v, cwd=origin)
    sh("git", "add", "-A", cwd=origin)
    sh("git", "commit", "-qm", "init", cwd=origin)
    sh("git", "clone", "-q", str(origin), str(work), cwd=t)
    wdr = work / "docs" / "decision-records"

    check("DR-0102", "clean checkout of main reports nothing",
          cn.unmerged_numbered(work) == [])

    (wdr / "DR-pending-topic.md").write_text("Cites DR-0001, DR-0093, DR-0199 in prose.\n")
    check("DR-0102", "pending-named draft citing numbers in prose is not flagged",
          cn.unmerged_numbered(work) == [])

    (wdr / "DR-pending-topic.md").rename(wdr / "DR-0199-topic.md")
    check("DR-0102", "numbered file absent from origin/main is flagged",
          cn.unmerged_numbered(work) == ["docs/decision-records/DR-0199-topic.md"])
    script = Path(cn.__file__)
    rc = subprocess.run([sys.executable, str(script)], cwd=work,
                        capture_output=True).returncode
    check("DR-0102", "CLI (with real fetch) exits 1 on the breach", rc == 1)

    (wdr / "DR-0199-topic.md").rename(wdr / "DR-pending-topic.md")
    check("DR-0102", "renaming back to pending clears the finding",
          cn.unmerged_numbered(work) == [])
    rc = subprocess.run([sys.executable, str(script)], cwd=work,
                        capture_output=True).returncode
    check("DR-0102", "CLI exits 0 once drafted correctly", rc == 0)

print("FAILED" if fails else "ALL PASSED")
sys.exit(1 if fails else 0)
