# Phase II Output 3 — Conceptual Conflict Register (candidate, consolidated)

Consolidated from WP 0.2–0.8. Resolutions become semantic-registry entries
(DR-0050) on approval. "Never bare" = the word never appears unqualified in
specifications or canonical data.

| # | Term | Colliding senses | Resolution | Origin |
|---|---|---|---|---|
| C-01 | provenance | Archival origin/custody vs PREMIS events vs PROV derivation vs legal chain of custody | Always qualified: acquisition/preservation/derivation provenance; custody history | WP 0.2 |
| C-02 | event | PREMIS (action on archived object) vs CRM (historical occurrence) | Hard layer separation (DR-0004) | WP 0.2 |
| C-03 | agent | PREMIS/PROV pipeline agent vs historical actor | Separate registries/links (DR-0004); registry cross-reference | WP 0.2 |
| C-04 | object | PREMIS digital object vs physical object (§21) | "Digital object" vs "physical object" | WP 0.2 |
| C-05 | archive | OAIS organization vs web archive vs project corpus | Registry definitions | WP 0.2 |
| C-06 | fixity / integrity / authenticity | Bit-sameness vs copy soundness vs genuineness (§38) | Three separate assessments; never inferred from one another | WP 0.2 |
| C-07 | version | Source version vs object version vs release vs document vs annotation target state | One registry entry enumerating DR-0047's regimes | WP 0.2/0.4/0.8 |
| C-08 | work | LRMoo F1 vs colloquial | "Work" capitalized = F1 sense in technical documents | WP 0.3 |
| C-09 | item | LRMoo F5 exemplar vs PREMIS object vs colloquial | Item = documentary exemplar; preserved substance = PREMIS vocabulary | WP 0.3 |
| C-10 | document | CRM E31 breadth vs colloquial | Registry-qualified | WP 0.3 |
| C-11 | period | CRM E4 (phenomenon) vs time interval | E4 sense includes the happening | WP 0.3 |
| C-12 | observation | CRMsci S4 vs intelligence usage vs §30 category | §30 sense subsumes; instrument observations add §49 metadata | WP 0.3/0.5 |
| C-13 | annotation | W3C model vs editorial note vs TEI markup | Unqualified = W3C sense | WP 0.4 |
| C-14 | fragment | Holdings fragment (§26) vs FragmentSelector | "Holdings fragment" vs "fragment selector" | WP 0.4 |
| C-15 | transcription / transcript | TEI diplomatic vs A/V transcript vs OCR output | Three derivative types with distinct PROV methods | WP 0.4 |
| C-16 | accessibility | Source accessibility (§27) vs archive access tier (§12) | Separate vocabularies; never one field | WP 0.4 |
| C-17 | canvas | IIIF surface vs colloquial | IIIF-scoped only | WP 0.4 |
| C-18 | confidence | Analytic confidence vs probability vs confidence interval | "Confidence" = analytic only (DR-0026) | WP 0.5 |
| C-19 | evidence | Legal admissible material vs claim-relative relation vs anything archived | Requires a proposition; otherwise "source" (§29) | WP 0.5 |
| C-20 | belief | CRMinf I2 technical vs colloquial | Technical sense in modeling only; avoided in publications | WP 0.5 |
| C-21 | finding | Project finding (§30) vs legal finding (§62) | Legal findings always jurisdiction-qualified | WP 0.5 |
| C-22 | verification | Copy integrity vs extraction vs authenticity vs truth (§81) | Never one flag; six-way split in registry | WP 0.5 |
| C-23 | argument | Reasoning structure vs dispute | Technical sense only | WP 0.6 |
| C-24 | attack | Argumentation conflict relation vs military attack | Always layer-qualified | WP 0.6 |
| C-25 | scheme | Argument scheme vs data schema | "Argument scheme" spelled out; "schema" = data structures | WP 0.6 |
| C-26 | support | Evidential (layer 3) vs inferential (layer 6) | Named distinctly in registry | WP 0.6 |
| C-27 | hypothesis | §30 category vs loose guess | §30 sense; member of a hypothesis set | WP 0.6 |
| C-28 | sanctioned | Colloquial vs designation vs effects vs rule-derived | Never a bare status; always decomposed (§73, DR-0038/0041) | WP 0.7 |
| C-29 | designation | Act vs record vs designated person | Three objects (DR-0039) | WP 0.7 |
| C-30 | control | Corporate vs territorial vs export control | Three registry entries; always qualified | WP 0.7 |
| C-31 | license | Export license vs rights license | Spelled out (§65 vs §14) | WP 0.7 |
| C-32 | program | Sanctions regime vs software | "Regime" preferred for legal sense | WP 0.7 |
| C-33 | list | Authority-published sanctions list vs any enumeration | "Sanctions list" reserved | WP 0.7 |
| C-34 | owner | Legal/beneficial/registered/nominee/colloquial | Never bare; BODS interest types govern (DR-0040) | WP 0.7 |
| C-35 | record | Records-management sense vs database record vs "the Phase I record" | Registry-qualified; unqualified never used in specifications | WP 0.8 |
| C-36 | baseline | CM frozen configuration vs colloquial | CM sense in governance documents (DR-0048) | WP 0.8 |
| C-37 | release | Project baseline+publication vs software release vs press release | Registry-defined; press releases are "publications" | WP 0.8 |
| C-38 | effective | Document-control effective date vs legal effective time | Two registry entries; never one field | WP 0.8 |
| C-39 | status | Document-control vs epistemic vs legal status | Class-qualified always | WP 0.8 |
