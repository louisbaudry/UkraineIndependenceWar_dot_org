"""Read-only status tools for the archive — the logic behind the MCP server.

Kept free of the MCP SDK so it is testable with plain scripts and importable
by anything else that wants the same answers. `server.py` only wires these
functions to the protocol.

Two sources of truth, never mixed (CLAUDE.md, "Where state lives"):

- **The repository** — Decision Records, source candidates and registration
  classes. Always available.
- **The archive database** — what is actually registered and collected.
  Available only when libpq's standard environment names one (`PGDATABASE`).
  Without it, every field that would come from the database is `None`, which
  means *unknown*, never *no*: a session with no database must not be able to
  say "nothing has been collected" (CLAUDE.md, "What this repository is").

Nothing here writes. The database connection is opened read-only at the
server, so a bug in this module cannot register a source, start a run or
touch a holding: those stay a person's act (DR-0093 §3, OPS-001).
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Any

import psycopg

ROOT = Path(__file__).resolve().parent.parent
DR_DIR = ROOT / "docs" / "decision-records"

sys.path.insert(0, str(ROOT / "sources"))
from register import (  # noqa: E402  (path set up just above)
    RegistrationError, load_candidates, merge_class_defaults,
)

# `| [DR-0072](DR-0072-slug.md) | title | category | status | date |`
_REGISTER_ROW = re.compile(
    r"^\| \[(DR-\d{4})\]\(([^)]+)\) \| (.*?) \| (.*?) \| (.*?) \| (\S+) \|$")

# Header fields that sit on the first lines of every DR (DR-0046).
_HEADER_FIELD = re.compile(r"\*\*(Supersedes|Superseded by|Origin|Decided):\*\*"
                           r"\s*([^|\n]*?)\s*(?=\||$)", re.M)

# A source's long free-text fields are returned by get_source only; the list
# stays small enough to scan.
_LIST_FIELDS = ("key", "name", "class", "locator", "locator_verified",
                "collection_cadence", "capture_format", "default_access_tier",
                "rights_permission", "rights_review_state")


class ToolError(Exception):
    """A request the tools refuse, in words the caller can act on."""


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

def database_configured() -> bool:
    """True when libpq's environment names a database to read."""
    return bool(os.environ.get("PGDATABASE"))


def connect() -> psycopg.Connection | None:
    """A read-only connection, or None when no database is configured.

    Read-only is set on the session by the server
    (`default_transaction_read_only`), not by a convention in this module's
    queries, so the guarantee holds even if a later tool is written carelessly.
    Credentials come from the environment only and never appear in output.
    """
    if not database_configured():
        return None
    return psycopg.connect(options="-c default_transaction_read_only=on",
                           autocommit=True)


# ---------------------------------------------------------------------------
# Decision Records
# ---------------------------------------------------------------------------

def _register() -> list[dict[str, str]]:
    rows = []
    for line in (DR_DIR / "README.md").read_text().splitlines():
        m = _REGISTER_ROW.match(line)
        if m:
            rows.append({"id": m[1], "file": m[2], "title": m[3],
                         "category": m[4], "status": m[5], "decided": m[6]})
    return rows


def list_decisions(status: str | None = None,
                   query: str | None = None) -> list[dict[str, str]]:
    """Decision Records from the register, newest number last.

    `status` is a case-insensitive substring of the register's status column
    ("approved", "superseded" — which also finds "Approved — superseded by
    DR-nnnn" — or "proposed"); `query` a case-insensitive
    substring of the id, title or category. The register is the record of
    status — this never infers it from Git state (DR-0046).
    """
    rows = _register()
    if status:
        rows = [r for r in rows if status.lower() in r["status"].lower()]
    if query:
        q = query.lower()
        rows = [r for r in rows
                if q in f"{r['id']} {r['title']} {r['category']}".lower()]
    return rows


