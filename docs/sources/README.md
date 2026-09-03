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
