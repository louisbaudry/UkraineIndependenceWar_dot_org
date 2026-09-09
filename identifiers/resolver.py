#!/usr/bin/env python3
"""Resolution — SPEC-0007 §6 (DR-0089, DR-0090).

The resolver is deliberately thin. What an identifier resolves to is decided
in the database by `resolve_identifier()`, so the answer survives this code;
what remains here is the HTTP shape of it and the `?info` record.

The rule that governs every branch: **a minted identifier never returns 404.**
A merged object redirects, a split one disambiguates, a redacted one is gone
but says so, a restricted one exists but is withheld. Only a name the project
never issued is unknown, and saying so plainly is what lets a reader tell a
typo from a removal (DATA-009).
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ark import ArkError, normalise, parse, split_qualifier  # noqa: E402

# What each disposition answers with. The bodies are described, not rendered:
# rendering belongs to the site, and a resolver that could not render still
# has to answer correctly.
STATUS = {
    "active": 200,
    "redirect": 301,
    "disambiguation": 200,
    "tombstone": 410,
    "restricted": 403,
}

# ERC's tokens for a value that is absent, and why (DR-0029's discipline in
# someone else's vocabulary).
ERC_SUPPRESSED = "(:unal)"      # deliberately withheld — restricted
ERC_UNAVAILABLE = "(:unav)"     # was there, is not — tombstone

COMMITMENT = (
    "Identifier validity: this identifier will never be reassigned or "
    "deleted. Object permanence: the object it names may be superseded, "
    "merged, split, restricted or redacted; in every case this identifier "
    "continues to resolve and says which. Content invariance: the "
    "unqualified identifier resolves to the object's current state, which "
    "may change by append-only supersession; a .vN qualified state, once "
    "published, does not change. Change history: every state and every "
    "disposition change is retained and reachable from this identifier. "
    "Service: resolved by the project and, as backup, by the ARK resolver "
    "chain; the register is preserved in every archive dump so that a "
    "successor can resume resolution."
)


@dataclass
class Response:
    status: int
    body: str
    headers: dict[str, str] = field(default_factory=dict)
    media_type: str = "text/plain; charset=utf-8"


class Resolver:
    """Answers an ARK. Configuration is a NAAN and a base URL, nothing more."""

    def __init__(self, register, *, base_url: str):
        self.register = register
        self.base_url = base_url.rstrip("/")

    def url_for(self, ark: str) -> str:
        return f"{self.base_url}/{ark}"

    # -- the contract ------------------------------------------------------

    def get(self, request_path: str, *, inflection: str | None = None) -> Response:
        """Resolve one request. `inflection` is '?info', '?' or '??'."""
        try:
            normalised = normalise(request_path)
            base_for_check, _ = split_qualifier(normalised)
            # Verified here, not merely parsed: a name whose check character
            # fails cannot be an identifier this project ever issued, and
            # saying so is the difference between "you mistyped it" and "it
            # was withdrawn" (SPEC-0007 §2.3). Reading a stored value back
            # skips the check; an inbound request never does.
            parse(base_for_check, verify=True)
        except ArkError as exc:
            return Response(400, f"Not a usable ARK: {exc}")

        base, version = split_qualifier(normalised)
        record = self.register.resolve(base)

        if record is None:
            # The only 404 there is. Worth saying why, so a reader can tell a
            # mistyped identifier from a withdrawn one.
            return Response(
                404,
                f"{base} was never issued by this project. A published "
                "identifier always resolves; if you have this from a "
                "citation, check the transcription — the last character is "
                "a check character.",
            )

        if inflection in ("?info", "?", "??"):
            return Response(200, self.info(record), media_type="text/plain; charset=utf-8")

        disposition = record["disposition"]
        status = STATUS[disposition]

        if disposition == "redirect":
            target = self.url_for(record["terminal_ark"])
            return Response(
                status,
                f"Merged into {record['terminal_ark']} on "
                f"{record['disposition_at'].date().isoformat()}. The merge "
                "was a recorded decision and the lineage is permanent.",
                headers={"Location": target},
            )

        if disposition == "disambiguation":
            successors = self.register.conn.execute(
                "SELECT successor_ark FROM disambiguation_successor "
                "WHERE record_id = %s ORDER BY successor_ark",
                (record["disambiguation_id"],)).fetchall()
            row = self.register.conn.execute(
                "SELECT split_at, grounds FROM disambiguation_record "
                "WHERE id = %s", (record["disambiguation_id"],)).fetchone()
            listed = ", ".join(s[0] for s in successors)
            # The record holds the deciding agent (DR-0089 §5) but the body
            # does not name them: the stored value is an internal agent id,
            # which §4.3 keeps off public surfaces, and whether an editorial
            # byline is published is a policy question this resolver must
            # not answer on its own (SPEC-0007 §12).
            return Response(
                status,
                f"Split on {row[0].date().isoformat()}: {row[1]}\n"
                f"Successors: {listed}\n"
                "The deciding agent is recorded in the disambiguation record.",
            )

        if disposition == "tombstone":
            return Response(
                status,
                "Removed under governed redaction on "
                f"{record['disposition_at'].date().isoformat()}, under a "
                "recorded ground and authority. The fact of removal is part "
                "of the record; the content is not returned.",
            )

        if disposition == "restricted":
            return Response(
                status,
                f"{base} exists. Its access tier withholds it from this "
                "request (absence state: withheld). Nothing has been removed.",
            )

        return self.active(record, version)

    def active(self, record: dict, version: int | None) -> Response:
        """An identifier resolving to its object, or to one declared state."""
        subject = self.register.subject_of(record["ark"])
        if subject is None:
            # A register row with no subject is a bug, not a disposition.
            return Response(500, "register inconsistency: no subject recorded")
        table, row_id = subject

        # `table` and `row_id` locate the object internally. Neither is ever
        # written into a response body: an internal UUID on a public surface
        # is the one thing §4.3 forbids outright.
        if version is not None:
            versioned = self.register.conn.execute(
                "SELECT versioned FROM citable_class WHERE subject_table = %s",
                (table,)).fetchone()
            if not versioned or not versioned[0]:
                return Response(
                    400,
                    f"{record['ark']} names a {table}, which has no declared "
                    "states; a .vN qualifier is meaningless for it "
                    "(SPEC-0007 §7).",
                )
            known = self._states(table, row_id)
            if version not in known:
                return Response(
                    404,
                    f"{record['ark']} is valid; state v{version} is not. "
                    f"Known states: {', '.join('v%d' % v for v in known) or 'none'}.",
                )
            return Response(
                200,
                f"{record['ark']}.v{version} — {self._describe(record)}, "
                "as published in that state.",
                headers={"Link": f'<{self.url_for(record["ark"])}>; rel="original"'},
            )

        return Response(
            200, f"{record['ark']} — {self._describe(record)}, current state.",
            headers={"Link": f'<{self.url_for(record["ark"])}?info>; rel="describedby"'},
        )

    def _states(self, table: str, row_id: str) -> list[int]:
        """Which `.vN` states an object actually has (SPEC-0007 §7)."""
        if table == "published_page":
            return [r[0] for r in self.register.conn.execute(
                "SELECT revision FROM page_revision WHERE page_id = %s "
                "ORDER BY revision", (row_id,))]
        if table == "holding":
            row = self.register.conn.execute(
                "SELECT ocfl_object_id FROM holding WHERE id = %s",
                (row_id,)).fetchone()
            if not row or not row[0]:
                return []
            return [int(r[0].lstrip("v")) for r in self.register.conn.execute(
                "SELECT ocfl_version FROM preserved_object "
                "WHERE ocfl_object_id = %s AND ocfl_version ~ '^v[0-9]+$' "
                "ORDER BY ocfl_version", (row[0],))]
        return []

    # -- ?info -------------------------------------------------------------

    def info(self, record: dict) -> str:
        """The ERC record served by `?info` (SPEC-0007 §6.2).

        ANVL syntax: `name: value`, folded continuations indented, the record
        ending at a blank line. The four kernel elements first, then the
        disposition, then the commitment statement.
        """
        disposition = record["disposition"]
        what = {
            "restricted": ERC_SUPPRESSED,
            "tombstone": ERC_UNAVAILABLE,
        }.get(disposition, self._describe(record))

        lines = [
            "erc:",
            "who:    Ukraine's Second War of Independence (project)",
            f"what:   {what}",
            f"when:   {record['minted_at'].date().isoformat()}",
            f"where:  {self.url_for(record['ark'])}",
            f"disposition: {disposition}",
            f"disposition-at: {record['disposition_at'].date().isoformat()}",
        ]
        if disposition == "redirect":
            lines.append(f"successor: {record['terminal_ark']}")
        lines.append("support-erc:")
        lines.extend(_fold(COMMITMENT))
        return "\n".join(lines) + "\n\n"

    def _describe(self, record: dict) -> str:
        subject = self.register.subject_of(record["ark"])
        if subject is None:
            return "(:unkn)"
        table, _ = subject
        row = self.register.conn.execute(
            "SELECT record_class FROM citable_class WHERE subject_table = %s",
            (table,)).fetchone()
        return row[0] if row else table


def _fold(text: str, width: int = 68) -> list[str]:
    """ANVL continuation lines: indented, joined back into one value."""
    words, lines, current = text.split(), [], ""
    for word in words:
        if len(current) + len(word) + 1 > width:
            lines.append("    " + current)
            current = word
        else:
            current = f"{current} {word}".strip()
    if current:
        lines.append("    " + current)
    return lines
