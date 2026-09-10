# DR-0087 — Third-party web captures (Common Crawl, Wayback Machine) as an acquisition channel

**Category:** architecture / preservation | **Status:** Proposed | **Decided:** — | **Origin:** discussion on Common Crawl for source archiving | **Supersedes:** — | **Superseded by:** —

## AI provenance

Drafted by Claude (model: `claude-sonnet-5`) at the founder's request, following
the one-question-at-a-time process this project's working instructions
require. Five choices were put to the founder in sequence, each with named
options and a stated recommendation; the founder selected the recommended
option each time. No source material beyond this repository's own records
and general knowledge of Common Crawl and the Wayback Machine was used.
Nothing here is enacted: this DR is a **candidate**, unapproved, until the
founder marks it Approved (§80, DR-0046).

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

A retrieval from Common Crawl, the Wayback Machine, or a comparable
third-party web archive is collection *from the registered source that
published the original page*, using a channel other than a live fetch of
that source's own site. DR-0071(a)'s registration requirement is satisfied
by the origin source's registration; the archive itself is never separately
registered as a source. The origin source's rights assessment, default
access tier, and retention policy govern the recovered material, because
the underlying content's copyright rests with the original publisher, not
with the archive that copied it.

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
- This DR does not itself authorize retrieving from Common Crawl or the
  Wayback Machine against any specific registered source; per-source
  backfill scope remains a registry decision under DR-0067, taken by a
  human, per source.
- **Not addressed here:** the WACZ signing evaluation DR-0006 already
  requires as a standing Phase II task, which may bear on how a
  third-party WARC record is packaged once retrieved. That evaluation is
  unaffected by this decision and proceeds on its own timeline.

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
