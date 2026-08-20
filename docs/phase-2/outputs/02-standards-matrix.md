# Phase II Output 2 — Standards/Model Matrix (candidate, final dispositions)

Dispositions: **adopt** (conceptual adoption, DR-backed) · **adopt-pattern**
(its structural pattern adopted, not its serialization) · **selective** ·
**map-to** (mappings maintained; not internal model) · **study** (evaluation
required before a dependent decision) · **reference** (informs design; no
commitment) · **defer** · **rejected as master** (useful role, barred from
being the canonical model).

## Preservation & provenance (WS1)

| Standard | Disposition | DR / note |
|---|---|---|
| OAIS / ISO 14721:2025 | Adopt | DR-0001 |
| PREMIS 3.0 | Adopt | DR-0002; serialization deferred to Phase III |
| W3C PROV | Adopt | DR-0003 |
| WARC / ISO 28500 | Adopt (high-value capture) | DR-0006 |
| WACZ | Study (required before toolchain freeze) | DR-0006 |
| BagIt / RFC 8493 | Adopt | DR-0007 |
| RO-Crate | Study (required before evidence-package design) | DR-0007 |
| OCFL | Study (immutability-enforcing storage layout) | WP 0.2 §6; Q-13 |
| Memento / RFC 7089 | Adopt-pattern (capture series) | DR-0023 |
| METS | Compare/map in RO-Crate study | DR-0007 |
| ISO 16363 | Map-to (self-assessment checklist) | WP 0.2 §6 |
| PAIS / CCSDS 651.1 | Reference | WP 0.2 §6 |
| ODRL | Defer | WP 0.2 §6 |

## World model & documents (WS2–3)

| Standard | Disposition | DR / note |
|---|---|---|
| CIDOC CRM 7.1.3 / ISO 21127:2023 | Adopt | DR-0010; not the physical schema |
| CRMinf | Adopt + extensions | DR-0031 |
| CRMsci / CRMgeo / CRMdig / CRMsoc | Study (subset selection; CRMdig reconciled under DR-0003) | Q-08 |
| LRMoo 1.0 | Adopt | DR-0011 |
| IFLA LRM | Adopted via LRMoo | DR-0011 |
| BIBFRAME | Compare/map | WP 0.1 |
| TEI P5 (4.x) | Selective | DR-0020 |
| W3C Web Annotation | Adopt | DR-0017 |
| IIIF Presentation 3.0 | Study (required before media platform) | DR-0021 |
| CSL | Adopt | DR-0022 |
| Wikidata | External-identifier mapping target | DR-0012; per §16 |

## Epistemics & argumentation (WS4–5)

| Standard / instrument | Disposition | DR / note |
|---|---|---|
| ICD 203 / PHIA yardsticks | Adopt-pattern (band scale fixed by future DR) | DR-0026; Q-16 |
| IPCC calibrated uncertainty | Adopt-pattern (two-dimensional structure) | DR-0026 |
| Admiralty/NATO grading | Adopt-pattern, triage-only | DR-0027 |
| ACH (Heuer) | Adopt-pattern (derived views) | DR-0035 |
| AIF | Map-to (interchange) | DR-0032 |
| Walton argument schemes | Adopt-pattern (seed library) | DR-0034 |
| Toulmin | Editorial scaffold only | DR-0037 |
| Dung semantics / ASPIC+ | Reference; analytic aids only | DR-0033, DR-0036 |
| Berkeley Protocol | Adopt (methodology) | DR-0008 |

## Sanctions & trade (WS6)

| Standard / source | Disposition | DR / note |
|---|---|---|
| FollowTheMoney (FtM) | Map-to (interchange) | DR-0045 |
| OpenSanctions | External-identifier spine + source | DR-0045 |
| BODS (Open Ownership) | Adopt-pattern (interest statements) | DR-0040 |
| GLEIF LEI + relationships | Documentary source + identifier type | DR-0040 |
| ISO 20275 (legal forms) | Reference | WP 0.7 |
| HS/CN, ECCN, EU dual-use lists | Reference (classification systems, contextual) | DR-0042 |

## Governance & publishing (WS7)

| Standard | Disposition | DR / note |
|---|---|---|
| ISO 15489 (records mgmt) | Adopt-pattern (document control) | DR-0046 |
| ISO 10007 / CM tradition | Adopt-pattern (baselines) | DR-0048 |
| ISO/IEC 11179 | Adopt-pattern (registry) | DR-0050 |
| SKOS | Adopt | DR-0050 |
| TBX / ISO 30042 | Study (at first professional translation) | DR-0050 |
| DCAT 3 | Adopt | DR-0049 |
| DataCite | Adopt when release practice mature | DR-0049 |
| SemVer | Adopt for code/APIs/schemas only | DR-0047 |
| Schema.org | Publication/discovery mapping only — rejected as master | WP 0.1 |
| Dublin Core | Interoperability mapping only — rejected as master | WP 0.1 |
| Git | Governance-document store; rejected as universal history store | WP 0.1, DR-0046 |
| RDF/OWL | **Defer** — canonical-representation decision reserved for Phase III (§95) | Q-01 |
