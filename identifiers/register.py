#!/usr/bin/env python3
"""Minting and the identifier register — SPEC-0007 §4–5 (DR-0088, DR-0089).

Minting is not "generate a string". It is an assertion: *the project assigned
this name to this object, on this date, on this basis* (DR-0012). So every
mint writes an `identifier_assignment` row alongside the register row, in one
transaction, and the register can be rebuilt from the assertion family alone.

The disposition changes here are the public face of decisions taken
elsewhere — a merge (DR-0064), a split (DR-0064), a redaction (DR-0077), a
tier change (DR-0086). None of them invents a decision; each records where
one already exists, which is why every method demands a basis it cannot
default.
"""

from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ark import (  # noqa: E402
    ArkError,
    format_ark,
    mint_name,
    normalise,
    parse,
    split_qualifier,
)

# The project's own identifier type in the registry (DR-0087).
ARK_TYPE = "uiw-ark"

# The shared test NAAN from the ARK draft. Never a published identifier:
# SPEC-0007 §11 forbids minting under it outside the suite.
TEST_NAAN, TEST_SHOULDER = "99999", "t1"

MAX_MINT_ATTEMPTS = 8

REGISTRY_YAML = Path(__file__).resolve().parent.parent / "registry" / "registry.yaml"


class MintError(Exception):
    """A mint or disposition change that must not proceed."""


# The project asserts its own identifiers in its own name (SPEC-0007 §4.2).
# Not a person: an editor who leaves does not take the project's identifiers
# with them, and DR-0059 keeps the project itself in the pipeline registry.
PROJECT_AGENT_NAME = "Ukraine's Second War of Independence"


def project_agent(conn) -> str:
    """The project's own pipeline agent (SPEC-0007 §11, prerequisite 5)."""
    row = conn.execute(
        "SELECT id FROM pipeline_agent WHERE kind = 'organization' AND name = %s",
        (PROJECT_AGENT_NAME,)).fetchone()
    if row is None:
        raise MintError(
            "the project has no pipeline agent of its own, so an identifier "
            "assignment would have no asserter (DR-0012, SPEC-0007 §4.2). "
            f"Insert a pipeline_agent of kind 'organization' named "
            f"{PROJECT_AGENT_NAME!r} before minting."
        )
    return str(row[0])


def _uuid() -> str:
    return str(uuid.uuid4())


def from_registry(conn, *, allow_test_naan: bool = False, registry_path=None):
    """Build a Register from the NAAN recorded in `registry/registry.yaml`.

    Returns None when no NAAN has been issued, which is the project's actual
    state until one is requested (SPEC-0007 §11). That is not an error and
    must not be treated as one: it means nothing may be minted yet, and a
    caller that mints anyway would be publishing an identifier under a
    number the project does not hold.

    `allow_test_naan` is for the suite, which mints under the ARK Alliance's
    shared test NAAN. A published identifier never may.
    """
    import yaml

    config = (yaml.safe_load(Path(registry_path or REGISTRY_YAML).read_text())
              .get("identifiers") or {})
    naan, shoulder = config.get("naan"), config.get("shoulder")
    if naan and shoulder:
        return Register(conn, naan=naan, shoulder=shoulder)
    if allow_test_naan:
        return Register(conn,
                        naan=config.get("test_naan", TEST_NAAN),
                        shoulder=config.get("test_shoulder", TEST_SHOULDER))
    return None


