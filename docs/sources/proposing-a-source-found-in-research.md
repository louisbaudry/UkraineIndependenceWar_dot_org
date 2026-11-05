# Proposing a source found during research, and citing what the archive holds

A working note (2026-11-05), not a Decision Record, not a policy, and not an
authorisation to collect. It describes how a source that someone comes across
while doing their own research on the war becomes a candidate for this
archive, and how a holding of the archive can be cited by anyone once it
exists. It restates rules that are already enacted; where it and a DR differ,
the DR wins.

## Why

Much of what the archive should preserve is first met by someone reading
about the war for another purpose. That reading can feed the archive without
the archive collecting anything new: the person names a publisher, the
archive decides whether to register it, and from then on the archive holds
the bytes and the reader can cite them. Collection stays registered,
scoped and decided one source at a time (DR-0067, DR-0071(a)); open-web
crawling stays excluded.

## From a found source to a registered one

1. **Is it a source, or an item?** The archive registers publishers with a
   lasting output (a monitoring mission, a prosecutor's office, a ministry, an
   international mission's reports), not single articles or posts. A single
   item is evidence that its publisher may be worth a candidate note.
2. **Write a candidate note** in this directory, following "What a candidate
   note should contain" in [`README.md`](README.md): identity, context,
   collection and preservation policy, access and sensitivity, rights, triage
   grade, declared dependence. State what was and was not verified.
   The note says why the publisher belongs in the archive. It names no
   outside project, research question or person who suggested it.
3. **Draft the candidate entry** in [`sources/candidates/`](../../sources/candidates/)
   against the DR-0067 schema, under the matching registration class
   (DR-0103), and record a verification note of the locators actually checked.
4. **Open a PR.** Drafting a candidate registers nothing.
5. **The founder decides and registers** it on the archive server
   (`sources/register.py --commit --only <key>`), and **runs the collection**
   (`collector/run.py --source <key>`), with a person as agent of record
   (DR-0093 §3). Each is its own act; approving one source authorises no
   other.

While DR-0072 stands (POL-0001 §10 review not yet recorded), collection at
scale is suspended and retrospective recovery from other web archives
(WP 3.4 Track B) does not start. A found source can still be noted and
drafted.

## Personal data

A source whose output names private individuals is drafted under DR-0071(b)
and POL-0001 §4, and the civilian-harm rulings of DR-0109 and DR-0112 where
they apply: no automatic structuring of personal data, and no name published
before DR-0072's successor is approved.

## Citing a holding

Once a source has been collected, a reader outside the archive can cite a
holding by:

- **its public identifier**, the ARK of DR-0087 and SPEC-0007, once minted.
  No ARK exists yet: the project's NAAN has not been issued (SPEC-0007 §11);
- **until then**, the source key, the capture time and the content's
  **SHA-256**, which the OCFL inventory records in its fixity block for every
  preserved object (`collector/pipeline.py`).

The checksum lets a reader who saved a copy elsewhere tell whether it is the
same bytes. It matches only for byte-identical content: a file such as a PDF
usually matches; an HTML page saved by a browser rarely matches the body the
collector fetched, and a source captured as WARC (DR-0006) wraps the response
in a WARC record. A matching checksum says the bytes are the same; it is not a
claim of legal chain of custody (DR-0008, LEGAL-007).

Nothing flows back into the archive from whoever cites it.

## AI provenance

Drafted by an AI assistant (Anthropic Claude Code agent session) at the
founder's request. Checked against `docs/sources/README.md`, the
`sources/register.py` and `collector/run.py` arguments, the SHA-256 fixity
in `collector/pipeline.py`, and SPEC-0007's NAAN status as of this date.
Not checked against the archive server.
