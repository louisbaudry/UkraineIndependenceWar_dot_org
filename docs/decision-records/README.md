# Decision Records

Unified Decision Record (DR) system per Phase I record §98. Each DR captures
context, alternatives, decision, rationale, consequences, status, and supersession.

Categories (per §98): architecture, methodology, epistemology, preservation,
security, legal, editorial.

## Status vocabulary

- **Proposed** — drafted, awaiting founder decision
- **Approved** — decided by the founder/principal editor; in force
- **Superseded** — replaced by a later DR (both retained; supersession is explicit, per §77)
- **Rejected** — considered and declined (retained as record)

## Numbering (DR-0095)

**No draft ever writes a number that might not be free.** A Decision Record
in progress is named `DR-pending-<slug>.md`, titled `DR-pending-<slug>` in
its own header and any self-reference, and left out of the numbered table
below while pending. The real number is assigned exactly once, at the point
of merging into `main`: grep this table on `origin/main` for the highest
`DR-nnnn`, take the next integer, rename the file, fix its title and
self-references, and add its row in the same commit that completes the
merge. DR-0093 and DR-0094 were each renumbered after the fact because they
guessed a number while drafting and collided with a concurrent branch;
DR-0095 exists so a third collision is structurally impossible rather than
merely another renumbering.

## Register

