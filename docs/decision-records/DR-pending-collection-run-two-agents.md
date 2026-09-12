# DR-pending-collection-run-two-agents — A collection run carries two agents: a human agent of record and a versioned software agent on its preservation events

**Category:** architecture / preservation | **Status:** Approved | **Decided:** 2026-09-12 by founder/principal editor | **Origin:** DR-0093 §3's open tension, raised as three named options with a recommendation | **Supersedes:** — | **Superseded by:** —

## AI provenance

Drafted by Claude (model: `claude-sonnet-5`) after the founder chose option 1
of three put to them, following this project's one-question-at-a-time
process. No source material beyond this repository's own records was used.
The code change this DR authorises was written and verified (collector
suites green before and after, the new invariant shown to fail under
sabotage, `release/baseline.py --check` confirmed to pin `collector_version`
and `pipeline_version` from a real `collector/run.py` invocation) in the
same session, per CLAUDE.md's "Documents" convention that code implementing
a decision may land with it rather than waiting on a second round.

## Context

DR-0093 §3 deliberately made a person the agent of record for the project's
first two collection runs (2026-09-08/09) — a human-accountable choice for
runs the founder was performing directly. `collector_run.collector_agent_id`
and every `preservation_event` the run produced were all set to that one
person's `pipeline_agent` id, because `Collector.__init__` took exactly one
`collector_agent_id` and used it everywhere.

This left a real conflict, recorded in DR-0093's *Executed* section but not
resolved there: `release/baseline.py --check` requires `collector_version`
and `pipeline_version` to be pinned, and pins them by finding a **software**
`pipeline_agent` that has run (AI-002: "software agents carry their
version"). With every agent id a person's, no such row existed, and both
items showed `MISSING` after the first real collection — not because
nothing had run, but because what ran was attributed entirely to a human
who did not, in fact, compute any digest or write any byte.

Three options were put to the founder on 2026-09-09 (README's "Open
decisions for the next session") and answered on 2026-09-12.

## Alternatives considered

1. **Record two agents per run: the person stays the agent of record; a
   separate, versioned software agent is recorded on the run's preservation
   events** (chosen).
2. Derive the pinned version from the run configuration's recorded code
   commit instead of the agent registry (not chosen: sidesteps needing a
   software agent row, at the cost of `release/baseline.py` reading a
   different kind of fact than AI-002 describes — a commit is not a
   declared software version, and the two can diverge without either being
   wrong).
3. Make the software agent the agent of record and amend DR-0093 §3 (not
   chosen: reverses a deliberate founder ruling on human accountability for
   the first runs; CLAUDE.md's standing rulings say not to do this
   unilaterally, and nothing in this session's context makes it the
   founder's evident intent to reverse it now).

## Decision

**A collection run carries two agents, attributed to different facts about
the run, never merged into one:**

1. **The agent of record is unchanged and stays human where DR-0093 §3 put
   it.** `collector_run.collector_agent_id` and the Gate 1 admission
   decision (`quarantine_item.gate1_decided_by`) continue to name whoever
   `--agent` names — a person, unless `--allow-software-agent` is given.
   This DR does not touch either field or DR-0093 §3's rule.

2. **Every `preservation_event` a run produces names a separate, versioned
   software agent instead.** A fixity check, a virus check, an ingestion, a
   digest calculation — these are things the software mechanically did, and
   a person initiating the run did not personally perform them. Attributing
   them to the software that ran is the accurate PREMIS record, not merely
   a workaround for `release/baseline.py`.

3. **The software agent self-registers; nothing about it is a human
   decision.** Unlike a person agent (DR-0093 §3: a human is registered
   deliberately, by name, as an accountable party), a software agent's
   identity is exhausted by its own declared `(name, version)` — there is
   nothing for a founder to decide about which row represents "collector
   version 0.1.0" beyond the code itself declaring that it is. The same
   `(name, version)` pair is reused across runs, never duplicated, so every
   run of the same code names the same agent row.

4. **One software agent serves both `collector_version` and
   `pipeline_version`.** `release/baseline.py`'s two dimensions (DR-0047)
   are conceptually distinct, but this codebase's `Collector` class
   performs both roles with no split between them — inventing two
   differently-versioned agents for one undivided piece of code would
   assert a distinction the code does not have. The agent is named
   `collector-pipeline` precisely so it matches both of `baseline.py`'s
   existing `name ILIKE '%collector%'` / `%pipeline%'` lookups without any
   change to that script.

5. **This governs `run()` (live collection); `ingest_warc()` (retrospective
   recovery) is unaffected here.** `ingest_warc()`'s callers may pass the
   same id for both agent parameters where the person/software distinction
   is not the point of what is being tested or run — this DR does not
   require every caller of `Collector` to exercise a real split, only that
   the two concepts exist as separate parameters and separate database
   facts.

## Consequences

- `Collector.__init__` takes two agent ids, `collector_agent_id` (agent of
  record) and `software_agent_id` (preservation events), both required —
  every construction site states both explicitly rather than one silently
  standing in for the other. `collector/run.py`, `collector/pipeline.py`'s
  `ensure_software_agent()`, and the collector test suites are updated in
  the same change.
- `release/baseline.py --check` now pins `collector_version` and
  `pipeline_version` from a real `collector/run.py` invocation without any
  change to `release/baseline.py` itself — the gap was in what the
  collector recorded, not in what the baseline tool looked for.
- DR-0093's own *Executed* section and the `collector_version`/
  `pipeline_version` `MISSING` result it reported describe a true past
  state and are not corrected retroactively; a fresh run after this change
  pins both.
- The two 2026-09-08/09 runs already recorded remain exactly as they are:
  every event on those runs still names the person, because this DR governs
  future runs, not a retroactive relabelling of historical preservation
  events (§77 supersession discipline extended to data, not just
  documents — correcting the past by rewriting who did what would itself be
  the kind of overclaim DR-0008 exists to prevent).
- README's "Open decisions for the next session" item on this tension is
  resolved and the Track A / A1 note is updated to reflect it.

## What was verified, and what was not

**Verified in this environment**, against a real PostgreSQL database:
`collector/tests/test_pipeline.py` (44 checks), `test_warc_ingest.py` (54
checks) and `test_run.py` (21 checks) all pass after the change. The new
invariant — a preservation event never names the run's agent of record — was
shown to fail under sabotage (reverting `_record_event` to the old single-
agent behaviour turned three checks red, restored and re-verified green).
`release/baseline.py --check` was run against the database `collector/run.py`
actually populated and confirmed `collector_version` and `pipeline_version`
both `pinned`, sourced from a `collector-pipeline` software agent that
`ensure_software_agent()` created with no human step.

**Not verified:** this is exercised against the test/rehearsal databases
this session created, not the archive server DR-0093 ran the real 2026-09-09
collection on. Running `collector/run.py` again for real (a third live
collection, or a re-run against `eu-consolidated-list`/`ofac-sdn`) would be
the first live confirmation that a software agent is created correctly
outside a test fixture.
