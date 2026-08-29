#!/usr/bin/env python3
"""Access-tier policy for durable exports.

Resolves the risk SPEC-0006 §9 recorded and DR-0084 acted on: a dump of
everything is a dump of confidential material too (§12, SEC-001). No dump may
be produced without saying, explicitly, what it is for and who may hold it.

Two purposes, and the distinction is not cosmetic:

  preservation  Complete. Nothing filtered, because succession (PRES-010) and
                reconstruction (PRES-009) need the whole archive. Carries the
                highest tier present and may only be handled accordingly.

  disclosure    Filtered to a named access tier. Rows above it are omitted,
                and the count of omissions is recorded so the dump does not
                misrepresent its own completeness (§57).

Two safety properties, both structural rather than procedural:

  * **Fail closed.** Every table must have a declared tier rule. A table added
    to the schema without one makes the dump refuse rather than quietly
    exporting it at public tier. Combined with SPEC-0006 §3's catalogue-derived
    table list, a forgotten table is loud in both directions: it appears, and
    it stops the run until someone classifies it.

  * **No accidental dump.** There is no default purpose and no default tier.
"""

from __future__ import annotations

from dataclasses import dataclass

# Tiers are not a total order. `researcher-restricted` and
# `investigator-restricted` are lateral grants to named parties, not steps on
# a ladder, and `private-preservation` is "disclosed to nobody" (§12).
# Containment is therefore declared, not computed from an ordering.
DISCLOSURE_TIERS: dict[str, frozenset[str]] = {
    "public": frozenset({"public"}),
    "subscriber": frozenset({"public", "subscriber"}),
    "internal": frozenset({"public", "subscriber", "internal"}),
    # A grant to named researchers admits the open material plus what the
    # grant covers — not the project's internal working data, and never
    # confidential source identity.
    "researcher-restricted": frozenset(
        {"public", "subscriber", "researcher-restricted"}
    ),
    "investigator-restricted": frozenset(
        {"public", "subscriber", "investigator-restricted"}
    ),
    # Deliberately absent: `confidential` and `private-preservation` are not
    # disclosure targets. Confidential material reaches a recipient through a
    # preservation dump under an explicit arrangement, never through a
    # routine disclosure export (SEC-001).
}


# How restrictive each tier is, for the question "several tiers apply; which
# governs?" The answer must be the most restrictive, and it cannot be read off
# an alphabetical or enum ordering — `min('public','subscriber')` is 'public'
# alphabetically, which is the *less* restrictive of the two and exactly the
# wrong answer.
#
# `researcher-restricted` and `investigator-restricted` share a rank because
# they are lateral grants to different named parties, not rungs. Where both
# apply, neither grant covers the other's material, so the resolution
# escalates to `internal` rather than picking one.
RESTRICTIVENESS: dict[str, int] = {
    "public": 0,
    "subscriber": 1,
    "researcher-restricted": 2,
    "investigator-restricted": 2,
    "internal": 3,
    "confidential": 4,
    "private-preservation": 5,
}


def most_restrictive(tiers) -> str:
    """The tier that governs when several apply. Fails closed on the unknown."""
    tiers = [t for t in tiers if t is not None]
    if not tiers:
        return "confidential"          # unclassified is not the same as safe
    unknown = [t for t in tiers if t not in RESTRICTIVENESS]
    if unknown:
        raise TierPolicyError(
            "unranked access tier(s): " + ", ".join(sorted(set(unknown)))
            + ". A tier with no declared restrictiveness cannot be resolved "
            "against others; add it to RESTRICTIVENESS deliberately."
        )
    top = max(RESTRICTIVENESS[t] for t in tiers)
    winners = {t for t in tiers if RESTRICTIVENESS[t] == top}
    if len(winners) > 1:
        # Two lateral grants. Neither covers the other's material.
        return "internal"
    return winners.pop()


@dataclass(frozen=True)
class TierRule:
    """How to determine the access tier of a table's rows.

    kind:
      fixed   — every row in the table sits at `tier`
      column  — the row's tier is in `column`
      join    — the tier comes from elsewhere; `sql` yields (id, tier) pairs
    """

    kind: str
    tier: str | None = None
    column: str | None = None
    sql: str | None = None
    rationale: str = ""


