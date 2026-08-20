# Phase III / Study 3 — Storage & Preservation Layout
## Working Paper 3.3

**Project:** Ukraine's Second War of Independence
**Status:** CANDIDATE — AI-drafted, awaiting founder review.
**Version:** 3.3
**Mandate:** Q-03 — evaluate OCFL and decide the at-rest storage layout for preserved bytes; answer WP 3.1 §5 Q5 ("does OCFL's versioning implement or conflict with the immutability rule?").
**Constraints inherited:** DR-0001 (OAIS AIPs), DR-0005 (SHA-256 at ingestion, fixity events), DR-0007 (BagIt envelopes), DR-0009 (backup ≠ archive ≠ release), DR-0055 (append-only, governed redaction), DR-0058 (durable export), DR-0061 (holding), DR-0068 (retention tiers), DR-0069 (quarantine outside the archive); PRES-001/002/003/009.

### AI provenance (record §80)

Drafted 2026-08-16 by an AI assistant (Anthropic Claude Code agent session)
at the founder's direction. OCFL version status verified by web retrieval
(§9). Candidate until approved.

---

## 1. What the requirements demand of at-rest storage

1. **Immutable originals, separate derivatives** (PRES-001, DR-0055).
2. **Fixity recorded and re-checkable** (DR-0005, PRES-002/003).
3. **Reconstructible without the project's software** (PRES-009) — the
   decisive requirement: a future archivist with the bytes and no code must
   be able to determine what is there, what it was, and whether it is
   intact.
4. **Natural AIP containers** (DR-0001), transferable to a successor archive
   (PRES-010).
5. **Separable from backup** (DR-0009): replication is infrastructure;
   archival preservation is a managed layer above it.
6. **Governed redaction possible but exceptional** (DR-0055, POL-0001 §6).
7. **Operationally boring** — WP 3.1's requirement 8: a single-founder
   project over decades cannot depend on exotic infrastructure.

## 2. OCFL in brief

The **Oxford Common File Layout** (current version **1.1.1**; 1.0 released
July 2020, 1.1 October 2022; a 2.0 is in early consideration) specifies an
application-independent way to store versioned digital objects on any
filesystem or object store:

- An **object** is a directory containing an `inventory.json` and versioned
  content directories (`v1`, `v2`, …).
- The inventory carries the **complete version history** and a manifest
  mapping **content digests → paths**; every version's full logical state is
  recorded, so any version can be reconstructed.
- **Forward-delta versioning:** a new version references unchanged content
  from earlier versions rather than copying it.
- **Content addressing by digest** (SHA-512 by default; SHA-256 permitted),
  with an optional **fixity block** carrying additional algorithms.
- **Self-describing and rebuildable:** the specification's guiding principle
  is that the object can be understood, validated, and reconstructed from
  the files alone, with no database and no originating software.

That last property is what distinguishes OCFL from every ad hoc convention:
it is designed for exactly the failure mode PRES-009 names.

## 3. Alternatives evaluated

| Option | Against the §1 demands |
|---|---|
| **Project-specific filesystem convention** | Everything in §1 becomes bespoke work — and the convention itself becomes undocumented tacit knowledge, the opposite of PRES-009. Violates the standards-first principle (§94). |
| **BagIt at rest** | BagIt is a *transfer* convention: no versioning, no forward-delta, no in-place evolution of an object. Adding derivatives means rewriting or proliferating bags. Correct for transfer (DR-0007), wrong for at-rest. |
| **Object storage with application-managed metadata** | Fast and cheap, but the layout's meaning lives in the application database — precisely the dependency PRES-009 forbids. (Note: OCFL *runs on* object storage; this option means OCFL-less object storage.) |
| **A repository platform (Fedora, Archivematica, etc.)** | Substantial operational surface for one founder; several already use OCFL underneath. Adopting the layout without the platform keeps the option to add a platform later. |
| **OCFL** | Meets every demand in §1 directly; widely implemented; plain files, replicable by any means. |

## 4. The immutability question (WP 3.1 §5 Q5), answered

**OCFL implements the rule; it does not conflict with it.** OCFL versions
are immutable once written: a new version adds content and a new inventory
state without altering prior version content. Adding a derivative in `v2`
never touches the original in `v1`, and forward-delta means the original is
referenced, not copied.

The apparent tension — "originals are immutable and derivatives are separate
objects" vs "OCFL versions an object" — dissolves once **storage identity
and conceptual identity are distinguished**, which is exactly the layered
architecture of DR-0054. A derivative is a distinct object in the canonical
store, with its own PREMIS identity and PROV lineage, *and* it may live as a
later version inside the same OCFL storage object. Sharing a storage
container does not merge conceptual identities.

## 5. Three design decisions

### 5.1 What is an OCFL object? → **the holding** (DR-0061)

A holding is precisely "what the archive possesses of one documentary item"
— the right granularity for an archival storage object.

- `v1` = the original preserved representation as acquired.
- Later versions add derivative representations (OCR text, transcript,
  normalized formats, extracted media) as they are produced.
- The holding's canonical-store record (DR-0061) remains the authority on
  what each representation *is*; OCFL is where the bytes live.