| ID | Title | Category | Status | Decided |
|---|---|---|---|---|
| [DR-0001](DR-0001-oais-reference-model.md) | Adopt OAIS (ISO 14721:2025) as archival reference model | preservation | Approved | 2026-08-10 |
| [DR-0002](DR-0002-premis-vocabulary.md) | Adopt PREMIS 3.0 as preservation-metadata vocabulary | preservation | Approved | 2026-08-10 |
| [DR-0003](DR-0003-prov-cross-pipeline.md) | Adopt W3C PROV as cross-pipeline derivation/agency model | architecture | Approved | 2026-08-10 |
| [DR-0004](DR-0004-pipeline-world-layer-boundary.md) | Hard boundary between pipeline and historical-world layers | architecture | Approved | 2026-08-10 |
| [DR-0005](DR-0005-fixity-policy.md) | Fixity: SHA-256 at ingestion, checked events, package manifests | preservation | Approved | 2026-08-10 |
| [DR-0006](DR-0006-warc-capture-wacz-evaluation.md) | WARC for high-value web capture; WACZ evaluation required | preservation | Approved | 2026-08-10 |
| [DR-0007](DR-0007-bagit-envelopes-ro-crate-study.md) | BagIt envelopes; RO-Crate study before evidence-package design | preservation | Approved | 2026-08-10 |
| [DR-0008](DR-0008-custody-claims-discipline.md) | Custody claims discipline; Berkeley Protocol guides practice | legal / methodology | Approved | 2026-08-10 |
| [DR-0009](DR-0009-backup-archive-release-separation.md) | Backup, archival preservation, and releases separated | preservation | Approved | 2026-08-10 |
| [DR-0010](DR-0010-cidoc-crm-world-layer.md) | Adopt CIDOC CRM conceptually for the historical world layer | architecture | Approved | 2026-08-11 |
| [DR-0011](DR-0011-lrmoo-documentary-identity.md) | Adopt LRMoo 1.0 conceptually for documentary identity | architecture | Approved | 2026-08-11 |
| [DR-0012](DR-0012-identification-as-events.md) | Names and identifiers attach via assignment events | architecture / epistemology | Approved | 2026-08-11 |
| [DR-0013](DR-0013-roles-as-temporal-events.md) | Roles and memberships are temporal events | architecture | Approved | 2026-08-11 |
| [DR-0014](DR-0014-product-type-vs-item.md) | Product-type vs individual-item distinction | architecture | Approved | 2026-08-11 |
| [DR-0015](DR-0015-ownership-sovereignty-layer-assignment.md) | Ownership/control and sovereignty relations assigned outside the CRM layer | architecture | Approved | 2026-08-11 |
| [DR-0016](DR-0016-crminf-epistemic-study-candidate.md) | CRMinf as starting candidate for the epistemic/argumentation layers | epistemology | Approved | 2026-08-11 |
| [DR-0017](DR-0017-web-annotation-targeting.md) | Adopt W3C Web Annotation as targeting vocabulary | architecture | Approved | 2026-08-11 |
| [DR-0018](DR-0018-anchoring-rule.md) | Evidential annotations target preserved captures, never live URLs alone | architecture / preservation | Approved | 2026-08-11 |
| [DR-0019](DR-0019-quotation-discipline.md) | Quotation discipline | editorial / methodology | Approved | 2026-08-11 |
| [DR-0020](DR-0020-tei-selective-adoption.md) | TEI P5 selective adoption | architecture / editorial | Approved | 2026-08-11 |
| [DR-0021](DR-0021-iiif-study.md) | IIIF study before media-platform design | architecture | Approved | 2026-08-11 |
| [DR-0022](DR-0022-csl-citation-rendering.md) | Adopt CSL for citation rendering | architecture / editorial | Approved | 2026-08-11 |
| [DR-0023](DR-0023-social-media-structural-mapping.md) | Social-media structural mapping | architecture | Approved | 2026-08-11 |
| [DR-0024](DR-0024-six-layer-epistemic-architecture.md) | Adopt the six-layer epistemic architecture | epistemology / architecture | Approved | 2026-08-11 |
| [DR-0025](DR-0025-epistemic-vocabulary-v1.md) | Adopt epistemic vocabulary v1 | epistemology | Approved | 2026-08-11 |
| [DR-0026](DR-0026-two-dimensional-uncertainty.md) | Two-dimensional uncertainty model | epistemology / methodology | Approved | 2026-08-11 |
| [DR-0027](DR-0027-source-grading-triage-only.md) | Source grading is triage-only | epistemology / methodology | Approved | 2026-08-11 |
| [DR-0028](DR-0028-explicit-source-dependence.md) | Source dependence explicit; corroboration counts independent lines | epistemology / methodology | Approved | 2026-08-11 |
| [DR-0029](DR-0029-absence-state-vocabulary.md) | Adopt the absence-state vocabulary | epistemology / architecture | Approved | 2026-08-11 |
| [DR-0030](DR-0030-quantitative-assertion-semantics.md) | Quantitative assertions preserve original semantics | epistemology / architecture | Approved | 2026-08-11 |
| [DR-0031](DR-0031-crminf-adoption-with-extensions.md) | CRMinf adopted as epistemic grounding, with extensions | epistemology / architecture | Approved | 2026-08-11 |
| [DR-0032](DR-0032-argument-representation.md) | Argument representation: CRMinf grounding with AIF-patterned structure | epistemology / architecture | Approved | 2026-08-11 |
| [DR-0033](DR-0033-defeater-typing.md) | Defeater typing: rebut, undercut, undermine | epistemology | Approved | 2026-08-11 |
| [DR-0034](DR-0034-argument-scheme-library.md) | Seed argument-scheme library with critical questions | epistemology / methodology | Approved | 2026-08-11 |
| [DR-0035](DR-0035-hypothesis-competition.md) | Hypothesis competition is first-class | epistemology / methodology | Approved | 2026-08-11 |
| [DR-0036](DR-0036-no-automatic-adjudication.md) | No automatic adjudication of arguments | epistemology / editorial | Approved | 2026-08-11 |
| [DR-0037](DR-0037-toulmin-editorial-scaffold.md) | Toulmin as editorial scaffold only | editorial / methodology | Approved | 2026-08-11 |
| [DR-0038](DR-0038-sanctions-legal-lifecycle.md) | Sanctions as instruments/regimes/designations/effects with full lifecycle | legal / architecture | Approved | 2026-08-11 |
| [DR-0039](DR-0039-designation-records-distinct.md) | Designation records distinct from canonical entities | legal / architecture | Approved | 2026-08-11 |
| [DR-0040](DR-0040-bods-ownership-statements.md) | Ownership/control follow the BODS statement pattern | legal / architecture | Approved | 2026-08-11 |
| [DR-0041](DR-0041-rule-derived-applicability.md) | Rule-derived applicability computed, versioned, never stored as designation | legal / architecture | Approved | 2026-08-11 |
| [DR-0042](DR-0042-export-control-decomposition.md) | Export-control state is decomposed | legal / architecture | Approved | 2026-08-11 |
| [DR-0043](DR-0043-transaction-shipment-payment-triad.md) | Transaction / shipment / payment triad | architecture | Approved | 2026-08-11 |
| [DR-0044](DR-0044-territorial-status-vocabulary.md) | Territorial-status vocabulary | architecture / legal | Approved | 2026-08-11 |
| [DR-0045](DR-0045-ftm-interchange-mapping.md) | FollowTheMoney/OpenSanctions as interchange mapping and identifier spine | architecture | Approved | 2026-08-11 |
| [DR-0046](DR-0046-unified-document-control.md) | Unified document control for the six governance document classes | architecture / methodology | Approved | 2026-08-11 |
| [DR-0047](DR-0047-versioning-regime-per-dimension.md) | One versioning regime per dimension | architecture | Approved | 2026-08-11 |
| [DR-0048](DR-0048-releases-are-baselines.md) | Releases are configuration-management baselines | architecture / preservation | Approved | 2026-08-11 |
| [DR-0049](DR-0049-dcat-datacite-releases.md) | DCAT for release description; DataCite DOIs when mature | architecture | Approved | 2026-08-11 |
| [DR-0050](DR-0050-11179-skos-registry.md) | Semantic registry: ISO/IEC 11179 pattern, SKOS-expressed | architecture | Approved | 2026-08-11 |
| [DR-0051](DR-0051-requirements-management.md) | Requirements management per record §99 | architecture / methodology | Approved | 2026-08-11 |
| [DR-0052](DR-0052-site-history-from-first-page.md) | Public site revision history from the first page | preservation / architecture | Approved | 2026-08-11 |
| [DR-0053](DR-0053-phase-2-closure.md) | Phase II closure: consolidation outputs approved | methodology / architecture | Approved | 2026-08-16 |
| [DR-0054](DR-0054-layered-canonical-representation.md) | Layered canonical representation (answers record §95) | architecture | Approved | 2026-08-16 |
| [DR-0055](DR-0055-append-only-canonical-store.md) | Append-only canonical store with governed redaction | architecture / preservation | Approved | 2026-08-16 |
| [DR-0056](DR-0056-projection-mappings-controlled.md) | Projection mappings are controlled artifacts | architecture | Approved | 2026-08-16 |
| [DR-0057](DR-0057-postgresql-default-candidate.md) | PostgreSQL as default implementation candidate | architecture | Approved | 2026-08-16 |
| [DR-0058](DR-0058-durable-export-obligation.md) | Durable export is a standing obligation | preservation / architecture | Approved | 2026-08-16 |
| [DR-0059](DR-0059-two-agent-registries.md) | Two agent registries, linked | architecture | Approved | 2026-08-16 |
| [DR-0060](DR-0060-premis-initial-subset.md) | Initial PREMIS subset | preservation / architecture | Approved | 2026-08-16 |
| [DR-0061](DR-0061-holding-object.md) | The holding object | architecture / preservation | Approved | 2026-08-16 |
| [DR-0062](DR-0062-entity-status-vocabulary.md) | Entity-status vocabulary | architecture / epistemology | Approved | 2026-08-16 |
| [DR-0063](DR-0063-match-lifecycle-tiered-confirmation.md) | Match lifecycle and tiered confirmation | architecture / methodology | Approved | 2026-08-16 |
| [DR-0064](DR-0064-merge-split-lineage.md) | Merge/split as lineage events with reviewed re-homing | architecture / preservation | Approved | 2026-08-16 |
| [DR-0065](DR-0065-likelihood-band-scale.md) | Likelihood band scale: ICD 203 canonical, PHIA mapped | epistemology / methodology | Approved | 2026-08-16 |
| [DR-0066](DR-0066-three-gate-pipeline.md) | Three-gate pipeline model | architecture | Approved | 2026-08-16 |
| [DR-0067](DR-0067-source-registry-schema.md) | Source registry schema | architecture / operations | Approved | 2026-08-16 |
| [DR-0068](DR-0068-retention-tiers.md) | Retention tiers | preservation | Approved | 2026-08-16 |
| [DR-0069](DR-0069-quarantine-zone.md) | Quarantine as a pre-archival zone | security / architecture | Approved | 2026-08-16 |
| [DR-0070](DR-0070-collector-run-coverage.md) | Collector-run coverage record | operations / preservation | Approved | 2026-08-16 |
| [DR-0071](DR-0071-interim-personal-data-constraints.md) | Interim personal-data constraints (self-lifting) | legal / operations | Approved | 2026-08-16 |
| [DR-0072](DR-0072-personal-data-policy-adoption.md) | Adoption of the Personal Data Policy (POL-0001) | legal / editorial | Approved | 2026-08-16 |
| [DR-0073](DR-0073-ocfl-storage-layout.md) | Adopt OCFL as the at-rest archival storage layout | preservation / architecture | Approved | 2026-08-16 |
| [DR-0074](DR-0074-ocfl-object-is-the-holding.md) | The OCFL object is the holding | preservation / architecture | Approved | 2026-08-16 |
| [DR-0075](DR-0075-digest-strategy.md) | Digest strategy: SHA-512 addressing, SHA-256 fixity block | preservation | Approved | 2026-08-16 |
| [DR-0076](DR-0076-tier-separated-storage-roots.md) | Retention-tier-separated storage roots | preservation / operations | Approved | 2026-08-16 |
| [DR-0077](DR-0077-redaction-sole-immutability-exception.md) | Governed redaction is the sole immutability exception | preservation / legal | Approved | 2026-08-16 |
| [DR-0078](DR-0078-registry-source-of-truth.md) | Registry source of truth: files in Git, runtime as projection | architecture | Approved | 2026-08-16 |
| [DR-0079](DR-0079-registry-entry-typology.md) | Registry entry typology and structure | architecture | Approved | 2026-08-16 |
| [DR-0080](DR-0080-registry-lifecycle-and-change-classes.md) | Registry lifecycle and change classes | architecture / methodology | Approved | 2026-08-16 |
| [DR-0081](DR-0081-governed-translation.md) | Governed translation of registry terminology | architecture / editorial | Approved | 2026-08-16 |
| [DR-0082](DR-0082-requirements-enactment.md) | Enactment of the requirement set (73 requirements, ten REQ documents) | architecture / methodology | Approved | 2026-08-16 |
| [DR-0083](DR-0083-registry-projection-mapping.md) | Adoption of the registry projection mapping (SPEC-0005) | architecture | Approved | 2026-08-20 |
| [DR-0084](DR-0084-durable-export-format-adoption.md) | Durable export format adopted; unfiltered dumps blocked | architecture / security | Approved | 2026-08-21 |
| [DR-0085](DR-0085-evidentiary-method-adoption.md) | Adoption of the evidentiary method (METH-0001) | methodology / epistemology | Approved | 2026-08-26 |
| [DR-0086](DR-0086-tier-restrictiveness-declared.md) | Access-tier restrictiveness is declared, never derived from an ordering | security / architecture | Approved | 2026-08-26 |
| [DR-0087](DR-0087-ark-public-identifier-scheme.md) | ARK as the public identifier scheme | architecture / preservation | Approved | 2026-09-09 |
| [DR-0088](DR-0088-public-identifiers-as-assignment-events.md) | Public identifiers are minted as assignment events at publication | architecture / editorial | Approved | 2026-09-09 |
| [DR-0089](DR-0089-identifier-register-dispositions.md) | The identifier register and its five dispositions | architecture / preservation / security | Approved | 2026-09-09 |
| [DR-0090](DR-0090-identifiers-name-objects-qualifiers-name-states.md) | Identifiers name objects; `.vN` qualifiers name states | architecture / preservation | Approved | 2026-09-09 |
| [DR-0091](DR-0091-project-uris-derive-from-arks.md) | Project URIs derive from ARKs; the registry namespace is the registry's ARK | architecture | Approved | 2026-09-09 |
| [DR-0092](DR-0092-split-byline-as-public-title.md) | A split's deciding agent is shown as a public title, snapshotted, never the agent row | architecture / editorial / security | Approved | 2026-09-09 |
| [DR-0093](DR-0093-first-source-registrations.md) | First source registrations: EU Consolidated Financial Sanctions List and OFAC SDN | operations / preservation | Approved | 2026-09-08 |
| [DR-0094](DR-0094-third-party-web-captures.md) | Third-party web captures (Common Crawl, Wayback Machine, qualifying archives) as an acquisition channel | architecture / preservation | Approved | 2026-09-11 |
| [DR-0095](DR-0095-dr-numbering-placeholder-until-merge.md) | Decision Records are drafted unnumbered; the number is assigned at merge | architecture / methodology | Approved — superseded by DR-0102 | 2026-09-11 |
| [DR-0096](DR-0096-second-source-registrations.md) | Second source registrations: UK OFSI Consolidated List and BIS Denied Persons List (DPL half only) | operations / preservation | Approved — executed 2026-09-21 | 2026-09-12 |
| [DR-0097](DR-0097-collection-run-two-agents.md) | A collection run carries two agents: a human agent of record and a versioned software agent on its preservation events | architecture / preservation | Approved | 2026-09-12 |
| [DR-0098](DR-0098-seco-sanctions-registration.md) | Third source registration: SECO sanctions list (Switzerland) | operations / preservation | Approved — executed 2026-09-21 | 2026-09-14 |
| [DR-0099](DR-0099-establishment-jurisdiction.md) | Interim establishment jurisdiction: France; POL-0001 amended to v1.1 | legal / editorial | Approved — superseded by DR-0100 | 2026-09-14 |
| [DR-0100](DR-0100-jurisdiction-controller-and-hosting.md) | Establishment jurisdiction confirmed; controller identity and archive hosting location | legal / operations | Approved | 2026-09-15 |
| [DR-0101](DR-0101-recording-the-legal-review.md) | What "the review's outcome is recorded" means, for POL-0001 §10 | legal / methodology | Approved | 2026-09-15 |
| [DR-0102](DR-0102-drafting-discipline-before-merge.md) | Drafting discipline before merge: CDR numbers assigned at merge, unmerged branches checked before starting, bounded in-place revision | architecture / methodology | Approved | 2026-09-15 |
| [DR-0103](DR-0103-registration-classes.md) | Registration classes (Option A): source authorization scales from per-source to per-class plus exceptions | architecture / operations | Approved | 2026-09-15 |
| [DR-0104](DR-0104-legal-entity-formation.md) | Legal entity formation: association loi 1901, started now, in parallel with pending counsel advice | legal / operations | Approved | 2026-09-20 |
| [DR-0105](DR-0105-eur-lex-sanctions-registration.md) | Fourth source registration: EUR-Lex restrictive measures (Ukraine/Russia) | operations / preservation | Approved — executed 2026-09-21 | 2026-09-21 |
| [DR-0106](DR-0106-strike-tracking-registration.md) | Fifth and sixth source registrations: `kpszsu` and `generalstaffzsu` (strike tracking) | operations / preservation | Approved — executed 2026-09-22 | 2026-09-21 |
| [DR-0107](DR-0107-strike-tracking-full-backfill.md) | Authorizing full historical backfill of `kpszsu` and `generalstaffzsu` | operations / preservation | Approved — in execution since 2026-09-23 | 2026-09-23 |
| [DR-0108](DR-0108-backup-deferral.md) | Independent backups (OPS-005) deferred until the association exists | operations / preservation | Approved — OPS-005 knowingly unmet until the trigger | 2026-09-24 |
| [DR-0109](DR-0109-civilian-harm-and-memorial.md) | Civilian harm and war crimes as a subject area, and a memorial site built on the archive | scope / publication / personal data | Approved — authorises no collection, registration or publication | 2026-09-24 |

