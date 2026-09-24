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
from interpretation, and the reason "we collected it" never quietly
becomes "we're claiming it's true":
- **Gate 1** — admitting quarantined material into the archive as
  preserved bytes. Creates zero documentary assertions and zero evidence
  relations by itself (DR-0066, Principle 5).
- **Gate 2** — a human decision to *structure* preserved material into
  documentary assertions and evidence relations (`editorial/gate2.py`).
- **Gate 3** — a human decision to *publish* structured material for a
  given access tier (`publication/gate3.py`).
Each gate is a separate, accountable human decision at a declared risk
tier — never automated, and never skipped by an earlier gate's approval.

**Semantic registry**
The project's controlled vocabulary store (record §101) — where
enumerated terms like the epistemic vocabulary (DR-0025) or the
absence-state vocabulary (DR-0029) are formally defined, including
multilingual labels, so the same term means the same thing everywhere in
the archive. Changes happen only by Decision Record, never by editing a
label ad hoc. Implemented as `registry/` in this codebase, with enum SQL
generated from it (`schema/gen_enums.py`, DR-0078).

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
time (DR-0001). OAIS is the "why" behind many of the terms below: it
defines the roles (producer, archive, consumer) and packages that a
long-term digital archive needs, independent of any specific technology.

**SIP / AIP / DIP**
Three package types from OAIS describing the same content at different
stages of its life in the archive: a **Submission Information Package**
(what a producer hands over), an **Archival Information Package** (what
the archive actually stores and preserves long-term, with full metadata),
and a **Dissemination Information Package** (what a consumer receives when
they access it). This project's quarantine-to-Gate-1 flow is, in effect,
turning submissions into SIPs and then AIPs.

**Designated community**
An OAIS concept: the specific audience an archive commits to keeping
content understandable and usable for (e.g., future historians and
researchers, not the general public today). It shapes how much context
and format-migration effort preservation requires.

**PREMIS**
The preservation-metadata vocabulary (v3.0) used to record events like
fixity checks, migrations, and ingestion (DR-0002). PREMIS organizes
everything around five entity types: **objects** (the digital things being
preserved), **events** (fixity checks, migrations, ingestion — things that
happen to objects), **agents** (who or what caused an event — a person,
organization, or piece of software), **rights** (permissions governing an
object), and **relationships** (links between any of the above, e.g. "this
object derives from that one").

**PROV**
The W3C provenance vocabulary used across the pipeline to record
derivation and agency — who or what produced or acted on a given object
(DR-0003). PROV's three core building blocks are **entities** (things:
files, documents, records), **activities** (processes that use or produce
entities: a collection run, a transcription), and **agents** (who or what
was responsible: a person, an organization, or software) — closely
mirroring PREMIS's own object/event/agent split, since both standards
describe the same kind of "what happened, and who did it" history.

**Pipeline agent**
An agent (person, organization, or software) recorded because it *acts on*
the archive — e.g., a collector run's software agent, or the human agent
of record for a collection run. Kept in a registry separate from world
actors (DR-0059); confidential as a whole, because it may include people
acting on behalf of a confidential source (DR-0092, SEC-001).

**World actor**
A historical person or group the archive holds information *about* — as
opposed to a pipeline agent, which acts *on* the archive. Kept in a
separate registry from pipeline agents so that queries about the world
can never accidentally expose confidential pipeline-agent data (DR-0059).

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

**Archive server**
The one machine that holds the archive itself: the PostgreSQL database
(`uiw`) and the OCFL storage roots. It is hosted with IONOS in Spain
(DR-0100). GitHub holds only code and documents, and AI sessions never
touch this machine. Every command run on it so far was run by the founder.
See `docs/infrastructure.md`.

**Schema drift**
When a live database's table structure falls behind the DDL files in
`schema/` on `main`, so newer code expects columns or tables that do not
exist yet. This project rebuilds databases from DDL instead of migrating
them, so drift on a database with real data is fixed by backing up,
rebuilding and reloading (DR-0105 *Executed*), not by running a migration.

**Restore test**
Actually restoring a backup somewhere and checking that it is complete,
rather than only taking the backup. OPS-005 requires one a year. A backup
that has never been restored is not yet known to work.

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

**Quarantine (quarantine zone)**
A holding area explicitly *outside* the archive proper, where every newly
acquired file lands first — whether fetched automatically or submitted by
a third party — before Gate 1. While quarantined, material gets malware
and format checks, and its provenance and privacy/legal exposure are
assessed; critically, **none of the archive's integrity guarantees apply
to it yet**. Undischarged quarantine copies (material sitting in
quarantine rather than admitted or discarded) factor into the project's
storage/duplication accounting (`storage/measure.py`, A7; DR-0069).

