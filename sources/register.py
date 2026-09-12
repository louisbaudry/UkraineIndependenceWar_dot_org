#!/usr/bin/env python3
"""Register candidate sources into the DR-0067 source registry.

Candidate source definitions live in `sources/candidates/*.yaml` and are
**not registered** until someone runs this with `--commit`. That gap is the
point: OPS-001 makes collection registry-driven, so registering a source is
the act that authorises collecting from it, and it should be as deliberate as
any other authorisation.

    python3 sources/register.py --check              validate, change nothing
    python3 sources/register.py --dry-run --dbname X what a first run attempts
    python3 sources/register.py --commit  --dbname X register them
    python3 sources/register.py --commit  --dbname X --only eur-lex-sanctions

`--only` takes source keys and is how a per-source decision is executed. The
founder accepts sources individually; this flag is what "individually" means
in practice.

What this deliberately does NOT do: fetch anything. Registration authorises
collection; it does not perform it. Running the collector is a separate act
with its own record (DR-0070).
"""

from __future__ import annotations

import argparse
import sys
import uuid
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CANDIDATES = ROOT / "sources" / "candidates"

# Fields the registry requires. A candidate missing any of these is refused
# rather than defaulted: DR-0067's whole point is that collection policy is
# stated per source, and a silent default is a policy nobody chose.
REQUIRED = (
    "key", "source_type", "name", "jurisdiction", "collection_method",
    "scope_rules", "default_retention_tier", "default_access_tier",
    "rights_permission",
)

# Fields that carry a policy choice and must not be inherited by accident.
POLICY_FIELDS = (
    "scope_rules", "exclusions", "default_retention_tier",
    "default_access_tier", "rights_permission", "rights_basis",
)

# Optional verification fields. None of these is stored in the registry;
# they exist so the dry-run can say which locators have actually been
# fetched and which are still claims. `run_locators` lists the exact URLs a
# first collection run would pass to the collector; `locator_verified` is
# the date those were last fetched successfully; `verification_note` says
# where the record of that fetch lives.
VERIFICATION_FIELDS = ("locator_verified", "run_locators", "verification_note")


class RegistrationError(Exception):
    """A candidate that must not be registered as it stands."""


def load_candidates() -> tuple[list[dict], list[dict]]:
    """Read every candidate file. Returns (sources, dependence)."""
    sources: list[dict] = []
    dependence: list[dict] = []
    for path in sorted(CANDIDATES.glob("*.yaml")):
        doc = yaml.safe_load(path.read_text()) or {}
        for source in doc.get("sources", []):
            source["_file"] = path.name
            sources.append(source)
        dependence.extend(doc.get("dependence", []))
    return sources, dependence


def validate(
    sources: list[dict], dependence: list[dict],
    known_keys: set[str] | None = None,
) -> list[str]:
    """Everything checkable without a database or a network.

    `known_keys`, if given, is used only for the dependence-existence check
    below, in place of `sources`' own keys: a `--only` call validates a
    filtered `sources`, but a dependence link may legitimately name a
    candidate outside that filter — one already registered by an earlier
    call, or one meant to be registered later (DR-pending-second-source-
    registrations). Every other check still scopes to `sources` as given.
    """
    problems: list[str] = []
    keys = [s.get("key") for s in sources]
    dependence_keys = known_keys if known_keys is not None else set(keys)

    for key in {k for k in keys if keys.count(k) > 1}:
        problems.append(f"duplicate source key: {key!r}")

    for source in sources:
        key = source.get("key", "<no key>")
        for field in REQUIRED:
            if not source.get(field):
                problems.append(f"{key}: missing required field {field!r}")

        # PRES-012 / POL-0001 §5.9, mirrored from the schema constraint so the
        # failure is caught at review time rather than at insert time.
        if source.get("expects_graphic_content") and \
                source.get("default_access_tier") == "public":
            problems.append(
                f"{key}: expects graphic content but defaults to public "
                "(PRES-012, POL-0001 §5.9)")

        # A rights basis that has not been checked must say so. Silence here
        # reads as "checked and fine", which is the wrong default (§14).
        basis = (source.get("rights_basis") or "")
        if source.get("rights_permission") in ("may-redistribute",
                                               "may-provide-to-subscribers") \
                and "NOT LEGALLY REVIEWED" not in basis.upper() \
                and "UNVERIFIED" not in basis.upper():
            problems.append(
                f"{key}: claims {source['rights_permission']!r} without "
                "flagging that the basis is unreviewed. Either record the "
                "review or say it has not happened (§14, POL-0001 §10)")

        # DR-0071(a): scope must be human-configured, not open-ended.
        scope = (source.get("scope_rules") or "").lower()
        if any(word in scope for word in ("all pages", "entire site",
                                          "crawl", "everything")):
            problems.append(
                f"{key}: scope reads as open-ended crawling, which DR-0071(a) "
                "prohibits until POL-0001 §9's releases take effect")

        # Verification fields are optional, but if present they must be
        # what they claim to be: a date, and absolute https locators. A
        # verification that cannot be read is not a verification.
        verified = source.get("locator_verified")
        if verified is not None and not isinstance(verified, date):
            problems.append(
                f"{key}: locator_verified must be an ISO date, got {verified!r}")
        run_locators = source.get("run_locators")
        if run_locators is not None:
            if not isinstance(run_locators, list) or not run_locators:
                problems.append(f"{key}: run_locators must be a non-empty list")
            else:
                for locator in run_locators:
                    if not (isinstance(locator, str)
                            and locator.startswith("https://")):
                        problems.append(
                            f"{key}: run locator {locator!r} is not an "
                            "absolute https URL")
        if run_locators and verified is None:
            problems.append(
                f"{key}: run_locators are listed but locator_verified is not "
                "set; either record the date they were fetched or do not "
                "claim them as run locators")

    for link in dependence:
        for end in ("from", "to"):
            if link.get(end) not in dependence_keys:
                problems.append(
                    f"dependence references unknown source {link.get(end)!r}")
        if not link.get("note"):
            problems.append(
                f"dependence {link.get('from')}→{link.get('to')}: no note. "
                "Independence is a researched conclusion and dependence is a "
                "stated one; both need their reasoning (DR-0028)")

    return problems