def get_decision(number: str, include_text: bool = False) -> dict[str, Any]:
    """One Decision Record: register row, header fields, and optionally text.

    `number` is `DR-0072`, `0072` or `72`. The register row is authoritative
    for status; the header fields (supersession, origin) are read from the
    file's own header block. `include_text` returns the whole record.
    """
    digits = re.sub(r"\D", "", number or "")
    if not digits or len(digits) > 4:
        raise ToolError(f"{number!r} is not a Decision Record number")
    wanted = f"DR-{int(digits):04d}"
    row = next((r for r in _register() if r["id"] == wanted), None)
    if row is None:
        raise ToolError(f"{wanted} is not in the register")
    path = (DR_DIR / row["file"]).resolve()
    if DR_DIR.resolve() not in path.parents or not path.is_file():
        raise ToolError(f"{wanted}'s register row points at a missing file")
    text = path.read_text()
    out: dict[str, Any] = dict(row)
    out["path"] = str(path.relative_to(ROOT))
    # Only the header block: a "**Supersedes:**" quoted in the body is not one.
    header = "\n".join(text.splitlines()[:12])
    out["header"] = {k.lower().replace(" ", "_"): v
                     for k, v in _HEADER_FIELD.findall(header)}
    if include_text:
        out["text"] = text
    return out


# ---------------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------------

def _merged_candidates() -> dict[str, dict[str, Any]]:
    sources, _dependence, classes = load_candidates()
    merged: dict[str, dict[str, Any]] = {}
    for s in sources:
        m = merge_class_defaults(s, classes)
        m["class"] = s.get("class")
        m["file"] = m.pop("_file", s.get("_file"))
        merged[s["key"]] = m
    return merged


def _registration(conn: psycopg.Connection, source: dict) -> dict[str, Any]:
    """What the database says about one candidate, by `(name, locator)` —
    the identity `collector/run.py` resolves on (see register.registered_id).
    """
    row = conn.execute(
        "SELECT s.id, s.lifecycle_state, s.rights_review_state, s.created_at, "
        "       count(r.id), max(r.started_at), "
        "       coalesce(sum(r.items_acquired), 0), "
        "       coalesce(sum(r.items_failed), 0), "
        "       coalesce(sum(r.bytes_preserved), 0) "
        "FROM source s LEFT JOIN collector_run r ON r.source_id = s.id "
        "WHERE s.name = %s AND s.locator IS NOT DISTINCT FROM %s "
        "GROUP BY s.id",
        (source["name"], source.get("locator"))).fetchone()
    if row is None:
        return {"registered": False}
    return {"registered": True, "lifecycle_state": row[1],
            "rights_review_state": row[2],
            "registered_at": row[3].isoformat(),
            "runs": row[4],
            "last_run_started": row[5].isoformat() if row[5] else None,
            "items_acquired": int(row[6]), "items_failed": int(row[7]),
            "bytes_preserved": int(row[8])}


def _unknown_registration() -> dict[str, Any]:
    return {"registered": None,
            "note": "no database configured: registration is unknown, "
                    "not 'no'. Set PGDATABASE (and PGHOST/PGUSER) to see it."}


def list_sources(registered: bool | None = None) -> list[dict[str, Any]]:
    """Every candidate source, with its registration state when knowable.

    `registered=True/False` filters on the database's answer and requires a
    database; asking for it without one is refused rather than answered
    from nothing.
    """
    candidates = _merged_candidates()
    conn = connect()
    if registered is not None and conn is None:
        raise ToolError("filtering on registration needs a database: "
                        "PGDATABASE is not set")
    try:
        out = []
        for key, src in candidates.items():
            entry = {f: src.get(f) for f in _LIST_FIELDS}
            entry["file"] = src["file"]
            entry.update(_registration(conn, src) if conn
                         else _unknown_registration())
            if registered is None or entry["registered"] == registered:
                out.append(entry)
        return out
    finally:
        if conn:
            conn.close()


def get_source(key: str) -> dict[str, Any]:
    """One candidate in full (class defaults merged, as `register.py` sees
    it), plus its registration state and its five most recent collector runs
    when a database is configured. Run rows carry counts and outcomes only."""
    candidates = _merged_candidates()
    if key not in candidates:
        raise ToolError(f"unknown source key {key!r}; list_sources gives the "
                        f"{len(candidates)} known keys")
    src = candidates[key]
    out = {k: v for k, v in src.items() if not k.startswith("_")}
    conn = connect()
    try:
        out["registration"] = (_registration(conn, src) if conn
                               else _unknown_registration())
        if conn and out["registration"]["registered"]:
            rows = conn.execute(
                "SELECT r.started_at, r.ended_at, r.items_discovered, "
                "       r.items_acquired, r.items_skipped, r.items_failed, "
                "       r.bytes_preserved, r.outage_note "
                "FROM collector_run r JOIN source s ON s.id = r.source_id "
                "WHERE s.name = %s AND s.locator IS NOT DISTINCT FROM %s "
                "ORDER BY r.started_at DESC LIMIT 5",
                (src["name"], src.get("locator"))).fetchall()
            out["recent_runs"] = [
                {"started_at": r[0].isoformat(),
                 "ended_at": r[1].isoformat() if r[1] else None,
                 "items_discovered": r[2], "items_acquired": r[3],
                 "items_skipped": r[4], "items_failed": r[5],
                 "bytes_preserved": int(r[6]), "outage_note": r[7]}
                for r in rows]
    finally:
        if conn:
            conn.close()
    return out


