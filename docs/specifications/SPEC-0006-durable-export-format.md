# SPEC-0006 — Durable Export Format

**Class:** SPEC (DR-0046 control) | **Version:** 0.1 | **Status:** Draft — proposed
**Approval:** pending founder review | **Effective:** upon approval
**Supersedes:** — | **Superseded by:** —
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

## 9. Open questions

1. Whether a dump should carry the compiled registry itself, so a reader
   need not obtain it separately. Currently it records only the version.
2. Whether release baselines pin a dump by digest or merely require one
   (DR-0048 interaction).
3. Encryption or access-tier filtering for dumps containing restricted
   material — a dump of everything is a dump of confidential material too
   (§12, SEC-001). **Until this is resolved, dumps must be treated as
   carrying the highest access tier of any row they contain.**

## 10. Candidate Decision Record

- **CDR-P3-30:** Adopt SPEC-0006 as the controlled specification of the
  durable export format required by DR-0058, with JSONL authoritative and
  CSV documented as lossy, completeness derived from the database catalogue,
  and reconstruction verified by a process importing no project code.