def describe(sources: list[dict], dependence: list[dict]) -> None:
    """What registering these would authorise, and what it would commit to."""
    print(f"{len(sources)} candidate source(s) in {CANDIDATES}\n")

    for source in sources:
        print(f"  {source['key']}")
        print(f"    {source['name']}")
        print(f"    {source.get('jurisdiction','?')} · "
              f"{source['source_type']} · "
              f"{', '.join(source.get('primary_languages') or ['?'])} · "
              f"cadence {source.get('collection_cadence','unspecified')}")
        print(f"    retention {source['default_retention_tier']} · "
              f"access {source['default_access_tier']} · "
              f"rights {source['rights_permission']}")
        verified = source.get("locator_verified")
        status = f"verified {verified.isoformat()}" if verified else "UNFETCHED"
        print(f"    locator {source.get('locator','—')}  ({status})")
        for locator in source.get("run_locators") or []:
            print(f"      run locator {locator}")
        if source.get("verification_note"):
            print(f"    verification: {source['verification_note']}")
        print()

    if dependence:
        print("Declared dependence (DR-0028) — these do not corroborate each "
              "other:")
        for link in dependence:
            print(f"  {link['from']} --{link['relation']}--> {link['to']}")
        print()

    # Commitments the founder is taking on, stated rather than discovered
    # later. Each of these is a real obligation, not a nicety.
    languages = sorted({lang for s in sources
                        for lang in (s.get("primary_languages") or [])})
    non_english = [lang for lang in languages if lang != "en"]
    print("Registering these commits the project to:")
    if non_english:
        print(f"  · reading capacity in {', '.join(non_english)} at Gate 2 — "
              "no translations are seeded (DR-0081)")
    permanent = [s["key"] for s in sources
                 if s["default_retention_tier"] == "permanent"]
    if permanent:
        print(f"  · permanent retention for {len(permanent)} source(s), which "
              "means indefinite fixity checking (DR-0005, 180-day cadence)")
    unverified = [s["key"] for s in sources
                  if "UNVERIFIED" in (s.get("rights_basis") or "").upper()]
    if unverified:
        print(f"  · resolving unverified rights positions for: "
              f"{', '.join(unverified)} (§14)")
    unfetched = [s["key"] for s in sources if not s.get("locator_verified")]
    if unfetched:
        print(f"  · a first collection run against locators that have not been "
              f"fetched ({', '.join(unfetched)}); 404s and format surprises "
              "are expected outcomes, recorded as failed acquisitions "
              "(PRES-007), not system faults")
    else:
        print("  · a first collection run against locators that were fetched "
              "successfully at verification time. A past fetch does not "
              "guarantee the next one; a failure is still recorded as a "
              "failed acquisition (PRES-007), not a system fault")
    print()