# Every base table must appear here. The test suite fails if the schema
# contains a table this mapping does not classify.
TIER_RULES: dict[str, TierRule] = {
    # -- carry their own tier -------------------------------------------
    "holding": TierRule(
        "column", column="access_tier",
        rationale="A holding's tier is set at Gate 1 from its source (DR-0067).",
    ),
    "source": TierRule(
        "column", column="default_access_tier",
        rationale="A source's own tier governs what it yields.",
    ),

    # -- inherit from the holding they belong to -------------------------
    "preserved_object": TierRule(
        "join",
        sql="""
            SELECT o.id, most_restrictive_tier(
                       array_remove(array_agg(h.access_tier), NULL))::text
              FROM preserved_object o
              LEFT JOIN holding_representation hr ON hr.object_id = o.id
              LEFT JOIN holding h ON h.id = hr.holding_id
             GROUP BY o.id
        """,
        rationale=(
            "Bytes are as restricted as the most restricted holding that "
            "references them. An object referenced by no holding is treated as "
            "confidential, not public: an unclassified object is not a safe "
            "one. Resolution goes through `most_restrictive_tier()` — an "
            "earlier version used min() over the tier text, which is "
            "alphabetical and returns 'public' for {public, subscriber}, "
            "the opposite of what this rationale claims."
        ),
    ),
    "holding_representation": TierRule(
        "join",
        sql="""
            SELECT hr.holding_id::text || ':' || hr.object_id::text,
                   h.access_tier::text
              FROM holding_representation hr
              JOIN holding h ON h.id = hr.holding_id
        """,
        rationale="Follows its holding.",
    ),
    "documentary_assertion": TierRule(
        "join",
        sql="""
            SELECT a.id, coalesce(h.access_tier::text, 'confidential')
              FROM documentary_assertion a
              LEFT JOIN holding h ON h.id = a.holding_id
        """,
        rationale="What a source said is as restricted as the holding it is in.",
    ),
    "evidence_relation": TierRule(
        "join",
        sql="""
            SELECT e.id, coalesce(h.access_tier::text, 'internal')
              FROM evidence_relation e
              LEFT JOIN holding h ON h.id = e.holding_id
        """,
        rationale=(
            "An evidence relation exposes what the project is investigating. "
            "Without a holding to inherit from it stays internal."
        ),
    ),
    "capture_series_member": TierRule(
        "join",
        sql="""
            SELECT c.series_id::text || ':' || c.holding_id::text,
                   h.access_tier::text
              FROM capture_series_member c
              JOIN holding h ON h.id = c.holding_id
        """,
        rationale="Follows its holding.",
    ),

    # -- confidential by nature ------------------------------------------
    "quarantine_item": TierRule(
        "fixed", tier="confidential",
        rationale=(
            "Carries submitter pseudonyms and submitter claims. Even the "
            "existence of a submission can identify a source (SEC-001, §11)."
        ),
    ),
    "pipeline_agent": TierRule(
        "fixed", tier="confidential",
        rationale=(
            "May include agents acting for confidential sources. Cheap to "
            "withhold; expensive to have disclosed by mistake."
        ),
    ),

    # -- internal working data -------------------------------------------
    "collector_run": TierRule(
        "fixed", tier="internal",
        rationale="Coverage and operational detail; ships with releases in summary form instead (DR-0070).",
    ),
    "acquisition_attempt": TierRule(
        "fixed", tier="internal",
        rationale="Reveals what the project sought, including what it failed to get.",
    ),
    "preservation_event": TierRule(
        "fixed", tier="internal",
        rationale="Operational preservation record.",
    ),
    "source_dependence": TierRule(
        "fixed", tier="internal",
        rationale="Analytical judgment about sources (DR-0028).",
    ),
    "world_actor": TierRule(
        "fixed", tier="internal",
        rationale=(
            "Bare entity rows carrying an entity status. Publishing which "
            "identities the project treats as fabricated or disproved is an "
            "editorial act, not a data export (DR-0062)."
        ),
    ),
    "proposition": TierRule(
        "fixed", tier="internal",
        rationale="Propositions under investigation, including ones not concluded.",
    ),

    # -- Gate 2: editorial layer -------------------------------------------
    #
    # Everything Gate 2 produces sits at `internal` for one structural
    # reason: **Gate 3 does not exist yet.** OPS-001 requires that no path
    # lead to a public surface without a recorded Gate 3 decision, and
    # publishing this material in a public dump would be exactly that path.
    #
    # This is not a judgment that the project's own conclusions are secret.
    # It is the classification that holds while the publication gate is
    # unbuilt; when Gate 3 lands, these become `join` rules following each
    # conclusion's recorded publication decision, the way holdings already
    # follow their source.

    "proposal": TierRule(
        "fixed", tier="internal",
        rationale=(
            "What automation extracted, including what a person then "
            "rejected. Reveals what the project is investigating before it "
            "has concluded anything (DR-0063)."
        ),
    ),
    "acceptance": TierRule(
        "fixed", tier="internal",
        rationale=(
            "Editorial decisions with their reasoning, including rejections "
            "and the discriminating evidence relied on. Working record, not "
            "published output (SPEC-0003 §7)."
        ),
    ),
    "project_assertion": TierRule(
        "fixed", tier="internal",
        rationale=(
            "The project's own voice — but nothing here has passed Gate 3. "
            "Disclosing a conclusion at public tier without a publication "
            "decision is the path OPS-001 forbids."
        ),
    ),
    "critical_question_answer": TierRule(
        "fixed", tier="internal",
        rationale="Follows its assertion; discloses which checks remain open.",
    ),
    "review_record": TierRule(
        "fixed", tier="internal",
        rationale=(
            "Editorial process record. The *qualification* a reader must see "
            "is rendered from `publishable_conclusion` at Gate 3 "
            "(METH-0001 §10.1); the review record itself stays internal."
        ),
    ),
    "hypothesis_set": TierRule(
        "fixed", tier="internal",
        rationale=(
            "Which explanations the project entertains about named parties. "
            "Publishing an unconcluded hypothesis reads as an accusation — "
            "the same reasoning that keeps entity statuses internal "
            "(DR-0062)."
        ),
    ),
    "hypothesis": TierRule(
        "fixed", tier="internal", rationale="Follows its set.",
    ),
    "conclusion_hypothesis_set": TierRule(
        "fixed", tier="internal", rationale="Follows its set.",
    ),
    "argument": TierRule(
        "fixed", tier="internal",
        rationale=(
            "Reasoning about conclusions that have not been published. "
            "Evidence packages export argument structure deliberately and "
            "case by case (DR-0007), never through a routine dump."
        ),
    ),
    "argument_premise": TierRule(
        "fixed", tier="internal", rationale="Follows its argument.",
    ),
    "defeater": TierRule(
        "fixed", tier="internal",
        rationale=(
            "A live objection to an unpublished conclusion. Disclosing the "
            "attack without the conclusion it attacks misleads in both "
            "directions."
        ),
    ),

    # -- Gate 3: the published surface --------------------------------------
    #
    # These are the one part of the store that is public by nature: they
    # record what the project already said in public, at a tier a person
    # deliberately chose. They travel at that tier — a decision to publish at
    # `public` is itself public, and one taken at `subscriber` travels with
    # its content.
    #
    # The deliberate cost: `rationale` and `sensitivity` travel too. That is
    # the right default for a project whose method is meant to be
    # inspectable (§85), but it makes the rationale field a place where
    # personal data must not be written casually — POL-0001's structuring
    # decision governs what goes in it.

    "publication_decision": TierRule(
        "column", column="access_tier",
        rationale=(
            "A publication decision travels at the tier it granted. Its "
            "rationale is disclosed with it, which is intended: the reasons "
            "for publishing are part of what makes editorial independence "
            "demonstrable (§85)."
        ),
    ),
    "published_page": TierRule(
        "join",
        sql="""
            SELECT p.id, most_restrictive_tier(
                       array_remove(array_agg(pd.access_tier), NULL))::text
              FROM published_page p
              LEFT JOIN page_revision r ON r.page_id = p.id
              LEFT JOIN revision_assertion ra ON ra.revision_id = r.id
              LEFT JOIN publication_decision pd
                     ON pd.assertion_id = ra.assertion_id
                    AND pd.withdrawn_at IS NULL
             GROUP BY p.id
        """,
        rationale=(
            "A page is as restricted as its most restricted live decision. A "
            "page whose decisions were all withdrawn resolves to "
            "`confidential` and stays out of disclosure dumps — it is no "
            "longer published, and re-disclosing it through an export would "
            "undo the withdrawal (§77)."
        ),
    ),
    "page_revision": TierRule(
        "join",
        sql="""
            SELECT r.id, most_restrictive_tier(
                       array_remove(array_agg(pd.access_tier), NULL))::text
              FROM page_revision r
              LEFT JOIN revision_assertion ra ON ra.revision_id = r.id
              LEFT JOIN publication_decision pd
                     ON pd.assertion_id = ra.assertion_id
                    AND pd.withdrawn_at IS NULL
             GROUP BY r.id
        """,
        rationale=(
            "Follows the decisions behind the content it rendered. The "
            "revision carries the exact published text, so its tier must "
            "track what that text was cleared to say."
        ),
    ),
    "revision_assertion": TierRule(
        "fixed", tier="internal",
        rationale=(
            "Which internal assertions a page rendered. The page text is as "
            "public as its decision; the mapping back into the assertion "
            "layer is working data, and the assertions themselves are "
            "`internal` (above)."
        ),
    ),
    "revision_holding": TierRule(
        "fixed", tier="internal",
        rationale="Follows revision_assertion, for the same reason.",
    ),

    # -- public reference data --------------------------------------------
    "source_types": TierRule("fixed", tier="public", rationale="Registry vocabulary."),
    "classification_systems": TierRule("fixed", tier="public", rationale="Registry vocabulary."),
    "identifier_types": TierRule("fixed", tier="public", rationale="Registry vocabulary."),
    "assertion_core_columns": TierRule(
        "fixed", tier="public",
        rationale="A documented contract, not data (SPEC-0001 §2.1).",
    ),
}


