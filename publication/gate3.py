#!/usr/bin/env python3
"""Gate 3 — the publication decision (SPEC-0003 §2; DR-0066).

The last gate. Does accepted knowledge, or a preserved item, appear on a
public surface, and at which access tier (§12)?

Gate 3 is a **separate decision from Gate 2**, and the separation is the
point: accepting something as true and deciding to say it in public are
different acts with different consequences. Collapsing them is how archives
end up publishing what they merely believe.

Two things this module is not:

  * **Not a website.** It records publication decisions and the revisions
    that resulted. Rendering, routing and serving are a later product
    concern; the record of what was said has to exist first, because §90's
    history can only start from the beginning.

  * **Not the archive.** The site is a projection (Principle 18). Every
    revision pins the baseline, methodology, terminology and template it was
    built from, so §86's question — *what exactly did we say about X, in
    language Y, on date Z, and on what evidence and methodology?* — is
    answerable. But the answer is reconstructed from the archive, never
    substituted for it.

The rules live in `schema/07-publication.sql`, so they bind whatever writes.
This module makes the right thing convenient and refuses a few things early,
where a clear message beats a constraint violation.
"""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass

# §12's tier set. Containment is declared, not derived from an ordering: the
# restricted tiers are lateral grants to named parties, not rungs. This
# mirrors `tier_admits()` in the schema and `DISCLOSURE_TIERS` in
# export/tiers.py; the test suite checks all three agree rather than trusting
# them to stay aligned.
PUBLICATION_TIERS: dict[str, frozenset[str]] = {
    "public": frozenset({"public"}),
    "subscriber": frozenset({"public", "subscriber"}),
    "internal": frozenset({"public", "subscriber", "internal"}),
    "researcher-restricted": frozenset(
        {"public", "subscriber", "researcher-restricted"}),
    "investigator-restricted": frozenset(
        {"public", "subscriber", "investigator-restricted"}),
    # `confidential` and `private-preservation` are absent deliberately: they
    # are not publication targets at any tier (SEC-001, §12).
}

REVISION_KINDS = ("initial", "update", "correction", "retraction")


class PublicationError(Exception):
    """A publication act that must not proceed."""


def _uuid() -> str:
    return str(uuid.uuid4())


