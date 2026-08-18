# POL-0001 — Personal Data Policy

**Class:** POL (DR-0046 control) | **Version:** 0.1 | **Status:** Draft — proposed
**Approval:** pending founder review | **Effective:** upon approval
**Supersedes:** — | **Superseded by:** —
**Fulfils:** record §13, LEGAL-009, Q-35; releases the interim constraints of DR-0071 on the terms in §9 below.
**Governed by:** DR-0055 (append-only, governed redaction), DR-0066 (three gates), DR-0069 (quarantine), SEC-001/003, §10 (graphic material), §12 (access tiers), §14 (rights).

### AI provenance (record §80)

Drafted 2026-08-16 by an AI assistant (Anthropic Claude Code agent session)
at the founder's direction. **This is not legal advice.** The drafter is not
a lawyer; §10 makes external legal review a condition of the policy's
operation at scale. Candidate until approved.

---

## 1. The governing distinction

Record §13's first sentence carries the policy's core: *raw material may
contain personal information, but unnecessary personal data should not
automatically become searchable structured data.*

This yields **three independent decisions**, not two:

| Decision | Question | Gate |
|---|---|---|
| **Preserve** | Do we keep this material, containing whatever it contains? | Gate 1 (DR-0066) |
| **Structure** | Do we promote a person's data into queryable fields — names, identifiers, locations, relationships? | Gate 2 |
| **Publish** | Does this personal data appear on a public surface, at which access tier? | Gate 3 |

A "yes" at one gate never implies a "yes" at the next. **The structuring
decision is the one this policy exists to govern**: preservation is usually
permissible and often obligatory; publication is already gated; structuring
is where a document quietly becomes a surveillance index.

## 2. Legal framework the policy is tested against

The project is European-based and processes personal data about people in
Ukraine, Russia, and elsewhere. The relevant framework — stated as the test
the policy must pass, **not as a legal conclusion**:

- **GDPR Art. 6(1)(f)** legitimate interests, and **Art. 89** safeguards for
  archiving in the public interest and historical/scientific research, are
  the project's expected primary basis.
- **Art. 9** special categories (political opinions, religious belief,
  health, sexual life, biometric and genetic data, racial or ethnic origin)
  require an **Art. 9(2)(j)** archiving/research exception and heightened
  safeguards.
- **Art. 10** restricts data on criminal convictions and offences — directly
  relevant to atrocity and sanctions-evasion documentation.
- **Art. 85** member-state provisions reconciling data protection with
  freedom of expression and information, including journalistic and academic
  purposes.
- **Art. 17(3)(d)** limits erasure where processing is necessary for
  archiving in the public interest or historical research.
- **Recital 27:** the GDPR does not apply to the deceased; member states may
  legislate. The project applies a dignity standard regardless (§5.7).
- **Geneva Convention III, Art. 13:** prisoners of war must be protected
  against insults and **public curiosity** — a constraint routinely ignored
  in open-source practice and binding on this project's editorial conduct
  regardless of its own legal obligations.

## 3. Standing principles

1. **Purpose limitation by role.** Personal data is structured only where the
   person's relationship to the documented events makes it necessary — not
   because it was technically extractable.
2. **Preservation ≠ structuring ≠ publication** (§1).
3. **Identification is a decision, not a by-product.** Naming a person in a
   project assertion is an editorial act subject to review at the tier the
   subject demands (§78, DR-0063).
4. **Asymmetric caution for the vulnerable.** Where a person's category is
   uncertain, the more protective treatment applies until determined.
5. **Risk is contextual.** Identification carries state-actor risk for people
   in Russia and in occupied territory; the same datum may be innocuous for
   a Western official and dangerous for a Kherson resident.
6. **No silent inference.** Deriving a person's location, affiliation,
   health, ethnicity, or beliefs from data is a project assertion under
   DR-0024, with evidence and review — never an automated enrichment.

## 4. Special-category and high-risk data

The following are **never structured automatically**, by any collector or
enrichment process, for any category of person:

- special-category data under GDPR Art. 9 (political opinion, religious
  belief, health, sexual life, biometrics, ethnicity);