**Successive captures of the same URL are different holdings**, hence
different OCFL objects, related by the capture-series relation in the
canonical store (Memento pattern, DR-0023). Capture series are a data-model
relationship, not a storage-layout artifact — otherwise the evidential
distinctness of each capture would be buried in version history.

Rejected alternatives: one object per representation (scatters a holding
across storage, loses natural grouping without conceptual gain); one object
per capture series (buries evidentially distinct captures inside versions).

### 5.2 Digest algorithm → **SHA-512 content addressing + SHA-256 fixity block**

OCFL's default content-addressing digest is SHA-512, which carries a better
collision margin for a decades-horizon archive. DR-0005 mandates SHA-256 at
ingestion and existing practice already records it.

Both are kept: **SHA-512 as the OCFL content digest, SHA-256 recorded in the
OCFL fixity block** and in the canonical store. This satisfies DR-0005
literally, preserves continuity with every hash recorded so far, gains the
specification default, and gives independent cross-checking — two algorithms
disagreeing is itself a signal.

### 5.3 Retention tiers → **separate storage roots**

Only `permanent` and `medium-term` items (DR-0068) have bytes in OCFL;
`metadata-only` has none, and `discard` never enters.

`permanent` and `medium-term` live in **separate OCFL storage roots**, so
that disposition at a medium-term review date is a clean operation on the
medium-term root and **can never touch the permanent archive**. Promotion
from medium-term to permanent is a recorded preservation event that moves
the object between roots.

Storage-root layout: a **hashed n-tuple** mapping of object ID to path —
avoids directory-size limits and keeps identifiers (which may echo source
URLs) out of directory names.

## 6. How it composes with what is already decided

- **BagIt (DR-0007)** is for transfer and export envelopes; **OCFL** is the
  at-rest layout. Complementary, not competing: an evidence package is
  assembled *from* OCFL holdings into a bag.
- **The durable dump (DR-0058)** carries *assertions*; OCFL carries
  *bytes*. Together they are the complete archive — a future archivist needs
  both, and both are exercised at every release baseline (DR-0048).
- **Quarantine (DR-0069)** is **not** OCFL: quarantined material is not
  archival. Material enters OCFL at Gate 1 (DR-0066), which is the moment
  archival guarantees begin.
- **Backup (DR-0009)** replicates the OCFL roots by ordinary means (plain
  files replicate anywhere). Backups are not preservation: fixity checking,
  format watch, and preservation planning operate on the OCFL layer.
- **Redaction (DR-0055, POL-0001 §6)** is the one operation that breaks
  OCFL's normal guarantees. It is permitted only through the governed path:
  a recorded decision, content purged, inventory corrected, a **preservation
  event and tombstone retained**, and the redaction itself never silent.
- **Fixity events (DR-0005)** are PREMIS events in the canonical store;
  OCFL validation is how they are performed.

## 7. Candidate Decision Records (proposals — require founder approval)

- **CDR-P3-20:** **Adopt OCFL (1.1.1) as the at-rest archival storage
  layout** for preserved bytes, on the grounds that it satisfies PRES-009's
  reconstructibility requirement by design; OCFL objects are the project's
  AIP containers (DR-0001).
- **CDR-P3-21:** **The OCFL object is the holding** (DR-0061); derivative
  representations are later versions of the same object; successive captures
  are separate objects related in the canonical store, not versions.
- **CDR-P3-22:** **SHA-512 content addressing with SHA-256 in the fixity
  block**, satisfying DR-0005 and preserving continuity with existing
  practice.
- **CDR-P3-23:** **Separate OCFL storage roots per retention tier**
  (`permanent`, `medium-term`), with promotion as a recorded event, and a
  hashed n-tuple storage-root layout.
- **CDR-P3-24:** **Redaction is the sole exception** to OCFL immutability,
  permitted only via the DR-0055 / POL-0001 §6 governed path, always leaving
  a preservation event and tombstone.

## 8. Open questions raised

1. OCFL implementation library vs direct implementation — small enough to
   implement directly, but existing libraries are validated; decide at build
   time.
2. Whether to run OCFL on filesystem or S3-compatible object storage (the
   spec supports both); interacts with hosting choices not yet made.
3. Fixity-check cadence and sampling strategy for a growing archive
   (DR-0005 left cadence open).
4. Format identification and normalization policy — what gets normalized on
   ingest vs preserved as-is (touches PREMIS event types in DR-0060).
5. Whether WARC files receive any special treatment inside OCFL objects, or
   are simply content like any other (probably the latter).

## 9. Sources

- OCFL: [ocfl.io specifications](https://ocfl.io/); [1.1 change log](https://ocfl.io/1.1/spec/change-log.html); [OCFL news, version history](https://ocfl.io/news/); [specification archive on Zenodo](https://zenodo.org/records/14204936); [CNI, OCFL as a storage foundation for digital preservation systems](https://www.cni.org/topics/digital-preservation/oxford-common-file-layout-a-storage-foundation-for-digital-preservation-systems)
- DR-0001, DR-0005, DR-0007, DR-0009, DR-0055, DR-0058, DR-0061, DR-0068, DR-0069; Phase II output 6 (PRES requirements)
