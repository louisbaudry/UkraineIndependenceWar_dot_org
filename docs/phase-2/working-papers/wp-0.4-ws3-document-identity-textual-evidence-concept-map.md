# Phase II / Workstream 3 — Document Identity & Textual Evidence Concept Map
## Working Paper 0.4

**Project:** Ukraine's Second War of Independence
**Status:** CANDIDATE — AI-drafted, awaiting founder review and approval. Nothing in this paper is canonical.
**Version:** 0.4 (first draft of Workstream 3)
**Mandate:** WP 0.1 research sequence item 3 — IFLA LRM/LRMoo, TEI, Web Annotation for document identity and textual evidence.
**Constraints inherited:** DR-0004 (layer boundary), DR-0011 (LRMoo documentary identity), DR-0003 (PROV derivation), DR-0012 (identification as events).

### AI provenance (per Phase I record §80)

| Field | Value |
|---|---|
| Drafted by | AI assistant (Anthropic Claude Code agent session), at the founder's direction to continue the workstream sequence |
| Date | 2026-08-11 |
| Inputs | Phase I record; WP 0.1–0.3; DR-0001…0016; web verification of current TEI release status (sources at end) |
| Human review | **Pending** — founder is final editor (record §78) |
| Disposition | Candidate working paper; all candidate Decision Records herein are proposals |

---

## 1. Scope and method

DR-0011 already fixes the documentary identity stack (Work / Expression /
Manifestation / Item). This workstream maps what sits *on top of* that stack:
how the project points at, quotes, transcribes, translates, contextualizes, and
cites **exact passages and regions** of sources — the textual-evidence machinery
required by record §15, §23–§27, §58–§59, and the evidence-targeting needs of §29.

Standards studied: **W3C Web Annotation** (Data Model / Vocabulary / Protocol,
W3C Recommendations 2017), **TEI P5** (Guidelines, current release line 4.x —
4.12.0 as of July 2026), **IIIF** (Presentation API 3.0, image/AV canvases and
regions), **CSL** (citation rendering), with **Memento (RFC 7089)** concepts
carried over from WP 0.2 for capture series.

## 2. Conceptual cores

### 2.1 W3C Web Annotation

An annotation is a typed link with a **body** (the note, tag, or assertion) and
one or more **targets** — where a target is not just a resource but a resource
**plus a selector** refining it to an exact segment:

- **TextQuoteSelector** — exact text with prefix/suffix context (robust to
  reflow; survives markup changes);
