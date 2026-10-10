# DR-pending-kyiv-oblast-telegram-registration — Register the Kyiv Oblast administration's Telegram channel

**Category:** operations / preservation | **Status:** Proposed — both rulings made 2026-10-10; the record itself awaits the founder's approval; nothing is enacted | **Decided:** — 
**Origin:** DR-0109 Decision 5, step 2; the founder chose Kyiv Oblast as the first channel on 2026-10-09 | **Supersedes:** — | **Superseded by:** —

> **AI provenance (§80).** Drafted 2026-10-09 by an AI assistant (Anthropic
> Claude Code agent session). The only founder ruling behind it is the choice
> of Kyiv Oblast as the first channel (2026-10-09) and, on 2026-10-10, the
> two rulings below, each put as a question with three options and a
> recommendation; on both the founder chose the recommended option. The
> wording, reasons and consequences are the drafter's. The record itself is
> not yet approved. Approval would authorise the registration and runs
> described, **executed on the archive server by the founder** per *How to
> execute*; this record executes nothing and this session cannot reach the
> archive server.

## Context

[DR-0109](DR-0109-civilian-harm-and-memorial.md) Decision 5 puts the regional
administrations' Telegram channels second, each source a separate decision, and
says step 2 (about two dozen channels) is weighed against the DR-0072
suspension of collection at scale. This record is the first and only channel
of step 2 and does not decide the others.

The candidate is `ua-oda-kyiv-oblast-telegram` in
[`sources/candidates/civilian-harm.yaml`](../../sources/candidates/civilian-harm.yaml),
class `UA-regional-administration-telegram`. Its provenance is the
administration's own site, `koda.gov.ua`, which links `t.me/kyivoda` (verified
2026-10-09; record in
[`verification-ua-regional-administration-telegram.md`](../sources/verification-ua-regional-administration-telegram.md)).
In the sample, 13 of 20 visible posts mention strikes, casualties or damage and
none carried an age-like victim detail, but a sample of 20 is not an audit.

### The finding that shapes this decision

The public preview shows only the newest posts. On 2026-10-09 the 20 visible
posts spanned **2 h 20 min** (17:16 to 19:37 UTC, message ids 60721 to 60740).
**A daily run would keep about 20 posts of a day's output and lose the rest.**
The same is true of every channel in the class. kpszsu and generalstaffzsu
were backfilled by paging `?before=<message_id>` (DR-0106, DR-0107), which
works here too but is a separate, larger act than registering.

### Relation to POL-0001 §10 and DR-0072

One registered source with a configured scope, no crawl and no discovery
(DR-0071(a)). Not the scale-up DR-0072 suspends **if** it stays one channel;
whether step 2 as a whole is, is a separate ruling. Nothing is structured
(DR-0066, DR-0071(b)); posts may name victims, so nothing is published and no
person is entered (DR-0109 Decisions 4 and 7).

## Alternatives considered

**A. Access tier** (the candidate is drafted `private-preservation`, because
`register.py --check` refuses a public default for a source expecting graphic
content and the channel's media were not inspected):

1. **`private-preservation`** (chosen). Preserved, not exposed. Costs nothing
   now; a tier can be changed later by a recorded decision.
2. **`public`.** Refused by the registry while graphic content is expected;
   would need the expectation dropped after the media are inspected.
3. **`investigator-restricted`.** For access by named investigators. Premature
   with no investigator process built.

**B. How the first collection captures posts:**

1. **Daily preview run only** (cheapest). Keeps roughly the newest 20 posts a
   day. The archive would hold a thin sample while looking like a record.
2. **Daily preview run plus a one-off paginated backfill** (chosen), done as
   for DR-0106/0107. The backfill needs a person on the archive server and an
   operator-written loop (the project has none for this class), and its volume
   was not measured for this channel.
3. **Hourly preview runs.** Catches most posts going forward without a
   backfill, but needs a scheduled job on the server (`docs/infrastructure.md`
   records none for collection; a credential question).

## Decision

On approval:

1. **`ua-oda-kyiv-oblast-telegram` is registered** with its candidate field
   values at approval, by `register.py --commit --only ua-oda-kyiv-oblast-telegram`.
2. **Access tier: `private-preservation`** (ruling A, 2026-10-10).
3. **Collection: a first preview run, then a one-off paginated backfill**
   (ruling B, 2026-10-10). The founder sets the backfill's depth when it is
   run; its start, depth and volume are recorded in *Executed*, not guessed
   here.
4. **Scope:** the one locator `https://t.me/s/kyivoda` and its `?before=`
   pages. No other channel of this administration or its head, no media
   downloads beyond what the preview page itself carries, no link-following.
5. **Nothing crosses Gate 2** (DR-0066). No post is structured, no victim
   entered, nothing published. Before any structuring, a person reads the
   preserved posts for personal data.
6. **Independent of the other six candidates and every other pending
   registration.** Approving this does not authorise them.
7. Re-check before each run that `koda.gov.ua` still links the handle
   (impostor channels exist; see the verification record).

### How to execute

On the archive server, on current `main`, with `.venv` active, reusing the
person `pipeline_agent` id from DR-0093's step 1.

```bash
# 1. read-only: provenance and a look at the preview
curl -s -A "UIW-collector/0.1" https://koda.gov.ua/ | grep -o 't\.me/[A-Za-z0-9_]*' | sort -u
curl -s -o /dev/null -w "%{http_code} %{size_download}\n" -A "UIW-collector/0.1" https://t.me/s/kyivoda

# 2. register
python3 sources/register.py --check
python3 sources/register.py --dry-run --only ua-oda-kyiv-oblast-telegram
python3 sources/register.py --commit --dbname uiw \
        --agent <person agent id> --only ua-oda-kyiv-oblast-telegram

# 3. first run, then the backfill chosen under B
python3 collector/run.py --source ua-oda-kyiv-oblast-telegram \
        --dbname uiw --agent <agent id> --archive-root ~/uiw-archive --dry-run
python3 collector/run.py --source ua-oda-kyiv-oblast-telegram \
        --dbname uiw --agent <agent id> --archive-root ~/uiw-archive

# 4. where the project stands
PAGER=cat psql -d uiw -c "SELECT count(*) FROM documentary_assertion;"
PGDATABASE=uiw python3 storage/measure.py --archive-root ~/uiw-archive
python3 release/baseline.py --check --dbname uiw
```

Expected: step 1 shows `t.me/kyivoda` and 200; step 3 is 1 discovered,
1 acquired, 0 failed, about 110 KB, 0 documentary assertions.

## Consequences

1. The archive gains the first regional per-incident feed, beside the national
   counts of DR-0110 and DR-0111. Counts stay per source (DR-0112).
2. **The backfill is what makes this a record.** Without it, a daily preview
   run would keep a sample of each day's posts (alternative B1).
3. Posts may carry victims' names and media. Preserved privately; the legal
   position is untested (§14, POL-0001 §10).
4. **The backfill needs a loop the project does not yet have for this class,**
   written and run by a person on the archive server; the board, not this
   record, tracks it.
5. Rights stay unverified. A channel can change its handle or be replaced; the
   provenance re-check (Decision 7) is part of every run.

## Open questions for the founder

None. Both rulings are made; what remains is approving this record.

*Executed:* not executed.
