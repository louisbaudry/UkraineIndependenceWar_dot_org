# DR-0069 — Quarantine as a pre-archival zone

**Category:** security / architecture | **Status:** Approved | **Decided:** 2026-08-16 by founder/principal editor
**Origin:** CDR-P3-16, SPEC-0003 §5 | **Supersedes:** — | **Superseded by:** —

## Context

Record §11 requires controlled evidence intake with quarantine, original-file
preservation, malware and security checks, provenance assessment, privacy
and legal review, submitter claims kept separate from project conclusions,
and architecturally separable confidential source identity (SEC-001/002).

## Alternatives considered

1. Quarantine as a zone outside the archive, preceding Gate 1 (chosen).
2. Ingest first, assess later (rejected: unvetted material would inherit the
   archive's integrity claims, and malware would enter preserved storage).
3. Defer the submission machinery (rejected: the separability of confidential
   identity must exist before the first confidential source, not after).

## Decision

Acquired material — automated fetches and third-party submissions alike —
lands in a **quarantine zone that is not part of the archive**: original
bytes and submission metadata are held, malware and format checks run, and
provenance plus legal/privacy exposure are assessed before Gate 1
(DR-0066). **Archive integrity guarantees are never claimed for quarantined
material.**

For third-party submissions: **submitter claims are preserved separately
from project conclusions** (§11); confidential submitter identity lives in
the separable confidential store (SEC-001, DR-0059) and is referenced only
by pseudonymous submitter ID.

## Consequences

- The archive's guarantees mean what they say, because nothing enters it
  unchecked.
- Confidential-source protection is structural from the first submission.
- Quarantine holdings are not archival holdings: they carry no §26
  completeness claim until they pass Gate 1.
