# SPEC-0003 — Collection Pipeline Architecture

**Class:** SPEC (DR-0046 control) | **Version:** 0.1 | **Status:** Draft — proposed
**Approval:** pending founder review | **Effective:** upon approval
**Supersedes:** — | **Superseded by:** —
**Governed by:** record §8–§13, §26–§28, §57; DR-0003 (PROV), DR-0005 (fixity), DR-0006 (WARC), DR-0055 (append-only), DR-0060 (PREMIS subset), DR-0061 (holding), DR-0063 (matchers propose only), DR-0027 (grades triage-only), SPEC-0001, SPEC-0002; requirements OPS-001/006, PRES-005/007/011, SEC-002, LEGAL-009.

### AI provenance (record §80)

Drafted 2026-08-16 by an AI assistant (Anthropic Claude Code agent session)
at the founder's direction. Candidate until approved.

---

## 1. Scope

The architecture of automated and manual collection: the source registry,
the stage model and its gates, quarantine, retention decisions, the AI
enrichment boundary, editorial acceptance, and coverage accounting.
**Not in scope:** collector implementations per source type, scheduler
technology, matcher internals (implementation specs).

## 2. The stage model and its three gates

Record §8's stages, with the gates that make "collection never implies
publication" (OPS-001) structural rather than procedural:

```
  discovery → acquisition → [QUARANTINE] → GATE 1: preservation
      → preserved holding → normalization → enrichment → classification
      → GATE 2: editorial acceptance → canonical knowledge
      → GATE 3: publication decision → published surface
```

**Gate 1 — Preservation.** Does this acquired item become an archival
object, and at what retention tier (§4)? Passing requires: security checks
cleared, fixity computed (DR-0005), acquisition provenance recorded. Items
may fail Gate 1 and still leave a permanent trace (a recorded acquisition
event with its outcome — including refusals and failures, §28/PRES-007).

**Gate 2 — Editorial acceptance.** Does anything extracted from this item
become canonical knowledge? Nothing crosses on automated confidence alone:
extractions and matches arrive as proposals (DR-0063, AI-001) and become
canonical only by human acceptance at the risk tier the content demands
(§78). Material can be permanently preserved and never cross Gate 2 —
that is the normal case for bulk collection.

**Gate 3 — Publication.** Does accepted knowledge, or a preserved item,
appear on a public surface, and at which access tier (§12)? Preservation
status and access status remain independent (Principle 11).

Every stage transition is a PROV activity (DR-0003) with its collector or
agent, inputs, outputs, and version; the pipeline is **restartable and
idempotent** — re-running a stage produces a new derivative with new
provenance, never an in-place mutation (DR-0055).

## 3. The source registry

Collection is driven by a configurable registry (§8, OPS-001). Each source
entry carries:

| Field group | Content |
|---|---|
| Identity | Stable ID; names; URLs/handles/feeds; publisher or operator; type (government, official Russian/Ukrainian, IO, media, investigative, think tank, NGO, social/Telegram, video, dataset, court/prosecutor, sanctions authority) |
| Context | Jurisdiction; primary language(s); coverage start; description of what the source publishes |
| Collection policy | Method (feed, API, crawl, WARC capture, manual deposit); cadence; scope rules and exclusions; politeness/rate constraints; authentication needs |
| Preservation policy | Capture format per DR-0006 (WARC for high-value; lighter forms recorded honestly per §26); retention tier default (§4); fixity cadence |
| Access & sensitivity defaults | Default access tier and sensitivity (§12) for items from this source; graphic-content expectation (§10) |
| Rights | Rights assessment per §14 (may preserve / display / redistribute / provide to subscribers / unknown) — unknown is an explicit value (DR-0029) |
| Triage grade | Optional Admiralty-style source grade — **triage only** (DR-0027), never propagating to truth |
| Declared dependence | Known dependence on other sources (aggregates, syndicates, mirrors, republishes) per DR-0028 — declared at registry level, not only discovered per item |
| Lifecycle | Active/paused/retired with reasons and dates; outage history |

**Declared dependence at registry level** is a deliberate addition: when an
aggregator is known to republish an outlet, every item inherits a dependence
hypothesis rather than requiring rediscovery per article (§36).

## 4. Retention tiers (§9, PRES-011)

Every acquired item receives a retention decision at Gate 1, from the
source's default, revisable upward:

| Tier | Meaning |
|---|---|
| `discard` | Not retained; the acquisition event and its outcome are still recorded |
| `metadata-only` | Descriptive record retained; content not stored (rights, sensitivity, or volume) |
| `medium-term` | Retained with a review date, then re-decided |
| `permanent` | Archival preservation under full OAIS/PREMIS treatment |

Tiers escalate, never silently downgrade: a downgrade is a governed
disposition decision with a recorded rationale. Fragile or high-value
sources may be collected at `permanent` before item-level relevance is
known (§9), and a source's escalation may trigger retrospective recovery
from external archives.

## 5. Quarantine and intake (§11, SEC-002)