# ---------------------------------------------------------------------------
# Archive status
# ---------------------------------------------------------------------------

def archive_status() -> dict[str, Any]:
    """Aggregate counts from the archive database, or `{"database": None}`.

    Counts only: no holding, locator or row from any source is returned, so
    nothing here can carry a person's data out of the archive (DR-0071(b),
    POL-0001). The numbers are what `collector_run`, `holding` and
    `acquisition_attempt` hold *now* — CLAUDE.md's own status claims are
    deliberately not repeated, because this is the check they say to make.
    """
    conn = connect()
    if conn is None:
        return {"database": None,
                "note": "no database configured (PGDATABASE unset): the "
                        "archive's state is unknown from here, not empty."}
    try:
        def rows(sql: str) -> list[tuple]:
            return conn.execute(sql).fetchall()

        sources = dict(rows("SELECT lifecycle_state, count(*) FROM source "
                            "GROUP BY 1"))
        runs = rows("SELECT count(*), max(started_at), "
                    "coalesce(sum(items_acquired),0), "
                    "coalesce(sum(items_failed),0), "
                    "coalesce(sum(bytes_preserved),0) FROM collector_run")[0]
        return {
            "database": "connected, read-only",
            "sources_by_lifecycle": sources,
            "collector_runs": {
                "runs": runs[0],
                "last_started": runs[1].isoformat() if runs[1] else None,
                "items_acquired": int(runs[2]),
                "items_failed": int(runs[3]),
                "bytes_preserved": int(runs[4])},
            "holdings_by_retention_tier": dict(rows(
                "SELECT retention_tier::text, count(*) FROM holding "
                "GROUP BY 1")),
            "holdings_by_rights_review_state": dict(rows(
                "SELECT rights_review_state, count(*) FROM holding "
                "GROUP BY 1")),
            "acquisition_attempts_by_outcome": dict(rows(
                "SELECT outcome, count(*) FROM acquisition_attempt "
                "GROUP BY 1")),
        }
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Documentation search
# ---------------------------------------------------------------------------

# Only these places are searchable: published governance and working text.
# Candidate YAML, collected material and anything outside the repository's
# documentation never enter a result, so a query cannot be used to read them.
SEARCH_SCOPES: dict[str, tuple[str, ...]] = {
    "decisions": ("docs/decision-records/DR-*.md",),
    "working-papers": ("docs/phase-3/working-papers/*.md",),
    "sources": ("docs/sources/*.md",),
    "runbooks": ("docs/runbooks/*.md",),
    "legal": ("docs/legal/*.md",),
    "glossary": ("GLOSSARY.md",),
}
_MAX_WORDS = 8
_MAX_QUERY = 200
_SNIPPET = 240
_HEADING = re.compile(r"^#{1,6}\s+(.*)")


def _scope_files(scope: str | None) -> list[Path]:
    if scope is not None and scope not in SEARCH_SCOPES:
        raise ToolError(f"unknown scope {scope!r}; choose one of "
                        f"{', '.join(sorted(SEARCH_SCOPES))}")
    globs = (SEARCH_SCOPES[scope] if scope
             else [g for gs in SEARCH_SCOPES.values() for g in gs])
    return sorted({f for g in globs for f in ROOT.glob(g) if f.is_file()})


