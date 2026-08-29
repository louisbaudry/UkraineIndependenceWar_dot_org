#!/usr/bin/env python3
"""Gate 2 — editorial acceptance (SPEC-0003 §2, §7; DR-0066).

The gate between a preserved holding and canonical knowledge. Its whole
purpose is that **nothing crosses on automated confidence alone**: extractions
and matches arrive as proposals and become canonical only by a person's
acceptance, at the risk tier the content demands.

The API mirrors the acts a person actually performs, because those acts are
what the record has to show:

    propose()               automation offers something
    accept() / reject()     a person decides, at a tier, with reasoning
    adopt()                 the accepted proposal becomes a project assertion
    assert_directly()       a person's own judgment, no proposal involved
    record_review()         what review the conclusion actually received
    open_hypothesis_set()   competing explanations for a defined question
    record_argument()       premises, warrant, and the scheme relied on
    raise_defeater()        a typed attack; answering it is a separate act

Most of the discipline is in the schema (05-editorial.sql, 06-argument.sql),
where it holds regardless of which code path writes. This module is the path
that makes the right thing convenient — it does not enforce what the database
already enforces, and it deliberately does not catch those exceptions.

Not covered here: Gate 1 (collector/pipeline.py) or Gate 3, which does not
exist yet. A conclusion may pass Gate 2 and never be published; that is the
normal case, and Principle 11 requires the two to stay independent.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from typing import Any

# METH-0001 §1.5, ruled by DR-0085 Q1. A conclusion is consequential if any
# one of these holds; they are not cumulative.
CONSEQUENCE_LIMBS = (
    "names-identifiable-party",
    "feeds-legal-layer",
    "materially-relied-on",
)

# METH-0001 §7, ruled by DR-0085 Q3. All three are mandatory triggers, the
# third deliberately being the uncomfortable one.
HYPOTHESIS_TRIGGERS = ("single-explanation", "consequential", "strong-prior")

# Tier ordering by scrutiny, highest first. The enum's own ordering already
# runs this way; naming it here keeps the queue code honest about which
# direction "higher" means.
TIERS_BY_SCRUTINY = ("T1", "T2", "T3")


class GateError(Exception):
    """A Gate 2 act that must not proceed."""


def _uuid() -> str:
    return str(uuid.uuid4())


def timespan(value) -> tuple:
    """Normalize a caller's valid time to the five-field composite.

    Accepts the full five-tuple, a shorter prefix, or a single absence state.
    A span carries bounds *or* declares why it has none — never both and never
    neither (DR-0029: a missing value must not quietly mean "no").
    """
    if isinstance(value, str):                      # an absence state alone
        return (None, None, None, None, value)
    fields = tuple(value) + (None,) * (5 - len(value))
    if len(fields) != 5:
        raise GateError(
            "a timespan has five fields (begin_earliest, begin_latest, "
            "end_earliest, end_latest, absence)"
        )
    if any(f is not None for f in fields[:4]) == (fields[4] is not None):
        raise GateError(
            "a timespan carries bounds or declares an absence state, never "
            "both and never neither (DR-0029)"
        )
    return fields


@dataclass
class Proposal:
    """What automation produced, before anyone accepted it."""

    id: str
    kind: str
    review_tier: str
    state: str
    content: dict[str, Any]
    feature_basis: dict[str, Any] = field(default_factory=dict)


class Gate:
    """Editorial acceptance over one database connection."""

    def __init__(self, conn):
        self.conn = conn

    # -- what automation may do ---------------------------------------------

    def propose(
        self,
        *,
        agent_id: str,
        kind: str,
        content: dict,
        feature_basis: dict,
        review_tier: str,
        holding_id: str | None = None,
        documentary_assertion_id: str | None = None,
        ai_provenance: dict | None = None,
    ) -> str:
        """Record a proposal. Never creates canonical knowledge (AI-003).

        `feature_basis` is what a reviewer interrogates — the features the
        extractor actually relied on. An empty basis makes the proposal
        unreviewable, so it is refused here rather than accepted and puzzled
        over later.
        """
        if not feature_basis:
            raise GateError(
                "a proposal needs a feature basis: a reviewer confirms on "
                "discriminating evidence, and there is nothing to interrogate "
                "without one (DR-0063)"
            )
        if review_tier not in TIERS_BY_SCRUTINY:
            raise GateError(f"unknown review tier {review_tier!r}")

        proposal_id = _uuid()
        self.conn.execute(
            """
            INSERT INTO proposal (id, kind, proposed_by, holding_id,
                                  documentary_assertion_id, content,
                                  feature_basis, review_tier, ai_provenance)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (proposal_id, kind, agent_id, holding_id, documentary_assertion_id,
             json.dumps(content), json.dumps(feature_basis), review_tier,
             json.dumps(ai_provenance) if ai_provenance else None),
        )
        return proposal_id

    # -- what only a person may do ------------------------------------------

    def accept(
        self,
        *,
        proposal_id: str,
        person_id: str,
        tier_applied: str,
        reasoning: str,
        batch_id: str | None = None,
    ) -> str:
        """Accept a proposal at a tier, with reasoning.

        The reasoning is not decoration. At T1 and T2 it is the record of the
        discriminating evidence relied on — DR-0063 forbids confirmation on
        name similarity alone, at any tier, and this column is where a later
        audit finds out what was actually relied on.
        """
        return self._decide(proposal_id, person_id, "confirmed", tier_applied,
                            reasoning, batch_id)

    def reject(
        self, *, proposal_id: str, person_id: str, tier_applied: str,
        reasoning: str,
    ) -> str:
        """Reject a proposal. The record is kept and is meant to be consulted.

        SPEC-0003 §7 retains rejections as audit trail and matcher input
        alike: a rejection nobody can look up gets re-proposed forever.
        """
        return self._decide(proposal_id, person_id, "rejected", tier_applied,
                            reasoning, None)

    def _decide(self, proposal_id, person_id, disposition, tier_applied,
                reasoning, batch_id) -> str:
        if not reasoning.strip():
            raise GateError(
                "a Gate 2 decision without reasoning is unreviewable; "
                "rejections especially are kept to be consulted (SPEC-0003 §7)"
            )
        acceptance_id = _uuid()
        self.conn.execute(
            """
            INSERT INTO acceptance (id, proposal_id, decided_by, disposition,
                                    tier_applied, reasoning, batch_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,
            (acceptance_id, proposal_id, person_id, disposition, tier_applied,
             reasoning, batch_id),
        )
        return acceptance_id

    def adopt(
        self,
        *,
        proposal_id: str,
        asserter_id: str,
        proposition_id: str,
        valid_time: tuple,
        epistemic_category: str,
        consequence_limb: str | None = None,
        likelihood: str | None = None,
        confidence: str | None = None,
        reasoning: str | None = None,
        basis: dict | None = None,
    ) -> str:
        """Turn a confirmed proposal into a project assertion.

        Adoption is a separate act from acceptance, and deliberately so: the
        adopting agent takes on the content as if they had authored it
        (METH-0001 §11). The database refuses adoption of anything not
        confirmed by a person.
        """
        return self._assert(
            proposition_id=proposition_id, asserter_id=asserter_id,
            valid_time=valid_time, epistemic_category=epistemic_category,
            adopted_from_id=proposal_id, consequence_limb=consequence_limb,
            likelihood=likelihood, confidence=confidence, reasoning=reasoning,
            basis=basis,
        )

    def assert_directly(self, **kwargs) -> str:
        """A person's own judgment, formed without a proposal.

        Equally legitimate and equally accountable. §79 asks who holds the
        belief, not where it came from.
        """
        return self._assert(adopted_from_id=None, **kwargs)

    def raise_late_critical_question(
        self, *, assertion_id: str, scheme_id: str, question_id: str,
        unanswered_defeater: str, asserter_id: str, reason: str,
    ) -> tuple[str, str]:
        """Raise a critical question against an assertion already recorded.

        The awkward case, and the one that matters: someone notices months
        later that a check was never done. The confidence cap would otherwise
        refuse the objection to protect the claim — the worst possible failure
        mode for an evidentiary archive.

        So the objection is admitted together with a superseding assertion at
        `moderate`, atomically. The original stands in the record at whatever
        it claimed; it was what the project held at the time (EVID-015), and
        the successor carries the corrected confidence.

        Returns (superseding assertion id, critical-question row id).
        """
        row = self.conn.execute(
            """
            SELECT proposition_id, epistemic_category::text, likelihood::text,
                   consequence_limb::text, reasoning,
                   (valid_time).begin_earliest, (valid_time).begin_latest,
                   (valid_time).end_earliest, (valid_time).end_latest,
                   (valid_time).absence::text
              FROM project_assertion WHERE id = %s
            """,
            (assertion_id,),
        ).fetchone()
        if row is None:
            raise GateError(f"no assertion {assertion_id}")

        with self.conn.transaction():
            successor = self._assert(
                proposition_id=row[0], asserter_id=asserter_id,
                valid_time=tuple(row[5:10]), epistemic_category=row[1],
                adopted_from_id=None, consequence_limb=row[3],
                likelihood=row[2], confidence="moderate",
                reasoning=(row[4] or "") + f"\n\nConfidence reduced: {reason}",
                supersedes_id=assertion_id,
            )
            question_id_row = self.record_critical_question(
                assertion_id=successor, scheme_id=scheme_id,
                question_id=question_id,
                unanswered_defeater=unanswered_defeater,
            )
        return successor, question_id_row

    def _assert(
        self, *, proposition_id, asserter_id, valid_time, epistemic_category,
        adopted_from_id, consequence_limb=None, likelihood=None,
        confidence=None, reasoning=None, basis=None, supersedes_id=None,
    ) -> str:
        if consequence_limb is not None and consequence_limb not in CONSEQUENCE_LIMBS:
            raise GateError(
                f"{consequence_limb!r} is not a limb of the consequence test. "
                f"METH-0001 §1.5: {', '.join(CONSEQUENCE_LIMBS)}"
            )
        assertion_id = _uuid()
        self.conn.execute(
            """
            INSERT INTO project_assertion
                (id, valid_time, asserter_id, epistemic_category, likelihood,
                 confidence, basis, proposition_id, adopted_from_id,
                 consequence_limb, reasoning, supersedes_id)
            VALUES (%s, ROW(%s,%s,%s,%s,%s)::timespan,
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (assertion_id, *timespan(valid_time),
             asserter_id, epistemic_category, likelihood, confidence,
             json.dumps(basis) if basis else None, proposition_id,
             adopted_from_id, consequence_limb, reasoning, supersedes_id),
        )
        return assertion_id

    # -- critical questions (METH-0001 §6.2) --------------------------------

    def record_critical_question(
        self, *, assertion_id: str, scheme_id: str, question_id: str,
        answer: str | None = None, answered_by: str | None = None,
        unanswered_defeater: str | None = None,
    ) -> str:
        """Record a critical question as answered, or as standing open.

        An open question must declare the defeater type it implies — that is
        the scheme's own declaration, and it is what makes the confidence cap
        defensible rather than arbitrary. The cap itself lives in the schema.
        """
        row_id = _uuid()
        self.conn.execute(
            """
            INSERT INTO critical_question_answer
                (id, assertion_id, scheme_id, question_id, answer,
                 unanswered_defeater, answered_by)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,
            (row_id, assertion_id, scheme_id, question_id, answer,
             unanswered_defeater, answered_by),
        )
        return row_id

    def open_questions(self, assertion_id: str) -> list[tuple[str, str, str]]:
        """Which critical questions still stand open, and what they imply."""
        return [
            (row[0], row[1], row[2])
            for row in self.conn.execute(
                """
                SELECT scheme_id, question_id, unanswered_defeater::text
                  FROM critical_question_answer
                 WHERE assertion_id = %s AND answer IS NULL
                 ORDER BY scheme_id, question_id
                """,
                (assertion_id,),
            )
        ]

    # -- review (METH-0001 §10.1) -------------------------------------------

    def record_review(
        self, *, assertion_id: str, tier_required: str, state: str,
        reviewed_by: str | None = None, notes: str | None = None,
    ) -> str:
        """Record what review a conclusion actually received.

        `unreviewed` is a legitimate state and the honest one while the
        project is one person. What it is not is invisible: the
        `publishable_conclusion` view renders the qualification a reader sees.
        """
        row_id = _uuid()
        self.conn.execute(
            """
            INSERT INTO review_record
                (id, assertion_id, tier_required, state, reviewed_by, notes)
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (row_id, assertion_id, tier_required, state, reviewed_by, notes),
        )
        return row_id

    def publication_qualification(self, assertion_id: str) -> str | None:
        """The qualification a publication surface must render, if any."""
        row = self.conn.execute(
            "SELECT review_qualification FROM publishable_conclusion WHERE id = %s",
            (assertion_id,),
        ).fetchone()
        return row[0] if row else None

    # -- hypotheses (METH-0001 §7) ------------------------------------------

    def open_hypothesis_set(
        self, *, question: str, opened_by: str, trigger: str,
        hypotheses: list[tuple[str, bool]],
    ) -> str:
        """Open a competing-hypothesis set.

        `hypotheses` is a list of (proposition_id, is_alternative). At least
        two, at least one alternative — enforced by the schema, which is why
        this method does not re-check it.
        """
        if trigger not in HYPOTHESIS_TRIGGERS:
            raise GateError(
                f"{trigger!r} is not a hypothesis-set trigger. METH-0001 §7: "
                f"{', '.join(HYPOTHESIS_TRIGGERS)}"
            )
        set_id = _uuid()
        # One transaction: the "at least two, one alternative" rule is a
        # deferred constraint trigger, so a set and its hypotheses must reach
        # the database together or the empty set is rejected on its own.
        with self.conn.transaction():
            self.conn.execute(
                "INSERT INTO hypothesis_set (id, question, opened_by, trigger) "
                "VALUES (%s,%s,%s,%s)",
                (set_id, question, opened_by, trigger),
            )
            for proposition_id, is_alternative in hypotheses:
                self.conn.execute(
                    "INSERT INTO hypothesis (id, set_id, proposition_id, "
                    "is_alternative) VALUES (%s,%s,%s,%s)",
                    (_uuid(), set_id, proposition_id, is_alternative),
                )
        return set_id

    def link_hypothesis_set(self, *, assertion_id: str, set_id: str) -> None:
        self.conn.execute(
            "INSERT INTO conclusion_hypothesis_set (assertion_id, set_id) "
            "VALUES (%s,%s)",
            (assertion_id, set_id),
        )

    def discriminating_evidence(self, set_id: str) -> list[str]:
        """Evidence that tells the hypotheses apart — the point of the set.

        Evidence consistent with every hypothesis distinguishes nothing,
        however much of it there is. This query doubles as the research-gap
        inventory: an empty result names what still needs finding (§74–75).
        """
        return [
            str(row[0])
            for row in self.conn.execute(
                "SELECT DISTINCT evidence_id FROM discriminating_evidence "
                "WHERE set_id = %s AND evidence_id IS NOT NULL",
                (set_id,),
            )
        ]

    # -- arguments (DR-0032, DR-0033) ---------------------------------------

    def record_argument(
        self, *, assertion_id: str, warrant: str, made_by: str,
        scheme_id: str | None = None, premises: list[dict] | None = None,
    ) -> str:
        """Record the inference: its warrant, its scheme, and its premises.

        The warrant is a required column because DR-0037 identifies it as one
        of the two Toulmin slots most often left implicit. A premise that
        rests on nothing in the archive is recorded as a named assumption —
        making it visible is the point, since an unattacked assumption is
        exactly what a reviewer should be able to find.
        """
        argument_id = _uuid()
        self.conn.execute(
            "INSERT INTO argument (id, assertion_id, scheme_id, warrant, "
            "made_by) VALUES (%s,%s,%s,%s,%s)",
            (argument_id, assertion_id, scheme_id, warrant, made_by),
        )
        for premise in premises or []:
            self.conn.execute(
                """
                INSERT INTO argument_premise
                    (id, argument_id, documentary_assertion_id,
                     evidence_relation_id, project_assertion_id, assumption)
                VALUES (%s,%s,%s,%s,%s,%s)
                """,
                (_uuid(), argument_id,
                 premise.get("documentary_assertion_id"),
                 premise.get("evidence_relation_id"),
                 premise.get("project_assertion_id"),
                 premise.get("assumption")),
            )
        return argument_id

    def raise_defeater(
        self, *, argument_id: str, kind: str, statement: str, raised_by: str
    ) -> str:
        """Raise a typed attack. Answering it is a separate, later act.

        The typing determines what an answer must do: answering a forgery
        claim (undermining) with more counter-evidence about the event
        (rebutting) addresses nothing (DR-0033).
        """
        defeater_id = _uuid()
        self.conn.execute(
            "INSERT INTO defeater (id, argument_id, kind, statement, "
            "raised_by) VALUES (%s,%s,%s,%s,%s)",
            (defeater_id, argument_id, kind, statement, raised_by),
        )
        return defeater_id

    def answer_defeater(
        self, *, defeater_id: str, answer: str, answered_by: str
    ) -> None:
        """Answer a defeater. Not answering is a legitimate end-state (§40)."""
        self.conn.execute(
            "UPDATE defeater SET answer = %s, answered_by = %s, "
            "answered_at = now() WHERE id = %s",
            (answer, answered_by, defeater_id),
        )

    def contested(self) -> list[tuple[str, int, list[str]]]:
        """Conclusions with live objections. Reports; adjudicates nothing."""
        return [
            (str(row[0]), row[1], row[2])
            for row in self.conn.execute(
                "SELECT assertion_id, unanswered_defeaters, unanswered_kinds "
                "FROM contested_conclusion ORDER BY unanswered_defeaters DESC"
            )
        ]

    # -- the queue (SPEC-0003 §7) -------------------------------------------

    def queue(self, limit: int = 50) -> list[Proposal]:
        """Proposals awaiting a decision, ordered by triage signals.

        Ordering only, never acceptance (DR-0027): a source grade decides what
        to look at first and how hard to look, and is architecturally barred
        from deciding what is true. Items may sit here indefinitely; queue
        depth and age are coverage metrics, not failures (SPEC-0003 §7).
        """
        rows = self.conn.execute(
            """
            SELECT p.id, p.kind, p.review_tier::text, p.state::text,
                   p.content, p.feature_basis
              FROM proposal p
             WHERE p.state IN ('proposed', 'under-review')
             ORDER BY p.review_tier, p.proposed_at
             LIMIT %s
            """,
            (limit,),
        ).fetchall()
        return [
            Proposal(id=str(r[0]), kind=r[1], review_tier=r[2], state=r[3],
                     content=r[4], feature_basis=r[5])
            for r in rows
        ]

    def queue_depth(self) -> dict[str, int]:
        """Depth per tier — a coverage metric (SPEC-0003 §7, OPS-006)."""
        return {
            row[0]: row[1]
            for row in self.conn.execute(
                "SELECT review_tier::text, count(*) FROM proposal "
                "WHERE state IN ('proposed','under-review') "
                "GROUP BY review_tier ORDER BY review_tier"
            )
        }
