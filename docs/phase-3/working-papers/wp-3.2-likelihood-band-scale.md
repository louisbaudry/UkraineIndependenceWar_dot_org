# Phase III / Study 2 — Likelihood Band Scale
## Working Paper 3.2

**Project:** Ukraine's Second War of Independence
**Status:** CANDIDATE — AI-drafted, awaiting founder review.
**Version:** 3.2
**Mandate:** Q-16 — fix the calibrated verbal probability scale that DR-0026 requires but deliberately left unset ("until then no probability wording in project outputs is canonical").
**Constraints inherited:** DR-0026 (two-dimensional uncertainty; likelihood separate from analytic confidence; no bare numerics), DR-0025 (vocabulary changes by DR), DR-0050 (registry + SKOS mappings, §60 multilingual governance), record §42–43 (resist false precision).

### AI provenance (record §80)

Drafted 2026-08-16 by an AI assistant (Anthropic Claude Code agent session)
at the founder's direction. Band definitions verified against primary
sources (§6). Candidate until approved.

---

## 1. The two mature scales

### ICD 203 (US Intelligence Community, 2015)

Seven **contiguous** bands spanning 1–99%:

| Term | Range |
|---|---|
| almost no chance | 01–05% |
| very unlikely | 05–20% |
| unlikely | 20–45% |
| roughly even chance | 45–55% |
| likely | 55–80% |
| very likely | 80–95% |
| almost certain | 95–99% |

ICD 203 also supplies a second synonym row (remote / highly improbable /
improbable / roughly even odds / probable / highly probable / nearly certain)
and forbids mixing rows without a disclaimer.

### PHIA Probability Yardstick (UK, 2018/2019)

Seven bands with **deliberate gaps** between them:

| Term | Range |
|---|---|
| remote chance | ~5% |
| highly unlikely | 10–20% |
| unlikely | 25–35% |
| realistic possibility | 40–<50% |
| likely / probably | 55–75% |
| highly likely | 80–90% |
| almost certain | ~95% |

The gaps are the design: they refuse to pretend a judgment can be placed at
52% rather than 55%, forcing commitment to a band rather than hair-splitting
at boundaries.

## 2. Which fits this project

The deciding consideration is **not** which scale is better tradecraft —
both are mature and mutually intelligible — but which behaves correctly as a
**controlled vocabulary in a validating data system**:

- **Contiguity matters here.** DR-0029 forbids silent nulls and DR-0026
  forbids bare numerics. With a gapped scale, a judgment the analyst places
  at 52% has *no* expressible band: they must round to a neighbouring term
  whose stated range excludes their actual estimate, or leave the field
  empty. ICD 203's contiguous coverage guarantees every judgment has exactly
  one home.
- **"Roughly even chance" is a real band the project needs.** Historical and
  attribution work produces genuine 45–55% judgments; PHIA's structure
  deliberately has no even-odds term (its "realistic possibility" tops out
  below 50%).
- **PHIA's "realistic possibility" is nonetheless a valuable term** — it
  names the "could well have happened, below even odds" region that ICD 203
  buries inside a wide "unlikely" band. It is worth preserving as a mapped
  equivalence, not lost.
- **Precedent within the project:** DR-0045 already established the pattern —
  one canonical model, mappings maintained outward. The same move applies
  here.

## 3. Recommendation

**Adopt the ICD 203 seven-band scale as the canonical likelihood vocabulary**,
with **PHIA equivalences recorded as SKOS mapping relations** in the registry
(DR-0050) so PHIA-sourced assessments — UK government reporting is a
significant source for this project — can be ingested, compared, and cited
without silent translation loss.

Supporting rules proposed with it:

1. **The numeric range is the anchor; the words are labels.** Every recorded
   assessment stores the band identifier; verbal rendering is presentation
   (DR-0022/§61). This makes multilingual publication safe: the band means
   the same thing in every language because the range, not the wording,
   carries the meaning.
2. **One synonym row only.** ICD 203's primary row (almost no chance … almost
   certain) is the project's; the alternative row is registered as synonyms,
   never mixed in a single product (ICD 203's own rule).
3. **Multilingual governance under §60.** Each band gets per-language
   preferred terms with **forbidden-translation notes** — the known traps
   include French *probable/vraisemblable*, Ukrainian and Russian renderings
   of "likely" that read as near-certainty, and any translation that turns
   "roughly even chance" into "possible."
4. **Attribution never inherits a band.** When the project reports another
   body's estimative language ("the ministry assessed it as highly likely"),
   that is a documentary assertion carrying *their* scale, mapped but not
   converted into a project judgment (§32, DR-0024).
5. **No band without a stated basis.** A likelihood band is part of an
   assessment (DR-0026) and requires the assessment's evidence and reasoning;
   bands never attach to bare data fields.

## 4. Candidate Decision Record

- **CDR-P3-12:** Adopt the **ICD 203 seven-band contiguous scale** as the
  canonical likelihood vocabulary, with PHIA equivalences as registry
  mappings, the primary synonym row only, §60 multilingual governance with
  forbidden-translation notes, band-identifier storage with rendering at the
  presentation layer, no inheritance of others' bands into project
  judgments, and no band without a stated basis. Resolves Q-16 and completes
  DR-0026.

## 5. Open questions raised

1. Whether the project ever publishes the numeric range alongside the term
   in public outputs (a presentation-layer choice; the tradecraft literature
   is split).
2. Retrospective vs predictive phrasing: both scales were designed for
   forward estimates; historical judgments may need scope notes clarifying
   that "likely" describes the project's credence about a past fact, not a
   forecast.

## 6. Sources

- ICD 203 primary text: [Analytic Standards, ODNI (PDF)](https://www.intelligence.gov/assets/documents/intelligence-community-directives/ICD_203.pdf); band summary corroborated in [ICD 203 reference compilation](https://github.com/wesinator/ICD203-intel-analysis)
- PHIA primary text: [PHIA Probability Yardstick, first edition (PDF, UK government)](https://assets.publishing.service.gov.uk/media/6421b6a43d885d000fdadb70/2019-01_PHIA_PDF_First_Edition_Electronic_Distribution_v1.1__1_.pdf)
- Comparative review: Dhami & Mandel, "UK and US policies for communicating probability in intelligence analysis: A review"
- Record §42–43; DR-0026, DR-0050
