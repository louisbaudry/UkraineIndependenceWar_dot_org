# Working instructions for Claude

## How to ask the founder a question

**This is the standing instruction for every question, without exception.**

When anything needs a decision from the founder/principal editor:

1. **One question at a time.** Never batch questions into a single message.
   Ask, wait for the answer, then ask the next.
2. **Propose multiple concrete choices.** Not "what would you like to do?" —
   named options, each with what it means and what it costs.
3. **State a recommendation.** Say which option is best and why. A menu with
   no recommendation pushes the analysis back onto the founder, which is the
   opposite of the point.
4. **Give enough context to answer without scrolling back.** The question
   should be answerable on its own terms.

This applies to Decision Records, specification choices, policy rulings,
methodology questions, branch and merge decisions, and ordinary implementation
forks alike. It is not reserved for large decisions.

### Why

Record §78–79: the founder is final editorial authority, and AI proposes
while humans decide. A proposal with no options is not a proposal, and a set
of options with no recommendation is not analysis. Asking one at a time keeps
each decision separable and separately recorded — which is what the Decision
Record system requires.

### What does not need a question

Routine judgment calls within work already directed: naming, file layout,
test structure, wording of code comments, which of two equivalent
implementations to use. Make the call, mention it, and move on. Reserve
questions for choices that would change what gets built or what the project
commits to.

## Governance context

- The [Phase I record](docs/discovery/phase-1-requirements-discovery-record.md)
  is immutable source material. Changes happen by supersession, never in-place
  edits (§77).
- Every enacted decision is a [Decision Record](docs/decision-records/README.md).
  Drafts are proposed and marked as such; nothing is enacted unilaterally.
- Controlled documents (DR, SPEC, POL, REQ, METH, PROC) carry explicit status
  under [DR-0046](docs/decision-records/DR-0046-unified-document-control.md).
  **Status is document metadata, never inferred from Git state** — a commit is
  not an approval, and a merge is not an enactment.
- AI-drafted documents carry an **AI provenance** note per §80 and remain
  candidates until the founder approves them.

## Reporting work

State what was verified and what was not. A test suite that has never been
seen to fail proves nothing — when a suite is added, check that it fails when
the thing it tests is broken, and say so. Where something could not be
verified in this environment (no network access to a live source, no external
legal review), say that plainly rather than implying it away.