## Provenance of decisions

DR-0001 through DR-0009 originate from candidate Decision Records CDR-W1-1…9 in
[WP 0.2](../phase-2/working-papers/wp-0.2-ws1-preservation-provenance-concept-map.md)
(AI-drafted candidate paper). Each was individually reviewed and approved by the
founder/principal editor on 2026-08-10 in an interactive review session, per record
§78–79: AI proposed; the human decided.

DR-0010 through DR-0016 originate from CDR-W2-1…7 in
[WP 0.3](../phase-2/working-papers/wp-0.3-ws2-historical-event-knowledge-concept-map.md)
(AI-drafted candidate paper). The seven were presented to the founder with
per-item disposition options and approved as a set on 2026-08-11 ("Go ahead"
on the recommended approve-all disposition).

DR-0017 through DR-0023 originate from CDR-W3-1…7 in
[WP 0.4](../phase-2/working-papers/wp-0.4-ws3-document-identity-textual-evidence-concept-map.md)
(AI-drafted candidate paper), approved as a set by the founder on 2026-08-11
("Approve all seven").

DR-0024 through DR-0031 originate from CDR-W4-1…8 in
[WP 0.5](../phase-2/working-papers/wp-0.5-ws4-epistemology-evidence-concept-map.md)
(AI-drafted candidate paper), approved as a set by the founder on 2026-08-11
("OK. Let us continue" on the recommended approve-all disposition).

