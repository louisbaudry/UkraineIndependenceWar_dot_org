# DR-0110 — Register the UN monitoring mission's monthly civilian-casualty update

**Category:** operations / preservation | **Status:** Approved | **Decided:** 2026-09-24 by founder/principal editor
**Origin:** the founder's ruling of 2026-09-24 ("Do register `un-hrmmu-protection-of-civilians`"), answering the question that closed the verification of issue #69 | **Supersedes:** — | **Superseded by:** —

> **AI provenance (§80).** Drafted 2026-09-24 by an AI assistant (Anthropic
> Claude Code agent session) at the founder's direction. The ruling is the
> founder's: it was put as a question with three options (register as
> drafted; register the English PDF only; wait for the Prosecutor General
> candidate) and a recommendation for the first, and the founder chose it.
> The wording, reasons and consequences below are the drafter's. Approval
> authorises the registration and the runs described below. **Both are
> executed on the archive server by the founder, per *How to execute*, and
> have not been executed by this record.** This session had no access to
> the archive server or its database.

## Context

[DR-0109](DR-0109-civilian-harm-and-memorial.md) Decision 5 fills the
civilian-harm area in three steps, each source a separate decision, and puts
UN monitoring first. The candidate `un-hrmmu-protection-of-civilians` (in
[`sources/candidates/civilian-harm.yaml`](../../sources/candidates/civilian-harm.yaml))
is the UN Human Rights Monitoring Mission in Ukraine's monthly "Protection of
Civilians in Armed Conflict" update. It was verified live on 2026-09-24 and
rehearsed through the real collector in a throwaway database (3 acquired,
0 failed, 8 651 549 bytes, digests identical to `curl`, 0 documentary
assertions). The full record is
[`verification-un-hrmmu-civilian-casualties.md`](../sources/verification-un-hrmmu-civilian-casualties.md),
merged to `main` in PR #78.

What registration takes on, in short:

- **Counts, no victims' names**, as DR-0109 expected. The PDFs carry two UN
  press officers' published contacts, one anonymous witness quote, and
  aftermath photographs with identifiable bystanders (POL-0001 §5.8, §5.9).
- **Rights unverified**: the candidate claims `may-preserve` and nothing
  more (§14).
- **Irregular file names**: each month's `run_locators` must be read off
  that month's landing page and committed to the candidate file before the
  run, the same obligation `eur-lex-sanctions` (DR-0105) carries.

### Relation to POL-0001 §10 and DR-0072

This is not the collection scale-up DR-0072 and the 2026-09-08 ruling
suspend. It registers one source with a configured scope: one monthly
edition, three named files, about 9 MB a month. No crawl, no discovery, no
link-following (DR-0071(a)). Nothing is structured: DR-0066 holds, and
DR-0109 Decision 4's rule that a person enters incident and person data
only by a reviewer's hand is unaffected.

## Alternatives considered

1. **Register as drafted** (chosen). Landing page plus English and
   Ukrainian PDFs each month. It is the source DR-0109 names first, and it
   carries little personal data.
2. **Register the English PDF only.** Smallest footprint, but it drops the
   Ukrainian edition DR-0109 Decision 9 favours and the landing page that
   carries the publication date. Not chosen.
3. **Wait for the Prosecutor General candidate and decide step 1
   together.** Not chosen: DR-0109 makes each source its own decision, and
   waiting would delay counts that are ready now.

## Decision

On approval:

1. **`un-hrmmu-protection-of-civilians` is registered** in the source
   registry, with its class `UN-international-civilian-harm` and the field
   values in the candidate file as of this record's approval, by
   `sources/register.py --commit --only un-hrmmu-protection-of-civilians`.
2. **A first collection run is authorised** against the verified run
   locators: the August 2026 edition's landing page and its English and
   Ukrainian PDFs. `--dry-run` first, then a real run.
3. **One run per later month is authorised**, each against that month's
   edition only, after a person has read that month's landing page, put its
   landing-page and PDF URLs into `run_locators`, set `locator_verified`,
   and committed the change. A month whose files cannot be found is
   recorded as not collected, not guessed at.
4. **Earlier editions are NOT authorised** by this record: the October 2023
   to July 2026 editions on `ukraine.ohchr.org` and the 2022–2023 updates on
   `www.ohchr.org`. Collecting them backward is a separate decision.
5. **The Russian edition is left out** until it resolves (the August link
   returns 404). Adding it later is an edit to `run_locators` within this
   record's scope, since it is the same edition in another language.
6. **Nothing from any run crosses Gate 2** (DR-0066, Principle 5). No
   figure is structured into incidents or harms until DR-0109
   Consequence 5's working paper and a Gate 2 decision.
7. The registration carries the obligations `register.py --dry-run`
   prints: permanent retention with DR-0005 fixity checking, reading
   capacity in Ukrainian at Gate 2, and the unverified `may-preserve` rights
   position, unchanged by this record.
8. **This decision is independent of every other pending registration**
   (the Prosecutor General, `ua-nsdc-sanctions-*`, `isw-orca`,
   `deepstatemap`). None is required, authorised or affected by it.

### How to execute

On the archive server, on current `main`. Reuse the person
`pipeline_agent` id from DR-0093's step 1.

