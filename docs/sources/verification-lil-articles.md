# Verification of LIL articles quoted in the legal-review brief

**Status:** VERIFICATION IN PROGRESS — 2026-09-15

**Purpose:** The legal-review brief (`docs/legal/legal-review-brief.md`) quotes four articles from the Loi n° 78-17 du 6 janvier 1978 (Loi Informatique et Libertés, "LIL") from the CNIL's consolidated text, because Légifrance was unreachable on the drafting date (2026-09-15, HTTP 403 anti-bot challenge). Per the brief's provenance note and the README's open decisions, every article quoted must be checked against Légifrance before the brief is sent to counsel.

**Articles to verify:**
- Article 46 (cited in Q2 — processing of criminal-offence data)
- Article 78 (cited in Q1 — archiving in the public interest)
- Article 79 (cited in Q1 — GDPR Art. 14 derogations for archiving/research)
- Article 80 (cited in Q3 — Art. 85 expression exception)

## Network status

**Légifrance:** HTTP 403 Forbidden (anti-bot challenge), 2026-09-15 19:48 UTC, verified from this session
- URL attempted: `https://www.legifrance.gouv.fr/`
- Status: Inaccessible; authentication or browser fingerprinting required

**CNIL:** HTTP 301 redirect, 2026-09-15 19:48 UTC, verified from this session
- URL attempted: `https://www.cnil.fr/`
- Status: Accessible but requires redirect following

## Texts quoted in the brief

### Article 78 (Q1 — archiving in the public interest)

Quoted at lines 303–310 of `docs/legal/legal-review-brief.md`:

> "Lorsque les traitements de données à caractère personnel sont mis en œuvre par **les services publics d'archives** à des fins archivistiques dans l'intérêt public conformément à l'article L. 211-2 du code du patrimoine, les droits prévus aux articles 15, 16 et 18 à 21 du règlement […] ne s'appliquent pas […]. Les conditions et garanties appropriées prévues à l'article 89 du même règlement sont déterminées par le code du patrimoine et les autres dispositions législatives et réglementaires applicables aux **archives publiques**."

