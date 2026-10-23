---
name: deep-research
description: Rules for asking Perplexity, Gemini, ChatGPT or any external AI tool for deep research, and for handling what it returns. Use when writing a deep-research prompt, sending one, or receiving, checking or recording such a report.
---

# Deep research with external tools

Source: `DEEP-RESEARCH.md` in the shared rules. Read with `UNIVERSAL.md`
and `NON-CODING.md`. A repo's own `CLAUDE.md` may add handling rules; it must
not weaken these.

## Prompt content

- Public-source question only: one anyone could ask. No requester, purpose,
  tasking, client or person names, private-repo content or internal
  identifiers. Generalise context first.
- In a private repo with a sensitive subject, check the prompt against that
  repo's rules before sending. If unsure whether something identifies a
  person, client or project, leave it out and ask.
- Never paste a prior AI report in as source material; cite its underlying
  sources.

## Prompt structure (all four parts, every time)

1. **Scope block:** the question in one or two sentences; date range and
   "as of" date; jurisdictions; exclusions.
2. **Primary sources first** (laws, filings, standards, datasets,
   first-party statements) before secondary reports. Quotes verbatim in the
   source language, translation marked as such.
3. **Label every statement:** Fact (primary source, cited), Attributed
   claim (who, where) or Inference (reasoning shown).
4. **Gaps and negative findings:** what was searched and not found, what
   was inaccessible, where unsure. Gaps are reported, never filled.

Also ask for every URL in full with access date, and which tool and model
produced the report.

## Handling the output

- Everything is AI-assisted until verified. Each finding gets one status:
  _verified in session_, _AI-assisted_ or _unverified lead_.
- Open every cited URL and confirm page, date and wording; check quotes are
  verbatim and translations match. Drop or flag failures.
- Record what could not be checked (paywall, unreachable host, unread
  document).
- Never invent a URL, date, author, title, quote or statistic to repair
  output; omit it or use a visible placeholder.
- Output is a proposal; a human decides before it counts as evidence.

## Recording a run

In the repo holding the work, note: date, tool and model, the prompt as sent
(or a pointer), and the findings with status, saying what was verified and
how.
