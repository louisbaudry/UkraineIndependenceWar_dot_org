# Phase III / Study 6 — WACZ Evaluation
## Working Paper 3.6

**Project:** Ukraine's Second War of Independence
**Status:** CANDIDATE — AI-drafted, awaiting founder review.
**Version:** 3.6
**Mandate:** DR-0006's standing task — "before the capture toolchain is frozen, WACZ (packaged, cryptographically signable web-archive collections) must be evaluated, including the maturity and jurisdictional meaning of its signing" — and WP 0.2 §8 Q4 / Phase II output 7 Q-04, carried forward unresolved since 2026-08-10. WP 3.4 Track A item A4 names this study's deliverable: "a short evaluation note; a candidate DR on WACZ adoption or deferral."
**Constraints inherited:** DR-0006 (WARC adopted for high-value capture; this study's precondition); §26 (capture form recorded honestly, lighter forms valid for lower tiers); §28 (acquisition source ≠ original publisher); §92 (evidence/research packages — WACZ and RO-Crate both surfaced as candidates by WP 0.2 §4.9, RO-Crate already "Study — high priority", WACZ "Study — high priority" for web-evidence packages specifically); DR-0008/LEGAL-007 (never claim legal chain of custody); DR-0005/0075 (fixity, digest verification on ingest); DR-0067 (registry's `capture_format` field already distinguishes `warc` from `http`, per source).

### AI provenance (record §80)

Drafted 2026-09-15 by an AI assistant (Anthropic Claude Code agent session)
at the founder's direction, as Track A item A4, one of three options put to
the founder and chosen. The WACZ container specification (v1.1.1) and the
WACZ signing/authentication specification (v0.1.0) were both retrieved and
read from their primary texts at `specs.webrecorder.net`, reachable from
this session's container. Reference-tooling maturity (`wacz`/py-wacz,
`authsign`, `wacz-signing`) was checked against live PyPI release metadata,
not from memory. No legal research was performed; the "jurisdictionally
meaningful" half of Q-04 is answered as *unanswerable from the specification
alone*, not resolved. Candidate until the founder approves it.

---

## 1. What DR-0006 actually asks, and why it is still open

DR-0006 (2026-08-10) adopted WARC for high-value web capture and made one
condition explicit: **WACZ must be evaluated before the capture toolchain
is frozen**, specifically covering "the maturity and jurisdictional meaning
of its signing" (WP 0.2 §8 Q4). No document in this repository has ever
declared the capture toolchain "frozen" as a governance act — a search of
every controlled document finds no such declaration. So DR-0006's literal
precondition was never *violated*. But `collector/pipeline.py` has been in
real production use since 2026-09-09 (DR-0093: five files, ~211 MB, on the
archive server), and every source registered since carries a
`capture_format` of `warc` or `http` (DR-0067) with no WACZ option in the
registry schema at all. **In substance, the toolchain has been de facto
committed to WARC for five weeks without this evaluation existing.** This
study exists to close that gap honestly, not to pretend the sequencing DR-0006
described was followed to the letter.

## 2. What was checked, from primary sources

Both governing specifications live at `specs.webrecorder.net` and were
fetched directly (not from training-data memory) on 2026-09-15:

| Specification | Version | Status (as stated in the document itself) |
|---|---|---|
| **WACZ** (container format) | 1.1.1 | *"This is a stable version of the WACZ standard and is in active use by the Webrecorder project."* |
| **WACZ Signing and Verification** | 0.1.0 | *"This document is a working draft for a proposal to create signed WACZ packages..."* |

The version numbers alone are a finding: the container is at a stable
`1.x`; the signing mechanism the DR-0006 question is actually about is at a
pre-1.0 `0.1.0`, and its own first line calls itself a *working draft for a
proposal* — not a specification the authors themselves consider settled.

Reference tooling, checked against live PyPI metadata (not the projects'
own claims about themselves):

