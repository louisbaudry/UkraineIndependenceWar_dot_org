# site/

**Live at <https://louisbaudry.github.io/UkraineIndependenceWar_dot_org/>.**

The project's public-facing progress briefing — a plain-language page for people
outside the project (currently: contacts in the Armed Forces of Ukraine) who want
to see what's being built without reading the governance and engineering
documents under `docs/`.

**This folder is deliberately isolated.** It is the only thing this repository
publishes to the open internet. Nothing under `docs/`, `schema/`, `collector/`,
etc. is served by the publish workflow, and nothing should be copied into this
folder without the same care taken over anything else shown outside the project.

## What it is not

- Not a Decision Record, SPEC, POL, REQ or METH document (DR-0046 document
  control does not apply here).
- Not evidentiary or archival content — no documentary assertions, no
  connection to Gate 1/2/3.
- Not the eventual public archive website referred to in Principle 18
  ("an archive first, a website last") — this is a briefing page, built ahead
  of that, on purpose, because there was a concrete need to show progress now.

## Maintaining it

Edit `index.html` directly and push to `main` (or merge a PR into it). There is
no build step, no template engine, no dependency — the file you edit is the file
that gets published. `.github/workflows/deploy-pages.yml` publishes `site/` to
GitHub Pages automatically on every push to `main` that touches this folder.

**One-time setup: done.** Settings → Pages → Source: "GitHub Actions" is set.
The first push-triggered run (2026-09-10) failed, and the repository does not
record why. The most likely cause is that this setting was not yet in place.
A manual re-run the same day succeeded, and so did the 2026-09-25 deploy. If the site ever stops updating, check this setting first:
it is a GitHub UI setting that no workflow or AI session can change.

**Note on visibility:** once Pages is enabled, this content is visible on the
open internet, not restricted to any particular audience, unless the GitHub
organization has Enterprise Cloud's private-Pages feature enabled. Treat
anything added here as public before it's published, not after.

Keep it current, but **only when the founder says so** (ruling of 2026-09-25,
recorded in `CLAUDE.md`, "Where state lives"). When a milestone lands (a source
registered, a phase closes, a review completes), the session asks whether the
page should be updated, naming what a public reader would notice. On a yes, it
updates the relevant section and the "Last updated" date in `index.html`. It
never changes the page unasked, because the page is the project's only public
voice.

## What the page contains

Rewritten from a five-section update into one detailed page on 2026-09-25
(PR #85). The sections are, in order: At a glance, What this is, Principles,
How it works, What is collected, Safeguards, Civilian harm & memorial,
Timeline, What's next, and Glossary. Each has an `id`, so it can be linked
directly (for example `#sources`).

**These parts go stale first**, so check them whenever a milestone lands:

- the **At a glance** counts: sources collected, pages preserved and the
  number of Decision Records;
- the **What is collected** table: a candidate that gets registered moves to
  "Collected", and a new candidate gets a row once it is verified;
- the **Timeline** and **What's next** lists;
- the **Last updated** date;
- the **Ukrainian and Russian pages**, which repeat all of the above and go
  stale whenever the English page changes without them (see "Languages").

## Languages

Added 2026-09-26 at the founder's direction (option B of four: Ukrainian and
Russian only, for now).

| Language | File | Address |
|---|---|---|
| English (reference) | `index.html` | `/` |
| Ukrainian | `uk/index.html` | `/uk/` |
| Russian | `ru/index.html` | `/ru/` |

English stays at the root so existing links keep working. Each file is a
complete, standalone page, with no build step, as before. Each has the same
section `id`s, so `#sources` works in every language. The stylesheet is
copied into each file, so a style change has to be made three times.

**English is the reference version.** Each translation opens with a notice that
says three things: it was translated with AI help, it has not yet been
reviewed by a native speaker, and which English "Last updated" date it
matches. Change the notice when a native speaker has reviewed a translation.
Until then, keep it.

**When the founder approves an update to the page:**

1. Update `index.html` first.
2. Update `uk/index.html` and `ru/index.html` the same way, and change the
   date their notice says they match.
3. If a translation can't be updated in the same change, leave it as it is.
   Its notice still names the older English date, so readers can see it's
   behind. Never change that date without also changing the text.

Words to handle with care:

- Keep the English meaning exactly. The same "claim vs. fact" line applies in
  every language.
- In Ukrainian, use Ukrainian terms, not Russian loan words.
- In Russian, write "в Украине" (the UN's form) and "Вторая война Украины за
  независимость". The page names Russia's war against Ukraine as plainly as the
  English does.
- In both translations, source names stay in their original form where
  readers would look them up: EUR-Lex, OFAC, SECO, "Denied Persons List",
  "Entity List". The Ukrainian register is written РНБО in Ukrainian and СНБО
  in Russian.

**Not yet done, and deliberately deferred:** French, German, Polish and
Crimean Tatar. Crimean Tatar would need a native reviewer and a choice of
script (Ukraine's official Latin alphabet). It waits on the founder.

## What must never appear on it

The page is on the open internet, and so is this repository (see
`CLAUDE.md`, "This repository is public"). Beyond that list, the page
deliberately leaves out: the archive server's hosting provider and any way to
reach it, the backup deferral (DR-0108) and other operational weak points,
the founder's name, any person's name, and the detail of the open legal
questions. The page says only that the review is pending. Source names and
row counts are fine. Rows are not.

## Checking a change before merging

There is no build step, so open `index.html`, `uk/index.html` and
`ru/index.html` in a browser. Check the language switcher links work in every
direction. Check it at phone
width (375px) as well as desktop, and in both light and dark mode. At 375px
there should be no sideways scrolling: `document.documentElement.scrollWidth`
should equal the window width. After merging, the deploy takes about a
minute. Confirm by fetching the live URL and checking the "Last updated"
date.
