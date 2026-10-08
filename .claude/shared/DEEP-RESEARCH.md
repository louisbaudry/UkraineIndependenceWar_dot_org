# Rules for deep research with external AI tools

> Applies whenever Louis (or a session on his behalf) asks Perplexity,
> Gemini, ChatGPT or any other external tool to produce deep research, on
> any subject. Read with [`UNIVERSAL.md`](UNIVERSAL.md) and
> [`NON-CODING.md`](NON-CODING.md). A repo's own `CLAUDE.md` may add
> handling rules for its subject; it should not weaken these.

## 1. What goes into the prompt

- **Public-source question only.** The prompt states a question that could
  be asked by anyone. It carries no requester, no purpose, no tasking, no
  client or person names, no private-repo content and no internal
  identifiers. If context is needed, generalise it first.
- Where a repo is private and its subject is sensitive, the prompt is
  checked against that repo's rules before it is sent. When unsure whether
  something identifies a person, a client or a project, leave it out and
  ask.
- Never paste a prior AI report into a new prompt as if it were source
  material. Cite the underlying sources instead.

## 2. Required structure of every prompt

Every deep-research prompt contains these four parts.

1. **Scope block.**
   - Question, in one or two sentences.
   - Date range (and the "as of" date the answer must reflect).
   - Jurisdictions or geographies in scope.
   - Exclusions: what not to cover.
2. **Primary sources first.** Official and original documents (laws,
   filings, standards, datasets, first-party statements) before secondary
   reports. Quotations are verbatim in the source language, with the
   translation marked as a translation.
3. **Labels on every statement.** The tool must tag each point as one of:
   - **Fact**: stated by a primary source, with the source.
   - **Attributed claim**: someone says so; name who, and where.
   - **Inference**: the tool's own reasoning, with the reasoning shown.
4. **Gaps and negative findings.** The tool lists what it searched for and
   did not find, what it could not access, and where it is unsure. A gap
   is reported, never filled.

Also ask for: every URL given in full, with the access date, and a
statement of which tool and model produced the report.

## 3. Handling the output

- **Everything is AI-assisted until verified.** Each finding carries one
  status: _verified in session_ (checked against the primary text),
  _AI-assisted_ (not yet checked) or _unverified lead_.
- **Verify every cited URL and quote against the source** before a finding
  is relied on: open the link, confirm the page, date and wording exist.
  Drop or flag any that fail. Check that a quote is verbatim and that a
  translation matches the original.
- Record what could not be checked (paywall, unreachable host, document
  not read) instead of leaving it implied.
- Never invent a URL, date, author, title, quote or statistic to repair a
  tool's output. Unknown means omit it or use a visible placeholder.
- Output enters the record as a proposal: a human decides before it counts
  as evidence or as a final finding.

## 4. Recording a run

For each run, note in the repo that holds the work: date, tool and model,
the prompt as sent (or a pointer to it), and the findings with their
status. Say which parts, if any, were verified and how.
