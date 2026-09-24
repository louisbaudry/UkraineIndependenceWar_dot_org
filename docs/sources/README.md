# Source candidates

This directory holds **informal candidate-source notes** — a place to record
that a potential source has been identified and preliminarily assessed,
before it becomes anything governed.

## What this is not

- **Not** the source registry required by [DR-0067](../decision-records/DR-0067-source-registry-schema.md).
  That registry's instance store now exists: candidate registrations are YAML
  entries under [`sources/candidates/`](../../sources/candidates/), validated and
  written into the `source` table by `sources/register.py --commit`. Notes in
  *this* directory are the step before that — prose assessments of sources for
  which no registration has been drafted.
- **Not** an authorization to collect. Per [DR-0071(a)](../specifications/SPEC-0003-collection-pipeline.md),
  collection from unregistered sources is refused outright by the pipeline
  itself. A note in this directory does not register anything.
- **Not** a Decision Record. Nothing here is enacted; nothing here binds
  future work. These are working notes so candidate sources aren't lost
  between identification and formal registration.

## What a candidate note should contain

Loosely structured around the SPEC-0003 §3 field groups (identity, context,
collection policy, preservation policy, access/sensitivity, rights, triage
grade, declared dependence) so that promoting a note to a candidate
registration in [`sources/candidates/`](../../sources/candidates/) is a
transcription, not a re-investigation.

Each note should state plainly what has and has not been verified — including,
where it applies, that the source could not be reached from the drafting
environment at all.

## Verification and measurement records

This directory also holds a second kind of note: records of what happened
when a candidate's locators, or an already-registered source's collection
run, were actually checked against something live. Same non-status as
candidate notes above — not a registration, not an authorization, not a
Decision Record — but grounded in a specific session's real commands and
real output rather than preliminary assessment.

- [`verification-eu-consolidated-list-ofac-sdn.md`](verification-eu-consolidated-list-ofac-sdn.md)
  — the 2026-09-08 rehearsal behind [DR-0093](../decision-records/DR-0093-first-source-registrations.md).
- [`verification-bis-dpl-ofsi-consolidated.md`](verification-bis-dpl-ofsi-consolidated.md)
  — `uk-ofsi-consolidated` (full) and `bis-entity-list` (Denied Persons List
  half only), behind `DR-0096`.
- [`verification-seco-sanctions.md`](verification-seco-sanctions.md) —
  `seco-sanctions`, found on a second attempt on a different host, behind
  `DR-0098`.
- [`verification-un-hrmmu-civilian-casualties.md`](verification-un-hrmmu-civilian-casualties.md)
  — `un-hrmmu-protection-of-civilians`, the UN monitoring mission's monthly
  civilian-casualty update, DR-0109 Decision 5 step 1. Not registered.
- [`TEMPLATE-a7-measurement-results.md`](TEMPLATE-a7-measurement-results.md)
  — not a record itself but the fill-in shape for one: WP 3.4 Track A item
  A7's storage-and-bandwidth measurement, covering both the two A1 sources
  already collected and one retrospective WARC pull for a registered
  domain. Copy it to `a7-measurement-results-YYYY-MM-DD.md` once
  [`docs/runbooks/A7-storage-bandwidth-measurement.md`](../runbooks/A7-storage-bandwidth-measurement.md)
  is actually run on the archive server, and list the result here
  alongside the entries above.
