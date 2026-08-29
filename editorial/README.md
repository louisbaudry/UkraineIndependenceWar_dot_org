# Gate 2 — editorial acceptance

Implements SPEC-0003 §2 and §7 (DR-0066): the gate between a preserved
holding and canonical knowledge.

```
discovery → acquisition → [QUARANTINE] → GATE 1: preservation
    → preserved holding → normalization → enrichment → classification
    → GATE 2: editorial acceptance → canonical knowledge      ← this module
    → GATE 3: publication decision → published surface        ← not built
```

## The one thing this gate is for

**Nothing crosses on automated confidence alone.** Extractions and matches
arrive as proposals and become canonical only when a person accepts them, at
the risk tier the content demands. Material can be permanently preserved and
never cross Gate 2 — that is the normal case for bulk collection, not a
failure of it.

## Where the rules live

In the schema, not in this module. `05-editorial.sql` and `06-argument.sql`
hold the constraints, so they bind regardless of which code writes — a
future importer, a migration script, or someone at a `psql` prompt. `gate2.py`
is the path that makes the right thing convenient; it does not re-check what
the database already refuses, and it deliberately lets those exceptions
through rather than wrapping them in something friendlier.

| Rule | Where | Source |
|---|---|---|
| Only a person accepts | `acceptance_person_check` | AI-001, §79 |
| A person does not propose to themselves | `proposal_agent_check` | AI-003 |
| Consequential AI output carries provenance | `proposal_ai_provenance_check` | §80, AI-002 |
| A reviewer may raise a tier, never lower it | `acceptance_person_check` | §78 |
| AI output needs a confirming acceptance | `project_assertion_accountability_check` | AI-001 |
| An open critical question caps confidence | `*_confidence_cap` | METH-0001 §6.2 |
| A consequential conclusion needs competing hypotheses | `consequential_needs_hypothesis_set` | METH-0001 §7 |
| The asserter is never the reviewer | `review_second_party_check` | §83 |
| An argument is a human inference record | `argument_person_check` | DR-0036 |
| Nothing is edited in place | `make_append_only` | DR-0055 |

## The four METH-0001 rulings, made structural

DR-0085 recorded that two of the founder's rulings bound only as editorial
discipline because the schema could not carry them. Both are now enforced.

**§1.5 — consequence.** `consequence_limb` records *which* limb of the
three-part test fired, so the classification is reviewable: a later reader
can disagree with the reasoning rather than only with the verdict.

**§6.2 — the confidence cap.** An assertion with an unanswered critical
question cannot stand at `high`. Enforced by deferred constraint triggers on
both sides, so it holds whichever is written first.

**§7 — competing hypotheses.** A consequential conclusion without a linked
hypothesis set is refused, and a set needs at least two hypotheses with at
least one marked as a genuine alternative. The schema cannot detect a
strawman; review treats such a set as absent.

**§10.1 — review qualification.** `review_record` carries `unreviewed` as a
first-class state, and `publishable_conclusion` renders the qualification a
reader must see. It is a view rather than a column so it cannot drift out of
step with the reviews it summarizes.

## A design problem the tests found

The first version of the confidence cap refused to record a critical question
raised against an assertion already committed at `high`. That is the wrong
behaviour and it took a sabotage run to see it: **the archive would have been
refusing to hear an objection in order to protect a confidence claim** — the
worst available failure mode for an evidentiary system.

The cap now binds only a *live* claim. A late objection is admitted together
with a superseding assertion at `moderate`, atomically
(`raise_late_critical_question`). The original stands in the record at
whatever it claimed, because that is what the project held at the time and
rewriting it is what EVID-015 forbids. The objection is not refused; the
stale confidence is.

## What is deliberately absent

- **Any computed acceptability status on `argument`.** Formal semantics may
  run as analytic aids and their output is advisory (DR-0036, EVID-014). A
  column here would become the editor. `contested_conclusion` reports what
  is unanswered and adjudicates nothing.
- **A resolution for `§40`.** An attacked argument with no answer stays
  visibly contested. There is no step that makes a live objection go away.
- **Anything at `public` tier.** Everything Gate 2 produces is classified
  `internal` in `export/tiers.py` for one structural reason: Gate 3 does not
  exist, and OPS-001 forbids any path to a public surface without a recorded
  publication decision. When Gate 3 lands these become `join` rules following
  each conclusion's own decision.

## Verification

42 tests, each naming the requirement it verifies.

Every enforcement was checked by sabotage — removing the trigger and
confirming the suite fails:

| Sabotage | Tests that failed |
|---|---|
| AI-001 accountability trigger removed | 1 |
| Critical-question-side cap trigger removed | 1 |
| Hypothesis-set mandate removed | 1 |
| Reviewer identity check removed | 2 |
| Acceptance person check removed | 2 |
| Argument person check removed | 1 |

The cap's second trigger initially survived sabotage, which is what exposed
the design problem above: the case it protects — an objection raised in a
later transaction — was not being tested at all.

**Not verified here:** none of this has run against real archived material.
Every test builds its own fixtures. The gate is correct with respect to the
rules; whether the rules are workable in practice is a question only real
investigations answer, and METH-0001 §14 says so.
