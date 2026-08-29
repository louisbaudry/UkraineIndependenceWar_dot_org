#!/usr/bin/env python3
"""Tests for Gate 2 — editorial acceptance.

Each test names the requirement, decision record, or METH-0001 section it
verifies. The rules that matter most here are the ones a project under time
pressure would be tempted to bend: that AI output never becomes canonical on
its own, that an open critical question caps confidence, that a consequential
conclusion carries competing hypotheses, and that a conclusion nobody reviewed
says so where a reader can see it.

Run:  PGHOST=… PGPORT=… PGUSER=… python3 editorial/tests/test_gate2.py
"""

from __future__ import annotations

import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "editorial"))

import psycopg  # noqa: E402

from gate2 import Gate, GateError  # noqa: E402

PASSES: list[str] = []
FAILURES: list[str] = []
DB = "uiw_gate2_test"

WAR = ("2022-02-24", None, None, None, None)


def check(req: str, what: str, condition: bool) -> None:
    (PASSES if condition else FAILURES).append(
        f"{'PASS' if condition else 'FAIL'}  {req} — {what}")


def refuses(req: str, what: str, fn) -> None:
    """The act must be refused — by the schema or by the Gate."""
    try:
        fn()
    except (psycopg.Error, GateError):
        PASSES.append(f"PASS  {req} — {what}")
        return
    FAILURES.append(f"FAIL  {req} — {what}: accepted but must be refused")


def build_database() -> None:
    subprocess.run(["psql", "-q", "-c", f"DROP DATABASE IF EXISTS {DB}",
                    "-c", f"CREATE DATABASE {DB}", "postgres"],
                   check=True, capture_output=True)
    for sql in sorted((ROOT / "schema").glob("0*.sql")):
        subprocess.run(["psql", "-q", "-d", DB, "-v", "ON_ERROR_STOP=1",
                        "-f", str(sql)], check=True, capture_output=True)


def new_conn():
    return psycopg.connect(dbname=DB, autocommit=True)