| Tool | Latest version | Latest release date | Role |
|---|---|---|---|
| `wacz` (py-wacz) | 0.6.0 | 2026-09-10 | Creates/validates WACZ files (container only) |
| `authsign` | 0.6.1 | 2026-09-10 | Signing/verification server, implements the 0.1.0 draft |
| `wacz-signing` | 0.4.2 | 2025-02-12 | An older signing client library, last released over a year before this evaluation |

All three tools are still pre-1.0 by their own semantic versioning, which
is consistent with the specifications' own stated status: the container
format is stable enough that a 0.6.x tool implements it reliably; the
signing layer is still moving (`authsign` had a release five days before
this evaluation was written).

### 2.1 What the container format actually is

A WACZ is a ZIP file containing a WARC (or several), a CDXJ index, a
`pages.jsonl` manifest, and a `datapackage.json` manifest conforming to the
Frictionless Data Package specification — with per-file SHA-256 hashes
already required in that manifest, independent of any signature. Its
stated purpose, in its own words, is **portable browser replay**: "an
efficient way to dynamically load small amounts of data from a remotely
hosted file... without requiring the entire file to be downloaded" so that
tools like ReplayWeb.page and wabac.js can render archived pages directly
from a statically-hosted ZIP, via HTTP range requests into the ZIP's own
index. It is explicitly **not** a replacement for WARC — "WACZ is not
designed to replace other web archiving formats" — it is a distribution
wrapper around WARC files the project would produce anyway.

### 2.2 What the signing layer actually offers

The 0.1.0 draft defines two signature shapes, both stored in a
`datapackage-digest.json` alongside a hash of the manifest:

1. **Anonymous Signature** — an ECDSA keypair signs the manifest hash; the
   public key travels with the signature. The spec states plainly: *"To
   validate authorship of the WACZ, external key management is required,
   and this signature is otherwise anonymous."* No identity is asserted by
   the signature itself.
2. **Domain-Ownership Identity + Signed Timestamp** — the signature is made
   with the same private key backing a domain's TLS certificate (checkable
   via Certificate Transparency logs), plus an RFC 3161 timestamp from a
   timestamp authority. This is the stronger of the two: it proves *which
   domain's key* produced the WACZ and roughly *when*.

Both are bounded by the spec's own opening caveat: *"even TLS does not
provide non-repudiation."* The domain-identity scheme proves **who
packaged the file** (an organization controlling a given domain's TLS
key), not anything about the **original web content's** authenticity — the
spec says so directly: *"This proposal does not make any guarantees from
the perspective of the web server serving the content, as this is not
currently possible with HTTP/S."* A signed WACZ would prove this project
made the package, not that the sanctioned-entity list or court record
inside it is what the source publisher actually served — which is exactly
the gap `collector/pipeline.py`'s per-object SHA-256 digest and PREMIS-style
acquisition-attempt record (DR-0005, §28) already close by a different,
already-adopted mechanism.

## 3. Analysis against what the project actually needs

**Container packaging (WACZ proper).** The project's current need is
durable internal archival storage, which OCFL already serves (WP 3.3,
DR-0073…0077) — not portable browser replay of a subset of holdings, which
is the problem WACZ solves. Nothing about the project's present or planned
work (WP 3.4 Track A/B, the acquisition strategy) calls for handing anyone
a ZIP file that a browser extension renders. If the project later needs a
distributable, browser-replayable extract — for an investigator, a
journalist, a court, matching record §92's "evidence/research package" idea
— WACZ becomes directly relevant then, and adopting it is cheap **at that
point**: `_collect_one` already produces WARC records (DR-0006), so a WACZ
exporter would wrap already-correct data rather than requiring a change to
how anything is captured. Nothing about deferring WACZ now forecloses
adopting it later; the cost of waiting is close to zero.

