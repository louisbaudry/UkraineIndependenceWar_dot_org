#!/usr/bin/env python3
"""Tests for Gate 3 — the publication decision.

The rules that matter here are the ones whose failure reaches the outside
world: that nothing published skipped a gate, that a page never renders
material above its tier, that a consequential conclusion carries the review
qualification a reader must see, and that a published statement can be
reproduced from what the record kept.

The last of those is EDIT-005's demonstration, run here rather than asserted.

Run:  PGHOST=… PGPORT=… PGUSER=… python3 publication/tests/test_gate3.py
"""

from __future__ import annotations

import datetime as dt
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
for sub in ("editorial", "publication", "export"):
    sys.path.insert(0, str(ROOT / sub))

import psycopg  # noqa: E402

from gate2 import Gate  # noqa: E402
from gate3 import (  # noqa: E402
    PUBLICATION_TIERS,
    PublicationError,
    Publisher,
    Versions,
    digest,
)
from tiers import (  # noqa: E402
    DISCLOSURE_TIERS,
    RESTRICTIVENESS,
    most_restrictive,
)

PASSES: list[str] = []
FAILURES: list[str] = []
DB = "uiw_gate3_test"
WAR = ("2022-02-24", None, None, None, None)
V = Versions(methodology="1.0", terminology="registry:0.1.1",
             template="site-0.1.0", release_baseline="2026.1")


def check(req: str, what: str, condition: bool) -> None:
    (PASSES if condition else FAILURES).append(
        f"{'PASS' if condition else 'FAIL'}  {req} — {what}")


