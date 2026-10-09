# Rules for non-coding repos

> Applies to repos that store non-code work on GitHub: documents,
> research, content, translations, notes, datasets. Read after
> [`UNIVERSAL.md`](UNIVERSAL.md), which holds the rules common to every repo
> (communication, git and PRs, tracking, public-repo safety). A repo's own
> `CLAUDE.md` may narrow these.

## Before calling work done

- **Pass the docs gate in `UNIVERSAL.md`** before the PR: the `Docs:` line
  in the PR body. Content changes most often leave stale indexes, READMEs,
  glossaries and the backlog entry.
- There is no test suite, so review is the check. Re-read the whole change
  as a diff and report what you checked: facts against sources, figures
  against the data, links that resolve, formatting that renders.
- Say what was not checked (an unreachable source, an unread attachment,
  a rendering you could not see).
- If a check fails, fix the content. Don't weaken a style or consistency
  rule to make it pass.

## Sources and facts

- Every claim that could be wrong carries its source, or is marked as
  unsourced. Never invent URLs, dates, authors, titles, quotes or
  statistics; unknown means omit it or use a visible placeholder.
- Keep originals (source files, raw data, client-supplied text) separate
  from derived work, and never edit an original in place. Derived files
  say what they were derived from.
- A quote is verbatim or it is a paraphrase, and it is labelled as one.

## Structure and format

- Follow the repo's existing layout, naming and template. Propose a new
  structure; don't improvise one inside a content change.
- Prefer plain, diffable formats (Markdown, CSV, plain text) over binary
  ones. Where a binary file is required, say why and keep the editable
  source next to it.
- One file or topic per change where possible, so a reviewer can read the
  diff. Mechanical changes (renames, reformatting, bulk edits) go in their
  own commit, apart from content changes.

## Editing other people's work

- Change what was asked. Don't rewrite tone, terminology or structure
  beyond the brief; flag what you would change and let Louis decide.
- Keep terminology consistent with the repo's `GLOSSARY.md` (rule in
  `UNIVERSAL.md`) or existing usage. Where two terms collide, ask; don't
  pick silently.
- Translations and summaries keep meaning first: flag ambiguities and
  omissions in the PR instead of smoothing them over.

## Confidentiality

- Non-coding repos are the most likely to hold client or personal
  material. Before any push, check the repo's visibility and apply the
  public-repo rules in `UNIVERSAL.md` literally: names, emails, client
  documents, memories and glossaries stay out of public repos entirely.
- When unsure whether something identifies a person or a client, leave it
  out and ask.

## Deep research with external tools

- Asking Perplexity, Gemini or another tool for deep research follows
  [`DEEP-RESEARCH.md`](DEEP-RESEARCH.md): public-source prompts only, a
  required prompt structure, and verification before anything counts.

## AI output in content

- Model output (a draft, translation, extraction, classification,
  summary) is a proposal. Mark it as AI-assisted where the repo supports
  it; a human decides before it counts as final or as evidence.
