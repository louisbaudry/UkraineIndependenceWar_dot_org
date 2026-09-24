# Infrastructure overview

**Status:** Informal reference, not a Decision Record and not a controlled
document under DR-0046. It decides nothing and proposes no policy. It lists
what the project runs on, where each part is documented, and what is not
recorded yet. Where the facts are already in another file, this page links
to that file rather than copying it, because a second copy would go out of
date. If this page and a Decision Record disagree, the record is right and
this page needs fixing.
**Author:** AI assistant (Anthropic Claude Code agent session), at the
founder's direction, 2026-09-24.
**How it was compiled:** from the repository only, on `origin/main` at
`83810ed`. **No session has ever had shell access to the archive server**,
so anything about the server that the repository does not record is
marked **Unknown** below, not guessed. Filling those gaps in is the
founder's job, or the job of a session the founder runs on the server.

---

## 1. The picture

```
                        ┌──────────────────────────────────────────┐
                        │ GitHub — louisbaudry/                    │
                        │   UkraineIndependenceWar_dot_org         │
                        │  • code, DRs, SPEC/POL/REQ/METH (main)   │
                        │  • Actions → GitHub Pages (site/ only)   │
                        └──────┬───────────────┬───────────────────┘
               git push /      │               │ deploy-pages.yml
               pull requests   │               ▼
                               │     ┌──────────────────────┐
  ┌────────────────────────┐   │     │ Public briefing page │
  │ AI sessions (Claude    │◄──┤     │ (GitHub Pages)       │
  │ Code, cloud containers)│   │     └──────────────────────┘
  │ • edit the repo        │   │ git pull (by the founder)
  │ • throwaway Postgres   │   ▼
  │ • NO archive-server    │  ┌──────────────────────────────────────────┐
  │   access               │  │ Archive server — IONOS, Spain (DR-0100)  │
  └────────────────────────┘  │  • checkout of main, Python .venv        │
                              │  • PostgreSQL, database `uiw`            │
  ┌────────────────────────┐  │  • OCFL storage roots ~/uiw-archive      │
  │ Founder's own browser  │  │  • backups ~/uiw-backups (one-off so far)│
  │ • gets past Cloudflare │  └──────────────┬───────────────────────────┘
  │   where sessions can't │                 │ collector/run.py,
  └────────────────────────┘                 │ telegram_backfill.py
                                             ▼
                          Registered sources only (DR-0071(a)):
                          EUR-Lex, EU FSF, US Treasury (OFAC), OFSI, SECO,
                          t.me/s/… channels, …
```

Three kinds of machine touch the project, and **only one holds the
archive**:

- **The archive server** holds the preserved bytes and the canonical
  database. Everything evidential lives there.
- **GitHub** holds the code and the governance documents, and publishes
  one isolated page. It holds no archival content.
- **AI sessions** run in throwaway cloud containers. They edit the
  repository and test against their own temporary PostgreSQL. They have
  **never** had access to the archive server or its database. Every step
  on the server has been run by the founder, with a session proposing
  the commands (DR-0093 §3, DR-0105 *Executed*).

## 2. Components

### 2.1 Archive server

| Fact | Value | Source |
|---|---|---|
| Host | IONOS | DR-0100 Decision 3 |
| Country | Spain (EEA, so no Chapter V transfer question) | DR-0100, POL-0001 v1.2 §10 |
| Controller | The founder, as a natural person, until the association (DR-0104) legally exists and takes over | DR-0100 Decision 2, DR-0104 |
| Processor contract (GDPR Art. 28) with IONOS | **Outstanding administrative check** — no record that it has been done | CLAUDE.md standing rulings |
| Operating system | Debian-family (required by `setup/install.sh`). **Distribution and version: Unknown** | `setup/install.sh` |
| Control panel (Plesk/cPanel) | **Unknown.** The installer warns if it finds one | `setup/install.sh` |
| Hostname / IP address | **Unknown** — deliberately left out of the repository, which is public on GitHub. Record it somewhere private | — |
| Code checkout | Tracks `main` since 2026-09-21. Before that it was on a stale branch, which caused the schema drift in §3.2 | DR-0105 *Executed* §2 |
| Python | A `.venv` in the checkout. **It must be activated**, or `psycopg` is missing (`ModuleNotFoundError`, 2026-09-21) | DR-0105 *Executed* §2 |
| Database | PostgreSQL, database `uiw`. The session role is `root`; `postgres` is the superuser, needed for reloads (§3.2). **PostgreSQL version: Unknown** (14+ required) | DR-0105, `setup/install.sh` |
| Storage | OCFL roots under `~/uiw-archive`: separate `permanent` and `medium-term` roots, plus the quarantine directory | `storage/README.md`, DR-0073, DR-0076 |
| Registered sources | See `sources/README.md` and the DR register. This page does not keep a count, because it would go stale | — |

Installation follows [`setup/install.sh`](../setup/install.sh). It refuses
any path that looks web-served (`/var/www`, `httpdocs`, …), because the
archive holds material at every access tier (SEC-004).

### 2.2 GitHub