def _snippet(line: str, words: list[str]) -> str:
    line = line.strip()
    if len(line) <= _SNIPPET:
        return line
    at = min((i for i in (line.lower().find(w) for w in words) if i >= 0),
             default=0)
    start = max(0, at - _SNIPPET // 3)
    end = min(len(line), start + _SNIPPET)
    return ("\u2026" if start else "") + line[start:end] + (
        "\u2026" if end < len(line) else "")


def search_docs(query: str, scope: str | None = None,
                limit: int = 10) -> list[dict[str, Any]]:
    """All-words, case-insensitive search of the documentation.

    A file matches only if every word of `query` appears in it. Files rank by
    lines holding every word, then capped occurrences, with a bonus for words
    in the first line (the title); ties break by path, so the same query always answers the same way. Each
    hit gives the best line (most distinct query words, earliest on a tie),
    its number and the nearest heading above it. `scope` narrows to one of
    `SEARCH_SCOPES`. No index and no state: every call reads the files, so a
    result can never be staler than the checkout.
    """
    words = (query or "").lower().split()
    if not words:
        raise ToolError("query is empty")
    if len(query) > _MAX_QUERY or len(words) > _MAX_WORDS:
        raise ToolError(f"query too long: at most {_MAX_WORDS} words and "
                        f"{_MAX_QUERY} characters")
    limit = max(1, min(int(limit), 50))
    hits = []
    for path in _scope_files(scope):
        lines = path.read_text().splitlines()
        lowered = [ln.lower() for ln in lines]
        text = "\n".join(lowered)
        if not all(w in text for w in words):
            continue
        # Words sharing a line say more than words scattered through a long
        # file, so lines holding every word dominate; raw occurrences are
        # capped so a long document cannot win on length alone.
        best_i, best_n, together = 0, -1, 0
        for i, ln in enumerate(lowered):
            n = sum(1 for w in words if w in ln)
            together += n == len(words)
            if n > best_n:
                best_i, best_n = i, n
        score = (10 * together + min(sum(text.count(w) for w in words), 50)
                 + 20 * sum(1 for w in words if lowered and w in lowered[0]))
        heading = next((m[1] for ln in reversed(lines[:best_i + 1])
                        if (m := _HEADING.match(ln))), None)
        hits.append({"path": str(path.relative_to(ROOT)), "line": best_i + 1,
                     "heading": heading, "score": score,
                     "snippet": _snippet(lines[best_i], words)})
    hits.sort(key=lambda h: (-h["score"], h["path"]))
    return hits[:limit]


# ---------------------------------------------------------------------------
# Glossary
# ---------------------------------------------------------------------------

# `**Term**` or `**Term** (`alias`)` alone on a line opens an entry (GLOSSARY.md).
_TERM_LINE = re.compile(r"^\*\*([^*]+)\*\*(\s*\(.*\))?\s*$")


def _glossary() -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    section = ""
    current: dict[str, Any] | None = None
    for line in (ROOT / "GLOSSARY.md").read_text().splitlines():
        if line.startswith("## "):
            section, current = line[3:].strip(), None
            continue
        m = _TERM_LINE.match(line)
        if m:
            current = {"term": (m[1] + (m[2] or "")).strip(),
                       "section": section, "lines": []}
            entries.append(current)
        elif current is not None:
            current["lines"].append(line)
    return [{"term": e["term"], "section": e["section"],
             "definition": " ".join(" ".join(e["lines"]).split())}
            for e in entries]


def lookup_term(term: str) -> list[dict[str, str]]:
    """Glossary entries for `term`.

    An exact (case-insensitive) match on the entry's name wins and is returned
    alone; otherwise every entry whose name contains `term`, at most five.
    Refuses an empty term and an unknown one, naming the nearest entries so
    the caller can retry, rather than answering from memory.
    """
    needle = (term or "").strip().lower()
    if not needle:
        raise ToolError("term is empty")
    entries = _glossary()
    exact = [e for e in entries if e["term"].lower() == needle
             or e["term"].lower().startswith(needle + " (")]
    if exact:
        return exact
    partial = [e for e in entries if needle in e["term"].lower()][:5]
    if partial:
        return partial
    raise ToolError(f"no glossary entry for {term!r}; search_docs with "
                    f"scope='glossary' searches the definitions as well")


__all__ = ["ToolError", "RegistrationError", "SEARCH_SCOPES",
           "archive_status", "database_configured", "get_decision",
           "get_source", "list_decisions", "list_sources", "lookup_term",
           "search_docs"]