def refuses(req: str, what: str, fn) -> None:
    try:
        fn()
    except (psycopg.Error, PublicationError):
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
    gate, pub = Gate(conn), Publisher(conn)

    try:
        # ---- cast ---------------------------------------------------------

        editor, reviewer = str(uuid.uuid4()), str(uuid.uuid4())
        robot = str(uuid.uuid4())
        conn.execute("INSERT INTO pipeline_agent (id, kind, name) "
                     "VALUES (%s,'person','Principal editor')", (editor,))
        conn.execute("INSERT INTO pipeline_agent (id, kind, name) "
                     "VALUES (%s,'person','Reviewer')", (reviewer,))
        conn.execute("INSERT INTO pipeline_agent (id, kind, name, "
                     "software_version) VALUES (%s,'software','renderer',"
                     "'0.1.0')", (robot,))

        def holding(tier: str) -> str:
            hid = str(uuid.uuid4())
            conn.execute(
                """INSERT INTO holding (id, access_tier, retention_tier,
                   completeness, rights_permission, ocfl_object_id)
                   VALUES (%s,%s,'permanent','original','may-display',%s)""",
                (hid, tier, f"urn:uiw:{hid}"))
            return hid

        def proposition(text: str) -> str:
            pid = str(uuid.uuid4())
            conn.execute("INSERT INTO proposition (id, statement) "
                         "VALUES (%s,%s)", (pid, text))
            return pid

        public_holding = holding("public")
        internal_holding = holding("internal")

        routine = gate.assert_directly(
            proposition_id=proposition("The decree was published 2022-03-01"),
            asserter_id=editor, valid_time=WAR, epistemic_category="finding",
            reasoning="Date read from the official journal.")

        # ---- SEC-003: dimensions stay apart --------------------------------

        check("SEC-003", "no boolean is_public exists anywhere in the schema",
              conn.execute(
                  "SELECT count(*) FROM information_schema.columns "
                  "WHERE column_name IN ('is_public','public','published') "
                  "AND data_type = 'boolean'").fetchone()[0] == 0)

        decision = pub.decide(
            person_id=editor, assertion_id=routine, access_tier="public",
            rights_basis="Project text under CC-BY-4.0",
            sensitivity="none", evidentiary_disclosure="citable",
            rationale="Routine documentary date; no personal data.")
        dims = conn.execute(
            "SELECT access_tier::text, sensitivity, rights_basis, "
            "evidentiary_disclosure FROM publication_decision WHERE id = %s",
            (decision,)).fetchone()
        check("SEC-003", "the four §12 dimensions are recorded separately",
              all(d is not None for d in dims))

        refuses("SEC-001", "`confidential` is not a publication target",
                lambda: pub.decide(
                    person_id=editor, assertion_id=routine,
                    access_tier="confidential", rights_basis="x",
                    rationale="x"))
        refuses("§12", "`private-preservation` is not a publication target",
                lambda: pub.decide(
                    person_id=editor, assertion_id=routine,
                    access_tier="private-preservation", rights_basis="x",
                    rationale="x"))
        refuses("§79", "software cannot make a publication decision",
                lambda: pub.decide(
                    person_id=robot, assertion_id=routine,
                    access_tier="public", rights_basis="x", rationale="x"))
        refuses("Gate 3", "a decision without a rationale is refused",
                lambda: pub.decide(
                    person_id=editor, assertion_id=routine,
                    access_tier="public", rights_basis="x", rationale="  "))

        # ---- OPS-001: no path to a surface without both gates --------------

        page = pub.create_page(path="/decrees/2022-03-01", language="en")
        first = pub.publish(
            page_id=page, person_id=editor,
            rendered_text="The decree was published on 1 March 2022.",
            versions=V, assertions=[routine], holdings=[public_holding])
        check("OPS-004", "a page's history begins at its first publication",
              pub.history("/decrees/2022-03-01")[0][:2] == (1, "initial"))

        undecided = gate.assert_directly(
            proposition_id=proposition("An unpublished finding"),
            asserter_id=editor, valid_time=WAR, epistemic_category="finding",
            reasoning="Not yet through Gate 3.")
        orphan_page = pub.create_page(path="/orphan", language="en")
        refuses("OPS-001", "content with no Gate 3 decision cannot be rendered",
                lambda: pub.publish(
                    page_id=orphan_page, person_id=editor,
                    rendered_text="Something we never decided to publish.",
                    versions=V, assertions=[undecided]))

        # ---- SEC-004: no tier leak ------------------------------------------

        leak_page = pub.create_page(path="/leak", language="en")
        refuses("SEC-004", "a public page cannot render an internal holding",
                lambda: pub.publish(
                    page_id=leak_page, person_id=editor,
                    rendered_text="With a source we may not show.",
                    versions=V, assertions=[routine],
                    holdings=[internal_holding]))

        subscriber_only = gate.assert_directly(
            proposition_id=proposition("A subscriber-tier finding"),
            asserter_id=editor, valid_time=WAR, epistemic_category="finding",
            reasoning="Behind the subscriber line.")
        pub.decide(person_id=editor, assertion_id=subscriber_only,
                   access_tier="subscriber", rights_basis="Project text",
                   rationale="Subscriber analysis.")
        mixed_page = pub.create_page(path="/mixed", language="en")
        mixed = pub.publish(
            page_id=mixed_page, person_id=editor,
            rendered_text="Public and subscriber material together.",
            versions=V, assertions=[routine, subscriber_only],
            holdings=[public_holding])
        check("SEC-004", "a page is only as open as its most restricted content",
              mixed is not None)

        check("§12", "publication tiers agree with the export tier policy",
              {t: v for t, v in PUBLICATION_TIERS.items()} == DISCLOSURE_TIERS)
        agreed = conn.execute(
            "SELECT tier_admits('public','internal'), "
            "       tier_admits('subscriber','public'), "
            "       tier_admits('confidential','public')").fetchone()
        check("§12", "the schema's tier_admits agrees with the Python policy",
              agreed == (False, True, False))

        # Resolving several tiers must not be read off any ordering the
        # database supplies. Both the enum order and alphabetical order put
        # `public` before `subscriber`, so a min() would return `public` for
        # this pair — the *less* restrictive one, which is how a
        # subscriber-only holding ends up in a public dump.
        check("SEC-004", "{public, subscriber} resolves to subscriber, not public",
              conn.execute(
                  "SELECT most_restrictive_tier(ARRAY['public','subscriber']"
                  "::access_tiers[])::text").fetchone()[0] == "subscriber")
        check("SEC-004", "two lateral grants escalate rather than picking one",
              conn.execute(
                  "SELECT most_restrictive_tier(ARRAY['researcher-restricted',"
                  "'investigator-restricted']::access_tiers[])::text"
              ).fetchone()[0] == "internal")
        check("§12", "an unclassified set resolves to confidential, not public",
              conn.execute(
                  "SELECT most_restrictive_tier(ARRAY[]::access_tiers[])::text"
              ).fetchone()[0] == "confidential")
        check("§12", "SQL and Python rank restrictiveness identically",
              all(conn.execute(
                      "SELECT tier_restrictiveness(%s::access_tiers)", (t,)
                  ).fetchone()[0] == rank
                  for t, rank in RESTRICTIVENESS.items()))
        check("SEC-004", "Python resolution agrees with the schema's",
              most_restrictive(["public", "subscriber"]) == "subscriber"
              and most_restrictive(["researcher-restricted",
                                    "investigator-restricted"]) == "internal"
              and most_restrictive([]) == "confidential")

        # ---- METH-0001 §10.1: the reader is told ---------------------------

        strike = proposition("Unit U conducted the strike on 2023-05-01")
        alternative = proposition("Unit V conducted the strike on 2023-05-01")
        hset = gate.open_hypothesis_set(
            question="Which unit conducted the strike?", opened_by=editor,
            trigger="consequential",
            hypotheses=[(strike, False), (alternative, True)])

        with new_conn() as c2:
            c2.autocommit = False
            g2 = Gate(c2)
            consequential = g2.assert_directly(
                proposition_id=strike, asserter_id=editor, valid_time=WAR,
                epistemic_category="project-conclusion",
                consequence_limb="names-identifiable-party",
                likelihood="likely", confidence="moderate",
                reasoning="Insignia in three captures.")
            g2.link_hypothesis_set(assertion_id=consequential, set_id=hset)
            c2.commit()

        pub.decide(person_id=editor, assertion_id=consequential,
                   access_tier="public", rights_basis="Project text",
                   rationale="Public-interest attribution; POL-0001 reviewed.")

        needed = pub.required_qualification([consequential])
        check("METH §10.1", "the required qualification is discoverable before publishing",
              needed is not None and "Unreviewed" in needed)

        attribution = pub.create_page(path="/strikes/2023-05-01", language="en")
        refuses("METH §10.1",
                "a consequential conclusion cannot publish without the qualification",
                lambda: pub.publish(
                    page_id=attribution, person_id=editor,
                    rendered_text="Unit U likely conducted the strike.",
                    versions=V, assertions=[consequential]))

        attribution_rev = pub.publish(
            page_id=attribution, person_id=editor,
            rendered_text="Unit U likely conducted the strike of 1 May 2023.",
            versions=V, assertions=[consequential],
            review_qualification=needed)
        check("METH §10.1", "with the qualification, publication proceeds",
              attribution_rev is not None)
        check("DR-0085 Q4", "a reader is told what review the conclusion received",
              "Unreviewed" in conn.execute(
                  "SELECT review_qualification FROM page_revision WHERE id = %s",
                  (attribution_rev,)).fetchone()[0])

        check("METH §10.1", "a routine finding needs no qualification",
              pub.required_qualification([routine]) is None)

        # ---- §62: no legal findings ----------------------------------------

        legal_page = pub.create_page(path="/legal", language="en")
        for phrase in ("Unit U is guilty of the attack.",
                       "The commander was found guilty.",
                       "This constitutes a war crime."):
            refuses("§62", f"published text cannot assert {phrase.split()[-1]!r}",
                    lambda p=phrase: pub.publish(
                        page_id=legal_page, person_id=editor,
                        rendered_text=p, versions=V, assertions=[routine]))

        reported = pub.publish(
            page_id=legal_page, person_id=editor,
            rendered_text="The ICC prosecutor alleges the commander bears "
                          "responsibility; no judgment has been entered.",
            versions=V, assertions=[routine])
        check("§62", "reporting what an authority alleges is permitted",
              reported is not None)

        # ---- §77: corrections and retractions leave a trace ----------------

        refuses("§77", "a correction must say what it changes",
                lambda: pub.publish(
                    page_id=page, person_id=editor,
                    rendered_text="Corrected text.", versions=V,
                    assertions=[routine], kind="correction"))

        corrected = pub.publish(
            page_id=page, person_id=editor,
            rendered_text="The decree was published on 2 March 2022.",
            versions=V, assertions=[routine], kind="correction",
            change_note="Date corrected from 1 to 2 March: the earlier "
                        "reading came from the signature line, not the "
                        "publication line.")
        history = pub.history("/decrees/2022-03-01")
        check("§77", "a correction is a new revision, not an overwrite",
              len(history) == 2 and history[1][1] == "correction")
        check("EDIT-002", "the corrected revision still exists in the history",
              history[0][1] == "initial")
        check("§77", "the correction records what changed and why",
              "signature line" in history[1][3])

        refuses("DR-0055", "a published revision cannot be edited",
                lambda: conn.execute(
                    "UPDATE page_revision SET rendered_text = 'rewritten'"))

        retraction_page = pub.create_page(path="/retracted", language="en")
        pub.publish(page_id=retraction_page, person_id=editor,
                    rendered_text="An initial claim.", versions=V,
                    assertions=[routine])
        pub.publish(page_id=retraction_page, person_id=editor,
                    rendered_text="This conclusion is withdrawn. The evidence "
                                  "line proved dependent, not independent.",
                    versions=V, assertions=[routine], kind="retraction",
                    change_note="Retracted: corroboration was a repetition "
                                "count (DR-0028).")
        check("§77", "a retraction is recorded as such and keeps the original",
              [r[1] for r in pub.history("/retracted")] == ["initial", "retraction"])

        # ---- §86: reproducibility -------------------------------------------

        reproduced = pub.reproduce(path="/strikes/2023-05-01", revision=1)
        check("§86", "a published statement reproduces its exact text",
              reproduced["rendered_text"].startswith("Unit U likely"))
        check("§86", "the rendered text verifies against its recorded digest",
              reproduced["digest_verifies"])
        check("§86", "the statement pins its methodology and terminology versions",
              reproduced["methodology_version"] == "1.0"
              and reproduced["terminology_version"] == "registry:0.1.1")
        check("EDIT-005", "the statement names the baseline it was built from",
              reproduced["release_baseline"] == "2026.1")
        check("§86", "the statement names the assertions it rendered",
              reproduced["assertions"] == [consequential])

        tampered = digest(reproduced["rendered_text"] + " ")
        check("DR-0005", "a changed text would not match the recorded digest",
              tampered != reproduced["text_digest"])

        # ---- §90: what did the site say on date D --------------------------

        as_of = pub.site_as_of(dt.datetime.now(dt.timezone.utc))
        paths = {row[0]: row[2] for row in as_of}
        check("§90", "the site as of now shows each page's latest revision",
              paths["/decrees/2022-03-01"] == 2)
        check("§90", "every published page appears in the site history",
              {"/decrees/2022-03-01", "/strikes/2023-05-01",
               "/retracted"} <= set(paths))

        earlier = conn.execute(
            "SELECT published_at FROM page_revision WHERE page_id = %s "
            "AND revision = 1", (page,)).fetchone()[0]
        before = {row[0]: row[2] for row in pub.site_as_of(earlier)}
        check("§90", "the site as of an earlier moment shows the earlier revision",
              before["/decrees/2022-03-01"] == 1
              and "/retracted" not in before)

        # ---- I18N-001: translations are separate, derived pages ------------

        ukrainian = pub.create_page(path="/uk/strikes/2023-05-01",
                                    language="uk", translation_of=attribution)
        pub.publish(page_id=ukrainian, person_id=editor,
                    rendered_text="Ймовірно, удар 1 травня 2023 року завдало "
                                  "з'єднання U.",
                    versions=V, assertions=[consequential],
                    review_qualification=needed)
        check("I18N-001", "a translation is its own page with its own history",
              conn.execute(
                  "SELECT language, translation_of FROM published_page "
                  "WHERE path = %s", ("/uk/strikes/2023-05-01",)).fetchone()
              == ("uk", uuid.UUID(attribution)))
        check("§61", "each language carries its own rendered text",
              len({r["rendered_text"] for r in (
                  pub.reproduce(path="/strikes/2023-05-01", revision=1),
                  pub.reproduce(path="/uk/strikes/2023-05-01", revision=1))}) == 2)

        # ---- withdrawal ------------------------------------------------------

        pub.withdraw(decision_id=decision,
                     ground="Superseded by a corrected reading of the journal.")
        still_there = conn.execute(
            "SELECT withdrawal_ground FROM publication_decision WHERE id = %s",
            (decision,)).fetchone()
        check("§77", "a withdrawn decision keeps its row and its ground",
              still_there[0].startswith("Superseded"))
        check("§90", "withdrawal does not erase what was published",
              len(pub.history("/decrees/2022-03-01")) == 2)

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
