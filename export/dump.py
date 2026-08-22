#!/usr/bin/env python3
"""Durable export of the canonical store.

Implements DR-0058: the archive outlives the database product. OCFL already
makes the preserved *bytes* self-describing (DR-0073); this makes the
*assertions* about them self-describing too. Together they are the complete
archive, and PRES-009 — the archive is reconstructible without the project's
software — depends on both.

Format is specified in SPEC-0006. In outline:

    manifest.json          What this dump is, what it contains, and its fixity
    manifest.json.sha256   Sidecar for the manifest itself
    schema.json            Every table and column, linked to its registry entry
    README.txt             Orientation for a human with no other context
    data/<table>.jsonl     Authoritative data, one JSON object per row
    data/<table>.csv       Same data, flattened; lossy for composite columns

**Completeness is structural.** The table list comes from the database's own
catalogue, not from a list maintained here. A table added to the schema and
forgotten in the dumper would break PRES-009 silently; deriving the list
means a new table is exported whether or not anyone remembered it.

Usage:
  python3 export/dump.py <output-dir> [--registry registry/dist/registry.json]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import psycopg

FORMAT_VERSION = "1.0"
SPECIFICATION = "SPEC-0006"

# Views and the contract table are derived or documentary, not data.
EXCLUDED_TABLES: set[str] = set()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def list_tables(conn: psycopg.Connection) -> list[str]:
    """Every base table in the public schema, from the catalogue itself."""
    rows = conn.execute(
        """
        SELECT table_name
          FROM information_schema.tables
         WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
         ORDER BY table_name
        """
    ).fetchall()
    return [r[0] for r in rows if r[0] not in EXCLUDED_TABLES]


def describe_schema(conn: psycopg.Connection, registry: dict | None) -> dict:
    """Every table and column, linked to the registry where one applies.

    This is what makes the dump interpretable rather than merely readable:
    a column typed `likelihood_bands` resolves to the registry entry that
    defines what those bands mean, including their numeric ranges (DR-0065).
    """
    enum_values = {
        row[0]: row[1]
        for row in conn.execute(
            """
            SELECT t.typname, array_agg(e.enumlabel::text ORDER BY e.enumsortorder)
              FROM pg_type t JOIN pg_enum e ON e.enumtypid = t.oid
             GROUP BY t.typname
            """
        )
    }
    composites = {
        row[0]: row[1]
        for row in conn.execute(
            """
            SELECT t.typname,
                   jsonb_agg(jsonb_build_object('name', a.attname,
                                                'type', format_type(a.atttypid, a.atttypmod))
                             ORDER BY a.attnum)
              FROM pg_type t
              JOIN pg_class c ON c.oid = t.typrelid
              JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum > 0
             WHERE c.relkind = 'c'
             GROUP BY t.typname
            """
        )
    }

    # Registry entries are keyed by kebab-case id; database types are snake.
    registry_by_sql_name = {}
    if registry:
        for entry_id, entry in registry.get("entries", {}).items():
            registry_by_sql_name[entry_id.replace("-", "_")] = entry_id

    tables = {}
    for table in list_tables(conn):
        columns = []
        for name, data_type, udt, nullable, default in conn.execute(
            """
            SELECT column_name, data_type, udt_name, is_nullable, column_default
              FROM information_schema.columns
             WHERE table_schema = 'public' AND table_name = %s
             ORDER BY ordinal_position
            """,
            (table,),
        ):
            column: dict = {
                "name": name,
                "type": data_type if data_type != "USER-DEFINED" else udt,
                "nullable": nullable == "YES",
            }
            if default:
                column["default"] = default
            if udt in enum_values:
                column["enum_values"] = enum_values[udt]
                if udt in registry_by_sql_name:
                    column["registry_entry"] = registry_by_sql_name[udt]
            if udt in composites:
                column["composite_fields"] = composites[udt]
            columns.append(column)

        comment = conn.execute(
            "SELECT obj_description(%s::regclass, 'pg_class')", (table,)
        ).fetchone()[0]

        tables[table] = {"columns": columns}
        if comment:
            tables[table]["comment"] = comment

    return {
        "format_version": FORMAT_VERSION,
        "specification": SPECIFICATION,
        "registry_version": (registry or {}).get("registry", {}).get("version"),
        "tables": tables,
    }


def dump_table(conn: psycopg.Connection, table: str, data_dir: Path) -> dict:
    """Write one table as JSONL (authoritative) and CSV (convenience)."""
    jsonl_path = data_dir / f"{table}.jsonl"
    rows = 0
    with jsonl_path.open("w", encoding="utf-8") as out:
        # row_to_json expands composite columns and renders bytea as a hex
        # string, so structure survives without a custom encoder.
        for (record,) in conn.execute(f'SELECT row_to_json(t)::text FROM "{table}" t'):
            out.write(record + "\n")
            rows += 1

    csv_path = data_dir / f"{table}.csv"
    with csv_path.open("w", encoding="utf-8") as out:
        with conn.cursor().copy(
            f'COPY (SELECT * FROM "{table}") TO STDOUT WITH (FORMAT csv, HEADER true)'
        ) as copy:
            for chunk in copy:
                out.write(bytes(chunk).decode("utf-8"))

    return {
        "rows": rows,
        "files": {
            "jsonl": {"path": f"data/{table}.jsonl",
                      "sha256": _sha256_file(jsonl_path),
                      "bytes": jsonl_path.stat().st_size},
            "csv": {"path": f"data/{table}.csv",
                    "sha256": _sha256_file(csv_path),
                    "bytes": csv_path.stat().st_size},
        },
    }


README = """\
Durable export of the canonical store — Ukraine's Second War of Independence.