- criminal-offence data about individuals (Art. 10) — except where it is the
  **authoritative record itself** (a published indictment, judgment, or
  designation), typed per §62–63 as a legal finding or allegation;
- contact details, identity-document numbers, precise home addresses, and
  vehicle registrations of private individuals;
- precise location data of living private individuals;
- facial-recognition-derived identifications.

Any structuring of these requires an explicit, recorded editorial decision
citing necessity — never a pipeline default.

## 5. Treatment by category

Record §13's categories, resolved against the three decisions. "Structure"
means promoting the person into queryable fields; "publish" means appearing
on a public surface.

### 5.1 Public officials and commanders (in official capacity)
**Preserve:** yes, default. **Structure:** yes — name, office, tenure, role
(DR-0013), official acts. **Publish:** yes, default.
Rationale: the exercise of public power is the project's subject matter;
expectation of privacy in official acts is minimal. Private life remains out
of scope unless it is itself evidence (e.g., undisclosed assets in a
sanctions-evasion investigation).

### 5.2 Sanctioned persons and entities
**Preserve:** yes. **Structure:** yes — designation records are published by
authorities and carry official identifying data (DR-0039). **Publish:** yes.
The identifying data structured is that which the designating authority
published; the project does not augment it with private-life data absent
documented necessity.

### 5.3 Investigative subjects (not designated, not officials)
**Preserve:** yes. **Structure:** yes, with **T1 identity review** (DR-0063)
and necessity recorded. **Publish:** only through the editorial gate, with
allegations typed as allegations (§62–63) and never as findings.
This is the category where the project most risks harming someone who turns
out to be innocent; the argument scheme's critical questions (DR-0034) apply.

### 5.4 Rank-and-file combatants
**Preserve:** yes. **Structure:** restricted — only where the individual is
relevant to a specific documented act, order, or unit fact; not as a
population. **Publish:** restricted, with **Geneva III Art. 13** governing:
no publication that exposes an identified prisoner of war to public
curiosity, and no gratuitous identification of individual soldiers absent a
documented act.
Rank-and-file personnel are simultaneously potential perpetrators, potential
victims, and potential prisoners; the project does not build a personnel
index of an army.

### 5.5 Victims
**Preserve:** yes — victim documentation is core purpose. **Structure:**
only where identification serves a documentation or accountability purpose
(a named victim in an authoritative record, a documented deportation case),
never as a by-product of extraction. **Publish:** see the decision at §8.1.
Surviving relatives in occupied territory can be endangered by a published
name; re-traumatization is a real harm even where no legal duty binds.

### 5.6 Witnesses
**Preserve:** yes, at restricted access. **Structure:** **no, by default** —
witness identity is held in the separable confidential store (SEC-001,
DR-0069) under pseudonymous ID, not in the research graph. **Publish:**
never by default; publication requires a recorded decision, and informed
consent where the witness is reachable and consent is meaningful.
Witnesses face the most direct physical risk from identification.

### 5.7 Minors
**Preserve:** yes, restricted. **Structure:** no, except where a minor's
identity is legally significant and unavoidable (e.g., a named deported
child in an official record or ICC proceeding). **Publish:** strong
presumption against; requires a recorded decision citing necessity.
The presumption applies regardless of which other category the minor also
falls into, and survives the child reaching majority in already-published
material only by review.

### 5.8 Ordinary civilians incidentally present
**Preserve:** yes, as part of the source (removing them would falsify the
record). **Structure:** no. **Publish:** no as individuals; where a
derivative is published, consider face and identity redaction in the
derivative — the original stays intact in the archive (DR-0055).

### 5.9 Deceased persons
Outside GDPR by Recital 27, inside the project's dignity standard: no
gratuitous publication of identifiable remains or death imagery; §10's
graphic-material restrictions apply; family interests are weighed in
publication decisions.

## 6. Data-subject requests

The project accepts and records requests for access, rectification, erasure,
and objection.

- Requests are **logged, assessed, and answered** with a recorded rationale,
  whether granted or refused.
- Where the archiving/research derogations (Art. 17(3)(d), Art. 89) are
  invoked to refuse or limit a request, **the reason is recorded and the
  requester told which basis was applied**.
