# DR-0042 — Export-control state is decomposed

**Category:** legal / architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W6-5, WP 0.7 §2.3/§6 | **Supersedes:** — | **Superseded by:** —

## Context

Record §65: "license required" ≠ "license absent" ≠ "violation established."
Record §66: regulatory classification is contextual (system, jurisdiction,
authority, validity; official vs declared vs analytical).

## Alternatives considered

1. Decomposed model (chosen).
2. Per-product "controlled" flags (rejected: the export-control analogue of
   the sanctions boolean, §64/§65).

## Decision

Export-control state decomposes into independent facts:

- **Classification assertions** — contextual: system (HS/CN, ECCN, EU
  dual-use, national), jurisdiction, asserting authority, validity period;
  official, declared, and project-analytical classifications are distinct
  assertion types (§66); classifications attach to **product types**
  (DR-0014), and to individuals only where evidence individuates.
- **Licensing requirements** — rule-derived assertions from classification +
  destination + end-use/end-user rules, versioned like DR-0041.
- **Authorizations** — licenses, general licenses/exceptions, denials,
  revocations as legal acts with parties, scope, and dates.
- **Violations** — exist only as legal findings with jurisdiction, authority,
  procedural posture (§62–63); project assessments of likely violation are
  project assertions under DR-0024, never merged with findings.

## Consequences

- Battlefield-component tracing (Common High Priority List goods) links item
  evidence (DR-0014) to classification and licensing analysis without
  overclaiming.
- Absence of licensing data is carried by absence states (DR-0029), which this
  domain will exercise heavily.
