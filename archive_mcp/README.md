# archive_mcp — a read-only MCP server for the archive

Lets Claude ask the project what is true *now*: which Decision Records are in
force, which candidate sources exist, and — when a database is configured —
which are registered and what has been collected. It exists so a session
checks state instead of repeating a status claim from a file
(`CLAUDE.md`, "Where state lives"). Issue
[#167](https://github.com/louisbaudry/UkraineIndependenceWar_dot_org/issues/167).

**It is read-only by construction.** It registers nothing, collects nothing
and writes nothing: registration is the act that authorises collection
(OPS-001), a person is the agent of record for a run (DR-0093 §3), and Gates 2
and 3 are human decisions (DR-0066). The database session is opened with
`default_transaction_read_only=on`, so the guarantee is the server's, not a
convention in the queries. A write tool would need its own decision first.

## Tools

| Tool | Answers | Needs a database |
|---|---|---|
| `list_sources` | Every candidate source, with registered / lifecycle / run counts | for the registration fields |
| `get_source` | One candidate in full (class defaults merged, as `register.py` sees it), plus registration and its five latest runs | for registration and runs |
| `list_decisions` | The Decision Record register, filtered by status substring or text | no |
| `get_decision` | One DR: register row, supersession and origin from its header, optionally the full text | no |
| `archive_status` | Counts of sources by lifecycle, runs, holdings by tier and rights-review state, attempts by outcome | yes |

**Unknown is not no.** Without a database, every registration field is `null`
and `archive_status` returns `database: null` with a note. A session with no
database must not be able to say "nothing has been collected".

**Counts only.** No holding, locator or row from any source comes back from the
database, so nothing here carries a person's data out of the archive
(DR-0071(b), POL-0001).

## Install and register with Claude

```bash
pip install -r archive_mcp/requirements.txt     # the official `mcp` SDK
```

The repository's `.mcp.json` registers it for Claude Code as `uiw-archive`
(stdio, `python3 archive_mcp/server.py`). Claude Code asks you to approve a
project server the first time. For another client, point it at the same
command with the repository as the working directory.

To read a real database, export libpq's usual variables *before* launching
Claude; the server inherits them and `PGDATABASE` is what switches the
database tools on:

```bash
export PGDATABASE=uiw PGHOST=… PGUSER=…        # a read-only role is best
```

Credentials come from the environment only. Never put a host, user or
password in `.mcp.json` or anywhere else in this public repository
(`CLAUDE.md`, "This repository is public"). The live archive database is on
the archive server; whether and how a session can reach it is not decided
here.

## Tests

```bash
PGHOST=… PGPORT=… PGUSER=… python3 archive_mcp/tests/test_tools.py
```

31 checks against a real PostgreSQL (rebuilt from the DDL) and a real stdio
round trip through the SDK's own client. The protocol checks are skipped, and
say so, when `mcp` is not installed.

**Shown to fail.** Each rule was broken one at a time and the suite went red:

| Sabotage | Result |
|---|---|
| read-only session option removed from `connect()` | 3 failures (writes succeed, row counts change) |
| no database reported as zero counts | 1 failure |
| no database reported as "not registered" | 2 failures |
| `list_decisions` ignoring `status` | 1 failure |
| refusals not converted to the SDK's `ToolError` | 1 failure (the model would see only "Error executing tool") |
| class defaults not merged in `get_source` | red (an error, not a clean failure) |
| a tool annotated `readOnlyHint=False` | 1 failure |

## What this is not

- Not a write path, and not a way around "a person registers and collects".
- Not a deployment: nothing runs on the archive server and nothing listens on
  a network port, so `docs/infrastructure.md` is unchanged. A remote endpoint
  would need a Decision Record and a hardening pass first.
- Not a search engine over the documents (a candidate next tool).

## Dependency

`mcp>=2,<3` is the repository's only dependency beyond the standard library,
`psycopg` and `PyYAML`, approved by the founder on 2026-10-25 for this
component only. The server was developed against `mcp` 2.3.0; the 2.x
`MCPServer` API (`mcp.server.mcpserver`) differs from the 1.x `FastMCP`, hence
the upper bound.
