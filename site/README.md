# site/

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

**One-time setup required** (repo admin, done once in the GitHub UI, not
something this workflow or any AI session can do): Settings → Pages → Source:
"GitHub Actions". Until that's set, the workflow will run but nothing will be
publicly reachable.

**Note on visibility:** once Pages is enabled, this content is visible on the
open internet, not restricted to any particular audience, unless the GitHub
organization has Enterprise Cloud's private-Pages feature enabled. Treat
anything added here as public before it's published, not after.

Keep it current with development: when a milestone lands (a source registered,
a phase closes, a review completes), update the relevant section and the "Last
updated" date in `index.html` in the same session, so the page never drifts far
from `README.md`'s "Where things stand, plainly" section.