```bash
# 1. register (idempotent per source since #62's fix)
python3 sources/register.py --check
python3 sources/register.py --dry-run --only un-hrmmu-protection-of-civilians
python3 sources/register.py --commit --dbname uiw \
        --agent <person agent id> --only un-hrmmu-protection-of-civilians

# 2. the first run: August 2026 edition
python3 collector/run.py --source un-hrmmu-protection-of-civilians \
        --dbname uiw --agent <agent id> --archive-root ~/uiw-archive --dry-run
python3 collector/run.py --source un-hrmmu-protection-of-civilians \
        --dbname uiw --agent <agent id> --archive-root ~/uiw-archive

# 3. see where the project now stands
python3 release/baseline.py --check --dbname uiw
python3 storage/measure.py --dbname uiw
```

Expected from step 2, if the publisher has not changed the files: 3
discovered, 3 acquired, 0 failed, about 8.65 MB, 0 documentary assertions,
with SHA-256 digests matching the verification record's §3.

For each later month: open
`https://ukraine.ohchr.org/en/reports/protection-of-civilians`, open the
new edition, copy its landing-page URL and the English and Ukrainian PDF
links into `run_locators`, set `locator_verified` to that day, run
`register.py --check`, commit, pull on the server, then repeat step 2.

## Consequences

1. The archive gains its first civilian-harm source: a verified-only,
   conservative count that other publishers cite. It gives DR-0109
   Decision 7 stage 2 (incident pages with counts, no names) its first
   material, once structuring is designed and Gate 3 approves pages.
2. **A monthly manual step exists.** Someone has to update `run_locators`
   each month. If nobody does, the source silently stops growing. The
   board, not this record, tracks whether it is being done.
3. **Each edition is kept whole beside the others.** Because HRMMU revises
   earlier totals, the archive will hold several different figures for the
   same past month, each dated to its edition. That is intended (DR-0030,
   DR-0109 Decision 4), and any later structuring must say which edition a
   figure came from.
4. Rights stay unverified. Citing figures with attribution is DR-0109's
   plan; reproducing text or photographs waits for Part B of the legal
   brief.

## Executed

**2026-09-25, on the archive server**, by the founder, per *How to
execute*, step by step with an AI assistant (Anthropic Claude Code agent
session) reading each output before the next step. The server was on
`main` at `4391ce0`. The person agent was `442c1d13-a3e3-4e87-a856-f278e5063b47`
(Louis Baudry), the one DR-0093 created.

1. **Registration.** `register.py --check`: 14 candidates validate.
   `--dry-run --only un-hrmmu-protection-of-civilians` described the one
   source in class `UN-international-civilian-harm` (retention permanent,
   access public, rights `may-preserve`, the three August 2026 run
   locators). A read-only query found no `(name, locator)` pair
   registered twice. `--commit` was run once and registered source
   **`03411054-022a-41d6-998d-5803429169be`**, `lifecycle_state` `active`,
   `capture_format` `http`, created 2026-09-25 14:48:42 UTC.
2. **First run, August 2026 edition.** `collector/run.py --dry-run` was
   clean. The real run was **`c72bf2df-cb39-44d9-97b5-c72dc2067c53`**:
   3 discovered, 3 acquired, 0 skipped, 0 failed, **8 651 549 bytes** in
   1.7 s, 0 documentary assertions. The software agent on its
   preservation events is `collector-pipeline` 0.1.0 (DR-0097).
3. **Digests** (SHA-256 of the quarantined bytes), against the
   verification record's §3:

   | File | Bytes | SHA-256 | Against the record |
   |---|---|---|---|
   | Landing page | 55 537 | `d15c961d8857f8ec9336f16c687009767754c7d63768a8ddb11502a383fa7ccf` | differs from the 2026-09-24 `ae550e50…`, and equals the 2026-09-25 re-fetch the record already notes: the page was edited, same size |
   | Ukrainian PDF | 4 193 477 | `dec34226801d19468c983e8d060994ce2bfd5428d25d3c61d60af57cfde6ab83` | identical |
   | English PDF | 4 402 535 | `a8ff316b6d44753bf5be6ccffddb6a9fedba166426132d8c10fe2b17f0dc425b` | identical |

4. **Checks.** `SELECT count(*) FROM documentary_assertion` = 0, so
   DR-0066 held. `storage/measure.py`: the new source shows 1 run, 3 items
   and 8 651 549 bytes preserved. The archive now totals 1 043 721 127
   bytes preserved across nine sources, and the duplication ratio is
   2.01x (the known undischarged-quarantine gap). `release/baseline.py
   --check` is unchanged: every item is pinned except `dataset_snapshot`,
   because no dump was supplied and no release is being made.

**Two slips in *How to execute*, recorded here rather than edited above:**

- `storage/measure.py` takes no `--dbname`. It reads the database from the
  libpq environment, so it was run as `PGDATABASE=uiw python3
  storage/measure.py --archive-root ~/uiw-archive`.
- The step-1 SQL an assistant supplied asked for a `status` column. The
  column is `lifecycle_state`. That was a query error only; nothing was
  written by it.

**Schema drift, found and not fixed.** The #62 fix (`de6bbe7`) added a
`source_identity_unique` constraint to `schema/03-pipeline.sql`. The live
database was built before it and does not carry it. Registration was
still safe, because `register.py` itself refuses a re-run (the code
half of #62 is live), and no duplicate existed. Bringing the live schema
up to date is issue #57's open decision, and this is a second instance
of it.

**Not done:** no earlier edition was collected, and nothing was structured
or published. The next run waits for the September 2026 edition and a
person's update of `run_locators` (Decision 3). Issue #82 carries the
monthly reminder.
