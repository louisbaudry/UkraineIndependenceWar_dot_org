#!/usr/bin/env python3
"""Rebuild identifier resolution from a dump alone — SPEC-0007 §10 (PRES-009).

Imports nothing from this project: no `register`, no `ark`, no database. Given
a preservation dump directory and an ARK, it answers what that identifier
resolves to, using only the standard library and SPEC-0007 §2.4 and §6.1.

If this stops working, a successor with the archive but not the code can no
longer honour the citations the project published. That is what it is for.

Usage:  python3 rebuild.py <dump-dir> <ark>
"""

import json
import re
import sys
from pathlib import Path

XDIGIT = "0123456789bcdfghjkmnpqrstvwxz"
MAX_HOPS = 64


def normalise(ark):
    """SPEC-0007 §2.4, reimplemented from the specification."""
    text = ark.strip().split("?", 1)[0].split("#", 1)[0]
    marker = text.lower().find("ark:")
    if marker == -1:
        raise ValueError("not an ARK")
    text = text[marker:].replace("-", "")
    text = re.sub(r"/{2,}", "/", text.replace("ark://", "ark:/"))
    text = re.sub(r"\.{2,}", ".", text).rstrip("/.")
    label, _, rest = text.partition(":")
    naan, _, name = rest.lstrip("/").partition("/")
    return f"{label.lower()}:/{naan.lower()}/{name}"


def check_character(naan, name):
    covered = f"{naan}/{name}"
    total = sum((XDIGIT.index(c) if c in XDIGIT else 0) * i
                for i, c in enumerate(covered, start=1))
    return XDIGIT[total % len(XDIGIT)]


def rows(dump, table):
    path = Path(dump) / "data" / f"{table}.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.open() if line.strip()]


def resolve(dump, query):
    base = normalise(query)
    base = re.sub(r"\.v\d+$", "", base)
    register = {r["ark"]: r for r in rows(dump, "public_identifier")}
    subjects = {r["ark"]: r for r in rows(dump, "public_identifier_subject")}

    record = register.get(base)
    if record is None:
        return {"status": 404, "reason": "never issued"}

    hops, terminal = 0, record
    while terminal["disposition"] == "redirect" and hops <= MAX_HOPS:
        hops += 1
        terminal = register[terminal["successor_ark"]]

    status = {"active": 200, "redirect": 301, "disambiguation": 200,
              "tombstone": 410, "restricted": 403}[record["disposition"]]
    answer = {"status": status, "ark": base,
              "disposition": record["disposition"],
              "terminal_ark": terminal["ark"], "hops": hops}
    subject = subjects.get(terminal["ark"])
    if subject:
        answer["subject"] = f"{subject['subject_table']}/{subject['subject_id']}"
    return answer


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    dump, query = sys.argv[1], sys.argv[2]
    naan, name = normalise(query)[len("ark:/"):].split("/", 1)
    name = re.sub(r"\.v\d+$", "", name)
    if check_character(naan, name[:-1]) != name[-1]:
        print(json.dumps({"status": 400, "reason": "check character fails"}))
        return 0
    print(json.dumps(resolve(dump, query), default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
