# DR-0094 — Third-party web captures (Common Crawl, Wayback Machine, and qualifying archives) as an acquisition channel

**Category:** architecture / preservation | **Status:** Approved | **Decided:** 2026-09-11 by founder/principal editor | **Origin:** discussion on Common Crawl for source archiving | **Supersedes:** — | **Superseded by:** —

## AI provenance

Drafted by Claude (model: `claude-sonnet-5`) at the founder's request, following
the one-question-at-a-time process this project's working instructions
require. Five choices were put to the founder in sequence, each with named
options and a stated recommendation; the founder selected the recommended
option each time. No source material beyond this repository's own records
and general knowledge of Common Crawl and the Wayback Machine was used.

**Approved 2026-09-11**, after a second round of four questions the drafted
text had left open, put to the founder one at a time with named options and
a recommendation each: whether a loss-triggered retrieval needs a per-instance
human step (ruled: no, automatic is fine when scoped to the failed locator);
whether a future archive needs its own DR or can qualify by stated criteria
(ruled: criteria — against the drafting recommendation to name archives only);
whether third-party retrieval should block on the DR-0006 WACZ evaluation
(ruled: no, proceeds independently); and how to record all three in this
document (ruled: amend the text itself and approve in the same step, rather
than approving the original draft unchanged or leaving it Proposed). §§2, 1,
and Consequences below, and this note, reflect those four rulings.

**Numbered out of sequence.** Drafted on a branch cut before 2026-09-09 and
assigned DR-0087 at the time, unaware that a separate, already-merged branch
had taken DR-0087…0093 for the public-identifier scheme and the first source
registrations the same day. Renumbered to the next free slot, DR-0094, only
when this branch was reconciled against `origin/main` — the same collision
CLAUDE.md's onboarding notes now warn every session to check for before
drafting a DR.

## Context

Record §9 allows a source's escalation to a higher preservation tier to
trigger "retrospective recovery from external archives," and names
"archived webpages" among the continuous-collection sources at §8. No
Decision Record has yet governed what such recovery means: whether a
retrieval from Common Crawl or the Wayback Machine is collection from that
archive, or collection from the site the archive captured, and how the
retrieved record relates to the project's own captures of the same locator
under DR-0074's capture-series model.

Common Crawl publishes monthly, sampled web crawls since 2008 as WARC files
on public cloud storage, indexed by URL and domain, requiring no account to
read. The Wayback Machine offers point-in-time captures further back and
denser for many sites, reached differently (per-capture retrieval rather
than bulk WARC/index files) but raising the same provenance questions. Both
are third-party captures of pages the project did not itself fetch, made by
crawlers this project does not operate, with rights resting in the original
publisher rather than the archive.

