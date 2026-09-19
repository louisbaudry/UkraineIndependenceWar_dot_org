# Glossary

Terms specific to this project and to the archival, preservation, and
sanctions-compliance domains it works in. Definitions are written for a
reader new to the repository; they summarize how the term is used *here*,
not a full external standard. Where a term is defined more precisely by a
Decision Record, policy, or standard, that source is cited — this glossary
does not supersede it.

This is an informal reference, not a controlled document under DR-0046. It
carries no version/status block and is kept current by whoever edits it
next; if a definition here ever conflicts with a Decision Record or policy,
the DR/policy governs.

## Governance and process

**Decision Record (DR)**
A numbered, permanent record of a founder decision (`docs/decision-records/DR-nnnn-slug.md`),
covering context, alternatives considered, the decision, and its
consequences. Approved DRs are never edited in place — a change is a new DR
that supersedes the old one (see "Supersession"). See
[DR-0046](docs/decision-records/DR-0046-unified-document-control.md).

**DR-pending**
The working name and filename (`DR-pending-slug.md`) for a Decision Record
while it is being drafted. No DR is ever numbered before the founder has
decided; the real `DR-nnnn` is assigned once, at merge time, from the
highest number in `origin/main`'s register. See DR-0095.

**Candidate Decision Record (CDR)**
A decision proposed inside a working paper but not yet made — written as
`CDR-pending-slug` and numbered `CDR-P3-nn` only at merge, from a single
global sequence shared across all working papers (not per-paper). A CDR
that the founder rules on becomes a real DR.

**Working paper (WP)**
A study prepared for the founder's review, filed at
`docs/phase-3/working-papers/wp-3.N-slug.md`, carrying a header block
(status, mandate, constraints), an AI-provenance statement, and a
"Candidate Decision Records" section. Working papers do not decide
anything; they present options for the founder to rule on.

**Controlled document (DR-0046)**
Any Decision Record, SPEC, POL, REQ, METH, or PROC document, each carrying
an explicit status, version, approval/effective dates, and supersession
links as metadata — never inferred from Git history. A commit is not an
approval; a merge is not an enactment.

**Supersession**
The only way an approved controlled document changes: a new document
replaces it and both are retained, with the replacement explicit (Phase I
record §77). The narrow, enacted exception is in-place revision under four
strict conditions in the same session (DR-0102 Decision 7).

**AI provenance**
A required note on any AI-drafted document (working paper, candidate DR,
etc.) stating what was and was not verified, per record §80. Such documents
remain candidates until the founder approves them.

**Founder / principal editor**
The project's final editorial and decision-making authority (Phase I
record §78–79). AI drafts and proposes; the founder decides. Standing
rulings recorded in `CLAUDE.md` bind future sessions until superseded.

**Gate 1 / Gate 2 / Gate 3**
The project's sequence of human decision points that separate preservation
from interpretation: preserving bytes (Gate 1) creates no documentary
assertions on its own; structuring evidence (Gate 2) and publishing (Gate 3)
are each separate human decisions at a declared risk tier, never automated
(DR-0066, Principle 5).

**Track A / Track B (WP 3.4)**
The acquisition strategy's two phases. Track A (§4.1) is preparatory work —
census tooling, registration groundwork, format evaluation — that collects
nothing at scale and may proceed now. Track B (§4.2) is scaled collection
itself, and does not start until the POL-0001 §10 legal review is recorded.

**Registration class**
A named, reusable set of policy defaults (capture format, rights
permission, etc.) that a source record inherits from and can override,
reducing per-source authorization decisions to per-class ones (DR-0103).

## Archival and preservation

**OAIS**
Open Archival Information System (ISO 14721) — the reference model this
project adopts for what an archive must do to preserve information over
time (DR-0001).

**PREMIS**
The preservation-metadata vocabulary (v3.0) used to record events like
fixity checks, migrations, and ingestion (DR-0002).

**PROV**
The W3C provenance vocabulary used across the pipeline to record
derivation and agency — who or what produced or acted on a given object
(DR-0003).

**Fixity**
A cryptographic checksum (SHA-256, computed at ingestion and re-checked
later) proving that preserved bytes have not changed. Fixity checks and
their outcomes are recorded as PREMIS events (DR-0005).

**WARC**
Web ARChive format — the container used for high-value web captures,
preserving the full HTTP transaction (request, response, headers), not just
the payload (DR-0006).

**WACZ**
A newer web-archive container format built on WARC, evaluated but not yet
adopted here because its signing layer is still a pre-1.0 draft (see WP
3.6 / DR-0006).

**OCFL**
Oxford Common File Layout — the on-disk object storage layout this project
uses for archival storage, versioned and self-describing independent of any
particular database.

**BagIt**
A packaging convention for transferring and verifying a set of files as a
unit (a "bag"), used for envelopes around preserved content pending the
project's own evidence-package design (DR-0007).

**RO-Crate**
A lightweight packaging convention for research/data objects with linked
metadata, studied as an input to the evidence-package design (DR-0007).