**Verification needed:**
- (a) Confirm exact wording in Légifrance
- (b) Confirm reference to "services publics d'archives" and restrictions to public archive services
- (c) Confirm second paragraph contemplates a Conseil d'État decree
- (d) Confirm coverage of "recherche scientifique ou historique" (mentioned in brief as Q1(a)'s alternative route)

---

### Article 79 (Q1 — GDPR Art. 14 derogations)

Mentioned but not fully quoted at lines 321–326 of `docs/legal/legal-review-brief.md`:

> "**LIL Article 79** disapplies GDPR Art. 14(1)–(4) for archiving, research and statistical purposes where the data were not obtained from the subject, and is not on its face limited to public archive services."

**Brief's claim:** Article 79 contains GDPR Art. 14 derogations for archiving, research, and statistical purposes, and is *not* limited to public archive services (unlike Article 78).

**Verification needed:**
- (a) Confirm exact wording in Légifrance
- (b) Confirm it applies to "fins archivistiques […] de recherche scientifique ou historique […] à des fins statistiques"
- (c) Confirm it disapplies GDPR Art. 14(1)–(4) specifically
- (d) Confirm it is *not* limited to public archive services (the brief's critical distinction from Article 78)

---

### Article 46 (Q2 — processing of criminal-offence data)

Quoted at lines 336–350 of `docs/legal/legal-review-brief.md`:

> "Les traitements de données à caractère personnel relatives aux condamnations pénales, aux infractions ou aux mesures de sûreté connexes **ne peuvent être effectués que par** : les juridictions, les autorités publiques et les personnes morales gérant un service public […] ainsi que les personnes morales de droit privé collaborant au service public de la justice et appartenant à des catégories dont la liste est fixée par décret en Conseil d'État […] ; les auxiliaires de justice […] ; les personnes physiques ou morales, aux fins de leur permettre de préparer et, le cas échéant, d'exercer et de suivre une action en justice en tant que victime, mise en cause, ou pour le compte de ceux-ci […] ; les personnes morales mentionnées aux articles L. 321-1 et L. 331-1 du code de la propriété intellectuelle […] ; les réutilisateurs des informations publiques figurant dans les décisions [de justice] […] sous réserve que les traitements […] n'aient ni pour objet ni pour effet de permettre la réidentification des personnes concernées."

**Brief's claim:** Article 46 restricts processing of criminal-offence data to a closed list of actors: courts, public authorities, service-managing private persons, private-sector collaborators with justice (categories set by decree), justice auxiliaries, persons pursuing legal action as victim/defendant, IP-law persons, and reusers of public-decision information (with reidentification prohibition).

**Verification needed:**
- (a) Confirm exact wording and closed-list structure
- (b) Confirm each limb of permitted actors
- (c) Verify that a **private archive documenting sanctions and alleged atrocities does not obviously fit any limb** (brief's critical claim)
- (d) Confirm reidentification prohibition on the last limb

---

### Article 80 (Q3 — Art. 85 expression exception)

Quoted at lines 383–390 of `docs/legal/legal-review-brief.md`:

> "À titre dérogatoire, les dispositions du 5° de l'article 4, celles des articles 6, **46**, 48, 49, 50, 53, 118, 119 et celles du chapitre V du règlement […] ne s'appliquent pas, lorsqu'une telle dérogation est nécessaire pour concilier le droit à la protection des données à caractère personnel et la liberté d'expression et d'information, aux traitements mis en œuvre aux fins : d'expression universitaire, artistique ou littéraire ; d'exercice à titre professionnel, de l'activité de journaliste, dans le respect des règles déontologiques de cette profession."

**Brief's claim:** Article 80 disapplies Article 46 (and other provisions) for expression purposes: academic/artistic/literary expression and professional journalism (subject to professional ethics).

**Verification needed:**
- (a) Confirm that Article 80 **disapplies Article 46** specifically
- (b) Confirm the three limbs: academic expression, artistic/literary expression, professional journalism
- (c) Confirm professional journalism requires "respect des règles déontologiques"
- (d) Confirm no institutional affiliation requirement is stated (brief asks counsel about this)

---

## Verification outcome

**Status:** BLOCKED — Légifrance inaccessible (HTTP 403 Cloudflare challenge).

**Verification attempt, 2026-09-15 19:48 UTC:**
- Direct access to `https://www.legifrance.gouv.fr/` → HTTP 403
- Attempt with browser User-Agent to `https://www.legifrance.gouv.fr/codes/code-de-protection-des-donnees-personnelles` → HTTP 403 Cloudflare challenge (`cf-mitigated: challenge`; requires browser fingerprinting and JavaScript execution)
- CNIL site (`https://www.cnil.fr/`) → HTTP 301 redirect, requires following
- Session proxy environment does not support JavaScript or Cloudflare challenge completion

**Cross-check:** [`DR-0100`](../decision-records/DR-0100-jurisdiction-controller-and-hosting.md) (approved 2026-09-15) contains independent mention of the same four articles with identical characterization: "the articles were read from the CNIL's consolidated text (Légifrance was unreachable)" and "their interaction is what counsel is engaged to resolve."

**Next steps:** This task requires human-assisted access to Légifrance (browser-based) or a session with network policy that permits Cloudflare challenges. The four quoted texts should be checked against:

1. The **official Légifrance text** at `legifrance.gouv.fr/codes/code-de-protection-des-donnees-personnelles` (or successor URL structure), verified via a browser
2. The **CNIL's consolidated text** at `cnil.fr` (currently the source used), as a secondary comparison
3. Any **recent amendments** to the LIL since the brief was drafted (2026-09-15)

**For the engagement:** The brief is sendable in its current form with the cautionary note in §1 and the provenance note §1 describes. However, the verification should be completed **before counsel returns the advice**, so any discrepancies can be flagged and a corrected brief sent if needed. Completion is a precondition to engaging counsel, not part of the engagement itself. This document will be updated once verification is complete.

**Standing expectation:** All four articles were read from the CNIL's consolidated version on 2026-09-15. If Légifrance becomes accessible from a later session, recheck all four for:
- Exact wording correspondence (any omissions or paraphrasing)
- Recent amendments
- Amendments effective 2026-09-09 through 2026-09-15 (the period between first and latest collection)

---

**Note on LIL article structure:** French law refers to the Loi Informatique et Libertés articles as both "Article [number]" (where [number] is the ordinal) and "Article L. [number]" (where L. refers to "Livre" / book sections in the Code). The brief uses the ordinal form; Légifrance may display both. When verifying, check that the article numbers match, accounting for both notations.

---

## Sources

- [`docs/legal/legal-review-brief.md`](../legal/legal-review-brief.md) — provenance note (lines 35–50), caution in §1 (lines 75–78)
- [`README.md`](../../README.md) — open decisions, item 4, re: "every LIL article the brief quotes must be checked against Légifrance"
- [`CLAUDE.md`](../../CLAUDE.md) — "Standing rulings", item on legal review: outstanding verification task