def digest(text: str) -> str:
    """SHA-256 of the exact rendered text (§86, DR-0005)."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Versions:
    """What a revision was built from (§86).

    All four are required. A published statement whose methodology version is
    unrecorded cannot be reproduced, and Principle 16 makes reproducibility
    the point rather than an aspiration — so this is a dataclass with no
    defaults rather than a bag of optional keyword arguments.
    """

    methodology: str
    terminology: str
    template: str
    release_baseline: str | None = None


class Publisher:
    """Gate 3 over one database connection."""

    def __init__(self, conn):
        self.conn = conn

    # -- the decision --------------------------------------------------------

    def decide(
        self,
        *,
        person_id: str,
        access_tier: str,
        rights_basis: str,
        rationale: str,
        assertion_id: str | None = None,
        holding_id: str | None = None,
        sensitivity: str | None = None,
        evidentiary_disclosure: str | None = None,
    ) -> str:
        """Record a publication decision for one conclusion or one holding.

        The four §12 dimensions stay apart (SEC-003). `access_tier` says who
        may see it; `sensitivity` what makes it delicate; `rights_basis` what
        entitles the project to show it; `evidentiary_disclosure` what may be
        said about its evidentiary status. A thing can be public and
        sensitive, or rights-clear and undisclosable — one flag cannot say
        that.
        """
        if access_tier not in PUBLICATION_TIERS:
            raise PublicationError(
                f"{access_tier!r} is not a publication target. Available: "
                + ", ".join(sorted(PUBLICATION_TIERS))
                + ". 'confidential' and 'private-preservation' are excluded "
                "deliberately: material at those tiers reaches a recipient "
                "under an explicit arrangement, never a published surface "
                "(SEC-001, §12)."
            )
        if not rationale.strip():
            raise PublicationError(
                "a publication decision without a rationale cannot be "
                "reviewed, and reversing it later needs to know what it "
                "rested on"
            )

        decision_id = _uuid()
        self.conn.execute(
            """
            INSERT INTO publication_decision
                (id, assertion_id, holding_id, decided_by, access_tier,
                 sensitivity, rights_basis, evidentiary_disclosure, rationale)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (decision_id, assertion_id, holding_id, person_id, access_tier,
             sensitivity, rights_basis, evidentiary_disclosure, rationale),
        )
        return decision_id

    def withdraw(self, *, decision_id: str, ground: str) -> None:
        """Withdraw a publication decision. The row stays.

        §77 forbids silently unpublishing: "we published this and later
        withdrew it" is part of the record, and a reader who saw the earlier
        page is entitled to find out what happened to it.
        """
        if not ground.strip():
            raise PublicationError("a withdrawal states its ground (§77)")
        self.conn.execute(
            "UPDATE publication_decision SET withdrawn_at = now(), "
            "withdrawal_ground = %s WHERE id = %s",
            (ground, decision_id),
        )

    # -- pages and revisions -------------------------------------------------

    def create_page(
        self, *, path: str, language: str, translation_of: str | None = None
    ) -> str:
        """Register a page. Its history begins here (DR-0052, OPS-004)."""
        page_id = _uuid()
        self.conn.execute(
            "INSERT INTO published_page (id, path, language, translation_of) "
            "VALUES (%s,%s,%s,%s)",
            (page_id, path, language, translation_of),
        )
        return page_id

    def publish(
        self,
        *,
        page_id: str,
        person_id: str,
        rendered_text: str,
        versions: Versions,
        assertions: list[str] | None = None,
        holdings: list[str] | None = None,
        kind: str | None = None,
        change_note: str | None = None,
        review_qualification: str | None = None,
    ) -> str:
        """Publish a revision of a page.

        Everything lands in one transaction: the tier check (SEC-004) and the
        review-qualification check (METH-0001 §10.1) are deferred constraint
        triggers over the revision *and its contents*, so a revision written
        alone would be judged on an empty page.

        `kind` defaults to `initial` for a page's first revision and `update`
        afterwards. A `correction` or `retraction` must say what it changes
        (§77) — being wrong and correcting the record leaves a trace.
        """
        if kind is not None and kind not in REVISION_KINDS:
            raise PublicationError(
                f"{kind!r} is not a revision kind: {', '.join(REVISION_KINDS)}"
            )

        with self.conn.transaction():
            row = self.conn.execute(
                "SELECT coalesce(max(revision), 0), "
                "       (SELECT id FROM page_revision "
                "         WHERE page_id = %s ORDER BY revision DESC LIMIT 1) "
                "  FROM page_revision WHERE page_id = %s",
                (page_id, page_id),
            ).fetchone()
            previous, previous_id = row[0], row[1]
            revision = previous + 1
            kind = kind or ("initial" if revision == 1 else "update")

            if kind in ("correction", "retraction") and previous == 0:
                raise PublicationError(
                    f"a {kind} needs something to correct; a page's first "
                    "revision is `initial`"
                )

            revision_id = _uuid()
            self.conn.execute(
                """
                INSERT INTO page_revision
                    (id, page_id, revision, kind, published_by, rendered_text,
                     text_digest, release_baseline, methodology_version,
                     terminology_version, template_version,
                     review_qualification, supersedes_id, change_note)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (revision_id, page_id, revision, kind, person_id,
                 rendered_text, digest(rendered_text), versions.release_baseline,
                 versions.methodology, versions.terminology, versions.template,
                 review_qualification,
                 previous_id if kind in ("correction", "retraction") else None,
                 change_note),
            )
            for assertion_id in assertions or []:
                self.conn.execute(
                    "INSERT INTO revision_assertion (revision_id, assertion_id) "
                    "VALUES (%s,%s)", (revision_id, assertion_id))
            for holding_id in holdings or []:
                self.conn.execute(
                    "INSERT INTO revision_holding (revision_id, holding_id) "
                    "VALUES (%s,%s)", (revision_id, holding_id))
        return revision_id

    def required_qualification(self, assertions: list[str]) -> str | None:
        """The review qualification these conclusions would require.

        Call it before `publish()` to find out what the page must carry. The
        schema refuses a revision that omits it; this tells you what to write
        instead of making you guess from the error.
        """
        row = self.conn.execute(
            """
            SELECT review_qualification FROM publishable_conclusion
             WHERE id = ANY(%s) AND consequence_limb IS NOT NULL
               AND review_qualification IS NOT NULL
             ORDER BY review_state LIMIT 1
            """,
            (assertions,),
        ).fetchone()
        return row[0] if row else None

    # -- reading the record --------------------------------------------------

    def site_as_of(self, when) -> list[tuple]:
        """What the site said on a given date (§86, §90)."""
        return self.conn.execute(
            "SELECT path, language, revision, kind::text, published_at, "
            "text_digest, methodology_version, terminology_version, "
            "release_baseline, review_qualification "
            "FROM site_as_of(%s) ORDER BY path",
            (when,),
        ).fetchall()

    def history(self, path: str) -> list[tuple]:
        """A page's full history, corrections and retractions included (§77)."""
        return self.conn.execute(
            "SELECT revision, kind::text, published_at, change_note, "
            "text_digest FROM page_history WHERE path = %s ORDER BY revision",
            (path,),
        ).fetchall()

    def reproduce(self, *, path: str, revision: int) -> dict | None:
        """Everything needed to reconstruct one published statement (§86).

        Returns the exact text with the versions it was built from and the
        assertions it rendered. This is the shape EDIT-005's demonstration
        needs: reproduce a published conclusion from its named baseline and
        get the same text, evidence and methodology back.
        """
        row = self.conn.execute(
            """
            SELECT r.id, r.rendered_text, r.text_digest, r.published_at,
                   r.methodology_version, r.terminology_version,
                   r.template_version, r.release_baseline,
                   r.review_qualification, r.kind::text, p.language
              FROM page_revision r
              JOIN published_page p ON p.id = r.page_id
             WHERE p.path = %s AND r.revision = %s
            """,
            (path, revision),
        ).fetchone()
        if row is None:
            return None

        assertions = [
            str(a[0]) for a in self.conn.execute(
                "SELECT assertion_id FROM revision_assertion WHERE "
                "revision_id = %s ORDER BY assertion_id", (row[0],))
        ]
        holdings = [
            str(h[0]) for h in self.conn.execute(
                "SELECT holding_id FROM revision_holding WHERE "
                "revision_id = %s ORDER BY holding_id", (row[0],))
        ]
        return {
            "path": path,
            "revision": revision,
            "kind": row[9],
            "language": row[10],
            "rendered_text": row[1],
            "text_digest": row[2],
            "digest_verifies": digest(row[1]) == row[2],
            "published_at": row[3],
            "methodology_version": row[4],
            "terminology_version": row[5],
            "template_version": row[6],
            "release_baseline": row[7],
            "review_qualification": row[8],
            "assertions": assertions,
            "holdings": holdings,
        }

    def published_conclusions(self) -> list[tuple]:
        """Conclusions that reached a surface, with what a reader was told."""
        return self.conn.execute(
            "SELECT assertion_id, path, revision, access_tier::text, "
            "review_qualification, withdrawn_at FROM published_conclusion "
            "ORDER BY path, revision"
        ).fetchall()