**Submitter claim**
When material is submitted by a third party (rather than collected
automatically), whatever that person says about it (where it came from,
when, etc.) is kept as a labeled *claim*, stored separately from anything
the project itself later concludes about the material — so a submitter's
story is never confused with an established project finding (DR-0069).

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
or published material — e.g., `public`, `researcher-restricted`,
`investigator-restricted`, `confidential`, `private-preservation`,
`internal`, `subscriber`. Tiers are never computed from an ordering of
other properties (DR-0086).

**Tier restrictiveness (most-restrictive-governs rule)**
When more than one access tier could apply to the same content (e.g., an
object referenced by both a public holding and a subscriber-only one),
the **most restrictive tier always governs** — but which tier is "more
restrictive" must be an explicit, declared ranking, never inferred from
alphabetical order or enum-declaration order. A real 2026-08-26 bug
(`export/tiers.py` using `min()` over tier text) let a confidential object
resolve to `public` by alphabetical accident, which is exactly the failure
DR-0086 exists to prevent.

**Split (disambiguation record)**
An editorial act of separating out material that had been wrongly merged
under one identity (e.g., two different people conflated as one). The
record of that decision names a deciding agent, but — because pipeline
agents are confidentiality-sensitive as a whole — the public-facing record
shows only a **snapshotted public title/role** for that agent, never the
underlying agent record itself, so an editorial act stays inspectable
without risking exposure of a confidential agent's identity (DR-0089,
DR-0092).

**Redaction**
The sole exception to this archive's general immutability of preserved
content, used to remove or mask specific material after preservation. It
requires a recorded decision citing its legal ground, the content actually
purged, and a preservation event plus **tombstone** left behind recording
that something was removed, when, by what authority, and why — without the
removed content itself (DR-0077).

**Tombstone**
A permanent marker left in place of redacted content, so the archive can
show *that* something was removed and *why*, without keeping the removed
material itself (DR-0077).

**Immutability**
The general rule that once content is written into archival storage
(OCFL), it is never altered or deleted — the guarantee that lets anyone
verify later that a preserved file is exactly what was captured. Redaction
is the one governed exception (DR-0077).

**Web Annotation (W3C Web Annotation Data Model)**
The standard this project uses to point precisely at a piece of preserved
content — a paragraph, an image region, a video interval — rather than
just linking to a whole document. An annotation has a **body** (the
comment or claim) and a **target** (the thing being annotated), with the
target refined by a **selector** (e.g., quote the exact text, or give
pixel coordinates) so the same spot can be found again even if formatting
changes (DR-0017).

**Anchoring rule**
This project's rule that any annotation used as evidence must target a
*preserved* capture held by the archive — never a live URL alone — because
live web pages can silently change or disappear. A live URL may be
recorded as context, but preservation always comes before evidential
annotation (DR-0018).

**Source dependence / independence**
This project's discipline of never assuming that two sources repeating the
same claim are independent confirmation of it — most "corroboration" is
actually one source being copied, cited, or reposted by others.
Dependence is recorded as a typed relationship (cites, reposts, syndicates,
derives-from, shares-underlying-document, shares-underlying-witness,
common-evidentiary-origin), and a source counts as an independent
confirming line only when the *absence* of such a relationship has
actually been researched and established — never assumed by default
(DR-0028). This independence count feeds directly into analytic confidence
(see "Two-dimensional uncertainty").

