# DR-pending-nsdc-file-import — Collecting a register export that a person downloads by hand

**Category:** operations / preservation | **Status:** Candidate — founder's answers recorded, approval pending (not approved, not enacted)
**Origin:** issue #46 (register the three `ua-nsdc-sanctions` candidates); the founder chose on 2026-11-07 to hold the registrations until a collection path exists, and to have this design drafted first
**Supersedes:** nothing | **Superseded by:** nothing
**Numbering:** drafted as `DR-pending-nsdc-file-import`; the number is assigned at merge, after the candidate is approved (DR-0102).
**Relates to:** DR-0067 (registration schema), DR-0071(a) and (b), DR-0074 (capture series), DR-0093 §3 (a person as agent of record), DR-0097 (software agent on preservation events), DR-0109 (civilian harm; not affected)

> **AI provenance (§80).** Drafted by an AI assistant (Anthropic Claude Code agent
> session) on 2026-11-07 from `sources/candidates/sanctions-authorities.yaml`
> (`ua-nsdc-sanctions-*`), `docs/sources/verification-ua-nsdc-sanctions.md` and
> `collector/`. Nothing was run against the register or the archive. The
> founder has not reviewed it.

## Context

Three candidates from the State Register of Sanctions of the National Security
and Defence Council of Ukraine are verified (`legal-entities`, `individuals`,
`vessels`). Their export URLs were confirmed on 2026-09-22/23 through
human-assisted browser access, after the register's Cloudflare managed challenge
had refused every automated session. The verification note records HTTP 403
from automated sessions on the register's pages and paths (§1, §2a, §2b); the
archive server itself has not been tested against these export URLs.

The collector can only fetch a locator itself. So a registration that goes
through the existing path would register sources the collector cannot collect
from. The founder ruled on 2026-11-07 to hold the registrations until a path
exists.

## What must hold, whichever path is chosen

- **Registered sources only** (DR-0071(a)): a file is collected only as the
  capture of a registered source, never as a loose file.
- **Personal data** (DR-0071(b)): the `individuals` class is the only one that
  carries constrained personal data. Nothing is structured from it, and nothing
  is published before the DR-0072 successor.
- **Preserve, structure and publish stay separate** (POL-0001 §1). A file
  import preserves; it creates no assertion (DR-0066).
- **A person is the agent of record** for a run that brings in new material
  (DR-0093 §3). The software agent records the preservation events (DR-0097).
- **Integrity before admission**: the bytes are hashed when they arrive, and the
  hash, the download time and the person's identity are recorded before the
  file enters the archive.

## Alternatives considered

**A. A file-import mode for the collector (proposed).** A person downloads the
CSV in their own browser. A collector command takes that file, not a URL,
with the registered source key, the agent of record and the source's declared
export URL recorded as text. The command:

1. hashes the file while reading it, and refuses a file that is empty, larger
   than the register's stated count allows, or whose header is not the one
   recorded for its class (vessels §2d; legal entities and individuals §2e);
2. builds a fetch result from the file's bytes, with the declared export URL as
   its locator and the file's own hash, and admits it through the existing
   `_admit()` path (which takes a fetch result, not a file, so this is a new
   entry point, not a change to `_admit()`), so it gets an OCFL object, a
   capture-series row (DR-0074), a quarantine copy discharged after admission
   (issue #51) and the same preservation events as a live capture, with the
   software agent named on those events (DR-0097);
3. records a `file_import` acquisition attempt with the download time and the
   person's identity, so the difference from a live fetch is visible in the
   record and never hidden.

*Cost:* a new collector entry point and tests; a change to the acquisition
record. `acquisition_attempt` has no column that says how the bytes arrived, and
its `outcome` check accepts only `success`, `failure`, `refused`, `not-found` and
`unchanged`. The record needs either a new column for the acquisition method or
a new outcome value, chosen in the migration card; either is a schema change
with a migration. *Benefit:* the archive keeps the same
guarantees for these three sources as for the others, and every import is a
recorded human act.

**B. Load the file by hand, outside the collector.** The file is copied into the
archive folder and recorded by a one-off script. *Cost:* the pipeline's checks,
capture series and discharge are skipped, so this archive would be weaker than
for every other source. *Not recommended.*

**C. Keep the verification record only.** No preservation for these sources.
*Cost:* the archive holds nothing from the register, which the project was set
up to prevent. *Not recommended* unless the founder decides these sources are
not to be preserved at all.

## Decision requested

1. Approve option A, or choose B or C.
2. If A: confirm that each import is a separate human act with the person as
   agent of record, and that a registration is still a separate founder act per
   source (DR-0093 §3), as before.
3. If A: confirm the `file_import` acquisition attempt as the one new value, and
   that the schema change is drafted as its own card with its own migration.
4. Decide whether the `individuals` class waits for DR-0072's successor before its
   first import. The "Personal data" rule above already keeps its contents out of
   structuring and publication; this question is only about whether it may be
   preserved before that successor is recorded.

## Founder's answers, 2026-11-10 to 2026-11-11 (not an approval)

The founder answered the four decision points above in an interactive session.
These answers are recorded here so the next revision can cite them. They do not
approve the record, and nothing is enacted by them.

1. **Route:** A, the file-import mode.
2. **Agent of record:** yes, as written. Each download and import is a separate
   human act with the person named as agent of record; each registration stays
   a separate founder act per source (DR-0093 §3).
3. **Schema change:** yes, drafted as its own card with its own migration. The
   choice between a new column and a new outcome value is made there.
4. **Individuals class:** waits for DR-0072's successor before its first import
   is preserved.

The record stays a candidate until the founder approves it. Approval is a
separate act and is not implied by these answers.

## Consequences if A is approved

- `ua-nsdc-sanctions-legal-entities` is the first candidate, because it
  carries no DR-0071(b) constraint. `vessels` and `individuals` follow, each a
  separate decision.
- The collector gains a file-import command with tests that fail when a check is
  removed (issue #46 becomes buildable).
- Each later export needs a person to download it again, so the record shows
  one human act per capture.

## Open points

- Whether the register's terms permit storing the export at all (not verified;
  the verification note does not record them).
- The register's export is refreshed as the register changes; the capture
  series records each new file as its own capture, not as a replacement.