**Signing.** The signing layer's value proposition — cryptographically
provable authorship and timestamp — is closest in spirit to precisely the
claim DR-0008/LEGAL-007 tell the project **not** to make: legal chain of
custody. The project's actual evidentiary discipline is different and
already built: per-object digests at ingestion (DR-0005), declared
WARC-Payload-Digest verification against archive-sourced records (DR-0075),
explicit acquisition-source-vs-publisher distinction (§28), and a recorded
preservation-event trail with a named agent (DR-0093 §3, the two-agent
split). None of that requires WACZ's signing layer, and none of it makes
the stronger claim WACZ signing gestures toward and its own spec disclaims
providing. Adopting an unstable, pre-1.0 signing mechanism now would add
real tooling and process cost (running `authsign` or equivalent, key
management, Certificate Transparency-linked domain identity for the
project's own domain) for a guarantee the project's own claims discipline
doesn't plan to rely on.

**The jurisdictional half of Q-04 is not answerable by this study.**
Whether a signature scheme is *jurisdictionally meaningful* — whether a
court or authority in a given legal system would treat a WACZ signature as
evidentially significant — is a legal question, not a specification-reading
one. Nothing in either fetched specification discusses any jurisdiction's
evidence rules, digital-signature statutes, or admissibility standards; the
question cannot be closed from the primary texts alone, at any level of
scrutiny this study could apply. This connects to, but is distinct from,
the A6 legal-review brief now naming France as the interim establishment
jurisdiction (`DR-pending-establishment-jurisdiction`) — whether to add a
sixth question to that brief about digital-signature evidentiary weight is
raised at §8 below, not decided here.

## 4. Alternatives considered

| Option | Why not (or why) |
|---|---|
| **A. Defer WACZ (container and signing) entirely; WARC via `collector/pipeline.py` remains the high-value format; revisit on stated triggers** | **Recommended.** Matches what the project already built and is already using in production; costs nothing now; the container layer stays cheap to add later since it wraps already-correct WARC data. |
| B. Adopt the WACZ container now as the high-value capture/storage format, replacing bare WARC-in-OCFL | Solves a problem (portable browser replay) the project does not have yet; adds a packaging step to every capture for no current consumer; OCFL already gives durable, versioned, fixity-checked storage (WP 3.3) — WACZ would sit awkwardly alongside it, not replace it, since WACZ is itself a ZIP of WARC files, not a storage layout. |
| C. Adopt WACZ container now, defer signing specifically | A narrower version of B with the same objection: no current consumer for the packaging, and it still doesn't resolve Q-04 (the question was always about signing's maturity, not the container's). |
| D. Adopt full WACZ including signing now, using the domain-identity scheme | Commits to a pre-1.0 draft specification and its reference implementation (`authsign` 0.6.1) before either has reached a stable release; the resulting signature would prove packaging authorship, not source authenticity, while the project's existing digest/provenance trail already does the work the project actually relies on. Premature. |
| E. Formally declare this study closes DR-0006's precondition and additionally declare the capture toolchain "frozen" | Two separable decisions bundled together; freezing the toolchain is a larger commitment (no further structural change to capture without a DR) than this study was asked to evaluate. Raised as an open question (§8), not assumed here. |

## 5. Recommendation

**Defer WACZ adoption — both the container format and signing — for now.**
WARC via `collector/pipeline.py` (DR-0006) remains the project's high-value
capture format, unchanged by this study. This closes DR-0006's evaluation
precondition: an evaluation was performed, from primary sources, covering
exactly what DR-0006 asked (maturity and jurisdictional meaning of
signing), and its answer is *not yet, on stated triggers* rather than
*never*.

**Revisit triggers**, either of which should prompt re-evaluation rather
than another open-ended "not started":

1. **A concrete need for a distributable, browser-replayable package**
   arises — e.g., record §92's evidence-package deliverable becomes active
   work, and RO-Crate's study (still itself unstarted, WP 0.2 §4.9) finds a
   gap WACZ's container format fills better than a plain WARC bundle.
2. **The signing specification reaches a stable release** (1.0 or
   equivalent) with matured reference tooling, changing the "immature
   draft" half of this evaluation's finding.

Neither trigger is close: this recommendation is a genuine defer, not a
disguised "adopt later this month."

## 6. Candidate Decision Records

- **CDR-P3-42 — WACZ evaluated; adoption deferred (DR-0006's precondition
  discharged).** Records that the evaluation DR-0006 required has been
  performed (§2–§3 of this paper), states the finding (container stable at
  1.1.1, signing a pre-1.0 working draft at 0.1.0, jurisdictional
  meaningfulness unanswerable from the specification alone), and defers
  adoption of both the container and signing layers on the triggers in §5.
  WARC via `collector/pipeline.py` continues as the high-value capture
  format unchanged. Does not declare the capture toolchain "frozen" — that
  remains open (§8).

## 7. What was and was not verified

**Verified by direct retrieval on 2026-09-15**, not from memory: the WACZ
container specification text at `specs.webrecorder.net/wacz/1.1.1/`
(directory layout, `datapackage.json`/`datapackage-digest.json` structure,
ZIP compression rules, processing model, publishing considerations); the
WACZ signing specification text at `specs.webrecorder.net/wacz-auth/0.1.0/`
(both signature shapes, their fields, and the spec's own caveats about
non-repudiation); live PyPI release metadata for `wacz`, `authsign`, and
`wacz-signing` (current version, release counts, most recent upload dates).
The `/wacz-auth/latest/` alias was confirmed to redirect to `/0.1.0/` at
fetch time — i.e., 0.1.0 is the current latest, not a stale link this study
picked by mistake.

**Not verified**: the GitHub repositories themselves (`webrecorder/specs`,
`webrecorder/authsign`, `webrecorder/wacz-spec`) returned 403 from this
session's GitHub access, which is scoped to this project's own repository
only — commit history, issue discussion, and any signing-spec changelog
beyond what the rendered spec page itself states were not read. No
jurisdiction's law on digital signatures or evidentiary admissibility was
researched (§3, §8). No attempt was made to actually run `wacz` or
`authsign` against a project capture — this is a specification-and-tooling
maturity evaluation, not an implementation trial, matching WP 3.4 A4's
scope ("from specifications only; say so" per `CLAUDE.md`'s Track A table).

## 8. Open questions raised

1. **Should the A6 legal-review brief gain a sixth question** — whether a
   digital signature scheme (WACZ's or any other) carries evidentiary
   weight under France's law, alongside its existing five? Raised here
   because this study surfaced it; not added to the brief unilaterally,
   since the brief already has an approved shape and adding to it is the
   founder's call, not an automatic consequence of this paper.
2. **Should the capture toolchain now be formally declared "frozen"**,
   now that DR-0006's evaluation precondition is discharged (pending
   CDR-P3-42's approval), or left open given `collector/pipeline.py` may
   still need structural changes the two known gaps (WARC-Version 1.1 wrapping
   dropping the original request and redirect chain, per `collector/README.md`)
   could eventually prompt? Not resolved by this study — freezing is a
   larger commitment than evaluating.
3. **RO-Crate's own still-unstarted study** (WP 0.2 §4.9, "Study — high
   priority") remains the more directly relevant format for record §92's
   evidence-package deliverable; should it be sequenced before or
   independent of any future WACZ reconsideration?

## 9. Sources

- WACZ container specification: [specs.webrecorder.net/wacz/1.1.1/](https://specs.webrecorder.net/wacz/1.1.1/)
- WACZ signing/authentication specification: [specs.webrecorder.net/wacz-auth/0.1.0/](https://specs.webrecorder.net/wacz-auth/0.1.0/) (resolved from the `/latest/` alias, confirmed current at fetch time)
- PyPI release metadata: [`wacz`](https://pypi.org/project/wacz/), [`authsign`](https://pypi.org/project/authsign/), [`wacz-signing`](https://pypi.org/project/wacz-signing/)
- DR-0006, WP 0.2 §4.9/§8 Q4, Phase II output 7 Q-04, WP 3.4 Track A item A4
- DR-0008, LEGAL-007 (chain-of-custody claims discipline)
- DR-0005, DR-0075, §28 (fixity and acquisition-source-vs-publisher discipline already in place)
- `collector/README.md` (current WARC-wrapping implementation and its stated honest limits)
