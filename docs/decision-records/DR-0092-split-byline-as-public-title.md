# DR-0092 — A split's deciding agent is shown as a public title, snapshotted, never the agent row

**Category:** architecture / editorial / security | **Status:** Approved | **Decided:** 2026-09-09 by founder/principal editor
**Origin:** SPEC-0007 v0.3 §12 open question 2, put to the founder directly | **Supersedes:** — | **Superseded by:** —

## Context

DR-0089 §5 requires a split's disambiguation record to carry the deciding
agent, and the implementation does: `disambiguation_record.decided_by`
references `pipeline_agent`. But `pipeline_agent` is confidential tier as a
whole (SEC-001, §11), because it may include agents acting for confidential
sources, so the resolver withheld the decider's identity from the public
response and said only that the agent is recorded. Record §85 pulls the
other way: editorial acts should be inspectable, and `publication_decision`
already discloses its rationale on exactly that reasoning.

## Alternatives considered

1. **A public role or title, snapshotted onto the record itself, never the
   agent row** (chosen).
2. Withhold it entirely — the status quo pending this ruling. Rejected:
   leaves §85's inspectability goal permanently unmet for this one
   editorial act, when a cheap way to meet it exists.
3. Render the agent's name directly. Rejected: breaks the confidentiality
   tier rule for `pipeline_agent` (SEC-001) and risks deanonymizing an
   agent who elsewhere acts for a confidential source — the table is
   confidential as a whole precisely because which agents are which is not
   safe to disclose piecemeal.

## Decision

`pipeline_agent` gains a nullable `public_title` column — a role or title
an agent has chosen to carry on a public editorial act, e.g. "principal
editor". It is opt-in: software agents and any person without a chosen
title simply have none.

`disambiguation_record` gains `decided_by_title`, populated by a database
trigger at insert from the deciding agent's `public_title` — never supplied
by application code, so the register cannot be asked to publish a title
nobody chose. It is fixed at the moment of the split: `disambiguation_record`
rows are made immutable after insert (a dedicated guard, the same discipline
DR-0055 applies to assertions), so a title changed later does not rewrite
what a past decision's byline said.

The resolver renders `decided_by_title` when present ("Decided by
principal editor.") and falls back to the prior wording — the agent is
recorded without being named — when absent. `decided_by` itself never
reaches a resolver response; only `decided_by_title` does, and
`disambiguation_record` was already public tier, so no tier rule changes.

This resolves SPEC-0007 v0.3 §12 open question 2.

## Consequences

- `pipeline_agent` carries one more nullable column; existing rows have no
  title and the resolver's fallback wording is unchanged for them.
- A founder or editor who wants editorial acts attributable sets their own
  `public_title` once; nothing else needs to change per split.
- The pattern — snapshot a derived public fact onto an already-public
  record rather than exposing a join into a confidential table — is
  available the next time a confidential-tier agent's action needs a public
  face (e.g., a future publication-decision byline), without reopening
  SEC-001.
