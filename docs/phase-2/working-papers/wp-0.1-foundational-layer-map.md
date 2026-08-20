# Phase II — Theoretical Synthesis & Standards Mapping
## Working Paper 0.1 — Foundational Layer Map

**Project:** Ukraine's Second War of Independence  
**Status:** Phase II initiated  
**Version:** 0.1

## Phase II rule

Do not begin with database tables.

> **Which mature disciplines already possess the concepts required by Phase I, and which standards/models should we adopt, adapt, map to, defer, or reject?**

## Provisional conceptual layers

### A. Preservation / archival custody
Candidate standards: **OAIS, PREMIS, BagIt, WARC**

Questions: what exact objects are preserved, how fixity is maintained, how preservation events and rights are recorded, and how archival packages survive over time.

### B. General provenance
Candidate: **W3C PROV / PROV-O**

Questions: what entity was generated or derived by which activity, under responsibility of which agent; how transformations such as OCR, translation, AI enrichment, editorial review, dataset generation and publication are traced.

### C. Historical world model
Candidate: **CIDOC CRM**, with relevant extensions.

Questions: people, organizations, physical objects, places, events, processes, participation, time-spans and historical relationships.

### D. Documentary / bibliographic identity
Candidates: **IFLA LRM, LRMoo, BIBFRAME**, with **TEI** for deeply encoded textual material.

Questions: intellectual work/document, language/version, publication/manifestation, individual preserved copy and derived representation.

### E. Passage / annotation targeting
Candidate: **W3C Web Annotation**

Questions: how assertions and research notes point to exact paragraphs, image regions, pages, audio/video intervals or other source segments.

### F. Epistemic / assertion / evidence layer
No standard selected yet.

Research disciplines: epistemology, philosophy of science, historiography, intelligence analysis, legal evidence and scientific uncertainty.

### G. Argument / inference layer
No formalism selected yet.

Research disciplines: argumentation theory, formal logic, legal reasoning, Bayesian epistemology, intelligence analysis and computational argumentation.

### H. Sanctions / export-control legal layer
Must be grounded in actual EU, U.S., UK, UN and export-control legal structures rather than a generic `sanctioned` property.

### I. Research publication / citation
Candidates: **DataCite/DOI**, **CSL** and repository practices.

### J. Governance / records / configuration management
Dedicated standards study required for REQ, DR, POL, PROC, SPEC, METH, approval, effective dates, supersession, versioning and traceability.

## Initial standards matrix

| Standard / model | Initial disposition | Project role |
|---|---|---|
| OAIS / ISO 14721 | Adopt conceptually | Archival responsibilities and lifecycle |
| PREMIS | Adopt/map strongly | Preservation objects, events, agents, rights, fixity |
| W3C PROV | Adopt as interoperability foundation | General derivation, activity and agency provenance |
| BagIt / RFC 8493 | Adopt where useful | Reliable storage/transfer packages |
| WARC | Adopt selectively | High-value web capture preservation |
| CIDOC CRM / ISO 21127 | Deep study — high priority | Historical events/entities/relationships |
| IFLA LRM | Adopt concepts/map | Documentary and bibliographic identity |
| LRMoo | Deep study — high priority | Bridge between bibliographic and CIDOC CRM worlds |
| BIBFRAME | Compare/map | Bibliographic linked-data precedent |
| TEI P5 | Selective adoption | Rich scholarly textual encoding |
| W3C Web Annotation | Adopt/map strongly | Passage/image/timecode annotation |
| DataCite | Adopt for release layer | Dataset citation and persistent identifiers |
| CSL | Likely adopt | Citation rendering |
| Schema.org | Publication mapping | Web discovery/SEO, not canonical evidence model |
| Dublin Core | Interoperability mapping | Generic metadata, not master model |
| RDF/OWL | Defer persistence decision | Semantic representation possible; canonical role unresolved |

## Key synthesis

### OAIS, PREMIS and PROV are complementary

**OAIS** governs archival responsibilities and lifecycle.  
**PREMIS** describes preservation metadata and preservation events.  
**PROV** describes broader derivation, activities and agents.

Working principle:

> **Use PREMIS to describe preservation, PROV to describe broader derivation and agency, and OAIS to guide archival responsibility and lifecycle.**

### CIDOC CRM deserves central study

CIDOC CRM closely matches the project's historical/event requirements: actors, objects, events, time-spans, places, identifiers and participation. It is a strong conceptual candidate, but it must not yet be equated with the physical database schema.

### Documentary identity should not be reinvented

IFLA LRM and LRMoo provide mature distinctions corresponding to the Phase I requirement to separate intellectual work, language/version, publication/manifestation and individual copy.

### Web Annotation is highly relevant

It is a strong candidate for attaching evidence and research annotations to precise source segments rather than merely citing whole documents.

### Berkeley Protocol is methodologically central

The Berkeley Protocol should guide digital OSINT collection, preservation, verification, security, ethics and documentation. It should influence investigation methodology without becoming the entire historical ontology.

### Sanctions must remain legal-temporal

The authoritative sanctions ecosystem confirms that the project should model regimes, legal instruments, designations, effects, amendments/removals, rationale and derived applicability—not `sanctioned = true`.

## Standards that should not become the master ontology

**Schema.org:** publication/discovery layer only.  
**Dublin Core:** generic interoperability only.  
**Git:** excellent for code and governance documents, not a universal history store for evidence and live research data.

## Phase II research sequence

1. **Preservation & provenance:** OAIS, PREMIS, PROV, WARC, BagIt
2. **Historical/event knowledge:** CIDOC CRM, extensions, LRMoo
3. **Document identity & textual evidence:** IFLA LRM, LRMoo, TEI, Web Annotation
4. **Epistemology & evidence:** source assertions, project conclusions, uncertainty, verification
5. **Argumentation:** premises, conclusions, defeaters, competing hypotheses
6. **Sanctions/export controls:** authoritative legal structures and datasets
7. **Governance & versioning:** records management, configuration management, dataset/ontology releases

## Working hypothesis 0.1

The most promising conceptual composition currently appears to be:

**OAIS**
+ **PREMIS**
+ **W3C PROV**
+ **CIDOC CRM**
+ **IFLA LRM / LRMoo**
+ **Web Annotation / TEI where appropriate**
+ **DataCite**
+ a separately researched **epistemic/argumentation layer**
+ a domain-specific **sanctions/export-control layer** grounded in actual law.

This is a working hypothesis, **not an architectural decision**.

## No-go decisions at this stage

Do not yet:

- create the permanent database schema;
- create the permanent RDF ontology;
- choose RDF-first or relational-first canonical storage;
- choose a graph database;
- invent hundreds of custom relationship types;
- implement universal reliability scores;
- implement arbitrary numeric confidence scores;
- model sanctions as a boolean;
- allow AI-generated conclusions to become canonical silently;
- treat the public website as the archival source of truth.

## Next deliverable

**Phase II / Workstream 1 — Preservation & Provenance Concept Map**

Compare OAIS, PREMIS, PROV, WARC and BagIt against Phase I requirements for acquisition, immutable originals, fixity, custody, source lifecycle, transformation lineage, rights/access, failed acquisition, evidence packages, backup versus archive, succession and reproducibility.
