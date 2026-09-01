# Source candidates

This directory holds **informal candidate-source notes** — a place to record
that a potential source has been identified and preliminarily assessed,
before it becomes anything governed.

## What this is not

- **Not** the source registry required by [DR-0067](../decision-records/DR-0067-source-registry-schema.md).
  DR-0067 approved a *schema* (SPEC-0003 §3); no instance store for source
  registry entries has been built or decided (format, location, whether it
  lives in the canonical database or a config file). That is an open
  implementation question for Phase III, not resolved here.
- **Not** an authorization to collect. Per [DR-0071(a)](../specifications/SPEC-0003-collection-pipeline.md),
  collection from unregistered sources is refused outright by the pipeline
  itself. A note in this directory does not register anything.
- **Not** a Decision Record. Nothing here is enacted; nothing here binds
  future work. These are working notes so candidate sources aren't lost
  between identification and formal registration.

## What a candidate note should contain

Loosely structured around the SPEC-0003 §3 field groups (identity, context,
collection policy, preservation policy, access/sensitivity, rights, triage
grade, declared dependence) so that promoting a candidate to a real registry
entry later is a transcription, not a re-investigation — but nothing here
commits to that schema's final storage form.

Each note should state plainly what has and has not been verified (this
session had no live network access to the source itself unless noted
otherwise).
