#!/usr/bin/env python3
"""Tests for public identifiers and resolution — SPEC-0007 §10.

The checks that matter here are the ones whose failure reaches a reader:
that a citation published today still answers in thirty years, that it
answers *correctly* about what happened to the thing it names, and that the
answer does not leak what the project chose not to publish.

DATA-009 is the spine: no minted identifier ever dead-ends. It is checked
here over the whole register rather than on examples, because a rule with an
exception nobody noticed is not a guarantee.

Run:  PGHOST=… PGPORT=… PGUSER=… python3 identifiers/tests/test_identifiers.py
"""

from __future__ import annotations

import json
import os
import random
import re
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
for sub in ("identifiers", "publication", "editorial", "export"):
    sys.path.insert(0, str(ROOT / sub))

import psycopg  # noqa: E402

import ark as ark_mod  # noqa: E402
from dump import create_dump  # noqa: E402
from gate2 import Gate  # noqa: E402
from gate3 import Publisher, Versions  # noqa: E402
from register import (  # noqa: E402
    PROJECT_AGENT_NAME,
    MintError,
    Register,
    from_registry,
)
from resolver import Resolver  # noqa: E402

PASSES: list[str] = []
FAILURES: list[str] = []
DB = "uiw_identifiers_test"
WAR = ("2022-02-24", None, None, None, None)
V = Versions(methodology="1.0", terminology="registry:0.2.0",
             template="site-0.1.0", release_baseline="2026.1")
UUID_RE = re.compile(
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)


def check(req: str, what: str, condition: bool) -> None:
    (PASSES if condition else FAILURES).append(
        f"{'PASS' if condition else 'FAIL'}  {req} — {what}")


def refuses(req: str, what: str, fn) -> None:
    try:
        fn()
    except (psycopg.Error, MintError, ValueError):
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