DR-0032 through DR-0037 originate from CDR-W5-1…6 in
[WP 0.6](../phase-2/working-papers/wp-0.6-ws5-argumentation-concept-map.md)
(AI-drafted candidate paper), approved as a set by the founder on 2026-08-11
("Approve all six and continue").

DR-0038 through DR-0045 originate from CDR-W6-1…8 in
[WP 0.7](../phase-2/working-papers/wp-0.7-ws6-sanctions-export-controls-concept-map.md)
(AI-drafted candidate paper), approved as a set by the founder on 2026-08-11
("Approve all eight and continue").

DR-0046 through DR-0052 originate from CDR-W7-1…7 in
[WP 0.8](../phase-2/working-papers/wp-0.8-ws7-governance-versioning-concept-map.md)
(AI-drafted candidate paper), approved as a set by the founder on 2026-08-11
("Approve all seven and continue with the consolidation").

DR-0053 records the founder's approval of the Phase II consolidation outputs
and the closure of Phase II (2026-08-16, "OK. Let us continue").

DR-0054 through DR-0058 originate from CDR-P3-1…5 in
[WP 3.1](../phase-3/working-papers/wp-3.1-canonical-representation-study.md)
(AI-drafted candidate paper), approved as a set by the founder on 2026-08-16
("approved all") after a restated summary of the five proposals.

