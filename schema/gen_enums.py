#!/usr/bin/env python3
"""Generate PostgreSQL enum types from the compiled registry.

This is where DR-0078's enforcement surface becomes enforcement: the
`enumerations` map in registry/dist/registry.json is turned into database
types, so a value absent from the registry cannot enter the canonical store.

Only `closed` vocabularies become enum types. Open vocabularies (DR-0080)
may grow by registry process, and a database enum would make every addition
a migration; they become lookup tables seeded from the registry instead, so
adding a member is a data change rather than a schema change.

Deterministic output; `--check` verifies the committed file is current.

Usage:
  python3 schema/gen_enums.py            # write schema/01-enums-generated.sql
  python3 schema/gen_enums.py --check    # verify it is current
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPILED = ROOT / "registry" / "dist" / "registry.json"
OUTPUT = ROOT / "schema" / "01-enums-generated.sql"


def sql_name(vocab_id, axis=None):
    """Registry ids are kebab-case; PostgreSQL identifiers are snake_case."""
    base = vocab_id.replace("-", "_")
    return f"{base}_{axis.replace('-', '_')}" if axis else base


def quote(value):
    return "'" + str(value).replace("'", "''") + "'"


def enum_blocks(compiled):
    """One block per closed vocabulary, or per axis of a multi-axis one."""
    blocks = []
    for vocab_id in sorted(compiled["enumerations"]):
        vocab = compiled["enumerations"][vocab_id]
        if not vocab.get("closed"):
            continue
        entry = compiled["entries"].get(vocab_id, {})
        values = vocab["values"]
        authorised = ", ".join(entry.get("authorised_by") or []) or "—"

        if isinstance(values, dict):
            for axis in sorted(values):
                blocks.append(
                    render_enum(
                        sql_name(vocab_id, axis),
                        values[axis],
                        f"{vocab_id} / {axis}",
                        authorised,
                    )
                )
        else:
            blocks.append(render_enum(sql_name(vocab_id), values, vocab_id, authorised))
    return blocks


def render_enum(type_name, values, source_id, authorised):
    listed = ",\n    ".join(quote(v) for v in values)
    return (
        f"-- {source_id} (authorised by {authorised})\n"
        f"CREATE TYPE {type_name} AS ENUM (\n    {listed}\n);"
    )


def lookup_blocks(compiled):
    """Open vocabularies become seeded lookup tables, not enum types."""
    blocks = []
    for vocab_id in sorted(compiled["enumerations"]):
        vocab = compiled["enumerations"][vocab_id]
        if vocab.get("closed"):
            continue
        entry = compiled["entries"].get(vocab_id, {})
        authorised = ", ".join(entry.get("authorised_by") or []) or "—"
        table = sql_name(vocab_id)
        values = vocab["values"]
        rows = ",\n    ".join(f"({quote(v)})" for v in values)
        blocks.append(
            f"-- {vocab_id} (open vocabulary, authorised by {authorised})\n"
            f"-- Open per DR-0080: members may be added by registry process, so this\n"
            f"-- is a seeded lookup table rather than an enum type — adding a member\n"
            f"-- is a data change, not a migration.\n"
            f"CREATE TABLE {table} (\n"
            f"    id text PRIMARY KEY\n"
            f");\n"
            f"INSERT INTO {table} (id) VALUES\n    {rows};"
        )
    return blocks


def build(compiled):
    meta = compiled["registry"]
    header = f"""-- Registry-derived types for the canonical store.
--
-- GENERATED FILE — do not edit. Regenerate with schema/gen_enums.py.
-- Source of truth: registry/*.yaml (DR-0078), compiled per SPEC-0005.
--
-- This file is where DR-0078's enforcement surface becomes enforcement: a
-- value absent from the registry cannot enter the canonical store.
--
-- Registry: {meta['id']} version {meta['version']} ({meta['status']})
--
-- Closed vocabularies (DR-0080) become enum types: changing them requires a
-- Decision Record, and a migration is the appropriate cost of that.
-- Open vocabularies become seeded lookup tables so that additions by
-- registry process do not require schema migrations.
"""
    parts = [header, "", "-- Closed vocabularies -> enum types", ""]
    parts.extend(b + "\n" for b in enum_blocks(compiled))
    parts.extend(["", "-- Open vocabularies -> seeded lookup tables", ""])
    parts.extend(b + "\n" for b in lookup_blocks(compiled))
    return "\n".join(parts).rstrip() + "\n"


def main():
    if not COMPILED.exists():
        print(f"missing {COMPILED} — run registry/compile.py first")
        return 1
    compiled = json.loads(COMPILED.read_text())
    content = build(compiled)

    if "--check" in sys.argv:
        if not OUTPUT.exists() or OUTPUT.read_text() != content:
            print(f"STALE: {OUTPUT.name} — run schema/gen_enums.py")
            return 1
        print(f"{OUTPUT.name} is current.")
        return 0

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(content)
    closed = sum(1 for v in compiled["enumerations"].values() if v.get("closed"))
    open_ = len(compiled["enumerations"]) - closed
    print(
        f"wrote {OUTPUT.relative_to(ROOT)}: "
        f"{closed} closed vocabularies as enum types, "
        f"{open_} open as lookup tables"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
