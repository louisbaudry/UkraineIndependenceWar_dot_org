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
- the **Last updated** date.

## What must never appear on it

The page is on the open internet, and so is this repository (see
`CLAUDE.md`, "This repository is public"). Beyond that list, the page
deliberately leaves out: the archive server's hosting provider and any way to
reach it, the backup deferral (DR-0108) and other operational weak points,
the founder's name, any person's name, and the detail of the open legal
questions. The page says only that the review is pending. Source names and
row counts are fine. Rows are not.

## Checking a change before merging

There is no build step, so open `index.html` in a browser. Check it at phone
width (375px) as well as desktop, and in both light and dark mode. At 375px
there should be no sideways scrolling: `document.documentElement.scrollWidth`
should equal the window width. After merging, the deploy takes about a
minute. Confirm by fetching the live URL and checking the "Last updated"
date.