def run() -> int:  # noqa: C901 — one linear scenario, read top to bottom
    # ---- syntax, before any database ------------------------------------

    naan, shoulder = "99999", "t1"

    substitutions = transpositions = 0
    caught_sub = caught_trans = 0
    rng = random.Random(20260909)
    for _ in range(10_000):
        name = ark_mod.mint_name(naan, shoulder)
        position = rng.randrange(len(name))
        replacement = rng.choice(
            [c for c in ark_mod.BETANUMERIC if c != name[position]])
        mutated = name[:position] + replacement + name[position + 1:]
        substitutions += 1
        caught_sub += not ark_mod.is_valid(ark_mod.format_ark(naan, mutated))

        cut = rng.randrange(len(name) - 1)
        if name[cut] != name[cut + 1]:
            swapped = (name[:cut] + name[cut + 1] + name[cut]
                       + name[cut + 2:])
            transpositions += 1
            caught_trans += not ark_mod.is_valid(
                ark_mod.format_ark(naan, swapped))

    check("SPEC-0007 §2.3",
          f"the check character catches every single-character substitution "
          f"({caught_sub}/{substitutions})", caught_sub == substitutions)
    check("SPEC-0007 §2.3",
          f"the check character catches every adjacent transposition "
          f"({caught_trans}/{transpositions})", caught_trans == transpositions)

    name = ark_mod.mint_name(naan, shoulder)
    canonical = ark_mod.format_ark(naan, name)
    hyphenated = f"ark:/{naan}/{name[:4]}-{name[4:]}"
    hosted = f"https://ukraineindependencewar.org/ark:/{naan.upper()}/{name}?info"
    check("SPEC-0007 §2.4",
          "hyphenated, hosted and upper-cased forms normalise to one key",
          {ark_mod.normalise(x) for x in (canonical, hyphenated, hosted)}
          == {canonical})
    check("SPEC-0007 §2.1", "names carry no vowels and no 'l'",
          not (set(name) & set("aeioul")))
    check("SPEC-0007 §2.1", "names are drawn from the shoulder",
          name.startswith(shoulder))
    check("DR-0087", "two mints never collide in 5,000 draws",
          len({ark_mod.mint_name(naan, shoulder) for _ in range(5000)}) == 5000)

    # ---- the register ----------------------------------------------------

    build_database()
    conn = psycopg.connect(dbname=DB, autocommit=True)

    try:
        editor = str(uuid.uuid4())
        conn.execute("INSERT INTO pipeline_agent (id, kind, name) "
                     "VALUES (%s,'person','Principal editor')", (editor,))

        # Prerequisite 5: the project's own agent (SPEC-0007 §11).
        refuses("SPEC-0007 §11",
                "minting without the project's own agent is refused",
                lambda: Register(conn, naan=naan, shoulder=shoulder).mint(
                    subject_table="world_actor",
                    subject_id=str(uuid.uuid4())))

        project = str(uuid.uuid4())
        conn.execute("INSERT INTO pipeline_agent (id, kind, name) "
                     "VALUES (%s,'organization',%s)",
                     (project, PROJECT_AGENT_NAME))

        register = Register(conn, naan=naan, shoulder=shoulder)
        resolver = Resolver(register,
                            base_url="https://ukraineindependencewar.org")

        check("SPEC-0007 §11",
              "no NAAN is recorded, so production minting is impossible",
              from_registry(conn) is None)
        check("SPEC-0007 §11",
              "the suite mints under the shared test NAAN instead",
              from_registry(conn, allow_test_naan=True).naan == "99999")

        def actor() -> str:
            row_id = str(uuid.uuid4())
            conn.execute("INSERT INTO world_actor (id, kind, status) "
                         "VALUES (%s,'person','canonical')", (row_id,))
            return row_id

        subject = actor()
        first = register.mint(subject_table="world_actor", subject_id=subject)

        check("DR-0088", "a mint records an identifier-assignment assertion",
              conn.execute(
                  "SELECT count(*) FROM identifier_assignment "
                  "WHERE identifier_type = 'uiw-ark' AND value = %s",
                  (first,)).fetchone()[0] == 1)
        check("DR-0088", "the project asserts its own identifiers",
              conn.execute(
                  "SELECT asserter_id FROM identifier_assignment "
                  "WHERE value = %s", (first,)).fetchone()[0]
              == uuid.UUID(project))
        check("DR-0088", "minting is idempotent — one object, one identifier",
              register.mint(subject_table="world_actor",
                            subject_id=subject) == first)
        check("record §15",
              "an internal-only class cannot carry a public identifier",
              not conn.execute(
                  "SELECT 1 FROM citable_class WHERE subject_table IN "
                  "('pipeline_agent','quarantine_item','proposal',"
                  "'acceptance','collector_run','review_record')").fetchall())
        refuses("record §15", "minting for a non-citable class is refused",
                lambda: register.mint(subject_table="quarantine_item",
                                      subject_id=str(uuid.uuid4())))
        refuses("SPEC-0007 §4.2",
                "an assignment whose subject does not exist is refused",
                lambda: register.mint(subject_table="world_actor",
                                      subject_id=str(uuid.uuid4())))

        # ---- dispositions ------------------------------------------------

        merged_away, survivor = (
            register.mint(subject_table="world_actor", subject_id=actor()),
            register.mint(subject_table="world_actor", subject_id=actor()))
        register.redirect(ark=merged_away, successor_ark=survivor,
                          basis=str(uuid.uuid4()))

        split_source = register.mint(subject_table="world_actor",
                                     subject_id=actor())
        left = register.mint(subject_table="world_actor", subject_id=actor())
        right = register.mint(subject_table="world_actor", subject_id=actor())
        register.split(
            ark=split_source, successors=[left, right], decided_by=editor,
            grounds="Two officials of the same name conflated at import.")

        redacted = register.mint(subject_table="world_actor",
                                 subject_id=actor())
        register.tombstone(ark=redacted, basis=str(uuid.uuid4()))

        withheld = register.mint(subject_table="world_actor",
                                 subject_id=actor())
        register.restrict(ark=withheld, basis=str(uuid.uuid4()))

        check("DR-0089", "every disposition is represented in the register",
              {r["disposition"] for r in register.health()}
              == {"active", "redirect", "disambiguation", "tombstone",
                  "restricted"})

        refuses("DR-0089", "a disposition change without a basis is refused",
                lambda: conn.execute(
                    "UPDATE public_identifier SET disposition = 'tombstone' "
                    "WHERE ark = %s", (first,)))
        refuses("DR-0089", "a redirect is terminal",
                lambda: register.tombstone(ark=merged_away,
                                           basis=str(uuid.uuid4())))
        refuses("DR-0089", "a disambiguation is terminal",
                lambda: register.restrict(ark=split_source,
                                          basis=str(uuid.uuid4())))
        refuses("DR-0089", "a tombstone returns only to active",
                lambda: register.restrict(ark=redacted,
                                          basis=str(uuid.uuid4())))
        refuses("DR-0089", "an identifier's identity columns never change",
                lambda: conn.execute(
                    "UPDATE public_identifier SET minted_at = now() "
                    "WHERE ark = %s", (first,)))
        refuses("DATA-009", "a minted identifier is never deleted",
                lambda: conn.execute(
                    "DELETE FROM public_identifier WHERE ark = %s", (first,)))
        refuses("DATA-009", "its subject mapping is never deleted either",
                lambda: conn.execute(
                    "DELETE FROM public_identifier_subject WHERE ark = %s",
                    (first,)))
        refuses("DR-0089", "a redirect cycle is refused",
                lambda: register.redirect(ark=survivor,
                                          successor_ark=merged_away,
                                          basis=str(uuid.uuid4())))

        # A restriction lifts; a redaction reversal is a recorded decision.
        register.reinstate(ark=withheld, basis=str(uuid.uuid4()))
        check("DR-0089", "a lowered tier returns an identifier to active",
              register.resolve(withheld)["disposition"] == "active")
        register.restrict(ark=withheld, basis=str(uuid.uuid4()))

        # ---- negative control: is the guard doing the work? ---------------
        #
        # A test that has never been seen to fail proves nothing. Drop the
        # delete guard on a second connection, confirm the delete then
        # succeeds, and roll the whole thing back.
        control = psycopg.connect(dbname=DB)
        try:
            control.execute(
                "DROP TRIGGER public_identifier_subject_never_deleted "
                "ON public_identifier_subject")
            control.execute(
                "DELETE FROM public_identifier_subject WHERE ark = %s",
                (first,))
            deleted = control.execute(
                "SELECT count(*) FROM public_identifier_subject "
                "WHERE ark = %s", (first,)).fetchone()[0] == 0
        finally:
            control.rollback()
            control.close()
        check("DATA-009",
              "the deletion guard is what prevents deletion, not chance",
              deleted)
        check("DATA-009", "and the rollback left the register intact",
              conn.execute("SELECT count(*) FROM public_identifier_subject "
                           "WHERE ark = %s", (first,)).fetchone()[0] == 1)

        # ---- resolution ---------------------------------------------------

        every = register.health()
        answers = {r["ark"]: resolver.get(r["ark"]) for r in every}
        check("DATA-009", "no minted identifier returns 404",
              all(a.status != 404 for a in answers.values()))
        check("DATA-009", "every answer matches its recorded disposition",
              all(answers[r["ark"]].status
                  == {"active": 200, "redirect": 301, "disambiguation": 200,
                      "tombstone": 410, "restricted": 403}[r["disposition"]]
                  for r in every))
        check("SPEC-0007 §6.1",
              "an identifier that was never issued is the only 404",
              resolver.get(ark_mod.format_ark(
                  naan, ark_mod.mint_name(naan, shoulder))).status == 404)
        check("SPEC-0007 §2.3", "a mistyped citation is a 400, not a 404",
              resolver.get(f"ark:/{naan}/{'t1bcdfghj'}").status == 400)
        check("DR-0064", "a merged identifier redirects to its successor",
              answers[merged_away].headers["Location"].endswith(survivor))
        check("DR-0064", "a split identifier names its successors",
              left in answers[split_source].body
              and right in answers[split_source].body)
        check("DR-0064", "and gives the split's date and grounds",
              "conflated at import" in answers[split_source].body
              and "Split on 20" in answers[split_source].body)
        check("DR-0077", "a tombstone says removal happened, not what was there",
              "Removed under governed redaction" in answers[redacted].body)
        check("DR-0086", "a restricted identifier says the object exists",
              "exists" in answers[withheld].body
              and "withheld" in answers[withheld].body)

        # ---- ?info --------------------------------------------------------

        for target, disposition in ((first, "active"),
                                    (merged_away, "redirect"),
                                    (split_source, "disambiguation"),
                                    (redacted, "tombstone"),
                                    (withheld, "restricted")):
            info = resolver.get(target, inflection="?info")
            check("SPEC-0007 §6.2",
                  f"?info answers 200 for a {disposition} identifier",
                  info.status == 200
                  and info.body.startswith("erc:")
                  and f"disposition: {disposition}" in info.body
                  and info.body.endswith("\n\n"))

        check("SPEC-0007 §6.2", "?info carries the four ERC kernel elements",
              all(field in resolver.get(first, inflection="?info").body
                  for field in ("who:", "what:", "when:", "where:")))
        check("SPEC-0007 §6.2", "?info carries the commitment statement",
              "support-erc:" in resolver.get(first, inflection="?info").body
              and "never be reassigned"
              in resolver.get(first, inflection="?info").body)
        check("DR-0029",
              "a restricted ?info suppresses `what` rather than describing it",
              "what:   (:unal)"
              in resolver.get(withheld, inflection="?info").body)
        check("DR-0029", "a tombstoned ?info marks `what` unavailable",
              "what:   (:unav)"
              in resolver.get(redacted, inflection="?info").body)
        check("SPEC-0007 §6.2", "? and ?? are honoured as synonyms",
              resolver.get(first, inflection="?").body
              == resolver.get(first, inflection="??").body
              == resolver.get(first, inflection="?info").body)

        # ---- Gate 3 mints, and .vN names states ---------------------------

        gate, publisher = Gate(conn), Publisher(conn, register=register)

        proposition = str(uuid.uuid4())
        conn.execute("INSERT INTO proposition (id, statement) VALUES (%s,%s)",
                     (proposition, "The decree was published 2022-03-01."))
        assertion = gate.assert_directly(
            proposition_id=proposition, asserter_id=editor, valid_time=WAR,
            epistemic_category="finding",
            reasoning="Read from the official journal.")

        holding_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO holding (id, access_tier, retention_tier, "
            "completeness, rights_permission, ocfl_object_id) "
            "VALUES (%s,'public','permanent','original','may-display',%s)",
            (holding_id, f"holding-{holding_id}"))

        check("DR-0088", "nothing is minted before publication",
              register.ark_for("project_assertion", assertion) is None)

        decision = publisher.decide(
            person_id=editor, assertion_id=assertion, access_tier="public",
            rights_basis="Project text under CC-BY-4.0", sensitivity="none",
            evidentiary_disclosure="citable",
            rationale="Routine finding from a public source.")
        assertion_ark = register.ark_for("project_assertion", assertion)
        check("DR-0088", "a publication decision mints the assertion's ARK",
              assertion_ark is not None)
        check("DR-0088", "and records the decision as its basis",
              conn.execute(
                  "SELECT basis->>'publication_decision' "
                  "FROM identifier_assignment WHERE value = %s",
                  (assertion_ark,)).fetchone()[0] == decision)

        page = publisher.create_page(path="/decrees/2022-03-01", language="en")
        publisher.publish(page_id=page, person_id=editor,
                          rendered_text="The decree was published 2022-03-01.",
                          versions=V, assertions=[assertion],
                          holdings=[holding_id])
        page_ark = register.ark_for("published_page", page)
        check("DR-0088", "publishing a page mints the page",
              page_ark is not None)
        check("DR-0088", "and the holdings it rendered",
              register.ark_for("holding", holding_id) is not None)
        check("DR-0088", "an already-minted assertion keeps its identifier",
              register.ark_for("project_assertion", assertion)
              == assertion_ark)

        publisher.publish(page_id=page, person_id=editor,
                          rendered_text="The decree was published 1 March 2022.",
                          versions=V, assertions=[assertion],
                          kind="correction",
                          change_note="Date rendered in full (§77).")
        check("DR-0090", "a page ARK resolves to its current state",
              resolver.get(page_ark).status == 200)
        check("DR-0090", "and .vN resolves to a declared state",
              resolver.get(f"{page_ark}.v1").status == 200
              and resolver.get(f"{page_ark}.v2").status == 200)
        check("DR-0090", "an unknown state is a 404 while the ARK stays valid",
              resolver.get(f"{page_ark}.v9").status == 404
              and "is valid" in resolver.get(f"{page_ark}.v9").body)
        check("SPEC-0007 §7", "a class with no declared states refuses .vN",
              resolver.get(f"{first}.v1").status == 400)

        # ---- internal UUIDs never surface ---------------------------------

        bodies = [resolver.get(r["ark"]).body for r in register.health()]
        bodies += [resolver.get(r["ark"], inflection="?info").body
                   for r in register.health()]
        leaked = sorted({m for body in bodies for m in UUID_RE.findall(body)})
        check("SPEC-0007 §4.3",
              "no internal UUID appears in any resolver body",
              leaked == [])

        # ---- rebuild from the dump alone (PRES-009) ------------------------

        work = Path(os.environ.get("TMPDIR", "/tmp")) / f"uiw-ident-{os.getpid()}"
        dump_dir = work / "preservation"
        create_dump(conn, dump_dir, ROOT / "registry/dist/registry.json",
                    purpose="preservation")

        bare = {"PATH": os.environ.get("PATH", "/usr/bin:/bin")}
        rebuilt = {}
        for target in (first, merged_away, split_source, redacted, withheld):
            result = subprocess.run(
                [sys.executable, str(ROOT / "identifiers/tests/rebuild.py"),
                 str(dump_dir), target],
                capture_output=True, text=True, env=bare, cwd="/", check=True)
            rebuilt[target] = json.loads(result.stdout)

        # The rebuild implements SPEC-0007 §2.3 and §6.1 from the
        # specification text, not from `ark.py`. So this is not only a
        # preservation check: it is the only place where the check-character
        # rule as written down and the rule as implemented are compared. A
        # drift between them shows up here as a rejected identifier.
        check("SPEC-0007 §2.3",
              "the specification-derived rule accepts every minted identifier",
              all(r.get("reason") != "check character fails"
                  for r in rebuilt.values()))
        check("PRES-009",
              "a successor with the dump alone resolves every identifier",
              all(r["status"] != 404 for r in rebuilt.values()))
        check("PRES-009", "and agrees with the live resolver on every one",
              all(rebuilt[t]["status"] == resolver.get(t).status
                  for t in rebuilt))
        check("PRES-009", "including where a merge points",
              rebuilt[merged_away].get("terminal_ark") == survivor)

        public_dir = work / "public"
        create_dump(conn, public_dir, ROOT / "registry/dist/registry.json",
                    purpose="disclosure", access_tier="public")

        def rows_in(directory, table):
            path = directory / "data" / f"{table}.jsonl"
            return [json.loads(x) for x in path.open() if x.strip()]

        check("DATA-009",
              "a public dump carries the register, so citations still resolve",
              len(rows_in(public_dir, "public_identifier"))
              == len(register.health()))
        check("SPEC-0007 §4.3",
              "but not the mapping from identifiers to internal rows",
              rows_in(public_dir, "public_identifier_subject") == []
              and rows_in(public_dir, "identifier_assignment") == [])
        check("DR-0064",
              "and it carries what a split identifier resolves to",
              len(rows_in(public_dir, "disambiguation_record")) == 1)

        subprocess.run(["rm", "-rf", str(work)], check=False)

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