DR-0059 through DR-0061 originate from CDR-P3-6…8 in
[SPEC-0001](../specifications/SPEC-0001-conceptual-data-model.md), each
individually approved by the founder on 2026-08-16 in an interactive
one-by-one review; SPEC-0001 v1.0 was approved as effective in the same
review.

DR-0062 through DR-0064 originate from CDR-P3-9…11 in
[SPEC-0002](../specifications/SPEC-0002-identity-entity-resolution.md), each
individually approved by the founder on 2026-08-16 in an interactive
one-by-one review; SPEC-0002 v1.0 was approved as effective in the same
review.

DR-0065 originates from CDR-P3-12 in
[WP 3.2](../phase-3/working-papers/wp-3.2-likelihood-band-scale.md), approved
by the founder on 2026-08-16 after a side-by-side comparison of the ICD 203
and PHIA scales.

DR-0078 through DR-0081 originate from CDR-P3-25…28 in
[SPEC-0004](../specifications/SPEC-0004-semantic-registry.md), approved by
the founder on 2026-08-16 — DR-0078 in individual review, DR-0079 through
DR-0081 as a reviewed group. SPEC-0004 v1.0 was approved as effective in
the same review.

DR-0073 through DR-0077 originate from CDR-P3-20…24 in
[WP 3.3](../phase-3/working-papers/wp-3.3-storage-preservation-layout.md),
approved by the founder on 2026-08-16 — DR-0073 and DR-0074 in individual
review, DR-0075 through DR-0077 as a reviewed group of implementation
choices following from OCFL adoption.