DR-0071(a) refuses collection from unregistered sources outright. DR-0006
requires WARC as the capture format for high-value web sources — both
archives supply exactly that format (Common Crawl natively; the Wayback
Machine's captures are drawn from the same underlying model). DR-0008
forbids any documentation that reads as an overstated custody claim.
DR-0028 requires source dependence to be declared, not assumed.

## Alternatives considered

1. **Acquisition channel for already-registered sources** — a third-party
   capture of a page belonging to a registered source is collection *from
   that source*, by a channel other than a live fetch; rights, tier, and
   scope follow the origin source's registry entry (chosen).
2. **Register each archive as a source in its own right** (rejected:
   misattributes material to the archive rather than the original
   publisher, and forces rights/retention decisions onto Common Crawl's or
   the Internet Archive's terms rather than the origin site's, when the
   content copyright never left the origin publisher).
3. **Defer any decision until the fetch layer is proven live** (rejected:
   record §9 already anticipates this use, and the schema gap identified
   below — a fetch result and acquisition record built for one-locator,
   one-agent, one-timestamp captures — is cheaper to close before real
   holdings exist than after).

## Decision

### 1. Third-party captures are an acquisition channel, not a source

A retrieval from Common Crawl, the Wayback Machine, or **any archive
meeting the qualifying criteria below** is collection *from the registered
source that published the original page*, using a channel other than a
live fetch of that source's own site. DR-0071(a)'s registration requirement
is satisfied by the origin source's registration; the archive itself is
never separately registered as a source. The origin source's rights
assessment, default access tier, and retention policy govern the recovered
material, because the underlying content's copyright rests with the
original publisher, not with the archive that copied it.

**Qualifying criteria for a third-party archive**, decided directly rather
than by naming archives one at a time: it (a) supplies a record of an
original HTTP response — a WARC record or an equivalent capture of headers
and payload as served, not a re-rendering or a summary; (b) requires no
live crawling of new URLs by this project, only retrieval of records the
archive already made; and (c) leaves rights with the original publisher
rather than the archive itself. Common Crawl and the Wayback Machine both
qualify on their face. A future archive that meets all three needs no new
DR to use under this decision; one that fails any of them is out of scope
here regardless of how similar it otherwise looks, and needs its own DR.

### 2. Retrieval is triggered by escalation or recorded loss, scoped per source

Per §9 and DR-0068, a third-party-archive retrieval happens only when:

- a source is escalated to a higher retention tier and its registry entry
  states a backfill scope for that escalation, or
- a locator has a recorded failed acquisition (§28, PRES-007) and recovery
  from a third-party archive is attempted as the documented follow-up.

Bulk backfill of every registered source's full third-party-archive history
is out of scope for this decision. A registry entry may state a scope for
backfill (date range, path prefix) at the point a human configures it, but
retrieval is never a blanket default triggered by registration alone —
consistent with §9's warning not to archive everything equally.

**The loss-triggered case may run automatically, with no separate human
step, because the failure itself fixes the scope.** DR-0071(a) requires
collection to have human-configured scope; for a recorded failed
acquisition, that scope is exactly the one locator that already failed —
nothing wider is authorized, and nothing about which locator to try is left
to the collector's judgment. This is decided directly, not left to whoever
builds the `acquisition_attempt`/`FetchResult` extension: the collector may
attempt third-party recovery for a failed locator on a registered source
without a human approving that specific attempt. It may not attempt
recovery for any locator that has not itself recorded a failure, and it may
not widen the attempt beyond that locator. The recovered holding still goes
through Gate 1 and, if admitted, ordinary Gate 2 review like any other
acquisition — this decision concerns only whether the *attempt* needs
prior human sign-off, not whether its output is trusted uncritically.

### 3. Same capture series, capturing agent recorded

A third-party capture of a locator joins that locator's existing capture
series (DR-0074, Memento pattern per DR-0023) as its own holding, not a
derivative of any project-made capture and not a separate series. The
acquisition record for a third-party capture carries fields a project-made
capture does not need:

- the **capturing agent** (the archive, e.g. `common-crawl` or
  `wayback-machine`), distinct from the pipeline agent that performed the
  retrieval;
- the **original capture time**, which precedes the retrieval's attempted
  time, often by years;
- the **archive record locator** (e.g. the WARC record's offset and file,
  or the Wayback Machine timestamped URL), alongside the page's own locator.

`acquisition_attempt` and `FetchResult` (`collector/fetch.py`) are built for
a single locator, a single project agent, and a capture time equal to the
attempt time. Both need a schema and type extension before a third-party
retrieval can be recorded honestly. That extension is a consequence of this
decision, not part of it — implemented separately once this DR is approved.

### 4. Custody wording

Per DR-0008, the holding's custody history records that the *original*
capture was made by the third-party archive's own crawler, at its own
time, and that the project's custody begins at retrieval. No wording may
read as if the project captured the page itself. The archive's capture is
documented custody history, labeled as such; it is never elevated to a
legal chain-of-custody claim.

### 5. Truncated records are admitted, flagged incomplete

Common Crawl truncates a payload above roughly one megabyte; a truncated
record is common for long sanctions-list pages and large PDFs. A truncated
third-party capture is **admitted as a holding at Gate 1**, with an
incompleteness flag and the captured byte length recorded, following the
same "partial acquisition, honestly labeled" handling record §28 already
gives other partial acquisitions. It is never silently treated as the
complete page, and it is never refused outright merely for being
incomplete — refusing it would forfeit exactly the sanctions-PDF material
this channel is most useful for.

### 6. Independence is not assumed

A third-party capture and a project capture of the same page are two
observations of what the server sent, at different times, by different
means. DR-0028 still applies: whether they count as independent
corroboration of any proposition drawn from the page is a researched
conclusion, never a default, and the fact that one came from a third-party
archive does not by itself establish independence from the other content
on which any assertion relies.

## Consequences

- `acquisition_attempt` (`schema/03-pipeline.sql`) and `FetchResult`
  (`collector/fetch.py`) require a capturing-agent field, an original
  capture time distinct from attempted time, an archive record locator,
  and a truncation/incompleteness flag. This is tracked as follow-up
  implementation work, not enacted by this DR.
- A source's registry entry (DR-0067) gains an optional backfill-scope
  field for third-party-archive recovery, populated only when a human
  configures it at escalation or after a recorded loss.
- "What did this page say on date D" (§86, §90) can be answered from a
  single capture series regardless of who made the capture, while the
  capturing agent stays visible in that series' own records.
- No holding may ever read as though the project performed a capture it
  did not. Publication and API wording (DR-0008's constraint) must reflect
  the capturing agent on any third-party holding it surfaces.
- **The two trigger cases are authorized differently, and this DR is explicit
  about which.** Escalation-triggered backfill is *not* authorized by this DR
  alone: it still needs a human to configure a backfill scope on the source's
  registry entry under DR-0067, per source, before anything is retrieved.
  Loss-triggered recovery for one already-failed locator *is* authorized by
  this DR directly (§2), with no further per-instance human step, because the
  failure itself is the scope. A reader must not assume either case's rule
  applies to the other.
- A future archive meeting §1's qualifying criteria may be used under this
  DR without a new Decision Record; one that does not meet them needs its
  own DR regardless of how similar it looks to Common Crawl or the Wayback
  Machine. Whoever adds a third archive to the collector's configuration
  checks the criteria, not just the archive's reputation.
- **Third-party retrieval proceeds independently of DR-0006's WACZ signing
  evaluation.** That evaluation remains a standing Phase II task with no
  start date; it is not a precondition for using Common Crawl or the
  Wayback Machine under this DR. WACZ packaging, if adopted, can be applied
  to already-held WARC records later without redoing the retrieval — this
  decision does not wait on it, and does not need revisiting when WACZ is
  eventually evaluated.

## What has not been verified

This environment's egress proxy blocks both `commoncrawl.org` /
`index.commoncrawl.org` and `web.archive.org` (the same policy noted in
`docs/sources/candidate-war-sanctions-gur.md` for `web.archive.org`). No
query against either archive's index, no WARC record retrieval, and no
payload-digest verification has been performed in this environment. The
mechanics described above (index query, HTTP range request against a WARC
file, digest verification) reflect how each service is documented to work,
not a tested integration. Before any third-party-archive retrieval is
treated as working, it must be run against the live service in an
environment with network access.