def commit(conn, sources: list[dict], dependence: list[dict],
           asserter_id: str, all_sources_by_key: dict[str, dict] | None = None
           ) -> dict[str, str]:
    """Insert the sources and their declared dependence.

    `asserter_id` is a person: declaring that two sources are dependent is an
    analytic judgment about them (DR-0028), not a configuration value, and it
    carries an asserter like any other assertion.

    `all_sources_by_key`, if given, lets a dependence link's other end
    resolve against a source registered by an *earlier* call, not only this
    one: a name lookup in the database, when the key is not in this call's
    own batch. Without it, a dependence link is recorded only when both
    ends are registered in the same `--commit` call — the gap
    DR-pending-second-source-registrations found, where
    `uk-ofsi-consolidated`'s declared dependence on the already-registered
    `eu-consolidated-list` was silently dropped.
    """
    all_sources_by_key = all_sources_by_key or {}
    ids: dict[str, str] = {}
    with conn.transaction():
        for source in sources:
            source_id = str(uuid.uuid4())
            ids[source["key"]] = source_id
            conn.execute(
                """
                INSERT INTO source
                    (id, source_type, name, locator, publisher, jurisdiction,
                     primary_languages, coverage_start, collection_method,
                     collection_cadence, scope_rules, exclusions,
                     capture_format, default_retention_tier,
                     default_access_tier, default_sensitivity,
                     expects_graphic_content, rights_permission, rights_basis,
                     grade_source_reliability, grade_item_credibility)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                        %s,%s,%s,%s)
                """,
                (source_id, source["source_type"], source["name"],
                 source.get("locator"), source.get("publisher"),
                 source["jurisdiction"], source.get("primary_languages"),
                 source.get("coverage_start"), source["collection_method"],
                 source.get("collection_cadence"), source["scope_rules"],
                 source.get("exclusions"),
                 source.get("capture_format", "http"),
                 source["default_retention_tier"],
                 source["default_access_tier"],
                 source.get("default_sensitivity"),
                 bool(source.get("expects_graphic_content")),
                 source["rights_permission"], source.get("rights_basis"),
                 source.get("grade_source_reliability"),
                 source.get("grade_item_credibility")),
            )

        def resolve(key: str) -> str | None:
            """This call's own batch first; otherwise an existing source
            already in the database, by name. Never asserts a link to a
            source that does not exist as a real registered row yet."""
            if key in ids:
                return ids[key]
            candidate = all_sources_by_key.get(key)
            if candidate is None:
                return None
            row = conn.execute(
                "SELECT id FROM source WHERE name = %s", (candidate["name"],)
            ).fetchone()
            return str(row[0]) if row else None

        for link in dependence:
            dependent_id = resolve(link["from"])
            depends_on_id = resolve(link["to"])
            if dependent_id and depends_on_id:
                conn.execute(
                    "INSERT INTO source_dependence (id, dependent_id, "
                    "depends_on_id, relation, note, asserter_id) "
                    "VALUES (%s,%s,%s,%s,%s,%s)",
                    (str(uuid.uuid4()), dependent_id, depends_on_id,
                     link["relation"], link["note"], asserter_id),
                )
            else:
                unresolved = link["from"] if not dependent_id else link["to"]
                print(f"  dependence not recorded yet: {link['from']} -> "
                      f"{link['to']} ({unresolved!r} is not a registered "
                      "source)")
    return ids


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="validate candidates, change nothing")
    parser.add_argument("--dry-run", action="store_true",
                        help="describe what registering would authorise")
    parser.add_argument("--commit", action="store_true",
                        help="actually register")
    parser.add_argument("--dbname")
    parser.add_argument("--only", nargs="*", metavar="KEY",
                        help="register only these source keys")
    parser.add_argument("--agent", metavar="UUID",
                        help="pipeline_agent id of the person registering; "
                             "declared dependence is asserted by them "
                             "(DR-0028)")
    args = parser.parse_args()

    all_sources, dependence = load_candidates()
    sources = all_sources
    known_keys = None
    if args.only:
        unknown = set(args.only) - {s["key"] for s in sources}
        if unknown:
            print(f"unknown source key(s): {', '.join(sorted(unknown))}")
            return 1
        sources = [s for s in sources if s["key"] in args.only]
        # Keep a link if either end is in this batch: the other end may
        # already be registered from an earlier call, or may get registered
        # right now. commit() resolves whichever is the case; a plain
        # "both ends in this batch" filter silently dropped a dependence on
        # an already-registered source (DR-pending-second-source-registrations).
        dependence = [d for d in dependence
                      if d["from"] in args.only or d["to"] in args.only]
        known_keys = {s["key"] for s in all_sources}

    problems = validate(sources, dependence, known_keys=known_keys)
    if problems:
        print("Candidates cannot be registered as they stand:\n")
        for problem in problems:
            print(f"  {problem}")
        return 1
    print(f"{len(sources)} candidate(s) validate.\n")

    if args.check:
        return 0

    describe(sources, dependence)

    if not args.commit:
        print("Nothing registered. Re-run with --commit --dbname <db> to "
              "register, or --only <key> to register individually.")
        return 0

    if not args.dbname:
        print("--commit needs --dbname")
        return 1
    if dependence and not args.agent:
        print("--commit needs --agent: the declared dependence between these "
              "sources is an analytic judgment and carries an asserter "
              "(DR-0028). Pass the pipeline_agent id of the person "
              "registering them.")
        return 1

    import psycopg
    with psycopg.connect(dbname=args.dbname, autocommit=True) as conn:
        ids = commit(conn, sources, dependence, args.agent,
                    all_sources_by_key={s["key"]: s for s in all_sources})
    for key, source_id in ids.items():
        print(f"  registered  {key}  {source_id}")
    print(f"\n{len(ids)} source(s) registered. Collection is now authorised "
          "for them and has not been performed — running the collector is a "
          "separate act with its own record (DR-0070).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