- **Rectification** normally means adding a superseding assertion, not
  editing history (DR-0055) — the record shows both what was held and what
  corrected it.
- **Erasure**, where granted, follows the **governed redaction** path
  (DR-0055): content removed, tombstone retained recording the fact, date,
  authority, and grounds.
- Requests never silently alter published releases; effects on releases are
  recorded in change sets (DR-0048, §91).

## 7. Operational safeguards

- **Structuring defaults are per-source** (DR-0067) and default to the more
  protective setting for sources whose content is predominantly private
  individuals.
- **Access tiers** (§12) apply independently: restricted personal data is
  inaccessible below its tier at every layer, including derived projections
  (DR-0054) and search indexes.
- **Enrichment outputs touching persons are proposals** (AI-001, DR-0063);
  no person enters the graph by automation alone.
- **Review cadence:** personal data held at `medium-term` (DR-0068) is
  re-decided at its review date; `metadata-only` records are checked for
  drift into de-facto identification.
- **Training and pipeline changes** that would newly structure personal data
  require a recorded decision before deployment.

## 8. Decision points requiring the founder's ruling

### 8.1 Victim identification in public outputs
- **(a) Already-public standard (recommended):** the project names a victim
  publicly only where an authoritative or already-public source has named
  them (official record, court document, family's own public statement), or
  where the family has consented.
- **(b) Documentation-necessity standard:** the project may name where
  documentation or accountability requires it, even if not previously
  public.
- **(c) Never name:** public outputs never identify individual victims;
  identification remains internal for accountability use.

### 8.2 Identification of individual soldiers in documented acts
- **(a) Documented-act standard (recommended):** an individual combatant may
  be identified publicly where specific, reviewed evidence ties them to a
  specific documented act, typed as allegation unless a legal finding exists
  (§62); never for mere presence or unit membership; Geneva III Art. 13
  constraints on prisoners always apply.
- **(b) Conservative:** no public identification of individual rank-and-file
  personnel at all; identifications held internally for prosecutorial use.
- **(c) Permissive:** identification permitted wherever evidence supports it,
  including unit membership in units implicated collectively.

### 8.3 Primary legal posture
- **(a) Archiving/research primary, expression secondary (recommended):**
  the project presents itself as a public-interest archive and research
  infrastructure under Art. 89 with Art. 9(2)(j), invoking Art. 85
  expression provisions secondarily.
- **(b) Journalistic/expression primary:** relies mainly on Art. 85
  provisions.
- **(c) Both co-equal**, documented per processing purpose.

## 9. Release of the DR-0071 interim constraints

On this policy taking effect, the DR-0071 constraints lift as follows:

- **(a) Registered sources only** — **partially lifted**: collection may
  extend to systematic capture within registered source *domains* (e.g., all
  posts of a registered channel), but open-ended crawling of the general web
  and untargeted social harvesting remain prohibited.
- **(b) No automatic promotion into structured fields** — **retained and
  refined**: §4 and §5 now govern what may be structured, by category; the
  prohibition on automated structuring of special-category and high-risk data
  is permanent.
- **(c) No at-scale submission intake** — **lifted** conditionally on the
  quarantine and confidential-identity machinery (DR-0069) being operational
  and tested.

## 10. Legal review — a condition, not a footnote

This policy is drafted by a non-lawyer. Before collection at scale touching
living private individuals, the project obtains **external legal review** in
its establishment jurisdiction covering: lawful basis and Art. 89
safeguards; Art. 9/10 handling; the applicable member-state Art. 85
provisions; data-subject request procedure; retention; and any DPIA
obligation. The review's outcome is recorded, and this policy is revised to
match it. **Until that review is recorded, §9's releases do not take
effect** — the DR-0071 constraints continue to bind.

## 11. Review

This policy is reviewed annually and on any material change to collection
scope, jurisdiction, or applicable law; the review is recorded as a version
under DR-0046/DR-0047.

## 12. Candidate Decision Records

- **CDR-P3-19:** Adopt POL-0001 with the founder's rulings at §8, the
  three-decision model (§1), the never-auto-structure list (§4), the
  category treatments (§5), the data-subject procedure (§6), and the
  conditional release of DR-0071 (§9) — conditioned on the legal review of
  §10.
