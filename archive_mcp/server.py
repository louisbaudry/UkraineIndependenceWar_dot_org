#!/usr/bin/env python3
"""MCP server exposing the archive's read-only status tools to Claude.

Read-only by construction: it registers nothing, collects nothing and writes
nothing, because registration is the act that authorises collection
(OPS-001), a person is the agent of record for a run (DR-0093 §3), and
Gates 2 and 3 are human decisions (DR-0066). Any write tool would be a new
decision first.

Uses the official `mcp` Python SDK (`archive_mcp/requirements.txt`), a runtime
dependency the founder approved for this component on 2026-10-25 (CLAUDE.md:
adding one is the founder's call). The rest of the repository does not need it.

Run (stdio, which is how Claude launches an MCP server):

    python3 archive_mcp/server.py

See `archive_mcp/README.md` for registering it with Claude and for pointing
it at a database.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp.server.mcpserver import MCPServer  # noqa: E402
from mcp.server.mcpserver.exceptions import ToolError  # noqa: E402
from mcp.types import ToolAnnotations  # noqa: E402

from archive_mcp import tools  # noqa: E402

INSTRUCTIONS = (
    "Read-only view of the Ukraine Independence War archive project: its "
    "Decision Records, candidate sources and, when a database is "
    "configured, what has actually been registered and collected. Check "
    "state here before repeating any claim about what has or has not "
    "happened. A field that is null or says 'unknown' means the server "
    "could not see it (no database), never that the answer is no. The "
    "server cannot register, collect, publish or change anything."
)

READ_ONLY = ToolAnnotations(readOnlyHint=True, destructiveHint=False,
                            idempotentHint=True, openWorldHint=False)

server = MCPServer("uiw-archive", instructions=INSTRUCTIONS)


def _guard(fn, *args):
    """Run a tool function, turning its anticipated refusals into the SDK's
    ToolError so the model reads the reason. Any other exception is a crash,
    and the SDK deliberately withholds its text from the client."""
    try:
        return fn(*args)
    except tools.ToolError as exc:
        raise ToolError(str(exc)) from exc


@server.tool(annotations=READ_ONLY)
def list_sources(registered: bool | None = None) -> list[dict[str, Any]]:
    """List every candidate source with its registration state.

    Registration and run counts come from the archive database when one is
    configured (PGDATABASE); otherwise `registered` is null (unknown).
    `registered=true|false` filters and needs a database."""
    return _guard(tools.list_sources, registered)


@server.tool(annotations=READ_ONLY)
def get_source(key: str) -> dict[str, Any]:
    """One candidate source in full (class defaults merged), its registration
    state, and its five most recent collector runs when a database is
    configured. `key` is the candidate key from list_sources."""
    return _guard(tools.get_source, key)


@server.tool(annotations=READ_ONLY)
def list_decisions(status: str | None = None,
                   query: str | None = None) -> list[dict[str, str]]:
    """List Decision Records from the register. `status` is a substring of the
    register's status column (e.g. approved, superseded, proposed); `query`
    matches the id, title or category."""
    return _guard(tools.list_decisions, status, query)


@server.tool(annotations=READ_ONLY)
def get_decision(number: str, include_text: bool = False) -> dict[str, Any]:
    """One Decision Record by number (DR-0072, 0072 or 72): register row,
    supersession and origin from its header, and the full text if
    `include_text` is true."""
    return _guard(tools.get_decision, number, include_text)


@server.tool(annotations=READ_ONLY)
def archive_status() -> dict[str, Any]:
    """Aggregate counts from the archive database: sources by lifecycle,
    collector runs, holdings by retention tier and rights-review state, and
    acquisition attempts by outcome. Counts only. Returns database=null when
    none is configured, which means unknown, not empty."""
    return _guard(tools.archive_status)


if __name__ == "__main__":
    server.run("stdio")