class Register:
    """The identifier register over one database connection."""

    def __init__(self, conn, *, naan: str, shoulder: str,
                 project_agent_id: str | None = None):
        if not naan or not shoulder:
            raise MintError(
                "a NAAN and shoulder are required before anything is minted "
                "(SPEC-0007 §11). Until one is issued, the suite uses the "
                "shared test NAAN; published identifiers may not."
            )
        self.conn, self.naan, self.shoulder = conn, naan, shoulder
        self._project_agent_id = project_agent_id

    @property
    def project_agent_id(self) -> str:
        if self._project_agent_id is None:
            self._project_agent_id = project_agent(self.conn)
        return self._project_agent_id

    # -- minting -----------------------------------------------------------

    def mint(
        self,
        *,
        subject_table: str,
        subject_id: str,
        asserter_id: str | None = None,
        basis: dict | None = None,
    ) -> str:
        """Assign a public identifier to one object, once.

        Idempotent by rule, not by accident: an object that already has an
        ARK gets that same ARK back. Minting twice would give a reader two
        ways to cite one thing, and DATA-009 would then owe both forever.
        """
        existing = self.ark_for(subject_table, subject_id)
        if existing:
            return existing

        asserter_id = asserter_id or self.project_agent_id

        if not self.conn.execute(
            "SELECT 1 FROM citable_class WHERE subject_table = %s",
            (subject_table,),
        ).fetchone():
            raise MintError(
                f"{subject_table!r} is not a citable class (SPEC-0007 §3). "
                "Internal objects do not automatically require public "
                "identifiers (record §15); adding a class is a deliberate "
                "change to `citable_class`, not a side effect of minting."
            )

        for _ in range(MAX_MINT_ATTEMPTS):
            candidate = format_ark(self.naan, mint_name(self.naan, self.shoulder))
            if self.conn.execute(
                "SELECT 1 FROM public_identifier WHERE ark = %s", (candidate,)
            ).fetchone():
                continue                      # astronomically unlikely; still checked
            return self._write(
                candidate, subject_table, subject_id, asserter_id, basis
            )
        raise MintError("could not find an unused name; the generator is suspect")

    def _write(self, ark, subject_table, subject_id, asserter_id, basis) -> str:
        assignment_id = _uuid()
        with self.conn.transaction():
            self.conn.execute(
                """
                INSERT INTO identifier_assignment
                    (id, valid_time, asserter_id, epistemic_category,
                     basis, subject_table, subject_id, identifier_type, value)
                VALUES (%s, ROW(now(), now(), NULL, NULL, NULL)::timespan, %s,
                        'observation', %s, %s, %s, %s, %s)
                """,
                (assignment_id, asserter_id, json.dumps(basis or {}),
                 subject_table, subject_id, ARK_TYPE, ark),
            )
            self.conn.execute(
                "INSERT INTO public_identifier (ark, assignment_id) VALUES (%s,%s)",
                (ark, assignment_id),
            )
            self.conn.execute(
                "INSERT INTO public_identifier_subject (ark, subject_table, subject_id) "
                "VALUES (%s,%s,%s)",
                (ark, subject_table, subject_id),
            )
        return ark

    def ark_for(self, subject_table: str, subject_id: str) -> str | None:
        row = self.conn.execute(
            "SELECT ark FROM public_identifier_subject "
            "WHERE subject_table = %s AND subject_id = %s",
            (subject_table, subject_id),
        ).fetchone()
        return row[0] if row else None

    def subject_of(self, ark: str) -> tuple[str, str] | None:
        row = self.conn.execute(
            "SELECT subject_table, subject_id FROM public_identifier_subject "
            "WHERE ark = %s", (normalise(ark),)).fetchone()
        return (row[0], str(row[1])) if row else None

    # -- dispositions ------------------------------------------------------

    def _move(self, ark, disposition, basis, **columns) -> None:
        if basis is None:
            raise MintError(
                f"a move to {disposition!r} records the decision behind it "
                "(DR-0089 invariant 3): a merge event, a split, a redaction "
                "decision, or a tier decision."
            )
        assignments = "".join(f", {name} = %s" for name in columns)
        self.conn.execute(
            f"UPDATE public_identifier SET disposition = %s, "
            f"disposition_at = now(), disposition_basis = %s{assignments} "
            "WHERE ark = %s",
            (disposition, basis, *columns.values(), normalise(ark)),
        )

    def redirect(self, *, ark: str, successor_ark: str, basis: str) -> None:
        """Merged: this identifier now resolves to its successor (DR-0064)."""
        self._move(ark, "redirect", basis, successor_ark=normalise(successor_ark))

    def split(
        self, *, ark: str, successors: list[str], decided_by: str,
        grounds: str, split_at=None,
    ) -> str:
        """Split: this identifier resolves to a disambiguation record.

        A split has no single successor, so it never redirects. The public
        record carries the date, the successors, the grounds, and a public
        byline if the deciding agent has one (DR-0089 §5, DR-0092) — nothing
        more. The agent's own id is written only to `disambiguation_decision`
        (internal tier), never to `disambiguation_record` itself: putting a
        raw agent id in the same table a disclosure dump carries whole would
        let a preservation dump (which does carry `pipeline_agent`) be
        joined against it to identify an agent who chose to stay unnamed.
        The byline is computed from the agent's own row by this statement,
        not passed in — this method takes no `public_title` argument, so
        one cannot be supplied here by mistake.
        """
        if len(successors) < 2:
            raise MintError("a split has at least two successors")
        record_id = _uuid()
        with self.conn.transaction():
            self.conn.execute(
                "INSERT INTO disambiguation_record (id, split_at, "
                "decided_by_title, grounds) VALUES "
                "(%s, %s, (SELECT public_title FROM pipeline_agent "
                "WHERE id = %s), %s)",
                (record_id, split_at or "now()", decided_by, grounds),
            )
            self.conn.execute(
                "INSERT INTO disambiguation_decision (record_id, decided_by) "
                "VALUES (%s,%s)", (record_id, decided_by),
            )
            for successor in successors:
                self.conn.execute(
                    "INSERT INTO disambiguation_successor (record_id, successor_ark) "
                    "VALUES (%s,%s)", (record_id, normalise(successor)))
            self._move(ark, "disambiguation", record_id, disambiguation_id=record_id)
        return record_id

    def tombstone(self, *, ark: str, basis: str) -> None:
        """Redacted under a recorded ground: the identifier says so (DR-0077)."""
        self._move(ark, "tombstone", basis)

    def restrict(self, *, ark: str, basis: str) -> None:
        """Above the reader's tier: exists, withheld, not removed (DR-0086)."""
        self._move(ark, "restricted", basis)

    def reinstate(self, *, ark: str, basis: str) -> None:
        """Back to active — a lowered tier, or a redaction reversed under §77."""
        self._move(ark, "active", basis)

    # -- reading -----------------------------------------------------------

    def resolve(self, ark: str) -> dict | None:
        """The register's answer for one identifier, or None if never minted."""
        try:
            base = normalise(ark)
            parse(base, verify=False)
        except ArkError:
            return None
        base, version = split_qualifier(base)
        row = self.conn.execute(
            "SELECT ark, disposition::text, terminal_ark, hops, "
            "       disambiguation_id, disposition_basis, minted_at, disposition_at "
            "  FROM resolve_identifier(%s) "
            " WHERE ark IS NOT NULL",
            (base,),
        ).fetchone()
        if row is None:
            return None
        return {
            "ark": row[0], "disposition": row[1], "terminal_ark": row[2],
            "hops": row[3], "disambiguation_id": row[4],
            "disposition_basis": row[5], "minted_at": row[6],
            "disposition_at": row[7], "version": version,
        }

    def health(self) -> list[dict]:
        """Every minted identifier and what it resolves to (DATA-009)."""
        return [
            {"ark": r[0], "disposition": r[1], "terminal_ark": r[2],
             "subject_table": r[3], "subject_id": r[4]}
            for r in self.conn.execute(
                "SELECT ark, disposition::text, terminal_ark, subject_table, "
                "subject_id FROM identifier_register_health ORDER BY ark")
        ]
