# SPEC-0006 — Durable Export Format

**Class:** SPEC (DR-0046 control) | **Version:** 1.0 | **Status:** Approved — Effective
**Approval:** founder/principal editor, 2026-08-21 | **Effective:** 2026-08-21
**Supersedes:** — | **Superseded by:** —
**Change history:** 0.1 drafted 2026-08-21 alongside its implementation. Approved as 1.0 the same day on the condition that unfiltered dumps be blocked until access-tier filtering existed (DR-0084); §9's open question 3 is accordingly resolved and replaced by §9A, and the implementation now refuses to produce a dump without a declared purpose.
**Governed by:** DR-0058 (durable export is a standing obligation; the format specification is a SPEC-class controlled document), DR-0048 (release baselines), DR-0005 (fixity), DR-0050 (registry), DR-0054 (layered representation).
**Implemented by:** `export/dump.py`. Verified by `export/tests/reconstruct.py`.

### AI provenance (record §80)

Drafted 2026-08-21 by an AI assistant (Anthropic Claude Code agent session)
alongside the implementation it specifies. Candidate until approved.

---

## 1. Why this exists

OCFL makes the preserved **bytes** self-describing (DR-0073). It says nothing
about the **assertions** — what a holding is, what it is complete of, what a
source said, what the project concluded. Those live in a database, which is
precisely the dependency PRES-009 forbids:

> The archive is reconstructible without the public website — and, by
> extension, without the original database software.

This format is the other half. **A dump and an OCFL root together are the
archive; neither alone is.**

## 2. Layout

```
manifest.json           What this dump is, what it contains, and its fixity
manifest.json.sha256    Sidecar attesting to the manifest
schema.json             Every table and column, linked to its registry entry
README.txt              Orientation for a human with no other context
data/<table>.jsonl      Authoritative data, one JSON object per row
data/<table>.csv        The same data, flattened — lossy, see §5
```

## 3. Completeness is structural

The table list is read from the **database catalogue**, not from a list
maintained in the exporter. A table added to the schema and forgotten in the
dumper would break PRES-009 silently; deriving the list means a new table is
exported whether or not anyone remembered it. A test asserts that the set of
dumped tables equals the set of tables in the database.

## 4. `schema.json` — what makes the dump interpretable

Readable is not the same as interpretable. A column of values like `likely`
is legible but meaningless without knowing that it denotes 55–80% (DR-0065).
For every column the descriptor records name, type, nullability and default;
and additionally:

- `enum_values` — the permitted values, inline, for any controlled column;
- `registry_entry` — the semantic-registry entry defining them (DR-0050),
  so a reader can resolve meaning against the registry's own export;
- `composite_fields` — the internal structure of composite types such as
  `timespan` and `quantity`.

Table comments are carried through, so the reasons recorded in the schema —
why world actors have no name column, why quarantine is not the archive —
travel with the data.

## 5. Two forms, one authoritative

**JSONL is authoritative.** Composite values keep their structure, `jsonb`
stays JSON, and binary values are hex strings prefixed `\x`.

**CSV is a convenience and is lossy.** Composite and JSON columns render as
PostgreSQL's text representation rather than structure. It exists because a
spreadsheet in thirty years will open a CSV without help, and that is worth
the duplication. **Where the two differ, the JSONL is correct** — stated in
the README shipped inside every dump, not only here.

## 6. Fixity

Every data file carries a SHA-256 in the manifest, with row counts. The
manifest carries digests for `schema.json` and `README.txt`. A sidecar
attests to the manifest itself, so the chain is closed: sidecar → manifest →
every file.

`verify_dump()` checks all of it, including that JSONL row counts match what
the manifest claims. A dump is generated and verified at every release
baseline (DR-0048, DR-0058).

## 7. Reading it honestly

The README shipped in each dump tells a future reader four things that the
data alone would not convey, because misreading them would misrepresent the
project's knowledge:

- **absence states** — a field saying `unknown`, `not-researched`,
  `no-evidence-found`, `withheld` or `redacted` is recording *why* something
  is absent; a missing value never silently means "no" (DR-0029);
- **quantity semantics** — `at-least` means at least, not exactly (DR-0030);
- **tombstones** — redaction fields mark content removed under a recorded
  ground and authority; the removal is deliberate and its fact is part of
  the record (DR-0077);
- **supersession** — a superseded assertion is not an error; it is what the
  project held at that time, retained so its changes of mind survive
  (DR-0055).

## 8. Verification

`export/tests/reconstruct.py` performs the demonstration REQ-PRES-009
requires. It **imports nothing from the project** — no `ocfl`, no
`pipeline`, no `dump`, no database — using only the standard library, this
specification, the OCFL 1.1 specification, and the files on disk. It runs in
a separate process with a bare environment.

It reconstructs by: verifying the manifest chain; reading the schema to
confirm vocabulary columns resolve to registry entries; loading holdings,
preserved objects, events and attempts; locating each holding's OCFL object
**by reading inventories rather than reimplementing the storage layout**;
verifying content against the digest algorithm the inventory declares; and
cross-checking that the dump's recorded digest appears in the OCFL fixity
block, so a disagreement between dump and storage is caught.

If that script stops working, the archive's central promise has stopped
being true. That is what it is for.

## 9A. Access tiers — no dump without a declared purpose

A dump of everything is a dump of confidential material too (§12, SEC-001).
The founder's ruling on CDR-P3-30 was that unfiltered dumps be **blocked**
until filtering existed rather than governed by a documented caveat; DR-0084
records it, and the implementation enforces it. **There is no default
purpose and no default tier.**

### Two purposes

| Purpose | Contents | Handling |
|---|---|---|
| **preservation** | Complete — nothing filtered, because succession (PRES-010) and reconstruction (PRES-009) need the whole archive | Carries the highest tier present, named in the manifest, and must be handled at that tier. Not a disclosure export. |
| **disclosure** | Filtered to a named access tier | Omissions counted per table; the manifest states plainly that it is not the complete archive |

### Tiers are not a ladder

`researcher-restricted` and `investigator-restricted` are lateral grants to
named parties, not steps above `internal`; `private-preservation` means
disclosed to nobody (§12). Containment is therefore **declared**, not
computed from an ordering — `export/tiers.py` states which tiers each
disclosure target admits.

**`confidential` and `private-preservation` are not disclosure targets at
all.** Material at those tiers reaches a recipient through a preservation
dump under an explicit arrangement, never a routine export (SEC-001).

### Two structural safety properties

- **Fail closed.** Every table must have a declared tier rule. A table added
  to the schema without one makes the dump *refuse*, not export it at
  whatever tier is convenient. With §3's catalogue-derived table list, a
  forgotten table is loud in both directions: it appears, and it halts the
  run until someone classifies it deliberately.
- **Unresolvable means withheld.** A row whose tier cannot be determined is
  omitted, never published. Failing open here would be the single mistake
  this machinery exists to prevent.

### Omission is stated, not silent

A filtered dump records per-table omission counts and a completeness
statement saying it is not the whole archive — §57's discipline applied to
exports, so a reader cannot mistake a public dump for the archive itself.

## 9B. Remaining open questions

1. Whether a dump should carry the compiled registry itself, so a reader
   need not obtain it separately. Currently it records only the version.
2. Whether release baselines pin a dump by digest or merely require one
   (DR-0048 interaction).
3. Whether disclosure dumps should eventually **redact** rather than omit —
   keeping the row and replacing restricted values with the `withheld`
   absence state (DR-0029), so a reader can see that something exists
   without seeing it. Omission is the safer starting point; redaction is
   more informative and can follow once the column-level classification it
   needs exists.

## 10. Decision Record arising (enacted)

**DR-0084** — adoption of this specification, approved by the founder on
2026-08-21 with the condition recorded in §9A.