**Capture format**
The registry-declared shape a source's collected bytes take — `warc` for a
full web capture, `http` for a bare response body — honored exactly as
declared per source (DR-0006, DR-0067).

**Preservation event**
A recorded act on an object during ingestion or afterward (e.g., a fixity
check, a format migration), carrying an acting agent, per PREMIS/PROV. As
of DR-0097, collection runs record both a human agent of record and a
separate software agent.

**Collector run**
One execution of the collection pipeline (`collector/run.py`) against one
or more registered sources, producing fetch results and preservation
events but, by design, zero documentary assertions (DR-0066).

**Chain of custody**
The documented history of who held and handled a piece of evidence. This
project explicitly never claims *legal* chain of custody (DR-0008,
LEGAL-007) — it records acquisition and preservation facts instead.

**Berkeley Protocol**
An international protocol for open-source (digital) investigations that
guides this project's custody and documentation practices without being
adopted as a legal standard (DR-0008).

**Quarantine**
Storage holding for newly collected material before it is admitted into
the archive proper, pending checks (e.g., security scanning). Undischarged
quarantine copies factor into the project's storage/duplication accounting
(see `storage/measure.py`, A7).

**Acquisition source vs. original publisher**
A distinction this project always keeps: bytes recovered *from* an
external archive (e.g., the Wayback Machine) record that archive and its
capture time, separately from the original publisher and its own
publication time (record §28).

**Two-system write / storage-first**
The rule that a preserved object is written to storage (OCFL) *before* its
corresponding database rows are written, so an orphaned storage object is
detectable, rather than a database row pointing at bytes that do not exist
(record §26).

## Data model and epistemics

**CIDOC CRM**
An ISO-standard conceptual model for cultural-heritage information, adopted
conceptually for this project's "historical world" layer — the layer
describing people, events, and things in the world, as distinct from the
pipeline that handles preservation (DR-0010).

**LRMoo**
IFLA's Library Reference Model, object-oriented — adopted conceptually
here to model "documentary identity" (what makes two captures the same
work) (DR-0011).

**Pipeline layer vs. world layer**
The hard architectural boundary between the mechanics of preserving and
processing data (pipeline) and the historical claims that data supports
about people, organizations, and events (world) (DR-0004).

**Documentary assertion**
A claim recorded in the archive about the historical world (as opposed to
about the pipeline's own handling of bytes). Collection and preservation
create zero of these; only Gate 2/Gate 3 human review does (DR-0066).

**Evidence relation**
A structured link connecting a documentary assertion to the material that
supports it. Like documentary assertions, these are never created
automatically by collection (DR-0066).

**Source grade**
A triage-only quality signal attached to a source, used to prioritize
review — explicitly never read by any query that computes an assessment of
truth or reliability (DR-0027).

**Access tier**
A declared (not derived) level of who may see a given piece of preserved
or published material. Tiers are never computed from an ordering of other
properties (DR-0086).

**Redaction**
The sole exception to this archive's general immutability of preserved
content, used to remove or mask specific material after preservation
(DR-0077).

## Sanctions and compliance domain

**Sanctions authority**
A government or supranational body (e.g., the EU, OFAC, OFSI, BIS, SECO)
that publishes and maintains lists of sanctioned/designated persons,
entities, or vessels. This project treats each authority's published list
as a distinct source to register and collect.

**Consolidated list**
A sanctions authority's single, merged list of all currently designated
persons/entities under its regime (e.g., the "EU Consolidated List", the
UK's "OFSI Consolidated List"). Distinguished from partial or
program-specific lists.

**SDN (Specially Designated Nationals)**
OFAC's (U.S. Treasury) primary sanctions list — one of this project's two
currently registered sources (`ofac-sdn`).

**Designation**
The act by which a sanctions authority formally adds a person, entity, or
vessel to a sanctions list, typically citing a legal instrument or decision
as its basis.

**Denied Persons List**
A specific BIS (U.S. Bureau of Industry and Security) export-control list,
distinct from BIS's broader Entity List; this project's `bis-entity-list`
registration currently covers only this narrower list, not the full Entity
List.

**Registered source**
A locator that has passed through this project's registration process
(schema in DR-0067) and is recorded in `sources/`. Per DR-0071(a), only
registered, active sources may be collected from — an unregistered locator
is out of policy, not merely unverified.

**Source candidate**
An entry in `sources/candidates/*.yaml` describing a not-yet-registered
source and the reasoning for its proposed configuration. Registering a
candidate is a founder act, per source.

## Suggested next terms

The categories above are a starting set. Candidates not yet included, in
case they're wanted:
- Specific epistemic-layer terms from DR-0024/DR-0025 (e.g., "epistemic
  vocabulary", "two-dimensional uncertainty")
- IIIF, TEI, CSL (adopted per DR-0020/DR-0021/DR-0022 but not yet defined
  here)
- POL-0001-specific terms (e.g., "material change", "review trigger")

Say which (if any) to add, or flag any definition above that needs
correction.