class TierPolicyError(Exception):
    """Raised when a dump cannot be classified, so it must not be produced."""


def unclassified_tables(tables: list[str]) -> list[str]:
    """Tables with no declared rule. Any result means the dump must refuse."""
    return sorted(t for t in tables if t not in TIER_RULES)


def check_complete(tables: list[str]) -> None:
    missing = unclassified_tables(tables)
    if missing:
        raise TierPolicyError(
            "no access-tier rule declared for: " + ", ".join(missing) + ". "
            "A dump cannot be produced until every table is classified "
            "(DR-0084). Add a rule to export/tiers.py — deliberately, since "
            "the wrong answer discloses material that should not be."
        )


def resolve_disclosure(tier: str) -> frozenset[str]:
    if tier not in DISCLOSURE_TIERS:
        raise TierPolicyError(
            f"{tier!r} is not a disclosure target. Available: "
            + ", ".join(sorted(DISCLOSURE_TIERS))
            + ". 'confidential' and 'private-preservation' are deliberately "
            "excluded: material at those tiers reaches a recipient through a "
            "preservation dump under an explicit arrangement, never a routine "
            "disclosure export (SEC-001, §12)."
        )
    return DISCLOSURE_TIERS[tier]


def row_tiers(conn, table: str) -> dict[str, str] | str:
    """Tier per row for `table`, or a single tier if the rule is fixed."""
    rule = TIER_RULES[table]
    if rule.kind == "fixed":
        return rule.tier  # type: ignore[return-value]
    if rule.kind == "column":
        return {
            str(row[0]): row[1]
            for row in conn.execute(
                f'SELECT id, {rule.column}::text FROM "{table}"'
            )
        }
    return {str(row[0]): row[1] for row in conn.execute(rule.sql)}


def row_key(table: str, row: dict) -> str:
    """The identifier a tier map is keyed by — composite for link tables."""
    if table == "holding_representation":
        return f"{row['holding_id']}:{row['object_id']}"
    if table == "capture_series_member":
        return f"{row['series_id']}:{row['holding_id']}"
    return str(row["id"])