| Part | What it does | Source |
|---|---|---|
| Repository | Code and all governance documents. Changes go through `claude/<topic>` branches and founder-merged pull requests | CLAUDE.md "Git and pull requests" |
| GitHub Pages | Publishes `site/`, and only `site/`, on every push to `main` that touches it. **It is the project's only public web presence** | [`site/README.md`](../site/README.md), `.github/workflows/deploy-pages.yml` |
| Issue board | Proposed as the single home for project status, on the unmerged branch `claude/exciting-knuth-hbtdlh`. **Not adopted on `main`** | that branch |

There is **no CI test workflow**. The suites run only inside sessions and
on the server during install. Nothing on GitHub runs them on a push.

### 2.3 AI sessions

- Cloud containers, recreated for every session. PostgreSQL 16 is
  installed but stopped (CLAUDE.md "Environment notes").
- **Network access varies by session.** Some sessions reached
  `index.commoncrawl.org`/`web.archive.org`, others did not. Légifrance
  and `drs.nsdc.gov.ua` return anti-bot challenges to every session tried
  so far.
- **Scheduled Routines** (Claude Code triggers) send the founder
  reminders. The one on record is the quarterly revisit of
  `ua-nsdc-sanctions` (next 2026-10-01; `README.md`). A Routine only
  reminds. It runs no collection.

### 2.4 Founder's browser (human-assisted access)

Some publishers block automated clients (Cloudflare, anti-bot 403s). The
founder opens them in an ordinary browser and pastes back what
DevTools shows. This is how `ua-nsdc-sanctions` got its export URLs
confirmed (see [`docs/sources/verification-ua-nsdc-sanctions.md`](sources/verification-ua-nsdc-sanctions.md)).
It is a real part of the project's infrastructure. The confirmation step
cannot be automated, and a source that relies on it stays
blocked for scheduled collection until something changes.

### 2.5 Outbound traffic from the archive server

The server contacts **registered sources only** (DR-0071(a)). Open-web
crawling is excluded. One operational risk is recorded: the Telegram
historical backfill makes thousands of requests from the server's
single IP address. If Telegram blocks that IP, **every** Telegram
channel's collection stops, not only the backfill
([`docs/runbooks/telegram-channel-backfill.md`](runbooks/telegram-channel-backfill.md)).

## 3. Operations

### 3.1 Recurring jobs

| Job | Cadence defined | Actually scheduled on the server? |
|---|---|---|
| Collection runs (`collector/run.py`) | OPS-001 wants automatic collection. DR-0093 §3 makes the first runs manual, with a person as agent of record | **No** — every run on record was started by hand |
| Fixity checks (`storage/fixity_schedule.py --run`) | Every 180 days for `permanent`, every 365 for `medium-term` (PRES-003) | **Unknown** — no cron job or timer is recorded |
| Backups | OPS-005: independent backups, an annual restore test | **Unknown** — see §3.3 |

### 3.2 Schema changes on a live database

The project **has no migration mechanism**. Suites drop the database and
rebuild it from `schema/0*.sql`, which cannot be done to a database that
holds real data. The one time the server needed a schema change (2026-09-21),
it was done as a full backup and reload: `pg_dump` full and data-only,
rebuild from DDL as `postgres`, reload the data, and compare row counts
before and after. [DR-0105 *Executed* §2](decision-records/DR-0105-eur-lex-sanctions-registration.md)
records every step and both obstacles. **A written runbook for next time
is an open founder decision**, not done.

Practical rule until then: **before running anything on the server after
pulling `main`, check whether `schema/` changed since the server's last
reload.** If it did, the server needs the same procedure before any
collection run.

### 3.3 Backups

- **Recorded:** one set of dumps (full and data-only) taken on
  2026-09-21 to `~/uiw-backups/`, **on the same server**.
- **Not recorded:** any regular backup, any copy off the server or with
  another provider (OPS-005 requires "infrastructure independent of the
  primary"), any backup of the OCFL roots, and any restore test.
- For now, the archive's bytes and its database exist on one machine
  with one provider.

### 3.4 Runbooks

Operator instructions for the server live in [`docs/runbooks/`](runbooks/):
[A7 storage/bandwidth measurement](runbooks/A7-storage-bandwidth-measurement.md)
(written, not executed) and [Telegram backfill](runbooks/telegram-channel-backfill.md).
Each DR that authorises a registration has its own *How to execute*
section.

## 4. Gaps, in one list

Each of these is either unknown to the repository or known not to be done.
None is decided here.

1. Server facts not recorded: OS version, PostgreSQL version, whether a
   control panel is present. The hostname and IP belong somewhere
   private, not in this public repository.
2. The Art. 28 processor contract with IONOS: status unknown.
3. No regular backups and no off-server copy recorded (OPS-005 unmet as
   far as the repository shows).
4. No fixity schedule recorded as actually running (PRES-003).
5. No runbook for schema changes on the live database (DR-0105 open
   decision).
6. No CI: tests do not run on GitHub.
7. One IP address for all Telegram collection (runbook risk).

## 5. Keeping this page current

Update this page in the same commit as any change to what the project runs
on: a new host or provider, a new scheduled job, a backup arrangement, a
new publishing channel, a change of checkout branch on the server. A change
of hosting country is also a POL-0001 §11 material change and needs its own
recorded review (DR-0100). Updating this page does not replace that review.