- **TextPositionSelector** — character offsets (precise but fragile);
- **FragmentSelector** — including W3C Media Fragments for **audio/video
  time intervals** (§59's timecodes);
- **SvgSelector / geometric selectors** — image regions;
- **XPathSelector** — structured-document nodes;
- **State** specifiers — *which version* of the target (time-stamped state) —
  directly relevant to §24's "the same URL may later serve different content."

Selectors can be **combined for redundancy** (quote + position), which is the
established mitigation for anchor fragility.

### 2.2 TEI P5

The scholarly standard for deeply encoded text: diplomatic transcription,
editorial interventions, gaps/illegibility, named-entity and date markup,
manuscript/document description, critical apparatus for **variant readings** —
mature machinery for exactly the distinctions §59 requires (omissions marked,
transcription origin recorded, editorial context preserved). Cost: heavy;
WP 0.1 already set the disposition to **selective adoption**. Current release
line is 4.x (4.9.0 "Atocha" Jan 2025; 4.12.0 as of July 2026), stable and
actively maintained.

### 2.3 IIIF (Presentation API 3.0)

Canvas-based presentation of images and (since 3.0) audio/video, with
annotation of regions and intervals **using the Web Annotation model** — the two
compose by design. Relevant to §21 (photographs, component identification
regions), §48 (imagery observations), and public media delivery. Also relevant:
IIIF is delivery/presentation infrastructure, not evidence semantics.

### 2.4 CSL

Citation Style Language: rendering citations from structured metadata in
thousands of styles. Cleanly separates citation *data* (documentary layer) from
citation *presentation* (record §61's semantics-vs-wording split).

## 3. Requirement mapping

### 3.1 Quotation provenance (§59)

The §59 checklist — exact original-language passage, exact source version,
page/paragraph/timecode/offset, translation, transcription/OCR origin,
editorial context, omissions — maps onto:

- **passage + locus** → Web Annotation target: preserved expression +
  selector(s), with media fragments for A/V;
- **exact source version** → target State + the preserved capture (WP 0.2);
- **translation** → parallel expression (DR-0011) linked at passage level by an
  alignment annotation;
- **transcription/OCR origin** → PROV derivation on the transcript expression
  (DR-0003);
- **omissions/editorial context** → TEI-style markup where the material warrants
  deep encoding; annotation body metadata otherwise.

"Do not manufacture quotations from paraphrases" is not expressible in any
standard — it is a discipline rule and belongs in a candidate DR (below).

### 3.2 Anchoring and the live-web problem (§24, §29)

An annotation targeting a **live URL** silently decays as content changes. For
evidential use this is unacceptable: the anchor must hold to *what the project
preserved*, not to what the URL serves today. The composition already adopted
makes the fix natural: evidential annotations target **preserved
captures/expressions in the archive** (the LRMoo item / PREMIS representation
bridge of WP 0.3 §4), optionally recording the live-web origin as context. This
is the single most consequential rule in this workstream and is proposed as a
candidate DR.

### 3.3 Translations and parallel text (§58)

Translations are expressions (DR-0011) with PROV derivation identifying
translator/provider, human-vs-machine, version, and the exact source expression
translated. Passage-level parallelism (needed for §59 quotation pairs and for
terminology work, §60) is expressible as alignment annotations linking loci in
two expressions. Quotation, paraphrase, and summary remain distinct *types* of
annotation body — never collapsed.

### 3.4 Source context and threads (§25)

Reply chains, forwards, nearby posts, linked material: typed documentary
relations between manifestations/expressions, preserved as inexpensive
structural context at capture time. This resolves WP 0.3 §8 Q7 as follows
(candidate): **accounts** are actor identifiers assigned by events (DR-0012);
**posts** are manifestations (platform embodiment) of expressions;
**reply/forward/quote-post/thread membership** are typed relations in the
documentary layer; **capture series** of a changing post follow the Memento
pattern (WP 0.2 §4.5). Richer contextual packages for important evidence (§25)
are evidence-package territory (DR-0007).

### 3.5 Holdings, completeness, accessibility (§26–27)

What the archive holds of a document — original, archival copy, derivative,
screenshot, transcript, fragment, metadata-only — is a typed statement about
**items and derivative expressions**, never an implied property. Fragments carry
their locus within the whole (a selector, again). Accessibility states (§27:
public, paywalled, deleted, archived…) are temporal statuses of
manifestations/sources in the documentary layer, distinct from the archive's own
access tiers (§12) — a distinction for the conflict register.

### 3.6 Citation (§15)

Meaningful research objects — including quotations and source captures — need
stable citable identity. The documentary machinery here supplies the *targets*;
identifier syntax and resolvers remain a Phase III/infrastructure matter (§15
warns against freezing custom identifier syntax early). CSL renders citations at
the presentation layer from documentary metadata; adopting it costs nothing now
and honors §61.

## 4. Candidate conflict-register entries (additions)

| Term | Colliding senses | Resolution direction (candidate) |
|---|---|---|
| **annotation** | W3C Annotation (typed body+target link) vs editorial note vs TEI markup | Registry: "annotation" unqualified = W3C sense; editorial notes and TEI encoding named as such |
| **fragment** | Holdings fragment (§26, partial possession) vs FragmentSelector (locus syntax) | Qualify: "holdings fragment" vs "fragment selector" |
| **transcription / transcript** | TEI diplomatic transcription vs A/V transcript vs OCR output | Three derivative types with distinct PROV method vocabularies |
| **accessibility** | Source accessibility (§27, world/documentary) vs archive access tier (§12, project policy) | Never share a field; separate vocabularies |
| **canvas** | IIIF canvas (presentation surface) vs colloquial | IIIF-scoped term only |
| **version** (extended) | Target State (annotation anchoring) added to the senses in WP 0.2 §5 | Fold into the existing "version" register entry |

## 5. Candidate Decision Records (proposals only — require founder approval)

- **CDR-W3-1:** Adopt the **W3C Web Annotation Data Model** as the targeting
  vocabulary for passages, image regions, and A/V intervals — the mechanism by
  which assertions, quotations, and research notes point at exact source
  segments (record §59, §29; WP 0.1 layer E).
- **CDR-W3-2:** **Anchoring rule:** evidential annotations target preserved
  expressions/captures held by the archive — never a live URL alone — with
  selector redundancy (quote + position where applicable) and version-pinned
  targets (State). Live-web origin may be recorded as context.
- **CDR-W3-3:** **Quotation discipline:** a project quotation is an annotation
  carrying the exact original-language passage, exact source version, locus,
  linked translation (if any), transcription/OCR derivation, and marked
  omissions. No quotation is minted from a paraphrase or summary; quotation,
  paraphrase, and summary are distinct types (record §58–59).
- **CDR-W3-4:** **TEI P5 selective adoption:** deep TEI encoding is reserved for
  high-value transcripts and critical editions where variant readings, damage,
  or editorial apparatus matter; the project TEI subset is defined when the
  first such corpus is processed, not in advance. Routine transcripts remain
  plain derivatives with PROV lineage.
- **CDR-W3-5:** **IIIF study:** evaluate IIIF Presentation 3.0 for image/AV
  region annotation and public media delivery before the media platform is
  designed; adoption deferred until then. (Composes natively with CDR-W3-1.)
- **CDR-W3-6:** **Adopt CSL** for citation rendering at the presentation layer,
  driven by documentary-layer metadata (record §15, §61).
- **CDR-W3-7:** **Social-media structural mapping:** accounts are actor
  identifiers assigned by events (per DR-0012); posts are manifestations of
  expressions; reply/forward/quote-post/thread membership are typed documentary
  relations captured as inexpensive structural context (§25); capture series
  follow the Memento pattern. (Resolves WP 0.3 open question 7.)

## 6. Unresolved research questions (feed Phase II output 7)

1. Annotation identity and storage: are annotations first-class citable objects
   with stable IDs (§15), and what resolver serves them? (Phase III.)
2. What is the minimal TEI subset for the first deep-encoded corpus, and which
   corpus triggers it?
3. Alignment granularity for parallel translations: sentence, passage, or
   ad hoc loci?
4. Does non-public media (restricted graphic evidence, §10) use IIIF
   infrastructure with access control, or a simpler internal region model?
5. How do annotation bodies relate to the epistemic layer — is an evidential
   annotation itself an assertion with epistemic status? (WS4 must answer; the
   targeting vocabulary is deliberately status-neutral.)
6. Propaganda-narrative variant linking (§54): annotation-based, or a dedicated
   narrative-variant model? (WS4/5 with this workstream's tools.)

## 7. Sources

- Web Annotation: W3C Recommendations (Data Model, Vocabulary, Protocol), 23 Feb 2017
- TEI: [TEI Guidelines](https://tei-c.org/release/doc/tei-p5-doc/en/html/); [P5 Guidelines page](https://tei-c.org/guidelines/p5/); [4.10.2 patch release note](https://tei-c.org/news/2025/09/04/patch-release-tei-guidelines-4-10-2/); [Zenodo archive of releases](https://zenodo.org/records/14745421)
- IIIF: Presentation API 3.0 (iiif.io)
- CSL: Citation Style Language 1.0.2 (citationstyles.org)
- Memento: RFC 7089