**Absence-state vocabulary**
A set of specific labels for "we don't have a value here" that avoid the
single ambiguous meaning of a blank/null field: **unknown,
not-researched, no-evidence-found, unavailable, withheld, redacted,
lost-or-destroyed, not-applicable, indeterminate**. The point is that a
missing value must never be silently read as "no" — e.g.,
"no-evidence-found" (we looked, in a stated way, and found nothing) is a
completely different, and equally recordable, fact from "not-researched"
(we haven't looked yet) (DR-0029).

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

## Epistemic layers and vocabulary (DR-0024, DR-0025, DR-0026)

**Six-layer epistemic architecture**
The project's structure for keeping facts, sources, and judgments distinct:
(1) world layer, (2) documentary assertions, (3) evidence relations, (4)
project assertions, (5) epistemic assessments, (6) arguments. Being present
in the corpus never implies being evidentially used (DR-0024, Principle 5).

**Project assertion**
A belief held by the project or a named analyst, produced by visible
inference and held under human accountability (record §79) — distinct from
a documentary assertion, which is owned by its source, not the project
(DR-0024 layer 4).

**Epistemic assessment**
A versioned status/likelihood/confidence judgment attached to an assertion.
Prior states are never rewritten — a changed assessment is a new version,
not an edit (record §63; DR-0024 layer 5).

**Epistemic vocabulary v1**
The six controlled categories an assertion in this system may carry:
**observation, claim, assessment, hypothesis, finding,** and **project
conclusion**. Every assertion carries exactly one; the set changes only by
Decision Record (DR-0025).

**Finding**
One of the v1 epistemic categories. Includes *negative* findings (record
§76) as first-class — the project stating that something was looked for,
with a stated scope and method, and not found — not merely an absence of
data.

**Two-dimensional uncertainty**
This project's rule that probability and confidence are kept as two
separate, never-collapsed dimensions on a judgment (DR-0026):

- **Likelihood** — an ordered scale of verbal probability expressions
  (e.g., ICD 203/PHIA-style), each bound to an explicit numeric range.
- **Analytic confidence** — low/moderate/high, derived from evidence
  quality, corroboration, and reasoning strength — never a bare numeric
  score, and never averaged across contradictory assessments.

## Adopted standards not yet in wide use (DR-0020, DR-0021, DR-0022)

**TEI (TEI P5)**
The Text Encoding Initiative's scholarly text-encoding standard. Adopted
here only *selectively* — deep TEI encoding (variant readings, damage,
editorial apparatus) is reserved for high-value transcripts and critical
editions, with the project's specific subset defined only once such a
corpus exists, not speculatively (DR-0020). Routine transcripts stay plain
derivative expressions with PROV lineage instead.

**IIIF**
The International Image Interoperability Framework (Presentation API
3.0), used for region/interval annotation and delivery of image and audio/
video evidence. Must be formally evaluated before this project's media
delivery platform is designed; adoption is deferred to that point, and no
media-delivery decision may bypass the evaluation (DR-0021). Composes
natively with the Web Annotation vocabulary this project already uses
(DR-0017).

**CSL (Citation Style Language)**
The standard adopted for *rendering* citations at the presentation layer,
driven by documentary-layer metadata — so citation formatting can change
(e.g., a different house style) without touching the canonical citation
data underneath (record §61; DR-0022).

## POL-0001-specific terms

**Material change**
Under POL-0001 §11, any change to collection scope, jurisdiction, or
applicable law — explicitly including incorporation as a legal entity, or
a change to the establishment jurisdiction or hosting country — that
triggers a recorded policy review, rather than a silent update.

**Review trigger**
A named, specific condition (e.g., "the start of Gate 3 work," a material
change under §11) that a Decision Record records as the point at which a
held-open question or a policy section must be revisited — as opposed to
an open-ended "review later," which this project avoids (see DR-0101's
"recorded" act, and the founder's 2026-09-15 ruling that named review
triggers must be recorded per §9.4/§8 of the legal-review brief).

**CRMinf**
The argumentation extension of CIDOC CRM (argumentation activities,
beliefs, proposition sets, belief adoption, inference-making), named as
this project's starting *candidate* for the epistemic/argumentation layer
(layer 6 of the six-layer architecture) — a study commitment, not yet an
adoption (DR-0016).

**Document status vocabulary (DR-0046)**
The controlled lifecycle states every governance document (DR, SPEC, POL,
REQ, METH, PROC) moves through, always as explicit metadata rather than
inferred from Git: **draft → proposed → approved → effective → superseded
/ withdrawn**. Approval authority and date, effective date, and
supersession links are recorded alongside the status itself.

## Suggested next terms

The sections above now cover governance/process, archival/preservation
(including OAIS package types and PREMIS/PROV entity models), data
model/epistemics, sanctions domain, epistemic vocabulary, the
selectively-adopted standards (TEI/IIIF/CSL), POL-0001-specific terms,
security/access/redaction, source-dependence and absence-state
vocabularies, and quarantine/gate/split mechanics. Smaller candidates
still not included, purely because they're referenced only in passing so
far:
- DataCite (dataset-release citation identifiers, mentioned in DR-0022's
  consequences but not yet used)
- Specific identifier/resolver vocabulary from `identifiers/` and
  SPEC-0007 (e.g., how public identifiers resolve to internal records)
- METH-0001's evidentiary-method-specific terms, if any come up while
  reading it

This glossary is meant to grow with your own reading — if something in a
DR, SPEC, or POL confuses you, that's a good sign it belongs here. Just
name the term or the document and it can be added.