def run() -> int:
    build_database()
    conn = new_conn()
    gate = Gate(conn)

    try:
        # ---- cast ---------------------------------------------------------

        editor = str(uuid.uuid4())
        second_editor = str(uuid.uuid4())
        extractor = str(uuid.uuid4())
        conn.execute("INSERT INTO pipeline_agent (id, kind, name) "
                     "VALUES (%s,'person','Principal editor')", (editor,))
        conn.execute("INSERT INTO pipeline_agent (id, kind, name) "
                     "VALUES (%s,'person','Second editor')", (second_editor,))
        conn.execute(
            "INSERT INTO pipeline_agent (id, kind, name, software_version, "
            "model_identifier) VALUES (%s,'software','extractor','0.1.0',"
            "'test/model-1')", (extractor,))

        source_id = str(uuid.uuid4())
        conn.execute(
            """INSERT INTO source (id, source_type, name, collection_method,
               default_retention_tier, default_access_tier, rights_permission)
               VALUES (%s,'government','Test source','http','permanent',
                       'public','may-preserve')""", (source_id,))
        holding_id = str(uuid.uuid4())
        conn.execute(
            """INSERT INTO holding (id, access_tier, retention_tier,
               completeness, rights_permission, ocfl_object_id)
               VALUES (%s,'public','permanent','original','may-preserve',
                       'urn:uiw:test-holding')""",
            (holding_id,))

        def proposition(text: str) -> str:
            pid = str(uuid.uuid4())
            conn.execute("INSERT INTO proposition (id, statement) "
                         "VALUES (%s,%s)", (pid, text))
            return pid

        # ---- AI-003: automation proposes, it does not assert ---------------

        proposal_id = gate.propose(
            agent_id=extractor, kind="extraction", review_tier="T2",
            holding_id=holding_id,
            content={"claim": "The instrument entered force on 2022-03-15"},
            feature_basis={"matched": ["entry into force", "2022-03-15"]},
            ai_provenance={"model": "test/model-1", "instructions": "extract"},
        )
        state = conn.execute("SELECT state::text FROM proposal WHERE id = %s",
                             (proposal_id,)).fetchone()[0]
        check("AI-003", "an extraction lands as a proposal, not as knowledge",
              state == "proposed")

        refuses("AI-003", "a person cannot 'propose' to themselves",
                lambda: gate.propose(
                    agent_id=editor, kind="extraction", review_tier="T3",
                    holding_id=holding_id, content={}, feature_basis={"x": 1}))

        refuses("DR-0063", "a proposal with no feature basis is refused",
                lambda: gate.propose(
                    agent_id=extractor, kind="extraction", review_tier="T3",
                    holding_id=holding_id, content={}, feature_basis={}))

        refuses("AI-002", "a consequential AI proposal needs AI provenance",
                lambda: gate.propose(
                    agent_id=extractor, kind="extraction", review_tier="T1",
                    holding_id=holding_id, content={},
                    feature_basis={"x": 1}))

        # ---- AI-001: only a person crosses the gate ------------------------

        refuses("AI-001", "software cannot accept its own proposal",
                lambda: gate.accept(
                    proposal_id=proposal_id, person_id=extractor,
                    tier_applied="T2", reasoning="looks right"))

        refuses("SPEC-0003 §7", "a decision without reasoning is refused",
                lambda: gate.accept(
                    proposal_id=proposal_id, person_id=editor,
                    tier_applied="T2", reasoning="   "))

        refuses("§78", "a reviewer cannot lower the tier below the proposal's",
                lambda: gate.accept(
                    proposal_id=proposal_id, person_id=editor,
                    tier_applied="T3", reasoning="routine enough"))

        gate.accept(proposal_id=proposal_id, person_id=editor,
                    tier_applied="T1",
                    reasoning="Raised to T1: names a designated entity. "
                              "Confirmed against the official journal text.")
        state = conn.execute("SELECT state::text FROM proposal WHERE id = %s",
                             (proposal_id,)).fetchone()[0]
        check("§78", "a reviewer may raise the tier", state == "confirmed")

        # ---- rejections are kept -------------------------------------------

        rejected_id = gate.propose(
            agent_id=extractor, kind="match", review_tier="T2",
            holding_id=holding_id, content={"match": "same person"},
            feature_basis={"name_similarity": 0.94},
            ai_provenance={"model": "test/model-1"})
        gate.reject(proposal_id=rejected_id, person_id=editor,
                    tier_applied="T2",
                    reasoning="Name similarity alone; no discriminating "
                              "evidence (DR-0063). Two distinct birth years.")
        kept = conn.execute(
            "SELECT reasoning FROM acceptance WHERE proposal_id = %s",
            (rejected_id,)).fetchone()
        check("SPEC-0003 §7", "a rejection is retained as a consultable record",
              kept is not None and "discriminating" in kept[0])

        # ---- adoption ------------------------------------------------------

        entry_prop = proposition("The instrument entered force on 2022-03-15")
        adopted = gate.adopt(
            proposal_id=proposal_id, asserter_id=editor,
            proposition_id=entry_prop, valid_time=WAR,
            epistemic_category="finding",
            reasoning="Adopted from the confirmed extraction.")
        check("AI-003", "a confirmed proposal can be adopted as a project assertion",
              adopted is not None)

        orphan = gate.propose(
            agent_id=extractor, kind="extraction", review_tier="T3",
            holding_id=holding_id, content={}, feature_basis={"x": 1})
        refuses("AI-001", "an unconfirmed proposal cannot become canonical",
                lambda: conn.execute(
                    """INSERT INTO project_assertion
                       (id, valid_time, asserter_id, epistemic_category,
                        proposition_id, adopted_from_id)
                       VALUES (%s, ROW('2022-02-24'::timestamptz,NULL,NULL,
                               NULL,NULL)::timespan, %s,'finding',%s,%s)""",
                    (str(uuid.uuid4()), extractor, entry_prop, orphan)))

        refuses("EVID-002", "the project cannot record a source's claim as its own",
                lambda: gate.assert_directly(
                    proposition_id=entry_prop, asserter_id=editor,
                    valid_time=WAR, epistemic_category="claim"))

        # ---- METH-0001 §6.2 / DR-0085 Q2: the confidence cap ---------------

        geo_prop = proposition("Image I depicts location L")
        capped = gate.assert_directly(
            proposition_id=geo_prop, asserter_id=editor, valid_time=WAR,
            epistemic_category="assessment", likelihood="very-likely",
            confidence="moderate",
            reasoning="Six matched features; reference imagery contemporaneous.")
        gate.record_critical_question(
            assertion_id=capped, scheme_id="scheme-geolocation",
            question_id="cq-distinctiveness",
            answer="Six features including a distinctive roofline; generic "
                   "treelines excluded.", answered_by=editor)
        gate.record_critical_question(
            assertion_id=capped, scheme_id="scheme-geolocation",
            question_id="cq-image-provenance",
            unanswered_defeater="undermining")

        check("DR-0034", "open critical questions are reported with their defeater",
              gate.open_questions(capped) ==
              [("scheme-geolocation", "cq-image-provenance", "undermining")])

        refuses("METH §6.2", "an open critical question blocks high confidence",
                lambda: conn.execute(
                    "UPDATE project_assertion SET confidence = 'high' "
                    "WHERE id = %s", (capped,)))

        # The cap must also catch the other write order: assert at `high`
        # first, then record the open question.
        def high_then_open():
            with new_conn() as c2:
                c2.autocommit = False
                g2 = Gate(c2)
                aid = g2.assert_directly(
                    proposition_id=geo_prop, asserter_id=editor,
                    valid_time=WAR, epistemic_category="assessment",
                    confidence="high", reasoning="strong match")
                g2.record_critical_question(
                    assertion_id=aid, scheme_id="scheme-geolocation",
                    question_id="cq-shadow-consistency",
                    unanswered_defeater="undercutting")
                c2.commit()

        refuses("METH §6.2", "the cap holds whichever is written first",
                high_then_open)

        # An argued dismissal is an answer; the cap lifts.
        def answer_then_high():
            with new_conn() as c3:
                c3.autocommit = False
                g3 = Gate(c3)
                aid = g3.assert_directly(
                    proposition_id=geo_prop, asserter_id=editor,
                    valid_time=WAR, epistemic_category="assessment",
                    confidence="high", reasoning="strong match")
                g3.record_critical_question(
                    assertion_id=aid, scheme_id="scheme-geolocation",
                    question_id="cq-shadow-consistency",
                    answer="Immaterial: the claim does not rest on solar "
                           "geometry.", answered_by=editor)
                c3.commit()
                return aid

        answered = answer_then_high()
        check("METH §6.2", "an argued dismissal counts as an answer, lifting the cap",
              answered is not None)

        # The case that matters most: someone notices months later that a
        # check was never done, against an assertion already committed at
        # `high`. The archive must never refuse to hear the objection in order
        # to protect the claim.
        late_prop = proposition("Vessel V called at port P in March 2024")
        standing = gate.assert_directly(
            proposition_id=late_prop, asserter_id=editor, valid_time=WAR,
            epistemic_category="assessment", likelihood="very-likely",
            confidence="high", reasoning="AIS track continuous throughout.")

        refuses("METH §6.2", "a late objection is refused while the claim stands high",
                lambda: gate.record_critical_question(
                    assertion_id=standing, scheme_id="scheme-sign-indicator",
                    question_id="cq-signal-spoofing",
                    unanswered_defeater="undermining"))

        successor, _ = gate.raise_late_critical_question(
            assertion_id=standing, scheme_id="scheme-sign-indicator",
            question_id="cq-signal-spoofing",
            unanswered_defeater="undermining", asserter_id=editor,
            reason="AIS spoofing in the Kerch Strait was not ruled out.")
        check("DR-0055", "a late objection is admitted with a superseding assertion",
              conn.execute(
                  "SELECT confidence::text, supersedes_id FROM project_assertion "
                  "WHERE id = %s", (successor,)).fetchone()
              == ("moderate", uuid.UUID(standing)))
        check("EVID-015", "the superseded assertion keeps the confidence it had",
              conn.execute("SELECT confidence::text FROM project_assertion "
                           "WHERE id = %s", (standing,)).fetchone()[0] == "high")
        check("METH §6.2", "the objection is recorded against the live assertion",
              gate.open_questions(successor) ==
              [("scheme-sign-indicator", "cq-signal-spoofing", "undermining")])

        # ---- METH-0001 §7 / DR-0085 Q3: hypothesis sets --------------------

        strike_prop = proposition("Unit U conducted the strike on 2023-05-01")
        alternative = proposition("Unit V conducted the strike on 2023-05-01")

        def consequential_without_hypotheses():
            with new_conn() as c4:
                c4.autocommit = False
                Gate(c4).assert_directly(
                    proposition_id=strike_prop, asserter_id=editor,
                    valid_time=WAR, epistemic_category="project-conclusion",
                    consequence_limb="names-identifiable-party",
                    reasoning="Unit insignia visible in three captures.")
                c4.commit()

        refuses("METH §7", "a consequential conclusion needs a hypothesis set",
                consequential_without_hypotheses)

        refuses("DR-0035", "a hypothesis set of one is refused",
                lambda: gate.open_hypothesis_set(
                    question="Which unit conducted the strike?",
                    opened_by=editor, trigger="consequential",
                    hypotheses=[(strike_prop, False)]))

        refuses("METH §7", "a set with no genuine alternative is refused",
                lambda: gate.open_hypothesis_set(
                    question="Which unit conducted the strike?",
                    opened_by=editor, trigger="consequential",
                    hypotheses=[(strike_prop, False), (alternative, False)]))

        set_id = gate.open_hypothesis_set(
            question="Which unit conducted the strike on 2023-05-01?",
            opened_by=editor, trigger="strong-prior",
            hypotheses=[(strike_prop, False), (alternative, True)])
        check("METH §7", "strong prior expectation is a valid trigger",
              conn.execute("SELECT trigger FROM hypothesis_set WHERE id = %s",
                           (set_id,)).fetchone()[0] == "strong-prior")

        with new_conn() as c5:
            c5.autocommit = False
            g5 = Gate(c5)
            conclusion = g5.assert_directly(
                proposition_id=strike_prop, asserter_id=editor,
                valid_time=WAR, epistemic_category="project-conclusion",
                consequence_limb="names-identifiable-party",
                likelihood="likely", confidence="moderate",
                reasoning="Unit insignia in three independent captures.")
            g5.link_hypothesis_set(assertion_id=conclusion, set_id=set_id)
            c5.commit()
        check("METH §7", "a consequential conclusion with a set is accepted",
              conclusion is not None)

        # ---- discriminating evidence is the object of the exercise ---------

        er_id = str(uuid.uuid4())
        conn.execute(
            """INSERT INTO evidence_relation
               (id, valid_time, asserter_id, epistemic_category,
                proposition_id, holding_id, relation, reasoning)
               VALUES (%s, ROW('2022-02-24'::timestamptz,NULL,NULL,NULL,
                       NULL)::timespan, %s,'observation',%s,%s,
                       'discriminates','Insignia visible only on U vehicles')""",
            (er_id, editor, strike_prop, holding_id))
        check("DR-0035", "discriminating evidence is queryable, not a spreadsheet",
              gate.discriminating_evidence(set_id) == [er_id])

        # ---- METH-0001 §10.1 / DR-0085 Q4: review qualification ------------

        qualification = gate.publication_qualification(conclusion)
        check("METH §10.1", "an unreviewed conclusion carries a visible qualification",
              qualification is not None and "Unreviewed" in qualification)

        refuses("§83", "the asserter cannot review their own conclusion",
                lambda: gate.record_review(
                    assertion_id=conclusion, tier_required="T1",
                    state="independent", reviewed_by=editor))

        gate.record_review(assertion_id=conclusion, tier_required="T1",
                           state="unreviewed",
                           notes="Single-editor project; no second party available.")
        check("METH §10.1", "`unreviewed` is a recordable, legitimate state",
              "Unreviewed at tier T1" in gate.publication_qualification(conclusion))

        gate.record_review(assertion_id=conclusion, tier_required="T1",
                           state="independent", reviewed_by=second_editor,
                           notes="Evidence examined before seeing the conclusion.")
        check("METH §10.3", "independent reassessment replaces the qualification",
              gate.publication_qualification(conclusion) == "Independently reassessed.")

        non_consequential = gate.assert_directly(
            proposition_id=entry_prop, asserter_id=editor, valid_time=WAR,
            epistemic_category="finding", reasoning="Routine date extraction.")
        check("METH §10.1", "a non-consequential finding carries no qualification",
              gate.publication_qualification(non_consequential) is None)

        # ---- DR-0032/0033/0036: arguments and defeaters --------------------

        argument_id = gate.record_argument(
            assertion_id=conclusion, scheme_id="scheme-geolocation",
            warrant="Unit-specific insignia identifies the operating unit.",
            made_by=editor,
            premises=[{"evidence_relation_id": er_id},
                      {"assumption": "Insignia were not spoofed."}])
        check("DR-0037", "the warrant is recorded, not left implicit",
              conn.execute("SELECT warrant FROM argument WHERE id = %s",
                           (argument_id,)).fetchone()[0].startswith("Unit-specific"))
        check("DR-0032", "an unattacked assumption is visible as a premise",
              conn.execute("SELECT count(*) FROM argument_premise WHERE "
                           "argument_id = %s AND assumption IS NOT NULL",
                           (argument_id,)).fetchone()[0] == 1)

        refuses("DR-0036", "software cannot make an inference record",
                lambda: gate.record_argument(
                    assertion_id=conclusion, warrant="computed",
                    made_by=extractor))

        defeater_id = gate.raise_defeater(
            argument_id=argument_id, kind="undermining",
            statement="The capture showing the insignia may be a re-upload "
                      "of a 2022 image.", raised_by=second_editor)
        contested = gate.contested()
        check("§40", "a live objection leaves the conclusion visibly contested",
              len(contested) == 1 and contested[0][1] == 1
              and "undermining" in contested[0][2])

        check("DR-0036", "nothing in the schema adjudicates the outcome",
              conn.execute(
                  "SELECT count(*) FROM information_schema.columns WHERE "
                  "table_name = 'argument' AND column_name IN "
                  "('status','acceptability','resolved')").fetchone()[0] == 0)

        gate.answer_defeater(
            defeater_id=defeater_id,
            answer="Earliest known appearance is 2023-05-01; reverse search "
                   "returns no earlier copy.", answered_by=editor)
        check("DR-0033", "an answered defeater clears the contested list",
              gate.contested() == [])

        # ---- the queue is ordering, never acceptance -----------------------

        gate.propose(agent_id=extractor, kind="extraction", review_tier="T1",
                     holding_id=holding_id, content={"a": 1},
                     feature_basis={"x": 1},
                     ai_provenance={"model": "test/model-1"})
        queued = gate.queue()
        check("SPEC-0003 §7", "the queue orders by tier, highest scrutiny first",
              [p.review_tier for p in queued] == sorted(p.review_tier for p in queued))
        check("DR-0027", "queued proposals are still uncrossed at Gate 2",
              all(p.state in ("proposed", "under-review") for p in queued))
        check("OPS-006", "queue depth is reported per tier",
              sum(gate.queue_depth().values()) == len(queued))

        # ---- append-only holds here too ------------------------------------

        refuses("DR-0055", "an acceptance cannot be edited after the fact",
                lambda: conn.execute(
                    "UPDATE acceptance SET reasoning = 'changed my mind'"))
        refuses("DR-0055", "a project assertion cannot be deleted",
                lambda: conn.execute(
                    "DELETE FROM project_assertion WHERE id = %s", (adopted,)))

    finally:
        conn.close()

    for line in PASSES:
        print(line)
    for line in FAILURES:
        print(line)
    print(f"\n{len(PASSES)} passed, {len(FAILURES)} failed")
    return 1 if FAILURES else 0


def main() -> int:
    try:
        return run()
    except Exception as exc:  # noqa: BLE001
        import traceback
        traceback.print_exc()
        print(f"\nSUITE ERRORED — {type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