DR-0072 adopts [POL-0001](../policies/POL-0001-personal-data.md), approved by
the founder on 2026-08-16 with its three §8 rulings taken individually; the
policy's collection-scope releases remain suspended pending external legal
review.

DR-0066 through DR-0071 originate from CDR-P3-13…18 in
[SPEC-0003](../specifications/SPEC-0003-collection-pipeline.md), approved by
the founder on 2026-08-16 — DR-0066, DR-0069, and DR-0071 in individual
review; DR-0067, DR-0068, and DR-0070 as a reviewed group of mechanical
implementations. SPEC-0003 v1.0 was approved as effective in the same
review.

DR-0085 adopts
[METH-0001](../methodology/METH-0001-evidentiary-method.md), drafted
2026-08-25 after the DR-0048 release-readiness check reported that no METH
document existed and therefore no release could be created. Approved by the
founder on 2026-08-26 with METH-0001 §15's five open questions **ruled one at
a time** — the test for "consequential", the confidence cap on unanswered
critical questions, mandatory competing-hypothesis sets, how self-review is
recorded and published, and retrospective likelihood phrasing (which closes
DR-0065's carried-forward open item). Three rulings made the method stricter
than the draft proposed. METH-0001 v1.0 was approved as effective in the same
review.

DR-0086 arises from a defect found while implementing Gate 3: the export
policy resolved competing access tiers with `min()` over the tier text, which
is alphabetical and returns `public` for {public, subscriber} — the opposite
of the "most restricted wins" rule its own rationale stated. Approved by the
founder on 2026-08-26: restrictiveness is declared in both the schema and the
export policy, never derived from any ordering the database supplies, with
the suite checking the two agree. The alternative of reordering the
`access_tiers` enum was rejected — it cannot express the lateral grants, and
changing an enumeration data depends on is a structural registry change
(DR-0080). Its open item — whether the two lateral tiers should remain
distinct at all — is a §12 vocabulary question, not a resolution one.

DR-0096 through DR-0101 were **approved between 2026-09-12 and 2026-09-15 but
numbered only on 2026-09-15**, in one commit, when the branch carrying the
last of them was prepared for merge. Three of them (DR-0096, DR-0097,
DR-0098) had already reached `main` unnumbered and without register rows,
which is the step DR-0095 prescribes and which was missed on each. The
register is brought current here rather than left to drift further; the gap
is recorded rather than tidied away, because an index that silently omits
three enacted decisions is the failure mode the register exists to prevent.

**DR-0102 supersedes DR-0095**, carrying its rule forward verbatim and
withdrawing its clause 4, whose premise — that CDR numbers are scoped per
working paper — is not how the convention works: CLAUDE.md numbers them
"continuing from the last one used anywhere in `docs/`", a single global
sequence. DR-0102 also adds a pre-start check of unmerged branches, and a
bounded exception permitting in-place revision of a record that has not
reached `main` under four conditions, of which the founder having ruled the
change is the one that keeps it narrow.

**DR-0099 and DR-0100 are two records of one decision**, and both are kept.
Two agent sessions drafted the WP 3.4 Track A item A6 legal-review brief in
parallel on 2026-09-14 and 2026-09-15, neither aware of the other — one on an
unmerged branch — and each independently found that POL-0001 §10 presumed an
establishment jurisdiction no document named. The founder answered both.
DR-0099 named France as the **interim** jurisdiction and amended POL-0001 to
v1.1; DR-0100 confirms that ruling and its *interim* framing unchanged and
adds the controller's identity, the archive hosting location, and a POL-0001
§11 trigger for changes to either. DR-0099 is superseded, not withdrawn:
§77's discipline applies to decision records. POL-0001 reached **v1.2** on
2026-09-15 so its §10 names DR-0100 as the operative record and restates the
jurisdiction, controller and hosting facts in the policy itself, rather than
leaving a reader to follow the supersession chain; v1.1's citation of DR-0099
remains correct history. The same collision took
**CDR-P3-42** twice; WP 3.6's claim is the older and stands, and the A6
brief's candidates renumbered to CDR-P3-43…45. DR-0095 closes this for DR
numbers and does not reach CDR numbers or duplicated documents — see
DR-0100's Consequence 6, where extending it is proposed and left to the
founder.

DR-0087 through DR-0091 originate from CDR-P3-36…40 in
[WP 3.5](../phase-3/working-papers/wp-3.5-identifier-design.md) (AI-drafted
identifier-design study), each put to the founder as a separate question
with named options and a recommendation and **ruled one at a time** on
2026-09-09: the scheme (ARK, own NAAN, own resolver), the minting rule
(assignment events at publication or citation, annotations included), the
five-disposition register including `restricted`, object identifiers with
`.vN` qualifiers for states, and ARK-derived URIs including the registry
namespace. Together they resolve Q-12, discharge DR-0022's deferral, close
SPEC-0002 §6 Q3 and SPEC-0005 §7 Q1, and authorise SPEC-0007 — Public
Identifiers and Resolution.

DR-0092 resolves SPEC-0007 v0.3 §12 open question 2, put to the founder
directly rather than through a working paper: whether a split's deciding
agent is named in the public response. The founder ruled for a public role
or title, snapshotted onto the disambiguation record by trigger and never
read from `pipeline_agent` at resolution time, over withholding it
entirely or disclosing the agent's name.

DR-0093 was drafted 2026-09-08 at the founder's direction, after the founder
chose to begin collection with two of the seven sanctions-authority
candidates, and **approved by the founder the same day for both sources**.
Before drafting, every file a first run would collect was fetched, digested
and run through the real collector into a throwaway database (record in
[docs/sources/verification-eu-consolidated-list-ofac-sdn.md](../sources/verification-eu-consolidated-list-ofac-sdn.md)).
It authorises the two registrations and one manual first run against five
verified locators, executed by the founder on the archive server with
`collector/run.py` (built on approval); it does not automate the daily
cadence, which waits on rulings the rehearsal surfaced (captures are not
yet linked as a series; unchanged bytes are stored again; quarantine copies
are never removed). **Numbered out of date order:** drafted and approved
2026-09-08, before DR-0087…0092 (dated 2026-09-09), because it was developed
on a separate branch alongside the identifier-scheme work and assigned the
next free number only when the two branches were reconciled on 2026-09-10.
The register is ordered by number, not date, throughout; this is the one
entry where the two diverge.

DR-0094 is a second, independent instance of the same collision CLAUDE.md's
onboarding notes now warn about: drafted on a branch cut before the
identifier-scheme and DR-0093 branches were reconciled, and assigned
DR-0087 at the time on the strength of its own branch's then-current
register. It carried no other numbering dependency — nothing else in the
DR set references it — so reconciliation was a rename to the next free
number, DR-0094, with no reordering elsewhere in the register. It was
approved 2026-09-11, after a second round of four questions on points the
original draft had left open (whether loss-triggered retrieval needs a
per-instance human step, whether a future archive needs its own DR or can
qualify by criteria, whether retrieval blocks on the DR-0006 WACZ
evaluation, and how to record the answers), each put to the founder with
named options and a recommendation; the founder went against the
recommendation on the archive-qualification question. The DR's own text
was amended to carry all four rulings in the same step that approved it.

DR-0095 was raised by Claude immediately after reconciling DR-0094, put to
the founder directly with three named options and a recommendation, and
approved the same day: a Decision Record is now drafted under a
`DR-pending-<slug>` placeholder name, with its real number written exactly
once, at merge time, rather than guessed while drafting. It closes the gap
DR-0093 and DR-0094 each hit, and CLAUDE.md's drafting instruction is
updated in the same change to match (see "Numbering" below and CLAUDE.md's
"Documents" section).

DR-0103 originates from **CDR-P3-32**, deposited in WP 3.4 §8 on
2026-09-08 — not a newly minted CDR. The PR that implemented and merged
the mechanism (A5, merged 2026-09-16 as #29) deposited its own design
paper as `wp-3.5-registration-classes.md`, colliding with the already-taken
WP 3.5 (identifier design, DR-0087…0091) — the file merged to `main` under
that name, undetected, exactly the kind of collision DR-0102 exists to
catch, missed here because the collision is on the *working-paper* number,
which DR-0102's pre-start branch check does not itself compute. Enacting
DR-0103 renamed the file to `wp-3.7-registration-classes.md` (next free
working-paper number), corrected its self-references and its Candidate
Decision Records section to point at CDR-P3-32 rather than an
unassigned `CDR-pending-A5–class-mechanism`, and added its
`docs/phase-3/README.md` row and `PROVENANCE.md` entry, none of which the
merged PR had done. `CLAUDE.md`'s Track A table and `sources/register.py`,
`sources/candidates/sanctions-authorities.yaml` and
`sources/tests/test_register_classes.py`'s references to
`DR-pending-registration-classes` were updated to `DR-0103` in the same
change.

DR-0104 and DR-0105 reached `main` (via PR #34, merged 2026-09-21) still
named `DR-pending-legal-entity-formation` and
`DR-pending-eur-lex-sanctions-registration` — the merge that landed them
did not perform the renaming step DR-0095/DR-0102 require in the same
commit as the merge. Numbered here, in the session that executed DR-0105's
registration on the archive server and noticed the gap while updating this
register: DR-0104 (approved 2026-09-20) before DR-0105 (approved
2026-09-21), matching approval order. Self-references in both files and
every cross-reference in `README.md`, `CLAUDE.md` and `sources/README.md`
were updated in the same change.

DR-0106 and DR-0107 were numbered at merge (PR #39), from
`DR-pending-strike-tracking-registration` and
`DR-pending-strike-tracking-full-backfill`, in approval order: DR-0106
approved 2026-09-21, DR-0107 on 2026-09-23. `CDR-pending-telegram-backfill`
took `CDR-P3-46` in the same change, and every reference in `README.md`,
`collector/README.md`, `collector/telegram_backfill.py` and
`docs/runbooks/telegram-channel-backfill.md` was updated with it.

DR-0108 was numbered before its PR was opened, not at merge. The founder
merges from the UI, and PR #34 had shown that a number left for "merge time"
can reach `main` still reading `DR-pending-*`. It was drafted as
`DR-pending-backup-deferral`. The 2026-09-24 check found DR-0107 as the
highest record on `origin/main` and no unmerged branch drafting a new one.
If another record takes DR-0108 first, renumber this one when merging.

**Both records were also revised in place before merge, on 2026-09-24, under
DR-0102 Decision 7 — and only three of its four conditions held.** Neither had
reached `main`, the founder ruled each change, and each carries a Revision note
with its date and reason; but neither was revised *in the same session as its
approval*, and the founder **waived that condition explicitly**, having been
shown that it did not hold. Recorded here because Decision 7 states that "not
merged yet" is a bound on blast radius and **not** a reason: this is a waiver
granted per record, not a precedent for inferring revisability from Git state.
The substance was a review finding that neither record mentioned POL-0001 §10,
DR-0072, personal data or the pending legal review at all, so a reader could
not tell whether the review had been weighed; each gained a "Relation to
POL-0001 §10 and DR-0072" subsection that states why registered sources with
configured scope sit inside the founder's ruling of 2026-09-08 and leaves the
questions of degree and kind open. DR-0106's correction of a wrong candidate
count (it read "five of nine", self-corrected mid-clause to "six", where eleven
candidates exist and eight are registered) was the second change. Alternatives
offered and not chosen: merge as-is and supersede; pause the backfill until §10
is recorded.