Acquired material — especially third-party submissions — lands in a
**quarantine zone that is not part of the archive**: files are held with
their original bytes and submission metadata, scanned (malware/format
checks), and assessed for provenance and legal/privacy exposure before Gate
1. Archive integrity guarantees are never claimed for quarantined material.

For third-party submissions specifically: **submitter claims are preserved
separately from project conclusions** (§11); confidential submitter identity
lives in the separable confidential store (SEC-001, DR-0059's pipeline-agent
separation), referenced by pseudonymous submitter ID.

## 6. Normalization and enrichment — the AI boundary

Normalization (text extraction, transcoding, language detection) and
enrichment (entity/date/place extraction, translation, summarization,
classification) run automatically and produce **derivative expressions and
proposals only** (DR-0011, AI-001):

- Every derivative records its generator, model/version, parameters, and
  inputs (AI-002, DR-0003).
- Extracted entities produce **proposed** match assertions (DR-0063), never
  canonical entities.
- Relevance classification produces triage signals that route items to
  review queues; classification never accepts or rejects on its own.
- **Structural context is captured cheaply at acquisition** (§25, DR-0023):
  reply chains, forwards, thread membership, engagement counts where
  available — before they disappear.

## 7. Editorial acceptance (Gate 2)

Review queues are ordered by triage signals (source grade, classifier
confidence, topical priority) — ordering only, never acceptance. Acceptance
records: the accepting agent, the risk tier applied, what was accepted
(which proposals became assertions), and what was rejected. Rejections are
retained (they are training signal and audit trail alike). Items may sit in
a queue indefinitely; queue depth and age are coverage metrics (§8).

## 8. Coverage, failures, and outages (§57, OPS-006, §28)

Each execution is a **collector run** (SPEC-0001) recording: source, start
and end, collector version and configuration, items discovered, acquired,
skipped (with reasons), failed (with errors), and bytes preserved. Runs
compose into per-source coverage statements: what was collected, from when,
with which gaps.

- **Failed acquisitions are first-class** (§28, PRES-007): retries, later
  successes, and permanent losses are all recorded events; historically
  significant failures are preserved permanently.
- **Outages and exclusions** are recorded so that "absent from the archive"
  never silently reads as "absent from the world" (§57, DR-0029).
- Coverage statements ship with releases (DR-0048).

## 9. The personal-data gate (LEGAL-009, §13, Q-35)

Record §13 requires a formal personal-data policy **before broad automated
collection**. Until that POL document is effective, this SPEC permits only:

- collection from **explicitly registered sources** with human-configured
  scope — no open-ended crawling, no bulk social-media harvesting;
- **no automated extraction of personal data into structured, searchable
  fields** beyond what a registered source's purpose requires — raw material
  may contain personal data (it inevitably will); the enrichment pipeline
  must not automatically promote it into queryable structure (§13);
- **no third-party submission intake at scale** beyond individually handled
  cases.

These constraints lift when the personal-data policy takes effect, on that
policy's terms.

## 10. Candidate Decision Records (proposals — require founder approval)

- **CDR-P3-13:** Adopt the **three-gate pipeline model** (§2): preservation,
  editorial acceptance, and publication as distinct gates, each with its own
  criteria and record; stage transitions are PROV activities; re-runs
  produce new derivatives, never mutations.
- **CDR-P3-14:** Adopt the **source registry schema** (§3), including
  per-source preservation, access, sensitivity, and rights defaults, and
  **registry-level declared dependence** (DR-0028).
- **CDR-P3-15:** Adopt the **four retention tiers** (§4) with
  escalate-freely / downgrade-only-by-governed-decision semantics.
- **CDR-P3-16:** Adopt **quarantine as a pre-archival zone** (§5): archive
  guarantees are never claimed for unvetted material; submitter identity is
  architecturally separable; submitter claims stay distinct from project
  conclusions.
- **CDR-P3-17:** Adopt the **collector-run coverage record** (§8) as the
  unit of coverage accounting, with failures, skips, and outages first-class
  and coverage statements shipped with releases.
- **CDR-P3-18:** Adopt the **interim personal-data constraints** (§9) as
  binding until a personal-data POL document is effective: registered
  sources only, no automatic promotion of personal data into structured
  fields, no at-scale submission intake.

## 11. Open questions raised

1. Scheduler and queue technology; per-source politeness enforcement
   (implementation).
2. Telegram and other platform-specific acquisition constraints — legal and
   technical (§8's "where lawful and appropriate").
3. Whether medium-term retention review is calendar-driven or
   volume-driven.
4. Deduplication semantics: identical bytes vs same intellectual content
   across sources (interacts with SPEC-0001 holdings and DR-0028).
5. The personal-data policy itself (Q-35) — POL class, founder-led.

## 12. Sources

Record §8–§13, §25–§28, §57; DR-0003/0005/0006/0011/0018/0023/0027/0028/
0055/0059/0060/0061/0063; SPEC-0001, SPEC-0002; Berkeley Protocol
collection and preservation guidance (per DR-0008).