WHAT THIS IS
    A complete, software-independent copy of the project's canonical
    assertions. It exists because the archive must outlive the database
    product that held it, and must be reconstructible without the project's
    own software (requirement PRES-009, Decision Record DR-0058).

    This dump is one half of the archive. The other half is the OCFL storage
    root, which holds the preserved bytes and describes itself separately.
    You need both.

HOW TO READ IT
    schema.json   Describes every table and column. Columns whose values come
                  from a controlled vocabulary name the registry entry that
                  defines them, and list the permitted values inline.

    data/*.jsonl  The data. One JSON object per line, one file per table.
                  This is the authoritative form: composite values (time
                  spans, quantities) keep their structure, and binary values
                  are hex strings prefixed with \\x.

    data/*.csv    The same data flattened. Convenient for a spreadsheet, but
                  LOSSY: composite and JSON columns render as PostgreSQL text
                  rather than structure. Prefer the JSONL if the two differ.

    manifest.json Row counts and SHA-256 for every file above. Verify these
                  before trusting the contents.

READING IT HONESTLY
    Values that look absent usually are not. A field carrying an absence
    state — 'unknown', 'not-researched', 'no-evidence-found', 'withheld',
    'redacted' and others — is recording *why* something is absent. A missing
    value never silently means "no".

    Likewise, a quantity keeps the words it was stated in. A value marked
    'at-least' means at least; it does not mean exactly.

    Rows carrying redaction fields are tombstones: content was removed under
    a recorded ground and authority. The removal is deliberate and its fact
    is part of the record.

    Assertions are append-only. A row superseded by another is not wrong; it
    is what the project held at that time, retained so the record of its own
    changes of mind survives.
"""


def create_dump(
    conn: psycopg.Connection, output: Path, registry_path: Path | None
) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise SystemExit(f"output directory {output} is not empty")
    data_dir = output / "data"
    data_dir.mkdir()

    registry = None
    if registry_path and registry_path.exists():
        registry = json.loads(registry_path.read_text())

    schema = describe_schema(conn, registry)
    (output / "schema.json").write_text(
        json.dumps(schema, indent=2, sort_keys=True) + "\n"
    )
    (output / "README.txt").write_text(README)

    tables = {t: dump_table(conn, t, data_dir) for t in list_tables(conn)}

    manifest = {
        "format_version": FORMAT_VERSION,
        "specification": SPECIFICATION,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "registry_version": schema["registry_version"],
        "total_rows": sum(t["rows"] for t in tables.values()),
        "tables": tables,
        "files": {
            "schema.json": {"sha256": _sha256_file(output / "schema.json")},
            "README.txt": {"sha256": _sha256_file(output / "README.txt")},
        },
    }
    manifest_path = output / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    # The manifest attests to everything else; a sidecar attests to it.
    (output / "manifest.json.sha256").write_text(
        f"{_sha256_file(manifest_path)}  manifest.json\n"
    )
    return manifest


def verify_dump(output: Path) -> list[str]:
    """Check a dump against its own manifest. Empty list means intact."""
    problems: list[str] = []
    manifest_path = output / "manifest.json"
    if not manifest_path.is_file():
        return ["missing manifest.json"]

    sidecar = output / "manifest.json.sha256"
    if not sidecar.is_file():
        problems.append("missing manifest sidecar")
    elif sidecar.read_text().split()[0] != _sha256_file(manifest_path):
        problems.append("manifest does not match its sidecar")

    manifest = json.loads(manifest_path.read_text())

    for name, meta in manifest.get("files", {}).items():
        path = output / name
        if not path.is_file():
            problems.append(f"missing {name}")
        elif _sha256_file(path) != meta["sha256"]:
            problems.append(f"{name} does not match its recorded digest")

    for table, meta in manifest.get("tables", {}).items():
        for kind, file_meta in meta["files"].items():
            path = output / file_meta["path"]
            if not path.is_file():
                problems.append(f"missing {file_meta['path']}")
                continue
            if _sha256_file(path) != file_meta["sha256"]:
                problems.append(f"{file_meta['path']} does not match its digest")
            if kind == "jsonl":
                actual = sum(1 for line in path.open() if line.strip())
                if actual != meta["rows"]:
                    problems.append(
                        f"{file_meta['path']} has {actual} rows, manifest says {meta['rows']}"
                    )
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--dbname", default=None)
    parser.add_argument(
        "--registry", type=Path, default=Path("registry/dist/registry.json")
    )
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()

    if args.verify_only:
        problems = verify_dump(args.output)
        for problem in problems:
            print(f"  {problem}")
        print("dump verifies clean" if not problems else f"{len(problems)} problem(s)")
        return 1 if problems else 0

    with psycopg.connect(dbname=args.dbname) if args.dbname else psycopg.connect() as conn:
        manifest = create_dump(conn, args.output, args.registry)

    print(f"wrote {args.output}")
    print(f"  {len(manifest['tables'])} tables, {manifest['total_rows']} rows")
    print(f"  registry version {manifest['registry_version']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
