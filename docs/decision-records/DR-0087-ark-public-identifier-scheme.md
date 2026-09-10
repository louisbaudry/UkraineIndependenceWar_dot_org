# DR-0087 — ARK as the public identifier scheme

**Category:** architecture / preservation | **Status:** Approved | **Decided:** 2026-09-09 by founder/principal editor
**Origin:** CDR-P3-36, [WP 3.5](../phase-3/working-papers/wp-3.5-identifier-design.md) §3.1–3.3, §5 rule 1 | **Supersedes:** — | **Superseded by:** —

## Context

Record §15 requires stable public project identifiers and permanent
resolvable URLs for citable research objects, and forbids freezing a custom
identifier syntax "without researching established patterns first".
DR-0022 deferred identifier syntax and resolvers to "a separate, later
decision". WP 3.5 is that research: it compared ARK, DOI, Handle, URN and
UUID against §15, PRES-009 (the archive is reconstructible without the
website), DATA-009 (every published identifier resolves forever) and the
redirect, disambiguation and tombstone behaviours already required by
DR-0064 and DR-0077.

## Alternatives considered

1. **ARK under a project NAAN with a project-run resolver, registered with
   N2T as backup** (chosen).
2. Opaque project URLs with no scheme (rejected: identity bound to the
   domain; no resolver chain for succession; every persistence rule
   re-derived from scratch).
3. DataCite DOIs for all citable objects (rejected: fees per object; the
   open-metadata landing-page rule cannot be met for restricted-tier
   objects; DR-0049 already scopes DOIs to dataset releases at maturity).
4. A Handle prefix and local handle server (rejected: DOI's substrate
   without its ecosystem; infrastructure to run; no opacity or persistence
   conventions; Informational RFC without IETF consensus).
5. A formal URN namespace (rejected: IANA review for a namespace that
   resolves nowhere; the resolver of option 1 would still be needed).
6. Publishing the internal UUIDs (rejected: no check character, no
   persistence semantics, collapses §15's internal/public distinction).

## Decision

**Public identifiers are ARKs under a Name Assigning Authority Number
(NAAN) requested for the project.**

- Names are **opaque**, betanumeric, and end in a check character. They
  encode no type, name, date, tier, status or classification (the
  Cool-URIs exclusion list; DR-0062 and DR-0064 make any of these wrong
  for the object eventually).
- The **citation form is `ark:/NAAN/name`**. The hostname of the URL form
  is identity-inert: two URLs differing only in host are the same
  identifier.
- The project **operates its own resolver** on its domain and **registers
  it with N2T** so the ARK resolver chain can find it and a successor can
  take it over at hand-over.
- §15's research-first obligation is recorded as met by WP 3.5 §2; the
  deferral in DR-0022 is discharged.

## Consequences

- PRES-009 holds for identifiers: a citation outlives the domain and the
  website.
- A NAAN must be requested before the first public identifier is minted
  (WP 3.5 §8 Q1 — timing is operational).
- The name-generation algorithm, check-character rule and resolver HTTP
  contract are specified in **SPEC-0007 — Public Identifiers and
  Resolution**, which DR-0087…0091 authorise.
- Internal UUIDs remain primary keys and are never published as
  identifiers (DR-0088).
