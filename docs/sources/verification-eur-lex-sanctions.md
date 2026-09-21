# Verification record — EUR-Lex restrictive measures (Ukraine/Russia)

**Status:** Verification record for one candidate registration. Nothing
here is registered, nothing is collected into the project's archive, and
nothing is enacted by this document. Registering this candidate is the
founder's act (CLAUDE.md standing ruling) — the same standing ruling that
applies to the other six sanctions candidates.
**Verified:** 2026-09-20, ~19:00–19:10 UTC, from this session's container.
**Candidate:** `eur-lex-sanctions` in
[`sources/candidates/sanctions-authorities.yaml`](../../sources/candidates/sanctions-authorities.yaml).

Unlike the other six sanctions candidates, `eur-lex-sanctions`'s
`scope_rules` names a *category* of instrument ("Regulations, Council
Decisions and implementing acts under the Ukraine/Russia restrictive-measures
regimes, plus their consolidated versions"), not a single downloadable list.
This record identifies the specific instruments the candidate's `locator`
(the bare `https://eur-lex.europa.eu/` root) resolves to, since "identifying
a specific legal instrument or decision set" was flagged in README.md as
editorial/legal judgment a session could not attempt alone — this record
proposes candidates for founder review, it does not decide the question.

## 1. What was done, in order

1. Confirmed `eur-lex.europa.eu` is reachable from this session (`curl`,
   200) — worth recording because network access varies by session
   (CLAUDE.md), and a prior session's A2 work found other EU-adjacent hosts
   unreachable on different days.
2. Identified the two foundational legal instruments for the EU's
   Ukraine/Russia territorial-integrity sanctions regime, matching the
   candidate's `scope_rules` and `coverage_start` (2014-03-01, the first
   Crimea-related measures):
   - **Council Regulation (EU) No 269/2014**, CELEX `32014R0269` — the
     regulation imposing the restrictive measures, whose Annex I is the
     actual list of designated persons/entities.
   - **Council Decision 2014/145/CFSP**, CELEX `32014D0145` — the CFSP
     decision establishing the same measures, which the regulation
     implements.
   Both titles confirmed directly from EUR-Lex's own page `<title>`
   elements ("Regulation - 269/2014", "Decision - 2014/145").
3. Found each instrument's **current consolidated version** — EUR-Lex
   republishes a dated consolidated CELEX (`02014R0269-YYYYMMDD` /
   `02014D0145-YYYYMMDD`) each time an amendment takes effect, rather than
   requiring a reader to apply amendments by hand. As fetched this session,
   the current consolidated dates were **2026-08-07** for both instruments
   (`CELEX:02014R0269-20260807`, `CELEX:02014D0145-20260807`) — the
   candidate's own comment block already notes this pattern for
   `eu-consolidated-list` ("consolidated versions...collected as derivatives
   alongside the originals, never in place of them," DR-0038).
4. Fetched the regulation's current consolidated text three times
   (`.../legal-content/EN/AUTO/?uri=CELEX:02014R0269-20260807`, following
   its 302 redirect to the `TXT` view) — 200, 8 677 685 bytes each time,
   identical byte count all three fetches.
5. **The three fetches were not byte-identical**, unlike every other
   sanctions candidate verified so far. A `diff` isolated the difference to
   four `_csrf` hidden-form-field values embedded in the page — a
   per-request CSRF token EUR-Lex's application generates, not a content
   change. Everything outside those four tokens was identical across all
   three fetches. **This is a real caveat for the eventual collector run,
   not a blocker**: a naive whole-file digest comparison across two fetches
   of the same consolidated CELEX will show a false difference even when
   the legal text has not changed, which none of the other six sanctions
   candidates' capture formats need to account for.
6. **Rehearsal**, matching the seco-sanctions precedent (§1.6 of that
   record). A throwaway PostgreSQL database was built from `schema/0*.sql`.
   The source was inserted directly, matching the BIS/OFSI/SECO rehearsals'
   approach. The real `Collector` (`collector/pipeline.py`, two-agent split
   per DR-0097, `ensure_software_agent`) was run with the real
   `HttpFetcher` against both consolidated-text URLs, into a throwaway OCFL
   root. `collector_run` read back: **2 discovered, 2 acquired, 0 failed,
   16 196 543 bytes preserved.** Zero documentary assertions — confirmed
   structurally, not just by row count: this schema has no
   `documentary_object` table for a collector run to write into in the
   first place. Database and storage then destroyed.

## 2. The instruments

| | Regulation | Decision |
| --- | --- | --- |
| CELEX (base) | `32014R0269` | `32014D0145` |
| CELEX (current consolidated, as fetched 2026-09-20) | `02014R0269-20260807` | `02014D0145-20260807` |
| Locator | `https://eur-lex.europa.eu/legal-content/EN/AUTO/?uri=CELEX:02014R0269-20260807` | `https://eur-lex.europa.eu/legal-content/EN/AUTO/?uri=CELEX:02014D0145-20260807` |
| Size (this session) | 8 677 685 bytes | not separately measured (rehearsal totalled both) |
| Response | 302 → 200 (redirects to the dated `TXT` view) | same pattern |
| Content stability | Text stable across 3 fetches; a `_csrf` form token differs per fetch | not separately isolated |

**On the dated CELEX suffix.** The consolidated-version date (`20260807`
here) advances each time the Council amends the regime — this project has
observed it amended roughly monthly over 2025–2026 from the list of
available consolidated dates on the regulation's own page (20260807,
20260717, 20260615, 20260511, 20260423, 20260316, ...). **A `run_locator`
pinned to today's dated CELEX will go stale** the next time the Council
amends the regime; whether to re-verify and update the locator per
amendment, or to point at a to-be-confirmed "latest consolidated version"
redirect if EUR-Lex offers one, is a registration-time judgment call, not
resolved here.

## 3. What this does and does not settle

**Settled by this record:** the two instruments exist, match the
candidate's `scope_rules`, are reachable from at least this session, and a
real `Collector` run against them succeeds cleanly with zero documentary
assertions, matching every other sanctions candidate's rehearsal.

**Settled 2026-09-21:** the founder confirmed both instruments belong in
`run_locators` (over the Regulation alone), matching this record's original
reading of the candidate's `scope_rules` ("Regulations" and "Council
Decisions" both named).

**Settled 2026-09-21:** the founder confirmed both instruments belong in
`run_locators` (over the Regulation alone), matching this record's original
reading of the candidate's `scope_rules` ("Regulations" and "Council
Decisions" both named). Re-verification cadence for the dated CELEX suffix
is also settled: **manual, before each collection run** — a person
re-fetches EUR-Lex, finds the current dated CELEX, and updates
`run_locators`, the same agent-of-record model every other source uses
(DR-0093 §3), rather than new tooling to auto-resolve "latest consolidated
version." `locator_verified: 2026-09-20` in the candidate file records when
this session's fetch happened, not a guarantee the locator stays current
past that date.

**Not settled, and not this session's to settle:**
- Registration itself, as with all seven candidates, per the standing
  ruling that this is the founder's act, per source.

## Sources

- [`sources/candidates/sanctions-authorities.yaml`](../../sources/candidates/sanctions-authorities.yaml) — `eur-lex-sanctions` entry
- [`docs/sources/verification-seco-sanctions.md`](verification-seco-sanctions.md) — the verification-record template this follows
- [`docs/decision-records/DR-0097-collection-run-two-agents.md`](../decision-records/DR-0097-collection-run-two-agents.md) — the two-agent split exercised in this rehearsal
- `README.md`, "Open decisions for the next session," item 3 — the original flagging of this candidate as founder-guided work
