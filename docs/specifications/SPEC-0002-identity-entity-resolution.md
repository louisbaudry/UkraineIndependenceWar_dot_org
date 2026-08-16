# SPEC-0002 — Identity & Entity-Resolution Workflow

**Class:** SPEC (DR-0046 control) | **Version:** 1.0 | **Status:** Approved — Effective
**Approval:** founder/principal editor, 2026-08-16 (per-item interactive review) | **Effective:** 2026-08-16
**Supersedes:** — | **Superseded by:** —
**Change history:** 0.1 draft deposited 2026-08-16; approved as 1.0 the same day — status block and §7 enactment note are the only changes
**Governed by:** DR-0012 (identification as events), DR-0024/0026 (epistemic layers, assessments), DR-0028 (dependence), DR-0039 (designation mapping), DR-0059 (two registries), SPEC-0001 (assertion pattern); record §16–17, §72; requirements DATA-001/002/010.

### AI provenance (record §80)

Drafted 2026-08-16 by an AI assistant (Anthropic Claude Code agent session)
from DR-0001…0061 and SPEC-0001, at the founder's direction. Candidate until
approved.

---

## 1. Scope

How identities are proposed, reviewed, confirmed, rejected, merged, split,
and traced — for world actors, physical objects, places, organizations,
designation-record subjects, and cross-registry person links. Resolves Q-10.
**Not in scope:** matcher algorithms and scoring (implementation; §6).

## 2. Entity status

Every world-layer entity carries a registry-governed **entity status**:

| Status | Meaning |
|---|---|
| `canonical` | An entity the project treats as a real, distinct referent |
| `candidate` | A provisionally distinct entity, not yet consolidated (e.g., a name cluster from one dataset) |
| `fabricated` | An identity the project concludes never referred to a real distinct person/thing (invented persona, sockpuppet identity) — kept, because claims about it exist (§17) |
| `disproved` | A formerly canonical/candidate entity shown to be a duplicate or error, superseded via merge/split lineage |

Fabricated and disproved entities are never deleted: propaganda and
impersonation analysis (§17, §54) needs them as referents.

## 3. The match lifecycle

A **match assertion** proposes that two identity bearers refer to the same
referent (candidate↔canonical, designation-record↔entity, account↔actor,
external-dataset-entity↔entity, pipeline-agent↔world-actor per DR-0059).
It follows SPEC-0001's assertion pattern, with:

- **States:** `proposed` → `under-review` → `confirmed` | `rejected`
  (+`withdrawn` for proposer retraction). State changes are superseding
  assertions (DR-0055) with actor and basis.
- **Proposal:** automated matchers and AI **may only create `proposed`
  matches** (AI-001); every proposal records its feature basis (which
  attributes matched: name similarity, DOB, registration number, address,
  photo, relationship pattern…).
- **Confirmation:** requires a human decision at the tier the subject
  demands (§4), citing **discriminating evidence** — at least one basis
  beyond name/transliteration similarity (shared strong identifier, DOB +
  corroborating attribute, documented relationship, photographic or
  documentary corroboration). **Name similarity alone can never confirm**
  (§72, DATA-002) — for any entity type, at any tier.
- **Rejection:** recorded with reason and kept permanently; matchers must
  consult rejected matches to prevent re-proposal churn (§17 "rejected
  matches" as first-class).
- **Confirmed matches** produce effect by assertion, not mutation: the
  designation-record mapping (DR-0039), the account attribution (DR-0023),
  or the same-person link (DR-0059) — the underlying records stay distinct.

## 4. Review tiers (applying §78 to identity)

| Tier | Subjects | Confirmation requires |
|---|---|---|
| **T1 — highest** | Designation-record↔entity mappings; any identity used in a legal-layer conclusion (DR-0041 paths, LEGAL-003) | Human confirmation on discriminating evidence; a recorded review; independence of evidence lines considered (DR-0028) |
| **T2 — elevated** | World actors in consequential project assertions; cross-registry same-person links; individual physical items in tracing chains | Human confirmation on discriminating evidence |
| **T3 — routine** | Bibliographic identity (work/expression clustering), places with authoritative gazetteer IDs, low-stakes dataset alignment | Human confirmation may be batch-wise; single strong shared identifier suffices |

False merges remain costlier than missed matches at every tier (§16): when in
doubt, entities stay separate and the match stays `proposed`.

## 5. Merge, split, and lineage

- **Merge** is an event: it creates (or designates) a successor entity,
  marks the predecessors `disproved`-as-distinct with permanent redirects,
  and triggers a **re-homing review**: every assertion attached to a
  predecessor is explicitly re-pointed (or flagged) by review — never
  silently bulk-moved, because some assertions may have belonged only to the
  error.
- **Split** is the reverse event: a successor set, a disposition for each
  attached assertion, and redirects that dead-end into a disambiguation
  record.
- **Lineage is permanent:** every entity can answer "what merges/splits
  produced me, decided by whom, on what evidence" (§17 identity lineage).
  Public identifiers of merged/split entities keep resolving (§15) to the
  lineage explanation.
- Merge/split mappings ship in release change sets (DR-0048, §91).

## 6. Open questions raised

1. Matcher implementation: feature weights, blocking keys, batch cadence for
   external datasets (OpenSanctions, GLEIF, registries) — implementation
   SPEC after collector design (Phase III item 5).
2. Whether T3 batch confirmations need sampling-based audit (ties to §82 QA
   actions) — POL/PROC territory.
3. Disambiguation-record content for split redirects — small; with the
   §15 identifier design (Q-12).

## 7. Decision Records arising (enacted)

The three proposals were individually approved by the founder on 2026-08-16
and enacted:

- **DR-0062** — entity-status vocabulary (§2)
- **DR-0063** — match lifecycle and tiered confirmation (§3–4)
- **DR-0064** — merge/split as lineage events with reviewed re-homing (§5)

## 8. Sources

DR-0012, DR-0028, DR-0039, DR-0059; SPEC-0001; record §16–17, §72; Phase II
output 6 (DATA-001/002/010); entity-resolution practice in the OpenSanctions
ecosystem (candidate/confirmed/rejected judgement pattern) as prior art.
